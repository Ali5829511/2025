# استيراد بيانات منصة إيجار / Ejar Platform Data Import

## نظرة عامة / Overview

هذا الملف يوثق عملية استيراد البيانات من منصة إيجار السعودية إلى نظام إدارة إسكان أعضاء هيئة التدريس.

This document details the process of importing data from the Saudi Ejar platform into the Faculty Housing Management System.

---

## 🔗 عن منصة إيجار / About Ejar Platform

**منصة إيجار** هي منصة إلكترونية وطنية سعودية لتوثيق وتنظيم عقود الإيجار السكنية والتجارية.

**Ejar Platform** is the Saudi national electronic platform for documenting and organizing residential and commercial rental contracts.

🌐 **الموقع الإلكتروني / Website:** https://eservices.ejar.sa/ar/dashboard

---

## 📦 الملفات المتضمنة / Included Files

| الملف | الوصف | Description |
|-------|-------|-------------|
| `import_ejar_data.py` | سكريبت استيراد بيانات إيجار | Ejar data import script |
| `ejar_import.html` | واجهة الاستيراد | Import interface page |
| `ejar_template.csv` | ملف نموذجي | Sample template file |
| `EJAR_IMPORT_README.md` | هذا الملف | This documentation file |

---

## 🎯 البيانات المدعومة / Supported Data

يدعم السكريبت استيراد البيانات التالية من منصة إيجار:

The script supports importing the following data from Ejar:

- ✅ **العقارات** (فلل وعمارات) / Properties (Villas & Apartments)
- ✅ **المستأجرين** (السكان) / Tenants (Residents)
- ✅ **الملاك** (أصحاب العقارات) / Owners (Property Owners)
- ✅ **عقود الإيجار** / Rental Contracts
- ✅ **معلومات الاتصال** / Contact Information
- ✅ **التواريخ والحالات** / Dates & Status

---

## 📋 تنسيق الملف المطلوب / Required File Format

### الصيغ المدعومة / Supported Formats
- CSV (Comma-Separated Values)
- TSV (Tab-Separated Values)
- Excel (.xlsx)

### الترميز المطلوب / Required Encoding
- UTF-8 أو UTF-8 with BOM

### الأعمدة المطلوبة / Required Columns

| اسم العمود<br>Column Name | الوصف<br>Description | مثال<br>Example | إلزامي<br>Required |
|-------------------------|-------------------|--------------|----------------|
| نوع_العقار | نوع العقار (فلة/عمارة) | فلة | ✓ |
| رقم_العقار | رقم العقار أو الوحدة | 1 أو 101 | ✓ |
| اسم_المالك | اسم مالك العقار | إدارة الجامعة | |
| رقم_هوية_المالك | رقم هوية المالك | 1000000001 | |
| اسم_المستأجر | اسم المستأجر الكامل | أحمد بن محمد | ✓ |
| رقم_هوية_المستأجر | رقم الهوية الوطنية | 1234567890 | ✓ |
| جوال_المستأجر | رقم الجوال | 0501234567 | |
| بريد_المستأجر | البريد الإلكتروني | ahmed@email.com | |
| تاريخ_بدء_العقد | تاريخ بدء الإيجار | 2024-01-01 | |
| تاريخ_انتهاء_العقد | تاريخ انتهاء الإيجار | 2025-12-31 | |
| قيمة_الإيجار_السنوي | قيمة الإيجار (ريال) | 60000 | |
| حالة_العقد | حالة العقد | نشط | |
| ملاحظات | ملاحظات إضافية | عضو هيئة التدريس | |

---

## 🚀 طرق الاستيراد / Import Methods

### الطريقة 1: من خلال الواجهة / Via Web Interface

1. افتح المتصفح على / Open browser at:
   ```
   http://localhost:5000/ejar_import.html
   ```

2. اتبع التعليمات الموضحة في الصفحة
   Follow the instructions on the page

### الطريقة 2: من خلال سطر الأوامر / Via Command Line

#### استيراد من ملف / Import from File
```bash
python3 import_ejar_data.py ejar_export.csv
```

#### استيراد بيانات نموذجية / Import Sample Data
```bash
python3 import_ejar_data.py --sample
```

---

## 📝 خطوات تصدير البيانات من إيجار / Steps to Export from Ejar

### 1️⃣ تسجيل الدخول / Login
```
https://eservices.ejar.sa
```
قم بتسجيل الدخول باستخدام حسابك / Login with your account

