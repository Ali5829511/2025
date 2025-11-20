"""
ParkPow API Integration Module
نظام التكامل مع خدمة ParkPow لتمييز لوحات السيارات وتسجيل المخالفات

This module provides integration with ParkPow API for:
- Automatic license plate recognition
- Traffic violation recording
- Vehicle tracking and monitoring
"""

import os
import requests
import base64
from typing import Dict, List, Optional
from datetime import datetime
import database

# ParkPow API Configuration
PARKPOW_API_TOKEN = os.environ.get('PARKPOW_API_TOKEN', '')
PARKPOW_API_URL = os.environ.get('PARKPOW_API_URL', 'https://app.parkpow.com/api/v1')
PARKPOW_WEBHOOK_URL = f'{PARKPOW_API_URL}/webhook-receiver/'


def is_configured() -> bool:
    """
    Check if ParkPow API is configured
    التحقق من إعداد خدمة ParkPow
    
    Returns:
        bool: True if API token is configured, False otherwise
    """
    return bool(PARKPOW_API_TOKEN and len(PARKPOW_API_TOKEN) > 10)


def get_api_status() -> Dict:
    """
    Get ParkPow API status and configuration
    Test API connectivity by listing vehicles (lightweight check)
    الحصول على حالة خدمة ParkPow
    
    Returns:
        Dict containing API status information
    """
    if not is_configured():
        return {
            'success': False,
            'configured': False,
            'message': 'ParkPow API is not configured',
            'message_ar': 'خدمة ParkPow غير مفعلة'
        }
    
    try:
        headers = {
            'Authorization': f'Token {PARKPOW_API_TOKEN}'
        }
        
        # Test API connection by trying to list vehicles with page_size=1
        # This is the lightest way to test connectivity according to the official API
        response = requests.get(
            f'{PARKPOW_API_URL}/vehicles/',
            headers=headers,
            params={'page_size': 1},
            timeout=10
        )
        
        if response.status_code == 200:
            return {
                'success': True,
                'configured': True,
                'message': 'ParkPow API is active and working',
                'message_ar': 'خدمة ParkPow نشطة وتعمل بشكل صحيح',
                'api_url': PARKPOW_API_URL,
                'webhook_url': PARKPOW_WEBHOOK_URL
            }
        else:
            return {
                'success': False,
                'configured': True,
                'message': f'API returned status code: {response.status_code}',
                'message_ar': f'الخدمة أرجعت رمز الحالة: {response.status_code}'
            }
    
    except requests.exceptions.Timeout:
        return {
            'success': False,
            'configured': True,
            'message': 'API request timed out',
            'message_ar': 'انتهت مهلة طلب الخدمة'
        }
    except Exception as e:
        # Log the actual error but don't expose it to user
        print(f"ParkPow API error: {str(e)}")
        return {
            'success': False,
            'configured': True,
            'message': 'Error connecting to API',
            'message_ar': 'خطأ في الاتصال بالخدمة'
        }


