"""
Historical Vehicle Data Import Module
نظام استيراد البيانات التاريخية للسيارات

This module imports historical vehicle and violation data from Excel files.
"""

import pandas as pd
import database
from datetime import datetime
import os


def import_vehicles_from_excel(file_path: str, merge_mode: bool = True) -> dict:
    """
    Import vehicles from Excel file
    استيراد السيارات من ملف Excel
    
    Args:
        file_path: Path to Excel file
        merge_mode: If True, merge with existing data; if False, skip duplicates
    
    Returns:
        Dict with import statistics
    """
    try:
        # Read Excel file
        df = pd.read_excel(file_path)
        
        # Expected columns (flexible matching)
        column_mappings = {
            'plate_number': ['رقم اللوحة', 'plate_number', 'Plate Number', 'رقم_اللوحة'],
            'vehicle_type': ['نوع السيارة', 'vehicle_type', 'Vehicle Type', 'نوع_السيارة'],
            'make': ['الماركة', 'make', 'Make', 'ماركة'],
            'model': ['الموديل', 'model', 'Model', 'موديل'],
            'year': ['السنة', 'year', 'Year', 'سنة'],
            'color': ['اللون', 'color', 'Color', 'لون'],
            'owner_name': ['اسم المالك', 'owner_name', 'Owner Name', 'اسم_المالك'],
            'owner_national_id': ['الرقم الوطني', 'national_id', 'National ID', 'الرقم_الوطني'],
            'sticker_number': ['رقم الملصق', 'sticker_number', 'Sticker Number', 'رقم_الملصق'],
        }
        
        # Map columns
        mapped_columns = {}
        for standard_name, possible_names in column_mappings.items():
            for col in df.columns:
                if col in possible_names:
                    mapped_columns[col] = standard_name
                    break
        
        # Rename columns
        df = df.rename(columns=mapped_columns)
        
        # Import statistics
        stats = {
            'total': len(df),
            'imported': 0,
            'skipped': 0,
            'errors': 0,
            'error_details': []
        }
        
        conn = database.get_db_connection()
        cursor = conn.cursor()
        
        for index, row in df.iterrows():
            try:
                plate_number = str(row.get('plate_number', '')).strip()
                
                if not plate_number:
                    stats['skipped'] += 1
                    continue
                
                # Check if vehicle exists
                cursor.execute('SELECT id, owner_id FROM vehicles WHERE plate_number = ?', (plate_number,))
                existing_vehicle = cursor.fetchone()
                
                # Get or create owner
                owner_id = None
                owner_name = str(row.get('owner_name', '')).strip()
                owner_national_id = str(row.get('owner_national_id', '')).strip()
                
                if owner_national_id:
                    # Check if resident exists
                    cursor.execute('SELECT id FROM residents WHERE national_id = ?', (owner_national_id,))
                    existing_resident = cursor.fetchone()
                    
                    if existing_resident:
                        owner_id = existing_resident[0]
                    elif owner_name:
                        # Create new resident
                        cursor.execute('''
                            INSERT INTO residents (name, national_id, phone, is_active)
                            VALUES (?, ?, ?, 1)
                        ''', (owner_name, owner_national_id, ''))
                        owner_id = cursor.lastrowid
                
                if not owner_id and owner_name:
                    # Try to find by name
                    cursor.execute('SELECT id FROM residents WHERE name = ?', (owner_name,))
                    existing_resident = cursor.fetchone()
                    if existing_resident:
                        owner_id = existing_resident[0]
                
                # Vehicle data
                vehicle_type = str(row.get('vehicle_type', '')).strip() or None
                make = str(row.get('make', '')).strip() or None
                model = str(row.get('model', '')).strip() or None
                year = None
                try:
                    year_val = row.get('year')
                    if pd.notna(year_val):
                        year = int(float(year_val))
                except:
                    pass
                color = str(row.get('color', '')).strip() or None
                sticker_number = str(row.get('sticker_number', '')).strip() or None
                
                if existing_vehicle and merge_mode:
                    # Update existing vehicle
                    update_fields = []
                    update_values = []
                    
                    if vehicle_type:
                        update_fields.append('vehicle_type = ?')
                        update_values.append(vehicle_type)
                    if make:
                        update_fields.append('make = ?')
                        update_values.append(make)
                    if model:
                        update_fields.append('model = ?')
                        update_values.append(model)
                    if year:
                        update_fields.append('year = ?')
                        update_values.append(year)
                    if color:
                        update_fields.append('color = ?')
                        update_values.append(color)
                    if sticker_number:
                        update_fields.append('sticker_number = ?')
                        update_values.append(sticker_number)
                    if owner_id and owner_id != existing_vehicle[1]:
                        update_fields.append('owner_id = ?')
                        update_values.append(owner_id)
                    
                    if update_fields:
                        update_fields.append('updated_at = CURRENT_TIMESTAMP')
                        update_values.append(existing_vehicle[0])
                        
                        cursor.execute(f'''
                            UPDATE vehicles 
                            SET {', '.join(update_fields)}
                            WHERE id = ?
                        ''', update_values)
                        
                        stats['imported'] += 1
                    else:
                        stats['skipped'] += 1
                        
                elif not existing_vehicle:
                    # Insert new vehicle
                    if not owner_id:
                        # Create a placeholder resident
                        cursor.execute('''
                            INSERT INTO residents (name, national_id, phone, is_active)
                            VALUES (?, ?, ?, 1)
                        ''', (owner_name or 'غير محدد', owner_national_id or f'TEMP_{plate_number}', ''))
                        owner_id = cursor.lastrowid
                    
                    cursor.execute('''
                        INSERT INTO vehicles (
                            plate_number, owner_id, vehicle_type, make, model, 
                            year, color, sticker_number, is_active
                        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, 1)
                    ''', (plate_number, owner_id, vehicle_type, make, model, year, color, sticker_number))
                    
                    stats['imported'] += 1
                else:
                    stats['skipped'] += 1
                    
            except Exception as e:
                stats['errors'] += 1
                stats['error_details'].append(f"Row {index + 2}: {str(e)}")
                print(f"Error importing row {index + 2}: {str(e)}")
        
        conn.commit()
        conn.close()
        
        return stats
        
    except Exception as e:
        print(f"Error importing vehicles: {str(e)}")
        return {
            'total': 0,
            'imported': 0,
            'skipped': 0,
            'errors': 1,
            'error_details': [str(e)]
        }


