"""
Main Flask server for Faculty Housing Management System
خادم Flask الرئيسي لنظام إدارة إسكان أعضاء هيئة التدريس
"""

from flask import Flask, request, jsonify, send_from_directory, make_response, abort
from flask_cors import CORS
from werkzeug.security import safe_join
import os
import database
import auth
from datetime import datetime

# Initialize Flask app
app = Flask(__name__)
CORS(app, supports_credentials=True)

# Configuration
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
app.config['SESSION_COOKIE_SECURE'] = os.environ.get('FLASK_ENV') == 'production'
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'

# Base directory for serving files
BASE_DIR = os.path.abspath('.')

# Allowed file extensions
ALLOWED_EXTENSIONS = {'.html', '.css', '.js', '.png', '.jpg', '.jpeg', '.gif', '.svg', '.pdf', '.md'}

def is_safe_path(filename):
    """Check if the requested file is safe to serve"""
    if '..' in filename or filename.startswith('/'):
        return False
    
    blocked_files = {'.env', '.git', '__pycache__', 'requirements.txt', '.gitignore', '.py', '.db'}
    if any(blocked in filename for blocked in blocked_files):
        return False
    
    _, ext = os.path.splitext(filename)
    if ext.lower() not in ALLOWED_EXTENSIONS:
        return False
    
    return True

# Initialize database on startup
with app.app_context():
    database.init_database()

# ==================== Authentication Routes ====================

@app.route('/api/auth/login', methods=['POST'])
def login():
    """Login endpoint"""
    try:
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        
        if not username or not password:
            return jsonify({
                'success': False,
                'error': 'Username and password required',
                'error_ar': 'اسم المستخدم وكلمة المرور مطلوبان'
            }), 400
        
        # Verify credentials
        user = database.verify_user(username, password)
        
        if not user:
            # Log failed login attempt
            database.log_audit(
                None,
                f'Failed login attempt for username: {username}',
                ip_address=request.remote_addr
            )
            return jsonify({
                'success': False,
                'error': 'Invalid credentials',
                'error_ar': 'اسم المستخدم أو كلمة المرور غير صحيحة'
            }), 401
        
        # Create session
        session_token, expires_at = auth.create_session(
            user['id'],
            ip_address=request.remote_addr,
            user_agent=request.headers.get('User-Agent')
        )
        
        # Log successful login
        database.log_audit(
            user['id'],
            'User logged in',
            ip_address=request.remote_addr
        )
        
        # Create response
        response = make_response(jsonify({
            'success': True,
            'user': {
                'id': user['id'],
                'username': user['username'],
                'name': user['name'],
                'role': user['role'],
                'email': user['email']
            },
            'message': 'Login successful',
            'message_ar': 'تم تسجيل الدخول بنجاح'
        }))
        
        # Set session cookie
        response.set_cookie(
            'session_token',
            session_token,
            expires=expires_at,
            httponly=True,
            secure=app.config['SESSION_COOKIE_SECURE'],
            samesite=app.config['SESSION_COOKIE_SAMESITE']
        )
        
        return response
        
    except Exception as e:
        app.logger.error(f'Login error: {str(e)}')
        return jsonify({
            'success': False,
            'error': 'Internal server error',
            'error_ar': 'خطأ في الخادم'
        }), 500

@app.route('/api/auth/logout', methods=['POST'])
@auth.require_auth
def logout():
    """Logout endpoint"""
    try:
        session_token = request.cookies.get('session_token')
        
        if session_token:
            auth.destroy_session(session_token)
            
            # Log logout
            database.log_audit(
                request.user['id'],
                'User logged out',
                ip_address=request.remote_addr
            )
        
        response = make_response(jsonify({
            'success': True,
            'message': 'Logged out successfully',
            'message_ar': 'تم تسجيل الخروج بنجاح'
        }))
        
        # Clear session cookie
        response.set_cookie('session_token', '', expires=0)
        
        return response
        
    except Exception as e:
        app.logger.error(f'Logout error: {str(e)}')
        return jsonify({
            'success': False,
            'error': 'Internal server error',
            'error_ar': 'خطأ في الخادم'
        }), 500

