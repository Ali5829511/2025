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
import plate_recognizer
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

# ==================== Plate Recognition API ====================

@app.route('/api/plate-recognizer/status', methods=['GET'])
@auth.require_auth
def plate_recognizer_status():
    """Get Plate Recognizer API status"""
    try:
        status = plate_recognizer.get_api_status()
        return jsonify(status)
    except Exception as e:
        app.logger.error(f'Plate recognizer status error: {str(e)}')
        return jsonify({
            'success': False,
            'error': str(e),
            'error_ar': 'خطأ في التحقق من حالة الخدمة'
        }), 500

@app.route('/api/plate-recognizer/recognize', methods=['POST'])
@auth.require_auth
def recognize_plate():
    """Recognize license plate from uploaded image"""
    try:
        # Check if image is provided
        if 'image' not in request.files and 'base64_image' not in request.json:
            return jsonify({
                'success': False,
                'error': 'No image provided',
                'error_ar': 'لم يتم تقديم صورة'
            }), 400
        
        regions = request.form.get('regions', 'sa').split(',') if 'image' in request.files else None
        if request.json and 'regions' in request.json:
            regions = request.json['regions']
        
        # Handle file upload
        if 'image' in request.files:
            image_file = request.files['image']
            
            # Read image bytes
            image_bytes = image_file.read()
            
            # Recognize plate
            result = plate_recognizer.recognize_plate_from_bytes(image_bytes, regions)
        
        # Handle base64 image
        elif request.json and 'base64_image' in request.json:
            base64_image = request.json['base64_image']
            result = plate_recognizer.recognize_plate_from_base64(base64_image, regions)
        
        else:
            return jsonify({
                'success': False,
                'error': 'Invalid request',
                'error_ar': 'طلب غير صالح'
            }), 400
        
        # If recognition was successful, log it and check against database
        if result.get('success') and result.get('results'):
            for plate_data in result['results']:
                plate_number = plate_data['plate']
                confidence = plate_data['confidence']
                
                # Find vehicle in database
                vehicle = plate_recognizer.find_vehicle_by_plate(plate_number)
                
                # Log recognition
                vehicle_id = vehicle['id'] if vehicle else None
                plate_recognizer.log_plate_recognition(
                    request.user['id'],
                    plate_number,
                    confidence,
                    vehicle_id
                )
                
                # Add vehicle info to result
                plate_data['vehicle_info'] = vehicle
        
        # Log audit
        database.log_audit(
            request.user['id'],
            'Plate recognition performed',
            ip_address=request.remote_addr
        )
        
        return jsonify(result)
    
    except Exception as e:
        app.logger.error(f'Plate recognition error: {str(e)}')
        return jsonify({
            'success': False,
            'error': str(e),
            'error_ar': 'خطأ في تمييز اللوحة'
        }), 500