def import_violations_from_excel(file_path: str) -> dict:
    """
    Import traffic violations from Excel file
    استيراد المخالفات المرورية من ملف Excel
    
    Args:
        file_path: Path to Excel file
    
    Returns:
        Dict with import statistics
    """
    try:
        df = pd.read_excel(file_path)
        
        # Column mappings
        column_mappings = {
            'plate_number': ['رقم اللوحة', 'plate_number', 'Plate Number'],
            'violation_type': ['نوع المخالفة', 'violation_type', 'Violation Type'],
            'violation_date': ['تاريخ المخالفة', 'violation_date', 'Date'],
            'location': ['الموقع', 'location', 'Location'],
            'description': ['الوصف', 'description', 'Description'],
            'fine_amount': ['الغرامة', 'fine_amount', 'Fine', 'Amount'],
            'status': ['الحالة', 'status', 'Status'],
        }
        
        # Map columns
        mapped_columns = {}
        for standard_name, possible_names in column_mappings.items():
            for col in df.columns:
                if col in possible_names:
                    mapped_columns[col] = standard_name
                    break
        
        df = df.rename(columns=mapped_columns)
        
        stats = {
            'total': len(df),
            'imported': 0,
            'skipped': 0,
            'errors': 0,
            'error_details': []
        }
        
        conn = database.get_db_connection()
        cursor = conn.cursor()
        
        for index, row in df.iterrows():
            try:
                plate_number = str(row.get('plate_number', '')).strip()
                
                if not plate_number:
                    stats['skipped'] += 1
                    continue
                
                # Find vehicle
                cursor.execute('SELECT id FROM vehicles WHERE plate_number = ?', (plate_number,))
                vehicle = cursor.fetchone()
                
                if not vehicle:
                    stats['skipped'] += 1
                    stats['error_details'].append(f"Row {index + 2}: Vehicle not found: {plate_number}")
                    continue
                
                vehicle_id = vehicle[0]
                
                # Violation data
                violation_type = str(row.get('violation_type', '')).strip()
                if not violation_type:
                    stats['skipped'] += 1
                    continue
                
                violation_date = row.get('violation_date')
                if pd.isna(violation_date):
                    violation_date = datetime.now()
                elif isinstance(violation_date, str):
                    try:
                        violation_date = pd.to_datetime(violation_date)
                    except:
                        violation_date = datetime.now()
                
                location = str(row.get('location', '')).strip() or None
                description = str(row.get('description', '')).strip() or None
                
                fine_amount = 0
                try:
                    fine_val = row.get('fine_amount')
                    if pd.notna(fine_val):
                        fine_amount = float(fine_val)
                except:
                    pass
                
                status = str(row.get('status', 'pending')).strip()
                
                # Insert violation
                cursor.execute('''
                    INSERT INTO traffic_violations (
                        vehicle_id, violation_type, violation_date, location,
                        description, fine_amount, status
                    ) VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', (vehicle_id, violation_type, violation_date, location, description, fine_amount, status))
                
                stats['imported'] += 1
                
            except Exception as e:
                stats['errors'] += 1
                stats['error_details'].append(f"Row {index + 2}: {str(e)}")
                print(f"Error importing violation row {index + 2}: {str(e)}")
        
        conn.commit()
        conn.close()
        
        return stats
        
    except Exception as e:
        print(f"Error importing violations: {str(e)}")
        return {
            'total': 0,
            'imported': 0,
            'skipped': 0,
            'errors': 1,
            'error_details': [str(e)]
        }


if __name__ == '__main__':
    print("=" * 60)
    print("📥 Historical Vehicle Data Import")
    print("استيراد البيانات التاريخية للسيارات")
    print("=" * 60)
    print()
    
    # Example usage
    print("Usage:")
    print("  import_historical_vehicles.import_vehicles_from_excel('vehicles.xlsx')")
    print("  import_historical_vehicles.import_violations_from_excel('violations.xlsx')")
    print()
    print("Expected Excel format:")
    print("  Vehicles: رقم اللوحة, نوع السيارة, الماركة, الموديل, السنة, اللون, اسم المالك, الرقم الوطني")
    print("  Violations: رقم اللوحة, نوع المخالفة, تاريخ المخالفة, الموقع, الوصف, الغرامة, الحالة")
