# 🚀 دليل النشر على Fly.io
# Fly.io Deployment Guide

**الحالة / Status:** ✅ جاهز للنشر / Ready for Deployment  
**الوقت المطلوب / Time Required:** 10-15 دقيقة / minutes  
**التكلفة / Cost:** مجاني (مع حدود استخدام معقولة) / Free (with reasonable usage limits)

---

## 📋 نظرة عامة / Overview

Fly.io هي منصة حديثة لنشر التطبيقات على مستوى عالمي مع شبكة عالمية من مراكز البيانات. توفر Fly.io طبقة مجانية سخية مناسبة تماماً لنشر نظام إدارة الإسكان.

Fly.io is a modern platform for deploying applications globally with a worldwide network of data centers. Fly.io offers a generous free tier perfect for deploying the Housing Management System.

### ✨ مميزات Fly.io / Fly.io Features

- ✅ **طبقة مجانية سخية / Generous Free Tier:**
  - 3 آلات افتراضية مشتركة (Shared VMs)
  - 3 GB تخزين دائم / persistent storage
  - 160 GB نقل بيانات شهرياً / data transfer per month
  
- ✅ **نشر سريع / Fast Deployment:** نشر في أقل من دقيقة / Deploy in under a minute

- ✅ **SSL مجاني / Free SSL:** شهادات HTTPS تلقائية / Automatic HTTPS certificates

- ✅ **PostgreSQL مُدار / Managed PostgreSQL:** قاعدة بيانات مُدارة بالكامل / Fully managed database

- ✅ **شبكة عالمية / Global Network:** أكثر من 30 موقع حول العالم / 30+ locations worldwide

- ✅ **سهولة الاستخدام / Easy to Use:** واجهة سطر أوامر بسيطة / Simple CLI interface

- ✅ **Docker Native:** دعم كامل لـ Docker / Full Docker support

- ✅ **لا يتطلب بطاقة ائتمانية / No Credit Card Required:** للبدء بالطبقة المجانية / to start with free tier

---

## 🎯 المتطلبات / Requirements

1. **حساب GitHub / GitHub Account**
   - المشروع موجود على: https://github.com/Ali5829511/2025

2. **حساب Fly.io / Fly.io Account**
   - التسجيل: https://fly.io/app/sign-up
   - لا يتطلب بطاقة ائتمانية للبدء / No credit card required to start

3. **flyctl CLI (اختياري للنشر اليدوي) / flyctl CLI (optional for manual deployment)**
   - سيتم استخدام النشر عبر GitHub Actions / Will use GitHub Actions for deployment

---

## 📝 خطوات النشر / Deployment Steps

### الطريقة 1️⃣: النشر التلقائي عبر GitHub Actions (موصى به)

هذه الطريقة الأسهل - يتم النشر تلقائياً عند كل دفع للكود!

This is the easiest method - automatically deploys on every code push!

#### الخطوة 1: إنشاء حساب على Fly.io

1. اذهب إلى https://fly.io/app/sign-up
2. سجل باستخدام بريدك الإلكتروني أو حساب GitHub
3. أكمل عملية التحقق من البريد الإلكتروني
4. **لا تحتاج لإضافة بطاقة ائتمانية!**

#### الخطوة 2: الحصول على رمز API Token

1. بعد تسجيل الدخول، اذهب إلى: https://fly.io/user/personal_access_tokens
2. انقر على "Create token" أو "إنشاء رمز"
3. أدخل اسماً للرمز مثل: "GitHub Actions"
4. انقر على "Create"
5. **احفظ الرمز في مكان آمن - لن تتمكن من رؤيته مرة أخرى!**

#### الخطوة 3: إضافة الرمز إلى GitHub Secrets

1. اذهب إلى repository: https://github.com/Ali5829511/2025
2. انقر على "Settings" (الإعدادات)
3. في القائمة اليسرى، انقر على "Secrets and variables" ثم "Actions"
4. انقر على "New repository secret"
5. أضف secret جديد:
   - **Name:** `FLY_API_TOKEN`
   - **Value:** الصق الرمز الذي حصلت عليه من Fly.io
