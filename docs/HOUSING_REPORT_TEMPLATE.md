# تقرير تفصيلي شامل: بيانات وحدة إسكان هيئة التدريس
# Comprehensive Detailed Report: Faculty Housing Unit Data

**تاريخ التقرير / Report Date:** يتم إنشاؤه تلقائياً  
**نوع التقرير / Report Type:** تحليل شامل للبيانات  
**الحالة / Status:** قالب ديناميكي - يتم ملؤه من قاعدة البيانات

---

## المقدمة / Introduction

يقدم هذا التقرير تحليلاً تفصيلياً وشاملاً لجميع البيانات المتوفرة في وحدة إسكان هيئة التدريس. يتضمن التقرير إحصائيات مفصلة عن المباني، الوحدات السكنية، السكان، المواقف، وملصقات السيارات، بالإضافة إلى قوائم تفصيلية وتوزيعات حسب المباني والمناطق.

This report provides a detailed and comprehensive analysis of all available data in the Faculty Housing Unit. The report includes detailed statistics on buildings, residential units, residents, parking spaces, and vehicle stickers, in addition to detailed lists and distributions by buildings and areas.

تم إعداد هذا التقرير بناءً على البيانات المستخرجة مباشرة من قاعدة البيانات، مع التأكد من دقة جميع الأرقام والإحصائيات.

This report has been prepared based on data extracted directly from the database, ensuring the accuracy of all numbers and statistics.

---

## القسم الأول: المباني / Section One: Buildings

### 1.1 نظرة عامة / Overview

يحتوي النظام على **{total_buildings}** مبنى موزعة كالتالي:

The system contains **{total_buildings}** buildings distributed as follows:

| نوع المبنى<br>Building Type | العدد<br>Count | النسبة<br>Percentage |
|---------------------------|--------------|-------------------|
| عمارة<br>Apartment Building | {apartment_count} | {apartment_percentage}% |
| فيلا<br>Villa | {villa_count} | {villa_percentage}% |
| **الإجمالي<br>Total** | **{total_buildings}** | **100%** |

---

### 1.2 المباني القديمة / Old Buildings (عمارة 1-30)

تحتوي المباني القديمة على **{old_building_count}** عمارة بإجمالي **{old_total_units}** وحدة سكنية.

The old buildings contain **{old_building_count}** apartment buildings with a total of **{old_total_units}** residential units.

| رقم المبنى<br>Building No. | عدد الوحدات<br>Units | عدد السكان<br>Residents | عدد المواقف<br>Parking | نسبة الإشغال<br>Occupancy |
|------------------------|-----------------|-------------------|-------------------|---------------------|
| عمارة 1 | 20 | {residents_b1} | {parking_b1} | {occupancy_b1}% |
| عمارة 2 | 20 | {residents_b2} | {parking_b2} | {occupancy_b2}% |
| ... | ... | ... | ... | ... |
| **الإجمالي<br>Total** | **{old_total_units}** | **{old_total_residents}** | **{old_total_parking}** | **{old_avg_occupancy}%** |

**ملاحظات مهمة / Important Notes:**
- نسبة الإشغال / Occupancy Rate: **{old_avg_occupancy}%**
- متوسط السكان لكل مبنى / Average Residents per Building: **{old_avg_residents}**
- متوسط المواقف لكل مبنى / Average Parking per Building: **{old_avg_parking}**

---

### 1.3 المباني الجديدة / New Buildings (عمارة 53-79)

تحتوي المباني الجديدة على **{new_building_count}** عمارة بإجمالي **{new_total_units}** وحدة سكنية.

The new buildings contain **{new_building_count}** apartment buildings with a total of **{new_total_units}** residential units.

