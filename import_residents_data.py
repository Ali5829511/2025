#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script to import resident data from CSV format into the housing database.
This script reads resident information including names, building numbers, 
unit numbers, phone numbers, and parking spaces, then populates the database.

Usage:
    python3 import_residents_data.py <csv_file>
    
Or import sample data:
    python3 import_residents_data.py --sample
"""

import sqlite3
import sys
import os
from datetime import datetime

# Sample data based on provided information
SAMPLE_DATA = """م	الاسم	الوحدة السكنية	فلة/عمارة	شقة	رقم الجوال	رقم الموقف	مربع الوقوف
1	يحيى بن علي بن يحيى العمري	فلة	1	0	504444120	0	0
2	مشبب بن سعيد بن ظويفر القحطاني	فلة	2	0	507665005	0	0
3	عمر بن عبدالرحمن بن محمد العمر	فلة	3	0	505828583	0	0
4	يحيى بن صالح بن إبراهيم الطويان	فلة	4	0	504205092	0	0
5	محمد بن ناجي بن ناصر اليماني	فلة	5	0	561144374	0	0
6	عبدالرحمن بن محمد بن عبدالرحمن الخراشي	فلة	6	0	505233312	0	0
7	عبدالكريم بن عبدالله بن محمد العبدالكريم	فلة	7	0	505946304	0	0
8	عبدالله بن محمد بن عبدالعزيز المفلح	فلة	8	0	500688896	0	0
9	عبدالله بن ثاني بن عامق الرويلي	فلة	9	0	556311136	0	0
10	خالد بن عبدالعزيز بن محمد الداود	فلة	10	0	555466211	0	0
11	أحمد بن عبدالله بن أحمد الجميد ((السالم))	فلة	11	0	505407387	0	0
12	عبدالحميد بن عبدالله بن ناصر المجلي	فلة	12	0	503116763	0	0
13	إبراهيم بن عبدالله بن عبدالعزيز السعدان	فلة	13	0	555525285	0	0
14	محمد بن عبدالعزيز بن محمد أباعود	فلة	14	0	504254745	0	0
15	محمد بن عبدالعزيز بن محمد الفيصل	فلة	15	0	554447423	0	0
16	إبراهيم بن زيد بن حمد الفحيلة	فلة	16	0	555210570	0	0
17	أمل بنت سليمان بن محمد السيف	فلة	17	0	546090808	0	0
18	حياة بنت يوسف بن منصور الصبياني	فلة	18	0	503428297	0	0
19	عبدالعزيز بن محمد بن عبدالله السحيباني	فلة	19	0	505498660	0	0
20	صالح بن فهد بن صالح العصيمي	فلة	20	0	505488897	0	0
21	عبدالله بن عبدالرحمن بن عبدالعزيز التريكي	فلة	21	0	505267647	0	0
22	عبدالرحمن بن عبدالله بن عبدالعزيز الخضيري	فلة	22	0	505486484	0	0
23	ضيف الله بن دليم بن فيحان العتيبي	فلة	23	0	503138437	0	0
24	أحمد بن محمد بن محمد النشوان	فلة	24	0	504445574	0	0
25	وليد بن عبدالعزيز بن سليمان الجندل	فلة	25	0	505473949	0	0
26	مشعل بن سليمان بن عواد العنزي	فلة	26	0	567778911	0	0
27	عبدالكريم بن عبدالعزيز بن أحمد المحرج	فلة	27	0	505783432	0	0
28	سليمان بن سليمان بن عبد العزيز العنقري	فلة	28	0	505103580	0	0
29	وعد بنت محمد بن عبدالله الحوشان	فلة	29	0	554334240	0	0
30	عبدالعزيز بن ناصر بن عبدالعزيز التميمي	فلة	30	0	555139319	0	0"""


def create_building_if_not_exists(conn, building_name, building_number):
    """Create a building entry if it doesn't exist."""
    cursor = conn.cursor()
    
    # Check if building exists
    cursor.execute("SELECT id FROM buildings WHERE name = ? AND building_number = ?", (building_name, building_number))
    result = cursor.fetchone()
    
    if result:
        return result[0]
    
    # Create new building
    cursor.execute("""
        INSERT INTO buildings (name, building_number, total_floors, total_units, created_at)
        VALUES (?, ?, ?, ?, ?)
    """, (building_name, building_number, 1, 1, datetime.now()))
    
    conn.commit()
    return cursor.lastrowid


