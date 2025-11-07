# 🚀 دليل النشر على Fly.io
# Fly.io Deployment Guide

**الحالة / Status:** ✅ جاهز للنشر / Ready for Deployment  
**الوقت المطلوب / Time Required:** 10-15 دقيقة / minutes  
**التكلفة / Cost:** مجاني (فترة تجريبية دائمة) / Free (Permanent Free Tier)

---

## 📋 نظرة عامة / Overview

Fly.io هي منصة سحابية حديثة تتيح نشر التطبيقات بسهولة مع فترة مجانية دائمة. هذا الدليل يشرح كيفية نشر نظام إدارة الإسكان على Fly.io.

Fly.io is a modern cloud platform that allows easy application deployment with a permanent free tier. This guide explains how to deploy the Housing Management System on Fly.io.

### ✨ مميزات Fly.io / Fly.io Features

- ✅ **فترة مجانية دائمة / Permanent Free Tier:** $5 رصيد شهري مجاني / $5 monthly free credit
- ✅ **نشر سريع جداً / Very Fast Deployment:** يتم النشر في دقائق / Deploys in minutes
- ✅ **SSL مجاني / Free SSL:** شهادة HTTPS تلقائية / Automatic HTTPS certificate
- ✅ **قواعد بيانات PostgreSQL / PostgreSQL Databases:** مدمجة ومُدارة / Integrated and managed
- ✅ **خوادم عالمية / Global Servers:** قريبة من المستخدمين / Close to users
- ✅ **سهل الاستخدام / Easy to Use:** أوامر بسيطة / Simple commands
- ✅ **لا توقف تلقائي / No Auto-Sleep:** التطبيق يعمل دائماً / App always running

---

## 🎯 المتطلبات / Requirements

### 1. حساب Fly.io / Fly.io Account
- قم بالتسجيل على: https://fly.io/app/sign-up
- ⚠️ **ملاحظة:** قد يطلب بطاقة ائتمانية للتحقق فقط (لن يتم الخصم) / May require credit card for verification only (no charge)

### 2. تثبيت Fly CLI / Install Fly CLI

**على macOS / On macOS:**
```bash
brew install flyctl
```

**على Linux / On Linux:**
```bash
curl -L https://fly.io/install.sh | sh
```

**على Windows / On Windows:**
```powershell
iwr https://fly.io/install.ps1 -useb | iex
```

### 3. تسجيل الدخول / Login
```bash
flyctl auth login
```

---

## 📝 خطوات النشر / Deployment Steps

### الطريقة 1️⃣: النشر السريع (موصى به / Recommended)

#### الخطوة 1: استنساخ المشروع / Clone Project

```bash
# استنساخ المشروع / Clone the project
git clone https://github.com/Ali5829511/2025.git housing-system
cd housing-system
```

#### الخطوة 2: إنشاء التطبيق / Create App

```bash
# إنشاء تطبيق جديد / Create new app
flyctl launch

# أجب على الأسئلة كما يلي / Answer questions as follows:
# - App name: housing-system (أو اسم آخر / or another name)
# - Region: Dallas (dfw) - الأقرب للسعودية / Closest to Saudi Arabia
# - PostgreSQL: Yes (نعم) - اختر أصغر حجم / Choose smallest size
# - Redis: No (لا)
# - Deploy now: No (لا - سنفعل ذلك يدوياً)
```

#### الخطوة 3: إنشاء قاعدة البيانات / Create Database

```bash
# إنشاء قاعدة بيانات PostgreSQL / Create PostgreSQL database
flyctl postgres create --name housing-db --initial-cluster-size 1 --vm-size shared-cpu-1x --volume-size 1

# ربط القاعدة بالتطبيق / Attach database to app
flyctl postgres attach housing-db --app housing-system
```

#### الخطوة 4: إضافة المتغيرات البيئية / Add Environment Variables

```bash
# إضافة المتغيرات / Add variables
flyctl secrets set \
  FLASK_ENV=production \
  FLASK_DEBUG=false \
  SECRET_KEY=$(openssl rand -hex 32)
```

#### الخطوة 5: النشر / Deploy

```bash
# نشر التطبيق / Deploy application
flyctl deploy

# انتظر اكتمال النشر (2-3 دقائق) / Wait for deployment (2-3 minutes)
```

#### الخطوة 6: إنشاء قاعدة البيانات الأولية / Initialize Database

```bash
# فتح shell في التطبيق / Open shell in app
flyctl ssh console

# تشغيل سكريبت إنشاء الجداول / Run database initialization
python init_db.py

# الخروج / Exit
exit
```

#### الخطوة 7: الوصول للتطبيق / Access Application

```bash
# فتح التطبيق في المتصفح / Open app in browser
flyctl open
```

الرابط سيكون بصيغة: `https://housing-system.fly.dev`

**بيانات الدخول / Login Credentials:**
- اسم المستخدم / Username: `admin`
- كلمة المرور / Password: `Admin@2025`

