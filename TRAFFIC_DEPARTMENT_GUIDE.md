# دليل نظام قسم المرور
# Traffic Department System Guide

## نظرة عامة | Overview

نظام متكامل لإدارة قسم المرور في جامعة الإمام محمد بن سعود الإسلامية، يشمل إدارة المخالفات المرورية، الحوادث المرورية، السيارات المحجوزة، والتكامل مع نظام تمييز لوحات السيارات.

A comprehensive system for managing the Traffic Department at Imam Muhammad bin Saud Islamic University, including traffic violations management, traffic accidents management, impounded vehicles, and integration with license plate recognition system.

---

## المميزات الرئيسية | Key Features

### 1. إدارة المخالفات المرورية | Traffic Violations Management
- تسجيل المخالفات المرورية بجميع أنواعها
- متابعة حالة المخالفات (معلقة، تم حلها، تم الدفع)
- حساب الغرامات والرسوم
- ربط المخالفات بالمركبات وأصحابها
- إحصائيات وتقارير تفصيلية

### 2. إدارة الحوادث المرورية | Traffic Accidents Management
- تسجيل الحوادث المرورية بتفاصيل كاملة
- تصنيف الحوادث حسب الخطورة (بسيط، متوسط، خطير، حرج)
- ربط المركبات المتورطة في الحادث
- تتبع التحقيقات والإجراءات
- تسجيل الإصابات والوفيات
- تقدير الأضرار المادية

### 3. إدارة السيارات المحجوزة | Impounded Vehicles Management
- تسجيل السيارات المحجوزة أو المكبوحة
- متابعة الغرامات والرسوم المستحقة
- حساب رسوم السحب والتخزين
- ربط السيارات المحجوزة بالمخالفات المتسببة
- إجراءات الإفراج عن السيارات
- متابعة حالة الدفع

### 4. تمييز لوحات السيارات | License Plate Recognition
- التكامل مع خدمة platerecognizer.com
- التعرف التلقائي على لوحات السيارات من الصور
- ربط اللوحات المكتشفة بقاعدة البيانات
- تسجيل دخول وخروج المركبات
- تنبيهات للمركبات المخالفة

### 5. التقارير المتقدمة | Advanced Reports
- تقارير شاملة عن المخالفات
- تقارير الحوادث المرورية
- التقارير المالية للإيرادات
- إحصائيات متقدمة ورسوم بيانية
- تصدير التقارير بصيغ متعددة (PDF, Excel, CSV)

---

## هيكل قاعدة البيانات | Database Structure

### جدول المخالفات المرورية | traffic_violations
```sql
- id: معرف فريد
- vehicle_id: معرف المركبة
- violation_type: نوع المخالفة
- violation_date: تاريخ ووقت المخالفة
- location: موقع المخالفة
- description: وصف المخالفة
- fine_amount: قيمة الغرامة
- status: الحالة (pending, resolved, paid, cancelled)
- reported_by: المسؤول المسجل
- created_at: تاريخ الإنشاء
- updated_at: تاريخ آخر تحديث
```

### جدول الحوادث المرورية | traffic_accidents
```sql
- id: معرف فريد
- accident_number: رقم الحادث
- accident_date: تاريخ ووقت الحادث
- location: موقع الحادث
- description: وصف الحادث
- severity: الخطورة (minor, moderate, major, critical)
- weather_conditions: الظروف الجوية
- road_conditions: حالة الطريق
- vehicles_involved: عدد المركبات المتورطة
- injuries_count: عدد الإصابات
- fatalities_count: عدد الوفيات
- damage_estimate: تقدير الأضرار
- police_report_number: رقم محضر الشرطة
- insurance_claim_number: رقم المطالبة التأمينية
- status: الحالة (reported, investigated, resolved)
- reported_by: المبلغ
- investigated_by: المحقق
- resolution: الحل
- created_at: تاريخ الإنشاء
- updated_at: تاريخ آخر تحديث
- resolved_at: تاريخ الحل
```

### جدول المركبات المتورطة في الحادث | accident_vehicles
```sql
- id: معرف فريد
- accident_id: معرف الحادث
- vehicle_id: معرف المركبة (اختياري)
- plate_number: رقم اللوحة
- driver_name: اسم السائق
- driver_phone: هاتف السائق
- driver_license: رقم رخصة القيادة
- vehicle_owner_id: معرف مالك المركبة
- damage_description: وصف الأضرار
- at_fault: المتسبب (0/1)
- insurance_info: معلومات التأمين
- notes: ملاحظات
- created_at: تاريخ الإنشاء
```

