# إعداد GitHub Actions لنشر Docker Hub
# Setting up GitHub Actions for Docker Hub Publishing

هذا الدليل يشرح كيفية إعداد GitHub Actions للنشر التلقائي على Docker Hub.

This guide explains how to set up GitHub Actions for automatic publishing to Docker Hub.

---

## 📋 الخطوات / Steps

### 1. إنشاء Docker Hub Access Token / Create Docker Hub Access Token

1. سجل الدخول إلى Docker Hub / Login to Docker Hub:
   ```
   https://hub.docker.com/settings/security
   ```

2. اذهب إلى "Security" / Go to "Security"

3. اضغط على "New Access Token" / Click "New Access Token"

4. املأ المعلومات / Fill in the information:
   - **Description**: GitHub Actions Token
   - **Access permissions**: Read, Write, Delete
   
5. احفظ الـ Token (لن تتمكن من رؤيته مرة أخرى!)
   Save the token (you won't be able to see it again!)

---

### 2. إضافة Secret في GitHub / Add Secret in GitHub

1. اذهب إلى المستودع في GitHub / Go to repository on GitHub:
   ```
   https://github.com/Ali5829511/2025
   ```

2. اذهب إلى Settings > Secrets and variables > Actions
   Go to Settings > Secrets and variables > Actions

3. اضغط على "New repository secret" / Click "New repository secret"

4. أضف Secret جديد / Add new secret:
   - **Name**: `DOCKER_HUB_TOKEN`
   - **Value**: [Token الذي حصلت عليه من الخطوة 1]
   
5. اضغط "Add secret" / Click "Add secret"

---

### 3. التحقق من اسم المستخدم / Verify Username

تأكد من أن اسم المستخدم في الـ workflow صحيح:
Make sure the username in the workflow is correct:

```yaml
# في ملف .github/workflows/docker-publish.yml
# In file .github/workflows/docker-publish.yml
env:
  DOCKER_HUB_USERNAME: ali517  # تأكد من أن هذا هو اسمك الصحيح / Make sure this is your correct username
```

---

### 4. تفعيل GitHub Actions / Enable GitHub Actions

1. اذهب إلى تبويب "Actions" في المستودع
   Go to "Actions" tab in the repository

2. إذا كانت الـ Actions معطلة، اضغط "I understand my workflows, go ahead and enable them"
   If Actions are disabled, click "I understand my workflows, go ahead and enable them"

---

### 5. اختبار Workflow / Test Workflow

#### تشغيل يدوي / Manual Trigger:

1. اذهب إلى Actions > Build and Push Docker Image
   Go to Actions > Build and Push Docker Image

2. اضغط "Run workflow" / Click "Run workflow"

3. اختر branch (main) واضغط "Run workflow"
   Select branch (main) and click "Run workflow"

#### Push تلقائي / Automatic Push:

```bash
# أي push إلى main سيشغل الـ workflow
# Any push to main will trigger the workflow
git add .
git commit -m "Update Docker configuration"
git push origin main
```

#### نشر إصدار / Release Version:

```bash
# إنشاء tag سيشغل الـ workflow وينشئ إصدار
# Creating a tag will trigger the workflow and create a release
git tag -a v2.0.2 -m "Release version 2.0.2"
git push origin v2.0.2
```

---

## ✅ التحقق من النشر / Verify Publishing

### 1. التحقق في GitHub Actions / Check in GitHub Actions

```
https://github.com/Ali5829511/2025/actions
```

ابحث عن:
Look for:
- ✅ Build successful
- ✅ Push successful
- ✅ Security scan completed

### 2. التحقق في Docker Hub / Check in Docker Hub

```
https://hub.docker.com/r/ali517/housing-management
```

يجب أن ترى:
You should see:
- الصورة المنشورة / Published image
- Tags مختلفة / Different tags
- آخر تحديث / Last updated
- عدد السحبات / Pull count

### 3. اختبار السحب / Test Pulling

```bash
# سحب الصورة / Pull the image
docker pull ali517/housing-management:latest

# التحقق من الصورة / Verify image
docker images ali517/housing-management

# تشغيل / Run
docker run -d -p 8000:8000 ali517/housing-management:latest

# اختبار / Test
curl http://localhost:8000
```

---

## 🔧 استكشاف الأخطاء / Troubleshooting

### المشكلة: authentication failed / Problem: authentication failed

**الحل / Solution:**
1. تحقق من صحة الـ Token / Verify token is correct
2. تحقق من اسم Secret في GitHub (`DOCKER_HUB_TOKEN`)
3. تحقق من أن Token لم ينتهِ صلاحيته / Verify token hasn't expired
4. حاول إنشاء Token جديد / Try creating a new token

### المشكلة: push failed / Problem: push failed

**الحل / Solution:**
1. تحقق من أن لديك صلاحيات Write في Docker Hub
2. تحقق من أن Repository موجود أو يمكن إنشاؤه
3. تحقق من اسم المستخدم في workflow

### المشكلة: build failed / Problem: build failed

**الحل / Solution:**
1. تحقق من Dockerfile
2. تحقق من السجلات في GitHub Actions
3. جرب البناء محلياً أولاً / Try building locally first:
   ```bash
   docker build -t test-build .
   ```

---

## 📊 مراقبة الـ Workflow / Monitor Workflow

### عرض السجلات / View Logs

1. اذهب إلى Actions في GitHub / Go to Actions in GitHub
2. اضغط على آخر workflow run
3. اضغط على "build-and-push" job
4. انظر السجلات التفصيلية / View detailed logs

### البريد الإلكتروني / Email Notifications

GitHub سيرسل بريد إلكتروني إذا فشل الـ workflow
GitHub will send email if workflow fails

يمكنك تعطيل أو تفعيل هذا من:
You can disable or enable this from:
```
Settings > Notifications > Actions
```

---

## 🔒 أفضل الممارسات الأمنية / Security Best Practices

### 1. استخدم Tokens بدلاً من كلمات المرور
### Use Tokens Instead of Passwords

✅ استخدم Access Token (صحيح) / Use Access Token (correct)  
❌ لا تستخدم كلمة المرور مباشرة / Don't use password directly

### 2. صلاحيات محدودة
### Limited Permissions

أعط Token أقل صلاحيات ممكنة:
Give token minimum required permissions:
- Read: للسحب / For pulling
- Write: للنشر / For pushing
- Delete: فقط إذا لزم / Only if needed

### 3. تدوير Tokens
### Rotate Tokens

قم بتجديد Tokens بشكل دوري (كل 6-12 شهر)
Rotate tokens periodically (every 6-12 months)

### 4. مراقبة النشاط
### Monitor Activity

راقب نشاط النشر في Docker Hub:
Monitor publishing activity in Docker Hub:
```
https://hub.docker.com/settings/security
```

---

## 📚 موارد إضافية / Additional Resources

### الوثائق الرسمية / Official Documentation
- [GitHub Actions](https://docs.github.com/en/actions)
- [Docker Hub](https://docs.docker.com/docker-hub/)
- [Docker Build Push Action](https://github.com/docker/build-push-action)

### أدلة إضافية / Additional Guides
- [DOCKER_HUB_GUIDE.md](DOCKER_HUB_GUIDE.md) - دليل Docker Hub الكامل
- [النشر_باستخدام_Docker.md](النشر_باستخدام_Docker.md) - دليل النشر

---

## ✅ قائمة التحقق / Checklist

قبل البدء:
Before starting:

- [ ] لديك حساب Docker Hub / Have Docker Hub account
- [ ] أنشأت Access Token / Created Access Token
- [ ] أضفت DOCKER_HUB_TOKEN في GitHub Secrets
- [ ] تحققت من اسم المستخدم في workflow
- [ ] فعّلت GitHub Actions
- [ ] اختبرت البناء محلياً / Tested build locally

---

**تم إنشاؤه بواسطة / Created by:** فريق التطوير / Development Team  
**آخر تحديث / Last Updated:** نوفمبر 2025 / November 2025

**جامعة الإمام محمد بن سعود الإسلامية © 2025**