| رقم المبنى<br>Building No. | عدد الوحدات<br>Units | عدد السكان<br>Residents | عدد المواقف<br>Parking | نسبة الإشغال<br>Occupancy |
|------------------------|-----------------|-------------------|-------------------|---------------------|
| عمارة 53 | 20 | {residents_b53} | {parking_b53} | {occupancy_b53}% |
| عمارة 54 | 20 | {residents_b54} | {parking_b54} | {occupancy_b54}% |
| ... | ... | ... | ... | ... |
| **الإجمالي<br>Total** | **{new_total_units}** | **{new_total_residents}** | **{new_total_parking}** | **{new_avg_occupancy}%** |

**ملاحظات مهمة / Important Notes:**
- التطابق التام / Perfect Match: عدد المواقف يساوي عدد السكان بالضبط
- نسبة الإشغال / Occupancy Rate: **{new_avg_occupancy}%**
- أعلى إشغال / Highest Occupancy: **{highest_occupancy_building}**
- أقل إشغال / Lowest Occupancy: **{lowest_occupancy_building}**

---

### 1.4 الفلل / Villas ({villa_count} فيلا)

تحتوي الوحدة على **{villa_count}** فيلا موزعة على أرقام مختلفة.

The unit contains **{villa_count}** villas distributed across different numbers.

| رقم الفيلا<br>Villa No. | عدد السكان<br>Residents | الحالة<br>Status |
|---------------------|-------------------|--------------|
| فيلا {villa_1} | {residents_v1} | {status_v1} |
| فيلا {villa_2} | {residents_v2} | {status_v2} |
| ... | ... | ... |
| **الإجمالي<br>Total** | **{villa_total_residents}** | - |

**ملاحظة / Note:** الفلل ليس لها مواقف مخصصة في نظام المواقف المشتركة، حيث تحتوي كل فيلا على مواقف داخلية خاصة ضمن حدودها.

Villas do not have designated parking in the shared parking system, as each villa contains its own internal parking within its boundaries.

---

## القسم الثاني: الوحدات السكنية / Section Two: Residential Units

### 2.1 نظرة عامة / Overview

| المؤشر<br>Indicator | القيمة<br>Value |
|-----------------|-------------|
| إجمالي الوحدات<br>Total Units | **{total_units}** |
| الشقق<br>Apartments | {apartment_units} ({apartment_units_percentage}%) |
| الفلل<br>Villas | {villa_units} ({villa_units_percentage}%) |

---

### 2.2 حالة الإشغال / Occupancy Status

| الحالة<br>Status | العدد<br>Count | النسبة<br>Percentage |
|--------------|------------|----------------|
| مشغول<br>Occupied | **{occupied_units}** | **{occupied_percentage}%** |
| شاغر<br>Vacant | **{vacant_units}** | **{vacant_percentage}%** |
| **الإجمالي<br>Total** | **{total_units}** | **100%** |

---

### 2.3 قائمة الوحدات الشاغرة / List of Vacant Units ({vacant_units} وحدة)

| رقم المبنى<br>Building No. | رقم الشقة<br>Unit No. | نوع الوحدة<br>Unit Type | الملاحظات<br>Notes |
|------------------------|------------------|------------------|---------------|
| {building_1} | {unit_1} | {type_1} | {notes_1} |
| {building_2} | {unit_2} | {type_2} | {notes_2} |
| ... | ... | ... | ... |

---

## القسم الثالث: السكان / Section Three: Residents

### 3.1 الإحصائيات العامة / General Statistics

| المؤشر<br>Indicator | القيمة<br>Value |
|-----------------|-------------|
| إجمالي السكان<br>Total Residents | **{total_residents}** |
| سكان العمارات<br>Apartment Residents | {apartment_residents} ({apartment_residents_percentage}%) |
| سكان الفلل<br>Villa Residents | {villa_residents} ({villa_residents_percentage}%) |
| متوسط السكان لكل وحدة<br>Average Residents per Unit | **{avg_residents_per_unit}** |

---

### 3.2 التوزيع حسب نوع المبنى / Distribution by Building Type

