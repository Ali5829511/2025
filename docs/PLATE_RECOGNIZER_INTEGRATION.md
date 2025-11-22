# دليل تكامل Plate Recognizer Snapshot Cloud
# Plate Recognizer Snapshot Cloud Integration Guide

## نظرة عامة | Overview

تم تكامل نظام تمييز اللوحات مع خدمة Plate Recognizer Snapshot Cloud، وهي خدمة متقدمة لتمييز لوحات السيارات باستخدام الذكاء الاصطناعي.

The license plate recognition system has been integrated with Plate Recognizer Snapshot Cloud, an advanced AI-powered license plate recognition service.

## الإعداد | Setup

### 1. الحصول على مفتاح API | Obtaining API Key

1. قم بزيارة: https://app.platerecognizer.com/
2. قم بإنشاء حساب أو تسجيل الدخول
3. انتقل إلى قسم API Tokens
4. قم بإنشاء مفتاح API جديد
5. احفظ المفتاح بشكل آمن

Steps:
1. Visit: https://app.platerecognizer.com/
2. Create an account or log in
3. Navigate to API Tokens section
4. Create a new API token
5. Save the token securely

### 2. تكوين المتغيرات البيئية | Environment Variables Configuration

قم بإضافة المتغيرات التالية إلى ملف `.env`:

Add the following variables to your `.env` file:

```bash
# Plate Recognizer API Configuration
PLATE_RECOGNIZER_API_TOKEN=your_api_token_here
PLATE_RECOGNIZER_API_URL=https://api.platerecognizer.com/v1/plate-reader/
PLATE_RECOGNIZER_REGIONS=sa  # For Saudi Arabia (can be multiple: sa,ae,kw)
```

### 3. المناطق المدعومة | Supported Regions

يمكنك تحديد المناطق لتحسين دقة التمييز:

You can specify regions to improve recognition accuracy:

- `sa` - Saudi Arabia (المملكة العربية السعودية)
- `ae` - United Arab Emirates (الإمارات العربية المتحدة)
- `kw` - Kuwait (الكويت)
- `qa` - Qatar (قطر)
- `bh` - Bahrain (البحرين)
- `om` - Oman (عمان)

يمكن تحديد عدة مناطق مفصولة بفاصلة: `sa,ae,kw`

Multiple regions can be specified separated by comma: `sa,ae,kw`

## الاستخدام | Usage

### من واجهة الويب | From Web Interface

1. افتح الصفحة: `/pages/parkpow_integration.html`
2. تحقق من حالة الاتصال بالخدمة
3. قم برفع صورة السيارة
4. سيتم تمييز اللوحة تلقائياً
5. يمكنك تسجيل مخالفة للوحة المميزة

Steps:
1. Open page: `/pages/parkpow_integration.html`
2. Check service connection status
3. Upload vehicle image
4. Plate will be recognized automatically
5. You can record a violation for the recognized plate

### من API | From API

#### التحقق من حالة الخدمة | Check Service Status
```bash
GET /api/parkpow/status
```

#### تمييز اللوحة | Recognize Plate
```bash
POST /api/parkpow/recognize
Content-Type: application/json

{
  "image": "base64_encoded_image_data",
  "camera_id": "camera-01"  // optional
}
```

#### تسجيل مخالفة | Record Violation
```bash
POST /api/parkpow/record-violation
Content-Type: application/json

{
  "plate_number": "ABC123",
  "violation_type": "وقوف ممنوع",
  "location": "موقف الزوار",
  "description": "وقوف في مكان محظور",
  "payment_status": 0
}
```

#### الحصول على المخالفين المتكررين | Get Repeat Offenders
```bash
GET /api/parkpow/repeat-offenders?min_violations=3
```

## المميزات | Features

### ✅ التمييز التلقائي للوحات | Automatic Plate Recognition
- دقة عالية في تمييز اللوحات العربية والإنجليزية
- High accuracy for Arabic and English plates

### ✅ دعم المناطق المختلفة | Multi-Region Support
- دعم لوحات دول مجلس التعاون الخليجي
- Support for GCC countries' plates

### ✅ تسجيل المخالفات | Violation Recording
- تسجيل تلقائي للمخالفات المرورية
- Automatic traffic violation recording

### ✅ تتبع المخالفين المتكررين | Repeat Offenders Tracking
- تحديد المركبات ذات المخالفات المتكررة
- Identify vehicles with repeated violations

### ✅ التكامل مع قاعدة البيانات | Database Integration
- ربط تلقائي مع بيانات المركبات المسجلة
- Automatic linking with registered vehicle data

## الحدود والأسعار | Limits and Pricing

خدمة Plate Recognizer تقدم خطط مختلفة:

Plate Recognizer offers different plans:

- **Free Plan**: 2,500 API calls/month
- **Paid Plans**: بدءاً من $39.99/month

للمزيد من التفاصيل: https://platerecognizer.com/pricing/

For more details: https://platerecognizer.com/pricing/

## استكشاف الأخطاء | Troubleshooting

### الخطأ: "خدمة Plate Recognizer غير مفعلة"
**الحل:**
- تأكد من إضافة `PLATE_RECOGNIZER_API_TOKEN` في ملف `.env`
- تحقق من صحة المفتاح

### الخطأ: "رصيد غير كافٍ"
**الحل:**
- تحقق من رصيد API calls في حسابك
- قم بالترقية إلى خطة مدفوعة إذا لزم الأمر

### الخطأ: "رمز API غير صالح"
**الحل:**
- تحقق من المفتاح المستخدم
- قم بإنشاء مفتاح جديد إذا انتهت صلاحيته

## الدعم الفني | Technical Support

### وثائق API الرسمية | Official API Documentation
https://app.platerecognizer.com/service/snapshot-cloud/

### وثائق Plate Recognizer | Plate Recognizer Documentation
https://docs.platerecognizer.com/

### دعم المشروع | Project Support
للمساعدة، قم بفتح issue في مستودع GitHub

For assistance, open an issue in the GitHub repository

## الأمان | Security

⚠️ **مهم | Important:**
- لا تشارك مفتاح API الخاص بك
- Never share your API key
- احفظ المفتاح في متغيرات البيئة فقط
- Store the key in environment variables only
- لا تقم برفع المفتاح إلى Git
- Do not commit the key to Git

## التحديثات | Updates

### الإصدار 1.0 | Version 1.0
- تكامل أولي مع Plate Recognizer Snapshot Cloud
- Initial integration with Plate Recognizer Snapshot Cloud
- دعم تمييز اللوحات العربية
- Support for Arabic plate recognition
- تسجيل المخالفات المرورية
- Traffic violation recording
- تتبع المخالفين المتكررين
- Repeat offenders tracking
