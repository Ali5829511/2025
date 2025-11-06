# دليل نظام تتبع السيارات الشامل
# Comprehensive Vehicle Tracking System Guide

## نظرة عامة / Overview

نظام شامل لتتبع وتسجيل جميع السيارات الداخلة لإسكان أعضاء هيئة التدريس مع التكامل الكامل مع نظام التعرف الآلي على لوحات السيارات.

A comprehensive system for tracking and recording all vehicles entering the faculty housing with full integration with automatic license plate recognition system.

---

## المزايا الرئيسية / Key Features

### 1. قاعدة بيانات شاملة / Comprehensive Database
- تسجيل كل سيارة تدخل الإسكان / Record every vehicle entering housing
- بيانات كاملة عن السيارة والسائق والغرض / Complete data about vehicle, driver, and purpose
- تتبع أوقات الدخول والخروج / Track entry and exit times
- حفظ صور اللوحات (اختياري) / Save plate images (optional)

### 2. تصنيفات السيارات / Vehicle Categories
- **سكان (Residents)**: مركبات أعضاء هيئة التدريس المقيمين
- **زوار (Visitors)**: سيارات زوار السكان
- **مندوبين (Delivery)**: سيارات التوصيل والشحن
- **موظفين (Staff)**: مركبات الموظفين العاملين
- **مقاولين (Contractors)**: سيارات المقاولين والصيانة
- **طوارئ (Emergency)**: مركبات الطوارئ (إسعاف، إطفاء، إلخ)
- **أخرى (Other)**: أي تصنيف آخر

### 3. التكامل مع Plate Recognizer / Plate Recognizer Integration
- التعرف الآلي على لوحات السيارات / Automatic plate recognition
- دعم الكاميرا المباشرة / Direct camera support
- ربط تلقائي مع قاعدة البيانات / Automatic database linking
- دعم اللوحات السعودية / Saudi plates support

### 4. التصدير والاستيراد / Import/Export
- تصدير البيانات إلى CSV / Export data to CSV
- استيراد البيانات من CSV/Excel / Import from CSV/Excel
- دعم كامل للغة العربية / Full Arabic support

---

## إعداد النظام / System Setup

### 1. تكوين Plate Recognizer API

#### الخطوة 1: الحصول على API Key
1. قم بزيارة: https://app.platerecognizer.com/
2. سجل دخول أو أنشئ حساب جديد
3. انتقل إلى قسم API
4. انسخ API Token الخاص بك

#### الخطوة 2: تكوين متغيرات البيئة
قم بإنشاء ملف `.env` في مجلد المشروع:

```bash
# نسخ ملف المثال
cp .env.example .env

# تعديل الملف وإضافة API Key
nano .env
```

أضف السطر التالي:
```
PLATE_RECOGNIZER_API_TOKEN=your-api-token-here
```

**⚠️ مهم:** لا تشارك API token مع أحد ولا تضعه في Git!

### 2. تهيئة قاعدة البيانات

```bash
python3 database.py
```

هذا الأمر سينشئ جدول `vehicle_access_log` الجديد تلقائياً.

### 3. تشغيل الخادم

```bash
python3 server.py
```

---

## استخدام النظام / Using the System

### الوصول إلى الصفحة / Accessing the Page

بعد تسجيل الدخول، يمكن الوصول للنظام من:
1. الصفحة الرئيسية > قسم الأمن والسلامة > **تتبع السيارات الشامل**
2. صفحة الخدمات السريعة > **تتبع السيارات الشامل**
3. مباشرة: `http://your-server:5000/vehicle_tracking.html`

### 1. تسجيل دخول سيارة يدوياً / Manual Vehicle Entry

1. انقر على **"تسجيل دخول سيارة"**
2. املأ البيانات المطلوبة:
   - **رقم اللوحة*** (مطلوب)
   - **نوع المركبة*** (سيارة، دراجة نارية، شاحنة، إلخ)
   - **تصنيف السيارة*** (سكان، زائر، مندوب، إلخ)
   - **الغرض من الزيارة*** (مطلوب)
   - **معلومات إضافية** (اختياري): اسم، هاتف، شركة، موديل، لون، إلخ
