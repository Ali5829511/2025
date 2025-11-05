# دليل استيراد بيانات السكان / Residents Data Import Guide

## نظرة عامة / Overview

يوفر هذا الدليل معلومات شاملة حول كيفية استيراد بيانات السكان إلى قاعدة البيانات.

This guide provides comprehensive information on how to import resident data into the database.

---

## الطريقة الأولى: استيراد البيانات من ملف CSV
## Method 1: Import Data from CSV File

### تنسيق الملف المطلوب / Required File Format

يجب أن يكون ملف CSV بالتنسيق التالي (مفصول بـ Tab):

```
م	الاسم	الوحدة السكنية	فلة/عمارة	رقم المبنى	رقم الشقة	رقم الجوال	رقم الموقف	مربع الوقوف
1	يحيى بن علي بن يحيى العمري	فلة	فلة	1	0	504444120	0	0
2	مشبب بن سعيد بن ظويفر القحطاني	فلة	فلة	2	0	507665005	0	0
```

**الأعمدة المطلوبة / Required Columns:**
1. `م` - رقم تسلسلي (Sequence number)
2. `الاسم` - اسم الساكن الكامل (Full name)
3. `الوحدة السكنية` - نوع الوحدة (Unit type: فلة/عمارة)
4. `فلة/عمارة` - نوع المبنى (Building type: villa/apartment)
5. `رقم المبنى` - رقم المبنى (Building number)
6. `رقم الشقة` - رقم الشقة (Unit number, 0 for villas)
7. `رقم الجوال` - رقم الجوال (Phone number)
8. `رقم الموقف` - رقم الموقف (Parking number)
9. `مربع الوقوف` - مربع الوقوف (Parking spot)

### خطوات الاستيراد / Import Steps

#### 1. احفظ البيانات في ملف
Save your data to a file named `residents_data.csv`

#### 2. شغّل سكريبت الاستيراد
Run the import script:

```bash
python3 import_residents_data.py residents_data.csv
```

#### 3. تحقق من النتائج
Check the results in the console output.

---

## الطريقة الثانية: استيراد البيانات النموذجية
## Method 2: Import Sample Data

لاستيراد البيانات النموذجية المدمجة في السكريبت:

```bash
python3 import_residents_data.py --sample
```

هذا سيستورد 30 سجل نموذجي من سكان الفلل.

This will import 30 sample villa resident records.

---

## الميزات / Features

### ✅ الميزات المضمنة / Built-in Features

1. **التحقق من التكرار** - يتخطى السجلات المكررة تلقائياً
   - **Duplicate Detection** - Automatically skips duplicate records

2. **إنشاء المباني تلقائياً** - ينشئ سجلات المباني إذا لم تكن موجودة
   - **Auto-create Buildings** - Creates building records if they don't exist

3. **معالجة الأخطاء** - يتعامل مع البيانات غير الصحيحة بشكل آمن
   - **Error Handling** - Safely handles invalid data

4. **تقارير مفصلة** - يعرض ملخص شامل بعد الاستيراد
   - **Detailed Reports** - Shows comprehensive summary after import

### 📊 تقرير الاستيراد / Import Report

بعد الاستيراد، سترى ملخصاً يحتوي على:

```
📊 Import Summary:
   ✅ Successfully imported: 25
   ⏭️  Skipped (duplicates): 3
   ❌ Errors: 2
   📝 Total processed: 30
```

---

## أمثلة الاستخدام / Usage Examples

### مثال 1: استيراد بيانات الفلل
Example 1: Import Villa Data

```bash
# حفظ بيانات الفلل في ملف
# Save villa data to file
cat > villas.csv << 'EOF'
م	الاسم	الوحدة السكنية	فلة/عمارة	رقم المبنى	رقم الشقة	رقم الجوال	رقم الموقف	مربع الوقوف
1	أحمد بن محمد	فلة	فلة	1	0	501234567	0	0
2	سعيد بن علي	فلة	فلة	2	0	502345678	0	0
EOF

# تشغيل الاستيراد
# Run import
python3 import_residents_data.py villas.csv
```

### مثال 2: استيراد بيانات العمارات
Example 2: Import Apartment Data

