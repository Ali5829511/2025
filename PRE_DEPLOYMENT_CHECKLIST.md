# ✅ قائمة التحقق قبل النشر
# Pre-Deployment Checklist

**الإصدار / Version:** 2.0.1  
**التاريخ / Date:** ديسمبر 2025 / December 2025  
**الحالة / Status:** 🚀 جاهز للنشر / Ready for Deployment

---

## 📋 نظرة عامة / Overview

استخدم هذه القائمة للتحقق من جاهزية النظام قبل النشر في بيئة الإنتاج. تأكد من إكمال جميع العناصر قبل البدء.

Use this checklist to verify system readiness before deploying to production. Ensure all items are completed before starting.

---

## 1️⃣ التحقق من المتطلبات الأساسية / Basic Requirements Check

### البيئة / Environment
- [ ] خادم Ubuntu 20.04+ أو نظام Linux مشابه / Ubuntu 20.04+ or similar Linux system
- [ ] Python 3.8+ مثبت / Python 3.8+ installed
- [ ] pip3 مثبت / pip3 installed
- [ ] git مثبت / git installed
- [ ] الذاكرة: 4GB RAM على الأقل / Memory: Minimum 4GB RAM
- [ ] التخزين: 20GB متاح على الأقل / Storage: Minimum 20GB available

### الشبكة / Network
- [ ] المنفذ 80 متاح للاستخدام / Port 80 available
- [ ] المنفذ 443 متاح للاستخدام (للـ HTTPS) / Port 443 available (for HTTPS)
- [ ] اتصال إنترنت مستقر / Stable internet connection
- [ ] DNS مكون بشكل صحيح (إن وجد) / DNS configured correctly (if applicable)

---

## 2️⃣ تحميل وإعداد الكود / Code Download and Setup

### استنساخ المشروع / Clone Project
- [ ] استنساخ المستودع من GitHub / Clone repository from GitHub
  ```bash
  git clone https://github.com/Ali5829511/2025.git
  cd 2025
  ```

### التحقق من الملفات / Verify Files
- [ ] جميع الملفات الأساسية موجودة / All core files present
  - [ ] server.py
  - [ ] database.py
  - [ ] auth.py
  - [ ] requirements.txt
  - [ ] index.html
  - [ ] main_dashboard.html

### تثبيت المتطلبات / Install Requirements
- [ ] إنشاء بيئة افتراضية (موصى به) / Create virtual environment (recommended)
  ```bash
  python3 -m venv venv
  source venv/bin/activate
  ```
- [ ] تثبيت المتطلبات / Install requirements
  ```bash
  pip install -r requirements.txt
  ```
- [ ] التحقق من التثبيت / Verify installation
  ```bash
  pip list
  ```

---

## 3️⃣ إعداد قاعدة البيانات / Database Setup

### إنشاء قاعدة البيانات / Create Database
- [ ] تشغيل سكريبت إنشاء قاعدة البيانات / Run database creation script
  ```bash
  python3 database.py
  ```
- [ ] التحقق من إنشاء ملف housing.db / Verify housing.db file created
- [ ] التحقق من إنشاء الجداول / Verify tables created
- [ ] التحقق من المستخدمين الافتراضيين / Verify default users created

### اختبار قاعدة البيانات / Test Database
- [ ] اختبار الاتصال بقاعدة البيانات / Test database connection
- [ ] التحقق من بنية الجداول / Verify table structure
- [ ] اختبار المستخدمين الافتراضيين / Test default users

---

## 4️⃣ تكوين الأمان / Security Configuration

### ملف البيئة / Environment File
- [ ] إنشاء ملف .env / Create .env file
- [ ] تعيين SECRET_KEY قوي وعشوائي / Set strong random SECRET_KEY
  ```bash
  python3 -c "import os; print(os.urandom(32).hex())"
  ```
- [ ] تعيين FLASK_ENV=production / Set FLASK_ENV=production
- [ ] تعيين FLASK_DEBUG=False / Set FLASK_DEBUG=False

### كلمات المرور / Passwords
- [ ] **تغيير جميع كلمات المرور الافتراضية** / **Change all default passwords**
  - [ ] admin: Admin@2025 → كلمة مرور قوية جديدة / new strong password
  - [ ] violations_officer: Violations@2025 → جديدة / new
  - [ ] visitors_officer: Visitors@2025 → جديدة / new
  - [ ] viewer: Viewer@2025 → جديدة / new
  - [ ] violation_entry: Violation@2025 → جديدة / new

### HTTPS / SSL
- [ ] الحصول على شهادة SSL / Obtain SSL certificate
  - خيار 1: Let's Encrypt (مجاني) / Let's Encrypt (free)
  - خيار 2: شهادة تجارية / Commercial certificate