6. انقر على "Add secret"

#### الخطوة 4: إنشاء التطبيق على Fly.io (مرة واحدة فقط)

يمكنك إنشاء التطبيق بطريقتين:

**أ. عبر واجهة الويب (الأسهل):**

1. اذهب إلى: https://fly.io/dashboard
2. انقر على "Create an app" أو "إنشاء تطبيق"
3. اختر اسم التطبيق (أو اترك Fly.io يختار لك): `housing-management-system`
4. اختر المنطقة الأقرب لك:
   - `iad` - واشنطن، الولايات المتحدة
   - `lhr` - لندن، المملكة المتحدة
   - `cdg` - باريس، فرنسا
   - `fra` - فرانكفورت، ألمانيا
   - `sin` - سنغافورة
5. انقر على "Create app"

**ب. عبر flyctl CLI:**

```bash
# تثبيت flyctl (Linux/Mac)
curl -L https://fly.io/install.sh | sh

# تسجيل الدخول
flyctl auth login

# إنشاء التطبيق
flyctl apps create housing-management-system --org personal
```

#### الخطوة 5: تكوين قاعدة البيانات PostgreSQL

**عبر flyctl CLI:**

```bash
# إنشاء قاعدة بيانات PostgreSQL
flyctl postgres create --name housing-db --region iad

# ربط قاعدة البيانات بالتطبيق
flyctl postgres attach --app housing-management-system housing-db
```

**عبر واجهة الويب:**

1. في لوحة التحكم، اذهب إلى تطبيقك
2. انقر على "Add a Postgres database"
3. اختر:
   - **Name:** housing-db
   - **Region:** نفس منطقة التطبيق
   - **VM Size:** shared-cpu-1x (مجاني)
   - **Volume Size:** 1GB (مجاني)
4. انقر على "Create database"

#### الخطوة 6: تفعيل GitHub Actions Workflow

الملف موجود بالفعل في `.github/workflows/fly-deploy.yml`، لكنك تحتاج لتفعيله:

1. تأكد من وجود `FLY_API_TOKEN` في GitHub Secrets (من الخطوة 3)
2. ادفع أي تغيير للكود أو ادفع الكود الحالي:
   ```bash
   git add .
   git commit -m "Enable Fly.io deployment"
   git push origin main
   ```
3. اذهب إلى "Actions" في GitHub repository
4. شاهد سير العمل "Deploy to Fly.io"
5. انتظر حتى يكتمل النشر (5-10 دقائق)

#### الخطوة 7: الوصول للتطبيق

بعد نشر التطبيق بنجاح:

1. افتح: `https://housing-management-system.fly.dev`
   - أو استخدم اسم تطبيقك إذا كان مختلفاً
2. سجل دخول باستخدام:
   - **اسم المستخدم:** admin
   - **كلمة المرور:** Admin@2025

🎉 **تهانينا! تم نشر النظام بنجاح على Fly.io**

---

### الطريقة 2️⃣: النشر اليدوي عبر flyctl CLI

إذا كنت تفضل التحكم الكامل، يمكنك النشر يدوياً:

#### الخطوة 1: تثبيت flyctl

**على Linux/Mac:**
```bash
curl -L https://fly.io/install.sh | sh
```

**على Windows (PowerShell):**
```powershell
iwr https://fly.io/install.ps1 -useb | iex
```

#### الخطوة 2: تسجيل الدخول

```bash
flyctl auth login
```

سيفتح متصفح للمصادقة.

#### الخطوة 3: استنساخ المشروع (إذا لم يكن موجوداً)

```bash
git clone https://github.com/Ali5829511/2025.git
cd 2025
```

#### الخطوة 4: إنشاء التطبيق

```bash
# إنشاء تطبيق جديد
flyctl apps create housing-management-system

# أو إذا كنت تريد Fly.io أن تختار اسماً عشوائياً
flyctl apps create
```

