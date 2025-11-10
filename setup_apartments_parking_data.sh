#!/bin/bash
# Setup script for apartments and parking data
# برنامج إعداد بيانات الشقق والمواقف

echo "============================================================"
echo "Apartments and Parking Data Setup"
echo "إعداد بيانات الشقق والمواقف"
echo "============================================================"
echo ""

# Check if database exists
if [ ! -f "housing.db" ]; then
    echo "⚠️  Database not found. Initializing..."
    echo "⚠️  قاعدة البيانات غير موجودة. جاري التهيئة..."
    python3 -c "import database; database.init_database()"
    echo ""
fi

# Import buildings data
echo "📦 Step 1: Importing buildings data..."
echo "📦 الخطوة 1: استيراد بيانات المباني..."
echo "y" | python3 import_buildings_data.py
echo ""

# Import apartments and parking data
echo "📦 Step 2: Importing apartments and parking data..."
echo "📦 الخطوة 2: استيراد بيانات الشقق والمواقف..."
python3 import_apartments_parking.py
echo ""

# Verify data
echo "✅ Verifying data..."
echo "✅ التحقق من البيانات..."
sqlite3 housing.db "SELECT 'Buildings: ' || COUNT(*) FROM buildings; SELECT 'Apartments: ' || COUNT(*) FROM apartments; SELECT 'Parking Spots: ' || COUNT(*) FROM parking_spots;"
echo ""

echo "============================================================"
echo "✅ Setup complete! / ✅ اكتمل الإعداد!"
echo "============================================================"
echo "You can now access the apartments and parking management page:"
echo "يمكنك الآن الوصول إلى صفحة إدارة الشقق والمواقف:"
echo "http://localhost:5000/apartments_parking_management.html"
echo "============================================================"
