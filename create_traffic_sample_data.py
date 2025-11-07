#!/usr/bin/env python3
"""
Create sample data for Traffic Department System
إنشاء بيانات تجريبية لنظام قسم المرور
"""

import sqlite3
from datetime import datetime, timedelta
import random

def create_sample_data():
    """Create sample data for testing"""
    print("=" * 60)
    print("Creating Sample Data for Traffic Department")
    print("إنشاء بيانات تجريبية لقسم المرور")
    print("=" * 60)
    
    conn = sqlite3.connect('housing.db')
    cursor = conn.cursor()
    
    # Sample plate numbers
    plate_numbers = [
        'ABC1234', 'XYZ5678', 'DEF9012', 'GHI3456', 'JKL7890',
        'MNO2345', 'PQR6789', 'STU0123', 'VWX4567', 'YZA8901'
    ]
    
    # Get some vehicles from database
    cursor.execute('SELECT id, plate_number FROM vehicles LIMIT 10')
    existing_vehicles = cursor.fetchall()
    
    print("\n1. Creating Traffic Violations...")
    print("   إنشاء مخالفات مرورية...")
    
    violation_types = [
        'وقوف في مكان محظور',
        'تجاوز السرعة المقررة',
        'عدم الالتزام بالمسار المحدد',
        'الوقوف في موقف المعاقين',
        'الوقوف في الممرات',
        'عدم وجود ملصق صالح',
        'دخول بدون تصريح',
        'إعاقة حركة المرور'
    ]
    
    locations = [
        'موقف المبنى الرئيسي',
        'موقف مبنى الإدارة',
        'موقف الكليات',
        'الطريق الداخلي الرئيسي',
        'موقف الزوار',
        'المدخل الشمالي',
        'المدخل الجنوبي',
        'الطريق الدائري الداخلي'
    ]
    
    violations_created = 0
    for i in range(30):
        plate = random.choice(plate_numbers)
        vehicle_id = None
        
        # Try to find vehicle by plate
        if existing_vehicles:
            for vid, vplate in existing_vehicles:
                if vplate == plate:
                    vehicle_id = vid
                    break
        
        violation_date = datetime.now() - timedelta(days=random.randint(1, 90))
        violation_type = random.choice(violation_types)
        location = random.choice(locations)
        fine_amount = random.choice([100, 150, 200, 300, 500])
        status = random.choice(['pending', 'pending', 'resolved', 'paid'])
        
        try:
            cursor.execute('''
                INSERT INTO traffic_violations 
                (vehicle_id, plate_number, violation_type, violation_date, location, 
                 description, fine_amount, status, reported_by)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, 1)
            ''', (
                vehicle_id,
                plate,
                violation_type,
                violation_date,
                location,
                f'مخالفة {violation_type} في {location}',
                fine_amount,
                status
            ))
            violations_created += 1
        except Exception as e:
            print(f"   Warning: Could not create violation: {e}")
    
    print(f"   ✅ Created {violations_created} traffic violations")
    
    print("\n2. Creating Traffic Accidents...")
    print("   إنشاء حوادث مرورية...")
    
    accident_types = [
        'تصادم بسيط',
        'تصادم متوسط',
        'انقلاب',
        'اصطدام بعمود',
        'خدش سيارة',
        'كسر مرآة جانبية'
    ]
    
    severities = ['minor', 'minor', 'moderate', 'major']
    weather_conditions = ['صافي', 'غائم', 'ممطر', 'عاصف']
    road_conditions = ['جيدة', 'متوسطة', 'رطبة']
    
    accidents_created = 0
    for i in range(15):
        accident_date = datetime.now() - timedelta(days=random.randint(1, 120))
        location = random.choice(locations)
        severity = random.choice(severities)
        vehicles_involved = random.randint(1, 3)
        injuries_count = 0 if severity in ['minor', 'moderate'] else random.randint(0, 2)
        damage_estimate = random.randint(1000, 20000)
        
        try:
            cursor.execute('''
                INSERT INTO traffic_accidents 
                (accident_number, accident_date, location, description, severity,
                 weather_conditions, road_conditions, vehicles_involved, injuries_count,
                 fatalities_count, damage_estimate, status, reported_by)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, 0, ?, 'reported', 1)
            ''', (
                f'ACC-2025-{i+1:05d}',
                accident_date,
                location,
                random.choice(accident_types),
                severity,
                random.choice(weather_conditions),
                random.choice(road_conditions),
                vehicles_involved,
                injuries_count,
                damage_estimate
            ))
            
            accident_id = cursor.lastrowid
            
            # Add vehicles to accident
            for v in range(vehicles_involved):
                plate = random.choice(plate_numbers)
                at_fault = 1 if v == 0 else 0
                
                cursor.execute('''
                    INSERT INTO accident_vehicles
                    (accident_id, plate_number, driver_name, driver_phone,
                     damage_description, at_fault)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (
                    accident_id,
                    plate,
                    f'سائق {v+1}',
                    f'0501234{random.randint(100,999)}',
                    'أضرار في المصد والأبواب',
                    at_fault
                ))
            
            accidents_created += 1
        except Exception as e:
            print(f"   Warning: Could not create accident: {e}")
    
    print(f"   ✅ Created {accidents_created} traffic accidents")
    
    print("\n3. Creating Immobilized Cars...")
    print("   إنشاء سيارات محجوزة...")
    
    immobilization_types = ['boot', 'tow', 'compound']
    reasons = [
        'عدة مخالفات غير مدفوعة',
        'تجاوز عدد المخالفات المسموح',
        'وقوف في مكان خطر',
        'عدم وجود تصريح صالح',
        'سيارة مهجورة'
    ]
    
    immobilized_created = 0
    for i in range(10):
        immobilized_date = datetime.now() - timedelta(days=random.randint(1, 60))
        plate = random.choice(plate_numbers)
        immobilization_type = random.choice(immobilization_types)
        reason = random.choice(reasons)
        location = random.choice(locations)
        outstanding_fines = random.randint(500, 3000)
        towing_fee = 200 if immobilization_type == 'tow' else 0
        storage_fee = random.randint(0, 500)
        total_fees = outstanding_fines + towing_fee + storage_fee
        status = random.choice(['immobilized', 'immobilized', 'released'])
        payment_status = 'paid' if status == 'released' else random.choice(['unpaid', 'partial'])
        
        try:
            cursor.execute('''
                INSERT INTO immobilized_cars 
                (plate_number, immobilization_type, reason, location,
                 immobilized_date, immobilized_by, outstanding_fines, 
                 towing_fee, storage_fee, total_fees, payment_status, 
                 status, violation_count)
                VALUES (?, ?, ?, ?, ?, 1, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                plate,
                immobilization_type,
                reason,
                location,
                immobilized_date,
                outstanding_fines,
                towing_fee,
                storage_fee,
                total_fees,
                payment_status,
                status,
                random.randint(3, 8)
            ))
            immobilized_created += 1
        except Exception as e:
            print(f"   Warning: Could not create immobilized car: {e}")
    
    print(f"   ✅ Created {immobilized_created} immobilized cars")
    
    conn.commit()
    conn.close()
    
    print("\n" + "=" * 60)
    print("✅ Sample Data Creation Complete!")
    print("✅ اكتمل إنشاء البيانات التجريبية!")
    print("=" * 60)
    print("\nSummary / الملخص:")
    print(f"  - Traffic Violations: {violations_created}")
    print(f"  - Traffic Accidents: {accidents_created}")
    print(f"  - Immobilized Cars: {immobilized_created}")
    print("\nYou can now test the system with this sample data.")
    print("يمكنك الآن اختبار النظام باستخدام هذه البيانات التجريبية.")

if __name__ == '__main__':
    create_sample_data()
