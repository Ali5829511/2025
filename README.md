# نظام إدارة إسكان أعضاء هيئة التدريس
# Faculty Housing Management System

**🚀 الإصدار 2.0.1 - جاهز للنشر / Version 2.0.1 - Production Ready**

نظام شامل لإدارة إسكان أعضاء هيئة التدريس في جامعة الإمام محمد بن سعود الإسلامية.

A comprehensive system for managing faculty housing at Imam Mohammad Ibn Saud Islamic University.

[![Status](https://img.shields.io/badge/Status-Production%20Ready-success)](https://github.com/Ali5829511/2025)
[![Deployment](https://img.shields.io/badge/Deployment-Ready%20%7C%20Not%20Published-orange)](DEPLOYMENT_STATUS.md)
[![Version](https://img.shields.io/badge/Version-2.0.1-blue)](https://github.com/Ali5829511/2025)
[![Security](https://img.shields.io/badge/Security-Hardened-green)](SECURITY.md)
[![Docker](https://img.shields.io/badge/Docker-Hub-blue?logo=docker)](https://hub.docker.com/r/ali517/housing-management)

## ⭐ المراجعة الشاملة الأخيرة / Latest Comprehensive Review

**🎉 تم إجراء مراجعة شاملة للنظام بتاريخ 2025-11-07**

- ✅ **التقييم:** ⭐⭐⭐⭐⭐ ممتاز (5/5)
- ✅ **الحالة:** جاهز للنشر الإنتاجي
- ✅ **الأمان:** A- (ممتاز)
- 📄 **التقرير الكامل:** [COMPREHENSIVE_SYSTEM_REVIEW.md](COMPREHENSIVE_SYSTEM_REVIEW.md)
- 📄 **الملخص العربي:** [ملخص_المراجعة_النهائي.md](ملخص_المراجعة_النهائي.md)

**A comprehensive system review was conducted on 2025-11-07:**
- ✅ Rating: ⭐⭐⭐⭐⭐ Excellent (5/5)
- ✅ Status: Production Ready
- ✅ Security: A- (Excellent)
- 📄 Full Report: [COMPREHENSIVE_SYSTEM_REVIEW.md](COMPREHENSIVE_SYSTEM_REVIEW.md)

## 🌐 حالة النشر / Deployment Status

**📊 [تقرير حالة النشر الكامل / Full Deployment Status Report](DEPLOYMENT_STATUS.md)**

**السؤال:** هل تم نشر النظام؟ / **Question:** Has the system been published?

**الإجابة / Answer:**
- ✅ النظام مكتمل التطوير وجاهز 100% للنشر / System fully developed and 100% ready
- ✅ جميع ملفات النشر جاهزة / All deployment files ready
- ⚠️ **لم يتم النشر على بيئة إنتاجية عامة بعد** / **Not yet published to public production**
- 🚀 يمكن النشر في 10-15 دقيقة فقط / Can be deployed in just 10-15 minutes

**خيارات النشر السريع / Quick Deployment Options:**
- 🐳 [Docker Hub](https://hub.docker.com/r/ali517/housing-management) - متاح للتشغيل المحلي / Available for local deployment
- ☁️ [Render.com](RENDER_DEPLOYMENT.md) - جاهز للتفعيل (10 دقائق) / Ready to activate (10 min)
- ✈️ [Fly.io](FLY_IO_DEPLOYMENT.md) - جاهز للنشر الإنتاجي / Ready for production deployment
- 📖 [دليل النشر السريع / Quick Deploy Guide](دليل_النشر_السحابي.md)

**للمزيد من التفاصيل / For more details:** راجع [DEPLOYMENT_STATUS.md](DEPLOYMENT_STATUS.md)

## المميزات / Features

- 🏢 إدارة المباني والشقق / Buildings and Apartments Management
- 👥 إدارة السكان / Residents Management  
- 🚗 إدارة المواقف والملصقات / Parking and Stickers Management
- 🚦 إدارة المخالفات والحوادث المرورية / Traffic Violations and Accidents Management
- 🔒 إدارة الأمن والوقائع الأمنية / Security Incidents Management
- 📝 إدارة الشكاوى والزوار / Complaints and Visitors Management
- 📊 تقارير شاملة وإحصائيات / Comprehensive Reports and Statistics
- ✅ **تقرير التحقق الشامل من النظام** - مراجعة جميع الصفحات والبيانات مع علامات ⚠️ للصفحات الفارغة / **Comprehensive System Validation Report** - Review all pages and data with ⚠️ markers for empty pages
- 👮 صلاحيات متعددة للمستخدمين / Multi-level User Permissions
- 📷 **تمييز لوحات السيارات تلقائياً / Automatic License Plate Recognition** (NEW!)

## المتطلبات / Requirements

- Python 3.12 أو أحدث (موصى به) / Python 3.12 or higher (recommended)
- Python 3.8+ مدعوم / Python 3.8+ supported
- Flask 3.0.0
- Flask-CORS 4.0.0
- Werkzeug 3.0.3 (for password hashing)
- pandas 2.2.3 (متوافق مع Python 3.13 / Compatible with Python 3.13)
- SQLite 3 (included with Python)
- متصفح حديث يدعم HTML5 و CSS3 / Modern browser with HTML5 and CSS3 support

## التثبيت / Installation

### 🐳 النشر باستخدام Docker Hub (الطريقة الأسرع) / Using Docker Hub (Fastest)

**الطريقة الموصى بها للنشر السريع!** / **Recommended for quick deployment!**

```bash
# سحب الصورة من Docker Hub / Pull image from Docker Hub
docker pull ali517/housing-management:latest

# تشغيل مع docker-compose / Run with docker-compose
curl -O https://raw.githubusercontent.com/Ali5829511/2025/main/docker-compose.hub.yml
docker-compose -f docker-compose.hub.yml up -d

# الوصول للنظام / Access the system
# افتح المتصفح على / Open browser at: http://localhost
```

📖 **دليل كامل**: راجع [دليل Docker Hub](DOCKER_HUB_GUIDE.md) للتفاصيل  
📖 **Complete Guide**: See [Docker Hub Guide](DOCKER_HUB_GUIDE.md) for details

### 📦 التثبيت التقليدي / Traditional Installation

1. استنساخ المستودع / Clone the repository:
```bash
git clone https://github.com/Ali5829511/2025.git
cd 2025
```

2. إنشاء بيئة افتراضية (موصى به) / Create a virtual environment (recommended):
```bash
python3 -m venv venv
source venv/bin/activate  # على Linux/Mac / On Linux/Mac
# أو / or
venv\Scripts\activate  # على Windows / On Windows
```

3. تثبيت المتطلبات / Install dependencies:
```bash
pip install -r requirements.txt
```

4. إنشاء قاعدة البيانات / Initialize the database:
```bash
python3 database.py
```

سيتم إنشاء قاعدة بيانات SQLite مع المستخدمين الافتراضيين.  
This will create an SQLite database with default users.

## التشغيل / Running

### 🚀 التشغيل السريع / Quick Start

> **⚠️ مهم:** إذا واجهت خطأ 500، راجع [دليل البدء السريع](QUICK_START.md) لحل المشكلة  
> **⚠️ Important:** If you encounter error 500, check the [Quick Start Guide](QUICK_START.md) for troubleshooting

**على Linux/Mac:**
```bash
./run.sh
```

**على Windows:**
```cmd
run.bat
```

السكريبت سيقوم تلقائياً بـ:
- فحص وتثبيت المتطلبات
- إنشاء قاعدة البيانات إذا لم تكن موجودة
- تشغيل الخادم

The script will automatically:
- Check and install dependencies
- Create database if not exists
- Start the server

### التشغيل اليدوي / Manual Start

```bash
python3 server.py
```

سيعمل التطبيق على المنفذ 5000. افتح المتصفح على:

The application will run on port 5000. Open your browser at:

```
http://localhost:5000
```

## بيانات تسجيل الدخول الافتراضية / Default Login Credentials

**🔒 نظام المصادقة الآمن مع قاعدة البيانات / Secure Database Authentication**

### مدير النظام / System Administrator
- اسم المستخدم / Username: `admin`
- كلمة المرور / Password: `Admin@2025`
- الصلاحيات / Permissions: **كاملة** (إضافة، تعديل، حذف، عرض)

### مسؤول المخالفات / Violations Officer
- اسم المستخدم / Username: `violations_officer`
- كلمة المرور / Password: `Violations@2025`
- الصلاحيات / Permissions: **محدودة** (المخالفات والحوادث المرورية)

### مسؤول الزوار / Visitors Officer
- اسم المستخدم / Username: `visitors_officer`
- كلمة المرور / Password: `Visitors@2025`
- الصلاحيات / Permissions: **محدودة** (الزوار والشكاوى)

### مستخدم استعلام فقط / View-Only User
- اسم المستخدم / Username: `viewer`
- كلمة المرور / Password: `Viewer@2025`
- الصلاحيات / Permissions: **استعلام فقط** (عرض البيانات بدون تعديل)

### مسجل المخالفات / Violation Entry User
- اسم المستخدم / Username: `violation_entry`
- كلمة المرور / Password: `Violation@2025`
- الصلاحيات / Permissions: **تسجيل المخالفات المرورية فقط**
- التوجيه / Redirect: يتم توجيهه مباشرة إلى نموذج تسجيل المخالفة عند تسجيل الدخول

**⚠️ يرجى تغيير كلمات المرور بعد أول تسجيل دخول**  
**⚠️ Please change passwords after first login**

## هيكل المشروع / Project Structure

```
├── index.html                          # صفحة تسجيل الدخول / Login page
├── main_dashboard.html                 # لوحة التحكم الرئيسية / Main dashboard
├── buildings_management_updated.html   # إدارة المباني / Buildings management
├── apartments_management.html          # إدارة الشقق / Apartments management
├── residents_management_updated.html   # إدارة السكان / Residents management
├── enhanced_parking_management.html    # إدارة المواقف / Parking management
├── enhanced_stickers_management.html   # إدارة الملصقات / Stickers management
├── enhanced_immobilized_cars.html      # السيارات المكبوحة / Immobilized cars
├── enhanced_traffic_violations_updated.html  # المخالفات المرورية / Traffic violations
├── enhanced_traffic_accidents.html     # الحوادث المرورية / Traffic accidents
├── security_incidents.html             # الوقائع الأمنية / Security incidents
├── complaints_management.html          # إدارة الشكاوى / Complaints management
├── visitors_management.html            # إدارة الزوار / Visitors management
├── access_monitoring.html              # مراقبة الدخول / Access monitoring
├── comprehensive_reports_enhanced.html # التقارير الشاملة / Comprehensive reports
├── advanced_users_management.html      # إدارة المستخدمين / Users management
├── admin_permissions.js                # صلاحيات المدير / Admin permissions
├── server.py                           # ✅ خادم Flask مع قاعدة البيانات / Flask server with database
├── database.py                         # ✅ نظام قاعدة البيانات / Database system
├── auth.py                             # ✅ نظام المصادقة والجلسات / Authentication and session system
├── housing.db                          # قاعدة بيانات SQLite (تُنشأ تلقائياً) / SQLite database (auto-created)
├── requirements.txt                    # متطلبات Python / Python dependencies
├── .env.example                        # مثال ملف التكوين / Configuration file example
└── README.md                           # هذا الملف / This file
```

## الوثائق / Documentation

📚 **[فهرس الوثائق الشامل / Comprehensive Documentation Index](DOCUMENTATION_INDEX.md)** - دليل كامل لجميع الوثائق المتاحة

### وثائق النظام / System Documentation
- [الدليل التشغيلي الشامل](الدليل%20التشغيلي%20الشامل%20لنظام%20إدارة%20الإسكان%20الجامعي.md)
- [دليل تشغيل النظام](دليل%20تشغيل%20نظام%20إدارة%20إسكان%20أعضاء%20هيئة%20التدريس.md)
- [مخطط الدليل التشغيلي](user_manual_outline.md)
- [دليل المستخدم (PDF)](user_manual_with_images.pdf)
- [**دليل استخدام نظام تمييز لوحات السيارات**](PLATE_RECOGNIZER_GUIDE.md) ⭐ NEW!
- [**إدارة رمز-برو (نظام الملصقات)**](RAMZ_PRO_MANAGEMENT.md) | [النسخة العربية](إدارة_رمز_برو.md) ⭐ NEW!

### التقارير والمراجعة / Reports & Review
- [تقرير المراجعة الشاملة](تقرير_المراجعة_الشاملة.md) - تقرير كامل عن حالة النظام والبيانات
- [System Validation Report Documentation](SYSTEM_VALIDATION_REPORT.md) - Technical documentation for validation report
- [تقرير التحقق من النظام (صفحة ويب)](system_validation_report.html) - أداة تفاعلية لمراجعة البيانات

### إدارة الفروع والمستودع / Branch and Repository Management
- 🧹 **[تقرير تنظيف الفروع](BRANCH_CLEANUP_REPORT.md)** - قائمة الفروع للحذف مع سكريبت التنفيذ ⭐ **NEW!**
- 🌿 **[دليل اتخاذ القرار: دمج الفروع أو تركها](BRANCH_MANAGEMENT_DECISION_GUIDE.md)** - دليل شامل ثنائي اللغة
- 🌿 **[دليل إدارة الفروع](دليل_إدارة_الفروع.md)** - دليل عربي مفصل مع أمثلة عملية
- 📋 **[ملخص قرار إدارة الفروع](BRANCH_DECISION_SUMMARY.md)** - إجابة مباشرة على "دمج أو ترك؟"
- 📊 [تقرير حالة الدمج](MERGE_STATUS_REPORT.md) - تحليل تفصيلي لحالة دمج الفروع
- 📊 [ملخص الدمج (عربي)](MERGE_SUMMARY_AR.md) - ملخص ثنائي اللغة

### النشر والتثبيت / Deployment & Installation
- 🐳 **[دليل Docker Hub](DOCKER_HUB_GUIDE.md)** - نشر ومشاركة الصور على Docker Hub ⭐ **NEW!**
- 🔐 **[إعداد أسرار النشر](DEPLOYMENT_SECRETS_SETUP.md)** - تكوين أسرار GitHub لـ Docker Hub و Fly.io ⭐ **NEW!**
- 🌟 **[دليل النشر السحابي السريع](دليل_النشر_السحابي.md)** - ابدأ هنا! النشر في 10 دقائق ⭐ NEW!
- ☁️ **[خيارات الاستضافة السحابية](CLOUD_HOSTING_OPTIONS.md)** - مقارنة شاملة للمنصات مع فترة تجريبية ⭐ NEW!
- ✈️ **[النشر على Fly.io](FLY_IO_DEPLOYMENT.md)** - منصة حديثة مع طبقة مجانية سخية (موصى به!) ⭐ **NEW!**
- 🎯 **[النشر على Render.com](RENDER_DEPLOYMENT.md)** - الطريقة الموصى بها (لا يحتاج بطاقة ائتمانية) ⭐ NEW!
- 🚀 **[دليل النشر الكامل](دليل_النشر_الكامل.md)** - دليل شامل للنشر الاحترافي مع Nginx وPostgreSQL
- 🐳 **[النشر باستخدام Docker](النشر_باستخدام_Docker.md)** - الطريقة الأسرع للنشر (5 دقائق فقط!)
- ⚡ [QUICK_START.md](QUICK_START.md) - البدء السريع للتطوير المحلي
- 🔧 [حل_خطأ_500.md](حل_خطأ_500.md) - استكشاف الأخطاء وإصلاحها

## الأمان / Security

⚠️ **ملاحظة هامة:** بيانات تسجيل الدخول الحالية مخصصة للاختبار فقط. يجب تغييرها في بيئة الإنتاج.

⚠️ **Important Note:** Current login credentials are for testing only. They must be changed in production environment.

### اعتبارات الأمان / Security Considerations

**المصادقة والترخيص / Authentication & Authorization:**
- ✅ **نظام مصادقة من جانب الخادم مُنفّذ / Server-side authentication implemented**
- ✅ **قاعدة بيانات SQLite مع تشفير كلمات المرور / SQLite database with password hashing**
- ✅ **استخدام Werkzeug لتشفير كلمات المرور بـ pbkdf2 / Using Werkzeug for pbkdf2 password hashing**
- ✅ **إدارة الجلسات مع رموز آمنة / Session management with secure tokens**
- ✅ **تسجيل الدخول والخروج آمن / Secure login and logout**
- ✅ **سجل التدقيق للعمليات الحساسة / Audit log for sensitive operations**
- ✅ **تحكم الوصول المبني على الأدوار (RBAC) / Role-based access control (RBAC)**

**قاعدة البيانات / Database:**
- ✅ **SQLite مع جداول منظمة / SQLite with structured tables**
- ✅ **كلمات المرور مشفرة باستخدام pbkdf2:sha256 / Passwords hashed using pbkdf2:sha256**
- ✅ **جداول للمستخدمين، الجلسات، السكان، المركبات، المخالفات، الشكاوى، الزوار، الوقائع الأمنية / Tables for users, sessions, residents, vehicles, violations, complaints, visitors, security incidents**
- ✅ **سجل تدقيق شامل / Comprehensive audit log**

**حماية البيانات / Data Protection:**
- ✅ كلمات المرور مشفرة ولا تُخزن بنص عادي / Passwords hashed, not stored in plain text
- ✅ رموز الجلسات آمنة مع انتهاء صلاحية تلقائي / Secure session tokens with automatic expiry
- ⚠️ استخدم HTTPS في بيئة الإنتاج (مطلوب) / Use HTTPS in production (required)
- قم بتشفير البيانات الحساسة في قاعدة البيانات للإنتاج / Encrypt sensitive data in production database

**تطبيق Flask / Flask Application:**
- ✅ تم تطبيق حماية من اختراق المسارات / Path traversal protection implemented
- ✅ قائمة بيضاء لامتدادات الملفات المسموحة / Whitelist of allowed file extensions
- ✅ حظر الملفات الحساسة (.env، .git، .py، .db، إلخ) / Blocked sensitive files (.env, .git, .py, .db, etc.)
- ✅ API endpoints للمصادقة الآمنة / Secure authentication API endpoints
- ⚠️ وضع التصحيح مفعّل في التطوير - يجب تعطيله في الإنتاج / Debug mode enabled in development - must be disabled in production
- استخدم خادم WSGI إنتاجي (Gunicorn، uWSGI) / Use production WSGI server (Gunicorn, uWSGI)

### قائمة فحص ما قبل النشر / Pre-Deployment Checklist

**منجز / Completed:**
- [x] ✅ تنفيذ مصادقة من جانب الخادم / Implement server-side authentication
- [x] ✅ إعداد قاعدة بيانات آمنة (SQLite مع تشفير كلمات المرور) / Set up secure database (SQLite with password hashing)
- [x] ✅ نظام إدارة الجلسات / Session management system
- [x] ✅ سجل التدقيق / Audit logging
- [x] ✅ حماية من اختراق المسارات / Path traversal protection

**مطلوب للإنتاج / Required for Production:**
- [ ] تغيير جميع كلمات المرور الافتراضية / Change all default passwords
- [ ] تعطيل وضع التصحيح في Flask (تعيين FLASK_DEBUG=False) / Disable Flask debug mode (set FLASK_DEBUG=False)
- [ ] إعداد خادم WSGI إنتاجي (Gunicorn) / Set up production WSGI server (Gunicorn)
- [ ] تكوين HTTPS مع شهادة SSL صالحة / Configure HTTPS with valid SSL certificate
- [ ] نقل قاعدة البيانات إلى PostgreSQL أو MySQL (اختياري) / Migrate to PostgreSQL or MySQL (optional)
- [ ] إعداد النسخ الاحتياطي التلقائي لقاعدة البيانات / Configure automated database backups
- [ ] تكوين جدار الحماية / Configure firewall
- [ ] مراجعة صلاحيات الملفات / Review file permissions
- [ ] إعداد السجلات والمراقبة / Set up logging and monitoring
- [ ] اختبار الأمان والاختراق / Perform security and penetration testing
- [ ] مراجعة وتحديث الوثائق / Review and update documentation
- [ ] تدريب المستخدمين على الأمان / Train users on security practices

## المساهمة / Contributing

المساهمات مرحب بها! يرجى فتح issue أو pull request.

Contributions are welcome! Please open an issue or pull request.

## الترخيص / License

جميع الحقوق محفوظة © جامعة الإمام محمد بن سعود الإسلامية 2025

All rights reserved © Imam Mohammad Ibn Saud Islamic University 2025

## الدعم / Support

للحصول على الدعم، يرجى التواصل مع فريق تقنية المعلومات بالجامعة.

For support, please contact the university's IT team.
