#!/usr/bin/env python3
"""
Import ALL apartments and parking spots data into the database
استيراد جميع بيانات الشقق والمواقف إلى قاعدة البيانات
Based on the comprehensive apartment numbering scheme
"""

import sqlite3
import os
from datetime import datetime

DATABASE_PATH = os.path.join(os.path.dirname(__file__), 'housing.db')

def create_tables():
    """Create apartments and parking_spots tables if they don't exist"""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    
    # Create apartments table
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
    
    # Create parking_spots table
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
    
    conn.commit()
    conn.close()
    print("✅ Tables created successfully")

def get_building_id(cursor, building_number):
    """Get building ID from building number"""
    cursor.execute('SELECT id FROM buildings WHERE building_number = ?', (str(building_number),))
    result = cursor.fetchone()
    return result[0] if result else None

def generate_apartments_data():
    """Generate comprehensive apartments data based on the new requirements"""
    data = []
    
    # Buildings 1-30 (Old Buildings): apartments 1-4, 11-14, 21-24, 31-34, 41-44
    print("📦 Generating data for buildings 1-30 (Old Buildings)...")
    for building_num in range(1, 31):
        apartment_numbers = ['1', '2', '3', '4', '11', '12', '13', '14', 
                            '21', '22', '23', '24', '31', '32', '33', '34', 
                            '41', '42', '43', '44']
        for apt_num in apartment_numbers:
            data.append(("شقة", str(building_num), apt_num, "G . L . P - 7", f"{building_num}-{apt_num}"))
    
    # Buildings 53-56 (New Buildings): apartments 11-13, 21-23, 31-33, 41-43, 51-53, 61-63, 71-72
    print("📦 Generating data for buildings 53-56 (New Buildings)...")
    for building_num in range(53, 57):
        apartment_numbers = ['11', '12', '13', '21', '22', '23', 
                            '31', '32', '33', '41', '42', '43', 
                            '51', '52', '53', '61', '62', '63', 
                            '71', '72']
        for apt_num in apartment_numbers:
            data.append(("شقة", str(building_num), apt_num, "G . L . P - 8", f"{building_num}-{apt_num}"))
    
    # Buildings 61-68 (New Buildings): apartments 11-13, 21-23, 31-33, 41-43, 51-53, 61-63, 71-72
    print("📦 Generating data for buildings 61-68 (New Buildings)...")
    for building_num in range(61, 69):
        apartment_numbers = ['11', '12', '13', '21', '22', '23', 
                            '31', '32', '33', '41', '42', '43', 
                            '51', '52', '53', '61', '62', '63', 
                            '71', '72']
        for apt_num in apartment_numbers:
            data.append(("شقة", str(building_num), apt_num, "G . L . P - 9", f"{building_num}-{apt_num}"))
    
    # Buildings 71-79 (New Buildings): apartments 11-13, 21-23, 31-33, 41-43, 51-53, 61-63, 71-72
    print("📦 Generating data for buildings 71-79 (New Buildings)...")
    for building_num in range(71, 80):
        apartment_numbers = ['11', '12', '13', '21', '22', '23', 
                            '31', '32', '33', '41', '42', '43', 
                            '51', '52', '53', '61', '62', '63', 
                            '71', '72']
        for apt_num in apartment_numbers:
            data.append(("شقة", str(building_num), apt_num, "G . L . P - 10", f"{building_num}-{apt_num}"))
    
    return data

def import_apartments_and_parking():
    """Import apartments and parking data"""
    
    # Generate data
    data = generate_apartments_data()
    
    try:
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        
        apartments_added = 0
        parking_added = 0
        skipped = 0
        
        print(f"\n📊 Processing {len(data)} apartment-parking pairs...")
        
        for unit_type, building_num, apt_num, parking_area, parking_spot in data:
            # Get building ID
            building_id = get_building_id(cursor, building_num)
            
            if not building_id:
                print(f"⚠️  Building {building_num} not found, skipping")
                skipped += 1
                continue
            
            # Calculate floor number from apartment number
            try:
                floor_number = int(apt_num) // 10 if int(apt_num) >= 10 else 0
            except:
                floor_number = 0
            
            try:
                # Insert apartment
                cursor.execute('''
                    INSERT INTO apartments (building_id, unit_number, floor_number, unit_type)
                    VALUES (?, ?, ?, ?)
                ''', (building_id, apt_num, floor_number, unit_type))
                
                apartment_id = cursor.lastrowid
                apartments_added += 1
                
                # Insert parking spot
                cursor.execute('''
                    INSERT INTO parking_spots (spot_number, parking_area, building_id, apartment_id)
                    VALUES (?, ?, ?, ?)
                ''', (parking_spot, parking_area, building_id, apartment_id))
                
                parking_added += 1
                
            except sqlite3.IntegrityError as e:
                skipped += 1
                # Don't print each duplicate to avoid clutter
        
        conn.commit()
        
        # Show summary
        print("\n" + "=" * 60)
        print("✅ Import completed successfully!")
        print("✅ تم الاستيراد بنجاح!")
        print("=" * 60)
        print(f"📊 Apartments added: {apartments_added}")
        print(f"📊 Parking spots added: {parking_added}")
        if skipped > 0:
            print(f"⚠️  Skipped (duplicates or missing buildings): {skipped}")
        print("=" * 60)
        
        # Show breakdown by building category
        cursor.execute('''
            SELECT 
                CASE 
                    WHEN CAST(b.building_number AS INTEGER) BETWEEN 1 AND 30 THEN 'المباني القديمة (1-30)'
                    WHEN CAST(b.building_number AS INTEGER) BETWEEN 53 AND 56 THEN 'المباني الجديدة (53-56)'
                    WHEN CAST(b.building_number AS INTEGER) BETWEEN 61 AND 68 THEN 'المباني الجديدة (61-68)'
                    WHEN CAST(b.building_number AS INTEGER) BETWEEN 71 AND 79 THEN 'المباني الجديدة (71-79)'
                    ELSE 'أخرى'
                END as category,
                COUNT(DISTINCT b.id) as buildings_count,
                COUNT(a.id) as apartments_count
            FROM buildings b
            LEFT JOIN apartments a ON b.id = a.building_id
            WHERE b.building_number NOT LIKE 'V%'
            GROUP BY category
            ORDER BY MIN(CAST(b.building_number AS INTEGER))
        ''')
        
        results = cursor.fetchall()
        print("\n📈 Summary by Category / الملخص حسب الفئة:")
        print("-" * 60)
        total_buildings = 0
        total_apartments = 0
        for row in results:
            print(f"  {row[0]}: {row[1]} مبنى، {row[2]} شقة")
            total_buildings += row[1]
            total_apartments += row[2]
        print("-" * 60)
        print(f"  الإجمالي: {total_buildings} مبنى، {total_apartments} شقة")
        print("=" * 60)
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    print("=" * 60)
    print("Comprehensive Apartments and Parking Import Script")
    print("برنامج استيراد شامل لبيانات الشقق والمواقف")
    print("=" * 60)
    create_tables()
    import_apartments_and_parking()
