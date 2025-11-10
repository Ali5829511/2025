# دليل تكامل ParkPow API
# ParkPow API Integration Guide

## نظرة عامة | Overview

نظام ParkPow هو نظام متكامل لتمييز لوحات السيارات وتسجيل المخالفات المرورية. يستخدم النظام تقنية الذكاء الاصطناعي للتعرف التلقائي على اللوحات وربطها بقاعدة بيانات السيارات والسكان.

ParkPow system is an integrated system for vehicle plate recognition and traffic violation recording. The system uses AI technology for automatic plate recognition and links it to the vehicle and resident database.

---

## الميزات الرئيسية | Main Features

### 1. تمييز اللوحات | Plate Recognition
- رفع صورة سيارة والحصول على رقم اللوحة تلقائياً
- دقة عالية في التعرف على الأرقام العربية والإنجليزية
- ربط تلقائي مع قاعدة بيانات السيارات المسجلة
- عرض معلومات المالك والوحدة السكنية

### 2. تسجيل المخالفات | Violation Recording
- تسجيل سريع للمخالفات المرورية
- أنواع متعددة من المخالفات
- حساب الغرامات
- ربط تلقائي مع بيانات السيارة والمالك

### 3. المخالفين المتكررين | Repeat Offenders
- تتبع السيارات التي لديها مخالفات متعددة
- فلترة حسب عدد المخالفات
- عرض معلومات المالك والاتصال
- تقارير تفصيلية للمخالفات

### 4. Webhook Integration
- استقبال إشعارات تلقائية من ParkPow
- معالجة فورية للكشوفات الجديدة
- حفظ تلقائي في قاعدة البيانات

---

## الإعداد الأولي | Initial Setup

### 1. الحصول على API Token

قم بزيارة:
```
https://app.parkpow.com/accounts/token/
```

سجل الدخول واحصل على Token الخاص بك.

### 2. إعداد متغيرات البيئة | Environment Variables

أضف المتغيرات التالية إلى ملف `.env`:

```bash
# ParkPow API Configuration
PARKPOW_API_TOKEN=your-token-here
PARKPOW_API_URL=https://app.parkpow.com/api/v1
PARKPOW_WEBHOOK_TOKEN=your-webhook-token-here
```

**مثال:**
```bash
PARKPOW_API_TOKEN=7c13be422713a758a42a0bc453cf3331fbf4d346
PARKPOW_API_URL=https://app.parkpow.com/api/v1
PARKPOW_WEBHOOK_TOKEN=webhook_secret_token_123
```

### 3. تهيئة قاعدة البيانات | Database Setup

سيتم إنشاء جدول `parkpow_detections` تلقائياً عند تشغيل النظام:

