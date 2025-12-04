# دليل النشر على Render.com
# Render.com Deployment Guide

**الإصدار / Version:** 2.2.0  
**التاريخ / Date:** 4 ديسمبر 2025 / December 4, 2025  
**الحالة / Status:** ✅ جاهز للنشر / READY FOR DEPLOYMENT

---

## 🚀 النشر بـ 3 خطوات سهلة / Deploy in 3 Easy Steps

### ✅ الخطوة 1: اذهب إلى Render.com
```
https://render.com
```

### ✅ الخطوة 2: سجل الدخول/الإنشاء
```
اختر "Sign up with GitHub"
وافق على الأذونات
```

### ✅ الخطوة 3: أنشئ خدمة ويب جديدة
```
1. اضغط على "New +"
2. اختر "Web Service"
3. اختر "Deploy from a Git repository"
4. ابحث عن: Ali5829511/2025
5. اضغط "Connect"
```

---

## ⚙️ إعدادات النشر / Deployment Settings

### الإعدادات الأساسية:
```
Name:                    housing-management-system
Environment:             Python 3
Region:                  Oregon (أو أقرب منطقة)
Branch:                  main
Root Directory:          (اتركه فارغاً)
```

### أوامر البناء والتشغيل:
```
Build Command:
pip install -r requirements.txt

Start Command:
gunicorn --config gunicorn_config.py server:app
```

### متغيرات البيئة:
```
FLASK_ENV=production
FLASK_DEBUG=false
SECRET_KEY=your-secret-key-here
DATABASE_URL=sqlite:///housing_system.db
PYTHON_VERSION=3.11.0
```

---

## 🔧 الخطوات التفصيلية / Detailed Steps

### 1️⃣ إنشاء حساب Render

**الخطوات:**
```
1. اذهب إلى https://render.com
2. انقر على "Sign Up"
3. اختر "Sign up with GitHub"
4. وافق على الأذونات
5. أكمل إعداد الحساب
```

### 2️⃣ إنشاء خدمة ويب جديدة

**الخطوات:**
```
1. في لوحة التحكم، انقر على "New +"
2. اختر "Web Service"
3. اختر "Deploy from a Git repository"
```

### 3️⃣ ربط المستودع

**الخطوات:**
```
1. ابحث عن: Ali5829511/2025
2. انقر على "Connect"
3. اختر الفرع: main
```

### 4️⃣ تكوين الخدمة

**الخطوات:**
```
1. Name: housing-management-system
2. Environment: Python 3
3. Region: Oregon
4. Build Command: pip install -r requirements.txt
5. Start Command: gunicorn --config gunicorn_config.py server:app
```

### 5️⃣ إضافة متغيرات البيئة

**الخطوات:**
```
1. اضغط على "Advanced"
2. اضغط على "Add Environment Variable"
3. أضف:
   - FLASK_ENV = production
   - FLASK_DEBUG = false
   - SECRET_KEY = (قيمة عشوائية قوية)
```

### 6️⃣ ابدأ النشر

**الخطوات:**
```
1. اضغط على "Create Web Service"
2. انتظر 5-10 دقائق
3. سيظهر الرابط الخاص بك
```

---

## 📊 مراقبة النشر / Monitor Deployment

### عرض السجلات:
```
1. اذهب إلى لوحة التحكم
2. اختر الخدمة
3. انقر على "Logs"
4. شاهد السجلات الحية
```

### التحقق من الحالة:
```
✅ تم النشر بنجاح
⏳ جاري النشر
❌ فشل النشر
```

---

## 🌐 الوصول إلى الموقع / Access Your Site

### الرابط:
```
https://housing-management-system.onrender.com
```

### بيانات الدخول:
```
Username: admin
Password: Admin@2025
```

---

## 🔄 النشر التلقائي / Automatic Deployment

### كيف يعمل:
```
1. عند دفع تحديثات إلى GitHub
2. Render سينشر تلقائياً
3. الموقع سيتحدث بدون توقف
```

### تعطيل النشر التلقائي:
```
1. اذهب إلى الإعدادات
2. اختر "Auto-Deploy"
3. اختر "Off"
```

