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
        
        # Test API connection
        response = requests.get(
            f'{PARKPOW_API_URL}/status/',
            headers=headers,
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
        return {
            'success': False,
            'configured': True,
            'message': f'Error connecting to API: {str(e)}',
            'message_ar': f'خطأ في الاتصال بالخدمة: {str(e)}'
        }


def recognize_plate(image_data: str, camera_id: Optional[str] = None) -> Dict:
    """
    Send image to ParkPow for plate recognition
    إرسال صورة لتمييز اللوحة
    
    Args:
        image_data: Base64 encoded image or image URL
        camera_id: Optional camera identifier
    
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
        
        payload = {
            'image': image_data
        }
        
        if camera_id:
            payload['camera_id'] = camera_id
        
        response = requests.post(
            f'{PARKPOW_API_URL}/recognize/',
            headers=headers,
            json=payload,
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            return {
                'success': True,
                'results': data.get('results', []),
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
        return {
            'success': False,
            'error': f'Error during recognition: {str(e)}',
            'error_ar': f'خطأ أثناء التمييز: {str(e)}'
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
        
        # Insert violation
        cursor.execute('''
            INSERT INTO traffic_violations 
            (vehicle_id, plate_number, violation_type, violation_date, 
             location, description, fine_amount, status, recorded_by)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            vehicle_id,
            plate_number,
            violation_data.get('violation_type', 'Unknown'),
            violation_data.get('violation_date', datetime.now().isoformat()),
            violation_data.get('location', ''),
            violation_data.get('description', ''),
            violation_data.get('fine_amount', 0),
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
        return {
            'success': False,
            'error': f'Error recording violation: {str(e)}',
            'error_ar': f'خطأ في تسجيل المخالفة: {str(e)}'
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
        return {
            'success': False,
            'error': f'Error processing webhook: {str(e)}',
            'error_ar': f'خطأ في معالجة البيانات: {str(e)}'
        }
