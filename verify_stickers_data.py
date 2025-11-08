#!/usr/bin/env python3
"""
Verification Script for Car Stickers Data
سكريبت التحقق من بيانات ملصقات السيارات

This script checks if there is data in the car stickers table and provides
detailed statistics about the stickers in the database.
"""

import database
from datetime import datetime
import sys


def verify_stickers_data():
    """
    Verify if stickers data exists in the database
    التحقق من وجود بيانات ملصقات السيارات في قاعدة البيانات
    """
    try:
        conn = database.get_db_connection()
        cursor = conn.cursor()
        
        print("=" * 70)
        print("🔍 Car Stickers Data Verification")
        print("   التحقق من بيانات ملصقات السيارات")
        print("=" * 70)
        print()
        
        # Check if stickers table exists
        cursor.execute("""
            SELECT name FROM sqlite_master 
            WHERE type='table' AND name='stickers'
        """)
        table_exists = cursor.fetchone()
        
        if not table_exists:
            print("❌ Error: Stickers table does not exist!")
            print("   خطأ: جدول الملصقات غير موجود!")
            print()
            print("💡 Tip: Run 'python3 database.py' to initialize the database")
            return False
        
        print("✅ Stickers table exists")
        print()
        
        # Get total count of stickers
        cursor.execute("SELECT COUNT(*) FROM stickers")
        total_count = cursor.fetchone()[0]
        
        if total_count == 0:
            print("⚠️  Warning: No stickers data found in the database!")
            print("   تحذير: لا توجد بيانات ملصقات في قاعدة البيانات!")
            print()
            print("💡 Tip: Run 'python3 create_sample_data.py' to create sample data")
            return False
        
        print(f"✅ Total stickers found: {total_count}")
        print(f"   إجمالي الملصقات: {total_count}")
        print()
        
        # Get stickers by status
        cursor.execute("""
            SELECT status, COUNT(*) as count 
            FROM stickers 
            GROUP BY status
        """)
        status_counts = cursor.fetchall()
        
        print("📊 Stickers by Status / الملصقات حسب الحالة:")
        print("-" * 70)
        for status, count in status_counts:
            status_label = status if status else "Unknown"
            print(f"   {status_label:15} : {count:3} stickers")
        print()
        
        # Get recent stickers
        cursor.execute("""
            SELECT sticker_number, plate_number, vehicle_type, issue_date, status
            FROM stickers
            ORDER BY created_at DESC
            LIMIT 5
        """)
        recent_stickers = cursor.fetchall()
        
        print("📋 Recent Stickers (Last 5) / آخر 5 ملصقات:")
        print("-" * 70)
        for sticker in recent_stickers:
            sticker_num, plate, vehicle, issue_date, status = sticker
            print(f"   #{sticker_num:12} | Plate: {plate:15} | {vehicle:10} | {status}")
        print()
        
        # Get stickers by vehicle type
        cursor.execute("""
            SELECT vehicle_type, COUNT(*) as count 
            FROM stickers 
            WHERE vehicle_type IS NOT NULL
            GROUP BY vehicle_type
            ORDER BY count DESC
        """)
        vehicle_counts = cursor.fetchall()
        
        if vehicle_counts:
            print("🚗 Stickers by Vehicle Type / الملصقات حسب نوع المركبة:")
            print("-" * 70)
            for vehicle_type, count in vehicle_counts:
                print(f"   {vehicle_type:20} : {count:3} stickers")
            print()
        
        # Check for expired stickers
        cursor.execute("""
            SELECT COUNT(*) 
            FROM stickers 
            WHERE expiry_date < date('now') AND status = 'active'
        """)
        expired_count = cursor.fetchone()[0]
        
        if expired_count > 0:
            print(f"⚠️  Warning: {expired_count} expired stickers still marked as active")
            print(f"   تحذير: {expired_count} ملصق منتهي الصلاحية ولكن لا يزال نشطاً")
            print()
        
        # Get stickers without residents
        cursor.execute("""
            SELECT COUNT(*) 
            FROM stickers s
            LEFT JOIN residents r ON s.resident_id = r.id
            WHERE r.id IS NULL
        """)
        orphan_count = cursor.fetchone()[0]
        
        if orphan_count > 0:
            print(f"⚠️  Warning: {orphan_count} stickers without associated residents")
            print(f"   تحذير: {orphan_count} ملصق بدون ساكن مرتبط")
            print()
        
        # Summary
        print("=" * 70)
        print("✅ Verification Complete / اكتمل التحقق")
        print(f"   Total stickers: {total_count}")
        print(f"   Active stickers: {sum(count for status, count in status_counts if status == 'active')}")
        print(f"   Expired but active: {expired_count}")
        print(f"   Orphaned stickers: {orphan_count}")
        print("=" * 70)
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Error during verification: {str(e)}")
        print(f"   خطأ أثناء التحقق: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def get_stickers_data_status():
    """
    Get a simple status check for stickers data
    Returns: dict with status information
    """
    try:
        conn = database.get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT COUNT(*) FROM stickers")
        total_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM stickers WHERE status = 'active'")
        active_count = cursor.fetchone()[0]
        
        conn.close()
        
        return {
            'has_data': total_count > 0,
            'total_count': total_count,
            'active_count': active_count,
            'status': 'ok' if total_count > 0 else 'empty'
        }
    except Exception as e:
        return {
            'has_data': False,
            'total_count': 0,
            'active_count': 0,
            'status': 'error',
            'error': str(e)
        }


if __name__ == '__main__':
    """Run verification when script is executed directly"""
    print()
    success = verify_stickers_data()
    print()
    
    # Exit with appropriate code
    sys.exit(0 if success else 1)
