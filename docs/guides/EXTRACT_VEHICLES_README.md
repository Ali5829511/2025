# Vehicle Data Extraction Script
# سكربت استخراج بيانات المركبات

<div dir="rtl">

## نظرة عامة

سكربت Python لاستخراج بيانات المركبات من الصور بشكل تلقائي باستخدام Plate Recognizer API، مع إمكانية تتبع المخالفات بدون غرامات.

### المميزات الرئيسية

✅ **استخراج رقم اللوحة** - بدقة عالية باستخدام AI  
✅ **اكتشاف نوع المركبة** - سيارة، شاحنة، دراجة نارية، إلخ  
✅ **تحديد اللون** - بالعربية مع قيم RGB  
✅ **تتبع المخالفات** - تسجيل المخالفات بدون غرامات أو رسوم  
✅ **معالجة دفعات كبيرة** - دعم آلاف الصور  
✅ **الاستئناف التلقائي** - استمرار من آخر نقطة توقف  
✅ **تصدير Excel** - بأعمدة عربية  

</div>

---

## Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure Script
Edit `extract_vehicles.py`:
```python
IMAGE_FOLDER = r"C:\Path\To\Your\Images"
API_TOKEN = "your_platerecognizer_api_token"

# Violation tracking (optional)
TRACK_VIOLATIONS = True  # Enable violation recording (no fines)
DEFAULT_VIOLATION_TYPE = "مخالفة مرورية"  # Traffic violation
DEFAULT_LOCATION = "الموقع"  # Location (optional)
```

### 3. Run
```bash
python extract_vehicles.py
```

### 4. Get Results
Open `نتائج_المركبات.xlsx` in Excel.

---

## 📚 Documentation

### For Users / للمستخدمين

- 🚀 **[Quick Start Guide](QUICK_START_EXTRACT.md)** - Get started in 5 minutes / ابدأ في 5 دقائق
- 📖 **[Complete User Guide](EXTRACT_VEHICLES_GUIDE.md)** - Full documentation / الدليل الكامل
- ⚙️ **[Configuration Example](extract_vehicles.config.example)** - Sample configuration / مثال الإعدادات

### What's Included / المحتويات

| File | Description |
|------|-------------|
| `extract_vehicles.py` | Main extraction script / السكربت الرئيسي |
| `EXTRACT_VEHICLES_GUIDE.md` | Comprehensive user guide in Arabic & English / الدليل الشامل |
| `QUICK_START_EXTRACT.md` | Quick start guide / دليل البدء السريع |
| `extract_vehicles.config.example` | Configuration examples / أمثلة الإعدادات |

---

## Features / المميزات

### Core Features / المميزات الأساسية

- 🔍 **License Plate Recognition** - Using Plate Recognizer AI
- 🚗 **Vehicle Type Detection** - Car, truck, motorcycle, etc.
- 🎨 **Color Detection** - Dominant color with Arabic names
- 📝 **Violation Tracking** - Record violations without fines or fees
- 📊 **Excel Export** - With Arabic column names
- 🔄 **Resume Capability** - Continue from where you left off
- ⚡ **Batch Processing** - Process thousands of images

### Advanced Features / المميزات المتقدمة

- ✨ **Image Enhancement** - Improve recognition accuracy
- 🎯 **Region Filtering** - Focus on specific regions (e.g., Saudi Arabia)
- 📈 **Confidence Scoring** - Filter results by confidence level
- 🔁 **Alternative Readings** - Multiple plate candidates
- 💾 **Progress Tracking** - Periodic saves to prevent data loss
- 📝 **Detailed Logging** - Track processing status
- 🚫 **No Payment Fields** - Violations tracked without fines or payment amounts

---

## Requirements / المتطلبات

### Software / البرمجيات

