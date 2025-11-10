#!/bin/bash
# Clear all data from the database
# مسح جميع البيانات من قاعدة البيانات

echo "============================================================"
echo "Clear All Database Data"
echo "مسح جميع بيانات قاعدة البيانات"
echo "============================================================"
echo ""

# Check if database exists
if [ ! -f "housing.db" ]; then
    echo "⚠️  Database file not found (housing.db)"
    echo "⚠️  ملف قاعدة البيانات غير موجود"
    echo "Nothing to clear."
    echo "لا يوجد شيء لمسحه."
    exit 0
fi

echo "⚠️  WARNING: This will delete ALL data from the database!"
echo "⚠️  تحذير: سيتم حذف جميع البيانات من قاعدة البيانات!"
echo ""
read -p "Are you sure? (yes/no): " confirm

if [ "$confirm" != "yes" ]; then
    echo "❌ Operation cancelled / تم إلغاء العملية"
    exit 0
fi

echo ""
echo "🗑️  Deleting database file..."
echo "🗑️  جاري حذف ملف قاعدة البيانات..."
rm -f housing.db

echo ""
echo "============================================================"
echo "✅ Database cleared successfully!"
echo "✅ تم مسح قاعدة البيانات بنجاح!"
echo "============================================================"
echo ""
echo "To add data again, run:"
echo "لإضافة البيانات مرة أخرى، قم بتشغيل:"
echo "  ./setup_apartments_parking_data.sh"
echo "============================================================"
