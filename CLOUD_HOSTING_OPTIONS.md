# ☁️ خيارات الاستضافة السحابية مع فترة تجريبية مجانية
# Cloud Hosting Options with Free Trial

**تم التحديث:** نوفمبر 2025 / November 2025

---

## 📋 نظرة عامة / Overview

هذا الدليل يوضح خيارات الاستضافة السحابية المختلفة التي تدعم نشر نظام إدارة الإسكان مع فترة تجريبية مجانية.

This guide shows different cloud hosting options that support deploying the Housing Management System with free trial periods.

---

## 🌟 الخيارات الموصى بها / Recommended Options

### 1. ⭐ Render.com (موصى به بشدة / Highly Recommended)

**الفترة التجريبية / Trial Period:** 90 يوم قاعدة بيانات مجانية / 90-day free database

**المميزات / Advantages:**
- ✅ سهل الاستخدام جداً / Very easy to use
- ✅ نشر تلقائي من GitHub / Automatic deployment from GitHub
- ✅ SSL مجاني / Free SSL
- ✅ قاعدة بيانات PostgreSQL مُدارة / Managed PostgreSQL
- ✅ لا يتطلب بطاقة ائتمانية / No credit card required
- ✅ دعم ممتاز / Excellent support

**السلبيات / Disadvantages:**
- ⚠️ التطبيق ينام بعد 15 دقيقة من عدم النشاط / App sleeps after 15 min inactivity
- ⚠️ 512 MB RAM فقط في الخطة المجانية / Only 512 MB RAM in free tier

**التكلفة بعد الفترة التجريبية / Cost After Trial:**
- Starter: $7/month (Web Service + Database)
- Professional: $25/month

**الوثائق / Documentation:**
- [دليل النشر على Render](RENDER_DEPLOYMENT.md)

**رابط التسجيل / Sign Up:** https://render.com

---

### 2. 🚂 Railway.app

**الفترة التجريبية / Trial Period:** $5 رصيد مجاني شهرياً / $5 free credit monthly

**المميزات / Advantages:**
- ✅ واجهة بسيطة وجميلة / Simple and beautiful UI
- ✅ نشر سريع جداً / Very fast deployment
- ✅ قاعدة بيانات PostgreSQL / PostgreSQL database
- ✅ دعم Docker / Docker support
- ✅ لا timeout للتطبيقات / No app timeout

**السلبيات / Disadvantages:**
- ⚠️ يتطلب بطاقة ائتمانية بعد الرصيد المجاني / Requires credit card after free credit
- ⚠️ الرصيد المجاني محدود ($5/شهر) / Limited free credit ($5/month)

**التكلفة بعد الفترة التجريبية / Cost After Trial:**
- Pay-as-you-go: حسب الاستخدام / Based on usage
- تقريباً $5-20/month

**كيفية النشر / How to Deploy:**
1. سجل على https://railway.app
2. اربط حساب GitHub
3. انشئ مشروع جديد من GitHub repo
4. اختر `Ali5829511/2025`
5. أضف PostgreSQL database
6. أضف environment variables
7. Deploy!

**رابط التسجيل / Sign Up:** https://railway.app

---

### 3. 🔷 Heroku (خيار تقليدي / Traditional Option)

**الفترة التجريبية / Trial Period:** لم يعد يوفر خطة مجانية / No longer offers free tier

**ملاحظة / Note:** Heroku ألغى الخطة المجانية في نوفمبر 2022. الآن يتطلب اشتراك مدفوع.

Heroku discontinued free tier in November 2022. Now requires paid subscription.

