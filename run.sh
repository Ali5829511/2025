#!/bin/bash

# Script to run Faculty Housing Management System
# سكريبت لتشغيل نظام إدارة إسكان أعضاء هيئة التدريس

echo "=========================================="
echo "Faculty Housing Management System"
echo "نظام إدارة إسكان أعضاء هيئة التدريس"
echo "=========================================="
echo ""

# Check if housing.db exists
if [ ! -f "housing.db" ]; then
    echo "📦 Database not found. Initializing..."
    echo "📦 قاعدة البيانات غير موجودة. جاري الإنشاء..."
    python3 database.py
    
    if [ $? -eq 0 ]; then
        echo "✅ Database initialized successfully"
        echo "✅ تم إنشاء قاعدة البيانات بنجاح"
    else
        echo "❌ Failed to initialize database"
        echo "❌ فشل إنشاء قاعدة البيانات"
        exit 1
    fi
    echo ""
fi

# Check if Flask is installed
python3 -c "import flask" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "⚠️  Flask not found. Installing dependencies..."
    echo "⚠️  Flask غير مثبت. جاري تثبيت المتطلبات..."
    pip install -r requirements.txt
    echo ""
fi

echo "🚀 Starting server..."
echo "🚀 جاري تشغيل الخادم..."
echo ""
echo "📍 Server will be available at: http://localhost:5000"
echo "📍 سيكون الخادم متاحاً على: http://localhost:5000"
echo ""
echo "🔐 Default Login Credentials:"
echo "   Admin: admin / Admin@2025"
echo "   Violations: violations_officer / Violations@2025"
echo "   Visitors: visitors_officer / Visitors@2025"
echo ""
echo "⚠️  Press Ctrl+C to stop the server"
echo "⚠️  اضغط Ctrl+C لإيقاف الخادم"
echo "=========================================="
echo ""

# Run the server
python3 server.py
