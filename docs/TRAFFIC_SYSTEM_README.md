# 📊 نظام إدارة المخالفات المرورية - Traffic Violations Management System

نظام متكامل لإدارة المخالفات المرورية مع تكامل API لتمييز لوحات السيارات تلقائياً.

A comprehensive traffic violations management system with automatic license plate recognition via Plate Recognizer API integration.

## ✨ المميزات - Features

### الوظائف الأساسية - Core Features
- ✅ قاعدة بيانات SQLite لتخزين بيانات السيارات والمخالفات
- ✅ واجهة ويب احترافية لعرض المخالفات مع الصور المصغرة
- ✅ إضافة مخالفات جديدة مع رفع الصور
- ✅ بحث وتصفية متقدم في المخالفات
- ✅ إحصائيات فورية (إجمالي المخالفات، السيارات، الغرامات)

### تكامل Plate Recognizer API
- 🚗 تمييز تلقائي لأرقام اللوحات من الصور
- 🎯 دقة عالية في التعرف على اللوحات السعودية
- ⚡ معالجة سريعة للصور
- 📊 عرض نسبة الثقة في التمييز

## 🚀 التثبيت والتشغيل - Installation & Setup

### المتطلبات - Requirements

```bash
Python 3.8+
Flask
SQLite3
```

### خطوات التثبيت - Installation Steps

1. **استنساخ المشروع - Clone the repository**
```bash
git clone https://github.com/Ali5829511/2025.git
cd 2025
```

2. **تثبيت المكتبات المطلوبة - Install dependencies**
```bash
pip install -r requirements.txt
```

3. **إعداد متغيرات البيئة - Setup environment variables**

أنشئ ملف `.env` في المجلد الرئيسي:
```env
# Plate Recognizer API Token
PLATE_RECOGNIZER_API_TOKEN=your_api_token_here

# Flask Configuration
FLASK_DEBUG=False
PORT=5001
```

للحصول على API Token من Plate Recognizer:
1. زر https://app.platerecognizer.com/
2. سجل حساب جديد أو سجل دخول
3. انتقل إلى صفحة "API Keys"
4. انسخ المفتاح وضعه في `.env`

4. **تهيئة قاعدة البيانات - Initialize database**
```bash
python init_traffic_db.py
```

5. **تشغيل التطبيق - Run the application**
```bash
python traffic_app.py
```

6. **افتح المتصفح - Open your browser**
```
http://localhost:5001
```

## 📁 هيكل المشروع - Project Structure

```
2025/
├── traffic_app.py              # التطبيق الرئيسي - Main Flask app
├── init_traffic_db.py          # تهيئة قاعدة البيانات - Database initialization
├── traffic.db                  # قاعدة البيانات - SQLite database
├── templates/
│   ├── traffic_violations_index.html  # الصفحة الرئيسية - Main page
│   └── add_violation.html            # صفحة إضافة مخالفة - Add violation page
├── static/
│   ├── images/                 # صور العينات - Sample images
│   └── uploads/
│       └── violations/         # صور المخالفات المرفوعة - Uploaded violation images
├── requirements.txt            # المكتبات المطلوبة - Python dependencies
└── .env                        # متغيرات البيئة - Environment variables
```

## 🗄️ قاعدة البيانات - Database Schema

### جدول السيارات - Cars Table
```sql
CREATE TABLE cars (
    car_id INTEGER PRIMARY KEY AUTOINCREMENT,
    plate_number TEXT UNIQUE NOT NULL,
    owner_name TEXT,
    model TEXT,
    year INTEGER,
    color TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### جدول المخالفات - Violations Table
```sql
CREATE TABLE violations (
    violation_id INTEGER PRIMARY KEY AUTOINCREMENT,
    car_id INTEGER NOT NULL,
    violation_type TEXT NOT NULL,
    violation_date TEXT NOT NULL,
    fine_amount REAL NOT NULL,
    officer_name TEXT,
    image_path TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (car_id) REFERENCES cars(car_id)
);
```

## 🔌 واجهة برمجة التطبيقات - API Endpoints

### الحصول على جميع المخالفات - Get all violations
```
GET /api/violations
```

### الحصول على جميع السيارات - Get all cars
```
GET /api/cars
```

### رفع صورة مخالفة - Upload violation image
```
POST /api/upload-violation
Content-Type: multipart/form-data

