"""
Database module for Faculty Housing Management System
نظام قاعدة البيانات لنظام إدارة إسكان أعضاء هيئة التدريس
"""

import sqlite3
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
import os

DATABASE_PATH = os.path.join(os.path.dirname(__file__), 'housing.db')

def get_db_connection():
    """Create and return a database connection"""
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_database():
    """Initialize the database with required tables"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Users table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL,
        name TEXT NOT NULL,
        role TEXT NOT NULL,
        email TEXT,
        phone TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        last_login TIMESTAMP,
        is_active INTEGER DEFAULT 1
    )
    ''')
    
    # Sessions table for managing user sessions
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS sessions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        session_token TEXT UNIQUE NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        expires_at TIMESTAMP NOT NULL,
        ip_address TEXT,
        user_agent TEXT,
        FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
    )
    ''')
    
    # Buildings table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS buildings (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        building_number TEXT UNIQUE NOT NULL,
        total_floors INTEGER,
        total_units INTEGER,
        address TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    
    # Residents table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS residents (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        national_id TEXT UNIQUE NOT NULL,
        email TEXT,
        phone TEXT NOT NULL,
        department TEXT,
        job_title TEXT,
        building_id INTEGER,
        unit_number TEXT,
        move_in_date DATE,
        move_out_date DATE,
        is_active INTEGER DEFAULT 1,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (building_id) REFERENCES buildings (id)
    )
    ''')
    
    # Vehicles table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS vehicles (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        plate_number TEXT UNIQUE NOT NULL,
        owner_id INTEGER NOT NULL,
        vehicle_type TEXT,
        make TEXT,
        model TEXT,
        year INTEGER,
        color TEXT,
        sticker_number TEXT UNIQUE,
        sticker_issued_date DATE,
        sticker_expiry_date DATE,
        is_active INTEGER DEFAULT 1,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (owner_id) REFERENCES residents (id) ON DELETE CASCADE
    )
    ''')
    
    # Traffic violations table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS traffic_violations (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        vehicle_id INTEGER NOT NULL,
        violation_type TEXT NOT NULL,
        violation_date TIMESTAMP NOT NULL,
        location TEXT,
        description TEXT,
        fine_amount DECIMAL(10, 2),
        status TEXT DEFAULT 'pending',
        reported_by INTEGER,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (vehicle_id) REFERENCES vehicles (id),
        FOREIGN KEY (reported_by) REFERENCES users (id)
    )
    ''')
    
    # Complaints table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS complaints (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        resident_id INTEGER NOT NULL,
        category TEXT NOT NULL,
        title TEXT NOT NULL,
        description TEXT NOT NULL,
        priority TEXT DEFAULT 'medium',
        status TEXT DEFAULT 'open',
        assigned_to INTEGER,
        resolution TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        resolved_at TIMESTAMP,
        FOREIGN KEY (resident_id) REFERENCES residents (id),
        FOREIGN KEY (assigned_to) REFERENCES users (id)
    )
    ''')
    
    # Visitors log table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS visitors (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        visitor_name TEXT NOT NULL,
        visitor_national_id TEXT,
        visitor_phone TEXT,
        visiting_resident_id INTEGER NOT NULL,
        visit_date DATE NOT NULL,
        entry_time TIMESTAMP,
        exit_time TIMESTAMP,
        purpose TEXT,
        vehicle_plate TEXT,
        notes TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (visiting_resident_id) REFERENCES residents (id)
    )
    ''')
    
    # Security incidents table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS security_incidents (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        incident_type TEXT NOT NULL,
        incident_date TIMESTAMP NOT NULL,
        location TEXT NOT NULL,
        description TEXT NOT NULL,
        severity TEXT DEFAULT 'medium',
        status TEXT DEFAULT 'reported',
        reported_by INTEGER NOT NULL,
        resolved_by INTEGER,
        resolution TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        resolved_at TIMESTAMP,
        FOREIGN KEY (reported_by) REFERENCES users (id),
        FOREIGN KEY (resolved_by) REFERENCES users (id)
    )
    ''')
    
    # Audit log table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS audit_log (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        action TEXT NOT NULL,
        table_name TEXT,
        record_id INTEGER,
        old_values TEXT,
        new_values TEXT,
        ip_address TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users (id)
    )
    ''')
    
    # Plate recognition log table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS plate_recognition_log (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        plate_number TEXT NOT NULL,
        confidence REAL,
        vehicle_id INTEGER,
        image_path TEXT,
        recognized_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users (id),
        FOREIGN KEY (vehicle_id) REFERENCES vehicles (id)
    )
    ''')
    
    # Apartments table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS apartments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        building_id INTEGER NOT NULL,
        unit_number TEXT NOT NULL,
        floor_number INTEGER,
        unit_type TEXT DEFAULT 'شقة',
        is_occupied INTEGER DEFAULT 0,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (building_id) REFERENCES buildings (id),
        UNIQUE(building_id, unit_number)
    )
    ''')
    
    # Parking spots table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS parking_spots (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        spot_number TEXT UNIQUE NOT NULL,
        parking_area TEXT NOT NULL,
        building_id INTEGER,
        apartment_id INTEGER,
        is_occupied INTEGER DEFAULT 0,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (building_id) REFERENCES buildings (id),
        FOREIGN KEY (apartment_id) REFERENCES apartments (id)
    )
    ''')
    
    # Car images table for uploaded car images
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS car_images (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        original_filename TEXT NOT NULL,
        image_path TEXT NOT NULL,
        thumbnail_path TEXT,
        uploaded_by INTEGER NOT NULL,
        uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        processed INTEGER DEFAULT 0,
        FOREIGN KEY (uploaded_by) REFERENCES users (id)
    )
    ''')
    
    # Car analysis results table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS car_analysis (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        car_image_id INTEGER NOT NULL,
        plate_number TEXT,
        plate_confidence REAL,
        vehicle_type TEXT,
        vehicle_color TEXT,
        analysis_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        vehicle_id INTEGER,
        violation_count INTEGER DEFAULT 0,
        notes TEXT,
        FOREIGN KEY (car_image_id) REFERENCES car_images (id) ON DELETE CASCADE,
        FOREIGN KEY (vehicle_id) REFERENCES vehicles (id)
    )
    ''')
    
    # Car violations mapping table - links car analysis to violations
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS car_violations_mapping (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        car_analysis_id INTEGER NOT NULL,
        violation_id INTEGER NOT NULL,
        linked_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        linked_by INTEGER,
        FOREIGN KEY (car_analysis_id) REFERENCES car_analysis (id) ON DELETE CASCADE,
        FOREIGN KEY (violation_id) REFERENCES traffic_violations (id) ON DELETE CASCADE,
        FOREIGN KEY (linked_by) REFERENCES users (id),
        UNIQUE(car_analysis_id, violation_id)
    )
    ''')
    
    conn.commit()
    
    # Check if default users exist
    cursor.execute('SELECT COUNT(*) FROM users')
    user_count = cursor.fetchone()[0]
    
    if user_count == 0:
        # Create default users
        default_users = [
            {
                'username': 'admin',
                'password': 'Admin@2025',
                'name': 'مدير النظام',
                'role': 'admin',
                'email': 'admin@university.edu.sa'
            },
            {
                'username': 'violations_officer',
                'password': 'Violations@2025',
                'name': 'مسؤول المخالفات',
                'role': 'violations',
                'email': 'violations@university.edu.sa'
            },
            {
                'username': 'visitors_officer',
                'password': 'Visitors@2025',
                'name': 'مسؤول الزوار',
                'role': 'visitors',
                'email': 'visitors@university.edu.sa'
            },
            {
                'username': 'viewer',
                'password': 'Viewer@2025',
                'name': 'مستخدم استعلام فقط',
                'role': 'viewer',
                'email': 'viewer@university.edu.sa'
            },
            {
                'username': 'violation_entry',
                'password': 'Violation@2025',
                'name': 'مسجل المخالفات',
                'role': 'violation_entry',
                'email': 'violation.entry@university.edu.sa'
            }
        ]
        
        for user in default_users:
            password_hash = generate_password_hash(user['password'])
            cursor.execute('''
                INSERT INTO users (username, password_hash, name, role, email)
                VALUES (?, ?, ?, ?, ?)
            ''', (user['username'], password_hash, user['name'], user['role'], user['email']))
        
        conn.commit()
        print("✅ Default users created successfully")
        print("=" * 60)
        print("Default Login Credentials / بيانات الدخول الافتراضية:")
        print("=" * 60)
        for user in default_users:
            print(f"Username: {user['username']} | Password: {user['password']}")
        print("=" * 60)
        print("⚠️  Please change these passwords after first login")
        print("⚠️  يرجى تغيير كلمات المرور بعد أول تسجيل دخول")
        print("=" * 60)
    
    conn.close()
    print("✅ Database initialized successfully")

def create_user(username, password, name, role, email=None):
    """Create a new user"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    password_hash = generate_password_hash(password)
    
    try:
        cursor.execute('''
            INSERT INTO users (username, password_hash, name, role, email)
            VALUES (?, ?, ?, ?, ?)
        ''', (username, password_hash, name, role, email))
        conn.commit()
        user_id = cursor.lastrowid
        conn.close()
        return user_id
    except sqlite3.IntegrityError:
        conn.close()
        return None

