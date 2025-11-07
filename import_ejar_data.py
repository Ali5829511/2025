#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script to import property and tenant data from Saudi Ejar platform.
يقوم هذا السكريبت باستيراد بيانات العقارات والمستأجرين من منصة إيجار السعودية

This script imports property, tenant, owner, and contract data from
the Ejar platform (https://eservices.ejar.sa) into the housing database.

Ejar Data Format Expected:
- Properties: Building/Unit information
- Tenants: Resident information  
- Owners: Property owner information
- Contracts: Rental agreement data

Usage:
    python3 import_ejar_data.py <ejar_data_file.csv>
    python3 import_ejar_data.py --sample

Supported file formats: CSV, TSV, Excel (.xlsx)
"""

import sqlite3
import sys
import os
import csv
from datetime import datetime, timedelta
import json

# Sample Ejar data structure
SAMPLE_EJAR_DATA = """نوع_العقار	رقم_العقار	اسم_المالك	رقم_هوية_المالك	اسم_المستأجر	رقم_هوية_المستأجر	جوال_المستأجر	بريد_المستأجر	تاريخ_بدء_العقد	تاريخ_انتهاء_العقد	قيمة_الإيجار_السنوي	حالة_العقد	ملاحظات
فلة	1	إدارة الجامعة	1000000001	يحيى بن علي العمري	1234567890	504444120	yahya@example.com	2024-01-01	2025-12-31	60000	نشط	عضو هيئة تدريس
فلة	2	إدارة الجامعة	1000000001	مشبب بن سعيد القحطاني	1234567891	507665005	moshabbab@example.com	2024-01-01	2025-12-31	60000	نشط	عضو هيئة تدريس
فلة	3	إدارة الجامعة	1000000001	عمر بن عبدالرحمن العمر	1234567892	505828583	omar@example.com	2024-02-01	2025-12-31	60000	نشط	عضو هيئة تدريس
عمارة	101	إدارة الجامعة	1000000001	خالد بن محمد السعيد	1234567893	505111222	khaled@example.com	2024-01-15	2025-12-31	48000	نشط	عضو هيئة تدريس
عمارة	102	إدارة الجامعة	1000000001	فهد بن عبدالله الأحمد	1234567894	505222333	fahad@example.com	2024-03-01	2025-12-31	48000	نشط	عضو هيئة تدريس
عمارة	201	إدارة الجامعة	1000000001	سعد بن سليمان الحربي	1234567895	505333444	saad@example.com	2024-01-20	2025-12-31	48000	نشط	عضو هيئة تدريس
عمارة	202	إدارة الجامعة	1000000001	أحمد بن إبراهيم النصر	1234567896	505444555	ahmed@example.com	2024-02-15	2025-12-31	48000	نشط	عضو هيئة تدريس
فلة	4	إدارة الجامعة	1000000001	محمد بن ناصر اليماني	1234567897	561144374	mohammed@example.com	2024-01-10	2025-12-31	60000	نشط	عضو هيئة تدريس
فلة	5	إدارة الجامعة	1000000001	عبدالرحمن بن محمد الخراشي	1234567898	505233312	abdulrahman@example.com	2024-03-01	2025-12-31	60000	نشط	عضو هيئة تدريس
عمارة	301	إدارة الجامعة	1000000001	وليد بن عبدالعزيز الجندل	1234567899	505473949	waleed@example.com	2024-01-25	2025-12-31	48000	نشط	عضو هيئة تدريس"""


def parse_ejar_date(date_str):
    """Parse date from Ejar format (YYYY-MM-DD)."""
    if not date_str or date_str.strip() == '':
        return None
    try:
        return datetime.strptime(date_str.strip(), '%Y-%m-%d').date()
    except:
        try:
            # Try alternative format
            return datetime.strptime(date_str.strip(), '%d/%m/%Y').date()
        except:
            return None


def create_building_if_not_exists(conn, property_type, property_number):
    """Create a building entry if it doesn't exist.
    
    Args:
        property_type: نوع العقار (فلة/عمارة)
        property_number: رقم العقار
    """
    cursor = conn.cursor()
    
    # Determine building name and number
    if property_type == "فلة":
        building_name = "فلة"
        building_number = str(property_number)
    else:
        # For apartments, extract building number from unit number
        # e.g., 101 -> Building A, 201 -> Building B, etc.
        floor = str(property_number)[0] if len(str(property_number)) > 1 else "1"
        building_name = "عمارة"
        building_number = f"A{floor}"  # Use A1, A2, etc. for apartment buildings
    
    # Check if building exists
    cursor.execute(
        "SELECT id FROM buildings WHERE name = ? AND building_number = ?",
        (building_name, building_number)
    )
    result = cursor.fetchone()
    
    if result:
        return result[0], building_name, building_number
    
    # Create new building
    cursor.execute("""
        INSERT INTO buildings (name, building_number, total_floors, total_units, address, created_at)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        building_name,
        building_number,
        3 if property_type == "عمارة" else 1,  # Apartments have floors
        10 if property_type == "عمارة" else 1,  # Apartments have multiple units
        "إسكان أعضاء هيئة التدريس - جامعة الإمام محمد بن سعود الإسلامية",
        datetime.now()
    ))
    
    conn.commit()
    building_id = cursor.lastrowid
    print(f"  ✅ Created building: {building_name} {building_number}")
    return building_id, building_name, building_number


