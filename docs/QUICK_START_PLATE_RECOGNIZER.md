# Quick Start Guide - Plate Recognizer Integration
# دليل البدء السريع - تكامل Plate Recognizer

## إعداد سريع | Quick Setup

### 1. احصل على API Token
Get your free API token from: https://app.platerecognizer.com/
(2,500 free API calls per month)

### 2. أضف المفتاح إلى البيئة
Add the token to your environment:

```bash
# For Linux/Mac
export PLATE_RECOGNIZER_API_TOKEN="your_token_here"

# For Windows
set PLATE_RECOGNIZER_API_TOKEN=your_token_here

# Or add to .env file
echo "PLATE_RECOGNIZER_API_TOKEN=your_token_here" >> .env
```

### 3. ابدأ الخادم
Start the server:

```bash
python server.py
```

### 4. افتح الصفحة
Open the page:
```
http://localhost:5000/pages/parkpow_integration.html
```

## الاستخدام | Usage

### رفع صورة وتمييز اللوحة | Upload Image and Recognize Plate
1. Click "رفع صورة السيارة" (Upload vehicle image)
2. Select an image with a visible license plate
3. Click "تمييز اللوحة" (Recognize plate)
4. The plate number will be displayed automatically

### تسجيل مخالفة | Record Violation
1. Enter the plate number (or use auto-filled from recognition)
2. Select violation type
3. Add location and description (optional)
4. Click "تسجيل المخالفة" (Record violation)

### عرض المخالفين المتكررين | View Repeat Offenders
The system automatically shows vehicles with 3 or more violations.
You can adjust the threshold using the input field.

## ميزات متقدمة | Advanced Features

### تحديد المنطقة | Specify Region
For better accuracy, set the region in your .env file:
```bash
PLATE_RECOGNIZER_REGIONS=sa,ae,kw
```

### تكامل API | API Integration
Use the REST API endpoints:

```bash
# Check status
curl http://localhost:5000/api/parkpow/status \
  -H "Authorization: Bearer YOUR_TOKEN"

# Recognize plate
curl -X POST http://localhost:5000/api/parkpow/recognize \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{"image": "base64_encoded_image"}'
```

## استكشاف المشاكل | Troubleshooting

### Problem: "خدمة Plate Recognizer غير مفعلة"
**Solution:** Check that PLATE_RECOGNIZER_API_TOKEN is set correctly

### Problem: "رصيد غير كافٍ"
**Solution:** You've used all your API calls. Check your account or upgrade.

### Problem: Recognition not accurate
**Solution:** 
- Ensure image is clear and plate is visible
- Set the correct region (PLATE_RECOGNIZER_REGIONS)
- Use higher resolution images

## الدعم | Support

- Full Documentation: `/docs/PLATE_RECOGNIZER_INTEGRATION.md`
- API Docs: https://docs.platerecognizer.com/
- Get Help: Open an issue on GitHub

---

Made with ❤️ for better parking management