| نوع المبنى<br>Building Type | عدد السكان<br>Residents | النسبة<br>Percentage | متوسط السكان<br>Average |
|---------------------------|-------------------|----------------|-----------------|
| المباني القديمة<br>Old Buildings | {old_residents} | {old_residents_percentage}% | {old_avg_residents} |
| المباني الجديدة<br>New Buildings | {new_residents} | {new_residents_percentage}% | {new_avg_residents} |
| الفلل<br>Villas | {villa_residents} | {villa_residents_percentage}% | {villa_avg_residents} |
| **الإجمالي<br>Total** | **{total_residents}** | **100%** | **{overall_avg}** |

---

## القسم الرابع: المواقف / Section Four: Parking

### 4.1 الإحصائيات العامة / General Statistics

| المؤشر<br>Indicator | القيمة<br>Value |
|-----------------|-------------|
| إجمالي المواقف<br>Total Parking Spaces | **{total_parking}** |
| المواقف المشغولة<br>Occupied Parking | {occupied_parking} ({occupied_parking_percentage}%) |
| المواقف الشاغرة<br>Vacant Parking | {vacant_parking} ({vacant_parking_percentage}%) |

---

### 4.2 التوزيع حسب المبنى / Distribution by Building

| نوع المبنى<br>Building Type | عدد المواقف<br>Parking Spaces | النسبة<br>Percentage |
|---------------------------|--------------------------|----------------|
| المباني القديمة<br>Old Buildings | {old_parking} | {old_parking_percentage}% |
| المباني الجديدة<br>New Buildings | {new_parking} | {new_parking_percentage}% |
| **الإجمالي<br>Total** | **{total_parking}** | **100%** |

**ملاحظة / Note:** الفلل لا تشمل في نظام المواقف المشتركة.

Villas are not included in the shared parking system.

---

## القسم الخامس: المركبات والملصقات / Section Five: Vehicles and Stickers

### 5.1 إحصائيات المركبات / Vehicle Statistics

| المؤشر<br>Indicator | القيمة<br>Value |
|-----------------|-------------|
| إجمالي المركبات المسجلة<br>Total Registered Vehicles | **{total_vehicles}** |
| المركبات النشطة<br>Active Vehicles | {active_vehicles} ({active_vehicles_percentage}%) |
| المركبات غير النشطة<br>Inactive Vehicles | {inactive_vehicles} ({inactive_vehicles_percentage}%) |

---

### 5.2 إحصائيات الملصقات / Sticker Statistics

| نوع الملصق<br>Sticker Type | العدد<br>Count | النسبة<br>Percentage |
|------------------------|------------|----------------|
| ملصقات سارية<br>Valid Stickers | {valid_stickers} | {valid_stickers_percentage}% |
| ملصقات منتهية<br>Expired Stickers | {expired_stickers} | {expired_stickers_percentage}% |
| **الإجمالي<br>Total** | **{total_stickers}** | **100%** |

---

## القسم السادس: المخالفات المرورية / Section Six: Traffic Violations

### 6.1 الإحصائيات العامة / General Statistics

| المؤشر<br>Indicator | القيمة<br>Value |
|-----------------|-------------|
| إجمالي المخالفات<br>Total Violations | **{total_violations}** |
| المخالفات المفتوحة<br>Open Violations | {open_violations} ({open_violations_percentage}%) |
| المخالفات المغلقة<br>Closed Violations | {closed_violations} ({closed_violations_percentage}%) |

---

### 6.2 التوزيع حسب النوع / Distribution by Type

| نوع المخالفة<br>Violation Type | العدد<br>Count | النسبة<br>Percentage |
|------------------------------|------------|----------------|
| {violation_type_1} | {count_1} | {percentage_1}% |
| {violation_type_2} | {count_2} | {percentage_2}% |
| {violation_type_3} | {count_3} | {percentage_3}% |
| **الإجمالي<br>Total** | **{total_violations}** | **100%** |

---

