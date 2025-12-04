# Apartments and Parking Management Setup
# دليل إعداد إدارة الشقق والمواقف

## Overview / نظرة عامة

This document explains how to set up the apartments and parking management system with comprehensive initial data for **1020 apartments and 1300 parking spots**.

يشرح هذا المستند كيفية إعداد نظام إدارة الشقق والمواقف مع بيانات أولية شاملة لـ **1020 شقة و 1300 موقف**.

**Important Notes / ملاحظات مهمة:**
- Each apartment has its own dedicated parking spot (1020 spots)
- Special needs parking: 39 spots (18 in old buildings, 21 in new buildings)
- Public parking: 241 spots in old buildings
- كل شقة لها موقف خاص بها (1020 موقف)
- مواقف احتياجات خاصة: 39 موقف (18 في المباني القديمة، 21 في المباني الجديدة)
- مواقف عامة: 241 موقف في المباني القديمة

## Quick Setup / الإعداد السريع

### Option 1: Using Setup Script / الخيار 1: استخدام برنامج الإعداد

```bash
./setup_apartments_parking_data.sh
```

This will automatically:
- Initialize the database if needed
- Import 165 buildings (30 old buildings, 21 new buildings, 114 villas)
- Import 70 apartments across 4 buildings
- Import 70 parking spots in 2 parking areas

سيقوم هذا تلقائيًا بـ:
- تهيئة قاعدة البيانات إذا لزم الأمر
- استيراد 165 مبنى (30 مبنى قديم، 21 مبنى جديد، 114 فيلا)
- استيراد 70 شقة في 4 مباني
- استيراد 70 موقف في منطقتين للوقوف

### Clear Database / مسح قاعدة البيانات

To clear all data and start fresh:
لمسح جميع البيانات والبدء من جديد:

```bash
./clear_database.sh
```

This will delete the database file. You can then run the setup script again to add fresh data.
سيحذف هذا ملف قاعدة البيانات. يمكنك بعد ذلك تشغيل برنامج الإعداد مرة أخرى لإضافة بيانات جديدة.

### Option 2: Manual Setup / الخيار 2: الإعداد اليدوي

```bash
# Step 1: Initialize database / الخطوة 1: تهيئة قاعدة البيانات
python3 -c "import database; database.init_database()"

# Step 2: Import buildings / الخطوة 2: استيراد المباني
echo "y" | python3 import_buildings_data.py

# Step 3: Import apartments and parking / الخطوة 3: استيراد الشقق والمواقف
python3 import_apartments_parking.py
```

## Data Imported / البيانات المستوردة

### Buildings / المباني
- **Total / الإجمالي**: 165 buildings
- **Old Buildings / المباني القديمة**: 30 buildings (1-30)
  - Each has 20 apartments: 1-4, 11-14, 21-24, 31-34, 41-44
- **New Buildings / المباني الجديدة**: 21 buildings
  - Buildings 53-56: 4 buildings (20 apartments each)
  - Buildings 61-68: 8 buildings (20 apartments each)
  - Buildings 71-79: 9 buildings (20 apartments each)
  - Each has apartments: 11-13, 21-23, 31-33, 41-43, 51-53, 61-63, 71-72
- **Villas / الفلل**: 114 villas (V1-V114)

### Apartments / الشقق
- **Total / الإجمالي**: 1020 apartments across 51 buildings
- **Old Buildings (1-30)**: 600 apartments (20 apartments × 30 buildings)
- **New Buildings (53-56)**: 80 apartments (20 apartments × 4 buildings)
- **New Buildings (61-68)**: 160 apartments (20 apartments × 8 buildings)
- **New Buildings (71-79)**: 180 apartments (20 apartments × 9 buildings)

### Parking Spots / المواقف
- **Total / الإجمالي**: 1300 parking spots
- **Apartment parking / مواقف الشقق**: 1020 spots (each apartment has dedicated parking)
- **Special needs parking / مواقف احتياجات خاصة**: 39 spots
  - Old buildings (1-30): 18 spots
  - New buildings (53-56, 61-68, 71-79): 21 spots
- **Public parking / مواقف عامة**: 241 spots (old buildings only)
- **Parking spot number formats**:
  - Apartment parking: Building-Apartment (e.g., 1-11, 5-23, 71-42)
  - Special needs: S-OLD-1 to S-OLD-18, S-NEW-1 to S-NEW-21
  - Public parking: P-OLD-1 to P-OLD-241
- **Parking areas**: G.L.P-7, G.L.P-8, G.L.P-9, G.L.P-10

## Accessing the Page / الوصول إلى الصفحة

After setup, start the server and access:
بعد الإعداد، ابدأ الخادم وادخل إلى:

```bash
python3 server.py
```

Then open in browser / ثم افتح في المتصفح:
```
http://localhost:5000/apartments_parking_management.html
```

## Features / الميزات

The apartments and parking management page includes:
تتضمن صفحة إدارة الشقق والمواقف:

- **Statistics Dashboard / لوحة الإحصائيات**: View total apartments, parking spots, and occupancy
- **Apartments Tab / تبويب الشقق**: Browse and search all apartments with building information
- **Parking Tab / تبويب المواقف**: Browse and search all parking spots with location details
- **Filters / المرشحات**: Filter by building or parking area
- **Search / البحث**: Search by unit number, building name, or parking spot number
- **Export / التصدير**: Export data to CSV format

## Database Schema / مخطط قاعدة البيانات

### Tables / الجداول

1. **buildings** - Building information
2. **apartments** - Apartment units linked to buildings
3. **parking_spots** - Parking spots linked to buildings and apartments

### Relationships / العلاقات

```
buildings (1) ──→ (many) apartments
buildings (1) ──→ (many) parking_spots
apartments (1) ──→ (1) parking_spots
```

## Notes / ملاحظات

- The database file (`housing.db`) is in `.gitignore` and should not be committed
- ملف قاعدة البيانات في `.gitignore` ولا يجب رفعه
- Run the setup script whenever you need to reset or initialize the data
- قم بتشغيل برنامج الإعداد عندما تحتاج إلى إعادة تعيين أو تهيئة البيانات
- All data uses proper Arabic text encoding
- جميع البيانات تستخدم الترميز العربي الصحيح

## Troubleshooting / استكشاف الأخطاء

### Problem: Need to clear all data and start fresh
### المشكلة: الحاجة إلى مسح جميع البيانات والبدء من جديد

**Solution / الحل**: Use the clear database script
```bash
./clear_database.sh
```
Then run the setup script again to add fresh data.
ثم قم بتشغيل برنامج الإعداد مرة أخرى لإضافة بيانات جديدة.

### Problem: Database is empty
### المشكلة: قاعدة البيانات فارغة

**Solution / الحل**: Run the setup script
```bash
./setup_apartments_parking_data.sh
```

### Problem: Import script fails
### المشكلة: فشل برنامج الاستيراد

**Solution / الحل**: Make sure the database is initialized first
```bash
python3 -c "import database; database.init_database()"
```

### Problem: Page shows no data
### المشكلة: الصفحة لا تعرض بيانات

**Solution / الحل**: 
1. Check that the database file exists: `ls -l housing.db`
2. Verify data was imported: `sqlite3 housing.db "SELECT COUNT(*) FROM apartments;"`
3. Restart the server: `python3 server.py`

## API Endpoints / نقاط النهاية API

- `GET /api/apartments` - Get all apartments with building info
- `GET /api/apartments?building_id=1` - Get apartments for specific building
- `GET /api/parking-spots` - Get all parking spots
- `GET /api/parking-spots?building_id=1` - Get parking spots for specific building
