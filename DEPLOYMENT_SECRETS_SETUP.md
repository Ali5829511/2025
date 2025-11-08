# Deployment Secrets Setup Guide
# دليل إعداد أسرار النشر

This guide explains how to configure GitHub secrets for automated deployment workflows.

يشرح هذا الدليل كيفية تكوين أسرار GitHub لسير عمل النشر التلقائي.

---

## Overview / نظرة عامة

The repository uses GitHub Actions for automated deployments to:
- **Docker Hub**: For container image publishing
- **Fly.io**: For application hosting

يستخدم المستودع GitHub Actions للنشر التلقائي إلى:
- **Docker Hub**: لنشر صور الحاويات
- **Fly.io**: لاستضافة التطبيق

Both workflows require secrets to be configured in the repository settings.

يتطلب كلا سير العمل تكوين الأسرار في إعدادات المستودع.

---

## Required Secrets / الأسرار المطلوبة

### 1. Docker Hub Token

**Purpose / الغرض:**
Allows GitHub Actions to publish Docker images to Docker Hub.

يسمح لـ GitHub Actions بنشر صور Docker إلى Docker Hub.

**Steps to Create / خطوات الإنشاء:**

1. **Login to Docker Hub / تسجيل الدخول إلى Docker Hub:**
   - Visit: https://hub.docker.com
   - Sign in with your Docker Hub account / سجل الدخول بحساب Docker Hub الخاص بك