---

## 🐛 استكشاف الأخطاء / Troubleshooting

### المشكلة: خطأ 500
```
✅ الحل:
1. تحقق من السجلات
2. تأكد من متغيرات البيئة
3. تحقق من قاعدة البيانات
```

### المشكلة: الموقع بطيء
```
✅ الحل:
1. ترقية إلى خطة مدفوعة
2. تحسين الكود
3. تقليل حجم الملفات
```

### المشكلة: قاعدة البيانات لا تعمل
```
✅ الحل:
1. استخدم SQLite (الافتراضي)
2. أو أضف PostgreSQL
3. تحقق من الاتصال
```

---

## 💾 النسخ الاحتياطية / Backups

### إنشاء نسخة احتياطية:
```
1. قم بتحميل قاعدة البيانات
2. احفظها في مكان آمن
3. كرر كل أسبوع
```

### استعادة النسخة الاحتياطية:
```
1. قم برفع الملف
2. أعد تشغيل الخدمة
3. تحقق من البيانات
```

---

## 🔐 الأمان / Security

### تحديث كلمات المرور:
```
1. سجل الدخول بـ admin
2. اذهب إلى الإعدادات
3. غيّر كلمات المرور
```

### تفعيل HTTPS:
```
✅ Render يفعل HTTPS تلقائياً
✅ الشهادة مجانية
✅ التحديث تلقائي
```

### حماية البيانات:
```
✅ استخدم متغيرات البيئة
✅ لا تضع كلمات المرور في الكود
✅ استخدم HTTPS دائماً
```

---

## 📈 الخطة المجانية / Free Plan

### المميزات:
```
✅ مجاني تماماً
✅ 750 ساعة/شهر
✅ HTTPS مجاني
✅ نشر تلقائي
✅ قاعدة بيانات مجانية
```

### القيود:
```
⏰ قد تنام بعد 15 دقيقة عدم استخدام
📊 محدود بـ 750 ساعة/شهر
💾 مساحة محدودة
```

### الترقية:
```
💰 من $7/شهر
✅ بدون نوم
✅ أداء أفضل
✅ مساحة أكبر
```

---

## 📞 الدعم / Support

### روابط مفيدة:
- 🔗 [Render.com](https://render.com)
- 📖 [التوثيق](https://render.com/docs)
- 💬 [المجتمع](https://render.com/community)

### للمساعدة:
- 📧 support@render.com
- 💬 Discord Community
- 📚 Documentation

---

## ✅ قائمة التحقق / Checklist

قبل النشر:
```
☑️ تحديث الكود
☑️ اختبار محلي
☑️ دفع إلى GitHub
☑️ إعدادات Render
☑️ متغيرات البيئة
☑️ قاعدة البيانات
```

بعد النشر:
```
☑️ اختبار الموقع
☑️ تسجيل الدخول
☑️ اختبار الميزات
☑️ مراقبة السجلات
☑️ تحديث كلمات المرور
☑️ إنشاء نسخة احتياطية
```

---

## 🎉 تم النشر!

```
رابط موقعك:
https://housing-management-system.onrender.com

استمتع! 🚀
```

---

## 📝 ملاحظات مهمة

### 1. الخطة المجانية
```
✅ مجانية تماماً
⏰ قد تنام بعد 15 دقيقة
📊 محدودة بـ 750 ساعة/شهر
```

### 2. النشر التلقائي
```
✅ يحدث تلقائياً عند التحديث
✅ لا تحتاج إلى فعل شيء
✅ سريع جداً
```

### 3. قاعدة البيانات
```
✅ SQLite مدمج
✅ آمن وموثوق
✅ لا تحتاج إلى إعداد
```

### 4. الأداء
```
✅ سريع جداً
✅ HTTPS مجاني
✅ CDN عالمي
```

---

**آخر تحديث / Last Updated:** 4 ديسمبر 2025 / December 4, 2025  
**الإصدار / Version:** 2.2.0  
**الحالة / Status:** ✅ جاهز للنشر / READY FOR DEPLOYMENT
