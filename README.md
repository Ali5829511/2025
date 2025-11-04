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

## التشغيل / Running

يمكن تشغيل التطبيق باستخدام أحد الملفين:

You can run the application using either file:

```bash
python main.py
# أو / or
python app.py
```

سيعمل التطبيق على المنفذ 5000. افتح المتصفح على:

The application will run on port 5000. Open your browser at:

```
http://localhost:5000
```

## بيانات تسجيل الدخول الافتراضية / Default Login Credentials

### مدير النظام / System Administrator
- اسم المستخدم / Username: `admin`
- كلمة المرور / Password: `admin123`

### مسؤول المخالفات / Violations Officer
- اسم المستخدم / Username: `violations_officer`
- كلمة المرور / Password: `violations123`

### مسؤول الزوار / Visitors Officer
- اسم المستخدم / Username: `visitors_officer`
- كلمة المرور / Password: `visitors123`

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
├── app.py                              # تطبيق Flask / Flask application
├── main.py                             # تطبيق Flask (بديل) / Flask application (alternative)
├── requirements.txt                    # متطلبات Python / Python dependencies
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
- ⚠️ نظام المصادقة الحالي مبني على localStorage وهو للعرض التوضيحي فقط
- ⚠️ Current authentication is localStorage-based and for demonstration only
- يجب تنفيذ مصادقة من جانب الخادم قبل النشر / Implement server-side authentication before deployment
- استخدم JWT أو OAuth2 للمصادقة الآمنة / Use JWT or OAuth2 for secure authentication
- قم بتطبيق تحكم الوصول المبني على الأدوار (RBAC) من جانب الخادم / Implement server-side RBAC

**حماية البيانات / Data Protection:**
- استخدم HTTPS في بيئة الإنتاج (مطلوب) / Use HTTPS in production (required)
- قم بتشفير البيانات الحساسة في قاعدة البيانات / Encrypt sensitive data in database
- لا تخزن كلمات المرور بنص عادي / Never store passwords in plain text
- استخدم التشفير القوي (bcrypt، Argon2) لكلمات المرور / Use strong hashing (bcrypt, Argon2) for passwords

**تطبيق Flask / Flask Application:**
- ✅ تم تطبيق حماية من اختراق المسارات / Path traversal protection implemented
- ✅ قائمة بيضاء لامتدادات الملفات المسموحة / Whitelist of allowed file extensions
- ✅ حظر الملفات الحساسة (.env، .git، إلخ) / Blocked sensitive files (.env, .git, etc.)
- ⚠️ وضع التصحيح مفعّل - يجب تعطيله في الإنتاج / Debug mode enabled - must be disabled in production
- استخدم خادم WSGI إنتاجي (Gunicorn، uWSGI) / Use production WSGI server (Gunicorn, uWSGI)

### قائمة فحص ما قبل النشر / Pre-Deployment Checklist

- [ ] تغيير جميع كلمات المرور الافتراضية / Change all default passwords
- [ ] تعطيل وضع التصحيح في Flask / Disable Flask debug mode
- [ ] إعداد خادم WSGI إنتاجي / Set up production WSGI server
- [ ] تكوين HTTPS مع شهادة SSL صالحة / Configure HTTPS with valid SSL certificate
- [ ] تنفيذ مصادقة من جانب الخادم / Implement server-side authentication
- [ ] إعداد قاعدة بيانات آمنة / Set up secure database
- [ ] إعداد النسخ الاحتياطي التلقائي / Configure automated backups
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
