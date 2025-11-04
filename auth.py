"""
Authentication module for Faculty Housing Management System
نظام المصادقة لنظام إدارة إسكان أعضاء هيئة التدريس
"""

import secrets
from datetime import datetime, timedelta
from functools import wraps
from flask import request, jsonify, session
import database

# Session configuration
SESSION_TIMEOUT_HOURS = 24

def generate_session_token():
    """Generate a secure random session token"""
    return secrets.token_urlsafe(32)

def create_session(user_id, ip_address=None, user_agent=None):
    """Create a new session for user"""
    conn = database.get_db_connection()
    cursor = conn.cursor()
    
    # Clean up old sessions for this user
    cursor.execute('DELETE FROM sessions WHERE user_id = ? AND expires_at < ?',
                  (user_id, datetime.now()))
    
    # Create new session
    session_token = generate_session_token()
    expires_at = datetime.now() + timedelta(hours=SESSION_TIMEOUT_HOURS)
    
    cursor.execute('''
        INSERT INTO sessions (user_id, session_token, expires_at, ip_address, user_agent)
        VALUES (?, ?, ?, ?, ?)
    ''', (user_id, session_token, expires_at, ip_address, user_agent))
    
    conn.commit()
    conn.close()
    
    return session_token, expires_at

def validate_session(session_token):
    """Validate a session token and return user if valid"""
    if not session_token:
        return None
    
    conn = database.get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT s.*, u.* FROM sessions s
        JOIN users u ON s.user_id = u.id
        WHERE s.session_token = ? AND s.expires_at > ? AND u.is_active = 1
    ''', (session_token, datetime.now()))
    
    result = cursor.fetchone()
    conn.close()
    
    if result:
        return dict(result)
    return None

def destroy_session(session_token):
    """Destroy a session"""
    conn = database.get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('DELETE FROM sessions WHERE session_token = ?', (session_token,))
    
    conn.commit()
    conn.close()

def cleanup_expired_sessions():
    """Remove all expired sessions"""
    conn = database.get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('DELETE FROM sessions WHERE expires_at < ?', (datetime.now(),))
    
    deleted = cursor.rowcount
    conn.commit()
    conn.close()
    
    return deleted

def require_auth(f):
    """Decorator to require authentication for routes"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        session_token = request.cookies.get('session_token')
        
        if not session_token:
            return jsonify({'error': 'Authentication required', 'error_ar': 'المصادقة مطلوبة'}), 401
        
        user = validate_session(session_token)
        if not user:
            return jsonify({'error': 'Invalid or expired session', 'error_ar': 'جلسة غير صالحة أو منتهية'}), 401
        
        # Add user to request context
        request.user = user
        return f(*args, **kwargs)
    
    return decorated_function

def require_role(*roles):
    """Decorator to require specific role(s) for routes"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            session_token = request.cookies.get('session_token')
            
            if not session_token:
                return jsonify({'error': 'Authentication required', 'error_ar': 'المصادقة مطلوبة'}), 401
            
            user = validate_session(session_token)
            if not user:
                return jsonify({'error': 'Invalid or expired session', 'error_ar': 'جلسة غير صالحة أو منتهية'}), 401
            
            if user['role'] not in roles and 'admin' not in roles:
                return jsonify({'error': 'Insufficient permissions', 'error_ar': 'صلاحيات غير كافية'}), 403
            
            # Add user to request context
            request.user = user
            return f(*args, **kwargs)
        
        return decorated_function
    return decorator
