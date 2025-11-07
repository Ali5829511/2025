# 🐳 مرجع سريع لأوامر Docker Hub
# Docker Hub Quick Reference

مرجع سريع لأهم الأوامر المستخدمة مع Docker Hub.

Quick reference for the most important Docker Hub commands.

---

## 🔑 التسجيل / Login

```bash
# تسجيل الدخول / Login
docker login

# تسجيل الدخول بمستخدم محدد / Login with specific user
docker login -u ali517

# تسجيل الخروج / Logout
docker logout
```

---

## 🏗️ البناء / Build

```bash
# بناء أساسي / Basic build
docker build -t ali517/housing-management:latest .

# بناء مع tag محدد / Build with specific tag
docker build -t ali517/housing-management:v2.0.1 .

# بناء متعدد العلامات / Build with multiple tags
docker build \
  -t ali517/housing-management:latest \
  -t ali517/housing-management:v2.0.1 \
  -t ali517/housing-management:stable \
  .

# بناء بدون cache / Build without cache
docker build --no-cache -t ali517/housing-management:latest .
```

---

## 🏷️ العلامات / Tags

```bash
# إضافة علامة / Add tag
docker tag ali517/housing-management:latest ali517/housing-management:v2.0.1

# إضافة علامات متعددة / Add multiple tags
docker tag ali517/housing-management:latest ali517/housing-management:stable
docker tag ali517/housing-management:latest ali517/housing-management:production
```

---

## 📤 النشر / Push

```bash
# نشر صورة / Push image
docker push ali517/housing-management:latest

# نشر tag محدد / Push specific tag
docker push ali517/housing-management:v2.0.1

# نشر جميع العلامات / Push all tags
docker push ali517/housing-management --all-tags
```

---

## 📥 السحب / Pull

```bash
# سحب آخر إصدار / Pull latest
docker pull ali517/housing-management:latest

# سحب إصدار محدد / Pull specific version
docker pull ali517/housing-management:v2.0.1

# سحب على منصة محددة / Pull for specific platform
docker pull --platform linux/amd64 ali517/housing-management:latest
```

---

## 🔍 المعلومات / Information

```bash
# عرض الصور المحلية / Show local images
docker images ali517/housing-management

# عرض معلومات الصورة / Show image info
docker inspect ali517/housing-management:latest

# عرض history الصورة / Show image history
docker history ali517/housing-management:latest

# عرض manifest / Show manifest
docker manifest inspect ali517/housing-management:latest
```

---

## 🗑️ الحذف / Delete

```bash
# حذف صورة محلية / Delete local image
docker rmi ali517/housing-management:latest

# حذف جميع الصور المحلية / Delete all local images
docker rmi $(docker images ali517/housing-management -q)

# حذف من Docker Hub / Delete from Docker Hub
# يجب استخدام واجهة الويب / Must use web interface
# https://hub.docker.com/r/ali517/housing-management
```

---

## 🚀 التشغيل / Run

```bash
# تشغيل أساسي / Basic run
docker run -d -p 8000:8000 ali517/housing-management:latest

# تشغيل مع متغيرات بيئة / Run with environment variables
docker run -d \
  -p 8000:8000 \
  -e FLASK_ENV=production \
  -e DATABASE_TYPE=postgresql \
  ali517/housing-management:latest

# تشغيل مع volumes / Run with volumes
docker run -d \
  -p 8000:8000 \
  -v housing_data:/app/data \
  --name housing-system \
  ali517/housing-management:latest

# تشغيل مع docker-compose / Run with docker-compose
docker-compose -f docker-compose.hub.yml up -d
```

---

## 🔄 التحديث / Update

```bash
# سحب التحديث / Pull update
docker pull ali517/housing-management:latest

# إيقاف الحاوية القديمة / Stop old container
docker stop housing-system

# حذف الحاوية القديمة / Remove old container
docker rm housing-system

# تشغيل الجديدة / Start new
docker run -d \
  -p 8000:8000 \
  --name housing-system \
  ali517/housing-management:latest

# أو استخدام docker-compose / Or use docker-compose
docker-compose -f docker-compose.hub.yml pull
docker-compose -f docker-compose.hub.yml up -d
```

---

## 🔒 الأمان / Security

```bash
# فحص الثغرات مع Docker Scout / Scan with Docker Scout
docker scout cves ali517/housing-management:latest

# فحص مع Trivy / Scan with Trivy
trivy image ali517/housing-management:latest

# تفعيل Content Trust / Enable Content Trust
export DOCKER_CONTENT_TRUST=1
docker push ali517/housing-management:latest
```

