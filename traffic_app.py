"""
Traffic Violations Management System
نظام إدارة المخالفات المرورية

Flask application for managing traffic violations with Plate Recognizer integration
"""
from flask import Flask, render_template, request, jsonify, send_from_directory
from flask_cors import CORS
import sqlite3
import os
from datetime import datetime
from werkzeug.utils import secure_filename
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__, static_folder='static', template_folder='templates')
CORS(app)

# Configuration
DATABASE_PATH = os.path.join(os.path.dirname(__file__), 'traffic.db')
UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'static', 'uploads', 'violations')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

# Plate Recognizer API Configuration
PLATE_RECOGNIZER_API_TOKEN = os.environ.get('PLATE_RECOGNIZER_API_TOKEN', '')
PLATE_RECOGNIZER_API_URL = 'https://api.platerecognizer.com/v1/plate-reader/'

# Create upload folder if it doesn't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def get_db_connection():
    """Get database connection"""
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def recognize_plate_from_file(image_path):
    """
    Recognize license plate using Plate Recognizer API
    تمييز رقم اللوحة باستخدام Plate Recognizer
    """
    if not PLATE_RECOGNIZER_API_TOKEN:
        return {'success': False, 'error': 'API token not configured'}
    
    try:
        with open(image_path, 'rb') as image_file:
            headers = {'Authorization': f'Token {PLATE_RECOGNIZER_API_TOKEN}'}
            files = {'upload': image_file}
            data = {'regions': ['sa']}  # Saudi Arabia region
            
            response = requests.post(
                PLATE_RECOGNIZER_API_URL,
                headers=headers,
                files=files,
                data=data,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                if result.get('results'):
                    plate_data = result['results'][0]
                    return {
                        'success': True,
                        'plate': plate_data.get('plate', '').upper(),
                        'confidence': plate_data.get('score', 0.0),
                        'region': plate_data.get('region', {}).get('code', '')
                    }
                else:
                    return {'success': False, 'error': 'No plate detected'}
            else:
                return {'success': False, 'error': f'API error: {response.status_code}'}
    
    except Exception as e:
        return {'success': False, 'error': str(e)}

@app.route('/')
def index():
    """Main page showing all violations with details"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT c.plate_number, c.owner_name, c.model, c.year, c.color,
               v.violation_type, v.violation_date, v.fine_amount, v.officer_name, v.image_path,
               v.violation_id
        FROM violations v
        JOIN cars c ON v.car_id = c.car_id
        ORDER BY v.violation_date DESC
    """)
    
    records = cursor.fetchall()
    conn.close()
    
    return render_template('traffic_violations_index.html', records=records)

@app.route('/api/violations')
def get_violations():
    """API endpoint to get all violations"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT c.plate_number, c.owner_name, c.model, c.year, c.color,
               v.violation_type, v.violation_date, v.fine_amount, v.officer_name, v.image_path,
               v.violation_id, v.car_id
        FROM violations v
        JOIN cars c ON v.car_id = c.car_id
        ORDER BY v.violation_date DESC
    """)
    
    rows = cursor.fetchall()
    conn.close()
    
    violations = []
    for row in rows:
        violations.append({
            'plate_number': row['plate_number'],
            'owner_name': row['owner_name'],
            'model': row['model'],
            'year': row['year'],
            'color': row['color'],
            'violation_type': row['violation_type'],
            'violation_date': row['violation_date'],
            'fine_amount': row['fine_amount'],
            'officer_name': row['officer_name'],
            'image_path': row['image_path'],
            'violation_id': row['violation_id'],
            'car_id': row['car_id']
        })
    
    return jsonify({
        'success': True,
        'data': violations,
        'total': len(violations)
    })

