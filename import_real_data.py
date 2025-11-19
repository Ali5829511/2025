#!/usr/bin/env python3
import zipfile
import xml.etree.ElementTree as ET
import os
import sys

def read_excel_data(filename):
    """قراءة بيانات Excel وإرجاعها كقائمة من الصفوف"""
    try:
        with zipfile.ZipFile(filename, 'r') as zip_ref:
            try:
                with zip_ref.open('xl/sharedStrings.xml') as f:
                    tree = ET.parse(f)
                    root = tree.getroot()
                    strings = []
                    for elem in root.iter('{http://schemas.openxmlformats.org/spreadsheetml/2006/main}t'):
                        strings.append(elem.text or '')
            except:
                strings = []

            with zip_ref.open('xl/worksheets/sheet1.xml') as f:
                tree = ET.parse(f)
                root = tree.getroot()

                rows = []
                for row in root.iter('{http://schemas.openxmlformats.org/spreadsheetml/2006/main}row'):
                    row_data = []
                    for cell in row.iter('{http://schemas.openxmlformats.org/spreadsheetml/2006/main}c'):
                        cell_type = cell.get('t')
                        value = cell.find('{http://schemas.openxmlformats.org/spreadsheetml/2006/main}v')
                        if value is not None:
                            if cell_type == 's':
                                try:
                                    row_data.append(strings[int(value.text)])
                                except:
                                    row_data.append('')
                            else:
                                row_data.append(value.text)
                        else:
                            row_data.append('')
                    if row_data:
                        rows.append(row_data)

                return rows
    except Exception as e:
        print(f"خطأ في قراءة {filename}: {e}")
        return []

print("=" * 80)
print("قراءة ملف بيانات السكان")
print("=" * 80)
residents_data = read_excel_data('بيانات السكان.xlsx')
print(f"عدد الصفوف: {len(residents_data)}")
if residents_data:
    print(f"الأعمدة: {residents_data[0]}")
    print(f"عينة من البيانات:")
    for i in range(min(3, len(residents_data))):
        print(f"  {i}: {residents_data[i]}")

print("\n" + "=" * 80)
print("قراءة ملف ملصقات السيارات")
print("=" * 80)
stickers_data = read_excel_data('ملصقات السيارات.xlsx')
print(f"عدد الصفوف: {len(stickers_data)}")
if stickers_data:
    print(f"الأعمدة: {stickers_data[0]}")
    print(f"عينة من البيانات:")
    for i in range(min(3, len(stickers_data))):
        print(f"  {i}: {stickers_data[i]}")

print("\n" + "=" * 80)
print("قراءة ملف المواقف")
print("=" * 80)
parking_data = read_excel_data('المواقف.xlsx')
print(f"عدد الصفوف: {len(parking_data)}")
if parking_data:
    print(f"الأعمدة: {parking_data[0]}")
    print(f"عينة من البيانات:")
    for i in range(min(3, len(parking_data))):
        print(f"  {i}: {parking_data[i]}")

print("\n" + "=" * 80)
print("إنشاء ملفات SQL للاستيراد")
print("=" * 80)

sql_residents = []
sql_vehicles = []
sql_stickers = []
sql_parking = []

print("\nمعالجة بيانات السكان...")
if len(residents_data) > 1:
    headers = residents_data[0]
    for i, row in enumerate(residents_data[1:], 1):
        if len(row) >= 8 and row[1]:
            name = str(row[1]).replace("'", "''")
            unit_type = str(row[2]) if len(row) > 2 and row[2] else 'فلة'
            villa_num = str(row[3]) if len(row) > 3 and row[3] else '0'
            apt_num = str(row[4]) if len(row) > 4 and row[4] else '0'
            phone = str(row[5]) if len(row) > 5 and row[5] else ''

            phone = phone.strip()
            if not phone or phone == '0':
                phone = f'50000{i:04d}'

            national_id = f'10{i:08d}'

            building_prefix = 'V' if unit_type == 'فلة' else 'A'
            building_number = f'{building_prefix}{villa_num}'

            sql_residents.append(f"""
INSERT INTO residents (name, national_id, phone, building_id, unit_number, is_active)
SELECT '{name}', '{national_id}', '{phone}',
       (SELECT id FROM buildings WHERE building_number = '{building_number}' LIMIT 1),
       '{apt_num}', true
WHERE NOT EXISTS (SELECT 1 FROM residents WHERE name = '{name}');
""")

