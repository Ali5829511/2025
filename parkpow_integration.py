"""
Plate Recognizer Integration Module (Snapshot Cloud)
نظام التكامل مع خدمة Plate Recognizer لتمييز لوحات السيارات
 
This module provides integration with Plate Recognizer Snapshot Cloud API for:
- Automatic license plate recognition
- Traffic violation recording
- Vehicle tracking and monitoring

API Documentation: https://app.platerecognizer.com/service/snapshot-cloud/
"""

import os
import requests
import base64
import json
from typing import Dict, List, Optional
from datetime import datetime
import database

# Plate Recognizer API Configuration (Snapshot Cloud)
PLATE_RECOGNIZER_API_TOKEN = os.environ.get('PLATE_RECOGNIZER_API_TOKEN', '')
PLATE_RECOGNIZER_API_URL = os.environ.get('PLATE_RECOGNIZER_API_URL', 'https://api.platerecognizer.com/v1/plate-reader/')
PLATE_RECOGNIZER_REGIONS = os.environ.get('PLATE_RECOGNIZER_REGIONS', 'sa').split(',')  # Default to Saudi Arabia


def is_configured() -> bool:
    """
    Check if Plate Recognizer API is configured
    التحقق من إعداد خدمة Plate Recognizer
    
    Returns:
        bool: True if API token is configured, False otherwise
    """
    return bool(PLATE_RECOGNIZER_API_TOKEN and len(PLATE_RECOGNIZER_API_TOKEN) > 10)


