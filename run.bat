@echo off
chcp 65001 >nul
cls

echo ==========================================
echo Faculty Housing Management System
echo نظام إدارة إسكان أعضاء هيئة التدريس
echo ==========================================
echo.

REM Check if housing.db exists
if not exist "housing.db" (
    echo 📦 Database not found. Initializing...
    echo 📦 قاعدة البيانات غير موجودة. جاري الإنشاء...
    python database.py
    
    if errorlevel 1 (
        echo ❌ Failed to initialize database
        echo ❌ فشل إنشاء قاعدة البيانات
        pause
        exit /b 1
    )
    
    echo ✅ Database initialized successfully
    echo ✅ تم إنشاء قاعدة البيانات بنجاح
    echo.
)

REM Check if Flask is installed
python -c "import flask" 2>nul
if errorlevel 1 (
    echo ⚠️  Flask not found. Installing dependencies...
    echo ⚠️  Flask غير مثبت. جاري تثبيت المتطلبات...
    pip install -r requirements.txt
    echo.
)

echo 🚀 Starting server...
echo 🚀 جاري تشغيل الخادم...
echo.
echo 📍 Server will be available at: http://localhost:5000
echo 📍 سيكون الخادم متاحاً على: http://localhost:5000
echo.
echo 🔐 Default Login Credentials:
echo    Admin: admin / Admin@2025
echo    Violations: violations_officer / Violations@2025
echo    Visitors: visitors_officer / Visitors@2025
echo.
echo ⚠️  Press Ctrl+C to stop the server
echo ⚠️  اضغط Ctrl+C لإيقاف الخادم
echo ==========================================
echo.

REM Run the server
python server.py
