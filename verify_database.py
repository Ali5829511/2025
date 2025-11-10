#!/usr/bin/env python3
"""
Database Verification Script / سكريبت التحقق من قاعدة البيانات
====================================================================
This script reviews and verifies the database structure and data integrity
for the Faculty Housing Management System.

يقوم هذا السكريبت بمراجعة والتحقق من بنية قاعدة البيانات وسلامة البيانات
لنظام إدارة إسكان أعضاء هيئة التدريس.
"""

import sqlite3
import os
import sys
from datetime import datetime

# Database path
DATABASE_PATH = os.path.join(os.path.dirname(__file__), 'housing.db')

def get_db_connection():
    """Create and return a database connection"""
    if not os.path.exists(DATABASE_PATH):
        print(f"❌ Error: Database file not found at {DATABASE_PATH}")
        sys.exit(1)
    
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def print_header(title):
    """Print a formatted header"""
    print("\n" + "=" * 80)
    print(f"  {title}")
    print("=" * 80)

def verify_table_structure():
    """Verify that all required tables exist"""
    print_header("📊 Database Structure Verification / التحقق من بنية قاعدة البيانات")
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Get all tables
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
    tables = cursor.fetchall()
    
    # Expected tables
    expected_tables = [
        'users', 'sessions', 'buildings', 'residents', 'vehicles', 'stickers',
        'traffic_violations', 'complaints', 'visitors', 'security_incidents',
        'audit_log', 'plate_recognition_log', 'apartments', 'parking_spots',
        'car_images', 'car_analysis', 'car_violations_mapping', 'parkpow_detections'
    ]
    
    print(f"\n✅ Found {len(tables)} tables in database:")
    table_names = [table['name'] for table in tables]
    
    for i, table in enumerate(tables, 1):
        status = "✅" if table['name'] in expected_tables else "⚠️"
        print(f"  {status} {i}. {table['name']}")
    
    # Check for missing tables
    missing_tables = [t for t in expected_tables if t not in table_names]
    if missing_tables:
        print(f"\n⚠️  Warning: Missing expected tables:")
        for table in missing_tables:
            print(f"  ❌ {table}")
    else:
        print(f"\n✅ All {len(expected_tables)} expected tables are present!")
    
    conn.close()
    return table_names