### جدول السيارات المحجوزة | immobilized_cars
```sql
- id: معرف فريد
- vehicle_id: معرف المركبة (اختياري)
- plate_number: رقم اللوحة
- immobilization_type: نوع الحجز (boot, tow, compound)
- reason: سبب الحجز
- location: موقع الحجز
- immobilized_date: تاريخ الحجز
- release_date: تاريخ الإفراج
- immobilized_by: المسؤول عن الحجز
- released_by: المسؤول عن الإفراج
- outstanding_fines: الغرامات المستحقة
- towing_fee: رسوم السحب
- storage_fee: رسوم التخزين
- total_fees: إجمالي الرسوم
- payment_status: حالة الدفع (paid, unpaid, partial)
- payment_date: تاريخ الدفع
- status: الحالة (immobilized, released)
- violation_count: عدد المخالفات
- notes: ملاحظات
- created_at: تاريخ الإنشاء
- updated_at: تاريخ آخر تحديث
```

### جدول ربط السيارات المحجوزة بالمخالفات | immobilized_car_violations
```sql
- id: معرف فريد
- immobilized_car_id: معرف السيارة المحجوزة
- violation_id: معرف المخالفة
- linked_at: تاريخ الربط
```

---

## واجهات برمجة التطبيقات | API Endpoints

### المخالفات المرورية | Traffic Violations
```
GET    /api/traffic-violations          - الحصول على قائمة المخالفات
POST   /api/traffic-violations          - إضافة مخالفة جديدة
GET    /api/traffic-violations/:id      - الحصول على تفاصيل مخالفة
PUT    /api/traffic-violations/:id      - تحديث مخالفة
DELETE /api/traffic-violations/:id      - حذف مخالفة
```

### الحوادث المرورية | Traffic Accidents
```
GET    /api/traffic-accidents           - الحصول على قائمة الحوادث
POST   /api/traffic-accidents           - تسجيل حادث جديد
GET    /api/traffic-accidents/:id       - الحصول على تفاصيل حادث
PUT    /api/traffic-accidents/:id       - تحديث حادث
DELETE /api/traffic-accidents/:id       - حذف حادث
```

### السيارات المحجوزة | Immobilized Cars
```
GET    /api/immobilized-cars            - الحصول على قائمة السيارات المحجوزة
POST   /api/immobilized-cars            - حجز سيارة جديدة
GET    /api/immobilized-cars/:id        - الحصول على تفاصيل سيارة محجوزة
PUT    /api/immobilized-cars/:id        - تحديث حالة سيارة محجوزة
DELETE /api/immobilized-cars/:id        - حذف سجل سيارة محجوزة
```

### الإحصائيات | Statistics
```
GET    /api/traffic-department/statistics  - إحصائيات شاملة لقسم المرور
```

### تمييز لوحات السيارات | Plate Recognition
```
GET    /api/plate-recognizer/status     - حالة خدمة تمييز اللوحات
POST   /api/plate-recognizer/recognize  - تمييز لوحة من صورة
GET    /api/plate-recognizer/history    - سجل عمليات التمييز
```

---

## الصفحات الرئيسية | Main Pages

### 1. لوحة تحكم قسم المرور | Traffic Department Dashboard
**الملف:** `traffic_department_dashboard.html`

**المميزات:**
- عرض إحصائيات شاملة (المخالفات، الحوادث، السيارات المحجوزة، الإيرادات)
- روابط سريعة للأنظمة الفرعية
- رسوم بيانية تحليلية
- النشاطات الأخيرة

### 2. إدارة المخالفات المرورية | Traffic Violations Management
**الملف:** `enhanced_traffic_violations_updated.html`

**المميزات:**
- تسجيل مخالفات جديدة
- البحث والتصفية
- عرض وتحرير المخالفات
- ربط المخالفات بالمركبات
- طباعة المخالفات

### 3. إدارة الحوادث المرورية | Traffic Accidents Management
**الملف:** `enhanced_traffic_accidents.html`

**المميزات:**
- تسجيل حوادث جديدة
- ربط المركبات المتورطة
- تسجيل التحقيقات
- إحصائيات الحوادث
- التقارير التفصيلية

### 4. إدارة السيارات المحجوزة | Immobilized Cars Management
**الملف:** `enhanced_immobilized_cars.html`

**المميزات:**
- تسجيل سيارات محجوزة
- متابعة الرسوم والغرامات
- إجراءات الإفراج
- سجل الدفعات
- التقارير

### 5. تمييز لوحات السيارات | License Plate Recognition
**الملف:** `plate_recognition.html`

**المميزات:**
- رفع صور اللوحات
- التعرف التلقائي على اللوحات
- ربط بقاعدة البيانات
- سجل العمليات
- الإحصائيات

### 6. التقارير المتقدمة | Advanced Reports
**الملف:** `traffic_reports.html`

**المميزات:**
- تقارير مخصصة
- تقارير سريعة جاهزة
- رسوم بيانية تحليلية
- تصدير بصيغ متعددة
- الطباعة

