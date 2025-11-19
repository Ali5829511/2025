#!/usr/bin/env python3
import os
import sys
import zipfile
import xml.etree.ElementTree as ET
from urllib import request, parse
import json

SUPABASE_URL = os.getenv('SUPABASE_URL', '')
SUPABASE_KEY = os.getenv('SUPABASE_ANON_KEY', '')

def execute_sql(query):
    """تنفيذ استعلام SQL في Supabase"""
    url = f"{SUPABASE_URL}/rest/v1/rpc/execute_sql"
    headers = {
        'apikey': SUPABASE_KEY,
        'Authorization': f'Bearer {SUPABASE_KEY}',
        'Content-Type': 'application/json'
    }
    data = json.dumps({'query': query}).encode('utf-8')

    try:
        req = request.Request(url, data=data, headers=headers, method='POST')
        with request.urlopen(req) as response:
            return response.read().decode('utf-8')
    except Exception as e:
        print(f"خطأ في تنفيذ SQL: {e}")
        return None

def read_excel_data(filename):
    """قراءة بيانات Excel"""
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
print("استيراد البيانات الحقيقية إلى Supabase")
print("=" * 80)

print("\nاستيراد بيانات السكان...")
residents_data = read_excel_data('بيانات السكان.xlsx')
residents_imported = 0

if len(residents_data) > 1:
    for i, row in enumerate(residents_data[1:101], 1):
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

            print(f"  {i}. {name[:30]}... -> {building_number}")
            residents_imported += 1

print(f"\nتم معالجة {residents_imported} سكان (عينة من أول 100)")

print("\n" + "=" * 80)
print("ملاحظة: استخدم Supabase SQL Editor لاستيراد البيانات الكاملة")
print("=" * 80)
print("الملفات الجاهزة للاستيراد:")
print("  - import_residents.sql (أول 100 سجل)")
print("  - import_stickers.sql (أول 100 ملصق)")
print("  - import_parking.sql (أول 100 موقف)")