#### الخطوة 5: إنشاء قاعدة البيانات

```bash
# إنشاء PostgreSQL database
flyctl postgres create --name housing-db --region iad

# ربط قاعدة البيانات بالتطبيق
flyctl postgres attach --app housing-management-system housing-db
```

#### الخطوة 6: تعيين متغيرات البيئة

```bash
# تعيين SECRET_KEY عشوائي آمن
flyctl secrets set SECRET_KEY=$(openssl rand -hex 32)

# متغيرات إضافية إذا لزم الأمر
flyctl secrets set FLASK_ENV=production
flyctl secrets set FLASK_DEBUG=false
```

#### الخطوة 7: النشر

```bash
# نشر التطبيق
flyctl deploy

# أو إذا كنت تريد متابعة السجلات مباشرة
flyctl deploy --detach=false
```

#### الخطوة 8: فتح التطبيق

```bash
# فتح التطبيق في المتصفح
flyctl open

# أو عرض معلومات التطبيق
flyctl info
```

---

## 🔧 إدارة التطبيق / Application Management

### عرض السجلات / View Logs

```bash
# عرض السجلات المباشرة
flyctl logs

# عرض آخر 100 سطر من السجلات
flyctl logs --limit 100
```

### توسيع النطاق / Scaling

```bash
# عرض حالة الآلات الافتراضية
flyctl scale show

# زيادة الذاكرة
flyctl scale memory 512

# زيادة عدد الآلات
flyctl scale count 2
```

### الوصول إلى قاعدة البيانات / Database Access

```bash
# الاتصال بقاعدة البيانات
flyctl postgres connect --app housing-db

# عرض بيانات الاتصال
flyctl postgres db list --app housing-db
```

### تنفيذ أوامر / Execute Commands

```bash
# تنفيذ أمر داخل التطبيق
flyctl ssh console

# مثال: إنشاء قاعدة البيانات
flyctl ssh console -C "python database.py"
```

---

## 🛡️ الأمان والإعدادات / Security & Settings

### تغيير كلمات المرور الافتراضية

**مهم جداً!** بعد أول نشر، قم بتغيير كلمات المرور الافتراضية:

1. سجل دخول كـ admin
2. اذهب إلى إدارة المستخدمين
3. غيّر كلمة مرور admin
4. غيّر كلمات مرور المستخدمين الآخرين

### تفعيل HTTPS

HTTPS مفعّل تلقائياً على Fly.io مع شهادات مجانية!

### النسخ الاحتياطي / Backups

```bash
# أخذ نسخة احتياطية من قاعدة البيانات
flyctl postgres db backup --app housing-db

# عرض النسخ الاحتياطية
flyctl postgres db list-backups --app housing-db
```

---

## 💰 التكاليف والحدود / Costs & Limits

### الطبقة المجانية / Free Tier

- **3 آلات افتراضية مشتركة** (Shared CPUs)
- **3 GB تخزين دائم** (Persistent storage)
- **160 GB نقل بيانات شهرياً** (Data transfer per month)

### بعد تجاوز الحد المجاني / After Free Tier

إذا تجاوزت الحدود المجانية:
- **Shared CPU VM:** $1.94/month
- **PostgreSQL (1GB):** $0/month (مجاني ضمن الحدود)
- **نقل البيانات:** $0.02/GB

**💡 نصيحة:** لمعظم الاستخدامات، الطبقة المجانية كافية تماماً!

---

## 📊 المراقبة / Monitoring

### عرض حالة التطبيق / Application Status

```bash
# حالة التطبيق
flyctl status

# معلومات مفصلة
flyctl info
```

### المراقبة عبر الويب / Web Monitoring

1. اذهب إلى: https://fly.io/dashboard
2. اختر تطبيقك
3. شاهد:
   - حالة الآلات الافتراضية
   - استخدام الذاكرة والمعالج
   - حركة الشبكة
   - السجلات

---

## ❓ استكشاف الأخطاء / Troubleshooting

### التطبيق لا يبدأ / App Won't Start

