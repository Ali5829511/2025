# Quick Start - Vehicle Extraction Script
# دليل البدء السريع - سكربت استخراج بيانات المركبات

## للمستخدمين المستعجلين / For Users in a Hurry

### الخطوات السريعة (5 دقائق) / Quick Steps (5 minutes)

#### 1. تثبيت Python / Install Python
```bash
# Download from python.org
# تأكد من تفعيل "Add to PATH"
```

#### 2. تثبيت المكتبات / Install Libraries
```bash
pip install requests pandas openpyxl pillow colorthief
```

#### 3. تعديل السكربت / Edit Script
افتح `extract_vehicles.py` وعدّل السطور التالية:

```python
# Line 44: Your image folder path
IMAGE_FOLDER = r"C:\Your\Path\To\Images"

# Line 48: Your Plate Recognizer API token
API_TOKEN = "your_api_token_here"
```

#### 4. تشغيل السكربت / Run Script
```bash
python extract_vehicles.py
```

#### 5. النتيجة / Result
ستجد ملف `نتائج_المركبات.xlsx` في نفس المجلد.

---

## مثال عملي / Practical Example

### السيناريو / Scenario
لديك 8000 صورة في المجلد:
```
E:\WhatsApp Chat - الامام المرور\6\
```

### الخطوات / Steps

**1. تجهيز المجلد:**
```
E:\WhatsApp Chat - الامام المرور\6\
├── IMG_0001.jpg
├── IMG_0002.jpg
├── IMG_0003.jpg
...
└── IMG_8000.jpg
```

**2. تعديل السكربت:**
```python
IMAGE_FOLDER = r"E:\WhatsApp Chat - الامام المرور\6"
API_TOKEN = "sk_abc123xyz789"  # استبدله برمزك
```

**3. تشغيل:**
```bash
cd C:\Users\ALI\Desktop
python extract_vehicles.py
```

**4. المخرجات:**
```
🚗 Vehicle Data Extraction System
============================================================
📊 Found 8000 images to process
🚀 Starting processing...

[1/8000] Processing: IMG_0001.jpg
   ✅ Plate: ABC1234 (Confidence: 95.2%)
[2/8000] Processing: IMG_0002.jpg
   ✅ Plate: XYZ5678 (Confidence: 89.7%)
...

💾 Saving intermediate results... (every 50 images)

============================================================
📊 PROCESSING SUMMARY
Total images:      8000
Successful:        7850
Failed:            150
Success rate:      98.1%
Processing time:   4325.6 seconds (~ 1.2 hours)
============================================================

✅ Processing complete!
📄 Results saved to: نتائج_المركبات.xlsx
```

**5. فتح النتائج:**
افتح `نتائج_المركبات.xlsx` في Excel:

| الرقم | اسم الملف | رقم اللوحة | الثقة | نوع المركبة | اللون |
|------|-----------|-----------|------|------------|-------|
| 1 | IMG_0001.jpg | ABC1234 | 0.952 | Sedan | أبيض - RGB(240,240,245) |
| 2 | IMG_0002.jpg | XYZ5678 | 0.897 | SUV | أسود - RGB(25,30,35) |
| ... | ... | ... | ... | ... | ... |

---

## استكشاف الأخطاء السريع / Quick Troubleshooting

### خطأ 1: "API token not configured"
```python
# عدّل السطر 48 في extract_vehicles.py:
API_TOKEN = "your_actual_token_here"  # ❌ خطأ
API_TOKEN = "sk_abc123xyz789"         # ✅ صحيح
```

### خطأ 2: "Image folder not found"
```python
# تأكد من المسار الصحيح:
IMAGE_FOLDER = r"E:\Folder\Images"  # ✅ صحيح (لاحظ r قبل المسار)
IMAGE_FOLDER = "E:\Folder\Images"   # ❌ قد يسبب مشاكل
```

### خطأ 3: "Module not found"
```bash
pip install --upgrade requests pandas openpyxl pillow colorthief
```

### خطأ 4: "Insufficient credits"
- تحقق من رصيد API على platerecognizer.com
- قد تحتاج لترقية الخطة

---

## نصائح للنجاح / Success Tips

### ✅ جودة الصور
- دقة 800x600 أو أعلى
- إضاءة جيدة
- لوحة واضحة

### ✅ الأداء
- ابدأ بدفعة صغيرة (10-50 صورة) للاختبار
- راقب استهلاك API
- استخدم الحفظ الدوري

### ✅ الدقة
```python
# للسعودية فقط:
REGIONS = ['sa']

# لدول الخليج:
REGIONS = ['sa', 'ae', 'kw', 'qa', 'om', 'bh']

# للعالم كله:
REGIONS = []  # أو لا تحدد
```

---

## مثال كود مخصص / Custom Code Example

### معالجة دفعة صغيرة فقط
```python
# عدّل process_images() لمعالجة أول 100 صورة فقط:

for index, filename in enumerate(image_files[:100], 1):  # أضف [:100]
    # ... باقي الكود
```

### تصفية حسب الثقة
```python
# عدّل السطر 56 في السكربت:
MIN_CONFIDENCE = 0.8  # قبول فقط النتائج بثقة 80% أو أعلى
```

### تغيير التأخير
```python
# للمعالجة الأسرع (احذر من تجاوز الحد):
API_DELAY = 0.1  # 0.1 ثانية

# للمعالجة الآمنة:
API_DELAY = 1.0  # 1 ثانية
```

---

## الحصول على رمز API / Getting API Token

### 1. انتقل إلى Plate Recognizer
https://platerecognizer.com

### 2. سجل حساب جديد
- اضغط "Sign Up"
- أدخل بريدك الإلكتروني
- فعّل الحساب

### 3. احصل على الرمز
- سجل دخولك
- انتقل إلى Dashboard
- انسخ API Token
- يبدأ عادةً بـ `sk_` متبوعاً بأحرف وأرقام

### 4. الخطط المتاحة
- **مجانية:** 2,500 طلب/شهر
- **مدفوعة:** 10,000+ طلب/شهر
- **مؤسسات:** غير محدود

---

## دعم إضافي / Additional Support

### الوثائق الكاملة
- 📖 [EXTRACT_VEHICLES_GUIDE.md](EXTRACT_VEHICLES_GUIDE.md) - الدليل الشامل

### الأسئلة
- 🐛 GitHub Issues: https://github.com/Ali5829511/2025/issues

### Plate Recognizer
- 📚 Docs: https://docs.platerecognizer.com/
- 💬 Support: support@platerecognizer.com

---

## ملاحظة مهمة / Important Note

⚠️ **هذا السكربت يستخدم API خارجي وقد يستهلك رصيدك.**

- ابدأ بدفعة صغيرة للاختبار
- راقب الاستهلاك على لوحة التحكم
- احتفظ برمز API في مكان آمن

✅ **الاستخدام المسؤول**

---

تم إعداد هذا الدليل: نوفمبر 2024
