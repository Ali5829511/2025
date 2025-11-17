"""
Plate Recognizer ParkPow API Integration Module
نظام التكامل مع خدمة Plate Recognizer ParkPow لتمييز لوحات السيارات

This module provides integration with Plate Recognizer's ParkPow service
for automatic license plate recognition from images.
"""

import os
import requests
import base64
from typing import Dict, List, Optional, Tuple
from datetime import datetime
from io import BytesIO
import database

try:
    from PIL import Image, ImageEnhance, ImageFilter
    PILLOW_AVAILABLE = True
except ImportError:
    PILLOW_AVAILABLE = False
    print("Warning: Pillow not installed. Image preprocessing will be disabled.")

# API Configuration
API_TOKEN = os.environ.get('PLATE_RECOGNIZER_API_TOKEN', '')
API_URL = os.environ.get('PLATE_RECOGNIZER_API_URL', 'https://api.platerecognizer.com/v1/plate-reader/')

# Image Enhancement Configuration
CONTRAST_FACTOR = 1.3  # Increase contrast by 30%
SHARPNESS_FACTOR = 1.5  # Increase sharpness by 50%
BRIGHTNESS_FACTOR = 1.1  # Increase brightness by 10%
MAX_CANDIDATES = 5  # Maximum number of alternative plate readings to return


def is_configured() -> bool:
    """
    Check if Plate Recognizer API is configured
    التحقق من إعداد خدمة Plate Recognizer
    
    Returns:
        bool: True if API token is configured, False otherwise
    """
    return bool(API_TOKEN and API_TOKEN != 'your-api-token-here')


def preprocess_image(image_bytes: bytes, enhance: bool = True) -> bytes:
    """
    Preprocess image to improve plate recognition accuracy
    معالجة الصورة مسبقاً لتحسين دقة تمييز اللوحات
    
    Args:
        image_bytes: Original image bytes
        enhance: Whether to apply image enhancements
    
    Returns:
        bytes: Preprocessed image bytes
    """
    if not PILLOW_AVAILABLE or not enhance:
        return image_bytes
    
    try:
        # Open image
        image = Image.open(BytesIO(image_bytes))
        
        # Convert to RGB if needed
        if image.mode != 'RGB':
            image = image.convert('RGB')
        
        # Apply enhancements for better plate detection
        # 1. Increase contrast
        enhancer = ImageEnhance.Contrast(image)
        image = enhancer.enhance(CONTRAST_FACTOR)
        
        # 2. Increase sharpness
        enhancer = ImageEnhance.Sharpness(image)
        image = enhancer.enhance(SHARPNESS_FACTOR)
        
        # 3. Adjust brightness slightly
        enhancer = ImageEnhance.Brightness(image)
        image = enhancer.enhance(BRIGHTNESS_FACTOR)
        
        # 4. Apply slight sharpening filter
        image = image.filter(ImageFilter.SHARPEN)
        
        # Convert back to bytes
        output = BytesIO()
        image.save(output, format='JPEG', quality=95, optimize=True)
        return output.getvalue()
    
    except (OSError, ValueError) as e:
        print(f"Error preprocessing image: {str(e)}")
        return image_bytes


def validate_image_quality(image_bytes: bytes) -> Dict:
    """
    Validate image quality for plate recognition
    التحقق من جودة الصورة لتمييز اللوحات
    
    Args:
        image_bytes: Image bytes to validate
    
    Returns:
        Dict with validation results:
        {
            'valid': bool,
            'issues': List[str],
            'warnings': List[str],
            'resolution': Tuple[int, int],
            'file_size': int
        }
    """
    result = {
        'valid': True,
        'issues': [],
        'warnings': [],
        'resolution': None,
        'file_size': len(image_bytes)
    }
    
    if not PILLOW_AVAILABLE:
        return result
    
    try:
        image = Image.open(BytesIO(image_bytes))
        result['resolution'] = image.size
        width, height = image.size
        
        # Check minimum resolution
        if width < 400 or height < 300:
            result['issues'].append('Image resolution too low (minimum 400x300 recommended)')
            result['issues'].append('دقة الصورة منخفضة جداً (ينصح بـ 400×300 كحد أدنى)')
            result['valid'] = False
        
        # Check if image is too small
        elif width < 800 or height < 600:
            result['warnings'].append('Image resolution is low. Higher resolution recommended for better accuracy.')
            result['warnings'].append('دقة الصورة منخفضة. يُنصح بدقة أعلى لنتائج أفضل.')
        
        # Check file size
        if len(image_bytes) > 10 * 1024 * 1024:  # 10MB
            result['warnings'].append('Image file size is very large. This may slow down processing.')
            result['warnings'].append('حجم الصورة كبير جداً. قد يؤدي ذلك إلى بطء المعالجة.')
        
        # Check aspect ratio (should be reasonable for car plates)
        aspect_ratio = width / height
        if aspect_ratio < 0.5 or aspect_ratio > 3.0:
            result['warnings'].append('Unusual image aspect ratio. Ensure the plate is clearly visible.')
            result['warnings'].append('نسبة أبعاد الصورة غير عادية. تأكد من وضوح اللوحة.')
    
    except (OSError, ValueError) as e:
        result['valid'] = False
        result['issues'].append(f'Error validating image: {str(e)}')
        result['issues'].append(f'خطأ في التحقق من الصورة: {str(e)}')
    
    return result