def verify_table_columns(table_name):
    """Verify columns in a specific table"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute(f"PRAGMA table_info({table_name})")
    columns = cursor.fetchall()
    
    conn.close()
    return columns

def verify_data_integrity():
    """Verify data integrity and relationships"""
    print_header("🔍 Data Integrity Verification / التحقق من سلامة البيانات")
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Check users table
    cursor.execute("SELECT COUNT(*) as count FROM users")
    user_count = cursor.fetchone()['count']
    print(f"\n👥 Users Table:")
    print(f"  Total users: {user_count}")
    
    if user_count > 0:
        cursor.execute("SELECT username, name, role, is_active FROM users")
        users = cursor.fetchall()
        for user in users:
            status = "✅ Active" if user['is_active'] else "❌ Inactive"
            print(f"  - {user['username']} ({user['name']}) - Role: {user['role']} - {status}")
    
    # Check buildings table
    cursor.execute("SELECT COUNT(*) as count FROM buildings")
    building_count = cursor.fetchone()['count']
    print(f"\n🏢 Buildings Table:")
    print(f"  Total buildings: {building_count}")
    
    if building_count > 0:
        cursor.execute("SELECT name, building_number, total_units FROM buildings LIMIT 5")
        buildings = cursor.fetchall()
        for building in buildings:
            print(f"  - {building['name']} (#{building['building_number']}) - Units: {building['total_units']}")
        if building_count > 5:
            print(f"  ... and {building_count - 5} more")
    
    # Check residents table
    cursor.execute("SELECT COUNT(*) as count FROM residents")
    resident_count = cursor.fetchone()['count']
    print(f"\n👨‍🏫 Residents Table:")
    print(f"  Total residents: {resident_count}")
    
    if resident_count > 0:
        cursor.execute("""
            SELECT COUNT(*) as active_count 
            FROM residents 
            WHERE is_active = 1
        """)
        active_residents = cursor.fetchone()['active_count']
        print(f"  Active residents: {active_residents}")
        print(f"  Inactive residents: {resident_count - active_residents}")
    
    # Check vehicles table
    cursor.execute("SELECT COUNT(*) as count FROM vehicles")
    vehicle_count = cursor.fetchone()['count']
    print(f"\n🚗 Vehicles Table:")
    print(f"  Total vehicles: {vehicle_count}")
    
    if vehicle_count > 0:
        cursor.execute("""
            SELECT COUNT(*) as active_count 
            FROM vehicles 
            WHERE is_active = 1
        """)
        active_vehicles = cursor.fetchone()['active_count']
        print(f"  Active vehicles: {active_vehicles}")
        print(f"  Inactive vehicles: {vehicle_count - active_vehicles}")
    
    # Check stickers table
    cursor.execute("SELECT COUNT(*) as count FROM stickers")
    sticker_count = cursor.fetchone()['count']
    print(f"\n🏷️  Stickers Table:")
    print(f"  Total stickers: {sticker_count}")
    
    if sticker_count > 0:
        cursor.execute("""
            SELECT status, COUNT(*) as count 
            FROM stickers 
            GROUP BY status
        """)
        sticker_status = cursor.fetchall()
        for status in sticker_status:
            print(f"  {status['status']}: {status['count']}")
    
    # Check traffic violations
    cursor.execute("SELECT COUNT(*) as count FROM traffic_violations")
    violation_count = cursor.fetchone()['count']
    print(f"\n🚦 Traffic Violations Table:")
    print(f"  Total violations: {violation_count}")
    
    if violation_count > 0:
        cursor.execute("""
            SELECT status, COUNT(*) as count 
            FROM traffic_violations 
            GROUP BY status
        """)
        violation_status = cursor.fetchall()
        for status in violation_status:
            print(f"  {status['status']}: {status['count']}")
    
    # Check complaints
    cursor.execute("SELECT COUNT(*) as count FROM complaints")
    complaint_count = cursor.fetchone()['count']
    print(f"\n📝 Complaints Table:")
    print(f"  Total complaints: {complaint_count}")
    
    if complaint_count > 0:
        cursor.execute("""
            SELECT status, COUNT(*) as count 
            FROM complaints 
            GROUP BY status
        """)
        complaint_status = cursor.fetchall()
        for status in complaint_status:
            print(f"  {status['status']}: {status['count']}")
    
    # Check visitors
    cursor.execute("SELECT COUNT(*) as count FROM visitors")
    visitor_count = cursor.fetchone()['count']
    print(f"\n🚶 Visitors Table:")
    print(f"  Total visitor records: {visitor_count}")
    
    # Check security incidents
    cursor.execute("SELECT COUNT(*) as count FROM security_incidents")
    incident_count = cursor.fetchone()['count']
    print(f"\n🔒 Security Incidents Table:")
    print(f"  Total incidents: {incident_count}")
    
    if incident_count > 0:
        cursor.execute("""
            SELECT status, COUNT(*) as count 
            FROM security_incidents 
            GROUP BY status
        """)
        incident_status = cursor.fetchall()
        for status in incident_status:
            print(f"  {status['status']}: {status['count']}")
    
    # Check apartments
    cursor.execute("SELECT COUNT(*) as count FROM apartments")
    apartment_count = cursor.fetchone()['count']
    print(f"\n🏘️  Apartments Table:")
    print(f"  Total apartments: {apartment_count}")
    
    if apartment_count > 0:
        cursor.execute("""
            SELECT COUNT(*) as occupied_count 
            FROM apartments 
            WHERE is_occupied = 1
        """)
        occupied_apartments = cursor.fetchone()['occupied_count']
        print(f"  Occupied: {occupied_apartments}")
        print(f"  Vacant: {apartment_count - occupied_apartments}")
    
    # Check parking spots
    cursor.execute("SELECT COUNT(*) as count FROM parking_spots")
    parking_count = cursor.fetchone()['count']
    print(f"\n🅿️  Parking Spots Table:")
    print(f"  Total parking spots: {parking_count}")
    
    if parking_count > 0:
        cursor.execute("""
            SELECT COUNT(*) as occupied_count 
            FROM parking_spots 
            WHERE is_occupied = 1
        """)
        occupied_parking = cursor.fetchone()['occupied_count']
        print(f"  Occupied: {occupied_parking}")
        print(f"  Available: {parking_count - occupied_parking}")
    
    # Check audit log
    cursor.execute("SELECT COUNT(*) as count FROM audit_log")
    audit_count = cursor.fetchone()['count']
    print(f"\n📋 Audit Log Table:")
    print(f"  Total audit entries: {audit_count}")
    
    conn.close()

def verify_foreign_keys():
    """Verify foreign key relationships"""
    print_header("🔗 Foreign Key Relationships / التحقق من العلاقات")
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    checks = [
        {
            'name': 'Residents → Buildings',
            'query': '''
                SELECT COUNT(*) as orphan_count 
                FROM residents r 
                WHERE r.building_id IS NOT NULL 
                AND NOT EXISTS (SELECT 1 FROM buildings b WHERE b.id = r.building_id)
            '''
        },
        {
            'name': 'Vehicles → Residents',
            'query': '''
                SELECT COUNT(*) as orphan_count 
                FROM vehicles v 
                WHERE NOT EXISTS (SELECT 1 FROM residents r WHERE r.id = v.owner_id)
            '''
        },
        {
            'name': 'Traffic Violations → Vehicles',
            'query': '''
                SELECT COUNT(*) as orphan_count 
                FROM traffic_violations tv 
                WHERE NOT EXISTS (SELECT 1 FROM vehicles v WHERE v.id = tv.vehicle_id)
            '''
        },
        {
            'name': 'Stickers → Residents',
            'query': '''
                SELECT COUNT(*) as orphan_count 
                FROM stickers s 
                WHERE NOT EXISTS (SELECT 1 FROM residents r WHERE r.id = s.resident_id)
            '''
        },
        {
            'name': 'Visitors → Residents',
            'query': '''
                SELECT COUNT(*) as orphan_count 
                FROM visitors v 
                WHERE NOT EXISTS (SELECT 1 FROM residents r WHERE r.id = v.visiting_resident_id)
            '''
        },
        {
            'name': 'Apartments → Buildings',
            'query': '''
                SELECT COUNT(*) as orphan_count 
                FROM apartments a 
                WHERE NOT EXISTS (SELECT 1 FROM buildings b WHERE b.id = a.building_id)
            '''
        }
    ]
    
    print("\n🔍 Checking referential integrity:")
    all_valid = True
    
    for check in checks:
        cursor.execute(check['query'])
        result = cursor.fetchone()
        orphan_count = result['orphan_count']
        
        if orphan_count == 0:
            print(f"  ✅ {check['name']}: Valid (0 orphan records)")
        else:
            print(f"  ⚠️  {check['name']}: Found {orphan_count} orphan record(s)")
            all_valid = False
    
    if all_valid:
        print("\n✅ All foreign key relationships are valid!")
    else:
        print("\n⚠️  Some foreign key relationships have issues.")
    
    conn.close()

def verify_indexes():
    """Check if important indexes exist"""
    print_header("📇 Index Verification / التحقق من الفهارس")
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT name, tbl_name, sql 
        FROM sqlite_master 
        WHERE type='index' 
        AND sql IS NOT NULL
        ORDER BY tbl_name, name
    """)
    
    indexes = cursor.fetchall()
    
    if len(indexes) > 0:
        print(f"\n✅ Found {len(indexes)} custom indexes:")
        current_table = None
        for idx in indexes:
            if idx['tbl_name'] != current_table:
                current_table = idx['tbl_name']
                print(f"\n  📊 {current_table}:")
            print(f"    - {idx['name']}")
    else:
        print("\n⚠️  No custom indexes found (using default primary key indexes only)")
    
    conn.close()