@app.route('/api/plate-recognizer/history', methods=['GET'])
@auth.require_auth
def plate_recognition_history():
    """Get plate recognition history"""
    try:
        # Get query parameters
        limit = request.args.get('limit', 50, type=int)
        offset = request.args.get('offset', 0, type=int)
        
        conn = database.get_db_connection()
        cursor = conn.cursor()
        
        # Get recognition history with user and vehicle info
        cursor.execute('''
            SELECT 
                p.*,
                u.username,
                u.name as user_name,
                v.plate_number as registered_plate,
                v.make,
                v.model,
                r.name as owner_name,
                r.unit_number
            FROM plate_recognition_log p
            LEFT JOIN users u ON p.user_id = u.id
            LEFT JOIN vehicles v ON p.vehicle_id = v.id
            LEFT JOIN residents r ON v.owner_id = r.id
            ORDER BY p.recognized_at DESC
            LIMIT ? OFFSET ?
        ''', (limit, offset))
        
        rows = cursor.fetchall()
        
        # Get total count
        cursor.execute('SELECT COUNT(*) FROM plate_recognition_log')
        total = cursor.fetchone()[0]
        
        conn.close()
        
        history = [dict(row) for row in rows]
        
        return jsonify({
            'success': True,
            'history': history,
            'total': total,
            'limit': limit,
            'offset': offset
        })
    
    except Exception as e:
        app.logger.error(f'Plate recognition history error: {str(e)}')
        return jsonify({
            'success': False,
            'error': str(e),
            'error_ar': 'خطأ في جلب سجل التمييز'
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

# ==================== System Statistics ====================

@app.route('/api/system/stats')
def system_stats():
    """Get system statistics for validation report"""
    try:
        conn = database.get_db_connection()
        cursor = conn.cursor()
        
        # Get counts for each table
        stats = {}
        
        # Buildings
        cursor.execute('SELECT COUNT(*) FROM buildings')
        stats['buildings'] = cursor.fetchone()[0]
        
        # Residents
        cursor.execute('SELECT COUNT(*) FROM residents')
        stats['residents'] = cursor.fetchone()[0]
        cursor.execute('SELECT COUNT(*) FROM residents WHERE is_active = 1')
        stats['activeResidents'] = cursor.fetchone()[0]
        
        # Vehicles
        cursor.execute('SELECT COUNT(*) FROM vehicles')
        stats['vehicles'] = cursor.fetchone()[0]
        cursor.execute('SELECT COUNT(*) FROM vehicles WHERE is_active = 1')
        stats['activeVehicles'] = cursor.fetchone()[0]
        
        # Traffic violations
        cursor.execute('SELECT COUNT(*) FROM traffic_violations')
        stats['violations'] = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM traffic_violations WHERE status = 'مفتوحة' OR status = 'open'")
        stats['openViolations'] = cursor.fetchone()[0]
        
        # Security incidents
        cursor.execute('SELECT COUNT(*) FROM security_incidents')
        stats['securityIncidents'] = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM security_incidents WHERE status = 'مفتوحة' OR status = 'open'")
        stats['openIncidents'] = cursor.fetchone()[0]
        
        # Visitors
        cursor.execute('SELECT COUNT(*) FROM visitors')
        stats['visitors'] = cursor.fetchone()[0]
        
        # Complaints
        cursor.execute('SELECT COUNT(*) FROM complaints')
        stats['complaints'] = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM complaints WHERE status = 'مفتوحة' OR status = 'open'")
        stats['openComplaints'] = cursor.fetchone()[0]
        
        # Users
        cursor.execute('SELECT COUNT(*) FROM users')
        stats['users'] = cursor.fetchone()[0]
        cursor.execute('SELECT COUNT(*) FROM users WHERE is_active = 1')
        stats['activeUsers'] = cursor.fetchone()[0]
        
        # Active sessions
        cursor.execute('SELECT COUNT(*) FROM sessions WHERE expires_at > datetime("now")')
        stats['activeSessions'] = cursor.fetchone()[0]
        
        conn.close()
        
        return jsonify(stats)
        
    except Exception as e:
        app.logger.error(f'System stats error: {str(e)}')
        return jsonify({
            'error': 'Failed to get system statistics',
            'error_ar': 'فشل في الحصول على إحصائيات النظام'
        }), 500

# ==================== Health Check ====================

@app.route('/api/health')
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'database': 'connected'
    })

# ==================== Unified Dashboard API ====================

@app.route('/api/statistics')
def get_statistics():
    """Get statistics for unified dashboard"""
    try:
        conn = database.get_db()
        cursor = conn.cursor()
        
        stats = {}
        
        # Total residents
        cursor.execute('SELECT COUNT(*) FROM residents')
        stats['total_residents'] = cursor.fetchone()[0]
        
        # Total buildings
        cursor.execute('SELECT COUNT(*) FROM buildings')
        stats['total_buildings'] = cursor.fetchone()[0]
        
        # Total stickers
        cursor.execute('SELECT COUNT(*) FROM stickers')
        stats['total_stickers'] = cursor.fetchone()[0]
        
        # Total units (apartments)
        cursor.execute('SELECT COUNT(*) FROM apartments')
        stats['total_units'] = cursor.fetchone()[0]
        
        # Total parking spots
        cursor.execute('SELECT COUNT(*) FROM parking_spots')
        stats['total_parking'] = cursor.fetchone()[0]
        
        # Active violations
        cursor.execute("SELECT COUNT(*) FROM traffic_violations WHERE status = 'نشط' OR status = 'active'")
        stats['active_violations'] = cursor.fetchone()[0]
        
        conn.close()
        
        return jsonify({
            'success': True,
            'data': stats
        })
        
    except Exception as e:
        app.logger.error(f'Statistics error: {str(e)}')
        return jsonify({
            'success': False,
            'error': 'Failed to get statistics',
            'error_ar': 'فشل في الحصول على الإحصائيات'
        }), 500