def recognize_plate_from_file(image_path: str, regions: Optional[List[str]] = None,
                             enhance: bool = True, min_confidence: float = 0.0) -> Dict:
    """
    Recognize license plate from an image file
    تمييز لوحة السيارة من ملف صورة
    
    Args:
        image_path: Path to the image file
        regions: Optional list of region codes to improve accuracy (e.g., ['sa'] for Saudi Arabia)
        enhance: Whether to preprocess and enhance the image
        min_confidence: Minimum confidence threshold (0.0-1.0)
    
    Returns:
        Dict containing recognition results with the following structure:
        {
            'success': bool,
            'results': [
                {
                    'plate': str,          # Detected plate number
                    'confidence': float,   # Confidence score (0-1)
                    'region': str,        # Detected region
                    'vehicle_type': str,  # Type of vehicle
                    'candidates': list    # Alternative plate readings
                }
            ],
            'error': str (if success=False),
            'enhanced': bool,     # Whether image was enhanced
            'validation': dict    # Image quality validation results
        }
    """
    if not is_configured():
        return {
            'success': False,
            'error': 'Plate Recognizer API is not configured. Please set PLATE_RECOGNIZER_API_TOKEN in environment.',
            'error_ar': 'خدمة Plate Recognizer غير مفعلة. يرجى تعيين PLATE_RECOGNIZER_API_TOKEN في متغيرات البيئة.'
        }
    
    try:
        with open(image_path, 'rb') as image_file:
            return recognize_plate_from_bytes(image_file.read(), regions, enhance, min_confidence)
    except FileNotFoundError:
        return {
            'success': False,
            'error': f'Image file not found: {image_path}',
            'error_ar': f'لم يتم العثور على ملف الصورة: {image_path}'
        }
    except Exception as e:
        return {
            'success': False,
            'error': f'Error reading image file: {str(e)}',
            'error_ar': f'خطأ في قراءة ملف الصورة: {str(e)}'
        }