---

## التكامل مع Plate Recognizer

### إعداد الخدمة | Service Setup

1. **الحصول على API Token:**
   - زيارة https://app.platerecognizer.com/
   - إنشاء حساب أو تسجيل الدخول
   - نسخ API Token من لوحة التحكم

2. **إعداد ملف البيئة:**
   ```bash
   # في ملف .env
   PLATE_RECOGNIZER_API_TOKEN=your-actual-api-token-here
   PLATE_RECOGNIZER_API_URL=https://api.platerecognizer.com/v1/plate-reader/
   ```

3. **رابط Dashboard الخاص:**
   https://app.platerecognizer.com/service/snapshot-cloud/dashboard/22ba3cf7155a1ea730a0b64787f98ab5f9a3de94

### استخدام الخدمة | Using the Service

```python
import plate_recognizer

# التحقق من حالة الخدمة
status = plate_recognizer.get_api_status()

# تمييز لوحة من ملف صورة
result = plate_recognizer.recognize_plate_from_file(
    'path/to/image.jpg',
    regions=['sa']  # للمملكة العربية السعودية
)

# تمييز لوحة من base64
result = plate_recognizer.recognize_plate_from_base64(
    base64_image_string,
    regions=['sa']
)

# البحث عن مركبة برقم اللوحة
vehicle = plate_recognizer.find_vehicle_by_plate('ABC1234')
```

---

## الصلاحيات | Permissions

### مدير النظام | System Administrator (admin)
- الوصول الكامل لجميع الوظائف
- إضافة وتحرير وحذف جميع البيانات
- إدارة المستخدمين
- الوصول للتقارير المتقدمة

### مسؤول المخالفات | Violations Officer (violations)
- تسجيل وإدارة المخالفات المرورية
- تسجيل وإدارة الحوادث المرورية
- حجز وإفراج السيارات
- الوصول للتقارير
- لا يمكنه حذف البيانات

### مستخدم الاستعلام | Viewer (viewer)
- عرض البيانات فقط
- لا يمكنه إضافة أو تحرير أو حذف

### مسجل المخالفات | Violation Entry (violation_entry)
- تسجيل المخالفات المرورية فقط
- عرض المخالفات المسجلة
- لا يمكنه تحرير أو حذف

---

## التثبيت والتشغيل | Installation and Running

### المتطلبات | Requirements
```bash
Python 3.8+
Flask 3.0.0
Werkzeug 3.0.3
SQLite 3
```

### التثبيت | Installation
```bash
# تثبيت المتطلبات
pip install -r requirements.txt

# إنشاء قاعدة البيانات
python database.py
```

### التشغيل | Running
```bash
# تشغيل الخادم
python server.py

# الوصول للنظام
http://localhost:5000
```

---

## الأمان | Security

### اعتبارات الأمان | Security Considerations

1. **كلمات المرور:**
   - جميع كلمات المرور مشفرة باستخدام pbkdf2:sha256
   - يجب تغيير كلمات المرور الافتراضية

2. **الجلسات:**
   - إدارة جلسات آمنة مع انتهاء صلاحية تلقائي
   - رموز جلسات فريدة لكل مستخدم

3. **صلاحيات الوصول:**
   - نظام صلاحيات متعدد المستويات
   - التحقق من الصلاحيات في كل عملية

4. **سجل التدقيق:**
   - تسجيل جميع العمليات الحساسة
   - متابعة من قام بماذا ومتى

5. **للإنتاج:**
   - استخدام HTTPS
   - تعطيل وضع التصحيح
   - استخدام خادم WSGI إنتاجي (Gunicorn)
   - تشفير البيانات الحساسة

---

## الدعم الفني | Technical Support

للحصول على الدعم الفني أو الإبلاغ عن مشاكل:
- البريد الإلكتروني: it-support@university.edu.sa
- الهاتف: +966-11-XXXXXXX
- ساعات العمل: الأحد - الخميس، 8:00 صباحاً - 4:00 مساءً

For technical support or to report issues:
- Email: it-support@university.edu.sa
- Phone: +966-11-XXXXXXX
- Working Hours: Sunday - Thursday, 8:00 AM - 4:00 PM

---

## الإصدار | Version

**الإصدار:** 2.0.1
**تاريخ الإصدار:** 2025
**المطور:** قسم تقنية المعلومات - جامعة الإمام محمد بن سعود الإسلامية

**Version:** 2.0.1
**Release Date:** 2025
**Developer:** IT Department - Imam Mohammad Ibn Saud Islamic University

---

## الترخيص | License

جميع الحقوق محفوظة © جامعة الإمام محمد بن سعود الإسلامية 2025

All rights reserved © Imam Mohammad Ibn Saud Islamic University 2025