@app.route('/api/cars')
def get_cars():
    """API endpoint to get all cars"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM cars ORDER BY plate_number')
    rows = cursor.fetchall()
    conn.close()
    
    cars = []
    for row in rows:
        cars.append({
            'car_id': row['car_id'],
            'plate_number': row['plate_number'],
            'owner_name': row['owner_name'],
            'model': row['model'],
            'year': row['year'],
            'color': row['color']
        })
    
    return jsonify({
        'success': True,
        'data': cars,
        'total': len(cars)
    })

@app.route('/api/upload-violation', methods=['POST'])
def upload_violation():
    """
    Upload violation image and optionally detect plate
    رفع صورة المخالفة واكتشاف اللوحة تلقائياً
    """
    if 'image' not in request.files:
        return jsonify({'success': False, 'error': 'No image provided'}), 400
    
    file = request.files['image']
    
    if file.filename == '':
        return jsonify({'success': False, 'error': 'No file selected'}), 400
    
    if file and allowed_file(file.filename):
        # Save file
        filename = secure_filename(file.filename)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        unique_filename = f"{timestamp}_{filename}"
        filepath = os.path.join(UPLOAD_FOLDER, unique_filename)
        file.save(filepath)
        
        # Relative path for database
        relative_path = f'/static/uploads/violations/{unique_filename}'
        
        # Try to recognize plate if API is configured
        plate_result = None
        if PLATE_RECOGNIZER_API_TOKEN:
            plate_result = recognize_plate_from_file(filepath)
        
        return jsonify({
            'success': True,
            'image_path': relative_path,
            'plate_recognition': plate_result
        })
    
    return jsonify({'success': False, 'error': 'Invalid file type'}), 400

@app.route('/api/add-violation', methods=['POST'])
def add_violation():
    """
    Add new violation to database
    إضافة مخالفة جديدة
    """
    data = request.get_json()
    
    # Required fields
    plate_number = data.get('plate_number')
    violation_type = data.get('violation_type')
    violation_date = data.get('violation_date')
    fine_amount = data.get('fine_amount')
    
    if not all([plate_number, violation_type, violation_date, fine_amount]):
        return jsonify({'success': False, 'error': 'Missing required fields'}), 400
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Check if car exists, if not create it
    cursor.execute('SELECT car_id FROM cars WHERE plate_number = ?', (plate_number,))
    car = cursor.fetchone()
    
    if not car:
        # Create new car entry
        cursor.execute('''
            INSERT INTO cars (plate_number, owner_name, model, year, color)
            VALUES (?, ?, ?, ?, ?)
        ''', (
            plate_number,
            data.get('owner_name', 'غير محدد'),
            data.get('model', 'غير محدد'),
            data.get('year'),
            data.get('color', 'غير محدد')
        ))
        car_id = cursor.lastrowid
    else:
        car_id = car['car_id']
    
    # Insert violation
    cursor.execute('''
        INSERT INTO violations (car_id, violation_type, violation_date, fine_amount, officer_name, image_path)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (
        car_id,
        violation_type,
        violation_date,
        fine_amount,
        data.get('officer_name', 'غير محدد'),
        data.get('image_path', '')
    ))
    
    conn.commit()
    violation_id = cursor.lastrowid
    conn.close()
    
    return jsonify({
        'success': True,
        'violation_id': violation_id,
        'message': 'Violation added successfully',
        'message_ar': 'تم إضافة المخالفة بنجاح'
    })

@app.route('/api/plate-recognizer/status')
def plate_recognizer_status():
    """Check Plate Recognizer API status"""
    if not PLATE_RECOGNIZER_API_TOKEN:
        return jsonify({
            'configured': False,
            'message': 'API token not configured',
            'message_ar': 'لم يتم تكوين رمز API'
        })
    
    try:
        headers = {'Authorization': f'Token {PLATE_RECOGNIZER_API_TOKEN}'}
        response = requests.get(
            'https://api.platerecognizer.com/v1/statistics/',
            headers=headers,
            timeout=10
        )
        
        if response.status_code == 200:
            stats = response.json()
            return jsonify({
                'configured': True,
                'connected': True,
                'message': 'API connection successful',
                'message_ar': 'تم الاتصال بنجاح',
                'usage': stats.get('usage', {}),
                'total_calls': stats.get('total_calls', 0)
            })
        else:
            return jsonify({
                'configured': True,
                'connected': False,
                'message': f'API error: {response.status_code}'
            })
    except Exception as e:
        return jsonify({
            'configured': True,
            'connected': False,
            'error': str(e)
        })

@app.route('/add-violation')
def add_violation_page():
    """Page for adding new violations"""
    return render_template('add_violation.html')

@app.route('/about')
def about_page():
    """About page with system information"""
    return render_template('about.html')

@app.route('/static/<path:filename>')
def serve_static(filename):
    """Serve static files"""
    return send_from_directory('static', filename)

if __name__ == '__main__':
    # Initialize database if it doesn't exist
    if not os.path.exists(DATABASE_PATH):
        print("Initializing database...")
        from init_traffic_db import init_traffic_database
        init_traffic_database()
    
    # Run server
    port = int(os.environ.get('PORT', 5001))
    debug = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    app.run(host='0.0.0.0', port=port, debug=debug)