def import_resident_data(conn, row_data):
    """Import a single resident record."""
    cursor = conn.cursor()
    
    # Parse row data
    parts = row_data.split('\t')
    if len(parts) < 8:
        print(f"⚠️  Skipping invalid row: {row_data[:50]}...")
        return False
    
    try:
        seq = int(parts[0])
        name = parts[1].strip()
        unit_type_name = parts[2].strip()  # "فلة" or "عمارة" - unit type
        building_num = parts[3].strip()    # Building number
        unit_num = parts[4].strip()        # Unit/apartment number
        phone = parts[5].strip()
        parking_num = parts[6].strip() if len(parts) > 6 else "0"
        parking_spot = parts[7].strip() if len(parts) > 7 else "0"
    except (ValueError, IndexError) as e:
        print(f"⚠️  Error parsing row: {e}")
        return False
    
    # Determine building type
    if unit_type_name == "فلة":
        building_name = f"فلة"
        building_number = building_num
    else:
        building_name = f"عمارة"
        building_number = building_num
    
    # Create building if not exists
    building_id = create_building_if_not_exists(conn, building_name, building_number)
    
    # Check if resident already exists
    cursor.execute("SELECT id FROM residents WHERE name = ? AND building_id = ?", 
                  (name, building_id))
    if cursor.fetchone():
        print(f"ℹ️  Resident '{name}' already exists in {building_name} {building_number}, skipping...")
        return False
    
    # Generate a unique national_id (using phone number as base)
    national_id = f"ID{phone[:10]}" if phone and phone != "0" else f"ID{seq:010d}"
    
    # Insert resident
    try:
        cursor.execute("""
            INSERT INTO residents (
                name, national_id, building_id, unit_number, phone, 
                email, move_in_date, is_active, created_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            name,
            national_id,
            building_id,
            unit_num if unit_num != "0" else None,
            phone if phone and phone != "0" else "0000000000",  # phone is required
            None,  # email
            datetime.now().date(),
            1,  # is_active
            datetime.now()
        ))
        
        conn.commit()
        print(f"✅ Imported: {name} → {building_name} {building_number}")
        return True
        
    except sqlite3.IntegrityError as e:
        print(f"⚠️  Error importing {name}: {e}")
        return False


def import_from_text(text_data, db_path='housing.db'):
    """Import resident data from text format."""
    
    # Check if database exists
    if not os.path.exists(db_path):
        print(f"❌ Database file '{db_path}' not found!")
        print("Please run 'python3 database.py' first to create the database.")
        return
    
    # Connect to database
    conn = sqlite3.connect(db_path)
    
    lines = text_data.strip().split('\n')
    
    # Skip header line
    header = lines[0]
    print(f"📋 Header: {header}")
    print(f"📊 Processing {len(lines)-1} resident records...\n")
    
    success_count = 0
    skip_count = 0
    error_count = 0
    
    for line in lines[1:]:
        if not line.strip():
            continue
            
        result = import_resident_data(conn, line)
        if result:
            success_count += 1
        elif result is False:
            skip_count += 1
        else:
            error_count += 1
    
    conn.close()
    
    print(f"\n{'='*60}")
    print(f"📊 Import Summary:")
    print(f"   ✅ Successfully imported: {success_count}")
    print(f"   ⏭️  Skipped (duplicates): {skip_count}")
    print(f"   ❌ Errors: {error_count}")
    print(f"   📝 Total processed: {success_count + skip_count + error_count}")
    print(f"{'='*60}\n")


def import_from_file(filename, db_path='housing.db'):
    """Import resident data from CSV file."""
    
    if not os.path.exists(filename):
        print(f"❌ File '{filename}' not found!")
        return
    
    with open(filename, 'r', encoding='utf-8') as f:
        text_data = f.read()
    
    import_from_text(text_data, db_path)


def main():
    """Main function."""
    
    print("="*60)
    print("🏘️  Housing Residents Data Import Tool")
    print("="*60)
    print()
    
    if len(sys.argv) < 2:
        print("Usage:")
        print("  Import from file:  python3 import_residents_data.py <csv_file>")
        print("  Import sample data: python3 import_residents_data.py --sample")
        print()
        sys.exit(1)
    
    if sys.argv[1] == '--sample':
        print("📥 Importing sample resident data...\n")
        import_from_text(SAMPLE_DATA)
    else:
        filename = sys.argv[1]
        print(f"📥 Importing data from file: {filename}\n")
        import_from_file(filename)
    
    print("✨ Import complete!")
    print("💡 Tip: Visit http://localhost:5000/housing_report.html to view the updated report")


if __name__ == '__main__':
    main()
