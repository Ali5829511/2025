"""
Car Image Analyzer Module
نظام تحليل صور السيارات

This module provides functionality to analyze car images and extract:
- License plate numbers
- Vehicle type
- Vehicle color

Using EasyOCR for OCR with Arabic support.
"""

import os
import re
from typing import Dict, List, Optional, Tuple
from datetime import datetime
import database
from PIL import Image
import io


def init_easyocr_reader():
    """
    Initialize EasyOCR reader with Arabic and English support
    تهيئة قارئ EasyOCR مع دعم العربية والإنجليزية
    
    Returns:
        easyocr.Reader or None
    """
    try:
        import easyocr
        # Initialize reader with Arabic and English
        reader = easyocr.Reader(['ar', 'en'], gpu=False)
        return reader
    except Exception as e:
        print(f"Error initializing EasyOCR: {str(e)}")
        return None


# Global reader instance (lazy initialization)
_reader = None


def get_reader():
    """Get or initialize the EasyOCR reader"""
    global _reader
    if _reader is None:
        _reader = init_easyocr_reader()
    return _reader


def extract_plate_number(text_results: List) -> Tuple[Optional[str], float]:
    """
    Extract license plate number from OCR results
    استخراج رقم اللوحة من نتائج OCR
    
    Args:
        text_results: List of OCR detection results
    
    Returns:
        Tuple of (plate_number, confidence)
    """
    plate_patterns = [
        r'[أ-ي]{1,3}\s*\d{1,4}',  # Arabic letters + numbers
        r'[A-Z]{1,3}\s*\d{1,4}',   # English letters + numbers
        r'\d{1,4}\s*[أ-ي]{1,3}',  # Numbers + Arabic letters
        r'\d{1,4}\s*[A-Z]{1,3}',   # Numbers + English letters
    ]
    
    best_match = None
    best_confidence = 0.0
    
    for detection in text_results:
        text = detection[1].strip()
        confidence = detection[2]
        
        # Try to match plate patterns
        for pattern in plate_patterns:
            if re.search(pattern, text, re.UNICODE):
                if confidence > best_confidence:
                    best_match = text
                    best_confidence = confidence
                    break
    
    return best_match, best_confidence


def detect_vehicle_type(image) -> str:
    """
    Detect vehicle type from image
    تحديد نوع السيارة من الصورة
    
    Args:
        image: PIL Image object
    
    Returns:
        Vehicle type string
    """
    # Simple heuristic based on image aspect ratio
    # In a production system, this would use a trained model
    width, height = image.size
    aspect_ratio = width / height
    
    if aspect_ratio > 1.5:
        return "سيارة"  # Car
    elif aspect_ratio > 1.2:
        return "شاحنة صغيرة"  # Pickup truck
    else:
        return "سيارة"  # Default to car
    
    # This is a placeholder - in production, use a proper vehicle classifier
    return "غير محدد"


def detect_vehicle_color(image) -> str:
    """
    Detect dominant color in image
    تحديد اللون السائد في الصورة
    
    Args:
        image: PIL Image object
    
    Returns:
        Color name in Arabic
    """
    try:
        # Convert to RGB if needed
        if image.mode != 'RGB':
            image = image.convert('RGB')
        
        # Resize for faster processing
        small_image = image.resize((100, 100))
        
        # Get pixel data
        pixels = list(small_image.getdata())
        
        # Calculate average RGB
        r_avg = sum(p[0] for p in pixels) / len(pixels)
        g_avg = sum(p[1] for p in pixels) / len(pixels)
        b_avg = sum(p[2] for p in pixels) / len(pixels)
        
        # Simple color classification
        if r_avg > 200 and g_avg > 200 and b_avg > 200:
            return "أبيض"  # White
        elif r_avg < 50 and g_avg < 50 and b_avg < 50:
            return "أسود"  # Black
        elif r_avg > g_avg and r_avg > b_avg:
            if r_avg > 150:
                return "أحمر"  # Red
            else:
                return "بني"  # Brown
        elif b_avg > r_avg and b_avg > g_avg:
            return "أزرق"  # Blue
        elif g_avg > r_avg and g_avg > b_avg:
            return "أخضر"  # Green
        elif abs(r_avg - g_avg) < 30 and abs(r_avg - b_avg) < 30:
            if r_avg > 150:
                return "رمادي فاتح"  # Light gray
            else:
                return "رمادي"  # Gray
        else:
            return "متعدد الألوان"  # Multi-colored
            
    except Exception as e:
        print(f"Error detecting color: {str(e)}")
        return "غير محدد"  # Unknown