def import_ejar_property(conn, row_data, stats):
    """Import a single property and tenant record from Ejar data.
    
    Expected columns:
    - نوع_العقار (property_type): فلة/عمارة
    - رقم_العقار (property_number)
    - اسم_المالك (owner_name)
    - رقم_هوية_المالك (owner_id)
    - اسم_المستأجر (tenant_name)
    - رقم_هوية_المستأجر (tenant_id)
    - جوال_المستأجر (tenant_phone)
    - بريد_المستأجر (tenant_email)
    - تاريخ_بدء_العقد (contract_start)
    - تاريخ_انتهاء_العقد (contract_end)
    - قيمة_الإيجار_السنوي (annual_rent)
    - حالة_العقد (contract_status)
    - ملاحظات (notes)
    """
    cursor = conn.cursor()
    
    try:
        property_type = row_data.get('نوع_العقار', '').strip()
        property_number = row_data.get('رقم_العقار', '').strip()
        tenant_name = row_data.get('اسم_المستأجر', '').strip()
        tenant_id = row_data.get('رقم_هوية_المستأجر', '').strip()
        tenant_phone = row_data.get('جوال_المستأجر', '').strip()
        tenant_email = row_data.get('بريد_المستأجر', '').strip()
        contract_start = parse_ejar_date(row_data.get('تاريخ_بدء_العقد', ''))
        contract_status = row_data.get('حالة_العقد', '').strip()
        notes = row_data.get('ملاحظات', '').strip()
        
        # Validate required fields
        if not property_type or not property_number or not tenant_name or not tenant_id:
            print(f"  ⚠️  Skipping invalid row: missing required fields")
            stats['errors'] += 1
            return False
        
        # Create or get building
        building_id, building_name, building_number = create_building_if_not_exists(
            conn, property_type, property_number
        )
        
        # Determine unit number
        if property_type == "فلة":
            unit_number = "0"  # Villas don't have unit numbers
        else:
            unit_number = str(property_number)
        
        # Check if resident already exists
        cursor.execute(
            "SELECT id FROM residents WHERE national_id = ?",
            (tenant_id,)
        )
        existing = cursor.fetchone()
        
        if existing:
            print(f"  ℹ️  Tenant '{tenant_name}' (ID: {tenant_id}) already exists, skipping...")
            stats['skipped'] += 1
            return False
        
        # Insert tenant as resident
        cursor.execute("""
            INSERT INTO residents (
                name, national_id, email, phone, department, job_title,
                building_id, unit_number, move_in_date, is_active, created_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            tenant_name,
            tenant_id,
            tenant_email if tenant_email else None,
            tenant_phone if tenant_phone else '0000000000',
            'عضو هيئة التدريس' if 'هيئة' in notes else None,
            notes if notes else None,
            building_id,
            unit_number if unit_number != "0" else None,
            contract_start if contract_start else datetime.now().date(),
            1 if contract_status == 'نشط' else 0,
            datetime.now()
        ))
        
        conn.commit()
        
        display_unit = f"{building_name} {building_number}" + (f" - وحدة {unit_number}" if unit_number != "0" else "")
        print(f"  ✅ Imported: {tenant_name} → {display_unit}")
        stats['success'] += 1
        return True
        
    except Exception as e:
        print(f"  ❌ Error importing row: {e}")
        stats['errors'] += 1
        conn.rollback()
        return False


def import_from_csv_text(text_data, db_path='housing.db'):
    """Import Ejar data from CSV text format."""
    
    # Check if database exists
    if not os.path.exists(db_path):
        print(f"❌ Database file '{db_path}' not found!")
        print("Please run 'python3 database.py' first to create the database.")
        return
    
    # Connect to database
    conn = sqlite3.connect(db_path)
    
    # Parse CSV
    lines = text_data.strip().split('\n')
    if len(lines) < 2:
        print("❌ No data found in file!")
        return
    
    # Parse header
    header = lines[0].split('\t')
    print(f"📋 Found {len(header)} columns: {', '.join(header[:5])}...")
    print(f"📊 Processing {len(lines)-1} property records...\n")
    
    stats = {
        'success': 0,
        'skipped': 0,
        'errors': 0,
        'total': len(lines) - 1
    }
    
    # Process each row
    for i, line in enumerate(lines[1:], 1):
        if not line.strip():
            continue
        
        values = line.split('\t')
        if len(values) != len(header):
            print(f"  ⚠️  Row {i}: Column count mismatch, skipping...")
            stats['errors'] += 1
            continue
        
        # Create dictionary from header and values
        row_data = dict(zip(header, values))
        import_ejar_property(conn, row_data, stats)
    
    conn.close()
    
    # Print summary
    print(f"\n{'='*70}")
    print(f"📊 Ejar Import Summary / ملخص استيراد بيانات إيجار:")
    print(f"{'='*70}")
    print(f"   ✅ Successfully imported / تم الاستيراد بنجاح: {stats['success']}")
    print(f"   ⏭️  Skipped (duplicates) / تم التخطي (مكرر): {stats['skipped']}")
    print(f"   ❌ Errors / أخطاء: {stats['errors']}")
    print(f"   📝 Total processed / إجمالي المعالج: {stats['total']}")
    print(f"{'='*70}\n")


def import_from_file(filename, db_path='housing.db'):
    """Import Ejar data from CSV/TSV file."""
    
    if not os.path.exists(filename):
        print(f"❌ File '{filename}' not found!")
        return
    
    # Read file with UTF-8 encoding
    with open(filename, 'r', encoding='utf-8-sig') as f:
        content = f.read()
    
    # Check if it's tab-separated or comma-separated
    if '\t' in content:
        import_from_csv_text(content, db_path)
    else:
        # Convert comma-separated to tab-separated
        lines = content.strip().split('\n')
        csv_reader = csv.reader(lines)
        rows = list(csv_reader)
        
        # Convert to tab-separated format
        text_data = '\n'.join(['\t'.join(row) for row in rows])
        import_from_csv_text(text_data, db_path)


def import_sample_data(db_path='housing.db'):
    """Import sample Ejar data for testing."""
    print("📥 Importing sample Ejar data...\n")
    import_from_csv_text(SAMPLE_EJAR_DATA, db_path)


def main():
    """Main function."""
    
    print("="*70)
    print("🏘️  Ejar Data Import Tool / أداة استيراد بيانات إيجار")
    print("="*70)
    print("Import property data from Saudi Ejar platform")
    print("استيراد بيانات العقارات من منصة إيجار السعودية")
    print("="*70)
    print()
    
    if len(sys.argv) < 2:
        print("Usage / الاستخدام:")
        print("  Import from file / استيراد من ملف:")
        print("    python3 import_ejar_data.py <ejar_data_file.csv>")
        print()
        print("  Import sample data / استيراد بيانات نموذجية:")
        print("    python3 import_ejar_data.py --sample")
        print()
        print("Expected file format / تنسيق الملف المتوقع:")
        print("  - CSV or TSV format / صيغة CSV أو TSV")
        print("  - UTF-8 encoding / ترميز UTF-8")
        print("  - Tab or comma separated / مفصولة بفاصلة أو تاب")
        print()
        sys.exit(1)
    
    if sys.argv[1] == '--sample':
        import_sample_data()
    else:
        filename = sys.argv[1]
        print(f"📥 Importing data from file: {filename}\n")
        import_from_file(filename)
    
    print("✨ Import complete! / اكتمل الاستيراد!")
    print("💡 Tip: Visit http://localhost:5000/housing_report.html to view updated data")
    print("💡 نصيحة: زُر http://localhost:5000/housing_report.html لعرض البيانات المحدثة")


if __name__ == '__main__':
    main()