## القسم السابع: الزوار / Section Seven: Visitors

### 7.1 الإحصائيات العامة / General Statistics

| المؤشر<br>Indicator | القيمة<br>Value |
|-----------------|-------------|
| إجمالي الزوار (اليوم)<br>Total Visitors (Today) | **{today_visitors}** |
| إجمالي الزوار (هذا الشهر)<br>Total Visitors (This Month) | **{month_visitors}** |
| إجمالي الزوار (هذا العام)<br>Total Visitors (This Year) | **{year_visitors}** |

---

## القسم الثامن: الشكاوى / Section Eight: Complaints

### 8.1 الإحصائيات العامة / General Statistics

| المؤشر<br>Indicator | القيمة<br>Value |
|-----------------|-------------|
| إجمالي الشكاوى<br>Total Complaints | **{total_complaints}** |
| الشكاوى المفتوحة<br>Open Complaints | {open_complaints} ({open_complaints_percentage}%) |
| الشكاوى المغلقة<br>Closed Complaints | {closed_complaints} ({closed_complaints_percentage}%) |

---

### 8.2 التوزيع حسب النوع / Distribution by Type

| نوع الشكوى<br>Complaint Type | العدد<br>Count | النسبة<br>Percentage |
|---------------------------|------------|----------------|
| {complaint_type_1} | {count_c1} | {percentage_c1}% |
| {complaint_type_2} | {count_c2} | {percentage_c2}% |
| {complaint_type_3} | {count_c3} | {percentage_c3}% |
| **الإجمالي<br>Total** | **{total_complaints}** | **100%** |

---

## القسم التاسع: الوقائع الأمنية / Section Nine: Security Incidents

### 9.1 الإحصائيات العامة / General Statistics

| المؤشر<br>Indicator | القيمة<br>Value |
|-----------------|-------------|
| إجمالي الوقائع<br>Total Incidents | **{total_incidents}** |
| الوقائع المفتوحة<br>Open Incidents | {open_incidents} ({open_incidents_percentage}%) |
| الوقائع المغلقة<br>Closed Incidents | {closed_incidents} ({closed_incidents_percentage}%) |

---

## الخلاصة والتوصيات / Summary and Recommendations

### الخلاصة / Summary

1. **المباني / Buildings:** {total_buildings} مبنى بنسبة إشغال إجمالية {overall_occupancy}%
2. **السكان / Residents:** {total_residents} ساكن موزعين على {occupied_units} وحدة
3. **المواقف / Parking:** {total_parking} موقف بنسبة استخدام {parking_utilization}%
4. **المخالفات / Violations:** {total_violations} مخالفة، منها {open_violations} مخالفة مفتوحة

### التوصيات / Recommendations

1. **الوحدات الشاغرة / Vacant Units:** العمل على تقليل عدد الوحدات الشاغرة ({vacant_units} وحدة)
2. **المواقف / Parking:** تحسين استخدام المواقف الشاغرة ({vacant_parking} موقف)
3. **المخالفات / Violations:** متابعة المخالفات المفتوحة ({open_violations} مخالفة)
4. **الشكاوى / Complaints:** سرعة الرد على الشكاوى المفتوحة ({open_complaints} شكوى)

---

## معلومات التقرير / Report Information

- **تاريخ الإنشاء / Creation Date:** {report_date}
- **وقت الإنشاء / Creation Time:** {report_time}
- **المستخدم / User:** {report_user}
- **النسخة / Version:** 1.0
- **النظام / System:** نظام إدارة إسكان هيئة التدريس

---

**ملاحظة / Note:** هذا تقرير ديناميكي يتم إنشاؤه تلقائياً من قاعدة البيانات. جميع الأرقام والإحصائيات محدثة حتى لحظة إنشاء التقرير.

This is a dynamic report automatically generated from the database. All numbers and statistics are updated up to the moment of report creation.

---

**نهاية التقرير / End of Report**