3. انقر **"حفظ"**

### 2. تسجيل بالكاميرا والتعرف الآلي / Camera & Auto Recognition

1. انقر على **"تسجيل بالكاميرا"**
2. انقر **"تشغيل الكاميرا"**
3. وجه الكاميرا نحو لوحة السيارة
4. انقر **"التقاط الصورة"**
5. انقر **"التعرف على اللوحة"**
6. إذا نجح التعرف، انقر **"استخدام هذا الرقم"**
7. أكمل باقي البيانات واحفظ

### 3. تسجيل خروج سيارة / Vehicle Exit

1. ابحث عن السيارة في الجدول
2. انقر على أيقونة **الخروج** (✓)
3. سيتم تسجيل وقت الخروج تلقائياً

### 4. البحث والفلترة / Search & Filtering

استخدم شريط الفلاتر للبحث حسب:
- رقم اللوحة
- تصنيف السيارة
- الحالة (داخل/خارج الإسكان)
- نطاق تاريخي

### 5. تصدير البيانات / Exporting Data

1. انقر على **"تصدير البيانات"**
2. سيتم تنزيل ملف CSV يحتوي على جميع السجلات
3. يمكن فتحه في Excel أو Google Sheets

### 6. استيراد البيانات / Importing Data

1. جهز ملف CSV بنفس تنسيق ملف التصدير
2. انقر على **"استيراد البيانات"**
3. اختر الملف
4. سيتم استيراد السجلات تلقائياً

---

## هيكل قاعدة البيانات / Database Structure

### جدول vehicle_access_log

| Field | Type | Description |
|-------|------|-------------|
| id | INTEGER | المعرف الفريد / Unique ID |
| plate_number | TEXT | رقم اللوحة / Plate number |
| vehicle_type | TEXT | نوع المركبة / Vehicle type |
| vehicle_category | TEXT | التصنيف / Category |
| entry_time | TIMESTAMP | وقت الدخول / Entry time |
| exit_time | TIMESTAMP | وقت الخروج / Exit time |
| purpose | TEXT | الغرض / Purpose |
| visitor_name | TEXT | اسم الزائر / Visitor name |
| visitor_phone | TEXT | رقم الهاتف / Phone |
| visitor_id_number | TEXT | رقم الهوية / ID number |
| company_name | TEXT | اسم الشركة / Company |
| make | TEXT | الماركة / Make |
| model | TEXT | الموديل / Model |
| color | TEXT | اللون / Color |
| year | INTEGER | السنة / Year |
| gate_entry | TEXT | بوابة الدخول / Entry gate |
| gate_exit | TEXT | بوابة الخروج / Exit gate |
| security_officer_entry | INTEGER | ضابط الدخول / Entry officer |
| security_officer_exit | INTEGER | ضابط الخروج / Exit officer |
| status | TEXT | الحالة (inside/exited) |
| recognized_by_system | INTEGER | تعرف آلي (0/1) |
| confidence | REAL | نسبة الثقة / Confidence |
| image_path | TEXT | مسار الصورة / Image path |
| notes | TEXT | ملاحظات / Notes |

---

## API Endpoints

### 1. قائمة السيارات / List Vehicles
```
GET /api/vehicle-tracking/list
```
**Authentication:** Required  
**Response:** JSON array of vehicle records

### 2. الإحصائيات / Statistics
```
GET /api/vehicle-tracking/stats
```
**Authentication:** Required  
**Response:** 
```json
{
  "success": true,
  "stats": {
    "total": 150,
    "inside": 45,
    "today": 23,
    "recognized": 67
  }
}
```

