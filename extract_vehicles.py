"""
Vehicle Data Extraction System
نظام استخراج بيانات المركبات من الصور

This script processes a folder of vehicle images and extracts:
- License plate numbers (رقم اللوحة)
- Vehicle type (نوع المركبة)
- Dominant color (اللون)

يقوم هذا السكربت بمعالجة مجلد من صور المركبات واستخراج:
- أرقام اللوحات
- أنواع المركبات
- الألوان السائدة

Requirements:
- Python 3.7+
- Plate Recognizer API account with API token
- Internet connection for API calls

Usage:
    python extract_vehicles.py

Configuration:
    Set the following variables before running:
    - IMAGE_FOLDER: Path to folder containing vehicle images
    - API_TOKEN: Your Plate Recognizer API token
"""

import os
import sys
import requests
import pandas as pd
from datetime import datetime
from typing import Dict, List, Optional
import json
import time

try:
    from PIL import Image
    PILLOW_AVAILABLE = True
except ImportError:
    print("⚠️  Warning: Pillow not installed. Image validation will be limited.")
    print("⚠️  تحذير: Pillow غير مثبت. ستكون عملية التحقق من الصور محدودة.")
    PILLOW_AVAILABLE = False

try:
    from colorthief import ColorThief
    COLORTHIEF_AVAILABLE = True
except ImportError:
    print("⚠️  Warning: ColorThief not installed. Color detection will be disabled.")
    print("⚠️  تحذير: ColorThief غير مثبت. سيتم تعطيل اكتشاف الألوان.")
    COLORTHIEF_AVAILABLE = False


# ============================================================================
# CONFIGURATION / الإعدادات
# ============================================================================

# Path to folder containing vehicle images
# مسار مجلد الصور
IMAGE_FOLDER = r"E:\WhatsApp Chat - الامام المرور\6"

# Your Plate Recognizer API Token
# رمز API الخاص بك من Plate Recognizer
API_TOKEN = "ضع رمز API الخاص بك هنا"

# Plate Recognizer API URL
# رابط API الخاص بـ Plate Recognizer
API_URL = "https://api.platerecognizer.com/v1/plate-reader/"

# Output Excel file name
# اسم ملف Excel الناتج
OUTPUT_FILE = "نتائج_المركبات.xlsx"

# Batch size for processing (number of images to process before saving)
# حجم الدفعة (عدد الصور التي تتم معالجتها قبل الحفظ)
BATCH_SIZE = 50

# Delay between API calls (seconds) to avoid rate limiting
# التأخير بين طلبات API (بالثواني) لتجنب تجاوز الحد المسموح
API_DELAY = 0.5

# Enable/disable image enhancement
# تفعيل/تعطيل تحسين الصور
ENHANCE_IMAGES = True

# Minimum confidence threshold (0.0 to 1.0)
# الحد الأدنى للثقة (من 0.0 إلى 1.0)
MIN_CONFIDENCE = 0.0

# Region codes for better accuracy (e.g., ['sa'] for Saudi Arabia)
# رموز المناطق لتحسين الدقة (مثلاً ['sa'] للسعودية)
REGIONS = ['sa']


# ============================================================================
# HELPER FUNCTIONS / الدوال المساعدة
# ============================================================================

def rgb_to_arabic_color(rgb: tuple) -> str:
    """
    Convert RGB values to Arabic color name
    تحويل قيم RGB إلى اسم اللون بالعربية
    
    Args:
        rgb: Tuple of (R, G, B) values
    
    Returns:
        Arabic color name
    """
    r, g, b = rgb
    
    # Calculate color characteristics
    brightness = (r + g + b) / 3
    max_val = max(r, g, b)
    min_val = min(r, g, b)
    saturation = (max_val - min_val) / max_val if max_val > 0 else 0
    
    # Black and white
    if brightness < 50:
        return "أسود"
    elif brightness > 200 and saturation < 0.15:
        return "أبيض"
    elif 150 < brightness < 200 and saturation < 0.2:
        return "رمادي فاتح"
    elif 100 < brightness < 150 and saturation < 0.2:
        return "رمادي"
    elif brightness < 100 and saturation < 0.2:
        return "رمادي غامق"
    
    # Determine dominant color
    if r > g and r > b:
        if g > b:
            return "برتقالي" if saturation > 0.4 else "بيج"
        else:
            return "أحمر" if saturation > 0.5 else "وردي"
    elif g > r and g > b:
        if r > b:
            return "أصفر" if saturation > 0.5 else "كريمي"
        else:
            return "أخضر" if saturation > 0.3 else "أخضر فاتح"
    elif b > r and b > g:
        if r > g:
            return "بنفسجي"
        else:
            return "أزرق" if saturation > 0.3 else "أزرق فاتح"
    else:
        return "بني"


