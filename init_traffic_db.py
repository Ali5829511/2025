"""
Initialize Traffic Database
إنشاء قاعدة بيانات المخالفات المرورية
"""
import sqlite3
import os

def init_traffic_database():
    """Create traffic.db with cars and violations tables"""
    
    db_path = os.path.join(os.path.dirname(__file__), 'traffic.db')
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # جدول السيارات - Cars table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS cars (
        car_id INTEGER PRIMARY KEY AUTOINCREMENT,
        plate_number TEXT UNIQUE NOT NULL,
        owner_name TEXT,
        model TEXT,
        year INTEGER,
        color TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    
    # جدول المخالفات - Violations table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS violations (
        violation_id INTEGER PRIMARY KEY AUTOINCREMENT,
        car_id INTEGER NOT NULL,
        violation_type TEXT NOT NULL,
        violation_date TEXT NOT NULL,
        fine_amount REAL NOT NULL,
        officer_name TEXT,
        image_path TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (car_id) REFERENCES cars(car_id)
    )
    ''')
    
    # Create indexes for performance
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_cars_plate ON cars(plate_number)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_violations_car ON violations(car_id)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_violations_date ON violations(violation_date)')
    
    conn.commit()
    
    # Add sample data if tables are empty
    cursor.execute('SELECT COUNT(*) FROM cars')
    if cursor.fetchone()[0] == 0:
        print("Adding sample data...")
        
        # Sample cars
        sample_cars = [
            ('ABC-1234', 'أحمد محمد', 'تويوتا كامري', 2020, 'أبيض'),
            ('XYZ-5678', 'فاطمة علي', 'هيونداي سوناتا', 2019, 'أسود'),
            ('DEF-9012', 'محمد سعيد', 'نيسان التيما', 2021, 'رمادي'),
        ]
        
        cursor.executemany('''
            INSERT INTO cars (plate_number, owner_name, model, year, color)
            VALUES (?, ?, ?, ?, ?)
        ''', sample_cars)
        
        # Sample violations
        sample_violations = [
            (1, 'تجاوز السرعة', '2024-01-15', 500.0, 'محمد أحمد', '/static/images/violation1.jpg'),
            (1, 'وقوف ممنوع', '2024-02-10', 300.0, 'علي حسن', '/static/images/violation2.jpg'),
            (2, 'عكس السير', '2024-01-20', 1000.0, 'خالد سالم', '/static/images/violation3.jpg'),
            (3, 'استخدام الجوال', '2024-03-05', 500.0, 'محمد أحمد', '/static/images/violation4.jpg'),
        ]
        
        cursor.executemany('''
            INSERT INTO violations (car_id, violation_type, violation_date, fine_amount, officer_name, image_path)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', sample_violations)
        
        conn.commit()
        print("Sample data added successfully!")
    
    conn.close()
    print(f"Database initialized: {db_path}")
    return db_path

if __name__ == "__main__":
    init_traffic_database()
