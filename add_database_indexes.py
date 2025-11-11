#!/usr/bin/env python3
"""
Add Database Indexes for Performance Optimization
سكريبت لإضافة فهارس لتحسين أداء قاعدة البيانات
"""

import sqlite3
import os
import sys

DATABASE_PATH = os.path.join(os.path.dirname(__file__), 'housing.db')

def add_indexes():
    """Add indexes to frequently queried columns"""
    
    if not os.path.exists(DATABASE_PATH):
        print(f"❌ Error: Database file not found at {DATABASE_PATH}")
        sys.exit(1)
    
    print("\n" + "=" * 80)
    print("  📊 Adding Database Indexes for Performance Optimization")
    print("  إضافة فهارس لتحسين أداء قاعدة البيانات")
    print("=" * 80 + "\n")
    
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    
    # List of indexes to create
    indexes = [
        # Users table
        {
            'name': 'idx_users_username',
            'table': 'users',
            'columns': 'username',
            'description': 'User login lookups'
        },
        {
            'name': 'idx_users_email',
            'table': 'users',
            'columns': 'email',
            'description': 'User email lookups'
        },
        # Residents table
        {
            'name': 'idx_residents_national_id',
            'table': 'residents',
            'columns': 'national_id',
            'description': 'Resident ID lookups'
        },
        {
            'name': 'idx_residents_building_id',
            'table': 'residents',
            'columns': 'building_id',
            'description': 'Residents by building'
        },
        {
            'name': 'idx_residents_is_active',
            'table': 'residents',
            'columns': 'is_active',
            'description': 'Active residents filter'
        },
        # Vehicles table
        {
            'name': 'idx_vehicles_plate_number',
            'table': 'vehicles',
            'columns': 'plate_number',
            'description': 'Vehicle plate lookups'
        },
        {
            'name': 'idx_vehicles_owner_id',
            'table': 'vehicles',
            'columns': 'owner_id',
            'description': 'Vehicles by owner'
        },
        {
            'name': 'idx_vehicles_sticker_number',
            'table': 'vehicles',
            'columns': 'sticker_number',
            'description': 'Vehicle sticker lookups'
        },
        # Stickers table
        {
            'name': 'idx_stickers_sticker_number',
            'table': 'stickers',
            'columns': 'sticker_number',
            'description': 'Sticker number lookups'
        },
        {
            'name': 'idx_stickers_resident_id',
            'table': 'stickers',
            'columns': 'resident_id',
            'description': 'Stickers by resident'
        },
        {
            'name': 'idx_stickers_plate_number',
            'table': 'stickers',
            'columns': 'plate_number',
            'description': 'Stickers by plate number'
        },
        {
            'name': 'idx_stickers_status',
            'table': 'stickers',
            'columns': 'status',
            'description': 'Stickers by status'
        },
        # Buildings table
        {
            'name': 'idx_buildings_building_number',
            'table': 'buildings',
            'columns': 'building_number',
            'description': 'Building number lookups'
        },
        # Traffic violations
        {
            'name': 'idx_violations_vehicle_id',
            'table': 'traffic_violations',
            'columns': 'vehicle_id',
            'description': 'Violations by vehicle'
        },
        {
            'name': 'idx_violations_status',
            'table': 'traffic_violations',
            'columns': 'status',
            'description': 'Violations by status'
        },
        {
            'name': 'idx_violations_date',
            'table': 'traffic_violations',
            'columns': 'violation_date',
            'description': 'Violations by date'
        },
        # Complaints
        {
            'name': 'idx_complaints_resident_id',
            'table': 'complaints',
            'columns': 'resident_id',
            'description': 'Complaints by resident'
        },
        {
            'name': 'idx_complaints_status',
            'table': 'complaints',
            'columns': 'status',
            'description': 'Complaints by status'
        },
        # Visitors
        {
            'name': 'idx_visitors_visiting_resident_id',
            'table': 'visitors',
            'columns': 'visiting_resident_id',
            'description': 'Visitors by resident'
        },
        {
            'name': 'idx_visitors_visit_date',
            'table': 'visitors',
            'columns': 'visit_date',
            'description': 'Visitors by date'
        },
        # Security incidents
        {
            'name': 'idx_incidents_incident_date',
            'table': 'security_incidents',
            'columns': 'incident_date',
            'description': 'Incidents by date'
        },
        {
            'name': 'idx_incidents_status',
            'table': 'security_incidents',
            'columns': 'status',
            'description': 'Incidents by status'
        },
        # Apartments
        {
            'name': 'idx_apartments_building_id',
            'table': 'apartments',
            'columns': 'building_id',
            'description': 'Apartments by building'
        },
        {
            'name': 'idx_apartments_is_occupied',
            'table': 'apartments',
            'columns': 'is_occupied',
            'description': 'Occupied apartments filter'
        },
        # Parking spots
        {
            'name': 'idx_parking_spot_number',
            'table': 'parking_spots',
            'columns': 'spot_number',
            'description': 'Parking spot lookups'
        },
        {
            'name': 'idx_parking_building_id',
            'table': 'parking_spots',
            'columns': 'building_id',
            'description': 'Parking by building'
        },
        {
            'name': 'idx_parking_is_occupied',
            'table': 'parking_spots',
            'columns': 'is_occupied',
            'description': 'Occupied parking filter'
        },
        # Sessions
        {
            'name': 'idx_sessions_user_id',
            'table': 'sessions',
            'columns': 'user_id',
            'description': 'Sessions by user'
        },
        {
            'name': 'idx_sessions_token',
            'table': 'sessions',
            'columns': 'session_token',
            'description': 'Session token lookups'
        },
        {
            'name': 'idx_sessions_expires_at',
            'table': 'sessions',
            'columns': 'expires_at',
            'description': 'Session expiration checks'
        },
        # Audit log
        {
            'name': 'idx_audit_user_id',
            'table': 'audit_log',
            'columns': 'user_id',
            'description': 'Audit entries by user'
        },
        {
            'name': 'idx_audit_created_at',
            'table': 'audit_log',
            'columns': 'created_at',
            'description': 'Audit entries by date'
        },
        # Plate recognition log
        {
            'name': 'idx_plate_recognition_user_id',
            'table': 'plate_recognition_log',
            'columns': 'user_id',
            'description': 'Plate recognition by user'
        },
        {
            'name': 'idx_plate_recognition_plate',
            'table': 'plate_recognition_log',
            'columns': 'plate_number',
            'description': 'Plate recognition lookups'
        }
    ]
    
    created_count = 0
    skipped_count = 0
    
    for idx in indexes:
        try:
            # Check if index already exists
            cursor.execute(f"""
                SELECT name FROM sqlite_master 
                WHERE type='index' AND name='{idx['name']}'
            """)
            
            if cursor.fetchone():
                print(f"  ⏭️  Skipping {idx['name']} (already exists)")
                skipped_count += 1
                continue
            
            # Create index
            sql = f"CREATE INDEX {idx['name']} ON {idx['table']}({idx['columns']})"
            cursor.execute(sql)
            print(f"  ✅ Created {idx['name']} on {idx['table']}({idx['columns']})")
            print(f"     Purpose: {idx['description']}")
            created_count += 1
            
        except Exception as e:
            print(f"  ❌ Error creating {idx['name']}: {e}")
    
    conn.commit()
    conn.close()
    
    print("\n" + "=" * 80)
    print(f"  ✅ Index Creation Complete")
    print(f"  Created: {created_count} | Skipped: {skipped_count}")
    print("=" * 80 + "\n")
    
    return created_count

if __name__ == '__main__':
    add_indexes()