```bash
# فحص السجلات
flyctl logs

# فحص حالة التطبيق
flyctl status

# إعادة تشغيل التطبيق
flyctl apps restart housing-management-system
```

### مشاكل قاعدة البيانات / Database Issues

```bash
# فحص حالة قاعدة البيانات
flyctl postgres db list --app housing-db

# الاتصال مباشرة بقاعدة البيانات
flyctl postgres connect --app housing-db
```

### خطأ 500 أو أخطاء أخرى / 500 Error or Other Issues

1. فحص السجلات:
   ```bash
   flyctl logs
   ```

2. التحقق من متغيرات البيئة:
   ```bash
   flyctl secrets list
   ```

3. إعادة بناء ونشر التطبيق:
   ```bash
   flyctl deploy --force
   ```

---

## 🔄 التحديثات / Updates

### تحديث التطبيق تلقائياً

إذا كنت تستخدم GitHub Actions:
1. ادفع التغييرات إلى GitHub
2. سيتم النشر تلقائياً
3. شاهد التقدم في "Actions"

### تحديث التطبيق يدوياً

```bash
# سحب آخر التحديثات
git pull origin main

# نشر التحديثات
flyctl deploy
```

---

## 🌐 النطاقات المخصصة / Custom Domains

### إضافة نطاق مخصص / Add Custom Domain

```bash
# إضافة نطاق
flyctl certs add yourdomain.com

# عرض الشهادات
flyctl certs list

# عرض معلومات DNS المطلوبة
flyctl certs show yourdomain.com
```

### تكوين DNS / Configure DNS

أضف سجلات DNS التالية عند مزود النطاق:

```
Type: A
Name: @
Value: [IP from flyctl certs show]

Type: AAAA
Name: @
Value: [IPv6 from flyctl certs show]
```

---

## 📚 موارد إضافية / Additional Resources

### الوثائق الرسمية / Official Documentation
- [Fly.io Documentation](https://fly.io/docs/)
- [Flask on Fly.io](https://fly.io/docs/languages-and-frameworks/python/)
- [Fly.io PostgreSQL](https://fly.io/docs/postgres/)

### أدلة أخرى في هذا المشروع / Other Guides in This Project
- [دليل النشر على Render.com](RENDER_DEPLOYMENT.md)
- [خيارات الاستضافة السحابية](CLOUD_HOSTING_OPTIONS.md)
- [دليل Docker Hub](DOCKER_HUB_GUIDE.md)
- [دليل النشر الكامل](دليل_النشر_الكامل.md)

### الدعم / Support
- **Fly.io Community:** https://community.fly.io/
- **GitHub Issues:** https://github.com/Ali5829511/2025/issues

---

## ✅ قائمة التحقق النهائية / Final Checklist

قبل اعتبار النشر مكتملاً، تأكد من:

Before considering deployment complete, ensure:

- [x] تم إنشاء حساب Fly.io / Created Fly.io account
- [x] تم إنشاء التطبيق على Fly.io / Created application on Fly.io
- [x] تم تكوين قاعدة بيانات PostgreSQL / Configured PostgreSQL database
- [x] تم نشر التطبيق بنجاح / Application deployed successfully
- [x] تم اختبار تسجيل الدخول / Tested login functionality
- [ ] تم تغيير كلمات المرور الافتراضية / Changed default passwords
- [ ] تم اختبار جميع الميزات الرئيسية / Tested all major features
- [ ] تم إعداد النسخ الاحتياطي / Set up backups
- [ ] تم تكوين المراقبة / Configured monitoring
- [ ] تم توثيق بيانات الوصول / Documented access credentials

---

**🎉 تهانينا! نظامك الآن مُستضاف على Fly.io بنجاح!**

**🎉 Congratulations! Your system is now successfully hosted on Fly.io!**

---

**تم إنشاؤه بواسطة / Created by:** فريق التطوير / Development Team  
**آخر تحديث / Last Updated:** نوفمبر 2025 / November 2025
