#!/bin/bash
# Setup script for apartments and parking data
# برنامج إعداد بيانات الشقق والمواقف

echo "============================================================"
echo "Comprehensive Apartments and Parking Data Setup"
echo "إعداد شامل لبيانات الشقق والمواقف"
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

# Import ALL apartments and parking data
echo "📦 Step 2: Importing ALL apartments and parking data..."
echo "📦 الخطوة 2: استيراد جميع بيانات الشقق والمواقف..."
python3 import_all_apartments_parking.py
echo ""

# Verify data
echo "✅ Verifying data..."
echo "✅ التحقق من البيانات..."
sqlite3 housing.db "
SELECT '📊 Buildings: ' || COUNT(*) FROM buildings; 
SELECT '📊 Apartments: ' || COUNT(*) FROM apartments; 
SELECT '📊 Parking Spots: ' || COUNT(*) FROM parking_spots;
"
echo ""

echo "============================================================"
echo "✅ Setup complete! / ✅ اكتمل الإعداد!"
echo "============================================================"
echo "Data summary / ملخص البيانات:"
echo "  • 165 buildings (مبنى)"
echo "  • 1020 apartments (شقة)"
echo "  • 1020 parking spots (موقف)"
echo ""
echo "Each apartment has its own parking spot!"
echo "كل شقة لها موقف خاص برقم العمارة ورقم الشقة!"
echo ""
echo "You can now access the apartments and parking management page:"
echo "يمكنك الآن الوصول إلى صفحة إدارة الشقق والمواقف:"
echo "http://localhost:5000/apartments_parking_management.html"
echo "============================================================"
