"""
Create sample data for testing vehicle reports
إنشاء بيانات تجريبية لاختبار تقارير السيارات
"""

import database
from datetime import datetime, timedelta
import random

def create_sample_data():
    """Create sample vehicles and violations"""
    conn = database.get_db_connection()
    cursor = conn.cursor()
    
    # Sample data
    vehicle_types = ['سيدان', 'SUV', 'شاحنة صغيرة', 'دفع رباعي']
    makes = ['تويوتا', 'هيونداي', 'نيسان', 'مازدا', 'شيفروليه', 'فورد', 'هوندا']
    models = ['كامري', 'إلنترا', 'سوناتا', 'ألتيما', 'سيلفرادو', 'F-150', 'أكورد']
    colors = ['أبيض', 'أسود', 'فضي', 'رمادي', 'أزرق', 'أحمر']
    
    violation_types = [
        'وقوف في مكان ممنوع',
        'تجاوز السرعة',
        'عدم الالتزام بالمسار',
        'وقوف في موقف ذوي الاحتياجات',
        'عدم التقيد بالإشارات'
    ]
    
    locations = [
        'موقف المبنى A',
        'موقف المبنى B',
        'منطقة الفلل',
        'المدخل الرئيسي',
        'الشارع الداخلي'
    ]
    
    print("Creating sample residents and vehicles...")
    
    # Create sample residents and vehicles
    for i in range(1, 11):
        # Create resident
        cursor.execute('''
            INSERT INTO residents (name, national_id, phone, email, department, job_title, unit_number, is_active)
            VALUES (?, ?, ?, ?, ?, ?, ?, 1)
        ''', (
            f'أ.د. محمد أحمد {i}',
            f'10{i:08d}',
            f'0501234{i:03d}',
            f'user{i}@university.edu.sa',
            'كلية الهندسة',
            'أستاذ',
            f'A-{i:03d}'
        ))
        resident_id = cursor.lastrowid
        
        # Create 1-2 vehicles per resident
        num_vehicles = random.randint(1, 2)
        for v in range(num_vehicles):
            plate_number = f'ABC-{i}{v}{random.randint(100, 999)}'
            
            cursor.execute('''
                INSERT INTO vehicles (
                    plate_number, owner_id, vehicle_type, make, model, year, color,
                    sticker_number, sticker_issued_date, is_active
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, 1)
            ''', (
                plate_number,
                resident_id,
                random.choice(vehicle_types),
                random.choice(makes),
                random.choice(models),
                random.randint(2015, 2024),
                random.choice(colors),
                f'STK-{i:04d}{v}',
                (datetime.now() - timedelta(days=random.randint(30, 365))).date()
            ))
            vehicle_id = cursor.lastrowid
            
            # Create random violations (0-3 per vehicle)
            num_violations = random.randint(0, 3)
            for _ in range(num_violations):
                violation_date = datetime.now() - timedelta(days=random.randint(1, 180))
                
                cursor.execute('''
                    INSERT INTO traffic_violations (
                        vehicle_id, violation_type, violation_date, location,
                        description, fine_amount, status, reported_by
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, 1)
                ''', (
                    vehicle_id,
                    random.choice(violation_types),
                    violation_date,
                    random.choice(locations),
                    'تم رصد المخالفة من قبل الأمن',
                    random.choice([100, 150, 200, 300, 500]),
                    random.choice(['pending', 'resolved', 'appealed'])
                ))
    
    conn.commit()
    conn.close()
    
    print("✅ Sample data created successfully!")
    print("   - 10 residents")
    print("   - 10-20 vehicles")
    print("   - Random violations")

if __name__ == '__main__':
    print("=" * 60)
    print("📊 Creating Sample Data for Vehicle Reports")
    print("إنشاء بيانات تجريبية لتقارير السيارات")
    print("=" * 60)
    print()
    
    try:
        create_sample_data()
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
