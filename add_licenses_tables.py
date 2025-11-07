#!/usr/bin/env python3
"""
Script to add licenses tables to the database
إضافة جداول الرخص إلى قاعدة البيانات
"""

import database_adapter

def add_licenses_tables():
    """Add licenses-related tables to the database"""
    conn = database_adapter.get_db_connection()
    cursor = conn.cursor()
    
    print("Adding licenses tables to database...")
    
    # Driver licenses table
    cursor.execute(database_adapter.adapt_sql('''
    CREATE TABLE IF NOT EXISTS driver_licenses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        license_number TEXT UNIQUE NOT NULL,
        resident_id INTEGER,
        full_name TEXT NOT NULL,
        national_id TEXT NOT NULL,
        date_of_birth DATE,
        license_type TEXT NOT NULL,
        issue_date DATE NOT NULL,
        expiry_date DATE NOT NULL,
        issuing_authority TEXT DEFAULT 'المملكة العربية السعودية',
        blood_type TEXT,
        license_status TEXT DEFAULT 'active',
        points_balance INTEGER DEFAULT 24,
        violations_count INTEGER DEFAULT 0,
        photo_path TEXT,
        notes TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (resident_id) REFERENCES residents (id)
    )
    '''))
    print("✓ Driver licenses table created")
    
    # Vehicle registrations table
    cursor.execute(database_adapter.adapt_sql('''
    CREATE TABLE IF NOT EXISTS vehicle_registrations (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        registration_number TEXT UNIQUE NOT NULL,
        vehicle_id INTEGER,
        plate_number TEXT NOT NULL,
        owner_id INTEGER,
        owner_name TEXT NOT NULL,
        owner_national_id TEXT NOT NULL,
        vehicle_make TEXT NOT NULL,
        vehicle_model TEXT NOT NULL,
        vehicle_year INTEGER NOT NULL,
        vehicle_color TEXT,
        vehicle_type TEXT DEFAULT 'سيارة',
        chassis_number TEXT,
        engine_number TEXT,
        registration_date DATE NOT NULL,
        expiry_date DATE NOT NULL,
        registration_status TEXT DEFAULT 'active',
        insurance_company TEXT,
        insurance_policy_number TEXT,
        insurance_expiry_date DATE,
        technical_inspection_date DATE,
        technical_inspection_expiry DATE,
        notes TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (vehicle_id) REFERENCES vehicles (id),
        FOREIGN KEY (owner_id) REFERENCES residents (id)
    )
    '''))
    print("✓ Vehicle registrations table created")
    
    # License violations history
    cursor.execute(database_adapter.adapt_sql('''
    CREATE TABLE IF NOT EXISTS license_violations_history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        driver_license_id INTEGER NOT NULL,
        violation_id INTEGER NOT NULL,
        points_deducted INTEGER DEFAULT 0,
        violation_date TIMESTAMP NOT NULL,
        linked_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (driver_license_id) REFERENCES driver_licenses (id) ON DELETE CASCADE,
        FOREIGN KEY (violation_id) REFERENCES traffic_violations (id) ON DELETE CASCADE
    )
    '''))
    print("✓ License violations history table created")
    
    # License renewals history
    cursor.execute(database_adapter.adapt_sql('''
    CREATE TABLE IF NOT EXISTS license_renewals (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        license_id INTEGER NOT NULL,
        license_type TEXT NOT NULL,
        renewal_date DATE NOT NULL,
        old_expiry_date DATE NOT NULL,
        new_expiry_date DATE NOT NULL,
        renewal_fee DECIMAL(10,2) DEFAULT 0,
        renewed_by INTEGER,
        notes TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (license_id) REFERENCES driver_licenses (id) ON DELETE CASCADE,
        FOREIGN KEY (renewed_by) REFERENCES users (id)
    )
    '''))
    print("✓ License renewals table created")
    
    # Vehicle registration renewals
    cursor.execute(database_adapter.adapt_sql('''
    CREATE TABLE IF NOT EXISTS registration_renewals (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        registration_id INTEGER NOT NULL,
        renewal_date DATE NOT NULL,
        old_expiry_date DATE NOT NULL,
        new_expiry_date DATE NOT NULL,
        renewal_fee DECIMAL(10,2) DEFAULT 0,
        renewed_by INTEGER,
        notes TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (registration_id) REFERENCES vehicle_registrations (id) ON DELETE CASCADE,
        FOREIGN KEY (renewed_by) REFERENCES users (id)
    )
    '''))
    print("✓ Vehicle registration renewals table created")
    
    conn.commit()
    conn.close()
    
    print("\n✅ All licenses tables added successfully!")
    print("=" * 60)
    print("Tables created:")
    print("1. driver_licenses - رخص القيادة")
    print("2. vehicle_registrations - استمارات المركبات")
    print("3. license_violations_history - سجل مخالفات الرخصة")
    print("4. license_renewals - تجديدات الرخص")
    print("5. registration_renewals - تجديدات الاستمارات")
    print("=" * 60)

if __name__ == '__main__':
    try:
        add_licenses_tables()
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