def get_dominant_color(image_path: str) -> str:
    """
    Extract dominant color from vehicle image
    استخراج اللون السائد من صورة المركبة
    
    Args:
        image_path: Path to image file
    
    Returns:
        Color description in Arabic
    """
    if not COLORTHIEF_AVAILABLE:
        return "غير متوفر"
    
    try:
        color_thief = ColorThief(image_path)
        dominant_color = color_thief.get_color(quality=1)
        
        # Get Arabic color name
        arabic_color = rgb_to_arabic_color(dominant_color)
        
        # Return color with RGB values
        return f"{arabic_color} - RGB{dominant_color}"
    
    except Exception as e:
        print(f"   ⚠️  Error extracting color: {str(e)}")
        return "غير معروف"


def validate_image(image_path: str) -> bool:
    """
    Validate if image file is readable and has minimum quality
    التحقق من إمكانية قراءة الصورة وجودتها الدنيا
    
    Args:
        image_path: Path to image file
    
    Returns:
        True if image is valid, False otherwise
    """
    if not PILLOW_AVAILABLE:
        return True  # Skip validation if PIL not available
    
    try:
        with Image.open(image_path) as img:
            width, height = img.size
            
            # Check minimum resolution (400x300)
            if width < 400 or height < 300:
                print(f"   ⚠️  Image too small: {width}x{height}")
                print(f"   ⚠️  الصورة صغيرة جداً: {width}x{height}")
                return False
            
            return True
    
    except Exception as e:
        print(f"   ❌ Error validating image: {str(e)}")
        return False


def recognize_plate(image_path: str) -> Dict:
    """
    Recognize license plate from image using Plate Recognizer API
    التعرف على لوحة السيارة من الصورة باستخدام Plate Recognizer API
    
    Args:
        image_path: Path to image file
    
    Returns:
        Dictionary containing plate number, confidence, and vehicle type
    """
    try:
        with open(image_path, 'rb') as img_file:
            files = {'upload': img_file}
            headers = {'Authorization': f'Token {API_TOKEN}'}
            data = {}
            
            if REGIONS:
                data['regions'] = REGIONS
            
            response = requests.post(
                API_URL,
                files=files,
                headers=headers,
                data=data,
                timeout=30
            )
        
        if response.status_code == 200:
            data = response.json()
            
            if data.get('results'):
                result = data['results'][0]
                
                return {
                    'success': True,
                    'plate': result.get('plate', 'غير مقروء').upper(),
                    'confidence': result.get('score', 0.0),
                    'vehicle_type': result.get('vehicle', {}).get('type', 'غير محدد'),
                    'region': result.get('region', {}).get('code', ''),
                    'candidates': [
                        c.get('plate', '').upper() 
                        for c in result.get('candidates', [])[:3]
                    ]
                }
            else:
                return {
                    'success': False,
                    'plate': 'غير مقروء',
                    'confidence': 0.0,
                    'vehicle_type': 'غير محدد',
                    'error': 'No plate detected'
                }
        
        elif response.status_code == 401:
            return {
                'success': False,
                'plate': 'خطأ API',
                'confidence': 0.0,
                'vehicle_type': 'غير محدد',
                'error': 'Invalid API token'
            }
        
        elif response.status_code == 402:
            return {
                'success': False,
                'plate': 'رصيد منتهي',
                'confidence': 0.0,
                'vehicle_type': 'غير محدد',
                'error': 'Insufficient credits'
            }
        
        else:
            return {
                'success': False,
                'plate': 'خطأ',
                'confidence': 0.0,
                'vehicle_type': 'غير محدد',
                'error': f'API error: {response.status_code}'
            }
    
    except requests.exceptions.Timeout:
        return {
            'success': False,
            'plate': 'انتهى الوقت',
            'confidence': 0.0,
            'vehicle_type': 'غير محدد',
            'error': 'Request timeout'
        }
    
    except Exception as e:
        return {
            'success': False,
            'plate': 'خطأ',
            'confidence': 0.0,
            'vehicle_type': 'غير محدد',
            'error': str(e)
        }


def save_results(results: List[Dict], output_file: str):
    """
    Save results to Excel file
    حفظ النتائج إلى ملف Excel
    
    Args:
        results: List of result dictionaries
        output_file: Output Excel file path
    """
    try:
        df = pd.DataFrame(results)
        
        # Reorder columns for better readability
        column_order = [
            'الرقم التسلسلي',
            'اسم الملف',
            'رقم اللوحة',
            'الثقة',
            'نوع المركبة',
            'اللون',
            'المنطقة',
            'بدائل اللوحة',
            'الحالة',
            'رابط الصورة',
            'وقت المعالجة'
        ]
        
        # Only include columns that exist
        column_order = [col for col in column_order if col in df.columns]
        df = df[column_order]
        
        # Save to Excel
        df.to_excel(output_file, index=False, engine='openpyxl')
        
        print(f"\n✅ Results saved to: {output_file}")
        print(f"✅ تم حفظ النتائج في: {output_file}")
    
    except Exception as e:
        print(f"\n❌ Error saving results: {str(e)}")
        print(f"❌ خطأ في حفظ النتائج: {str(e)}")


