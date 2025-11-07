#!/usr/bin/env python3
"""
Test script for Traffic Department API endpoints
"""

import requests
import json
from datetime import datetime

BASE_URL = 'http://localhost:5000'

def test_login():
    """Test login and get session"""
    print("\n=== Testing Login ===")
    session = requests.Session()
    response = session.post(f'{BASE_URL}/api/auth/login', json={
        'username': 'admin',
        'password': 'Admin@2025'
    })
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Login successful")
        print(f"   User: {data['user']['name']}")
        print(f"   Role: {data['user']['role']}")
        return session
    else:
        print(f"❌ Login failed: {response.text}")
        return None

def test_statistics(session):
    """Test traffic department statistics endpoint"""
    print("\n=== Testing Statistics Endpoint ===")
    response = session.get(f'{BASE_URL}/api/traffic-department/statistics')
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Statistics retrieved successfully")
        print(f"   Total Violations: {data['statistics']['violations']['total_violations']}")
        print(f"   Total Accidents: {data['statistics']['accidents']['total_accidents']}")
        print(f"   Immobilized Cars: {data['statistics']['immobilized_cars']['currently_immobilized']}")
        return True
    else:
        print(f"❌ Failed to get statistics: {response.text}")
        return False

def test_create_accident(session):
    """Test creating a traffic accident"""
    print("\n=== Testing Create Accident ===")
    headers = {'Content-Type': 'application/json'}
    
    accident_data = {
        'accident_date': datetime.now().isoformat(),
        'location': 'موقف المبنى الرئيسي',
        'description': 'تصادم بسيط بين مركبتين',
        'severity': 'minor',
        'weather_conditions': 'صافي',
        'road_conditions': 'جيدة',
        'vehicles_involved': 2,
        'injuries_count': 0,
        'fatalities_count': 0,
        'damage_estimate': 5000.0,
        'vehicles': [
            {
                'plate_number': 'ABC1234',
                'driver_name': 'أحمد محمد',
                'driver_phone': '0501234567',
                'damage_description': 'خدش في الباب الأمامي',
                'at_fault': 1
            },
            {
                'plate_number': 'XYZ5678',
                'driver_name': 'محمد علي',
                'driver_phone': '0509876543',
                'damage_description': 'كسر في المصد الخلفي',
                'at_fault': 0
            }
        ]
    }
    
    response = session.post(f'{BASE_URL}/api/traffic-accidents', 
                            headers=headers, 
                            json=accident_data)
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Accident created successfully")
        print(f"   Accident ID: {data['accident_id']}")
        print(f"   Accident Number: {data['accident_number']}")
        return data['accident_id']
    else:
        print(f"❌ Failed to create accident: {response.text}")
        return None

def test_get_accidents(session):
    """Test getting accidents list"""
    print("\n=== Testing Get Accidents ===")
    response = session.get(f'{BASE_URL}/api/traffic-accidents')
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Accidents retrieved successfully")
        print(f"   Total Accidents: {len(data['accidents'])}")
        return True
    else:
        print(f"❌ Failed to get accidents: {response.text}")
        return False

def test_create_immobilized_car(session):
    """Test creating an immobilized car entry"""
    print("\n=== Testing Create Immobilized Car ===")
    headers = {'Content-Type': 'application/json'}
    
    immobilized_data = {
        'plate_number': 'DEF7890',
        'immobilization_type': 'boot',
        'reason': 'عدة مخالفات مرورية غير مدفوعة',
        'location': 'موقف الزوار',
        'immobilized_date': datetime.now().isoformat(),
        'outstanding_fines': 2000.0,
        'towing_fee': 0,
        'storage_fee': 0,
        'total_fees': 2000.0,
        'violation_count': 5,
        'notes': 'سيارة مركونة في موقف غير مخصص'
    }
    
    response = session.post(f'{BASE_URL}/api/immobilized-cars', 
                            headers=headers, 
                            json=immobilized_data)
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Immobilized car created successfully")
        print(f"   Immobilized ID: {data['immobilized_id']}")
        return data['immobilized_id']
    else:
        print(f"❌ Failed to create immobilized car: {response.text}")
        return None

def test_get_immobilized_cars(session):
    """Test getting immobilized cars list"""
    print("\n=== Testing Get Immobilized Cars ===")
    response = session.get(f'{BASE_URL}/api/immobilized-cars')
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Immobilized cars retrieved successfully")
        print(f"   Total Immobilized: {len(data['immobilized_cars'])}")
        return True
    else:
        print(f"❌ Failed to get immobilized cars: {response.text}")
        return False

def main():
    print("=" * 60)
    print("Traffic Department API Testing")
    print("=" * 60)
    
    # Test login
    session = test_login()
    if not session:
        print("\n❌ Cannot continue without authentication")
        return
    
    # Test statistics
    test_statistics(session)
    
    # Test traffic accidents
    accident_id = test_create_accident(session)
    test_get_accidents(session)
    
    # Test immobilized cars
    immobilized_id = test_create_immobilized_car(session)
    test_get_immobilized_cars(session)
    
    # Test statistics again to see updated numbers
    print("\n=== Final Statistics Check ===")
    test_statistics(session)
    
    print("\n" + "=" * 60)
    print("Testing Complete!")
    print("=" * 60)

if __name__ == '__main__':
    main()