2. **Create Access Token / إنشاء رمز الوصول:**
   - Go to: Account Settings → Security → Access Tokens
   - انتقل إلى: إعدادات الحساب ← الأمان ← رموز الوصول
   - Click "New Access Token" / انقر على "رمز وصول جديد"
   - Name: `GitHub Actions` or similar / الاسم: `GitHub Actions` أو ما شابه
   - Permissions: Read & Write / الأذونات: قراءة وكتابة
   - Click "Generate" / انقر على "إنشاء"
   - **Important**: Copy the token immediately (you won't see it again!)
   - **مهم**: انسخ الرمز فوراً (لن تتمكن من رؤيته مرة أخرى!)

3. **Add to GitHub / إضافة إلى GitHub:**
   - Go to your repository on GitHub / انتقل إلى مستودعك على GitHub
   - Navigate to: Settings → Secrets and variables → Actions
   - انتقل إلى: الإعدادات ← الأسرار والمتغيرات ← الإجراءات
   - Click "New repository secret" / انقر على "سر مستودع جديد"
   - Name: `DOCKER_HUB_TOKEN` / الاسم: `DOCKER_HUB_TOKEN`
   - Value: Paste the token you copied / القيمة: الصق الرمز الذي نسخته
   - Click "Add secret" / انقر على "إضافة سر"

**Direct Link / الرابط المباشر:**
```
https://github.com/Ali5829511/2025/settings/secrets/actions/new
```

---

### 2. Fly.io API Token

**Purpose / الغرض:**
Allows GitHub Actions to deploy the application to Fly.io.

يسمح لـ GitHub Actions بنشر التطبيق إلى Fly.io.

**Steps to Create / خطوات الإنشاء:**

1. **Login to Fly.io / تسجيل الدخول إلى Fly.io:**
   - Visit: https://fly.io/dashboard
   - Sign in with your Fly.io account / سجل الدخول بحساب Fly.io الخاص بك

2. **Create API Token / إنشاء رمز API:**
   - Go to: https://fly.io/dashboard/personal/tokens
   - انتقل إلى: https://fly.io/dashboard/personal/tokens
   - Click "Create Deploy Token" or "New Access Token"
   - انقر على "إنشاء رمز النشر" أو "رمز وصول جديد"
   - Name: `GitHub Actions` or similar / الاسم: `GitHub Actions` أو ما شابه
   - Click "Create" / انقر على "إنشاء"
   - **Important**: Copy the token immediately!
   - **مهم**: انسخ الرمز فوراً!

   **Alternative using CLI / البديل باستخدام سطر الأوامر:**
   ```bash
   # Install flyctl if not already installed
   # ثبت flyctl إذا لم يكن مثبتاً
   
   # Login
   flyctl auth login
   
   # Create token
   flyctl tokens create deploy
   ```

3. **Add to GitHub / إضافة إلى GitHub:**
   - Go to your repository on GitHub / انتقل إلى مستودعك على GitHub
   - Navigate to: Settings → Secrets and variables → Actions
   - انتقل إلى: الإعدادات ← الأسرار والمتغيرات ← الإجراءات
   - Click "New repository secret" / انقر على "سر مستودع جديد"
   - Name: `FLY_API_TOKEN` / الاسم: `FLY_API_TOKEN`
   - Value: Paste the token you copied / القيمة: الصق الرمز الذي نسخته
   - Click "Add secret" / انقر على "إضافة سر"

**Direct Link / الرابط المباشر:**
```
https://github.com/Ali5829511/2025/settings/secrets/actions/new
```

---

## Verification / التحقق

After adding the secrets, you can verify they're working:

بعد إضافة الأسرار، يمكنك التحقق من أنها تعمل:

### For Docker Hub / لـ Docker Hub:
1. Make a commit and push to `main` branch
   قم بعمل commit ودفعه إلى فرع `main`
2. Check the "Build and Push Docker Image" workflow
   تحقق من سير عمل "Build and Push Docker Image"
3. If successful, your image will appear at: https://hub.docker.com/r/ali517/housing-management
   إذا نجح، ستظهر صورتك في: https://hub.docker.com/r/ali517/housing-management

### For Fly.io / لـ Fly.io:
1. Make a commit and push to `main` branch
   قم بعمل commit ودفعه إلى فرع `main`
2. Check the "Deploy to Fly.io" workflow
   تحقق من سير عمل "Deploy to Fly.io"
3. If successful, visit: https://housing-management-system.fly.dev
   إذا نجح، زر: https://housing-management-system.fly.dev

---

## Troubleshooting / استكشاف الأخطاء

### Docker Hub Issues / مشاكل Docker Hub:

**Error: "Password required"**
- **Problem**: `DOCKER_HUB_TOKEN` secret is not set or incorrect
- **Solution**: Follow steps above to create and add the token
- **المشكلة**: لم يتم تعيين سر `DOCKER_HUB_TOKEN` أو أنه غير صحيح
- **الحل**: اتبع الخطوات أعلاه لإنشاء وإضافة الرمز

**Error: "unauthorized: incorrect username or password"**
- **Problem**: Token is expired or invalid
- **Solution**: Generate a new token and update the secret
- **المشكلة**: الرمز منتهي الصلاحية أو غير صالح
- **الحل**: أنشئ رمزاً جديداً وحدّث السر

### Fly.io Issues / مشاكل Fly.io:

**Error: "No access token available"**
- **Problem**: `FLY_API_TOKEN` secret is not set
- **Solution**: Follow steps above to create and add the token
- **المشكلة**: لم يتم تعيين سر `FLY_API_TOKEN`
- **الحل**: اتبع الخطوات أعلاه لإنشاء وإضافة الرمز

**Error: "Could not find App"**
- **Problem**: The Fly.io app doesn't exist
- **Solution**: Create the app first using `flyctl launch` or update the app name in the workflow
- **المشكلة**: تطبيق Fly.io غير موجود
- **الحل**: أنشئ التطبيق أولاً باستخدام `flyctl launch` أو حدّث اسم التطبيق في سير العمل

---

## Security Best Practices / أفضل الممارسات الأمنية

1. **Never commit secrets to the repository**
   لا تضف الأسرار أبداً إلى المستودع

2. **Use tokens with minimum required permissions**
   استخدم الرموز بأقل الأذونات المطلوبة

3. **Rotate tokens regularly** (every 3-6 months)
   قم بتدوير الرموز بانتظام (كل 3-6 أشهر)

4. **Delete tokens that are no longer needed**
   احذف الرموز التي لم تعد بحاجة إليها

5. **Use different tokens for different environments** (if applicable)
   استخدم رموزاً مختلفة لبيئات مختلفة (إن أمكن)

---

## What Happens Without Secrets? / ماذا يحدث بدون الأسرار؟

The workflows are now designed to handle missing secrets gracefully:

أصبح سير العمل مصمماً للتعامل مع الأسرار المفقودة بشكل صحيح:

- **Docker workflow**: Builds the image but doesn't push to Docker Hub
  - **سير عمل Docker**: يبني الصورة لكن لا ينشرها إلى Docker Hub

- **Fly.io workflow**: Skips deployment entirely with a clear message
  - **سير عمل Fly.io**: يتخطى النشر كلياً مع رسالة واضحة

Both workflows will show warning messages with instructions on how to configure the secrets.

سيعرض كلا سير العمل رسائل تحذير مع تعليمات حول كيفية تكوين الأسرار.

---

## Additional Resources / موارد إضافية

- [GitHub Secrets Documentation](https://docs.github.com/en/actions/security-guides/encrypted-secrets)
- [Docker Hub Access Tokens](https://docs.docker.com/docker-hub/access-tokens/)
- [Fly.io Tokens](https://fly.io/docs/reference/deploy-tokens/)

---

## Support / الدعم

If you encounter issues:
1. Check the workflow logs in the Actions tab
2. Review the error messages carefully
3. Consult the documentation linked above

إذا واجهت مشاكل:
1. تحقق من سجلات سير العمل في تبويب Actions
2. راجع رسائل الخطأ بعناية
3. استشر الوثائق المرتبطة أعلاه