def generate_summary():
    """Generate a summary report"""
    print_header("📊 Database Summary Report / ملخص تقرير قاعدة البيانات")
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Get file size
    db_size = os.path.getsize(DATABASE_PATH)
    db_size_mb = db_size / (1024 * 1024)
    
    print(f"\n📁 Database Information:")
    print(f"  Path: {DATABASE_PATH}")
    print(f"  Size: {db_size_mb:.2f} MB ({db_size:,} bytes)")
    print(f"  Created: {datetime.fromtimestamp(os.path.getctime(DATABASE_PATH)).strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"  Last Modified: {datetime.fromtimestamp(os.path.getmtime(DATABASE_PATH)).strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Count all records
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
    tables = cursor.fetchall()
    
    print(f"\n📊 Record Counts by Table:")
    total_records = 0
    
    for table in tables:
        table_name = table['name']
        cursor.execute(f"SELECT COUNT(*) as count FROM {table_name}")
        count = cursor.fetchone()['count']
        total_records += count
        print(f"  {table_name}: {count:,}")
    
    print(f"\n  📈 Total Records Across All Tables: {total_records:,}")
    
    conn.close()

def verify_data_quality():
    """Check for data quality issues"""
    print_header("✨ Data Quality Checks / فحوصات جودة البيانات")
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    issues = []
    
    # Check for users without names
    cursor.execute("SELECT COUNT(*) as count FROM users WHERE name IS NULL OR name = ''")
    result = cursor.fetchone()
    if result['count'] > 0:
        issues.append(f"⚠️  {result['count']} users without names")
    
    # Check for residents without phone numbers
    cursor.execute("SELECT COUNT(*) as count FROM residents WHERE phone IS NULL OR phone = ''")
    result = cursor.fetchone()
    if result['count'] > 0:
        issues.append(f"⚠️  {result['count']} residents without phone numbers")
    
    # Check for vehicles without plate numbers
    cursor.execute("SELECT COUNT(*) as count FROM vehicles WHERE plate_number IS NULL OR plate_number = ''")
    result = cursor.fetchone()
    if result['count'] > 0:
        issues.append(f"⚠️  {result['count']} vehicles without plate numbers")
    
    # Check for expired stickers
    cursor.execute("""
        SELECT COUNT(*) as count 
        FROM stickers 
        WHERE expiry_date < date('now') 
        AND status = 'active'
    """)
    result = cursor.fetchone()
    if result['count'] > 0:
        issues.append(f"⚠️  {result['count']} expired stickers still marked as active")
    
    # Check for buildings without units
    cursor.execute("SELECT COUNT(*) as count FROM buildings WHERE total_units IS NULL OR total_units = 0")
    result = cursor.fetchone()
    if result['count'] > 0:
        issues.append(f"⚠️  {result['count']} buildings without unit counts")
    
    if len(issues) == 0:
        print("\n✅ No data quality issues detected!")
    else:
        print(f"\n⚠️  Found {len(issues)} potential data quality issue(s):")
        for issue in issues:
            print(f"  {issue}")
    
    conn.close()

def main():
    """Main verification function"""
    print("\n" + "=" * 80)
    print("  🔍 DATABASE VERIFICATION REPORT")
    print("  تقرير التحقق من قاعدة البيانات")
    print("=" * 80)
    print(f"  Date/Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 80)
    
    try:
        # Run all verification checks
        verify_table_structure()
        verify_data_integrity()
        verify_foreign_keys()
        verify_indexes()
        verify_data_quality()
        generate_summary()
        
        print_header("✅ Verification Complete / اكتمل التحقق")
        print("\n✨ Database verification completed successfully!")
        print("✨ تم التحقق من قاعدة البيانات بنجاح!")
        print("\n" + "=" * 80 + "\n")
        
        return 0
    
    except Exception as e:
        print(f"\n❌ Error during verification: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == '__main__':
    sys.exit(main())
