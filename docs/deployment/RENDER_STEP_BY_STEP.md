# دليل النشر الكامل على Render.com (خطوة بخطوة)
# Complete Render.com Deployment Guide (Step by Step)

<div dir="rtl">

## ⚠️ تحذير هام

إذا كانت لديك خدمة منشورة بالفعل على Render.com وتحصل على خطأ SIGTERM، فهذا يعني أن Render ينشر تطبيق **Node.js** بدلاً من **Python**.

يجب حذف الخدمة القديمة وإنشاء خدمة جديدة بإعدادات صحيحة.

</div>

---

## 📋 المتطلبات الأساسية / Prerequisites

- حساب على Render.com (مجاني)
- مستودع GitHub متصل
- الفرع يحتوي على الملفات الصحيحة

---

## 🗑️ الخطوة 1: حذف النشر القديم (إذا وجد)

### في Render.com Dashboard:

1. انتقل إلى: https://dashboard.render.com
2. ابحث عن الخدمة (مثل "two025-upa7")
3. اضغط على الخدمة
4. اذهب إلى "Settings" (في القائمة اليمنى)
5. انزل إلى الأسفل → "Delete Service"
6. اكتب اسم الخدمة للتأكيد
7. اضغط "Delete"

```
╔════════════════════════════════╗
║   Render.com Dashboard         ║
╠════════════════════════════════╣
║ Services:                      ║
║  ☐ two025-upa7 (Node.js) ❌   ║
║     → Settings                 ║
║       → Delete Service ⚠️      ║
╚════════════════════════════════╝
```

---

## ✅ الخطوة 2: إنشاء خدمة جديدة

### 2.1 بدء الإنشاء

1. في Dashboard، اضغط **"New +"**
2. اختر **"Web Service"**

```
╔════════════════════════════════╗
║   New +   ▼                    ║
╠════════════════════════════════╣
║  → Web Service       [اختر]   ║
║  → Static Site                 ║
║  → PostgreSQL                  ║
║  → Redis                       ║
╚════════════════════════════════╝
```

### 2.2 ربط المستودع

1. اختر **"Connect a repository"**
2. ابحث عن: `Ali5829511/2025`
3. اضغط **"Connect"**

```
╔════════════════════════════════╗
║ Connect Repository             ║
╠════════════════════════════════╣
║ Search: Ali5829511/2025        ║
║                                ║
║ ☑ Ali5829511/2025              ║
║   main branch                  ║
║   [Connect] ← اضغط هنا        ║
╚════════════════════════════════╝
```

---

## ⚙️ الخطوة 3: تكوين الخدمة

### املأ الحقول التالية:

| الحقل | القيمة |
|-------|--------|
| **Name** | `traffic-violations-system` |
| **Region** | `Oregon (US West)` أو أي منطقة |
| **Branch** | `main` (أو `copilot/extracting-docker-image-sha256`) |
| **Runtime** | ⚠️ **Python 3** (مهم جداً!) |
| **Build Command** | `pip install -r requirements.txt && python init_traffic_db.py` |
| **Start Command** | `gunicorn --config gunicorn_traffic_config.py traffic_app:app` |

```
╔═══════════════════════════════════════════╗
║ Configure Web Service                     ║
╠═══════════════════════════════════════════╣
║ Name: traffic-violations-system           ║
║                                           ║
║ Region: [Oregon (US West)     ▼]         ║
║                                           ║
║ Branch: [main                 ▼]         ║
║                                           ║
║ Runtime: [Python 3            ▼] ✅      ║
║          NOT Node!                        ║
║                                           ║
║ Build Command:                            ║
║ pip install -r requirements.txt &&        ║
║ python init_traffic_db.py                 ║
║                                           ║
║ Start Command:                            ║
║ gunicorn --config gunicorn_traffic_config.py traffic_app:app
║                                           ║
╚═══════════════════════════════════════════╝
```

---

## 🔧 الخطوة 4: إضافة متغيرات البيئة

اضغط **"Advanced"** → **"Add Environment Variable"**

أضف هذه المتغيرات:

| المفتاح (Key) | القيمة (Value) |
|---------------|----------------|
| `PORT` | `10000` |
| `FLASK_DEBUG` | `false` |
| `FLASK_ENV` | `production` |
| `PLATE_RECOGNIZER_API_TOKEN` | `your_token` (اختياري) |

```
╔═══════════════════════════════════════════╗
║ Environment Variables                     ║
╠═══════════════════════════════════════════╣
║ Key: PORT                Value: 10000     ║
║ [+] Add another                           ║
║                                           ║
║ Key: FLASK_DEBUG         Value: false     ║
║ [+] Add another                           ║
║                                           ║
║ Key: FLASK_ENV           Value: production║
║ [+] Add another                           ║
╚═══════════════════════════════════════════╝
```