**التكلفة / Cost:**
- Eco Dyno: $5/month (ينام بعد 30 دقيقة / sleeps after 30 min)
- Basic: $7/month (لا ينام / doesn't sleep)
- Database: $5/month

**رابط التسجيل / Sign Up:** https://heroku.com

---

### 4. 🔵 DigitalOcean App Platform

**الفترة التجريبية / Trial Period:** $200 رصيد مجاني (60 يوم) / $200 free credit (60 days)

**المميزات / Advantages:**
- ✅ رصيد مجاني سخي / Generous free credit
- ✅ أداء ممتاز / Excellent performance
- ✅ قواعد بيانات مُدارة / Managed databases
- ✅ مناسب للإنتاج / Production-ready

**السلبيات / Disadvantages:**
- ⚠️ يتطلب بطاقة ائتمانية / Requires credit card
- ⚠️ أكثر تعقيداً من Render / More complex than Render

**التكلفة بعد الفترة التجريبية / Cost After Trial:**
- Basic: $5/month
- Professional: $12/month
- Database: $15/month

**كيفية النشر / How to Deploy:**
1. سجل على https://digitalocean.com
2. احصل على $200 رصيد مجاني
3. اختر "App Platform"
4. اربط GitHub repository
5. اختر Python buildpack
6. أضف PostgreSQL database
7. Deploy!

**رابط التسجيل / Sign Up:** https://digitalocean.com

---

### 5. 🟦 Microsoft Azure App Service

**الفترة التجريبية / Trial Period:** $200 رصيد مجاني (30 يوم) / $200 free credit (30 days)

**المميزات / Advantages:**
- ✅ رصيد مجاني كبير / Large free credit
- ✅ بنية تحتية قوية / Strong infrastructure
- ✅ تكامل مع Active Directory / Integration with Active Directory
- ✅ مناسب للمؤسسات / Enterprise-ready

**السلبيات / Disadvantages:**
- ⚠️ يتطلب بطاقة ائتمانية / Requires credit card
- ⚠️ معقد للمبتدئين / Complex for beginners
- ⚠️ واجهة معقدة / Complex interface

**التكلفة بعد الفترة التجريبية / Cost After Trial:**
- Free tier: محدود جداً / Very limited
- Basic: $13.14/month
- Standard: $50.40/month

**رابط التسجيل / Sign Up:** https://azure.microsoft.com

---

### 6. 🟩 Google Cloud Platform (Cloud Run)

**الفترة التجريبية / Trial Period:** $300 رصيد مجاني (90 يوم) / $300 free credit (90 days)

**المميزات / Advantages:**
- ✅ رصيد مجاني سخي جداً / Very generous free credit
- ✅ Cloud Run مجاني للحد معين / Cloud Run free tier
- ✅ أداء عالي / High performance
- ✅ تكامل مع خدمات Google / Integration with Google services

**السلبيات / Disadvantages:**
- ⚠️ يتطلب بطاقة ائتمانية / Requires credit card
- ⚠️ معقد للمبتدئين / Complex for beginners
- ⚠️ فواتير قد تكون مفاجئة / Billing can be surprising

**التكلفة بعد الفترة التجريبية / Cost After Trial:**
- Cloud Run: أول 2 مليون طلب مجاني / First 2M requests free
- Cloud SQL: ~$10/month

**رابط التسجيل / Sign Up:** https://cloud.google.com

---

### 7. 🟠 AWS Free Tier (Amazon Web Services)

**الفترة التجريبية / Trial Period:** 12 شهر مجاني (محدود) / 12 months free (limited)

**المميزات / Advantages:**
- ✅ سنة كاملة مجانية / Full year free
- ✅ خدمات متعددة / Multiple services
- ✅ الأكثر شهرة / Most popular
- ✅ وثائق ممتازة / Excellent documentation

**السلبيات / Disadvantages:**
- ⚠️ يتطلب بطاقة ائتمانية / Requires credit card
- ⚠️ معقد جداً / Very complex
- ⚠️ سهل تجاوز الحد المجاني / Easy to exceed free tier
- ⚠️ الفواتير قد تكون عالية / Bills can be high

**التكلفة بعد الفترة التجريبية / Cost After Trial:**
- EC2 t2.micro: مجاني لسنة / Free for 1 year
- بعد السنة: ~$10-30/month

**رابط التسجيل / Sign Up:** https://aws.amazon.com/free

---

## 📊 جدول المقارنة / Comparison Table

| المنصة / Platform | فترة تجريبية / Trial | سهولة الاستخدام / Ease | الأداء / Performance | التكلفة بعد / Cost After |
|-------------------|---------------------|----------------------|---------------------|------------------------|
| **Render** ⭐ | 90 يوم قاعدة بيانات | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | $7/month |
| **Railway** | $5 شهرياً | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | $5-20/month |
| **Heroku** | ❌ لا يوجد | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | $12/month |
| **DigitalOcean** | $200 (60 يوم) | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | $20/month |
| **Azure** | $200 (30 يوم) | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | $15+/month |
| **Google Cloud** | $300 (90 يوم) | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | $10+/month |
| **AWS** | 12 شهر محدود | ⭐⭐ | ⭐⭐⭐⭐⭐ | $10-30/month |

---

## 🎯 التوصيات / Recommendations

### للبدء والتجربة / For Getting Started & Testing:
1. **Render.com** ⭐ - الأفضل والأسهل / Best & Easiest
2. **Railway.app** - بديل ممتاز / Excellent alternative

### للاستخدام الرسمي / For Production Use:
1. **DigitalOcean** - موثوق وبسعر معقول / Reliable & affordable
2. **Azure** - للمؤسسات / For enterprises
3. **Google Cloud** - أداء عالي / High performance

### للمشاريع الكبيرة / For Large Projects:
1. **AWS** - الأكثر شمولاً / Most comprehensive
2. **Google Cloud** - أفضل أداء / Best performance
3. **Azure** - تكامل مؤسسي / Enterprise integration

---

## ✅ قائمة التحقق قبل النشر / Pre-Deployment Checklist

قبل نشر النظام على أي منصة، تأكد من:

Before deploying to any platform, ensure:

- [ ] اختيار المنصة المناسبة لاحتياجاتك / Choose the right platform for your needs
- [ ] قراءة وثائق المنصة / Read platform documentation
- [ ] تجهيز حساب GitHub / Prepare GitHub account
- [ ] فهم حدود الفترة التجريبية / Understand trial limitations
- [ ] تجهيز بطاقة ائتمانية (إن لزم) / Prepare credit card (if needed)
- [ ] عمل نسخة احتياطية من البيانات / Backup your data
- [ ] تغيير كلمات المرور الافتراضية / Change default passwords
- [ ] إعداد متغيرات البيئة / Set up environment variables
- [ ] اختبار النظام بعد النشر / Test system after deployment

---

## 🆘 الدعم والمساعدة / Support & Help

### لكل منصة وثائق رسمية / Official Documentation:

- **Render:** https://render.com/docs
- **Railway:** https://docs.railway.app
- **Heroku:** https://devcenter.heroku.com
- **DigitalOcean:** https://docs.digitalocean.com
- **Azure:** https://docs.microsoft.com/azure
- **Google Cloud:** https://cloud.google.com/docs
- **AWS:** https://docs.aws.amazon.com

### وثائق المشروع / Project Documentation:

- [دليل النشر على Render](RENDER_DEPLOYMENT.md)
- [دليل النشر الكامل](دليل_النشر_الكامل.md)
- [النشر باستخدام Docker](النشر_باستخدام_Docker.md)
- [دليل البدء السريع](QUICK_START.md)

---

## 💡 نصائح عامة / General Tips

### لتوفير التكاليف / To Save Costs:

1. استخدم الفترة التجريبية بحكمة / Use trial period wisely
2. راقب استخدام الموارد / Monitor resource usage
3. أوقف الخدمات غير المستخدمة / Stop unused services
4. استخدم التنبيهات للميزانية / Set up budget alerts

### للأداء الأفضل / For Better Performance:

1. اختر منطقة قريبة / Choose nearby region
2. استخدم CDN للملفات الثابتة / Use CDN for static files
3. فعّل الذاكرة المؤقتة / Enable caching
4. راقب السجلات / Monitor logs

### للأمان / For Security:

1. استخدم HTTPS دائماً / Always use HTTPS
2. غيّر كلمات المرور / Change passwords
3. فعّل المصادقة الثنائية / Enable 2FA
4. احفظ نسخ احتياطية / Keep backups

---

## 🎉 ملخص / Summary

**أفضل خيار للبدء:** Render.com 🌟

**Best option to start:** Render.com 🌟

- ✅ لا يتطلب بطاقة ائتمانية / No credit card required
- ✅ سهل جداً / Very easy
- ✅ 90 يوم قاعدة بيانات مجانية / 90-day free database
- ✅ مناسب للتجربة والاستخدام المتوسط / Good for testing & medium use

**اتبع دليل النشر:** [RENDER_DEPLOYMENT.md](RENDER_DEPLOYMENT.md)

**Follow deployment guide:** [RENDER_DEPLOYMENT.md](RENDER_DEPLOYMENT.md)

---

**جامعة الإمام محمد بن سعود الإسلامية © 2025**

تم التحديث: نوفمبر 2025 / Updated: November 2025