with open('import_residents.sql', 'w', encoding='utf-8') as f:
    f.write("-- استيراد بيانات السكان\n")
    f.write("BEGIN;\n\n")
    for sql in sql_residents[:100]:
        f.write(sql)
    f.write("\nCOMMIT;\n")

print(f"تم إنشاء {len(sql_residents)} سجل سكان")
print(f"تم حفظ أول 100 سجل في import_residents.sql")

print("\nمعالجة بيانات الملصقات...")
if len(stickers_data) > 1:
    for i, row in enumerate(stickers_data[1:], 1):
        if len(row) >= 5 and row[4]:
            sticker_num = str(row[0]) if row[0] else f'STK{i:06d}'
            name = str(row[1]).replace("'", "''") if row[1] else 'غير محدد'
            status = str(row[2]) if row[2] else 'فعال'
            plate = str(row[4]).replace("'", "''") if row[4] else ''
            vehicle_type = str(row[5]).replace("'", "''") if len(row) > 5 and row[5] else 'سيارة'

            if status != 'فعال':
                continue

            sql_stickers.append(f"""
INSERT INTO stickers (sticker_number, resident_id, plate_number, vehicle_type, issue_date, status)
SELECT '{sticker_num}',
       (SELECT id FROM residents WHERE name LIKE '%{name.split()[0]}%' LIMIT 1),
       '{plate}', '{vehicle_type}', CURRENT_DATE, 'active'
WHERE EXISTS (SELECT 1 FROM residents WHERE name LIKE '%{name.split()[0]}%');
""")

with open('import_stickers.sql', 'w', encoding='utf-8') as f:
    f.write("-- استيراد بيانات الملصقات\n")
    f.write("BEGIN;\n\n")
    for sql in sql_stickers[:100]:
        f.write(sql)
    f.write("\nCOMMIT;\n")

print(f"تم إنشاء {len(sql_stickers)} ملصق")
print(f"تم حفظ أول 100 ملصق في import_stickers.sql")

print("\nمعالجة بيانات المواقف...")
if len(parking_data) > 1:
    for i, row in enumerate(parking_data[1:], 1):
        if len(row) >= 5 and row[4]:
            unit_type = str(row[0]) if row[0] else 'شقة'
            building_num = str(row[1]) if row[1] else '0'
            apt_num = str(row[2]) if row[2] else '0'
            parking_area = str(row[3]).replace("'", "''") if row[3] else 'عام'
            spot_number = str(row[4]).replace("'", "''") if row[4] else f'P{i:04d}'

            building_prefix = 'V' if unit_type == 'فلة' else 'A'
            building_number = f'{building_prefix}{building_num}'

            sql_parking.append(f"""
INSERT INTO parking_spots (spot_number, parking_area, building_id, is_occupied)
SELECT '{spot_number}', '{parking_area}',
       (SELECT id FROM buildings WHERE building_number = '{building_number}' LIMIT 1),
       false
WHERE NOT EXISTS (SELECT 1 FROM parking_spots WHERE spot_number = '{spot_number}');
""")

with open('import_parking.sql', 'w', encoding='utf-8') as f:
    f.write("-- استيراد بيانات المواقف\n")
    f.write("BEGIN;\n\n")
    for sql in sql_parking[:100]:
        f.write(sql)
    f.write("\nCOMMIT;\n")

print(f"تم إنشاء {len(sql_parking)} موقف")
print(f"تم حفظ أول 100 موقف في import_parking.sql")

print("\n" + "=" * 80)
print("ملخص البيانات المعالجة")
print("=" * 80)
print(f"السكان: {len(sql_residents)} سجل")
print(f"الملصقات: {len(sql_stickers)} ملصق")
print(f"المواقف: {len(sql_parking)} موقف")
print("\nتم إنشاء ملفات SQL للاستيراد:")
print("  - import_residents.sql")
print("  - import_stickers.sql")
print("  - import_parking.sql")
