# 🐳 دليل نشر الصور على Docker Hub
# Docker Hub Publishing Guide

دليل شامل لنشر صور Docker للنظام على Docker Hub لتسهيل النشر والتوزيع.

A comprehensive guide for publishing Docker images of the system to Docker Hub for easier deployment and distribution.

---

## 📋 نظرة عامة / Overview

هذا الدليل يشرح كيفية:
- إنشاء حساب Docker Hub
- بناء ونشر صور Docker للنظام
- استخدام الصور المنشورة في النشر

This guide explains how to:
- Create a Docker Hub account
- Build and publish Docker images for the system
- Use published images in deployment

---

## 🔑 إنشاء حساب Docker Hub / Create Docker Hub Account

### الخطوة 1: التسجيل / Sign Up

1. افتح الرابط / Open: https://hub.docker.com/signup
2. أنشئ حساب جديد بالمعلومات التالية / Create a new account with:
   - **Username**: ali517 (أو أي اسم تفضله / or any preferred username)
   - **Email**: بريدك الإلكتروني / Your email
   - **Password**: كلمة مرور قوية / Strong password

3. تحقق من بريدك الإلكتروني / Verify your email

### الخطوة 2: تسجيل الدخول / Login

بعد إنشاء الحساب، يمكنك الوصول إلى لوحة التحكم:
After creating the account, you can access your dashboard at:

```
https://app.docker.com/
```

أو حسابك المحدد / Or your specific account:
```
https://app.docker.com/accounts/ali517
```

---

## 🚀 بناء ونشر الصور / Build and Publish Images

### المتطلبات المسبقة / Prerequisites

```bash
# التأكد من تثبيت Docker / Ensure Docker is installed
docker --version

# تسجيل الدخول إلى Docker Hub / Login to Docker Hub
docker login

# أدخل اسم المستخدم وكلمة المرور / Enter username and password
Username: ali517
Password: ********
```

---

## 📦 بناء صورة النظام / Build System Image

### الطريقة 1: البناء المباشر / Direct Build

```bash
# الانتقال إلى مجلد المشروع / Navigate to project directory
cd /path/to/2025

# بناء الصورة / Build the image
docker build -t ali517/housing-management:latest .

# إضافة علامات إضافية / Add additional tags
docker tag ali517/housing-management:latest ali517/housing-management:v2.0.1
docker tag ali517/housing-management:latest ali517/housing-management:stable
```

### الطريقة 2: البناء مع معلومات إضافية / Build with Additional Info

```bash
# بناء مع معلومات البناء / Build with build info
docker build \
  --label "org.opencontainers.image.title=Faculty Housing Management System" \
  --label "org.opencontainers.image.description=نظام إدارة إسكان أعضاء هيئة التدريس" \
  --label "org.opencontainers.image.version=2.0.1" \
  --label "org.opencontainers.image.authors=جامعة الإمام محمد بن سعود الإسلامية" \
  --label "org.opencontainers.image.url=https://github.com/Ali5829511/2025" \
  -t ali517/housing-management:latest \
  -t ali517/housing-management:v2.0.1 \
  .
```

---

## 📤 نشر الصور / Push Images

### نشر جميع العلامات / Push All Tags

```bash
# نشر الصورة الأساسية / Push main image
docker push ali517/housing-management:latest

# نشر الإصدارات المحددة / Push specific versions
docker push ali517/housing-management:v2.0.1
docker push ali517/housing-management:stable
```

### نشر جميع العلامات مرة واحدة / Push All Tags at Once

```bash
# نشر جميع العلامات / Push all tags
docker push ali517/housing-management --all-tags
```

---

## 🎯 استخدام الصور المنشورة / Using Published Images

### تحديث docker-compose.yml / Update docker-compose.yml

بدلاً من بناء الصورة محلياً، استخدم الصورة المنشورة:
Instead of building locally, use the published image:

```yaml
services:
  web:
    # استخدم الصورة المنشورة بدلاً من البناء المحلي
    # Use published image instead of local build
    image: ali517/housing-management:latest
    # أو إصدار محدد / Or specific version
    # image: ali517/housing-management:v2.0.1
    
    # احذف أو علق على سطور البناء / Remove or comment out build lines
    # build:
    #   context: .
    #   dockerfile: Dockerfile
    
    container_name: housing_web
    restart: always
    environment:
      - FLASK_APP=server.py
      - FLASK_ENV=production
      - FLASK_DEBUG=False
      - DATABASE_TYPE=postgresql
      - DATABASE_HOST=db
      - DATABASE_PORT=5432
      - DATABASE_NAME=housing_db
      - DATABASE_USER=housing_user
      - DATABASE_PASSWORD=${DB_PASSWORD:-ChangeThisPassword123!}
      - SECRET_KEY=${SECRET_KEY:-generate-a-strong-secret-key-here}
    ports:
      - "8000:8000"
    depends_on:
      db:
        condition: service_healthy
    networks:
      - housing_network
```

