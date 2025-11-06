#!/usr/bin/env python3
"""
Script to import residential units data
استيراد بيانات الوحدات السكنية
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
    print("📝 Adding villas data...")
    for i in range(1, 115):
        units_data.append({
            'name': f'فلة{i}',
            'type': 'villa',
            'description': 'منطقة الفلل',
            'building_number': i,
            'unit_number': 0,
            'status': 'vacant'
        })
    
    # Old Buildings Apartments (المباني القديمة)
    print("📝 Adding old buildings apartments data...")
    old_buildings = range(1, 31)  # Buildings 1-30
    
    for building_num in old_buildings:
        # Each old building has apartments on floors: 0, 1, 2, 3, 4
        # Floor 0: apartments 1-4
        # Floor 1: apartments 11-14
        # Floor 2: apartments 21-24
        # Floor 3: apartments 31-34
        # Floor 4: apartments 41-44
        
        for floor in [0, 1, 2, 3, 4]:
            for apt in range(1, 5):
                apt_number = (floor * 10) + apt if floor > 0 else apt
                
                # Special cases with services/facilities
                description = 'المباني القديمة'
                if building_num == 7 and apt_number == 4:
                    description = 'المباني القديمة ( خدمات)'
                elif building_num == 12 and apt_number == 4:
                    description = 'المباني القديمة( مغسلة)'
                elif building_num == 13 and apt_number == 4:
                    description = 'المباني القديمة( خدمات)'
                elif building_num == 25 and apt_number == 4:
                    description = 'المباني القديمة (الامن والسلامة)'
                elif building_num == 30 and apt_number == 4:
                    description = 'المباني القديمة( صيانة)'
                
                # Skip apartment 22 in building 10 (missing in data)
                if building_num == 10 and apt_number == 22:
                    continue
                
                units_data.append({
                    'name': f'شقة {apt_number:02d} عمارة {building_num}',
                    'type': 'apartment',
                    'description': description,
                    'building_number': building_num,
                    'unit_number': apt_number,
                    'status': 'vacant'
                })
    
    # New Buildings Apartments (المباني الجديدة)
    print("📝 Adding new buildings apartments data...")
    new_buildings = [53, 54, 55, 56, 61, 62, 63, 64, 65, 66, 67, 68, 71, 72, 73, 74, 75, 76, 77, 78, 79]
    
    for building_num in new_buildings:
        # Each new building has apartments on floors: 1, 2, 3, 4, 5, 6, 7
        # Each floor has 3 apartments (except floor 7 which has 2)
        
        for floor in range(1, 8):
            apartments_per_floor = 2 if floor == 7 else 3
            for apt in range(1, apartments_per_floor + 1):
                apt_number = (floor * 10) + apt
                
                units_data.append({
                    'name': f'شقة {apt_number} عمارة {building_num}',
                    'type': 'apartment',
                    'description': 'المباني الجديدة',
                    'building_number': building_num,
                    'unit_number': apt_number,
                    'status': 'vacant'
                })
    
    # Insert all units
    print(f"💾 Inserting {len(units_data)} units into database...")
    
    for unit in units_data:
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
    
    conn.commit()
    conn.close()
    
    print(f"✅ Successfully imported {len(units_data)} units")
    print(f"   - Villas: 114")
    print(f"   - Old Buildings Apartments: ~{20*20} (30 buildings)")
    print(f"   - New Buildings Apartments: ~{21*20} (21 buildings)")

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
        raise

if __name__ == '__main__':
    main()
