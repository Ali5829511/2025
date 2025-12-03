# Plate Recognizer Integration Setup Guide
# دليل إعداد تكامل Plate Recognizer

## 📋 Overview / نظرة عامة

This system is integrated with Plate Recognizer API for automatic license plate recognition.
النظام متكامل مع خدمة Plate Recognizer للتعرف التلقائي على لوحات السيارات.

## ✅ Integration Status / حالة التكامل

- **API Dashboard**: https://app.platerecognizer.com/service/snapshot-cloud/dashboard/
- **Parkpow Dashboard**: https://app.parkpow.com/accounts/token/
- **Integration Module**: `plate_recognizer.py`
- **Status**: ✅ Fully integrated / متكامل بالكامل

## 🔑 API Configuration / إعداد الـ API

### Your Account Information / معلومات حسابك

Based on your dashboard:
- **API Calls Used**: 16 / 50,000 (استدعاءات واجهة برمجة التطبيقات)
- **Rate Limit**: 8 requests/second (الحد الأقصى للمكالمات)
- **Reset Date**: 2025-12-01 05:38 PM (إعادة تعيين التاريخ)
- **Timezone**: Asia/Riyadh (المنطقة الزمنية)

### Supported Features / الميزات المدعومة
- ✅ Saudi Arabia region detection / كشف المنطقة السعودية
- ✅ Automatic plate recognition / التعرف التلقائي على اللوحات
- ✅ Confidence scoring / درجة الثقة
- ✅ Vehicle type detection / كشف نوع المركبة
- ✅ MMC (Make, Model, Color) detection / كشف العلامة التجارية والطراز واللون

## 🚀 Deployment Steps / خطوات النشر

### Step 1: Configure on Render.com / الخطوة الأولى: الإعداد على Render

1. **Go to Render Dashboard / اذهب إلى لوحة تحكم Render**
   - URL: https://dashboard.render.com/
   - Select your service: `two025-upa7` or `housing-system`

2. **Add Environment Variables / إضافة متغيرات البيئة**
   
   Go to "Environment" tab and add:
   
   ```
   PLATE_RECOGNIZER_API_TOKEN=22ba3cf7155a1ea730a0b64787f98ab5f9a3de94
   ```
   
   Optional (if using Parkpow):
   ```
   PARKPOW_CODE=7c13be422713a758a42a0bc453cf3331fbf4d346
   ```

3. **Save and Redeploy / احفظ وأعد النشر**
   - Click "Save Changes"
   - Render will automatically redeploy the application
   - Wait 2-3 minutes for deployment to complete

### Step 2: Merge Pull Request / الخطوة الثانية: دمج الـ PR

1. Go to: https://github.com/Ali5829511/2025/pulls
2. Find PR: "Fix pip root user warning and login endpoint mismatch"
3. Click "Merge pull request"
4. Confirm merge to `main` branch
5. Render will auto-deploy the updates

### Step 3: Verify Integration / الخطوة الثالثة: التحقق من التكامل

After deployment:

1. **Login to the system / تسجيل الدخول**
   - URL: https://two025-upa7.onrender.com/
   - Username: `admin`
   - Password: `Admin@2025`

2. **Test plate recognition / اختبار التعرف على اللوحات**
   - Go to parking management or car registration
   - Upload a car image with visible license plate
   - System should automatically detect and fill the plate number
   - If not configured, you'll see: "خدمة Plate Recognizer غير مفعلة"

## 📊 Usage Monitoring / مراقبة الاستخدام

- **Monitor usage**: https://app.platerecognizer.com/service/snapshot-cloud/dashboard/
- **Current limit**: 50,000 calls/month
- **Current usage**: 16 calls used
- **Remaining**: 49,984 calls
- **Reset date**: December 1, 2025 at 5:38 PM

## 🛠️ Troubleshooting / استكشاف الأخطاء

### Error: "خدمة Plate Recognizer غير مفعلة"
**Solution**: 
- Verify API token is added to Render environment variables
- Check token is correct: `22ba3cf7155a1ea730a0b64787f98ab5f9a3de94`
- Redeploy the service after adding environment variables

### Error: API rate limit exceeded
**Solution**:
- Current limit: 8 requests/second
- If exceeded, system will queue requests automatically
- Monitor usage in dashboard

### Error: Invalid API response
**Solution**:
- Check API token hasn't expired (resets: 2025-12-01)
- Verify image format is supported (JPEG, PNG)
- Check image size is within limits (recommended < 5MB)

## 📝 Notes / ملاحظات

⚠️ **IMPORTANT SECURITY NOTE / تنبيه أمني مهم**:
- Never commit API tokens to Git repository
- Always use environment variables for secrets
- API token should only be in Render dashboard, not in code

✅ **Best Practices / أفضل الممارسات**:
- Images should be clear with visible license plates
- Best results with direct front/back view of vehicle
- Supported regions: Saudi Arabia (SA) and many others
- For Saudi plates: System automatically detects Arabic and English text

## 🔗 Useful Links / روابط مفيدة

- **API Documentation**: https://docs.platerecognizer.com/
- **Dashboard**: https://app.platerecognizer.com/service/snapshot-cloud/dashboard/
- **Parkpow Portal**: https://app.parkpow.com/
- **Supported Countries**: https://guides.platerecognizer.com/docs/other/supported-countries/
- **GitHub Repository**: https://github.com/Ali5829511/2025

## 📞 Support / الدعم

For issues with:
- **Plate Recognizer API**: support@platerecognizer.com
- **System Integration**: Create issue on GitHub
- **Deployment**: Check Render logs at https://dashboard.render.com/

---

Last Updated: November 9, 2025
آخر تحديث: 9 نوفمبر 2025
