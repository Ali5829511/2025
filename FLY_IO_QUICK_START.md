# 🚀 Fly.io Quick Start / دليل البدء السريع

## النشر السريع في 5 خطوات / Quick Deploy in 5 Steps

### ✈️ الطريقة 1: GitHub Actions (أوتوماتيكي - موصى به)

**1. إنشاء حساب / Create Account:**
```
https://fly.io/app/sign-up
```
لا يحتاج بطاقة ائتمانية! / No credit card needed!

**2. الحصول على API Token:**
```
https://fly.io/user/personal_access_tokens
انقر على "Create token" / Click "Create token"
احفظ الرمز! / Save the token!
```

**3. إضافة الرمز إلى GitHub:**
```
GitHub → Settings → Secrets → Actions → New secret
Name: FLY_API_TOKEN
Value: [الصق الرمز / Paste token]
```

**4. إنشاء التطبيق على Fly.io:**

**عبر الويب / Via Web:**
```
https://fly.io/dashboard → Create app
Name: housing-management-system
Region: iad (أو الأقرب لك / or closest to you)
```

**أو عبر CLI / Or via CLI:**
```bash
curl -L https://fly.io/install.sh | sh
flyctl auth login
flyctl apps create housing-management-system
```

**5. إنشاء قاعدة البيانات / Create Database:**
```bash
flyctl postgres create --name housing-db --region iad
flyctl postgres attach --app housing-management-system housing-db
```

**6. دفع الكود للنشر / Push to Deploy:**
```bash
git push origin main
```
✅ سيتم النشر تلقائياً! / Will deploy automatically!

---

### 🖥️ الطريقة 2: flyctl CLI (يدوي)

**1. تثبيت flyctl:**
```bash
# Linux/Mac
curl -L https://fly.io/install.sh | sh

# Windows (PowerShell)
iwr https://fly.io/install.ps1 -useb | iex
```

**2. تسجيل الدخول:**
```bash
flyctl auth login
```

**3. إنشاء وربط قاعدة البيانات:**
```bash
flyctl postgres create --name housing-db
flyctl postgres attach --app housing-management-system housing-db
```

**4. النشر:**
```bash
flyctl deploy
```

**5. فتح التطبيق:**
```bash
flyctl open
```

---

## 🔑 بيانات الدخول الافتراضية / Default Credentials

```
Username: admin
Password: Admin@2025
```

⚠️ **مهم:** غيّر كلمة المرور بعد أول دخول!  
⚠️ **Important:** Change password after first login!

---

## 🌐 رابط التطبيق / Application URL

```
https://housing-management-system.fly.dev
```
(أو اسم تطبيقك / or your app name)

---

## 📊 أوامر مفيدة / Useful Commands

### إدارة التطبيق / App Management
```bash
flyctl status              # حالة التطبيق / App status
flyctl logs                # السجلات المباشرة / Live logs
flyctl info                # معلومات التطبيق / App info
```

### قاعدة البيانات / Database
```bash
flyctl postgres connect --app housing-db    # اتصال بقاعدة البيانات
flyctl postgres db list --app housing-db    # قائمة قواعد البيانات
```

### التوسع / Scaling
```bash
flyctl scale show          # عرض التكوين الحالي
flyctl scale memory 512    # زيادة الذاكرة
```

---

## 💰 الطبقة المجانية / Free Tier

✅ **3 آلات افتراضية مجانية** / 3 free VMs  
✅ **3 GB تخزين مجاني** / 3 GB free storage  
✅ **160 GB نقل بيانات شهرياً** / 160 GB monthly transfer  
✅ **لا ينام التطبيق!** / App doesn't sleep!

---

## 📚 المزيد من التفاصيل / More Details

للحصول على دليل كامل، راجع:  
For complete guide, see:

📖 **[FLY_IO_DEPLOYMENT.md](FLY_IO_DEPLOYMENT.md)**

---

## 🆘 الدعم / Support

- **Fly.io Docs:** https://fly.io/docs/
- **Community:** https://community.fly.io/
- **GitHub Issues:** https://github.com/Ali5829511/2025/issues

---

**✈️ استمتع بالنشر السريع مع Fly.io!**  
**✈️ Enjoy fast deployment with Fly.io!**