def analyze_car_image(image_path: str) -> Dict:
    """
    Analyze a car image to extract plate number, type, and color
    تحليل صورة سيارة لاستخراج رقم اللوحة والنوع واللون
    
    Args:
        image_path: Path to the car image
    
    Returns:
        Dict containing analysis results:
        {
            'success': bool,
            'plate_number': str,
            'plate_confidence': float,
            'vehicle_type': str,
            'vehicle_color': str,
            'error': str (if success=False)
        }
    """
    try:
        # Get EasyOCR reader
        reader = get_reader()
        
        if reader is None:
            return {
                'success': False,
                'error': 'EasyOCR reader not initialized',
                'error_ar': 'فشل تهيئة قارئ EasyOCR'
            }
        
        # Read image
        image = Image.open(image_path)
        
        # Perform OCR
        ocr_results = reader.readtext(image_path)
        
        # Extract plate number
        plate_number, plate_confidence = extract_plate_number(ocr_results)
        
        # Detect vehicle type and color
        vehicle_type = detect_vehicle_type(image)
        vehicle_color = detect_vehicle_color(image)
        
        return {
            'success': True,
            'plate_number': plate_number if plate_number else 'غير محدد',
            'plate_confidence': plate_confidence,
            'vehicle_type': vehicle_type,
            'vehicle_color': vehicle_color,
            'ocr_results': ocr_results  # Include raw OCR results for debugging
        }
        
    except FileNotFoundError:
        return {
            'success': False,
            'error': f'Image file not found: {image_path}',
            'error_ar': f'لم يتم العثور على ملف الصورة: {image_path}'
        }
    except Exception as e:
        return {
            'success': False,
            'error': f'Error analyzing image: {str(e)}',
            'error_ar': f'خطأ في تحليل الصورة: {str(e)}'
        }


def analyze_car_image_from_bytes(image_bytes: bytes, filename: str = "image.jpg") -> Dict:
    """
    Analyze a car image from bytes data
    تحليل صورة سيارة من بيانات البايتات
    
    Args:
        image_bytes: Image data as bytes
        filename: Original filename for context
    
    Returns:
        Dict containing analysis results
    """
    try:
        # Get EasyOCR reader
        reader = get_reader()
        
        if reader is None:
            return {
                'success': False,
                'error': 'EasyOCR reader not initialized',
                'error_ar': 'فشل تهيئة قارئ EasyOCR'
            }
        
        # Create PIL Image from bytes
        image = Image.open(io.BytesIO(image_bytes))
        
        # Save temporarily for OCR processing
        import tempfile
        with tempfile.NamedTemporaryFile(delete=False, suffix='.jpg') as tmp_file:
            temp_path = tmp_file.name
            image.save(temp_path)
        
        try:
            # Perform OCR
            ocr_results = reader.readtext(temp_path)
            
            # Extract plate number
            plate_number, plate_confidence = extract_plate_number(ocr_results)
            
            # Detect vehicle type and color
            vehicle_type = detect_vehicle_type(image)
            vehicle_color = detect_vehicle_color(image)
            
            return {
                'success': True,
                'plate_number': plate_number if plate_number else 'غير محدد',
                'plate_confidence': plate_confidence,
                'vehicle_type': vehicle_type,
                'vehicle_color': vehicle_color,
                'ocr_results': ocr_results
            }
        finally:
            # Clean up temp file
            if os.path.exists(temp_path):
                os.remove(temp_path)
        
    except Exception as e:
        return {
            'success': False,
            'error': f'Error analyzing image: {str(e)}',
            'error_ar': f'خطأ في تحليل الصورة: {str(e)}'
        }