### 2️⃣ الانتقال إلى العقارات / Navigate to Properties
انتقل إلى قسم "عقاراتي" أو "العقود"  
Go to "My Properties" or "Contracts" section

### 3️⃣ تصدير البيانات / Export Data
ابحث عن خيار "تصدير" أو "Export"  
Look for "Export" or "تصدير" option

اختر صيغة CSV أو Excel  
Choose CSV or Excel format

### 4️⃣ حفظ الملف / Save File
احفظ الملف في جهازك  
Save the file to your computer

### 5️⃣ استيراد إلى النظام / Import to System
استخدم أحد طرق الاستيراد المذكورة أعلاه  
Use one of the import methods mentioned above

---

## ✨ المميزات / Features

### ✅ استيراد ذكي / Smart Import
- كشف تلقائي للسجلات المكررة / Automatic duplicate detection
- إنشاء تلقائي للمباني والوحدات / Auto-creation of buildings and units
- معالجة آمنة للأخطاء / Safe error handling
- تجاهل السجلات غير الكاملة / Skip incomplete records

### 📊 تقارير مفصلة / Detailed Reports
```
======================================================================
📊 Ejar Import Summary / ملخص استيراد بيانات إيجار:
======================================================================
   ✅ Successfully imported / تم الاستيراد بنجاح: 10
   ⏭️  Skipped (duplicates) / تم التخطي (مكرر): 0
   ❌ Errors / أخطاء: 0
   📝 Total processed / إجمالي المعالج: 10
======================================================================
```

### 🔐 أمان البيانات / Data Security
- استعلامات SQL معاملية / Parameterized SQL queries
- التحقق من صحة البيانات / Data validation
- سجل التدقيق / Audit logging
- حماية من SQL Injection

---

## 🧪 اختبار الاستيراد / Testing Import

### اختبار سريع / Quick Test
```bash
# استيراد البيانات النموذجية / Import sample data
python3 import_ejar_data.py --sample

# التحقق من النتائج / Verify results
sqlite3 housing.db "SELECT COUNT(*) FROM residents;"
sqlite3 housing.db "SELECT COUNT(*) FROM buildings;"
```

### التحقق من البيانات / Verify Data
افتح المتصفح على / Open browser at:
- http://localhost:5000/housing_report.html
- http://localhost:5000/residents_management_updated.html
- http://localhost:5000/buildings_management_updated.html

---

## 🔧 استكشاف الأخطاء / Troubleshooting

### خطأ: قاعدة البيانات غير موجودة
**Error: Database not found**

```bash
# الحل / Solution
python3 database.py
```

### خطأ: ملف البيانات غير موجود
**Error: Data file not found**

```bash
# تحقق من المسار / Check path
ls -la ejar_export.csv

# تحقق من المجلد الحالي / Check current directory
pwd
```

### خطأ: صيغة التاريخ غير صحيحة
**Error: Invalid date format**

التواريخ يجب أن تكون بصيغة / Dates must be in format:
```
YYYY-MM-DD
مثال / Example: 2024-01-01
```

### تحذير: سجل مكرر
**Warning: Duplicate record**

هذا طبيعي - النظام يحمي البيانات من التكرار تلقائياً  
This is normal - the system protects data from duplication automatically

---

## 📚 مراجع إضافية / Additional Resources

### الوثائق / Documentation
- [دليل الاستيراد الشامل](IMPORT_GUIDE.md)
- [قاعدة البيانات](DATABASE.md)
- [دليل المستخدم](../../README.md)

### الأدوات / Tools
- [واجهة استيراد إيجار](ejar_import.html)
- [صفحة الاستيراد الرئيسية](import_data.html)
- [تقرير الإسكان](housing_report.html)

---

## 🆘 الدعم / Support

للحصول على الدعم، يرجى:  
For support, please:

1. مراجعة الوثائق أعلاه / Review documentation above
2. فحص رسائل الخطأ / Check error messages
3. اختبار البيانات النموذجية / Test with sample data
4. التواصل مع فريق تقنية المعلومات / Contact IT team

---

## 📄 الترخيص / License

جميع الحقوق محفوظة © جامعة الإمام محمد بن سعود الإسلامية 2025  
All rights reserved © Imam Mohammad Ibn Saud Islamic University 2025

---

## 🔄 التحديثات / Updates

**الإصدار 1.0** - نوفمبر 2024
- إصدار أولي مع دعم كامل لاستيراد بيانات إيجار
- Initial release with full Ejar data import support

---

**تم التطوير بواسطة / Developed by:** GitHub Copilot  
**التاريخ / Date:** نوفمبر 2024 / November 2024