def verify_user(username, password):
    """Verify user credentials"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM users WHERE username = ? AND is_active = 1', (username,))
    user = cursor.fetchone()
    
    if user and check_password_hash(user['password_hash'], password):
        # Update last login
        cursor.execute('UPDATE users SET last_login = ? WHERE id = ?', 
                      (datetime.now(), user['id']))
        conn.commit()
        conn.close()
        return dict(user)
    
    conn.close()
    return None

def get_user_by_id(user_id):
    """Get user by ID"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM users WHERE id = ? AND is_active = 1', (user_id,))
    user = cursor.fetchone()
    conn.close()
    
    return dict(user) if user else None

def update_user_password(user_id, new_password):
    """Update user password"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    password_hash = generate_password_hash(new_password)
    cursor.execute('''
        UPDATE users SET password_hash = ?, updated_at = ? WHERE id = ?
    ''', (password_hash, datetime.now(), user_id))
    
    conn.commit()
    affected = cursor.rowcount
    conn.close()
    
    return affected > 0

def log_audit(user_id, action, table_name=None, record_id=None, old_values=None, new_values=None, ip_address=None):
    """Log an audit entry"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT INTO audit_log (user_id, action, table_name, record_id, old_values, new_values, ip_address)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (user_id, action, table_name, record_id, old_values, new_values, ip_address))
    
    conn.commit()
    conn.close()

if __name__ == '__main__':
    # Initialize database when run directly
    print("Initializing database...")
    init_database()
