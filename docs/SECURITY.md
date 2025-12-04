# سياسة الأمان / Security Policy

## الإصدارات المدعومة / Supported Versions

| الإصدار / Version | مدعوم / Supported |
| ------- | ------------------ |
| 1.0.x   | :white_check_mark: |

## الإبلاغ عن الثغرات الأمنية / Reporting a Vulnerability

### باللغة العربية

إذا اكتشفت ثغرة أمنية في هذا المشروع، نرجو منك:

1. **عدم** فتح issue عام على GitHub
2. الاتصال بفريق الأمان في الجامعة مباشرة
3. تقديم وصف تفصيلي للثغرة وكيفية إعادة إنتاجها
4. إعطاء الفريق وقتاً معقولاً لمعالجة المشكلة قبل الكشف العام

### In English

If you discover a security vulnerability in this project, please:

1. **Do NOT** open a public issue on GitHub
2. Contact the university's security team directly
3. Provide a detailed description of the vulnerability and how to reproduce it
4. Give the team reasonable time to address the issue before public disclosure

## اعتبارات أمنية معروفة / Known Security Considerations

### ✅ منجز / Completed

1. **✅ المصادقة من جانب الخادم / Server-Side Authentication**
   - ✅ **تم تنفيذ** نظام مصادقة آمن من جانب الخادم
   - ✅ **Implemented** secure server-side authentication system
   - ✅ استخدام Werkzeug لتشفير كلمات المرور بـ pbkdf2:sha256
   - ✅ Using Werkzeug for pbkdf2:sha256 password hashing
   - ✅ إدارة الجلسات مع رموز آمنة
   - ✅ Session management with secure tokens

2. **✅ قاعدة بيانات آمنة / Secure Database**
   - ✅ **تم إنشاء** قاعدة بيانات SQLite مع جداول منظمة
   - ✅ **Created** SQLite database with structured tables
   - ✅ كلمات المرور مشفرة ولا تُخزن بنص عادي
   - ✅ Passwords hashed, not stored in plain text
   - ✅ سجل تدقيق شامل للعمليات الحساسة
   - ✅ Comprehensive audit log for sensitive operations

3. **✅ حماية من اختراق المسارات / Path Traversal Protection**
   - ✅ استخدام werkzeug.security.safe_join
   - ✅ Using werkzeug.security.safe_join
   - ✅ قائمة بيضاء لامتدادات الملفات
   - ✅ Whitelist for file extensions
   - ✅ حظر الملفات الحساسة
   - ✅ Blocked sensitive files

### ✅ تحديثات الأمان الأخيرة / Recent Security Updates (2025-11-17)

1. **✅ فرض تغيير كلمة المرور / Password Change Enforcement**
   - ✅ حقل must_change_password في جدول المستخدمين
   - ✅ must_change_password field in users table
   - ✅ فرض تلقائي عند أول تسجيل دخول
   - ✅ Automatic enforcement on first login
   - ✅ API endpoint لتغيير كلمة المرور
   - ✅ Password change API endpoint

2. **✅ ترويسات الأمان / Security Headers**
   - ✅ X-Frame-Options: SAMEORIGIN
   - ✅ X-Content-Type-Options: nosniff
   - ✅ X-XSS-Protection: 1; mode=block
   - ✅ Content-Security-Policy (للإنتاج / for production)
   - ✅ Strict-Transport-Security (HTTPS)
   - ✅ Referrer-Policy
   - ✅ Permissions-Policy

3. **✅ نظام السجلات الشامل / Comprehensive Logging**
   - ✅ سجلات منفصلة للأمان والتدقيق
   - ✅ Separate security and audit logs
   - ✅ تتبع جميع أحداث المصادقة
   - ✅ Track all authentication events
   - ✅ الاحتفاظ بالسجلات لمدة سنة
   - ✅ Log retention up to 1 year

4. **✅ النسخ الاحتياطي التلقائي / Automated Backups**
   - ✅ سكريبت نسخ احتياطي تلقائي
   - ✅ Automated backup script
   - ✅ دعم SQLite و PostgreSQL
   - ✅ SQLite and PostgreSQL support
   - ✅ ضغط وتحميل إلى S3
   - ✅ Compression and S3 upload