@app.route('/api/violation-report')
def get_violation_report():
    """Get violation report with resident information"""
    try:
        conn = database.get_db()
        cursor = conn.cursor()
        
        # Get violations with resident information
        query = """
        SELECT 
            tv.plate_number,
            COUNT(tv.id) as violation_count,
            tv.vehicle_type,
            tv.processing_date,
            r.name as resident_name,
            r.building_number,
            r.unit_number
        FROM traffic_violations tv
        LEFT JOIN stickers s ON tv.plate_number = s.plate_number
        LEFT JOIN residents r ON s.resident_id = r.id
        GROUP BY tv.plate_number
        ORDER BY violation_count DESC, tv.processing_date DESC
        """
        
        cursor.execute(query)
        rows = cursor.fetchall()
        
        # Format the data
        violations = []
        for row in rows:
            violations.append({
                'plateNumber': row[0],
                'violationCount': row[1],
                'vehicleType': row[2],
                'processingDate': row[3],
                'residentName': row[4],
                'buildingNumber': row[5],
                'unitNumber': row[6]
            })
        
        conn.close()
        
        return jsonify({
            'success': True,
            'data': violations
        })
        
    except Exception as e:
        app.logger.error(f'Violation report error: {str(e)}')
        return jsonify({
            'success': False,
            'error': 'Failed to get violation report',
            'error_ar': 'فشل في الحصول على تقرير المخالفات'
        }), 500

@app.route('/api/residents')
def get_residents():
    """Get all residents with building info"""
    try:
        conn = database.get_db_connection()
        cursor = conn.cursor()
        
        building_id = request.args.get('building_id', type=int)
        is_active = request.args.get('is_active', type=int)
        
        query = '''
            SELECT r.id, r.name, r.national_id, r.email, r.phone, r.department, 
                   r.job_title, r.unit_number, r.move_in_date, r.move_out_date, 
                   r.is_active, b.name as building_name, b.building_number
            FROM residents r
            LEFT JOIN buildings b ON r.building_id = b.id
        '''
        
        conditions = []
        params = []
        
        if building_id:
            conditions.append('r.building_id = ?')
            params.append(building_id)
        
        if is_active is not None:
            conditions.append('r.is_active = ?')
            params.append(is_active)
        
        if conditions:
            query += ' WHERE ' + ' AND '.join(conditions)
        
        query += ' ORDER BY b.building_number, r.unit_number, r.name'
        
        cursor.execute(query, params)
        
        residents = []
        for row in cursor.fetchall():
            residents.append({
                'id': row[0],
                'name': row[1],
                'national_id': row[2],
                'email': row[3],
                'phone': row[4],
                'department': row[5],
                'job_title': row[6],
                'unit_number': row[7],
                'move_in_date': row[8],
                'move_out_date': row[9],
                'is_active': row[10],
                'building_name': row[11],
                'building_number': row[12]
            })
        
        conn.close()
        
        return jsonify({
            'success': True,
            'data': residents,
            'total': len(residents)
        })
        
    except Exception as e:
        app.logger.error(f'Residents API error: {str(e)}')
        return jsonify({
            'success': False,
            'error': 'Failed to load residents data',
            'error_ar': 'فشل في تحميل بيانات السكان'
        }), 500

@app.route('/api/apartments')
def get_apartments():
    """Get all apartments with building info"""
    try:
        conn = database.get_db_connection()
        cursor = conn.cursor()
        
        building_id = request.args.get('building_id', type=int)
        
        if building_id:
            cursor.execute('''
                SELECT a.id, a.unit_number, a.floor_number, a.unit_type, a.is_occupied,
                       b.name as building_name, b.building_number
                FROM apartments a
                JOIN buildings b ON a.building_id = b.id
                WHERE a.building_id = ?
                ORDER BY a.floor_number, a.unit_number
            ''', (building_id,))
        else:
            cursor.execute('''
                SELECT a.id, a.unit_number, a.floor_number, a.unit_type, a.is_occupied,
                       b.name as building_name, b.building_number
                FROM apartments a
                JOIN buildings b ON a.building_id = b.id
                ORDER BY b.building_number, a.floor_number, a.unit_number
            ''')
        
        apartments = []
        for row in cursor.fetchall():
            apartments.append({
                'id': row[0],
                'unit_number': row[1],
                'floor_number': row[2],
                'unit_type': row[3],
                'is_occupied': row[4],
                'building_name': row[5],
                'building_number': row[6]
            })
        
        conn.close()
        
        return jsonify({
            'success': True,
            'data': apartments,
            'total': len(apartments)
        })
        
    except Exception as e:
        app.logger.error(f'Apartments API error: {str(e)}')
        return jsonify({
            'success': False,
            'error': 'Failed to load apartments data',
            'error_ar': 'فشل في تحميل بيانات الشقق'
        }), 500