---

## 🏥 الخطوة 5: تكوين Health Check

في قسم **"Health Check"**:

| الحقل | القيمة |
|-------|--------|
| **Health Check Path** | `/health` |

```
╔═══════════════════════════════════════════╗
║ Health Check                              ║
╠═══════════════════════════════════════════╣
║ Health Check Path: /health                ║
║                                           ║
║ This endpoint returns 200 OK when healthy║
╚═══════════════════════════════════════════╝
```

---

## 🚀 الخطوة 6: النشر

1. راجع جميع الإعدادات
2. اضغط **"Create Web Service"**
3. انتظر حتى يكتمل البناء (5-10 دقائق)

```
╔═══════════════════════════════════════════╗
║ Review & Deploy                           ║
╠═══════════════════════════════════════════╣
║ ✓ Name: traffic-violations-system         ║
║ ✓ Runtime: Python 3                       ║
║ ✓ Build & Start commands configured       ║
║ ✓ Environment variables set               ║
║ ✓ Health check configured                 ║
║                                           ║
║        [Create Web Service]               ║
╚═══════════════════════════════════════════╝
```

---

## 📊 الخطوة 7: مراقبة النشر

### في صفحة الخدمة، راقب:

1. **Build Logs** - يجب أن ترى:
```
Installing dependencies...
✓ Flask installed
✓ Gunicorn installed
✓ Database initialized
Build succeeded
```

2. **Deploy Logs** - يجب أن ترى:
```
Starting gunicorn 23.0.0

============================================================
🚀 نظام إدارة المخالفات المرورية
🚀 Traffic Violations Management System
============================================================

✅ Starting Gunicorn server
✅ Workers: 4
✅ Binding to: 0.0.0.0:10000
```

### ❌ إذا رأيت هذا (خطأ):
```
> node server.js  ← خطأ! هذا Node.js
npm error SIGTERM
```
→ **الحل**: ارجع للخطوة 1 واحذف الخدمة ثم أعد الإنشاء

---

## ✅ الخطوة 8: التحقق من النجاح

### 8.1 اختبار Health Check

```bash
curl https://your-app.onrender.com/health
```

**النتيجة المتوقعة:**
```json
{
  "status": "healthy",
  "service": "Traffic Violations Management System",
  "database": "connected",
  "timestamp": "2025-11-11T..."
}
```

### 8.2 اختبار الصفحة الرئيسية

افتح في المتصفح:
```
https://your-app.onrender.com/
```

يجب أن ترى واجهة نظام المخالفات المرورية.

---

## 🔍 استكشاف الأخطاء

### المشكلة: "node server.js" في اللوجات

**السبب**: Render ينشر تطبيق Node.js بدلاً من Python

**الحل**:
1. تحقق من Runtime = **Python 3** (وليس Node)
2. احذف الخدمة وأعد إنشاءها
3. تأكد من الفرع الصحيح

### المشكلة: "Module not found: gunicorn"

**السبب**: Build Command غير صحيح

**الحل**:
```bash
# Build Command يجب أن يكون:
pip install -r requirements.txt && python init_traffic_db.py
```

### المشكلة: "Failed to bind to port"

**السبب**: متغير PORT غير مضبوط

**الحل**:
```
Environment Variables:
PORT = 10000
```

---

## 📝 قائمة التحقق النهائية

قبل النشر، تأكد من:

- [ ] تم حذف النشر القديم (إذا كان Node.js)
- [ ] Runtime = **Python 3** ✅
- [ ] Build Command صحيح
- [ ] Start Command = `gunicorn --config...`
- [ ] متغيرات البيئة مضبوطة
- [ ] Health Check Path = `/health`
- [ ] الفرع الصحيح محدد

---

## 🎉 النجاح!

عند النجاح، ستحصل على:

```
╔═══════════════════════════════════════════╗
║ ✅ Deployment Successful                  ║
╠═══════════════════════════════════════════╣
║ Your service is live at:                  ║
║ https://traffic-violations-system.onrender.com
║                                           ║
║ Status: ● Running                         ║
║ Health: ✓ Healthy                         ║
║ Last Deploy: Just now                     ║
╚═══════════════════════════════════════════╝
```

---

## 📞 الدعم

إذا استمرت المشكلة:

1. راجع [RENDER_DEPLOYMENT_FIX.md](RENDER_DEPLOYMENT_FIX.md)
2. تحقق من اللوجات في Render Dashboard
3. تأكد من Runtime = Python 3

---

**آخر تحديث**: 2025-11-11  
**الحالة**: ✅ جاهز للنشر