def recognize_plate_from_bytes(image_bytes: bytes, regions: Optional[List[str]] = None, 
                              enhance: bool = True, min_confidence: float = 0.0) -> Dict:
    """
    Recognize license plate from image bytes
    تمييز لوحة السيارة من بيانات الصورة
    
    Args:
        image_bytes: Image data as bytes
        regions: Optional list of region codes (e.g., ['sa'] for Saudi Arabia)
        enhance: Whether to preprocess and enhance the image (default: True)
        min_confidence: Minimum confidence threshold (0.0-1.0, default: 0.0)
    
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
        # Validate image quality
        validation = validate_image_quality(image_bytes)
        if not validation['valid']:
            return {
                'success': False,
                'error': 'Image quality validation failed: ' + '; '.join(validation['issues']),
                'error_ar': 'فشل التحقق من جودة الصورة: ' + '; '.join(validation['issues']),
                'validation': validation
            }
        
        # Preprocess image if enhancement is enabled
        processed_bytes = preprocess_image(image_bytes, enhance) if enhance else image_bytes
        
        headers = {
            'Authorization': f'Token {API_TOKEN}'
        }
        
        files = {
            'upload': processed_bytes
        }
        
        data = {}
        if regions:
            data['regions'] = regions
        
        response = requests.post(
            API_URL,
            headers=headers,
            files=files,
            data=data,
            timeout=30
        )
        
        if response.status_code == 200:
            api_response = response.json()
            
            # Parse results
            results = []
            if 'results' in api_response:
                for result in api_response['results']:
                    confidence = result.get('score', 0.0)
                    
                    # Filter by minimum confidence
                    if confidence < min_confidence:
                        continue
                    
                    # Extract candidate plates for verification
                    candidates = []
                    for candidate in result.get('candidates', []):
                        if candidate.get('score', 0.0) >= min_confidence:
                            candidates.append({
                                'plate': candidate.get('plate', '').upper(),
                                'confidence': candidate.get('score', 0.0)
                            })
                    
                    plate_data = {
                        'plate': result.get('plate', '').upper(),
                        'confidence': confidence,
                        'region': result.get('region', {}).get('code', ''),
                        'vehicle_type': result.get('vehicle', {}).get('type', ''),
                        'box': result.get('box', {}),
                        'candidates': candidates[:MAX_CANDIDATES]  # Limit to configured maximum
                    }
                    results.append(plate_data)
            
            return {
                'success': True,
                'results': results,
                'processing_time': api_response.get('processing_time', 0),
                'timestamp': datetime.now().isoformat(),
                'enhanced': enhance,
                'validation': validation if validation.get('warnings') else None
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
                'error': f'API request failed with status {response.status_code}: {response.text}',
                'error_ar': f'فشل طلب API بالحالة {response.status_code}'
            }
    
    except requests.exceptions.Timeout:
        return {
            'success': False,
            'error': 'Request timeout. Please try again.',
            'error_ar': 'انتهى وقت الطلب. يرجى المحاولة مرة أخرى.'
        }
    
    except requests.exceptions.ConnectionError:
        return {
            'success': False,
            'error': 'Connection error. Please check your internet connection.',
            'error_ar': 'خطأ في الاتصال. يرجى التحقق من اتصال الإنترنت.'
        }
    
    except Exception as e:
        return {
            'success': False,
            'error': f'Unexpected error: {str(e)}',
            'error_ar': f'خطأ غير متوقع: {str(e)}'
        }


def recognize_plate_from_base64(base64_image: str, regions: Optional[List[str]] = None,
                               enhance: bool = True, min_confidence: float = 0.0) -> Dict:
    """
    Recognize license plate from base64 encoded image
    تمييز لوحة السيارة من صورة مشفرة base64
    
    Args:
        base64_image: Base64 encoded image string
        regions: Optional list of region codes
        enhance: Whether to preprocess and enhance the image
        min_confidence: Minimum confidence threshold (0.0-1.0)
    
    Returns:
        Dict containing recognition results
    """
    try:
        # Remove data URL prefix if present
        if ',' in base64_image:
            base64_image = base64_image.split(',')[1]
        
        # Decode base64 to bytes
        image_bytes = base64.b64decode(base64_image)
        
        return recognize_plate_from_bytes(image_bytes, regions, enhance, min_confidence)
    
    except Exception as e:
        return {
            'success': False,
            'error': f'Error decoding base64 image: {str(e)}',
            'error_ar': f'خطأ في فك تشفير الصورة: {str(e)}'
        }


def log_plate_recognition(user_id: int, plate_number: str, confidence: float, 
                         vehicle_id: Optional[int] = None, image_path: Optional[str] = None) -> bool:
    """
    Log a plate recognition event to the database
    تسجيل حدث تمييز لوحة السيارة في قاعدة البيانات
    
    Args:
        user_id: ID of the user who performed the recognition
        plate_number: Recognized plate number
        confidence: Confidence score of the recognition
        vehicle_id: Optional ID of the matched vehicle in the database
        image_path: Optional path to the image file
    
    Returns:
        bool: True if logging was successful, False otherwise
    """
    try:
        conn = database.get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO plate_recognition_log 
            (user_id, plate_number, confidence, vehicle_id, image_path, recognized_at)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (user_id, plate_number, confidence, vehicle_id, image_path, datetime.now()))
        
        conn.commit()
        conn.close()
        
        return True
    
    except Exception as e:
        print(f"Error logging plate recognition: {str(e)}")
        return False


def find_vehicle_by_plate(plate_number: str) -> Optional[Dict]:
    """
    Find a vehicle in the database by plate number
    البحث عن مركبة في قاعدة البيانات برقم اللوحة
    
    Args:
        plate_number: The plate number to search for
    
    Returns:
        Dict containing vehicle information if found, None otherwise
    """
    try:
        conn = database.get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT v.*, r.name as owner_name, r.phone, r.unit_number
            FROM vehicles v
            LEFT JOIN residents r ON v.owner_id = r.id
            WHERE v.plate_number = ? AND v.is_active = 1
        ''', (plate_number.upper(),))
        
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return dict(row)
        
        return None
    
    except Exception as e:
        print(f"Error finding vehicle by plate: {str(e)}")
        return None


def get_api_status() -> Dict:
    """
    Check the status of the Plate Recognizer API connection
    التحقق من حالة الاتصال بخدمة Plate Recognizer
    
    Returns:
        Dict containing status information
    """
    if not is_configured():
        return {
            'configured': False,
            'message': 'API token not configured',
            'message_ar': 'لم يتم تكوين رمز API'
        }
    
    try:
        headers = {
            'Authorization': f'Token {API_TOKEN}'
        }
        
        # Use the statistics endpoint to check connection
        response = requests.get(
            'https://api.platerecognizer.com/v1/statistics/',
            headers=headers,
            timeout=10
        )
        
        if response.status_code == 200:
            stats = response.json()
            return {
                'configured': True,
                'connected': True,
                'message': 'API connection successful',
                'message_ar': 'تم الاتصال بنجاح',
                'usage': stats.get('usage', {}),
                'total_calls': stats.get('total_calls', 0)
            }
        else:
            return {
                'configured': True,
                'connected': False,
                'message': f'API connection failed: {response.status_code}',
                'message_ar': f'فشل الاتصال: {response.status_code}'
            }
    
    except Exception as e:
        return {
            'configured': True,
            'connected': False,
            'message': f'Connection error: {str(e)}',
            'message_ar': f'خطأ في الاتصال: {str(e)}'
        }
