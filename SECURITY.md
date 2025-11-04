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

### 🔴 حرجة / Critical

1. **المصادقة من جانب العميل / Client-Side Authentication**
   - النظام الحالي يستخدم localStorage للمصادقة (للعرض التوضيحي فقط)
   - Current system uses localStorage for authentication (demonstration only)
   - **يجب** تنفيذ مصادقة من جانب الخادم قبل الإنتاج
   - **Must** implement server-side authentication before production

2. **عدم وجود قاعدة بيانات / No Database**
   - جميع البيانات مخزنة في localStorage (غير آمن)
   - All data stored in localStorage (not secure)
   - **يجب** استخدام قاعدة بيانات آمنة في الإنتاج
   - **Must** use secure database in production

### 🟡 تحذيرات / Warnings

1. **كلمات المرور المشفرة / Hardcoded Passwords**
   - كلمات المرور الافتراضية في index.html
   - Default passwords in index.html
   - **يجب** تغييرها أو استخدام نظام مصادقة حقيقي
   - **Must** change them or use real authentication system

2. **وضع التصحيح / Debug Mode**
   - Flask debug mode مفعّل في app.py و main.py
   - Flask debug mode enabled in app.py and main.py
   - **يجب** تعطيله في الإنتاج
   - **Must** disable in production

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