### 3. إضافة سيارة / Add Vehicle
```
POST /api/vehicle-tracking/add
Content-Type: application/json
```
**Authentication:** Required  
**Body:**
```json
{
  "plate_number": "ABC123",
  "vehicle_type": "سيارة",
  "vehicle_category": "visitor",
  "purpose": "زيارة عائلية",
  "visitor_name": "أحمد محمد",
  "visitor_phone": "0501234567"
}
```

### 4. تسجيل خروج / Exit Vehicle
```
POST /api/vehicle-tracking/exit/{vehicle_id}
```
**Authentication:** Required

### 5. حذف سجل / Delete Record
```
DELETE /api/vehicle-tracking/delete/{vehicle_id}
```
**Authentication:** Required (Admin only)

### 6. تصدير / Export
```
GET /api/vehicle-tracking/export
```
**Authentication:** Required  
**Response:** CSV file

### 7. استيراد / Import
```
POST /api/vehicle-tracking/import
Content-Type: multipart/form-data
```
**Authentication:** Required (Admin only)  
**Body:** file (CSV)

---

## الأمان / Security

### الصلاحيات / Permissions

- **Admin**: الوصول الكامل / Full access
- **Security Officers**: إضافة وتعديل السجلات / Add and modify records
- **Viewers**: عرض فقط / View only

### حماية البيانات / Data Protection

1. **المصادقة مطلوبة**: جميع API endpoints محمية / All endpoints protected
2. **التحقق من المدخلات**: تنظيف وتحقق من جميع البيانات / Input validation
3. **Audit Log**: تسجيل جميع العمليات / All operations logged
4. **عدم كشف الأخطاء**: رسائل خطأ عامة للمستخدمين / Generic error messages

---

## استكشاف الأخطاء / Troubleshooting

### مشكلة: API Token لا يعمل
**الحل:**
1. تأكد من صحة Token من لوحة تحكم Plate Recognizer
2. تحقق من ملف `.env` وتأكد من عدم وجود مسافات زائدة
3. أعد تشغيل الخادم بعد تعديل `.env`

### مشكلة: الكاميرا لا تعمل
**الحل:**
1. تأكد من منح الموقع صلاحية الوصول للكاميرا
2. استخدم HTTPS في الإنتاج (required for camera access)
3. جرب متصفح آخر

### مشكلة: التعرف على اللوحة فاشل
**الحل:**
1. تأكد من وضوح الصورة وإضاءة جيدة
2. تأكد من ظهور اللوحة كاملة في الصورة
3. جرب التقاط صورة من زاوية مختلفة

---

## أفضل الممارسات / Best Practices

1. **تسجيل منتظم**: سجل جميع السيارات الداخلة دون استثناء
2. **تحديث الخروج**: لا تنسَ تسجيل خروج السيارات
3. **بيانات دقيقة**: احرص على دقة المعلومات المسجلة
4. **نسخ احتياطي**: قم بتصدير البيانات بشكل دوري
5. **مراجعة السجلات**: راجع السجلات بانتظام للتأكد من صحتها

---

## الدعم الفني / Technical Support

للحصول على الدعم الفني:
- البريد الإلكتروني: support@housing.edu.sa
- الهاتف: 920003282
- ساعات العمل: الأحد - الخميس، 8 صباحاً - 4 مساءً

---

## التحديثات المستقبلية / Future Updates

### مخطط لها / Planned
- [ ] تكامل مع نظام البوابات الآلية
- [ ] تطبيق موبايل للحراس
- [ ] تقارير متقدمة وإحصائيات
- [ ] إشعارات تلقائية
- [ ] تكامل مع نظام المخالفات

---

## الإصدار / Version

**النسخة:** 1.0.0  
**تاريخ الإصدار:** 2025-11-06  
**المطورون:** نظام إدارة إسكان أعضاء هيئة التدريس

---

## الترخيص / License

جميع الحقوق محفوظة © جامعة الإمام محمد بن سعود الإسلامية 2025  
All rights reserved © Imam Mohammad Ibn Saud Islamic University 2025