- Python 3.7 or higher
- Plate Recognizer API account (get token from [platerecognizer.com](https://platerecognizer.com))
- Internet connection

### Python Libraries / مكتبات Python

```
requests>=2.31.0
pandas>=2.2.3
openpyxl>=3.1.2
Pillow>=10.2.0
colorthief>=0.2.1
```

All dependencies are listed in `requirements.txt`.

---

## Usage Examples / أمثلة الاستخدام

### Example 1: Basic Usage

```python
# Configure
IMAGE_FOLDER = r"E:\Traffic\Images"
API_TOKEN = "sk_abc123xyz"

# Run
python extract_vehicles.py
```

### Example 2: Custom Configuration

```python
# Configure for specific region
IMAGE_FOLDER = r"D:\Photos\Vehicles"
API_TOKEN = "sk_abc123xyz"
REGIONS = ['sa']  # Saudi Arabia only
MIN_CONFIDENCE = 0.8  # 80% minimum confidence
BATCH_SIZE = 100  # Save every 100 images
```

### Example 3: Multiple Regions

```python
# Gulf countries
REGIONS = ['sa', 'ae', 'kw', 'qa', 'om', 'bh']
```

---

## Output Format / صيغة المخرجات

The script generates an Excel file with the following columns:

| Column (AR) | Column (EN) | Description |
|-------------|-------------|-------------|
| الرقم التسلسلي | Serial Number | Sequential number |
| اسم الملف | Filename | Image filename |
| رقم اللوحة | Plate Number | Detected plate |
| الثقة | Confidence | 0.0 to 1.0 |
| نوع المركبة | Vehicle Type | Car, truck, etc. |
| اللون | Color | Color in Arabic |
| المنطقة | Region | Region code |
| بدائل اللوحة | Alternatives | Alternative readings |
| الحالة | Status | Success/Failed |
| تسجيل مخالفة | Violation Recorded | Yes/No (نعم/لا) |
| نوع المخالفة | Violation Type | Type of violation |
| موقع المخالفة | Violation Location | Location where captured |
| وصف المخالفة | Violation Description | Description of violation |
| رابط الصورة | Image Path | Full path to image |
| وقت المعالجة | Processing Time | Timestamp |

**Note:** Violation tracking does NOT include fines or payment amounts. It only records the violation type, location, and description for documentation purposes.

---

## Troubleshooting / استكشاف الأخطاء

### Common Issues / المشاكل الشائعة

**Q: Script says "API token not configured"**  
A: Edit `API_TOKEN` in the script with your actual token from platerecognizer.com

**Q: "Image folder not found"**  
A: Make sure `IMAGE_FOLDER` path is correct and use `r"path"` format for Windows

**Q: "Insufficient credits"**  
A: Check your Plate Recognizer account balance. You may need to upgrade your plan.

**Q: Script is slow**  
A: Reduce `API_DELAY` (but watch for rate limiting) or process in smaller batches

**Q: Low accuracy**  
A: Ensure images are high quality (800x600+), set appropriate `REGIONS`, and enable `ENHANCE_IMAGES`

See [EXTRACT_VEHICLES_GUIDE.md](EXTRACT_VEHICLES_GUIDE.md) for detailed troubleshooting.

---

## Performance / الأداء

### Processing Speed / سرعة المعالجة

With default settings (`API_DELAY = 0.5`):
- **~120 images per minute** (2 images/second)
- **8,000 images** in ~67 minutes (~1.1 hours)

You can adjust `API_DELAY` based on your API plan:
- Free tier: 0.5-1.0 seconds recommended
- Paid tier: 0.1-0.5 seconds

### API Usage / استخدام API

- Each image = 1 API call
- Free tier: 2,500 calls/month
- For 8,000 images: Consider paid plan

---

## Best Practices / أفضل الممارسات

### Image Quality / جودة الصور

✅ Minimum 400x300 pixels  
✅ Recommended 800x600 or higher  
✅ Clear, well-lit images  
✅ Plate clearly visible  

### Processing / المعالجة

✅ Test with 10-50 images first  
✅ Monitor API usage on dashboard  
✅ Use appropriate `REGIONS` for your area  
✅ Enable `ENHANCE_IMAGES` for better accuracy  
✅ Set `MIN_CONFIDENCE` to filter poor results  

### Security / الأمان

⚠️ Never commit API tokens to git  
⚠️ Keep extracted data secure  
⚠️ Respect privacy laws  
⚠️ Use data responsibly  

---

## Integration with Main System / التكامل مع النظام الرئيسي

This script is part of the Faculty Housing Management System and can be integrated with:

- `plate_recognizer.py` - Existing plate recognition module
- `plate_violation_detector.py` - Violation detection system
- `database.py` - For storing results in the main database

See the main [README.md](../README.md) for more information about the complete system.

---

## Support / الدعم

### Documentation / الوثائق

- 📖 [Complete Guide](EXTRACT_VEHICLES_GUIDE.md)
- 🚀 [Quick Start](QUICK_START_EXTRACT.md)
- ⚙️ [Configuration](extract_vehicles.config.example)

### Getting Help / الحصول على المساعدة

- 🐛 [GitHub Issues](https://github.com/Ali5829511/2025/issues)
- 📚 [Plate Recognizer Docs](https://docs.platerecognizer.com/)
- 💬 Plate Recognizer Support: support@platerecognizer.com

---

## License / الترخيص

This script is part of the Faculty Housing Management System.  
Use responsibly and in accordance with local laws and regulations.

---

## Credits / الشكر

- **Plate Recognizer** - AI-powered plate recognition API
- **ColorThief** - Color extraction library
- **pandas** - Data processing
- **openpyxl** - Excel export

---

<div dir="rtl">

## ملاحظة مهمة

⚠️ **هذا السكربت يستخدم API خارجي وقد يستهلك رصيدك.**

- ابدأ بدفعة صغيرة للاختبار (10-50 صورة)
- راقب الاستهلاك على لوحة تحكم Plate Recognizer
- احتفظ برمز API في مكان آمن
- استخدم البيانات بشكل مسؤول

</div>

---

**Last Updated:** November 2024  
**Version:** 1.0.0
