#!/usr/bin/env python3
"""
Create sample data for the integrated traffic management system
إنشاء بيانات تجريبية لنظام المرور المتكامل
"""

import database_adapter
from datetime import datetime, timedelta
import random

def create_sample_traffic_data():
    """Create comprehensive sample traffic data"""
    conn = database_adapter.get_db_connection()
    cursor = conn.cursor()
    
    print("=" * 70)
    print("Creating Sample Traffic Management Data")
    print("إنشاء بيانات تجريبية لنظام المرور المتكامل")
    print("=" * 70)
    
    # Sample vehicles with Saudi plate formats
    vehicles = [
        ('ABC1234', 'د. أحمد محمد العتيبي', 'تويوتا', 'كامري', 2022, 'أبيض'),
        ('XYZ5678', 'د. فاطمة علي الغامدي', 'هوندا', 'أكورد', 2021, 'أسود'),
        ('DEF9012', 'أ. محمد سعيد القحطاني', 'نيسان', 'التيما', 2020, 'فضي'),
        ('GHI3456', 'د. سارة عبدالله الشهري', 'مازدا', 'CX5', 2023, 'أحمر'),
        ('JKL7890', 'أ. خالد إبراهيم العمري', 'كيا', 'أوبتيما', 2019, 'أزرق'),
        ('MNO1111', 'د. نورة حسن المطيري', 'هيونداي', 'سوناتا', 2022, 'رمادي'),
        ('PQR2222', 'أ. عمر علي الدوسري', 'شيفروليه', 'ماليبو', 2021, 'أبيض'),
        ('STU3333', 'د. منيرة عبدالرحمن الزهراني', 'فورد', 'فيوجن', 2020, 'أسود'),
        ('VWX4444', 'أ. سلمان محمد السليم', 'لكزس', 'ES350', 2023, 'فضي'),
        ('YZA5555', 'د. عبير فيصل الخالدي', 'BMW', '320i', 2022, 'أزرق')
    ]
    
    # Sample violation types with fines
    violation_types = [
        ('وقوف في مكان ممنوع', 150, 'parking'),
        ('تجاوز السرعة المحددة', 300, 'speeding'),
        ('عدم الالتزام بإشارة المرور', 500, 'signal'),
        ('استخدام الهاتف أثناء القيادة', 500, 'phone'),
        ('عدم ربط حزام الأمان', 150, 'seatbelt'),
        ('الوقوف في مواقف ذوي الاحتياجات', 500, 'handicap'),
        ('قطع الإشارة الحمراء', 500, 'red_light'),
        ('القيادة العكسية', 300, 'wrong_way')
    ]
    
    # Sample locations
    locations = [
        'موقف المبنى الإداري',
        'موقف كلية العلوم',
        'موقف مبنى أعضاء هيئة التدريس',
        'الشارع الرئيسي - البوابة الشمالية',
        'موقف مبنى الطلاب',
        'موقف المكتبة المركزية',
        'الشارع الداخلي - قرب الكافتيريا',
        'موقف السكن الداخلي'
    ]
    
    print("\n1. Creating sample vehicles...")
    for plate, owner, make, model, year, color in vehicles:
        try:
            cursor.execute(database_adapter.adapt_sql('''
                INSERT OR IGNORE INTO vehicles 
                (plate_number, owner_name, make, model, year, color, vehicle_type, is_active)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            '''), (plate, owner, make, model, year, color, 'سيارة', 1))
            print(f"   ✓ Vehicle created: {plate} - {owner}")
        except Exception as e:
            print(f"   ✗ Error creating vehicle {plate}: {str(e)}")
    
    print("\n2. Creating traffic violations...")
    violation_count = 0
    for _ in range(50):  # Create 50 violations
        vehicle = random.choice(vehicles)
        plate = vehicle[0]
        owner = vehicle[1]
        
        violation = random.choice(violation_types)
        vtype, fine, category = violation
        
        location = random.choice(locations)
        days_ago = random.randint(1, 180)
        violation_date = datetime.now() - timedelta(days=days_ago)
        
        status = random.choice(['pending', 'pending', 'pending', 'resolved'])
        
        try:
            # Get vehicle_id
            cursor.execute('SELECT id FROM vehicles WHERE plate_number = ?', (plate,))
            result = cursor.fetchone()
            vehicle_id = result[0] if result else None
            
            cursor.execute(database_adapter.adapt_sql('''
                INSERT INTO traffic_violations 
                (vehicle_id, plate_number, violation_type, violation_date, location,
                 fine_amount, status, description, reported_by)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            '''), (vehicle_id, plate, vtype, violation_date, location, fine, status,
                   f'مخالفة {vtype} للسيارة {plate}', 1))
            violation_count += 1
            if violation_count % 10 == 0:
                print(f"   ✓ Created {violation_count} violations...")
        except Exception as e:
            print(f"   ✗ Error creating violation: {str(e)}")
    
    print(f"   ✓ Total violations created: {violation_count}")
    
    print("\n3. Creating traffic accidents...")
    accident_count = 0
    for i in range(10):  # Create 10 accidents
        days_ago = random.randint(1, 180)
        accident_date = datetime.now() - timedelta(days=days_ago)
        
        severity = random.choice(['minor', 'minor', 'moderate', 'severe'])
        vehicles_involved = random.randint(2, 3)
        
        location = random.choice(locations)
        
        try:
            accident_number = f'ACC-2025-{i+1:05d}'
            
            cursor.execute(database_adapter.adapt_sql('''
                INSERT INTO traffic_accidents
                (accident_number, accident_date, location, description, severity,
                 weather_conditions, road_conditions, vehicles_involved, 
                 injuries_count, fatalities_count, damage_estimate, status, reported_by)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            '''), (accident_number, accident_date, location,
                   f'حادث {severity} في {location}', severity,
                   'صافي', 'جيدة', vehicles_involved,
                   random.randint(0, 2) if severity != 'minor' else 0,
                   0, random.randint(5000, 50000), 'reported', 1))
            accident_count += 1
            print(f"   ✓ Accident created: {accident_number}")
        except Exception as e:
            print(f"   ✗ Error creating accident: {str(e)}")
    
    print(f"   ✓ Total accidents created: {accident_count}")
    
    print("\n4. Creating immobilized cars...")
    immobilized_count = 0
    for i in range(5):  # Create 5 immobilized cars
        vehicle = random.choice(vehicles[:5])  # Use first 5 vehicles
        plate = vehicle[0]
        
        days_ago = random.randint(1, 30)
        immobilized_date = datetime.now() - timedelta(days=days_ago)
        
        try:
            # Get vehicle_id
            cursor.execute('SELECT id FROM vehicles WHERE plate_number = ?', (plate,))
            result = cursor.fetchone()
            vehicle_id = result[0] if result else None
            
            outstanding_fines = random.randint(1000, 5000)
            towing_fee = 500
            storage_fee = days_ago * 50
            total_fees = outstanding_fines + towing_fee + storage_fee
            
            cursor.execute(database_adapter.adapt_sql('''
                INSERT INTO immobilized_cars
                (vehicle_id, plate_number, immobilization_type, reason, location,
                 immobilized_date, immobilized_by, outstanding_fines, towing_fee,
                 storage_fee, total_fees, payment_status, status, violation_count)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            '''), (vehicle_id, plate, 'boot', 'عدة مخالفات غير مدفوعة',
                   random.choice(locations), immobilized_date, 1,
                   outstanding_fines, towing_fee, storage_fee, total_fees,
                   'unpaid', 'immobilized', random.randint(3, 8)))
            immobilized_count += 1
            print(f"   ✓ Immobilized car created: {plate}")
        except Exception as e:
            print(f"   ✗ Error creating immobilized car: {str(e)}")
    
    print(f"   ✓ Total immobilized cars created: {immobilized_count}")
    
    print("\n5. Creating driver licenses...")
    license_count = 0
    for i, vehicle in enumerate(vehicles[:7], 1):
        owner = vehicle[1]
        
        try:
            issue_date = datetime.now() - timedelta(days=random.randint(365, 1825))
            expiry_date = issue_date + timedelta(days=3650)  # 10 years
            
            cursor.execute(database_adapter.adapt_sql('''
                INSERT INTO driver_licenses
                (license_number, full_name, national_id, license_type,
                 issue_date, expiry_date, blood_type, license_status, points_balance)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            '''), (f'1{random.randint(100000000, 999999999)}', owner,
                   f'1{random.randint(100000000, 999999999)}', 'خاصة',
                   issue_date, expiry_date,
                   random.choice(['A+', 'A-', 'B+', 'O+', 'AB+']),
                   'active', 24))
            license_count += 1
            print(f"   ✓ Driver license created for: {owner}")
        except Exception as e:
            print(f"   ✗ Error creating license: {str(e)}")
    
    print(f"   ✓ Total driver licenses created: {license_count}")
    
    print("\n6. Creating vehicle registrations...")
    registration_count = 0
    for vehicle in vehicles:
        plate, owner, make, model, year, color = vehicle
        
        try:
            registration_date = datetime(year, 1, 1) + timedelta(days=random.randint(1, 365))
            expiry_date = registration_date + timedelta(days=365)
            
            cursor.execute(database_adapter.adapt_sql('''
                INSERT INTO vehicle_registrations
                (registration_number, plate_number, owner_name, owner_national_id,
                 vehicle_make, vehicle_model, vehicle_year, vehicle_color,
                 vehicle_type, registration_date, expiry_date, registration_status)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            '''), (f'R{random.randint(100000, 999999)}', plate, owner,
                   f'1{random.randint(100000000, 999999999)}',
                   make, model, year, color, 'سيارة',
                   registration_date, expiry_date, 'active'))
            registration_count += 1
            print(f"   ✓ Vehicle registration created: {plate}")
        except Exception as e:
            print(f"   ✗ Error creating registration: {str(e)}")
    
    print(f"   ✓ Total vehicle registrations created: {registration_count}")
    
    conn.commit()
    conn.close()
    
    print("\n" + "=" * 70)
    print("✅ Sample data creation completed successfully!")
    print("=" * 70)
    print("\nSummary:")
    print(f"  • Vehicles: {len(vehicles)}")
    print(f"  • Violations: {violation_count}")
    print(f"  • Accidents: {accident_count}")
    print(f"  • Immobilized Cars: {immobilized_count}")
    print(f"  • Driver Licenses: {license_count}")
    print(f"  • Vehicle Registrations: {registration_count}")
    print("=" * 70)

if __name__ == '__main__':
    try:
        create_sample_traffic_data()
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