@app.route('/api/parking-spots')
def get_parking_spots():
    """Get all parking spots with building and apartment info"""
    try:
        conn = database.get_db_connection()
        cursor = conn.cursor()
        
        building_id = request.args.get('building_id', type=int)
        
        if building_id:
            cursor.execute('''
                SELECT p.id, p.spot_number, p.parking_area, p.is_occupied,
                       b.name as building_name, b.building_number,
                       a.unit_number
                FROM parking_spots p
                LEFT JOIN buildings b ON p.building_id = b.id
                LEFT JOIN apartments a ON p.apartment_id = a.id
                WHERE p.building_id = ?
                ORDER BY p.spot_number
            ''', (building_id,))
        else:
            cursor.execute('''
                SELECT p.id, p.spot_number, p.parking_area, p.is_occupied,
                       b.name as building_name, b.building_number,
                       a.unit_number
                FROM parking_spots p
                LEFT JOIN buildings b ON p.building_id = b.id
                LEFT JOIN apartments a ON p.apartment_id = a.id
                ORDER BY p.parking_area, p.spot_number
            ''')
        
        parking_spots = []
        for row in cursor.fetchall():
            parking_spots.append({
                'id': row[0],
                'spot_number': row[1],
                'parking_area': row[2],
                'is_occupied': row[3],
                'building_name': row[4],
                'building_number': row[5],
                'unit_number': row[6]
            })
        
        conn.close()
        
        return jsonify({
            'success': True,
            'data': parking_spots,
            'total': len(parking_spots)
        })
        
    except Exception as e:
        app.logger.error(f'Parking spots API error: {str(e)}')
        return jsonify({
            'success': False,
            'error': 'Failed to load parking spots data',
            'error_ar': 'فشل في تحميل بيانات المواقف'
        }), 500

