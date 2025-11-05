# نظام إدارة إسكان أعضاء هيئة التدريس
# Faculty Housing Management System

نظام شامل لإدارة إسكان أعضاء هيئة التدريس في جامعة الإمام محمد بن سعود الإسلامية.

A comprehensive system for managing faculty housing at Imam Mohammad Ibn Saud Islamic University.

## المميزات / Features

- 🏢 إدارة المباني والشقق / Buildings and Apartments Management
- 👥 إدارة السكان / Residents Management  
- 🚗 إدارة المواقف والملصقات / Parking and Stickers Management
- 🚦 إدارة المخالفات والحوادث المرورية / Traffic Violations and Accidents Management
- 🔒 إدارة الأمن والوقائع الأمنية / Security Incidents Management
- 📝 إدارة الشكاوى والزوار / Complaints and Visitors Management
- 📊 تقارير شاملة وإحصائيات / Comprehensive Reports and Statistics
- 👮 صلاحيات متعددة للمستخدمين / Multi-level User Permissions

## المتطلبات / Requirements

- Python 3.8 أو أحدث / Python 3.8 or higher
- Flask 2.3.3
- Flask-CORS 4.0.0
- Werkzeug 3.0.1 (for password hashing)
- SQLite 3 (included with Python)
- متصفح حديث يدعم HTML5 و CSS3 / Modern browser with HTML5 and CSS3 support

## التثبيت / Installation

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

**الخادم الجديد مع قاعدة البيانات / New Server with Database (Recommended):**

```bash
python3 server.py
```

**الخادم القديم (بدون قاعدة بيانات) / Legacy Server (No Database):**

```bash
python3 main.py
# أو / or
python3 app.py
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
├── server.py                           # ✅ خادم Flask الجديد مع قاعدة البيانات / New Flask server with database
├── database.py                         # ✅ نظام قاعدة البيانات / Database system
├── auth.py                             # ✅ نظام المصادقة والجلسات / Authentication and session system
├── app.py                              # خادم Flask القديم (بدون قاعدة بيانات) / Legacy Flask server (no database)
├── main.py                             # خادم Flask القديم (بدون قاعدة بيانات) / Legacy Flask server (no database)
├── housing.db                          # قاعدة بيانات SQLite (تُنشأ تلقائياً) / SQLite database (auto-created)
├── requirements.txt                    # متطلبات Python / Python dependencies
├── .env.example                        # مثال ملف التكوين / Configuration file example
└── README.md                           # هذا الملف / This file
```

## الوثائق / Documentation

- [الدليل التشغيلي الشامل](الدليل%20التشغيلي%20الشامل%20لنظام%20إدارة%20الإسكان%20الجامعي.md)
- [دليل تشغيل النظام](دليل%20تشغيل%20نظام%20إدارة%20إسكان%20أعضاء%20هيئة%20التدريس.md)
- [مخطط الدليل التشغيلي](user_manual_outline.md)
- [دليل المستخدم (PDF)](user_manual_with_images.pdf)

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