### النشر السريع / Quick Deployment

```bash
# سحب الصورة / Pull the image
docker pull ali517/housing-management:latest

# تشغيل مع docker-compose / Run with docker-compose
docker-compose up -d

# أو تشغيل مباشر / Or direct run
docker run -d \
  --name housing_web \
  -p 8000:8000 \
  -e FLASK_ENV=production \
  -e FLASK_DEBUG=False \
  ali517/housing-management:latest
```

---

## 🔄 التحديث التلقائي / Automated Updates

### إنشاء سكريبت تحديث / Create Update Script

```bash
# إنشاء ملف update.sh / Create update.sh file
cat > update.sh <<'EOF'
#!/bin/bash
set -e

echo "🔄 جاري تحديث النظام / Updating system..."

# سحب آخر صورة / Pull latest image
echo "📥 سحب الصورة الجديدة / Pulling new image..."
docker pull ali517/housing-management:latest

# إيقاف الخدمات الحالية / Stop current services
echo "🛑 إيقاف الخدمات / Stopping services..."
docker-compose down

# تشغيل بالصورة الجديدة / Start with new image
echo "🚀 تشغيل الصورة الجديدة / Starting new image..."
docker-compose up -d

# التحقق من الحالة / Check status
echo "✅ التحقق من الحالة / Checking status..."
sleep 5
docker-compose ps

echo "✅ تم التحديث بنجاح! / Update completed successfully!"
EOF

chmod +x update.sh
```

### جدولة التحديث التلقائي / Schedule Automatic Updates

```bash
# إضافة إلى crontab للتحديث الأسبوعي / Add to crontab for weekly update
crontab -e

# أضف السطر التالي للتحديث كل أحد الساعة 3 صباحاً
# Add the following line for weekly update every Sunday at 3 AM
0 3 * * 0 cd /path/to/2025 && ./update.sh >> /var/log/housing-update.log 2>&1
```

---

## 🏷️ إدارة الإصدارات / Version Management

### استراتيجية العلامات / Tagging Strategy

```bash
# إصدار أحدث دائماً / Always latest
ali517/housing-management:latest

# إصدارات محددة / Specific versions
ali517/housing-management:v2.0.1
ali517/housing-management:v2.0.0
ali517/housing-management:v1.0.0

# قنوات النشر / Release channels
ali517/housing-management:stable    # للإنتاج / For production
ali517/housing-management:beta      # للاختبار / For testing
ali517/housing-management:dev       # للتطوير / For development
```

### نشر إصدار جديد / Publish New Version

```bash
# بناء الإصدار الجديد / Build new version
VERSION="2.0.2"
docker build -t ali517/housing-management:latest .
docker tag ali517/housing-management:latest ali517/housing-management:v$VERSION
docker tag ali517/housing-management:latest ali517/housing-management:stable

# نشر جميع العلامات / Push all tags
docker push ali517/housing-management:latest
docker push ali517/housing-management:v$VERSION
docker push ali517/housing-management:stable
```

---

## 🔐 الأمان / Security

### استخدام Docker Content Trust / Using Docker Content Trust

```bash
# تفعيل التوقيع الرقمي / Enable digital signing
export DOCKER_CONTENT_TRUST=1

# بناء ونشر مع التوقيع / Build and push with signing
docker build -t ali517/housing-management:latest .
docker push ali517/housing-management:latest
```

### فحص الثغرات / Vulnerability Scanning

```bash
# فحص الصورة قبل النشر / Scan image before publishing
docker scan ali517/housing-management:latest

# أو استخدم Trivy / Or use Trivy
trivy image ali517/housing-management:latest
```

---

## 📊 المراقبة والإحصائيات / Monitoring and Statistics

### عرض معلومات الصورة / View Image Information

```bash
# معلومات الصورة المحلية / Local image info
docker images ali517/housing-management

# معلومات الصورة من Hub / Hub image info
docker manifest inspect ali517/housing-management:latest

# السجل / History
docker history ali517/housing-management:latest
```

