# دليل استخدام نظام تمييز لوحات السيارات
# Plate Recognizer Integration Guide

## نظرة عامة | Overview

تم دمج نظام Faculty Housing Management مع خدمة **Plate Recognizer ParkPow** لتمييز لوحات السيارات تلقائياً من الصور. هذه الميزة تتيح التعرف السريع على المركبات وربطها بسكان الإسكان.

The Faculty Housing Management System has been integrated with **Plate Recognizer ParkPow** service for automatic license plate recognition from images. This feature enables quick vehicle identification and linking to housing residents.

## رابط الخدمة | Service URL

https://app.platerecognizer.com/service/parkpow/

## المتطلبات | Requirements

### 1. الحصول على رمز API | Get API Token

1. قم بزيارة موقع Plate Recognizer: https://app.platerecognizer.com/
2. أنشئ حساب جديد أو سجل الدخول
3. اذهب إلى قسم "API Token" في لوحة التحكم
4. انسخ رمز API الخاص بك

---

1. Visit Plate Recognizer website: https://app.platerecognizer.com/
2. Create a new account or login
3. Go to "API Token" section in the dashboard
4. Copy your API token

### 2. إعداد التكوين | Configuration Setup

#### استخدام ملف البيئة | Using Environment File

1. أنشئ ملف `.env` في المجلد الرئيسي للمشروع
2. أضف التكوين التالي:

```bash
# Plate Recognizer ParkPow API Configuration
PLATE_RECOGNIZER_API_TOKEN=your-actual-api-token-here
PLATE_RECOGNIZER_API_URL=https://api.platerecognizer.com/v1/plate-reader/
```

3. استبدل `your-actual-api-token-here` برمز API الخاص بك

---

1. Create a `.env` file in the project root directory
2. Add the following configuration:

```bash
# Plate Recognizer ParkPow API Configuration
PLATE_RECOGNIZER_API_TOKEN=your-actual-api-token-here
PLATE_RECOGNIZER_API_URL=https://api.platerecognizer.com/v1/plate-reader/
```

3. Replace `your-actual-api-token-here` with your actual API token

#### استخدام متغيرات البيئة | Using Environment Variables

بدلاً من ملف `.env`, يمكنك تعيين متغيرات البيئة مباشرة:

Instead of `.env` file, you can set environment variables directly:

**Linux/Mac:**
```bash
export PLATE_RECOGNIZER_API_TOKEN="your-actual-api-token-here"
export PLATE_RECOGNIZER_API_URL="https://api.platerecognizer.com/v1/plate-reader/"
```

**Windows:**
```cmd
set PLATE_RECOGNIZER_API_TOKEN=your-actual-api-token-here
set PLATE_RECOGNIZER_API_URL=https://api.platerecognizer.com/v1/plate-reader/
```

### 3. إعادة تشغيل الخادم | Restart Server

بعد إعداد التكوين، أعد تشغيل الخادم:

After configuration, restart the server:

```bash
python3 server.py
```

## استخدام الواجهة | Using the Interface

### الوصول إلى صفحة تمييز اللوحات | Access Plate Recognition Page

1. سجل الدخول إلى النظام
2. من لوحة التحكم الرئيسية، اذهب إلى قسم "الأمن والسلامة"
3. اضغط على "تمييز لوحات السيارات"

---

1. Login to the system
2. From the main dashboard, go to "Security & Safety" section
3. Click on "تمييز لوحات السيارات" (Plate Recognition)

### إعدادات الدقة العالية | High Accuracy Settings

النظام يوفر الآن إعدادات متقدمة لتحسين دقة التعرف على اللوحات:

The system now provides advanced settings to improve plate recognition accuracy:

1. **تحسين الصورة تلقائياً** | **Auto Image Enhancement**
   - يتم تطبيق تحسينات تلقائية على الصورة (تباين، حدة، سطوع)
   - يحسن من دقة التعرف بنسبة تصل إلى 30%
   - Automatic enhancements applied (contrast, sharpness, brightness)
   - Improves recognition accuracy by up to 30%

2. **الحد الأدنى للثقة** | **Minimum Confidence Threshold**
   - 0% - عرض جميع النتائج | Show all results
   - 50% - دقة متوسطة | Medium accuracy
   - **70% - دقة عالية (موصى به)** | **High accuracy (recommended)**
   - 80% - دقة عالية جداً | Very high accuracy
   - 90% - دقة قصوى | Maximum accuracy

3. **اختيار المنطقة** | **Region Selection**
   - السعودية | Saudi Arabia
   - الإمارات | UAE
   - الكويت | Kuwait
   - البحرين | Bahrain
   - قطر | Qatar
   - عمان | Oman

### رفع الصورة وتمييز اللوحة | Upload Image and Recognize Plate