def recognize_plate(image_data: str, camera_id: Optional[str] = None) -> Dict:
    """
    Send image to ParkPow for plate recognition using the log-vehicle endpoint
    إرسال صورة لتمييز اللوحة باستخدام نقطة نهاية تسجيل المركبة
    
    According to ParkPow API docs, plate recognition is done through the
    /api/v1/log-vehicle/ endpoint which creates a visit and returns plate data.
    
    Args:
        image_data: Base64 encoded image (without data:image prefix)
        camera_id: Camera code identifier (required)
    
    Returns:
        Dict containing recognition results
    """
    if not is_configured():
        return {
            'success': False,
            'error': 'ParkPow API is not configured',
            'error_ar': 'خدمة ParkPow غير مفعلة'
        }
    
    try:
        headers = {
            'Authorization': f'Token {PARKPOW_API_TOKEN}',
            'Content-Type': 'application/json'
        }
        
        # Use default camera code if not provided
        if not camera_id:
            camera_id = 'default_camera'
        
        # Prepare payload according to ParkPow API specification
        # The image should be base64 encoded without the data:image prefix
        if image_data.startswith('data:image'):
            # Remove the data URL prefix if present
            image_data = image_data.split(',', 1)[1] if ',' in image_data else image_data
        
        payload = {
            'camera': camera_id,
            'image': image_data,
            'results': []  # Empty results array as per API docs
        }
        
        response = requests.post(
            f'{PARKPOW_API_URL}/log-vehicle/',
            headers=headers,
            json=payload,
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            # Extract results from the paginated response
            results_list = data.get('results', [])
            
            # Format results to match expected output
            formatted_results = []
            for visit in results_list:
                vehicle = visit.get('vehicle', {})
                start_data = visit.get('start_data', {})
                
                # Extract plate number from start_data
                plate = start_data.get('plate', vehicle.get('license_plate', ''))
                
                formatted_results.append({
                    'plate': plate,
                    'confidence': start_data.get('score', 0),
                    'vehicle_info': {
                        'license_plate': vehicle.get('license_plate'),
                        'make': vehicle.get('make'),
                        'model': vehicle.get('model'),
                        'color': vehicle.get('color'),
                        'type': vehicle.get('type')
                    }
                })
            
            return {
                'success': True,
                'results': formatted_results,
                'message': 'Plate recognized successfully',
                'message_ar': 'تم تمييز اللوحة بنجاح'
            }
        else:
            return {
                'success': False,
                'error': f'Recognition failed with status: {response.status_code}',
                'error_ar': f'فشل التمييز برمز الحالة: {response.status_code}'
            }
    
    except Exception as e:
        # Log the actual error but don't expose it to user
        print(f"ParkPow recognition error: {str(e)}")
        return {
            'success': False,
            'error': 'Error during recognition',
            'error_ar': 'خطأ أثناء التمييز'
        }


def find_vehicle_by_plate(plate_number: str) -> Optional[Dict]:
    """
    Find vehicle in database by plate number
    البحث عن سيارة في قاعدة البيانات برقم اللوحة
    
    Args:
        plate_number: License plate number to search for
    
    Returns:
        Dict with vehicle information or None if not found
    """
    try:
        conn = database.get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT 
                v.*,
                r.name as owner_name,
                r.national_id,
                r.phone as owner_phone,
                r.department,
                r.job_title,
                r.unit_number,
                b.name as building_name,
                b.building_number
            FROM vehicles v
            LEFT JOIN residents r ON v.owner_id = r.id
            LEFT JOIN buildings b ON r.building_id = b.id
            WHERE v.plate_number = ? AND v.is_active = 1
        ''', (plate_number,))
        
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return dict(row)
        return None
    
    except Exception as e:
        print(f"Error finding vehicle: {e}")
        return None


def record_violation(plate_number: str, violation_data: Dict, user_id: int) -> Dict:
    """
    Record a traffic violation in the database
    تسجيل مخالفة مرورية في قاعدة البيانات
    
    Args:
        plate_number: License plate number
        violation_data: Dict containing violation details
        user_id: ID of user recording the violation
    
    Returns:
        Dict with operation result
    """
    try:
        conn = database.get_db_connection()
        cursor = conn.cursor()
        
        # Find vehicle
        vehicle = find_vehicle_by_plate(plate_number)
        vehicle_id = vehicle['id'] if vehicle else None
        
        # Insert violation - removed fine_amount field
        cursor.execute('''
            INSERT INTO traffic_violations 
            (vehicle_id, plate_number, violation_type, violation_date, 
             location, description, payment_status, status, recorded_by)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            vehicle_id,
            plate_number,
            violation_data.get('violation_type', 'Unknown'),
            violation_data.get('violation_date', datetime.now().isoformat()),
            violation_data.get('location', ''),
            violation_data.get('description', ''),
            violation_data.get('payment_status', 0),
            'open',
            user_id
        ))
        
        violation_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return {
            'success': True,
            'violation_id': violation_id,
            'vehicle_found': vehicle is not None,
            'message': 'Violation recorded successfully',
            'message_ar': 'تم تسجيل المخالفة بنجاح'
        }
    
    except Exception as e:
        # Log the actual error but don't expose it to user
        print(f"ParkPow violation recording error: {str(e)}")
        return {
            'success': False,
            'error': 'Error recording violation',
            'error_ar': 'خطأ في تسجيل المخالفة'
        }