### إحصائيات Docker Hub / Docker Hub Statistics

قم بزيارة لوحة التحكم لمشاهدة:
Visit the dashboard to view:

- عدد مرات السحب / Pull count
- عدد النجوم / Star count
- آخر تحديث / Last update
- حجم الصورة / Image size

```
https://hub.docker.com/r/ali517/housing-management
```

---

## 🛠️ نصائح وأفضل الممارسات / Tips and Best Practices

### 1. تقليل حجم الصورة / Reduce Image Size

```dockerfile
# استخدم صور alpine الخفيفة / Use lightweight alpine images
FROM python:3.11-alpine

# استخدم multi-stage builds / Use multi-stage builds
FROM python:3.11 AS builder
# ... بناء التطبيق / Build application
FROM python:3.11-slim
# ... نسخ الملفات الضرورية فقط / Copy only necessary files
```

### 2. استخدام .dockerignore / Use .dockerignore

```bash
# إنشاء ملف .dockerignore / Create .dockerignore file
cat > .dockerignore <<'EOF'
.git
.github
.gitignore
*.md
*.pyc
__pycache__
venv/
.env
housing.db
*.log
EOF
```

### 3. إعداد CI/CD / Setup CI/CD

راجع دليل GitHub Actions المرفق لإعداد النشر التلقائي.
See the included GitHub Actions guide for automatic publishing setup.

---

## 🔗 روابط مفيدة / Useful Links

### الوثائق الرسمية / Official Documentation
- [Docker Hub Documentation](https://docs.docker.com/docker-hub/)
- [Docker Build Reference](https://docs.docker.com/engine/reference/builder/)
- [Docker Compose Reference](https://docs.docker.com/compose/compose-file/)

### حسابات Docker Hub / Docker Hub Accounts
- **Dashboard**: https://app.docker.com/
- **Account**: https://app.docker.com/accounts/ali517
- **Repository**: https://hub.docker.com/r/ali517/housing-management

### الوثائق المحلية / Local Documentation
- [دليل Docker المحلي](النشر_باستخدام_Docker.md)
- [دليل النشر الكامل](دليل_النشر_الكامل.md)
- [دليل البدء السريع](QUICK_START.md)

---

## ❓ الأسئلة الشائعة / FAQ

### س: كم عدد الصور التي يمكن نشرها مجاناً؟
**Q: How many images can I publish for free?**

ج: يوفر Docker Hub حسابات مجانية مع:
A: Docker Hub offers free accounts with:
- مستودع واحد خاص / One private repository
- مستودعات عامة غير محدودة / Unlimited public repositories
- 100 سحب للصور كل 6 ساعات / 100 pulls every 6 hours

### س: كيف أحذف صورة قديمة؟
**Q: How do I delete an old image?**

ج: من لوحة التحكم:
A: From the dashboard:
1. اذهب إلى المستودع / Go to the repository
2. اختر "Tags"
3. حدد العلامة المراد حذفها / Select the tag to delete
4. اضغط "Delete" / Click "Delete"

### س: هل يمكن جعل المستودع خاصاً؟
**Q: Can I make the repository private?**

ج: نعم، في إعدادات المستودع اختر "Settings" > "Make Private"
A: Yes, in repository settings choose "Settings" > "Make Private"

---

## 📞 الدعم / Support

للحصول على المساعدة:
For assistance:

- 📖 راجع [الوثائق الرسمية](https://docs.docker.com/)
- 💬 [منتدى Docker](https://forums.docker.com/)
- 📧 تواصل مع فريق تقنية المعلومات / Contact IT team

---

## ✅ قائمة التحقق / Checklist

قبل النشر على Docker Hub:
Before publishing to Docker Hub:

- [ ] تم إنشاء حساب Docker Hub
- [ ] تم تسجيل الدخول محلياً (docker login)
- [ ] تم بناء الصورة واختبارها محلياً
- [ ] تم فحص الصورة للثغرات الأمنية
- [ ] تم إضافة العلامات المناسبة
- [ ] تم تحديث الوثائق
- [ ] تم اختبار السحب والنشر

---

**تم إنشاؤه بواسطة / Created by:** فريق التطوير / Development Team  
**آخر تحديث / Last Updated:** نوفمبر 2025 / November 2025  
**الإصدار / Version:** 2.0.1

**جامعة الإمام محمد بن سعود الإسلامية © 2025**