---

## 📊 المراقبة / Monitoring

```bash
# عرض الحاويات قيد التشغيل / Show running containers
docker ps

# عرض استخدام الموارد / Show resource usage
docker stats

# عرض السجلات / Show logs
docker logs housing-system

# متابعة السجلات / Follow logs
docker logs -f housing-system

# عرض آخر 100 سطر / Show last 100 lines
docker logs --tail 100 housing-system
```

---

## 🧹 التنظيف / Cleanup

```bash
# حذف الصور غير المستخدمة / Remove unused images
docker image prune

# حذف كل شيء غير مستخدم / Remove all unused
docker system prune -a

# حذف volumes غير مستخدمة / Remove unused volumes
docker volume prune

# حذف كل شيء (خطر!) / Remove everything (dangerous!)
docker system prune -a --volumes
```

---

## 📋 Workflow كامل / Complete Workflow

### للمطورين / For Developers

```bash
# 1. تسجيل الدخول / Login
docker login

# 2. بناء الصورة / Build image
docker build -t ali517/housing-management:latest .

# 3. اختبار محلياً / Test locally
docker run -d -p 8000:8000 ali517/housing-management:latest
curl http://localhost:8000

# 4. إضافة علامات / Add tags
docker tag ali517/housing-management:latest ali517/housing-management:v2.0.2

# 5. نشر / Push
docker push ali517/housing-management --all-tags

# 6. التحقق / Verify
docker pull ali517/housing-management:latest
```

### للمستخدمين / For Users

```bash
# 1. سحب الصورة / Pull image
docker pull ali517/housing-management:latest

# 2. إنشاء docker-compose.yml / Create docker-compose.yml
curl -O https://raw.githubusercontent.com/Ali5829511/2025/main/docker-compose.hub.yml

# 3. تشغيل / Start
docker-compose -f docker-compose.hub.yml up -d

# 4. التحقق / Verify
docker-compose ps
curl http://localhost

# 5. المراقبة / Monitor
docker-compose logs -f
```

---

## 🆘 حل المشاكل / Troubleshooting

### لا يمكن تسجيل الدخول / Cannot Login
```bash
# حذف المصادقة القديمة / Remove old credentials
rm ~/.docker/config.json
docker login
```

### فشل النشر / Push Failed
```bash
# التحقق من المصادقة / Check authentication
docker login

# التحقق من اسم الصورة / Check image name
docker images | grep ali517

# إعادة المحاولة / Retry
docker push ali517/housing-management:latest
```

### الصورة قديمة / Image is Old
```bash
# حذف الصورة المحلية / Remove local image
docker rmi ali517/housing-management:latest

# سحب جديدة / Pull fresh
docker pull ali517/housing-management:latest

# أو بدون cache / Or no cache
docker pull --no-cache ali517/housing-management:latest
```

---

## 📱 الوصول السريع / Quick Access

### واجهة الويب / Web Interface
- **Repository**: https://hub.docker.com/r/ali517/housing-management
- **Account**: https://app.docker.com/accounts/ali517
- **Settings**: https://hub.docker.com/settings/security

### سطر الأوامر / Command Line
```bash
# فتح صفحة Repository / Open repository page
xdg-open https://hub.docker.com/r/ali517/housing-management

# أو على Mac / Or on Mac
open https://hub.docker.com/r/ali517/housing-management
```

---

## 📚 موارد إضافية / Additional Resources

- [DOCKER_HUB_GUIDE.md](DOCKER_HUB_GUIDE.md) - دليل شامل
- [GITHUB_ACTIONS_SETUP.md](GITHUB_ACTIONS_SETUP.md) - إعداد النشر التلقائي
- [النشر_باستخدام_Docker.md](النشر_باستخدام_Docker.md) - دليل النشر
- [Docker Documentation](https://docs.docker.com/)

---

**ملاحظة:** استبدل `ali517` باسم المستخدم الخاص بك إذا كان مختلفاً.  
**Note:** Replace `ali517` with your username if different.

---

**تم إنشاؤه بواسطة / Created by:** فريق التطوير / Development Team  
**آخر تحديث / Last Updated:** نوفمبر 2025 / November 2025

**جامعة الإمام محمد بن سعود الإسلامية © 2025**