5. **✅ اختبار الأمان / Security Testing**
   - ✅ سكريبت اختبار تلقائي
   - ✅ Automated testing script
   - ✅ فحص حقن SQL
   - ✅ SQL injection check
   - ✅ فحص XSS
   - ✅ XSS check
   - ✅ اختبار SSL/TLS
   - ✅ SSL/TLS testing

### 🟡 تحذيرات / Warnings

1. **كلمات المرور الافتراضية / Default Passwords**
   - كلمات مرور افتراضية قوية في قاعدة البيانات
   - Strong default passwords in database
   - **يجب** تغييرها بعد أول تسجيل دخول
   - **Must** change after first login
   - Admin@2025, Violations@2025, Visitors@2025

2. **وضع التصحيح / Debug Mode**
   - Flask debug mode مفعّل للتطوير فقط
   - Flask debug mode enabled for development only
   - **يجب** تعطيله في الإنتاج (FLASK_DEBUG=False)
   - **Must** disable in production (FLASK_DEBUG=False)

3. **HTTPS**
   - التطبيق يعمل على HTTP فقط
   - Application runs on HTTP only
   - **يجب** استخدام HTTPS في الإنتاج
   - **Must** use HTTPS in production

### ✅ تدابير أمنية منفذة / Implemented Security Measures

1. **حماية من اختراق المسارات / Path Traversal Protection**
   - استخدام werkzeug.security.safe_join
   - Using werkzeug.security.safe_join
   - منع الوصول إلى الدلائل الأم
   - Prevents access to parent directories

2. **قائمة بيضاء للملفات / File Whitelist**
   - السماح فقط بامتدادات ملفات محددة
   - Only allow specific file extensions
   - منع الوصول إلى ملفات Python وملفات التكوين
   - Prevents access to Python and configuration files

3. **حماية الملفات الحساسة / Sensitive Files Protection**
   - حظر الوصول إلى .env، .git، .gitignore، إلخ
   - Block access to .env, .git, .gitignore, etc.

## أفضل الممارسات للنشر / Best Practices for Deployment

### قبل النشر / Before Deployment

- [ ] تنفيذ مصادقة من جانب الخادم
- [ ] Implement server-side authentication
- [ ] استخدام قاعدة بيانات آمنة (PostgreSQL، MySQL)
- [ ] Use secure database (PostgreSQL, MySQL)
- [ ] تشفير كلمات المرور (bcrypt، Argon2)
- [ ] Encrypt passwords (bcrypt, Argon2)
- [ ] تعطيل وضع التصحيح
- [ ] Disable debug mode
- [ ] استخدام خادم WSGI إنتاجي (Gunicorn، uWSGI)
- [ ] Use production WSGI server (Gunicorn, uWSGI)
- [ ] تكوين HTTPS مع شهادة SSL
- [ ] Configure HTTPS with SSL certificate
- [ ] تنفيذ CORS بشكل صحيح
- [ ] Implement CORS properly
- [ ] إضافة rate limiting
- [ ] Add rate limiting
- [ ] إعداد السجلات والمراقبة
- [ ] Set up logging and monitoring
- [ ] اختبار الاختراق
- [ ] Penetration testing

### بعد النشر / After Deployment

- [ ] مراقبة السجلات بانتظام
- [ ] Monitor logs regularly
- [ ] تحديث التبعيات بانتظام
- [ ] Update dependencies regularly
- [ ] النسخ الاحتياطي المنتظم
- [ ] Regular backups
- [ ] مراجعة الأمان الدورية
- [ ] Periodic security reviews

## الموارد / Resources

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [Flask Security Best Practices](https://flask.palletsprojects.com/en/2.3.x/security/)
- [Python Security Best Practices](https://python.readthedocs.io/en/latest/library/security_warnings.html)

## الاتصال / Contact

للإبلاغ عن مشكلات أمنية، يرجى التواصل مع:

For reporting security issues, please contact:

- فريق تقنية المعلومات بجامعة الإمام محمد بن سعود الإسلامية
- IT Team at Imam Mohammad Ibn Saud Islamic University

---

**آخر تحديث / Last Updated:** نوفمبر 2025 / November 2025