1. **رفع الصورة** | **Upload Image**
   - اضغط على منطقة الرفع أو اسحب الصورة إليها
   - الصور المدعومة: JPG, PNG
   - **يُفضل دقة عالية (800×600 أو أكثر) للنتائج الأفضل**
   - Click on upload area or drag image to it
   - Supported formats: JPG, PNG
   - **Higher resolution (800×600 or more) recommended for best results**

2. **معلومات جودة الصورة** | **Image Quality Information**
   - يعرض النظام تلقائياً دقة الصورة وحجمها
   - تحذيرات إذا كانت الدقة منخفضة
   - System automatically displays image resolution and size
   - Warnings if resolution is low

3. **تمييز اللوحة** | **Recognize Plate**
   - بعد رفع الصورة، اضغط على زر "تمييز اللوحة بدقة عالية"
   - انتظر معالجة الصورة (عادة 2-5 ثواني)
   - After uploading, click "تمييز اللوحة بدقة عالية" button
   - Wait for processing (usually 2-5 seconds)

4. **عرض النتائج** | **View Results**
   - رقم اللوحة المكتشف
   - نسبة الدقة (Confidence Score)
   - **قراءات بديلة للتحقق** | **Alternative readings for verification**
   - معلومات المركبة إذا كانت مسجلة في النظام
   - معلومات المالك والوحدة السكنية
   - مؤشرات تحسين الصورة
   
   ---
   
   - Detected plate number
   - Confidence score
   - **Alternative plate readings for verification**
   - Vehicle information if registered in the system
   - Owner and unit information
   - Image enhancement indicators

### سجل التمييز | Recognition History

يتم حفظ جميع عمليات التمييز في قاعدة البيانات ويمكن الاطلاع عليها من قسم "سجل التمييز" في نفس الصفحة.

All recognition operations are saved in the database and can be viewed in the "Recognition History" section on the same page.

## استخدام API مباشرة | Using API Directly

### التحقق من حالة الخدمة | Check Service Status

```bash
curl -X GET http://localhost:5000/api/plate-recognizer/status \
  -H "Cookie: session_token=YOUR_SESSION_TOKEN"
```

### تمييز لوحة من صورة | Recognize Plate from Image

```bash
curl -X POST http://localhost:5000/api/plate-recognizer/recognize \
  -H "Cookie: session_token=YOUR_SESSION_TOKEN" \
  -F "image=@/path/to/image.jpg" \
  -F "regions=sa"
```

### عرض سجل التمييز | View Recognition History

```bash
curl -X GET http://localhost:5000/api/plate-recognizer/history?limit=10 \
  -H "Cookie: session_token=YOUR_SESSION_TOKEN"
```

## نموذج الاستجابة | Response Example

### استجابة ناجحة | Successful Response

```json
{
  "success": true,
  "results": [
    {
      "plate": "ABC1234",
      "confidence": 0.95,
      "region": "sa",
      "vehicle_type": "Car",
      "vehicle_info": {
        "id": 123,
        "owner_name": "د. أحمد محمد",
        "unit_number": "A-101",
        "vehicle_type": "سيارة",
        "make": "تويوتا",
        "model": "كامري",
        "color": "أبيض",
        "sticker_number": "ST-2025-001"
      }
    }
  ],
  "processing_time": 2.5,
  "timestamp": "2025-11-05T10:30:00"
}
```

### استجابة عند عدم العثور على لوحة | No Plate Found

```json
{
  "success": true,
  "results": [],
  "processing_time": 1.8,
  "timestamp": "2025-11-05T10:30:00"
}
```

### استجابة خطأ | Error Response

```json
{
  "success": false,
  "error": "Invalid API token",
  "error_ar": "رمز API غير صالح"
}
```

## قاعدة البيانات | Database

### جدول سجل التمييز | Recognition Log Table

```sql
CREATE TABLE plate_recognition_log (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    plate_number TEXT NOT NULL,
    confidence REAL,
    vehicle_id INTEGER,
    image_path TEXT,
    recognized_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users (id),
    FOREIGN KEY (vehicle_id) REFERENCES vehicles (id)
);
```

## الأمان | Security

### الصلاحيات | Permissions

- يتطلب تسجيل الدخول للوصول إلى جميع نقاط API
- يتم تسجيل جميع العمليات في سجل التدقيق
- Authentication required for all API endpoints
- All operations are logged in audit log

### خصوصية البيانات | Data Privacy

- لا يتم تخزين الصور في الخادم بشكل افتراضي
- يتم إرسال الصور مباشرة إلى Plate Recognizer API
- يتم تشفير الاتصال بـ HTTPS
- Images are not stored on server by default
- Images are sent directly to Plate Recognizer API
- Connection is encrypted with HTTPS

## استكشاف الأخطاء | Troubleshooting

### المشكلة: "الخدمة غير مفعلة" | Issue: "API not configured"

**الحل | Solution:**
- تأكد من تعيين `PLATE_RECOGNIZER_API_TOKEN` في متغيرات البيئة أو ملف `.env`
- أعد تشغيل الخادم بعد التعديل
- Ensure `PLATE_RECOGNIZER_API_TOKEN` is set in environment or `.env` file
- Restart server after modification