def create_thumbnail(image_path: str, thumbnail_path: str, max_size: Tuple[int, int] = (300, 300)) -> bool:
    """
    Create a thumbnail from an image
    إنشاء صورة مصغرة
    
    Args:
        image_path: Path to original image
        thumbnail_path: Path to save thumbnail
        max_size: Maximum thumbnail dimensions (width, height)
    
    Returns:
        bool: True if successful
    """
    try:
        image = Image.open(image_path)
        # Use LANCZOS for better quality - try new API first, fallback to old
        try:
            resample_filter = Image.Resampling.LANCZOS
        except AttributeError:
            resample_filter = Image.LANCZOS
        image.thumbnail(max_size, resample_filter)
        
        # Ensure directory exists
        os.makedirs(os.path.dirname(thumbnail_path), exist_ok=True)
        
        image.save(thumbnail_path, 'JPEG', quality=85)
        return True
    except Exception as e:
        print(f"Error creating thumbnail: {str(e)}")
        return False


def find_matching_vehicle(plate_number: str) -> Optional[Dict]:
    """
    Find a vehicle in the database by plate number
    البحث عن مركبة في قاعدة البيانات
    
    Args:
        plate_number: Plate number to search
    
    Returns:
        Vehicle dict if found, None otherwise
    """
    try:
        conn = database.get_db_connection()
        cursor = conn.cursor()
        
        # Clean plate number for matching
        clean_plate = plate_number.strip().upper()
        
        cursor.execute('''
            SELECT v.*, r.name as owner_name, r.phone, r.unit_number
            FROM vehicles v
            LEFT JOIN residents r ON v.owner_id = r.id
            WHERE UPPER(v.plate_number) = ? AND v.is_active = 1
        ''', (clean_plate,))
        
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return dict(row)
        
        return None
    
    except Exception as e:
        print(f"Error finding vehicle: {str(e)}")
        return None


def get_vehicle_violations(vehicle_id: int) -> List[Dict]:
    """
    Get all violations for a vehicle
    الحصول على جميع المخالفات لمركبة
    
    Args:
        vehicle_id: Vehicle ID
    
    Returns:
        List of violation dicts
    """
    try:
        conn = database.get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT tv.*, u.name as reported_by_name
            FROM traffic_violations tv
            LEFT JOIN users u ON tv.reported_by = u.id
            WHERE tv.vehicle_id = ?
            ORDER BY tv.violation_date DESC
        ''', (vehicle_id,))
        
        rows = cursor.fetchall()
        conn.close()
        
        return [dict(row) for row in rows]
    
    except Exception as e:
        print(f"Error getting violations: {str(e)}")
        return []


def save_car_analysis(car_image_id: int, analysis_result: Dict, vehicle_id: Optional[int] = None) -> Optional[int]:
    """
    Save car analysis results to database
    حفظ نتائج تحليل السيارة في قاعدة البيانات
    
    Args:
        car_image_id: ID of the car image
        analysis_result: Analysis result dict
        vehicle_id: Optional matched vehicle ID
    
    Returns:
        ID of created analysis record, or None if failed
    """
    try:
        conn = database.get_db_connection()
        cursor = conn.cursor()
        
        violation_count = 0
        if vehicle_id:
            # Count violations for this vehicle
            cursor.execute('SELECT COUNT(*) FROM traffic_violations WHERE vehicle_id = ?', (vehicle_id,))
            violation_count = cursor.fetchone()[0]
        
        cursor.execute('''
            INSERT INTO car_analysis 
            (car_image_id, plate_number, plate_confidence, vehicle_type, vehicle_color, 
             vehicle_id, violation_count, analysis_date)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            car_image_id,
            analysis_result.get('plate_number'),
            analysis_result.get('plate_confidence', 0.0),
            analysis_result.get('vehicle_type'),
            analysis_result.get('vehicle_color'),
            vehicle_id,
            violation_count,
            datetime.now()
        ))
        
        analysis_id = cursor.lastrowid
        
        # Mark car image as processed
        cursor.execute('UPDATE car_images SET processed = 1 WHERE id = ?', (car_image_id,))
        
        conn.commit()
        conn.close()
        
        return analysis_id
    
    except Exception as e:
        print(f"Error saving car analysis: {str(e)}")
        return None
