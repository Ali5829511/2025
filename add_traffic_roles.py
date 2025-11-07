#!/usr/bin/env python3
"""
Add new user roles for traffic system
إضافة أدوار مستخدمين جديدة لنظام المرور
"""

import database_adapter
from werkzeug.security import generate_password_hash

def add_traffic_roles():
    """Add new roles for traffic violations entry and inquiry"""
    conn = database_adapter.get_db_connection()
    cursor = conn.cursor()
    
    print("=" * 70)
    print("Adding Traffic System User Roles")
    print("إضافة أدوار مستخدمين نظام المرور")
    print("=" * 70)
    
    # 1. Traffic Violations Entry User (input only)
    try:
        cursor.execute(database_adapter.adapt_sql('''
            INSERT OR IGNORE INTO users (username, password_hash, name, role, email, is_active)
            VALUES (?, ?, ?, ?, ?, ?)
        '''), (
            'traffic_entry',
            generate_password_hash('TrafficEntry@2025'),
            'مسجل المخالفات المرورية',
            'traffic_entry',
            'traffic.entry@university.edu.sa',
            1
        ))
        print("✓ Traffic Entry User created: traffic_entry")
    except Exception as e:
        print(f"✗ Error creating traffic_entry user: {str(e)}")
    
    # 2. Inquiry User (view and reports only)
    try:
        cursor.execute(database_adapter.adapt_sql('''
            INSERT OR IGNORE INTO users (username, password_hash, name, role, email, is_active)
            VALUES (?, ?, ?, ?, ?, ?)
        '''), (
            'inquiry_user',
            generate_password_hash('Inquiry@2025'),
            'مستخدم الاستعلام',
            'inquiry',
            'inquiry@university.edu.sa',
            1
        ))
        print("✓ Inquiry User created: inquiry_user")
    except Exception as e:
        print(f"✗ Error creating inquiry_user: {str(e)}")
    
    conn.commit()
    conn.close()
    
    print("\n" + "=" * 70)
    print("✅ User roles added successfully!")
    print("=" * 70)
    print("\nNew Login Credentials / بيانات الدخول الجديدة:")
    print("-" * 70)
    print("1. Traffic Entry User (تسجيل المخالفات والحوادث - إدخال فقط)")
    print("   Username: traffic_entry")
    print("   Password: TrafficEntry@2025")
    print("   Role: إدخال المخالفات والحوادث وكبح السيارات")
    print()
    print("2. Inquiry User (الاستعلام والتقارير - عرض فقط)")
    print("   Username: inquiry_user")
    print("   Password: Inquiry@2025")
    print("   Role: الاستعلام وعرض التقارير")
    print("=" * 70)

if __name__ == '__main__':
    try:
        add_traffic_roles()
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