⚠️ **مهم جداً:** غيّر كلمة المرور فوراً!

---

### الطريقة 2️⃣: النشر اليدوي الكامل / Full Manual Deployment

إذا كنت تفضل التحكم الكامل:

#### 1. تعديل ملف fly.toml

تأكد من أن ملف `fly.toml` موجود ويحتوي على التكوين الصحيح:

```toml
app = "housing-system"
primary_region = "dfw"

[build]

[env]
  FLASK_ENV = "production"
  FLASK_DEBUG = "false"
  PORT = "8080"

[http_service]
  internal_port = 8080
  force_https = true
  auto_stop_machines = true
  auto_start_machines = true
  min_machines_running = 0

[[services]]
  internal_port = 8080
  protocol = "tcp"

  [[services.ports]]
    port = 80
    handlers = ["http"]
    force_https = true

  [[services.ports]]
    port = 443
    handlers = ["tls", "http"]

[[vm]]
  cpu_kind = "shared"
  cpus = 1
  memory_mb = 256
```

#### 2. إنشاء Dockerfile (إذا لم يكن موجوداً)

الملف موجود بالفعل في المشروع.

#### 3. النشر

```bash
flyctl deploy --ha=false
```

---

## 🔧 إعدادات إضافية / Additional Settings

### تكبير حجم التطبيق / Scale App

```bash
# زيادة الذاكرة / Increase memory
flyctl scale memory 512

# زيادة عدد النسخ / Increase instances
flyctl scale count 2
```

### مراقبة التطبيق / Monitor App

```bash
# مشاهدة السجلات / View logs
flyctl logs

# حالة التطبيق / App status
flyctl status

# معلومات التطبيق / App info
flyctl info
```

### تحديث التطبيق / Update App

```bash
# سحب آخر تحديثات / Pull latest updates
git pull origin main

# إعادة النشر / Redeploy
flyctl deploy
```

---

## 🔒 الأمان / Security

### تغيير كلمات المرور الافتراضية

⚠️ **مهم جداً:** بعد أول تسجيل دخول، قم بتغيير جميع كلمات المرور:

1. **admin:** Admin@2025 → كلمة مرور قوية جديدة
2. **violations_officer:** Violations@2025 → كلمة مرور قوية جديدة
3. **visitors_officer:** Visitors@2025 → كلمة مرور قوية جديدة
4. **viewer:** Viewer@2025 → كلمة مرور قوية جديدة
5. **violation_entry:** Violation@2025 → كلمة مرور قوية جديدة

### تأمين المتغيرات البيئية / Secure Environment Variables

```bash
# عرض المتغيرات الحالية / View current variables
flyctl secrets list

# تحديث SECRET_KEY / Update SECRET_KEY
flyctl secrets set SECRET_KEY=$(openssl rand -hex 32)
```

### تفعيل HTTPS فقط / Enable HTTPS Only

تأكد من أن `force_https = true` في ملف `fly.toml` (مُفعّل افتراضياً).

---

## 💾 النسخ الاحتياطي / Backup

### نسخ احتياطي لقاعدة البيانات / Database Backup

```bash
# الاتصال بقاعدة البيانات / Connect to database
flyctl postgres connect -a housing-db

# تصدير البيانات / Export data
pg_dump housing_db > backup.sql

# الخروج / Exit
\q
```

### جدولة النسخ الاحتياطي / Schedule Backups

يُنصح بإنشاء نسخة احتياطية يدوية أسبوعياً أو استخدام أدوات خارجية.

---

## 🔧 استكشاف الأخطاء / Troubleshooting

### المشكلة: التطبيق لا يبدأ / App Won't Start

**الحل / Solution:**
```bash
# فحص السجلات / Check logs
flyctl logs

# فحص حالة التطبيق / Check app status
flyctl status

# إعادة تشغيل / Restart
flyctl apps restart housing-system
```

### المشكلة: خطأ في قاعدة البيانات / Database Error

**الحل / Solution:**
```bash
# فحص حالة القاعدة / Check database status
flyctl postgres status -a housing-db

# الاتصال بالقاعدة للفحص / Connect to database
flyctl postgres connect -a housing-db

# إعادة تشغيل init_db.py / Re-run init_db.py
flyctl ssh console
python init_db.py
exit
```

### المشكلة: الصفحة تعرض "Application Error"

**الحل / Solution:**
1. راجع السجلات: `flyctl logs`
2. تأكد من تشغيل `python init_db.py`
3. تحقق من المتغيرات البيئية: `flyctl secrets list`

### المشكلة: بطء التطبيق / App is Slow

**الحل / Solution:**
```bash
# زيادة الذاكرة / Increase memory
flyctl scale memory 512

# أو اختيار منطقة أقرب / Or choose closer region
flyctl regions list
flyctl regions add dfw  # Dallas
```

---

## 📊 التكاليف / Costs

### الفترة المجانية / Free Tier

