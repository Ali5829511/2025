#!/usr/bin/env python3
"""
Import apartments and parking spots data into the database
استيراد بيانات الشقق والمواقف إلى قاعدة البيانات
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

def import_apartments_and_parking():
    """Import apartments and parking data"""
    
    # Data from the comment - format: (unit_type, building_number, apartment_number, parking_area, parking_spot)
    data = [
        # Building 1
        ("شقة", "1", "1", "G . L . P - 7", "1-1"),
        ("شقة", "1", "2", "G . L . P - 7", "1-2"),
        ("شقة", "1", "3", "G . L . P - 7", "1-3"),
        ("شقة", "1", "4", "G . L . P - 7", "1-4"),
        ("شقة", "1", "11", "G . L . P - 7", "1-11"),
        ("شقة", "1", "12", "G . L . P - 7", "1-12"),
        ("شقة", "1", "13", "G . L . P - 7", "1-13"),
        ("شقة", "1", "14", "G . L . P - 7", "1-14"),
        ("شقة", "1", "21", "G . L . P - 7", "1-21"),
        ("شقة", "1", "22", "G . L . P - 7", "1-22"),
        ("شقة", "1", "23", "G . L . P - 7", "1-23"),
        ("شقة", "1", "24", "G . L . P - 7", "1-24"),
        ("شقة", "1", "31", "G . L . P - 7", "1-31"),
        ("شقة", "1", "32", "G . L . P - 7", "1-32"),
        ("شقة", "1", "33", "G . L . P - 7", "1-33"),
        ("شقة", "1", "34", "G . L . P - 7", "1-34"),
        ("شقة", "1", "41", "G . L . P - 7", "1-41"),
        ("شقة", "1", "42", "G . L . P - 7", "1-42"),
        ("شقة", "1", "43", "G . L . P - 7", "1-43"),
        ("شقة", "1", "44", "G . L . P - 7", "1-44"),
        
        # Building 2
        ("شقة", "2", "1", "G . L . P - 7", "2-1"),
        ("شقة", "2", "2", "G . L . P - 7", "2-2"),
        ("شقة", "2", "3", "G . L . P - 7", "2-3"),
        ("شقة", "2", "4", "G . L . P - 7", "2-4"),
        ("شقة", "2", "11", "G . L . P - 7", "2-11"),
        ("شقة", "2", "12", "G . L . P - 7", "2-12"),
        ("شقة", "2", "13", "G . L . P - 7", "2-13"),
        ("شقة", "2", "14", "G . L . P - 7", "2-14"),
        ("شقة", "2", "21", "G . L . P - 7", "2-21"),
        ("شقة", "2", "22", "G . L . P - 7", "2-22"),
        ("شقة", "2", "23", "G . L . P - 7", "2-23"),
        ("شقة", "2", "24", "G . L . P - 7", "2-24"),
        ("شقة", "2", "31", "G . L . P - 7", "2-31"),
        ("شقة", "2", "32", "G . L . P - 7", "2-32"),
        ("شقة", "2", "33", "G . L . P - 7", "2-33"),
        ("شقة", "2", "34", "G . L . P - 7", "2-34"),
        ("شقة", "2", "41", "G . L . P - 7", "2-41"),
        ("شقة", "2", "42", "G . L . P - 7", "2-42"),
        ("شقة", "2", "43", "G . L . P - 7", "2-43"),
        ("شقة", "2", "44", "G . L . P - 7", "2-44"),
        
        # Building 3
        ("شقة", "3", "1", "G . L . P - 7", "3-1"),
        ("شقة", "3", "2", "G . L . P - 7", "3-2"),
        ("شقة", "3", "3", "G . L . P - 7", "3-3"),
        ("شقة", "3", "4", "G . L . P - 7", "3-4"),
        ("شقة", "3", "11", "G . L . P - 7", "3-11"),
        ("شقة", "3", "12", "G . L . P - 7", "3-12"),
        ("شقة", "3", "13", "G . L . P - 7", "3-13"),
        ("شقة", "3", "14", "G . L . P - 7", "3-14"),
        ("شقة", "3", "21", "G . L . P - 7", "3-21"),
        ("شقة", "3", "22", "G . L . P - 7", "3-22"),
        ("شقة", "3", "23", "G . L . P - 7", "3-23"),
        ("شقة", "3", "24", "G . L . P - 7", "3-24"),
        ("شقة", "3", "31", "G . L . P - 7", "3-31"),
        ("شقة", "3", "32", "G . L . P - 7", "3-32"),
        ("شقة", "3", "33", "G . L . P - 7", "3-33"),
        ("شقة", "3", "34", "G . L . P - 7", "3-34"),
        ("شقة", "3", "41", "G . L . P - 7", "3-41"),
        ("شقة", "3", "42", "G . L . P - 7", "3-42"),
        ("شقة", "3", "43", "G . L . P - 7", "3-43"),
        ("شقة", "3", "44", "G . L . P - 7", "3-44"),
        
        # Building 4
        ("شقة", "4", "1", "G . L . P - 6", "4-1"),
        ("شقة", "4", "2", "G . L . P - 6", "4-2"),
        ("شقة", "4", "3", "G . L . P - 6", "4-3"),
        ("شقة", "4", "4", "G . L . P - 6", "4-4"),
        ("شقة", "4", "11", "G . L . P - 6", "4-11"),
        ("شقة", "4", "12", "G . L . P - 6", "4-12"),
        ("شقة", "4", "13", "G . L . P - 6", "4-13"),
        ("شقة", "4", "14", "G . L . P - 6", "4-14"),
        ("شقة", "4", "21", "G . L . P - 6", "4-21"),
        ("شقة", "4", "22", "G . L . P - 6", "4-22"),
    ]
    
    try:
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        
        apartments_added = 0
        parking_added = 0
        
        for unit_type, building_num, apt_num, parking_area, parking_spot in data:
            # Get building ID
            building_id = get_building_id(cursor, building_num)
            
            if not building_id:
                print(f"⚠️  Building {building_num} not found, skipping")
                continue
            
            # Calculate floor number from apartment number
            floor_number = int(apt_num) // 10 if int(apt_num) >= 10 else 0
            
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
                print(f"⚠️  Skipping duplicate: Building {building_num}, Apt {apt_num} - {e}")
        
        conn.commit()
        
        # Show summary
        print("\n" + "=" * 60)
        print("✅ Import completed successfully!")
        print("✅ تم الاستيراد بنجاح!")
        print("=" * 60)
        print(f"📊 Apartments added: {apartments_added}")
        print(f"📊 Parking spots added: {parking_added}")
        print("=" * 60)
        
        # Show breakdown by building
        cursor.execute('''
            SELECT b.name, b.building_number, COUNT(a.id) as apt_count, COUNT(p.id) as parking_count
            FROM buildings b
            LEFT JOIN apartments a ON b.id = a.building_id
            LEFT JOIN parking_spots p ON b.id = p.building_id
            WHERE b.building_number IN ('1', '2', '3', '4')
            GROUP BY b.id
            ORDER BY b.building_number
        ''')
        
        results = cursor.fetchall()
        print("\n📈 Summary by Building / الملخص حسب المبنى:")
        print("-" * 60)
        for row in results:
            print(f"  {row[0]} (رقم {row[1]}): {row[2]} شقة، {row[3]} موقف")
        print("=" * 60)
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == '__main__':
    print("=" * 60)
    print("Apartments and Parking Import Script")
    print("برنامج استيراد بيانات الشقق والمواقف")
    print("=" * 60)
    create_tables()
    import_apartments_and_parking()
