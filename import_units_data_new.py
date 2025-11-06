#!/usr/bin/env python3
"""
Script to import residential units data - Updated with exact data from requirements
استيراد بيانات الوحدات السكنية - محدث بالبيانات الدقيقة من المتطلبات
"""

import sqlite3
import os
from datetime import datetime

DATABASE_PATH = os.path.join(os.path.dirname(__file__), 'housing.db')

def get_db_connection():
    """Create and return a database connection"""
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def clear_units_data():
    """Clear existing units data"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    print("🗑️  Clearing existing units data...")
    cursor.execute('DELETE FROM units')
    conn.commit()
    conn.close()
    print("✅ Existing data cleared")

def import_units_data():
    """Import units data from provided list"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    units_data = []
    
    # Villas (فلل) - 114 villas
    print("📝 Adding villas data (114 villas)...")
    for i in range(1, 115):
        units_data.append({
            'name': f'فلة{i}',
            'type': 'villa',
            'description': 'منطفة الفلل',  # Note: matches exact typo in provided data
            'building_number': i,
            'unit_number': 0,
            'status': 'vacant'
        })
    
    # Old Buildings Apartments (المباني القديمة) - Buildings 1-30
    print("📝 Adding old buildings apartments data (Buildings 1-30)...")
    
    # Define apartments for old buildings
    # Each building has apartments: 01-04, 11-14, 21-24, 31-34, 41-44 (20 apartments per building)
    # Except building 10 which is missing apartment 22
    
    old_buildings_apartments = {
        # Building 1 - has duplicate شقة 02 in original data, we'll add only once
        1: [1, 2, 3, 4, 11, 12, 13, 14, 21, 22, 23, 24, 31, 32, 33, 34, 41, 42, 43, 44],
        2: [1, 2, 3, 4, 11, 12, 13, 14, 21, 22, 23, 24, 31, 32, 33, 34, 41, 42, 43, 44],
        3: [1, 2, 3, 4, 11, 12, 13, 14, 21, 22, 23, 24, 31, 32, 33, 34, 41, 42, 43, 44],
        4: [1, 2, 3, 4, 11, 12, 13, 14, 21, 22, 23, 24, 31, 32, 33, 34, 41, 42, 43, 44],
        5: [1, 2, 3, 4, 11, 12, 13, 14, 21, 22, 23, 24, 31, 32, 33, 34, 41, 42, 43, 44],
        6: [1, 2, 3, 4, 11, 12, 13, 14, 21, 22, 23, 24, 31, 32, 33, 34, 41, 42, 43, 44],
        7: [1, 2, 3, 4, 11, 12, 13, 14, 21, 22, 23, 24, 31, 32, 33, 34, 41, 42, 43, 44],
        8: [1, 2, 3, 4, 11, 12, 13, 14, 21, 22, 23, 24, 31, 32, 33, 34, 41, 42, 43, 44],
        9: [1, 2, 3, 4, 11, 12, 13, 14, 21, 22, 23, 24, 31, 32, 33, 34, 41, 42, 43, 44],
        10: [1, 2, 3, 4, 11, 12, 13, 14, 21, 23, 24, 31, 32, 33, 34, 41, 42, 43, 44],  # Missing 22
        11: [1, 2, 3, 4, 11, 12, 13, 14, 21, 22, 23, 24, 31, 32, 33, 34, 41, 42, 43, 44],
        12: [1, 2, 3, 4, 11, 12, 13, 14, 21, 22, 23, 24, 31, 32, 33, 34, 41, 42, 43, 44],
        13: [1, 2, 3, 4, 11, 12, 13, 14, 21, 22, 23, 24, 31, 32, 33, 34, 41, 42, 43, 44],
        14: [1, 2, 3, 4, 11, 12, 13, 14, 21, 22, 23, 24, 31, 32, 33, 34, 41, 42, 43, 44],
        15: [1, 2, 3, 4, 11, 12, 13, 14, 21, 22, 23, 24, 31, 32, 33, 34, 41, 42, 43, 44],
        16: [1, 2, 3, 4, 11, 12, 13, 14, 21, 22, 23, 24, 31, 32, 33, 34, 41, 42, 43, 44],
        17: [1, 2, 3, 4, 11, 12, 13, 14, 21, 22, 23, 24, 31, 32, 33, 34, 41, 42, 43, 44],
        18: [1, 2, 3, 4, 11, 12, 13, 14, 21, 22, 23, 24, 31, 32, 33, 34, 41, 42, 43, 44],
        19: [1, 2, 3, 4, 11, 12, 13, 14, 21, 22, 23, 24, 31, 32, 33, 34, 41, 42, 43, 44],
        20: [1, 2, 3, 4, 11, 12, 13, 14, 21, 22, 23, 24, 31, 32, 33, 34, 41, 42, 43, 44],
        21: [1, 2, 3, 4, 11, 12, 13, 14, 21, 22, 23, 24, 31, 32, 33, 34, 41, 42, 43, 44],
        22: [1, 2, 3, 4, 11, 12, 13, 14, 21, 22, 23, 24, 31, 32, 33, 34, 41, 42, 43, 44],
        23: [1, 2, 3, 4, 11, 12, 13, 14, 21, 22, 23, 24, 31, 32, 33, 34, 41, 42, 43, 44],
        24: [1, 2, 3, 4, 11, 12, 13, 14, 21, 22, 23, 24, 31, 32, 33, 34, 41, 42, 43, 44],
        25: [1, 2, 3, 4, 11, 12, 13, 14, 21, 22, 23, 24, 31, 32, 33, 34, 41, 42, 43, 44],
        26: [1, 2, 3, 4, 11, 12, 13, 14, 21, 22, 23, 24, 31, 32, 33, 34, 41, 42, 43, 44],
        27: [1, 2, 3, 4, 11, 12, 13, 14, 21, 22, 23, 24, 31, 32, 33, 34, 41, 42, 43, 44],
        28: [1, 2, 3, 4, 11, 12, 13, 14, 21, 22, 23, 24, 31, 32, 33, 34, 41, 42, 43, 44],
        29: [1, 2, 3, 4, 11, 12, 13, 14, 21, 22, 23, 24, 31, 32, 33, 34, 41, 42, 43, 44],
        30: [1, 2, 3, 4, 11, 12, 13, 14, 21, 22, 23, 24, 31, 32, 33, 34, 41, 42, 43, 44],
    }
    
    # Special descriptions for specific apartments
    special_descriptions = {
        (7, 4): 'المباني القديمة ( خدمات)',
        (12, 4): 'المباني القديمة( مغسلة)',
        (13, 4): 'المباني القديمة( خدمات)',
        (25, 4): 'المباني القديمة (الامن والسلامة)',
        (30, 4): 'المباني القديمة( صيانة)',
    }
    
    for building_num in range(1, 31):
        apartments = old_buildings_apartments[building_num]
        for apt_num in apartments:
            # Get special description if exists
            description = special_descriptions.get((building_num, apt_num), 'المباني القديمة')
            
            # Format apartment name based on original data
            # Most use "شقة 01 عمارة X" format, some use "شقة 1 عمارة X"
            # Building 16 uses single digit format
            if building_num == 16 and apt_num < 10:
                apt_name = f'شقة {apt_num} عمارة {building_num}'
            elif apt_num == 13 and building_num == 1:
                apt_name = f'شقة {apt_num:d}عمارة {building_num}'
            elif apt_num == 4 and building_num == 4:
                apt_name = f'شقة {apt_num:02d}عمارة {building_num}'
            elif apt_num == 2 and building_num == 5:
                apt_name = f'شقة {apt_num:02d}عمارة {building_num}'
            elif apt_num == 1 and building_num == 6:
                apt_name = f'شقة {apt_num:02d}عمارة {building_num}'
            elif apt_num in [42, 43] and building_num == 5:
                apt_name = f'شقة {apt_num} عمارة {building_num}  '
            elif apt_num == 1 and building_num in [2, 11]:
                apt_name = f'شقة {apt_num:02d}عمارة {building_num}'
            else:
                apt_name = f'شقة {apt_num:02d} عمارة {building_num}'
            
            units_data.append({
                'name': apt_name,
                'type': 'apartment',
                'description': description,
                'building_number': building_num,
                'unit_number': apt_num,
                'status': 'vacant'
            })
    
    # New Buildings Apartments (المباني الجديدة)
    print("📝 Adding new buildings apartments data (Buildings 53-79)...")
    
    # New buildings: 53, 54, 55, 56, 61, 62, 63, 64, 65, 66, 67, 68, 71, 72, 73, 74, 75, 76, 77, 78, 79
    new_buildings = [53, 54, 55, 56, 61, 62, 63, 64, 65, 66, 67, 68, 71, 72, 73, 74, 75, 76, 77, 78, 79]
    
    for building_num in new_buildings:
        # Each new building has apartments: 11-13, 21-23, 31-33, 41-43, 51-53, 61-63, 71-72
        # Floors 1-6 have 3 apartments each (X1, X2, X3)
        # Floor 7 has 2 apartments (71, 72)
        
        for floor in range(1, 8):
            apartments_per_floor = 2 if floor == 7 else 3
            for apt in range(1, apartments_per_floor + 1):
                apt_num = (floor * 10) + apt
                apt_name = f'شقة {apt_num} عمارة {building_num}'
                
                units_data.append({
                    'name': apt_name,
                    'type': 'apartment',
                    'description': 'المباني الجديدة',
                    'building_number': building_num,
                    'unit_number': apt_num,
                    'status': 'vacant'
                })
    
    # Insert all units
    print(f"💾 Inserting {len(units_data)} units into database...")
    
    inserted_count = 0
    for unit in units_data:
        try:
            cursor.execute('''
                INSERT INTO units (name, type, description, building_number, unit_number, status)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                unit['name'],
                unit['type'],
                unit['description'],
                unit['building_number'],
                unit['unit_number'],
                unit['status']
            ))
            inserted_count += 1
        except sqlite3.IntegrityError as e:
            print(f"⚠️  Skipping duplicate: {unit['name']} - {str(e)}")
    
    conn.commit()
    conn.close()
    
    # Count units by type
    villas_count = sum(1 for u in units_data if u['type'] == 'villa')
    old_apts_count = sum(1 for u in units_data if u['type'] == 'apartment' and 'القديمة' in u['description'])
    new_apts_count = sum(1 for u in units_data if u['type'] == 'apartment' and 'الجديدة' in u['description'])
    
    print(f"✅ Successfully imported {inserted_count} units")
    print(f"   - Villas (فلل): {villas_count}")
    print(f"   - Old Buildings Apartments (المباني القديمة): {old_apts_count}")
    print(f"   - New Buildings Apartments (المباني الجديدة): {new_apts_count}")
    print(f"   - Total: {villas_count + old_apts_count + new_apts_count}")

def main():
    """Main function"""
    print("=" * 60)
    print("🏠 Residential Units Data Import")
    print("استيراد بيانات الوحدات السكنية")
    print("=" * 60)
    
    try:
        # Clear existing data
        clear_units_data()
        
        # Import new data
        import_units_data()
        
        print("=" * 60)
        print("✅ Import completed successfully!")
        print("✅ اكتمل الاستيراد بنجاح!")
        print("=" * 60)
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        print(f"❌ خطأ: {str(e)}")
        import traceback
        traceback.print_exc()
        raise

if __name__ == '__main__':
    main()