### المشكلة: "رصيد غير كافٍ" | Issue: "Insufficient credits"

**الحل | Solution:**
- تحقق من رصيدك في حساب Plate Recognizer
- قم بشراء رصيد إضافي إذا لزم الأمر
- Check your credit balance in Plate Recognizer account
- Purchase additional credits if needed

### المشكلة: "خطأ في الاتصال" | Issue: "Connection error"

**الحل | Solution:**
- تحقق من اتصال الإنترنت
- تأكد من عدم حظر الجدار الناري للاتصال بـ api.platerecognizer.com
- Check internet connection
- Ensure firewall is not blocking api.platerecognizer.com

## الدعم | Support

للحصول على دعم فني:
- Plate Recognizer: https://guides.platerecognizer.com/
- النظام: اتصل بفريق تقنية المعلومات بالجامعة

For technical support:
- Plate Recognizer: https://guides.platerecognizer.com/
- System: Contact university IT team

## حدود الاستخدام | Usage Limits

- تعتمد حدود الاستخدام على خطة Plate Recognizer الخاصة بك
- الخطة المجانية: 2,500 طلب/شهر
- الخطط المدفوعة: راجع موقع Plate Recognizer

---

- Usage limits depend on your Plate Recognizer plan
- Free plan: 2,500 requests/month
- Paid plans: Check Plate Recognizer website

## ملاحظات مهمة | Important Notes

⚠️ **تنبيه** | **Warning:**
- رمز API حساس وسري - لا تشاركه أو تضعه في نظام التحكم بالإصدارات
- استخدم ملف `.env` واتأكد من إضافته إلى `.gitignore`

---

- API token is sensitive and confidential - don't share it or commit it to version control
- Use `.env` file and ensure it's added to `.gitignore`

✅ **أفضل الممارسات للحصول على دقة عالية** | **Best Practices for High Accuracy:**
- استخدم صور واضحة وذات دقة جيدة (800×600 بكسل كحد أدنى، 1920×1080 موصى به)
- تأكد من رؤية اللوحة بشكل كامل في الصورة
- استخدم الإضاءة المناسبة (تجنب الظلال القوية أو الإضاءة الزائدة)
- التقط الصورة من زاوية مباشرة قدر الإمكان
- **فعّل خيار "تحسين الصورة تلقائياً" للحصول على أفضل النتائج**
- استخدم حد أدنى للثقة 70% أو أكثر لتصفية النتائج الضعيفة
- راجع القراءات البديلة عند وجود شك في النتيجة
- اختر المنطقة الجغرافية الصحيحة للوحة

---

- Use clear, high-resolution images (minimum 800×600 pixels, 1920×1080 recommended)
- Ensure the plate is fully visible in the image
- Use proper lighting (avoid strong shadows or overexposure)
- Capture image from as direct angle as possible
- **Enable "Auto Image Enhancement" for best results**
- Use minimum confidence threshold of 70% or higher to filter weak results
- Review alternative readings when in doubt
- Select the correct geographic region for the plate

## ميزات الدقة العالية | High Accuracy Features

### تحسين الصورة التلقائي | Automatic Image Enhancement

يقوم النظام بتطبيق التحسينات التالية تلقائياً عند تفعيل الخيار:

The system automatically applies the following enhancements when enabled:

1. **تحسين التباين** | **Contrast Enhancement**
   - يزيد من وضوح الحروف والأرقام على اللوحة
   - Increases visibility of characters and numbers on the plate

2. **زيادة الحدة** | **Sharpness Enhancement**
   - يجعل حواف اللوحة أكثر وضوحاً
   - Makes plate edges clearer

3. **ضبط السطوع** | **Brightness Adjustment**
   - يحسن من رؤية اللوحة في ظروف الإضاءة المختلفة
   - Improves plate visibility in different lighting conditions

4. **تطبيق مرشح الحدة** | **Sharpening Filter**
   - يحسن من جودة الصورة الإجمالية
   - Improves overall image quality

### التحقق من جودة الصورة | Image Quality Validation

قبل معالجة الصورة، يقوم النظام بالتحقق من:

Before processing, the system validates:

- **الدقة** | **Resolution**: الحد الأدنى 400×300، موصى به 800×600 أو أكثر
- **حجم الملف** | **File Size**: تحذير عند تجاوز 10 ميجابايت
- **نسبة الأبعاد** | **Aspect Ratio**: التحقق من نسبة معقولة للصورة

### القراءات البديلة | Alternative Readings

- يعرض النظام حتى 5 قراءات بديلة مع نسب الثقة
- مفيد للتحقق اليدوي عند وجود شك
- يساعد في التعامل مع اللوحات المتآكلة أو غير الواضحة

---

- System displays up to 5 alternative readings with confidence scores
- Useful for manual verification when in doubt
- Helps with worn or unclear plates