```bash
cat > apartments.csv << 'EOF'
م	الاسم	الوحدة السكنية	فلة/عمارة	رقم المبنى	رقم الشقة	رقم الجوال	رقم الموقف	مربع الوقوف
1	خالد بن سعود	عمارة	عمارة	1	101	503456789	45	A12
2	فهد بن عبدالله	عمارة	عمارة	1	102	504567890	46	A13
EOF

python3 import_residents_data.py apartments.csv
```

---

## استكشاف الأخطاء / Troubleshooting

### خطأ: قاعدة البيانات غير موجودة
Error: Database not found

```bash
❌ Database file 'housing.db' not found!
```

**الحل / Solution:**
```bash
python3 database.py
```

### خطأ: ملف البيانات غير موجود
Error: Data file not found

```bash
❌ File 'residents_data.csv' not found!
```

**الحل / Solution:**
تأكد من وجود الملف في المجلد الحالي
- Ensure the file exists in the current directory

### تحذير: سجل مكرر
Warning: Duplicate record

```bash
ℹ️  Resident 'أحمد بن محمد' already exists in فلة 1, skipping...
```

**الحل / Solution:**
هذا طبيعي - السكريبت يتخطى السجلات المكررة تلقائياً
- This is normal - the script automatically skips duplicates

---

## التحقق من البيانات / Data Verification

بعد الاستيراد، يمكنك التحقق من البيانات بعدة طرق:

### 1. عرض التقرير التفاعلي
View Interactive Report

```
http://localhost:5000/housing_report.html
```

### 2. عرض صفحة الاختبار
View Test Page

```
http://localhost:5000/test_data_display.html
```

### 3. الاستعلام المباشر من قاعدة البيانات
Direct Database Query

```bash
sqlite3 housing.db
```

```sql
-- عرض جميع السكان
-- Show all residents
SELECT * FROM residents;

-- عرض إحصائيات
-- Show statistics
SELECT 
    COUNT(*) as total_residents,
    COUNT(DISTINCT building_id) as total_buildings
FROM residents;
```

---

## ملاحظات مهمة / Important Notes

### 🔒 الأمان / Security

- السكريبت يستخدم parameterized queries لمنع SQL injection
- The script uses parameterized queries to prevent SQL injection

- يتحقق من صحة البيانات قبل الإدراج
- Validates data before insertion

### 📝 التكامل / Integration

- البيانات المستوردة تظهر فوراً في التقارير
- Imported data appears immediately in reports

- يتم تسجيل جميع العمليات في audit_log
- All operations are logged in audit_log

- يمكن استيراد البيانات عدة مرات بأمان
- Data can be imported multiple times safely

### 🔄 التحديث / Updates

لتحديث بيانات ساكن موجود:
To update existing resident data:

1. احذف السجل القديم من واجهة الإدارة
   - Delete old record from admin interface

2. أعد استيراد البيانات المحدثة
   - Re-import updated data

---

## الدعم / Support

إذا واجهت أي مشاكل:
If you encounter any issues:

1. تحقق من تنسيق ملف CSV
   - Check CSV file format

2. تأكد من تشغيل قاعدة البيانات
   - Ensure database is running

3. راجع رسائل الخطأ في console
   - Review error messages in console

4. استخدم البيانات النموذجية للاختبار
   - Use sample data for testing

---

## أمثلة إضافية / Additional Examples

### استيراد بيانات من Excel

1. احفظ ملف Excel كـ CSV (UTF-8)
   - Save Excel file as CSV (UTF-8)

2. تأكد من الفصل بـ Tab
   - Ensure tab-separated format

3. شغّل السكريبت
   - Run the script

### استيراد بيانات كبيرة

للملفات الكبيرة (أكثر من 1000 سجل):
For large files (more than 1000 records):

```bash
# قد يستغرق بعض الوقت
# May take some time
python3 import_residents_data.py large_dataset.csv
```

السكريبت يعالج السجلات تدريجياً ويعرض التقدم.
The script processes records progressively and shows progress.

---

## الخلاصة / Summary

✅ سهل الاستخدام - يدعم استيراد CSV وبيانات نموذجية
- **Easy to use** - Supports CSV import and sample data

✅ آمن - يمنع التكرار والأخطاء
- **Safe** - Prevents duplicates and errors

✅ شامل - تقارير مفصلة ومعالجة أخطاء
- **Comprehensive** - Detailed reports and error handling

✅ مرن - يعمل مع الفلل والعمارات
- **Flexible** - Works with villas and apartments