Body:
- image: file
```

### إضافة مخالفة جديدة - Add new violation
```
POST /api/add-violation
Content-Type: application/json

Body:
{
    "plate_number": "ABC-1234",
    "owner_name": "أحمد محمد",
    "model": "تويوتا كامري",
    "year": 2020,
    "color": "أبيض",
    "violation_type": "تجاوز السرعة",
    "violation_date": "2024-01-15",
    "fine_amount": 500.0,
    "officer_name": "محمد أحمد",
    "image_path": "/static/uploads/violations/image.jpg"
}
```

### حالة Plate Recognizer API - API Status
```
GET /api/plate-recognizer/status
```

## 🔐 الأمان - Security

- ✅ التحقق من صحة الملفات المرفوعة
- ✅ استخدام secure_filename لأسماء الملفات
- ✅ التحقق من أنواع الملفات المسموحة
- ✅ حماية CORS
- ✅ معالجة الأخطاء بشكل آمن

## 🌐 النشر - Deployment

### النشر على Render.com

1. **أنشئ حساب على Render.com**
   - زر https://render.com
   - سجل باستخدام GitHub

2. **أنشئ Web Service جديد**
   - اختر "New +" → "Web Service"
   - اربط مستودع GitHub
   - اختر فرع النشر

3. **إعدادات النشر:**
   ```
   Name: traffic-violations-system
   Environment: Python 3
   Build Command: pip install -r requirements.txt
   Start Command: python traffic_app.py
   ```

4. **أضف متغيرات البيئة:**
   ```
   PLATE_RECOGNIZER_API_TOKEN=your_token
   FLASK_DEBUG=False
   PORT=5001
   ```

5. **انشر التطبيق** - Deploy

### النشر على Heroku

1. **تسجيل الدخول إلى Heroku**
```bash
heroku login
```

2. **إنشاء تطبيق جديد**
```bash
heroku create traffic-violations-app
```

3. **إضافة متغيرات البيئة**
```bash
heroku config:set PLATE_RECOGNIZER_API_TOKEN=your_token
```

4. **النشر**
```bash
git push heroku main
```

### النشر على Railway

1. **زر Railway.app**
   - https://railway.app

2. **أنشئ مشروع جديد من GitHub**
   - اربط المستودع
   - اختر الفرع

3. **أضف متغيرات البيئة**
   - في إعدادات المشروع
   - أضف PLATE_RECOGNIZER_API_TOKEN

4. **النشر التلقائي**
   - سيتم النشر تلقائياً عند كل push

## 📝 ملاحظات - Notes

### تكامل Plate Recognizer
- الخدمة تقدم نسخة تجريبية مجانية بـ 2500 استعلام شهرياً
- يدعم التعرف على اللوحات السعودية والخليجية
- نسبة دقة عالية جداً (>95%)
- API سريع جداً (معالجة في أقل من ثانية)

### البيانات التجريبية
- يتضمن النظام بيانات تجريبية للاختبار
- 3 سيارات و 4 مخالفات كعينات
- يمكنك حذفها بعد التجربة

### التطوير المستقبلي
- [ ] إضافة نظام مستخدمين والصلاحيات
- [ ] تصدير التقارير إلى Excel/PDF
- [ ] لوحة تحكم إحصائية متقدمة
- [ ] إشعارات البريد الإلكتروني
- [ ] تطبيق موبايل

## 🤝 المساهمة - Contributing

نرحب بمساهماتكم! يرجى:
1. Fork المستودع
2. إنشاء فرع للميزة الجديدة
3. Commit التغييرات
4. Push إلى الفرع
5. فتح Pull Request

## 📞 الدعم - Support

للمساعدة والدعم:
- GitHub Issues: https://github.com/Ali5829511/2025/issues
- Plate Recognizer Docs: https://docs.platerecognizer.com/

## 📄 الترخيص - License

MIT License - يمكنك استخدام وتعديل المشروع بحرية.

## 👨‍💻 المطور - Developer

Ali5829511

---

**صُمم وطُور في المملكة العربية السعودية 🇸🇦**

**Designed and Developed in Saudi Arabia 🇸🇦**