def load_progress(progress_file: str) -> Dict:
    """
    Load processing progress from file
    تحميل تقدم المعالجة من الملف
    
    Args:
        progress_file: Path to progress JSON file
    
    Returns:
        Dictionary with progress information
    """
    if os.path.exists(progress_file):
        try:
            with open(progress_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            pass
    
    return {'processed_files': [], 'last_index': 0}


def save_progress(progress: Dict, progress_file: str):
    """
    Save processing progress to file
    حفظ تقدم المعالجة إلى ملف
    
    Args:
        progress: Progress dictionary
        progress_file: Path to progress JSON file
    """
    try:
        with open(progress_file, 'w', encoding='utf-8') as f:
            json.dump(progress, f, ensure_ascii=False, indent=2)
    except:
        pass


# ============================================================================
# MAIN PROCESSING FUNCTION / الدالة الرئيسية للمعالجة
# ============================================================================

def process_images():
    """
    Main function to process all images in the folder
    الدالة الرئيسية لمعالجة جميع الصور في المجلد
    """
    
    print("\n" + "="*70)
    print("🚗 Vehicle Data Extraction System")
    print("🚗 نظام استخراج بيانات المركبات")
    print("="*70)
    
    # Validate configuration
    print("\n📋 Checking configuration...")
    print("📋 التحقق من الإعدادات...")
    
    if API_TOKEN == "ضع رمز API الخاص بك هنا":
        print("\n❌ ERROR: API token not configured!")
        print("❌ خطأ: لم يتم تكوين رمز API!")
        print("\nPlease edit the script and set your API_TOKEN.")
        print("يرجى تعديل السكربت وتعيين API_TOKEN الخاص بك.")
        sys.exit(1)
    
    if not os.path.exists(IMAGE_FOLDER):
        print(f"\n❌ ERROR: Image folder not found: {IMAGE_FOLDER}")
        print(f"❌ خطأ: مجلد الصور غير موجود: {IMAGE_FOLDER}")
        print("\nPlease edit the script and set the correct IMAGE_FOLDER path.")
        print("يرجى تعديل السكربت وتعيين مسار IMAGE_FOLDER الصحيح.")
        sys.exit(1)
    
    print("✅ Configuration OK")
    print("✅ الإعدادات صحيحة")
    
    # Get list of image files
    print(f"\n📁 Scanning folder: {IMAGE_FOLDER}")
    print(f"📁 فحص المجلد: {IMAGE_FOLDER}")
    
    image_files = []
    supported_extensions = ('.jpg', '.jpeg', '.png', '.bmp')
    
    for filename in os.listdir(IMAGE_FOLDER):
        if filename.lower().endswith(supported_extensions):
            image_files.append(filename)
    
    if not image_files:
        print("\n❌ ERROR: No image files found in folder!")
        print("❌ خطأ: لم يتم العثور على صور في المجلد!")
        sys.exit(1)
    
    total_images = len(image_files)
    print(f"\n📊 Found {total_images} images to process")
    print(f"📊 تم العثور على {total_images} صورة للمعالجة")
    
    # Load previous progress if exists
    progress_file = OUTPUT_FILE.replace('.xlsx', '_progress.json')
    progress = load_progress(progress_file)
    processed_files = set(progress.get('processed_files', []))
    
    if processed_files:
        print(f"\n🔄 Resuming from previous session...")
        print(f"🔄 استئناف من الجلسة السابقة...")
        print(f"   Already processed: {len(processed_files)} files")
        print(f"   تم معالجتها مسبقاً: {len(processed_files)} ملف")
    
    # Process images
    results = []
    successful = 0
    failed = 0
    start_time = datetime.now()
    
    print(f"\n🚀 Starting processing...")
    print(f"🚀 بدء المعالجة...")
    print(f"   Batch size: {BATCH_SIZE} images")
    print(f"   حجم الدفعة: {BATCH_SIZE} صورة")
    print(f"   API delay: {API_DELAY} seconds")
    print(f"   تأخير API: {API_DELAY} ثانية")
    print("-" * 70)
    
    for index, filename in enumerate(image_files, 1):
        # Skip if already processed
        if filename in processed_files:
            continue
        
        image_path = os.path.join(IMAGE_FOLDER, filename)
        
        print(f"\n[{index}/{total_images}] Processing: {filename}")
        print(f"[{index}/{total_images}] معالجة: {filename}")
        
        # Validate image
        if not validate_image(image_path):
            print("   ❌ Image validation failed - skipping")
            print("   ❌ فشل التحقق من الصورة - تخطي")
            
            results.append({
                'الرقم التسلسلي': index,
                'اسم الملف': filename,
                'رقم اللوحة': 'صورة غير صالحة',
                'الثقة': 0.0,
                'نوع المركبة': 'غير محدد',
                'اللون': 'غير متوفر',
                'المنطقة': '',
                'بدائل اللوحة': '',
                'الحالة': 'فشل - صورة غير صالحة',
                'رابط الصورة': image_path,
                'وقت المعالجة': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            })
            
            failed += 1
            continue
        
        # Recognize plate
        print("   🔍 Recognizing plate...")
        print("   🔍 التعرف على اللوحة...")
        
        recognition = recognize_plate(image_path)
        
        # Get color
        print("   🎨 Detecting color...")
        print("   🎨 اكتشاف اللون...")
        
        color = get_dominant_color(image_path)
        
        # Store result
        status = "نجح" if recognition.get('success') else "فشل"
        if recognition.get('error'):
            status += f" - {recognition['error']}"
        
        candidates_str = ', '.join(recognition.get('candidates', []))
        
        result = {
            'الرقم التسلسلي': index,
            'اسم الملف': filename,
            'رقم اللوحة': recognition['plate'],
            'الثقة': round(recognition['confidence'], 3),
            'نوع المركبة': recognition['vehicle_type'],
            'اللون': color,
            'المنطقة': recognition.get('region', ''),
            'بدائل اللوحة': candidates_str,
            'الحالة': status,
            'رابط الصورة': image_path,
            'وقت المعالجة': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        
        results.append(result)
        
        if recognition.get('success'):
            successful += 1
            print(f"   ✅ Plate: {recognition['plate']} (Confidence: {recognition['confidence']:.2%})")
            print(f"   ✅ اللوحة: {recognition['plate']} (الثقة: {recognition['confidence']:.2%})")
        else:
            failed += 1
            print(f"   ❌ Failed: {recognition.get('error', 'Unknown error')}")
            print(f"   ❌ فشل: {recognition.get('error', 'خطأ غير معروف')}")
        
        # Mark as processed
        processed_files.add(filename)
        
        # Save progress every BATCH_SIZE images
        if len(results) % BATCH_SIZE == 0:
            print(f"\n💾 Saving intermediate results...")
            print(f"💾 حفظ النتائج المؤقتة...")
            save_results(results, OUTPUT_FILE)
            
            # Save progress
            progress['processed_files'] = list(processed_files)
            progress['last_index'] = index
            save_progress(progress, progress_file)
            
            print(f"   ✅ Saved {len(results)} results")
            print(f"   ✅ تم حفظ {len(results)} نتيجة")
        
        # Delay between API calls
        if index < total_images:
            time.sleep(API_DELAY)
    
    # Save final results
    print(f"\n💾 Saving final results...")
    print(f"💾 حفظ النتائج النهائية...")
    save_results(results, OUTPUT_FILE)
    
    # Clean up progress file
    if os.path.exists(progress_file):
        os.remove(progress_file)
    
    # Print summary
    end_time = datetime.now()
    duration = (end_time - start_time).total_seconds()
    
    print("\n" + "="*70)
    print("📊 PROCESSING SUMMARY / ملخص المعالجة")
    print("="*70)
    print(f"Total images:      {total_images} / إجمالي الصور")
    print(f"Successful:        {successful} / نجح")
    print(f"Failed:            {failed} / فشل")
    print(f"Success rate:      {(successful/total_images*100):.1f}% / نسبة النجاح")
    print(f"Processing time:   {duration:.1f} seconds / وقت المعالجة")
    print(f"Output file:       {OUTPUT_FILE} / ملف النتائج")
    print("="*70)
    
    print("\n✅ Processing complete!")
    print("✅ اكتملت المعالجة!")
    print(f"\n📄 Results saved to: {OUTPUT_FILE}")
    print(f"📄 تم حفظ النتائج في: {OUTPUT_FILE}")


# ============================================================================
# SCRIPT ENTRY POINT / نقطة دخول السكربت
# ============================================================================

if __name__ == "__main__":
    try:
        process_images()
    except KeyboardInterrupt:
        print("\n\n⚠️  Processing interrupted by user")
        print("⚠️  تم إيقاف المعالجة من قبل المستخدم")
        print("\n💡 Progress has been saved. Run the script again to resume.")
        print("💡 تم حفظ التقدم. شغّل السكربت مرة أخرى للاستئناف.")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Unexpected error: {str(e)}")
        print(f"❌ خطأ غير متوقع: {str(e)}")
        sys.exit(1)