- [ ] تثبيت شهادة SSL / Install SSL certificate
- [ ] اختبار HTTPS / Test HTTPS

---

## 5️⃣ تكوين الخادم / Server Configuration

### خيار 1: نشر سريع للاختبار / Quick Deployment for Testing
- [ ] تشغيل السكريبت المناسب / Run appropriate script
  ```bash
  ./run.sh  # Linux/Mac
  # OR
  run.bat   # Windows
  ```

### خيار 2: نشر بـ Docker (موصى به) / Docker Deployment (Recommended)
- [ ] تثبيت Docker و Docker Compose / Install Docker and Docker Compose
- [ ] تعديل docker-compose.yml إن لزم / Modify docker-compose.yml if needed
- [ ] تشغيل Docker Compose / Run Docker Compose
  ```bash
  docker-compose up -d
  ```
- [ ] التحقق من حالة الخدمات / Check services status
  ```bash
  docker-compose ps
  ```

### خيار 3: نشر احترافي / Professional Deployment
- [ ] تثبيت Nginx / Install Nginx
- [ ] تثبيت Gunicorn / Install Gunicorn
- [ ] تثبيت Supervisor / Install Supervisor
- [ ] تكوين Nginx / Configure Nginx
- [ ] تكوين Gunicorn / Configure Gunicorn
- [ ] تكوين Supervisor / Configure Supervisor
- [ ] اختبار التكوينات / Test configurations

---

## 6️⃣ تكوين جدار الحماية / Firewall Configuration

### UFW (Ubuntu)
- [ ] تمكين UFW / Enable UFW
  ```bash
  sudo ufw enable
  ```
- [ ] السماح بـ SSH / Allow SSH
  ```bash
  sudo ufw allow OpenSSH
  ```
- [ ] السماح بـ HTTP / Allow HTTP
  ```bash
  sudo ufw allow 80/tcp
  ```
- [ ] السماح بـ HTTPS / Allow HTTPS
  ```bash
  sudo ufw allow 443/tcp
  ```
- [ ] التحقق من الحالة / Check status
  ```bash
  sudo ufw status
  ```

---

## 7️⃣ النسخ الاحتياطي / Backup Setup

### إعداد النسخ الاحتياطي التلقائي / Setup Automatic Backup
- [ ] إنشاء سكريبت النسخ الاحتياطي / Create backup script
- [ ] اختبار سكريبت النسخ الاحتياطي / Test backup script
- [ ] جدولة النسخ الاحتياطي اليومي (cron) / Schedule daily backup (cron)
- [ ] تحديد موقع حفظ النسخ / Define backup location
- [ ] اختبار الاستعادة / Test restore

### مكان التخزين / Storage Location
- [ ] تحديد مجلد النسخ الاحتياطي / Define backup folder
- [ ] التأكد من وجود مساحة كافية / Ensure sufficient space
- [ ] إعداد النسخ الاحتياطي الخارجي (اختياري) / Setup external backup (optional)

---

## 8️⃣ الاختبار النهائي / Final Testing

### اختبارات الوظائف / Functionality Tests
- [ ] اختبار تسجيل الدخول لجميع المستخدمين / Test login for all users
- [ ] اختبار لوحة التحكم / Test dashboard
- [ ] اختبار إضافة البيانات / Test data entry
- [ ] اختبار التقارير / Test reports
- [ ] اختبار البحث / Test search
- [ ] اختبار الصلاحيات / Test permissions

### اختبارات الأمان / Security Tests
- [ ] اختبار تسجيل الخروج / Test logout
- [ ] اختبار انتهاء الجلسة / Test session expiry
- [ ] اختبار حماية CSRF / Test CSRF protection
- [ ] محاولة الوصول غير المصرح / Test unauthorized access
- [ ] اختبار كلمات المرور / Test passwords

### اختبارات الأداء / Performance Tests
- [ ] اختبار تحميل الصفحات / Test page load times
- [ ] اختبار تحت ضغط (عدة مستخدمين) / Test under load (multiple users)
- [ ] مراقبة استخدام الموارد / Monitor resource usage

### اختبارات المتصفحات / Browser Tests
- [ ] Chrome/Chromium
- [ ] Firefox
- [ ] Safari (Mac/iOS)
- [ ] Edge
- [ ] المتصفحات المحمولة / Mobile browsers

---

## 9️⃣ المراقبة والسجلات / Monitoring and Logs

### إعداد السجلات / Setup Logs
- [ ] التحقق من مسارات السجلات / Verify log paths
- [ ] إعداد دوران السجلات / Setup log rotation
- [ ] اختبار كتابة السجلات / Test log writing