@app.route('/api/buildings')
def get_buildings():
    """Get all buildings data"""
    try:
        conn = database.get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, name, building_number, address, total_units, total_floors, 
                   created_at, updated_at
            FROM buildings
            ORDER BY building_number
        ''')
        
        buildings = []
        for row in cursor.fetchall():
            buildings.append({
                'id': row[0],
                'name': row[1],
                'building_number': row[2],
                'address': row[3],
                'total_units': row[4],
                'total_floors': row[5],
                'created_at': row[6],
                'updated_at': row[7]
            })
        
        conn.close()
        
        return jsonify({
            'success': True,
            'data': buildings,
            'total': len(buildings)
        })
        
    except Exception as e:
        app.logger.error(f'Buildings API error: {str(e)}')
        return jsonify({
            'success': False,
            'error': 'Failed to load buildings data',
            'error_ar': 'فشل في تحميل بيانات المباني'
        }), 500

@app.route('/api/comprehensive-reports')
def get_comprehensive_reports():
    """Get comprehensive system reports data"""
    try:
        conn = database.get_db_connection()
        cursor = conn.cursor()
        
        reports = {}
        
        # Residents summary
        cursor.execute('SELECT COUNT(*) FROM residents WHERE is_active = 1')
        reports['totalResidents'] = cursor.fetchone()[0]
        
        cursor.execute('SELECT COUNT(*) FROM residents WHERE is_active = 0')
        reports['inactiveResidents'] = cursor.fetchone()[0]
        
        # Buildings summary
        cursor.execute('SELECT COUNT(*) FROM buildings')
        reports['totalBuildings'] = cursor.fetchone()[0]
        
        # Violations summary
        cursor.execute('SELECT COUNT(*) FROM traffic_violations')
        reports['totalViolations'] = cursor.fetchone()[0]
        
        cursor.execute("""
            SELECT COUNT(*) FROM traffic_violations 
            WHERE status IN ('pending', 'open', 'مفتوحة', 'معلقة')
        """)
        reports['openViolations'] = cursor.fetchone()[0]
        
        # Security incidents
        cursor.execute('SELECT COUNT(*) FROM security_incidents')
        reports['totalIncidents'] = cursor.fetchone()[0]
        
        cursor.execute("""
            SELECT COUNT(*) FROM security_incidents 
            WHERE status IN ('reported', 'open', 'مفتوحة')
        """)
        reports['openIncidents'] = cursor.fetchone()[0]
        
        # Complaints
        cursor.execute('SELECT COUNT(*) FROM complaints')
        reports['totalComplaints'] = cursor.fetchone()[0]
        
        cursor.execute("""
            SELECT COUNT(*) FROM complaints 
            WHERE status IN ('open', 'مفتوحة')
        """)
        reports['openComplaints'] = cursor.fetchone()[0]
        
        cursor.execute("""
            SELECT COUNT(*) FROM complaints 
            WHERE status IN ('resolved', 'محلولة', 'closed', 'مغلقة')
        """)
        reports['resolvedComplaints'] = cursor.fetchone()[0]
        
        # Vehicles and parking
        cursor.execute('SELECT COUNT(*) FROM vehicles WHERE is_active = 1')
        reports['activeVehicles'] = cursor.fetchone()[0]
        
        # Monthly occupancy trend (last 7 months)
        # TODO: Calculate from actual residents data when available
        reports['occupancyTrend'] = {
            'labels': ['يناير', 'فبراير', 'مارس', 'أبريل', 'مايو', 'يونيو', 'يوليو'],
            'data': [85, 87, 89, 91, 88, 90, 92]  # Mock data - requires residents data
        }
        
        # Violations by type
        cursor.execute("""
            SELECT violation_type, COUNT(*) as count
            FROM traffic_violations
            GROUP BY violation_type
            ORDER BY count DESC
            LIMIT 5
        """)
        violation_types = cursor.fetchall()
        reports['violationsByType'] = {
            'labels': [row[0] for row in violation_types] if violation_types else ['وقوف ممنوع', 'عكس سير', 'مواقف ذوي الاحتياجات', 'عدم التقيد بالإشارات'],
            'data': [row[1] for row in violation_types] if violation_types else [15, 12, 6, 5]
        }
        
        # Security incidents trend (last 7 months)
        # TODO: Group by month when sufficient data exists
        reports['securityTrend'] = {
            'labels': ['يناير', 'فبراير', 'مارس', 'أبريل', 'مايو', 'يونيو', 'يوليو'],
            'data': [8, 6, 10, 7, 9, 11, 12]  # Mock data - will be replaced with real aggregation
        }
        
        # Complaints trend
        # TODO: Calculate from actual complaints data with monthly grouping
        reports['complaintsTrend'] = {
            'labels': ['يناير', 'فبراير', 'مارس', 'أبريل', 'مايو', 'يونيو', 'يوليو'],
            'new': [25, 30, 28, 35, 32, 29, 31],  # Mock data
            'resolved': [23, 28, 26, 33, 30, 27, 29]  # Mock data
        }
        
        # Residents by building
        cursor.execute("""
            SELECT b.name, COUNT(r.id) as count
            FROM buildings b
            LEFT JOIN residents r ON b.id = r.building_id AND r.is_active = 1
            GROUP BY b.id, b.name
            ORDER BY count DESC
            LIMIT 4
        """)
        residents_by_building = cursor.fetchall()
        reports['residentsByBuilding'] = {
            'labels': [row[0] for row in residents_by_building] if residents_by_building else ['المبنى 1', 'المبنى 2', 'المبنى 3', 'الفلل'],
            'data': [row[1] for row in residents_by_building] if residents_by_building else [65, 58, 72, 50]
        }
        
        conn.close()
        
        return jsonify({
            'success': True,
            'data': reports
        })
        
    except Exception as e:
        app.logger.error(f'Comprehensive reports error: {str(e)}')
        return jsonify({
            'success': False,
            'error': 'Failed to load comprehensive reports data',
            'error_ar': 'فشل في تحميل بيانات التقارير الشاملة'
        }), 500

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
