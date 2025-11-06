#!/usr/bin/env python3
"""
Database initialization script for both SQLite and PostgreSQL
سكريبت تهيئة قاعدة البيانات لـ SQLite و PostgreSQL

This script detects the environment and initializes the appropriate database.
"""

import os
import sys

# Add current directory to path
sys.path.insert(0, os.path.dirname(__file__))

def main():
    print("\n" + "="*60)
    print("🚀 Initializing Housing Management System Database")
    print("تهيئة قاعدة بيانات نظام إدارة الإسكان")
    print("="*60 + "\n")
    
    try:
        # Import database adapter to check configuration
        from database_adapter import print_database_info, get_connection_params
        
        print_database_info()
        
        # Import and run the original database initialization
        import database
        
        print("📊 Creating database tables...")
        print("جاري إنشاء جداول قاعدة البيانات...")
        
        database.init_database()
        
        print("\n✅ Database initialized successfully!")
        print("تم تهيئة قاعدة البيانات بنجاح!")
        
        print("\n📝 Default users created:")
        print("المستخدمون الافتراضيون:")
        print("  - admin (Admin@2025)")
        print("  - violations_officer (Violations@2025)")
        print("  - visitors_officer (Visitors@2025)")
        print("  - viewer (Viewer@2025)")
        print("  - violation_entry (Violation@2025)")
        
        print("\n⚠️  IMPORTANT: Change default passwords immediately!")
        print("مهم: غيّر كلمات المرور الافتراضية فوراً!")
        print("\n" + "="*60 + "\n")
        
        return 0
        
    except Exception as e:
        print(f"\n❌ Error initializing database: {e}")
        print(f"خطأ في تهيئة قاعدة البيانات: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == '__main__':
    sys.exit(main())