### المراقبة / Monitoring
- [ ] إعداد مراقبة حالة النظام / Setup system health monitoring
- [ ] إعداد تنبيهات (اختياري) / Setup alerts (optional)
- [ ] مراقبة استخدام القرص / Monitor disk usage
- [ ] مراقبة استخدام الذاكرة / Monitor memory usage

---

## 🔟 التوثيق والتدريب / Documentation and Training

### التوثيق / Documentation
- [ ] طباعة أو حفظ ملفات التوثيق / Print or save documentation files
  - [ ] README.md
  - [ ] DEPLOYMENT_READY.md
  - [ ] USER_ROLES.md
  - [ ] user_manual.pdf
- [ ] توثيق إعدادات الخادم الخاصة / Document custom server settings
- [ ] توثيق كلمات المرور الجديدة (بشكل آمن!) / Document new passwords (securely!)

### التدريب / Training
- [ ] تدريب المديرين / Train administrators
- [ ] تدريب المستخدمين / Train users
- [ ] إعداد دليل استخدام سريع / Prepare quick user guide
- [ ] تسجيل فيديو توضيحي (اختياري) / Record demo video (optional)

---

## 1️⃣1️⃣ الإطلاق / Launch

### قبل الإطلاق مباشرة / Just Before Launch
- [ ] مراجعة نهائية لجميع النقاط أعلاه / Final review of all points above
- [ ] إنشاء نسخة احتياطية نهائية / Create final backup
- [ ] إعلام المستخدمين بالإطلاق / Notify users of launch
- [ ] تحديد نافذة الصيانة (إن لزم) / Define maintenance window (if needed)

### الإطلاق / Launch
- [ ] تشغيل النظام / Start system
- [ ] التحقق من الوصول / Verify access
- [ ] اختبار سريع نهائي / Quick final test
- [ ] إعلان الجاهزية / Announce readiness

### بعد الإطلاق / After Launch
- [ ] مراقبة مكثفة للـ 24 ساعة الأولى / Intensive monitoring for first 24 hours
- [ ] جمع ملاحظات المستخدمين / Collect user feedback
- [ ] معالجة أي مشاكل فورية / Address any immediate issues
- [ ] توثيق الدروس المستفادة / Document lessons learned

---

## 📞 جهات الاتصال للطوارئ / Emergency Contacts

### فريق الدعم / Support Team
- **الدعم الفني / Technical Support:**
  - الاسم / Name: _________________
  - الهاتف / Phone: _________________
  - البريد / Email: _________________

- **مدير النظام / System Administrator:**
  - الاسم / Name: _________________
  - الهاتف / Phone: _________________
  - البريد / Email: _________________

- **مسؤول الأمان / Security Officer:**
  - الاسم / Name: _________________
  - الهاتف / Phone: _________________
  - البريد / Email: _________________

---

## ✅ التوقيعات / Signatures

### الموافقة على النشر / Deployment Approval

**قام بالإعداد / Prepared By:**
- الاسم / Name: _________________
- التاريخ / Date: _________________
- التوقيع / Signature: _________________

**راجعه / Reviewed By:**
- الاسم / Name: _________________
- التاريخ / Date: _________________
- التوقيع / Signature: _________________

**وافق عليه / Approved By:**
- الاسم / Name: _________________
- التاريخ / Date: _________________
- التوقيع / Signature: _________________

---

## 📊 ملخص الجاهزية / Readiness Summary

```
إجمالي النقاط / Total Points: 100+
النقاط المكتملة / Completed: ___
نسبة الإنجاز / Completion: ___%

الحالة / Status:
[ ] ✅ جاهز للنشر (>95%) / Ready for deployment (>95%)
[ ] ⚠️ يحتاج مراجعة (80-95%) / Needs review (80-95%)
[ ] ❌ غير جاهز (<80%) / Not ready (<80%)
```

---

## 🎯 ملاحظات إضافية / Additional Notes

```
استخدم هذا القسم لتوثيق أي ملاحظات أو اعتبارات خاصة:
Use this section to document any special notes or considerations:

_______________________________________________________________
_______________________________________________________________
_______________________________________________________________
_______________________________________________________________
_______________________________________________________________
```

---

**تم الإعداد بواسطة / Prepared By:** فريق التطوير / Development Team  
**الإصدار / Version:** 2.0.1  
**التاريخ / Date:** ديسمبر 2025 / December 2025

**جامعة الإمام محمد بن سعود الإسلامية © 2025**  
**Imam Mohammad Ibn Saud Islamic University © 2025**