```sql
CREATE TABLE parkpow_detections (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    plate_number TEXT NOT NULL,
    vehicle_id INTEGER,
    detection_time TIMESTAMP,
    camera_id TEXT,
    confidence REAL,
    raw_data TEXT,
    processed BOOLEAN DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

---

## استخدام النظام | System Usage

### 1. الدخول إلى النظام

1. افتح البوابة الرئيسية: `welcome_portal.html`
2. اضغط على بطاقة "نظام ParkPow"
3. سيتم فتح صفحة `parkpow_integration.html`

### 2. التحقق من حالة الخدمة

عند فتح الصفحة، سيتم التحقق تلقائياً من:
- ✅ الاتصال بـ ParkPow API
- ✅ صلاحية Token
- ✅ حالة الخدمة

### 3. تمييز لوحة سيارة

**خطوات التمييز:**

1. اضغط على "رفع صورة السيارة"
2. اختر صورة من جهازك
3. (اختياري) أدخل معرف الكاميرا
4. اضغط على "تمييز اللوحة"

**النتيجة:**
- رقم اللوحة المكتشف
- نسبة الثقة (%)
- معلومات السيارة (إذا كانت مسجلة)
- اسم المالك ورقم الوحدة

**ملاحظة:** سيتم ملء رقم اللوحة تلقائياً في نموذج المخالفات.

### 4. تسجيل مخالفة

**الحقول المطلوبة:**
- ✅ رقم اللوحة (مطلوب)
- ✅ نوع المخالفة (مطلوب)
- الموقع (اختياري)
- الوصف (اختياري)
- قيمة الغرامة (افتراضي: 0)

**أنواع المخالفات:**
- وقوف ممنوع
- تجاوز السرعة
- عكس السير
- مواقف ذوي الاحتياجات
- عدم التقيد بالإشارات
- أخرى

**بعد التسجيل:**
- رقم المخالفة
- تأكيد حفظ المخالفة
- تحديث قائمة المخالفين المتكررين

### 5. عرض المخالفين المتكررين

**الفلترة:**
- حدد الحد الأدنى للمخالفات (افتراضي: 3)
- اضغط على "تحديث القائمة"

**المعلومات المعروضة:**
- رقم اللوحة
- عدد المخالفات
- اسم المالك
- رقم الوحدة
- تاريخ آخر مخالفة

---

## API Endpoints

### 1. التحقق من الحالة | Status Check

```http
GET /api/parkpow/status
Authorization: Required (Session Token)
```

**Response:**
```json
{
  "success": true,
  "configured": true,
  "message": "ParkPow API is active and working",
  "message_ar": "خدمة ParkPow نشطة وتعمل بشكل صحيح",
  "api_url": "https://app.parkpow.com/api/v1",
  "webhook_url": "https://app.parkpow.com/api/v1/webhook-receiver/"
}
```

### 2. تمييز لوحة | Plate Recognition

```http
POST /api/parkpow/recognize
Authorization: Required (Session Token)
Content-Type: application/json
```

**Request Body:**
```json
{
  "image": "data:image/jpeg;base64,/9j/4AAQSkZJRg...",
  "camera_id": "camera-01"
}
```

**Response:**
```json
{
  "success": true,
  "results": [
    {
      "plate": "ABC123",
      "confidence": 0.95,
      "vehicle_info": {
        "id": 1,
        "owner_name": "محمد أحمد",
        "unit_number": "101",
        "building_name": "مبنى أ"
      }
    }
  ],
  "message_ar": "تم تمييز اللوحة بنجاح"
}
```

### 3. تسجيل مخالفة | Record Violation

```http
POST /api/parkpow/record-violation
Authorization: Required (Session Token)
Content-Type: application/json
```

**Request Body:**
```json
{
  "plate_number": "ABC123",
  "violation_type": "وقوف ممنوع",
  "location": "موقف المبنى أ",
  "description": "الوقوف في مكان محظور",
  "fine_amount": 200
}
```

**Response:**
```json
{
  "success": true,
  "violation_id": 42,
  "vehicle_found": true,
  "message_ar": "تم تسجيل المخالفة بنجاح"
}
```

### 4. المخالفين المتكررين | Repeat Offenders

```http
GET /api/parkpow/repeat-offenders?min_violations=3
Authorization: Required (Session Token)
```

**Response:**
```json
{
  "success": true,
  "offenders": [
    {
      "plate_number": "ABC123",
      "violation_count": 5,
      "owner_name": "محمد أحمد",
      "unit_number": "101",
      "latest_violation": "2025-11-09T10:30:00"
    }
  ],
  "count": 1,
  "min_violations": 3
}
```

### 5. Webhook

```http
POST /api/parkpow/webhook
Authorization: Token {PARKPOW_WEBHOOK_TOKEN}
Content-Type: application/json
```

**Request Body:**
```json
{
  "plate_number": "ABC123",
  "camera_id": "camera-01",
  "confidence": 0.95,
  "timestamp": "2025-11-09T10:30:00Z"
}
```

**Response:**
```json
{
  "success": true,
  "plate_number": "ABC123",
  "vehicle_found": true,
  "message_ar": "تمت معالجة البيانات بنجاح"
}
```

---

## الأمان | Security

### 1. المصادقة | Authentication

جميع endpoints (ما عدا webhook) تتطلب:
- Session token صالح
- المستخدم يجب أن يكون مسجل دخول

### 2. الصلاحيات | Permissions

**القراءة فقط (Viewer):**
- ✅ عرض حالة الخدمة
- ✅ عرض المخالفين المتكررين
- ❌ تمييز اللوحات
- ❌ تسجيل المخالفات

**المستخدمون العاديون:**
- ✅ جميع الوظائف

**المدير (Admin):**
- ✅ جميع الوظائف
- ✅ إعدادات النظام

### 3. سجل التدقيق | Audit Log

يتم تسجيل جميع العمليات:
- تمييز اللوحات
- تسجيل المخالفات
- الوصول إلى البيانات
- استقبال Webhook

---

## استكشاف الأخطاء | Troubleshooting

### المشكلة: "خدمة ParkPow غير مفعلة"

**الحل:**
1. تحقق من ملف `.env`
2. تأكد من وجود `PARKPOW_API_TOKEN`
3. تأكد من صحة Token
4. أعد تشغيل الخادم

### المشكلة: خطأ في تمييز اللوحة

**الحل:**
1. تحقق من جودة الصورة
2. تأكد من وضوح اللوحة
3. تحقق من حجم الصورة (أقل من 10MB)
4. جرب صورة أخرى

### المشكلة: لا تظهر معلومات السيارة

**الحل:**
1. تحقق من أن السيارة مسجلة في النظام
2. تحقق من تطابق رقم اللوحة
3. تأكد من أن السيارة نشطة (`is_active = 1`)

### المشكلة: Webhook لا يعمل

**الحل:**
1. تحقق من `PARKPOW_WEBHOOK_TOKEN` في `.env`
2. تأكد من إعداد URL في ParkPow dashboard
3. تحقق من firewall/network settings
4. راجع سجلات الخادم (logs)

---

## الأهداف المحققة | Goals Achieved

✅ **الهدف الأول:** ربط قاعدة بيانات السيارات داخل إسكان هيئة التدريس
- تم ربط ParkPow مع جدول السيارات (`vehicles`)
- عرض معلومات المالك والوحدة تلقائياً
- تتبع جميع السيارات المسجلة

✅ **الهدف الثاني:** تسجيل مخالفات مرورية ومعرفة تكرار المخالفين
- نظام متكامل لتسجيل المخالفات
- تصنيف حسب نوع المخالفة
- قائمة ديناميكية للمخالفين المتكررين
- إحصائيات وتقارير

---

## الدعم الفني | Technical Support

لأي استفسارات أو مشاكل:
1. راجع هذا الدليل
2. تحقق من سجلات النظام (logs)
3. تواصل مع فريق الدعم الفني

---

## التحديثات المستقبلية | Future Updates

- [ ] إضافة تقارير Excel للمخالفات
- [ ] إرسال إشعارات للمخالفين
- [ ] لوحة تحكم للإحصائيات
- [ ] تكامل مع أنظمة دفع إلكتروني
- [ ] تطبيق موبايل

---

**تاريخ الإنشاء:** 2025-11-09  
**الإصدار:** 1.0.0  
**الحالة:** ✅ جاهز للاستخدام
