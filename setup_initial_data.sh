#!/bin/bash
# Setup script to import all initial data into the database
# برنامج لاستيراد جميع البيانات الأولية إلى قاعدة البيانات

set -e  # Exit on error

echo "========================================================================"
echo "🚀 Setting up Housing Management System Database"
echo "🚀 إعداد قاعدة بيانات نظام إدارة الإسكان"
echo "========================================================================"

# Check if database already exists
if [ -f "housing.db" ]; then
    echo ""
    echo "⚠️  Database file already exists: housing.db"
    echo "⚠️  ملف قاعدة البيانات موجود بالفعل: housing.db"
    echo ""
    read -p "Do you want to delete and recreate it? (y/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "❌ Setup cancelled."
        echo "❌ تم إلغاء الإعداد."
        exit 1
    fi
    rm housing.db
    echo "✅ Old database deleted"
    echo "✅ تم حذف قاعدة البيانات القديمة"
fi

echo ""
echo "========================================================================"
echo "📦 Step 1: Initialize database and create tables"
echo "📦 الخطوة 1: تهيئة قاعدة البيانات وإنشاء الجداول"
echo "========================================================================"
python3 database.py

echo ""
echo "========================================================================"
echo "📦 Step 2: Import buildings data (165 buildings)"
echo "📦 الخطوة 2: استيراد بيانات المباني (165 مبنى)"
echo "========================================================================"
python3 import_buildings_data.py <<EOF
y
EOF

echo ""
echo "========================================================================"
echo "📦 Step 3: Import apartments and parking spots (1,020 + 1,300)"
echo "📦 الخطوة 3: استيراد الشقق والمواقف (1,020 + 1,300)"
echo "========================================================================"
python3 import_all_apartments_parking.py

echo ""
echo "========================================================================"
echo "✅ Setup completed successfully!"
echo "✅ تم الإعداد بنجاح!"
echo "========================================================================"
echo ""
echo "📊 Database Summary / ملخص قاعدة البيانات:"
echo ""

python3 << 'EOF'
import sqlite3
conn = sqlite3.connect('housing.db')
cursor = conn.cursor()

cursor.execute('SELECT COUNT(*) FROM buildings')
buildings = cursor.fetchone()[0]

cursor.execute('SELECT COUNT(*) FROM apartments')
apartments = cursor.fetchone()[0]

cursor.execute('SELECT COUNT(*) FROM parking_spots')
parking = cursor.fetchone()[0]

print(f"   🏢 Buildings / المباني: {buildings}")
print(f"   🏠 Apartments / الشقق: {apartments}")
print(f"   🅿️  Parking spots / المواقف: {parking}")
print(f"   📊 Total records / إجمالي السجلات: {buildings + apartments + parking}")

conn.close()
EOF

echo ""
echo "========================================================================"
echo "🎉 You can now start the server and use the system!"
echo "🎉 يمكنك الآن تشغيل الخادم واستخدام النظام!"
echo ""
echo "To start the server / لتشغيل الخادم:"
echo "   python3 server.py"
echo ""
echo "Then open your browser at / ثم افتح المتصفح على:"
echo "   http://localhost:5000"
echo "========================================================================"