def get_api_status() -> Dict:
    """
    Get Plate Recognizer API status and configuration
    Test API connectivity using statistics endpoint
    الحصول على حالة خدمة Plate Recognizer
    
    Returns:
        Dict containing API status information
    """
    if not is_configured():
        return {
            'success': False,
            'configured': False,
            'message': 'Plate Recognizer API is not configured',
            'message_ar': 'خدمة Plate Recognizer غير مفعلة'
        }
    
    try:
        headers = {
            'Authorization': f'Token {PLATE_RECOGNIZER_API_TOKEN}'
        }
        
        # Test API connection using statistics endpoint
        response = requests.get(
            'https://api.platerecognizer.com/v1/statistics/',
            headers=headers,
            timeout=10
        )
        
        if response.status_code == 200:
            stats = response.json()
            return {
                'success': True,
                'configured': True,
                'message': 'Plate Recognizer API is active and working',
                'message_ar': 'خدمة Plate Recognizer نشطة وتعمل بشكل صحيح',
                'api_url': PLATE_RECOGNIZER_API_URL,
                'usage': stats.get('usage', {}),
                'total_calls': stats.get('total_calls', 0)
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
        print(f"Plate Recognizer API error: {str(e)}")
        return {
            'success': False,
            'configured': True,
            'message': 'Error connecting to API',
            'message_ar': 'خطأ في الاتصال بالخدمة'
        }


def recognize_plate(image_data: str, camera_id: Optional[str] = None) -> Dict:
    """
    Send image to Plate Recognizer for plate recognition using Snapshot Cloud API
    إرسال صورة لتمييز اللوحة باستخدام Plate Recognizer
    
    Uses Plate Recognizer's Snapshot Cloud API endpoint:
    https://api.platerecognizer.com/v1/plate-reader/
    
    Args:
        image_data: Base64 encoded image (with or without data:image prefix)
        camera_id: Camera code identifier (optional, for logging purposes)
    
    Returns:
        Dict containing recognition results
    """
    if not is_configured():
        return {
            'success': False,
            'error': 'Plate Recognizer API is not configured',
            'error_ar': 'خدمة Plate Recognizer غير مفعلة'
        }
    
    try:
        headers = {
            'Authorization': f'Token {PLATE_RECOGNIZER_API_TOKEN}'
        }
        
        # Remove data URL prefix if present (e.g., "data:image/jpeg;base64,")
        if image_data.startswith('data:image'):
            image_data = image_data.split(',', 1)[1] if ',' in image_data else image_data
        
        # Decode base64 to bytes
        image_bytes = base64.b64decode(image_data)
        
        # Prepare files for upload
        files = {
            'upload': ('image.jpg', image_bytes, 'image/jpeg')
        }
        
        # Prepare data with regions
        # Plate Recognizer API expects regions as a JSON array string for multipart form data
        data = {}
        if PLATE_RECOGNIZER_REGIONS and len(PLATE_RECOGNIZER_REGIONS) > 0:
            # Filter out empty strings
            regions = [r.strip() for r in PLATE_RECOGNIZER_REGIONS if r.strip()]
            if regions:
                # Send as JSON array string for proper API parsing
                data['regions'] = json.dumps(regions)
        
        # Send request to Plate Recognizer API
        response = requests.post(
            PLATE_RECOGNIZER_API_URL,
            headers=headers,
            files=files,
            data=data,
            timeout=30
        )
        
        if response.status_code == 200:
            api_response = response.json()
            
            # Format results to match expected output
            formatted_results = []
            
            if 'results' in api_response:
                for result in api_response['results']:
                    plate = result.get('plate', '').upper()
                    confidence = result.get('score', 0.0)
                    
                    # Try to find vehicle in database
                    vehicle = find_vehicle_by_plate(plate) if plate else None
                    
                    # Return both 'plate' and 'plate_number' for API compatibility
                    # (different consumers may expect different field names)
                    formatted_results.append({
                        'plate': plate,
                        'plate_number': plate,
                        'confidence': confidence,
                        'region': result.get('region', {}).get('code', ''),
                        'vehicle_type': result.get('vehicle', {}).get('type', ''),
                        'vehicle_info': vehicle,
                        'candidates': [
                            {
                                'plate': c.get('plate', '').upper(),
                                'confidence': c.get('score', 0.0)
                            }
                            for c in result.get('candidates', [])[:5]
                        ]
                    })
            
            return {
                'success': True,
                'results': formatted_results,
                'processing_time': api_response.get('processing_time', 0),
                'message': 'Plate recognized successfully',
                'message_ar': 'تم تمييز اللوحة بنجاح'
            }
        
        elif response.status_code == 401:
            return {
                'success': False,
                'error': 'Invalid API token',
                'error_ar': 'رمز API غير صالح'
            }
        
        elif response.status_code == 402:
            return {
                'success': False,
                'error': 'Insufficient credits. Please check your Plate Recognizer account.',
                'error_ar': 'رصيد غير كافٍ. يرجى التحقق من حساب Plate Recognizer.'
            }
        
        else:
            return {
                'success': False,
                'error': f'Recognition failed with status: {response.status_code}',
                'error_ar': f'فشل التمييز برمز الحالة: {response.status_code}'
            }
    
    except Exception as e:
        # Log the actual error but don't expose it to user
        print(f"Plate Recognizer recognition error: {str(e)}")
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
    Log Plate Recognizer activity for audit trail
    تسجيل نشاط Plate Recognizer للمراجعة
    
    Args:
        user_id: User performing the action
        event_type: Type of event (recognition, violation, etc.)
        plate_number: Plate number involved
        details: Additional details
    
    Returns:
        bool: True if logged successfully
    """
    try:
        log_message = f"Plate Recognizer {event_type}: {plate_number}"
        if details:
            log_message += f" - {details}"
        
        database.log_audit(user_id, log_message)
        return True
    
    except Exception as e:
        print(f"Error logging Plate Recognizer event: {e}")
        return False


def process_webhook_data(webhook_data: Dict) -> Dict:
    """
    Process incoming webhook data from Plate Recognizer
    معالجة البيانات الواردة من Plate Recognizer
    
    Note: This function is kept for compatibility but Plate Recognizer
    Snapshot Cloud doesn't provide webhook functionality by default.
    
    Args:
        webhook_data: Data received from webhook
    
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
        print(f"Webhook processing error: {str(e)}")
        return {
            'success': False,
            'error': 'Error processing webhook',
            'error_ar': 'خطأ في معالجة البيانات'
        }