def get_repeat_offenders(min_violations: int = 3) -> List[Dict]:
    """
    Get list of repeat offenders
    الحصول على قائمة المخالفين المتكررين
    
    Args:
        min_violations: Minimum number of violations to be considered repeat offender
    
    Returns:
        List of dicts containing offender information
    """
    try:
        conn = database.get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT 
                v.plate_number,
                COUNT(tv.id) as violation_count,
                v.vehicle_type,
                v.make,
                v.model,
                r.name as owner_name,
                r.national_id,
                r.phone as owner_phone,
                r.department,
                r.unit_number,
                b.building_number,
                MAX(tv.violation_date) as latest_violation
            FROM traffic_violations tv
            LEFT JOIN vehicles v ON tv.vehicle_id = v.id
            LEFT JOIN residents r ON v.owner_id = r.id
            LEFT JOIN buildings b ON r.building_id = b.id
            WHERE tv.status IN ('open', 'مفتوحة', 'pending', 'معلقة')
            GROUP BY v.plate_number
            HAVING violation_count >= ?
            ORDER BY violation_count DESC, latest_violation DESC
        ''', (min_violations,))
        
        rows = cursor.fetchall()
        conn.close()
        
        return [dict(row) for row in rows]
    
    except Exception as e:
        print(f"Error getting repeat offenders: {e}")
        return []


def log_parkpow_event(user_id: int, event_type: str, plate_number: str, 
                      details: Optional[str] = None) -> bool:
    """
    Log ParkPow activity for audit trail
    تسجيل نشاط ParkPow للمراجعة
    
    Args:
        user_id: User performing the action
        event_type: Type of event (recognition, violation, etc.)
        plate_number: Plate number involved
        details: Additional details
    
    Returns:
        bool: True if logged successfully
    """
    try:
        log_message = f"ParkPow {event_type}: {plate_number}"
        if details:
            log_message += f" - {details}"
        
        database.log_audit(user_id, log_message)
        return True
    
    except Exception as e:
        print(f"Error logging ParkPow event: {e}")
        return False


def process_webhook_data(webhook_data: Dict) -> Dict:
    """
    Process incoming webhook data from ParkPow
    معالجة البيانات الواردة من ParkPow
    
    Args:
        webhook_data: Data received from ParkPow webhook
    
    Returns:
        Dict with processing result
    """
    try:
        # Extract plate information
        plate_number = webhook_data.get('plate_number') or webhook_data.get('plate')
        
        if not plate_number:
            return {
                'success': False,
                'error': 'No plate number in webhook data',
                'error_ar': 'لا يوجد رقم لوحة في البيانات'
            }
        
        # Find vehicle in database
        vehicle = find_vehicle_by_plate(plate_number)
        
        # Log the detection
        conn = database.get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO parkpow_detections 
            (plate_number, vehicle_id, detection_time, camera_id, confidence, raw_data)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            plate_number,
            vehicle['id'] if vehicle else None,
            datetime.now().isoformat(),
            webhook_data.get('camera_id', ''),
            webhook_data.get('confidence', 0.0),
            str(webhook_data)
        ))
        
        conn.commit()
        conn.close()
        
        return {
            'success': True,
            'plate_number': plate_number,
            'vehicle_found': vehicle is not None,
            'message': 'Webhook processed successfully',
            'message_ar': 'تمت معالجة البيانات بنجاح'
        }
    
    except Exception as e:
        # Log the actual error but don't expose it to user
        print(f"ParkPow webhook processing error: {str(e)}")
        return {
            'success': False,
            'error': 'Error processing webhook',
            'error_ar': 'خطأ في معالجة البيانات'
        }


def create_or_update_camera(camera_code: str, camera_name: str, 
                            camera_type: int = 0, latitude: Optional[float] = None,
                            longitude: Optional[float] = None, 
                            notes: str = '') -> Dict:
    """
    Create or update a camera in ParkPow
    إنشاء أو تحديث كاميرا في ParkPow
    
    According to ParkPow API docs, this endpoint creates or updates camera details.
    
    Args:
        camera_code: Unique camera identifier (required)
        camera_name: Human-readable camera name (required)
        camera_type: Camera type (0=Entrance, 1=Exit, 2=Entrance & Exit, etc.)
        latitude: Camera latitude (-90 to 90)
        longitude: Camera longitude (-180 to 180)
        notes: Additional notes about the camera
    
    Returns:
        Dict with operation result
    """
    if not is_configured():
        return {
            'success': False,
            'error': 'ParkPow API is not configured',
            'error_ar': 'خدمة ParkPow غير مفعلة'
        }
    
    try:
        headers = {
            'Authorization': f'Token {PARKPOW_API_TOKEN}',
            'Content-Type': 'application/json'
        }
        
        payload = {
            'code': camera_code,
            'name': camera_name,
            'type': camera_type,
            'notes': notes
        }
        
        if latitude is not None:
            payload['latitude'] = latitude
        if longitude is not None:
            payload['longitude'] = longitude
        
        response = requests.post(
            f'{PARKPOW_API_URL}/create-camera/',
            headers=headers,
            json=payload,
            timeout=15
        )
        
        if response.status_code == 200:
            return {
                'success': True,
                'camera': response.json(),
                'message': 'Camera created/updated successfully',
                'message_ar': 'تم إنشاء/تحديث الكاميرا بنجاح'
            }
        else:
            return {
                'success': False,
                'error': f'Failed with status: {response.status_code}',
                'error_ar': f'فشل برمز الحالة: {response.status_code}'
            }
    
    except Exception as e:
        print(f"ParkPow camera creation error: {str(e)}")
        return {
            'success': False,
            'error': 'Error creating/updating camera',
            'error_ar': 'خطأ في إنشاء/تحديث الكاميرا'
        }


def create_or_update_vehicle(license_plate: str, region: Optional[str] = None,
                             make: Optional[str] = None,
                             model: Optional[str] = None, color: Optional[str] = None,
                             vehicle_type: Optional[str] = None,
                             field1: Optional[str] = None, field2: Optional[str] = None,
                             field3: Optional[str] = None, field4: Optional[str] = None,
                             field5: Optional[str] = None, field6: Optional[str] = None) -> Dict:
    """
    Create or update a vehicle in ParkPow
    إنشاء أو تحديث مركبة في ParkPow
    
    According to ParkPow API docs, this incorporates 3rd party data into ParkPow
    so you can fully understand the vehicles captured in the dashboard.
    
    Args:
        license_plate: License plate number (required)
        region: Region code (e.g., 'us-ny')
        make: Vehicle make
        model: Vehicle model
        color: Vehicle color (black, blue, brown, green, red, silver, white, yellow)
        vehicle_type: Type (bus, sedan, motorcycle, pickup_truck, suv, big_truck, unknown, van)
        field1-field6: Custom fields for additional data
    
    Returns:
        Dict with operation result
    """
    if not is_configured():
        return {
            'success': False,
            'error': 'ParkPow API is not configured',
            'error_ar': 'خدمة ParkPow غير مفعلة'
        }
    
    try:
        headers = {
            'Authorization': f'Token {PARKPOW_API_TOKEN}',
            'Content-Type': 'application/json'
        }
        
        payload = {
            'license_plate': license_plate
        }
        
        # Add optional fields only if provided
        if region:
            payload['region'] = region
        if make:
            payload['make'] = make
        if model:
            payload['model'] = model
        if color:
            payload['color'] = color
        if vehicle_type:
            payload['type'] = vehicle_type
        if field1:
            payload['field1'] = field1
        if field2:
            payload['field2'] = field2
        if field3:
            payload['field3'] = field3
        if field4:
            payload['field4'] = field4
        if field5:
            payload['field5'] = field5
        if field6:
            payload['field6'] = field6
        
        response = requests.post(
            f'{PARKPOW_API_URL}/create-vehicle/',
            headers=headers,
            json=payload,
            timeout=15
        )
        
        if response.status_code == 200:
            return {
                'success': True,
                'vehicle': response.json(),
                'message': 'Vehicle created/updated successfully',
                'message_ar': 'تم إنشاء/تحديث المركبة بنجاح'
            }
        else:
            return {
                'success': False,
                'error': f'Failed with status: {response.status_code}',
                'error_ar': f'فشل برمز الحالة: {response.status_code}'
            }
    
    except Exception as e:
        print(f"ParkPow vehicle creation error: {str(e)}")
        return {
            'success': False,
            'error': 'Error creating/updating vehicle',
            'error_ar': 'خطأ في إنشاء/تحديث المركبة'
        }


def sync_vehicle_to_parkpow(vehicle_data: Dict) -> Dict:
    """
    Sync a vehicle from local database to ParkPow
    مزامنة مركبة من قاعدة البيانات المحلية إلى ParkPow
    
    Args:
        vehicle_data: Dict containing vehicle information from local database
    
    Returns:
        Dict with sync result
    """
    try:
        # Extract relevant fields from local vehicle data
        return create_or_update_vehicle(
            license_plate=vehicle_data.get('plate_number', ''),
            make=vehicle_data.get('make'),
            model=vehicle_data.get('model'),
            color=vehicle_data.get('color'),
            vehicle_type=vehicle_data.get('vehicle_type'),
            field1=vehicle_data.get('owner_name'),
            field2=vehicle_data.get('national_id'),
            field3=vehicle_data.get('department'),
            field4=vehicle_data.get('unit_number'),
            field5=vehicle_data.get('building_name')
        )
    except Exception as e:
        print(f"Error syncing vehicle to ParkPow: {str(e)}")
        return {
            'success': False,
            'error': 'Error syncing vehicle',
            'error_ar': 'خطأ في مزامنة المركبة'
        }