Fly.io يوفر:
- ✅ 3 shared-cpu-1x VMs (256MB RAM each)
- ✅ 160GB bandwidth شهرياً
- ✅ 3GB قاعدة بيانات PostgreSQL
- ✅ SSL مجاني

**تقدير التكلفة الشهرية / Monthly Cost Estimate:**
- نظامنا (تكوين أساسي): **مجاني تماماً / Completely Free**
- مع استخدام أعلى: **$0-5 / شهر**

### مراقبة الاستهلاك / Monitor Usage

```bash
# عرض الاستخدام / View usage
flyctl dashboard
```

---

## 🌐 Domain مخصص / Custom Domain

لربط نطاق خاص بك:

```bash
# إضافة domain / Add domain
flyctl certs add yourdomain.com

# عرض شهادات SSL / View SSL certificates
flyctl certs list

# إضافة سجلات DNS / Add DNS records
# A record: @  →  IP من flyctl info
# AAAA record: @  →  IPv6 من flyctl info
```

---

## 📈 الترقية / Scaling

### زيادة الموارد / Increase Resources

```bash
# زيادة الذاكرة إلى 512MB / Increase memory to 512MB
flyctl scale memory 512

# زيادة عدد النسخ لـ High Availability
flyctl scale count 2

# اختيار CPU أسرع / Choose faster CPU
flyctl scale vm shared-cpu-2x
```

---

## 🔄 التحديثات التلقائية / Auto-Updates

لتفعيل النشر التلقائي عند دفع الكود:

```bash
# ربط GitHub Actions (إذا كنت تستخدمه)
# راجع: https://fly.io/docs/app-guides/continuous-deployment-with-github-actions/
```

---

## ✅ قائمة التحقق بعد النشر / Post-Deployment Checklist

- [ ] التطبيق يعمل: `flyctl open`
- [ ] تسجيل الدخول يعمل
- [ ] تم تشغيل `python init_db.py`
- [ ] تم تغيير جميع كلمات المرور
- [ ] تم اختبار جميع الوظائف الأساسية
- [ ] السجلات لا تحتوي على أخطاء: `flyctl logs`
- [ ] قاعدة البيانات تعمل بشكل صحيح
- [ ] HTTPS يعمل (التحقق من القفل في المتصفح)

---

## 📞 الدعم / Support

### موارد Fly.io

- **الوثائق:** https://fly.io/docs
- **المجتمع:** https://community.fly.io
- **Discord:** https://fly.io/discord
- **الدعم:** support@fly.io

### موارد المشروع

- **GitHub:** https://github.com/Ali5829511/2025
- **دليل البدء السريع:** [QUICK_START.md](QUICK_START.md)
- **خيارات الاستضافة:** [CLOUD_HOSTING_OPTIONS.md](CLOUD_HOSTING_OPTIONS.md)

---

## 🎯 المقارنة مع منصات أخرى / Comparison with Other Platforms

| الميزة / Feature | Fly.io | Render | Railway |
|-----------------|--------|--------|---------|
| الفترة المجانية / Free Tier | دائمة / Permanent | 90 يوم DB | $5 شهرياً |
| السرعة / Speed | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| السهولة / Ease | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| التوقف / Sleep | ❌ لا ينام | ✅ ينام 15د | ❌ لا ينام |
| الذاكرة / RAM | 256 MB | 512 MB | 512 MB |
| قاعدة البيانات / DB | PostgreSQL | PostgreSQL | PostgreSQL |
| SSL | ✅ مجاني | ✅ مجاني | ✅ مجاني |
| خوادم عالمية / Global | ✅ 30+ منطقة | ⚠️ محدودة | ⚠️ محدودة |

**التوصية / Recommendation:**
- **للأداء:** Fly.io ⭐
- **للسهولة:** Render
- **للسرعة:** Railway أو Fly.io

---

## 🎉 تهانينا! / Congratulations!

نظامك الآن منشور على Fly.io! 🚀

Your system is now deployed on Fly.io! 🚀

**الرابط / URL:** https://housing-system.fly.dev

**بيانات الدخول / Login Credentials:**
- Username: admin
- Password: Admin@2025 (⚠️ غيّرها فوراً / change immediately)

---

## 💡 نصائح إضافية / Additional Tips

### لتحسين الأداء / Performance Tips

1. **استخدم منطقة قريبة / Use nearby region:**
   ```bash
   flyctl regions list
   flyctl regions add dfw  # Dallas - الأقرب للسعودية
   ```

2. **فعّل الذاكرة المؤقتة / Enable caching**
3. **راقب السجلات / Monitor logs:** `flyctl logs`
4. **استخدم metrics:** `flyctl metrics`

### للأمان / Security Tips

1. **غيّر جميع كلمات المرور**
2. **استخدم secrets للمتغيرات الحساسة**
3. **فعّل HTTPS فقط**
4. **راجع السجلات بانتظام**
5. **انسخ احتياطياً أسبوعياً**

---

**جامعة الإمام محمد بن سعود الإسلامية © 2025**

تم التحديث: نوفمبر 2025 / Updated: November 2025
