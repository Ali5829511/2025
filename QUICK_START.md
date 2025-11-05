# 🚀 البدء السريع / Quick Start Guide

## خطوات التشغيل السريعة / Quick Setup Steps

### 1️⃣ تثبيت المتطلبات / Install Requirements
```bash
pip install -r requirements.txt
```

أو استخدم / Or use:
```bash
pip3 install Flask==2.3.3 Flask-CORS==4.0.0 Werkzeug==3.0.1
```

### 2️⃣ إنشاء قاعدة البيانات / Initialize Database
```bash
python3 database.py
```

سيتم إنشاء ملف `housing.db` تلقائياً مع 5 مستخدمين افتراضيين.

### 3️⃣ تشغيل الخادم / Start Server
```bash
python3 server.py
```

أو استخدم السكريبت السريع / Or use quick script:
```bash
./run.sh          # Linux/Mac
run.bat           # Windows
```

### 4️⃣ فتح المتصفح / Open Browser
```
http://localhost:5000
```

---

## 🔐 بيانات الدخول الافتراضية / Default Credentials

| المستخدم / User | اسم المستخدم / Username | كلمة المرور / Password |
|-----------------|------------------------|---------------------|
| مدير النظام | admin | Admin@2025 |
| مسؤول المخالفات | violations_officer | Violations@2025 |
| مسؤول الزوار | visitors_officer | Visitors@2025 |
| مستخدم عرض فقط | viewer | Viewer@2025 |
| مسجل المخالفات | violation_entry | Violation@2025 |

---

## 📊 صفحة التقرير الشامل / Validation Report

للوصول إلى تقرير التحقق الشامل / To access the validation report:

**الطريقة 1 / Method 1:** عبر لوحة التحكم
1. افتح / Open: `http://localhost:5000/main_dashboard.html`
2. انتقل إلى قسم / Go to: "الإدارة والتقارير"
3. انقر على / Click: "تقرير التحقق الشامل"

**الطريقة 2 / Method 2:** الرابط المباشر
```
http://localhost:5000/system_validation_report.html
```

---

## ⚠️ حل المشاكل الشائعة / Troubleshooting

### خطأ 500 / Error 500

**المشكلة / Problem:** لم يتم تثبيت المتطلبات
**الحل / Solution:**
```bash
pip3 install -r requirements.txt
```

### خطأ في قاعدة البيانات / Database Error

**المشكلة / Problem:** قاعدة البيانات غير موجودة
**الحل / Solution:**
```bash
python3 database.py
```

### المنفذ 5000 مستخدم / Port 5000 Busy

**الحل / Solution:** استخدم منفذ آخر
```bash
PORT=8080 python3 server.py
```

---

## ✅ التحقق من التثبيت / Verify Installation

```bash
# تحقق من Python
python3 --version

# تحقق من المتطلبات
pip3 list | grep -E "Flask|Werkzeug"

# تحقق من قاعدة البيانات
ls -lh housing.db

# تحقق من الخادم
curl http://localhost:5000/api/health
```

---

## 📝 ملاحظات / Notes

- **التطوير / Development:** استخدم `server.py` (مع قاعدة بيانات)
- **الإنتاج / Production:** راجع `DEPLOYMENT.md` للإعدادات الكاملة
- **الأمان / Security:** غيّر كلمات المرور الافتراضية فوراً

---

**للمزيد من التفاصيل / For more details:**
- [README.md](README.md) - الدليل الشامل
- [SYSTEM_VALIDATION_REPORT.md](SYSTEM_VALIDATION_REPORT.md) - وثائق التقرير
- [تقرير_المراجعة_الشاملة.md](تقرير_المراجعة_الشاملة.md) - دليل عربي

---

جامعة الإمام محمد بن سعود الإسلامية © 2025
