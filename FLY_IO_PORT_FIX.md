# Fly.io Port Configuration Fix
# إصلاح تكوين منفذ Fly.io

## Problem / المشكلة

```
Load balancer issues
Machines aren't listening on 0.0.0.0:8000, so our proxy has trouble finding a candidate to route requests to.
```

**السبب الجذري / Root Cause:**
- التطبيق كان يستخدم المنفذ 5000 بشكل افتراضي
- Fly.io يتوقع أن يستمع التطبيق على المنفذ 8000 (كما هو محدد في `fly.toml`)
- عدم تطابق المنفذ يمنع موازن التحميل من توجيه الطلبات

**The Root Cause:**
- Application was using port 5000 by default
- Fly.io expects the application to listen on port 8000 (as specified in `fly.toml`)
- Port mismatch prevents load balancer from routing requests

---

## Solution Implemented / الحل المُنفذ

### 1. Updated `fly.toml` / تحديث ملف التكوين

**Changes / التغييرات:**
```toml
[env]
  PORT = "8000"              # Explicitly set port to 8000
  FLASK_DEBUG = "False"       # Disable debug in production
  FLASK_ENV = "production"    # Set production environment
  HOST = "0.0.0.0"           # Listen on all interfaces

[http_service]
  internal_port = 8000        # Match the PORT environment variable
  
  # Added health check
  [http_service.checks.health]
    grace_period = "30s"
    interval = "15s"
    method = "GET"
    path = "/api/health"
    timeout = "10s"
    type = "http"

[[vm]]
  memory_mb = 512              # Increased from 256MB for stability
```

**Why This Works / لماذا يعمل هذا:**
- `PORT=8000` environment variable is read by `gunicorn_config.py`
- Gunicorn binds to `0.0.0.0:8000`
- Fly.io proxy can now find and route to the application
- Health checks ensure the app is ready before receiving traffic

### 2. Updated `Dockerfile` / تحديث Dockerfile

**Added Explicit Environment Variables:**
```dockerfile
ENV PORT=8000
ENV HOST=0.0.0.0
ENV FLASK_ENV=production
ENV FLASK_DEBUG=False
```

**Improved Health Check:**
```dockerfile
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD python3 -c "import requests; requests.get('http://localhost:8000/api/health', timeout=5)" || exit 1
```

### 3. How It Works Now / كيف يعمل الآن

**Boot Sequence / تسلسل التشغيل:**
```
1. Dockerfile sets PORT=8000
2. fly.toml confirms PORT=8000
3. gunicorn_config.py reads PORT from environment
4. Gunicorn binds to 0.0.0.0:8000
5. Fly.io proxy detects service on port 8000
6. Health check passes
7. Traffic routes successfully ✅
```

---

## How `gunicorn_config.py` Reads the Port / كيف يقرأ التكوين المنفذ

The configuration file automatically reads the PORT environment variable:

```python
# In gunicorn_config.py
bind = "0.0.0.0:" + str(os.environ.get("PORT", "10000"))
```

**Priority Order / ترتيب الأولوية:**
1. Fly.io sets `PORT=8000` in environment
2. Dockerfile also sets `PORT=8000` as backup
3. Gunicorn reads and binds to `0.0.0.0:8000`

---

## Verification Steps / خطوات التحقق

### After Deploying / بعد النشر:

1. **Check Fly.io Logs / تحقق من سجلات Fly.io:**
   ```bash
   fly logs
   ```
   
   Look for:
   ```
   ✅ Housing Management System is ready!
      Workers: 1
      Binding: 0.0.0.0:8000
   ```

2. **Check App Status / تحقق من حالة التطبيق:**
   ```bash
   fly status
   ```
   
   Should show:
   ```
   Status: running
   Health checks: passing
   ```

3. **Test Health Endpoint / اختبر نقطة فحص الصحة:**
   ```bash
   curl https://housing-management-system.fly.dev/api/health
   ```
   
   Should return:
   ```json
   {
     "status": "healthy",
     "timestamp": "2025-11-08T..."
   }
   ```

4. **Test Main Application / اختبر التطبيق الرئيسي:**
   ```bash
   curl https://housing-management-system.fly.dev/
   ```
   
   Should return the login page HTML

---

## Deployment Instructions / تعليمات النشر

### First Time Setup / الإعداد الأول:

```bash
# Install flyctl if not already installed
# ثبت flyctl إذا لم يكن مثبتاً
curl -L https://fly.io/install.sh | sh

# Login to Fly.io
# سجل الدخول إلى Fly.io
fly auth login

# Launch the app (only needed once)
# أطلق التطبيق (مطلوب مرة واحدة فقط)
fly launch --name housing-management-system --region iad --no-deploy

# Deploy the application
# انشر التطبيق
fly deploy
```

### Updating the App / تحديث التطبيق:

```bash
# Deploy latest changes
# انشر أحدث التغييرات
fly deploy

# View logs in real-time
# عرض السجلات في الوقت الفعلي
fly logs

# Check status
# تحقق من الحالة
fly status

# Open in browser
# افتح في المتصفح
fly open
```

---

## Troubleshooting / استكشاف الأخطاء

### Issue: "Machines aren't listening on 0.0.0.0:8000"
### المشكلة: "الأجهزة لا تستمع على 0.0.0.0:8000"

**Solution / الحل:**
1. Verify `fly.toml` has `PORT=8000` in `[env]` section
2. Check Fly.io logs for Gunicorn binding message
3. Ensure Dockerfile sets environment variables correctly

### Issue: Health checks failing
### المشكلة: فشل فحوصات الصحة

**Solution / الحل:**
1. Verify `/api/health` endpoint is working:
   ```bash
   fly ssh console
   curl http://localhost:8000/api/health
   ```
2. Check if database initialization succeeded
3. Review application logs for errors

### Issue: Connection timeout
### المشكلة: انتهاء مهلة الاتصال

**Solution / الحل:**
1. Increase VM memory if needed:
   ```toml
   [[vm]]
     memory_mb = 1024
   ```
2. Increase health check grace period:
   ```toml
   [http_service.checks.health]
     grace_period = "60s"
   ```

---

## Important Notes / ملاحظات مهمة

### Port Configuration / تكوين المنفذ

**✅ DO / افعل:**
- Always use `0.0.0.0` as host (not `localhost` or `127.0.0.1`)
- Set PORT environment variable to match `fly.toml`
- Use health checks to verify app is ready

**❌ DON'T / لا تفعل:**
- Don't hardcode port numbers in application code
- Don't use `localhost` or `127.0.0.1` - Fly.io proxy can't reach it
- Don't skip health checks

### Memory Considerations / اعتبارات الذاكرة

- **256MB**: May be insufficient, can cause crashes
  قد يكون غير كافٍ، يمكن أن يسبب أعطالاً
- **512MB**: Recommended minimum for stable operation
  الحد الأدنى الموصى به للتشغيل المستقر
- **1GB**: Better for production with multiple workers
  أفضل للإنتاج مع عمال متعددين

### Database Persistence / استمرارية قاعدة البيانات

For SQLite on Fly.io, you need volumes:
```bash
fly volumes create housing_data --size 1
```

Then update `fly.toml`:
```toml
[[mounts]]
  source = "housing_data"
  destination = "/app/data"
```

---

## Configuration Summary / ملخص التكوين

| Component | Setting | Value |
|-----------|---------|-------|
| Host | HOST | 0.0.0.0 |
| Port | PORT | 8000 |
| Internal Port | internal_port | 8000 |
| Debug Mode | FLASK_DEBUG | False |
| Environment | FLASK_ENV | production |
| Memory | memory_mb | 512 |
| Workers | WEB_CONCURRENCY | 1 |

---

## Additional Resources / موارد إضافية

- [Fly.io Configuration Reference](https://fly.io/docs/reference/configuration/)
- [Fly.io Troubleshooting Guide](https://fly.io/docs/getting-started/troubleshooting/)
- [Gunicorn Configuration](https://docs.gunicorn.org/en/stable/settings.html)

---

## Success Indicators / مؤشرات النجاح

When everything is working correctly, you should see:

عندما يعمل كل شيء بشكل صحيح، يجب أن ترى:

```bash
$ fly status
App
  Name     = housing-management-system
  Owner    = personal
  Hostname = housing-management-system.fly.dev
  Platform = machines

Machines
ID              STATE   REGION  ROLE    IMAGE                           CREATED
148e226e59e687  started iad     app     housing-management:latest       2m ago

$ curl https://housing-management-system.fly.dev/api/health
{"status":"healthy","timestamp":"2025-11-08T22:30:00Z"}
```

✅ **Status: FIXED / الحالة: تم الإصلاح**