@app.route('/api/auth/validate', methods=['GET'])
def validate():
    """Validate session endpoint"""
    try:
        session_token = request.cookies.get('session_token')
        
        if not session_token:
            return jsonify({
                'success': False,
                'authenticated': False
            }), 401
        
        user = auth.validate_session(session_token)
        
        if not user:
            return jsonify({
                'success': False,
                'authenticated': False
            }), 401
        
        return jsonify({
            'success': True,
            'authenticated': True,
            'user': {
                'id': user['id'],
                'username': user['username'],
                'name': user['name'],
                'role': user['role'],
                'email': user['email']
            }
        })
        
    except Exception as e:
        app.logger.error(f'Validation error: {str(e)}')
        return jsonify({
            'success': False,
            'error': 'Internal server error',
            'error_ar': 'خطأ في الخادم'
        }), 500

@app.route('/api/auth/change-password', methods=['POST'])
@auth.require_auth
def change_password():
    """Change password endpoint"""
    try:
        data = request.get_json()
        current_password = data.get('current_password')
        new_password = data.get('new_password')
        
        if not current_password or not new_password:
            return jsonify({
                'success': False,
                'error': 'Current and new password required',
                'error_ar': 'كلمة المرور الحالية والجديدة مطلوبة'
            }), 400
        
        # Verify current password
        user = database.verify_user(request.user['username'], current_password)
        if not user:
            return jsonify({
                'success': False,
                'error': 'Current password is incorrect',
                'error_ar': 'كلمة المرور الحالية غير صحيحة'
            }), 401
        
        # Update password
        success = database.update_user_password(request.user['id'], new_password)
        
        if success:
            # Log password change
            database.log_audit(
                request.user['id'],
                'Password changed',
                ip_address=request.remote_addr
            )
            
            return jsonify({
                'success': True,
                'message': 'Password changed successfully',
                'message_ar': 'تم تغيير كلمة المرور بنجاح'
            })
        else:
            return jsonify({
                'success': False,
                'error': 'Failed to change password',
                'error_ar': 'فشل تغيير كلمة المرور'
            }), 500
            
    except Exception as e:
        app.logger.error(f'Change password error: {str(e)}')
        return jsonify({
            'success': False,
            'error': 'Internal server error',
            'error_ar': 'خطأ في الخادم'
        }), 500

# ==================== Static File Serving ====================

@app.route('/')
def index():
    """Serve index page"""
    return send_from_directory('.', 'index.html')

@app.route('/<path:filename>')
def serve_static(filename):
    """Serve static files with security checks"""
    if not is_safe_path(filename):
        abort(403)
    
    safe_path = safe_join(BASE_DIR, filename)
    if safe_path is None or not os.path.isfile(safe_path):
        abort(404)
    
    return send_from_directory('.', filename)

# ==================== Health Check ====================

@app.route('/api/health')
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'database': 'connected'
    })

# ==================== Error Handlers ====================

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({
        'error': 'Resource not found',
        'error_ar': 'المورد غير موجود'
    }), 404

@app.errorhandler(403)
def forbidden(error):
    """Handle 403 errors"""
    return jsonify({
        'error': 'Access forbidden',
        'error_ar': 'الوصول ممنوع'
    }), 403

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    return jsonify({
        'error': 'Internal server error',
        'error_ar': 'خطأ في الخادم'
    }), 500

# ==================== Startup ====================

if __name__ == '__main__':
    # Cleanup expired sessions on startup
    auth.cleanup_expired_sessions()
    
    # Get configuration from environment
    debug_mode = os.environ.get('FLASK_DEBUG', 'True').lower() == 'true'
    port = int(os.environ.get('PORT', 5000))
    host = os.environ.get('HOST', '0.0.0.0')
    
    if debug_mode:
        print("=" * 60)
        print("⚠️  WARNING: Debug mode is enabled")
        print("⚠️  تحذير: وضع التصحيح مفعّل")
        print("⚠️  DO NOT use debug mode in production!")
        print("⚠️  لا تستخدم وضع التصحيح في بيئة الإنتاج!")
        print("=" * 60)
    
    app.run(host=host, port=port, debug=debug_mode)
