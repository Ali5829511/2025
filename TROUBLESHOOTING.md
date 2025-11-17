# دليل استكشاف الأخطاء وإصلاحها
# Troubleshooting Guide

## 🔧 المشاكل الشائعة وحلولها / Common Issues and Solutions

### 1. مشاكل تسجيل الدخول / Login Issues

#### المشكلة: لا يمكنني تسجيل الدخول بكلمة المرور الافتراضية
**Problem: Cannot login with default password**

**الأسباب المحتملة / Possible Causes:**
- تم تغيير كلمة المرور بالفعل / Password already changed
- قاعدة البيانات غير مهيأة / Database not initialized
- خطأ في كتابة كلمة المرور / Password typo

**الحل / Solution:**
```bash
# 1. Check if database exists
ls -la *.db

# 2. Initialize database if needed
python init_db.py

# 3. Try default credentials
# Username: admin
# Password: Admin@2025
```

---

#### المشكلة: رسالة "must_change_password" ولكن لا يمكنني تغيير كلمة المرور
**Problem: "must_change_password" message but cannot change password**

**الحل / Solution:**
```bash
# Use the API endpoint directly
curl -X POST http://localhost:5000/api/auth/change-password \
  -H "Content-Type: application/json" \
  -b cookies.txt \
  -d '{
    "current_password": "Admin@2025",
    "new_password": "YourNewPassword123!"
  }'

# Or use Python
python3 << EOF
import requests
session = requests.Session()
session.post('http://localhost:5000/api/auth/login', 
    json={'username': 'admin', 'password': 'Admin@2025'})
response = session.post('http://localhost:5000/api/auth/change-password',
    json={'current_password': 'Admin@2025', 'new_password': 'NewPass123!'})
print(response.json())
EOF
```

---

### 2. مشاكل قاعدة البيانات / Database Issues

#### المشكلة: خطأ "table users has no column named must_change_password"
**Problem: Error "table users has no column named must_change_password"**

**الحل / Solution:**
```bash
# Run database migration
python3 << EOF
import database
database.init_database()
print("Database migrated successfully")
EOF

# Or recreate database (WARNING: deletes all data)
# rm housing.db
# python init_db.py
```

---

#### المشكلة: قاعدة البيانات محظورة (locked)
**Problem: Database is locked**

**الأسباب / Causes:**
- عملية أخرى تستخدم قاعدة البيانات / Another process using database
- ملف قاعدة البيانات تالف / Database file corrupted

**الحل / Solution:**
```bash
# 1. Check for running processes
ps aux | grep python | grep -E "server|app|main"

# 2. Kill any hung processes
pkill -f "python.*server.py"

# 3. Check database integrity
sqlite3 housing.db "PRAGMA integrity_check;"

# 4. If corrupted, restore from backup
cp backups/housing_latest.db.gz ./
gunzip housing_latest.db.gz
mv housing_latest.db housing.db
```

---

#### المشكلة: فقدان البيانات بعد إعادة التشغيل
**Problem: Data lost after restart**

**الأسباب / Causes:**
- استخدام قاعدة بيانات في الذاكرة / Using in-memory database
- ملف قاعدة البيانات في مجلد مؤقت / Database file in temp directory

**الحل / Solution:**
```bash
# Check DATABASE_URL in .env
cat .env | grep DATABASE

# For SQLite, ensure path is correct
# DATABASE_PATH=/opt/housing-system/housing.db

# For PostgreSQL, check connection
psql $DATABASE_URL -c "\dt"
```

---

### 3. مشاكل الأذونات / Permission Issues

#### المشكلة: خطأ "Permission denied" عند رفع الملفات
**Problem: "Permission denied" when uploading files**

**الحل / Solution:**
```bash
# Fix upload directory permissions
chmod 755 uploads/
chmod 755 uploads/car_images/
chmod 644 uploads/car_images/*

# If running with systemd
chown -R www-data:www-data uploads/

# Check current permissions
ls -la uploads/
```

---

#### المشكلة: خطأ "Permission denied" عند الكتابة إلى السجلات
**Problem: "Permission denied" when writing to logs**

**الحل / Solution:**
```bash
# Create logs directory
mkdir -p logs

# Fix permissions
chmod 755 logs/
chmod 640 logs/*.log

# If running with systemd
chown -R www-data:www-data logs/
```

---

### 4. مشاكل HTTPS/SSL

#### المشكلة: شهادة SSL غير صالحة
**Problem: Invalid SSL certificate**

**الحل / Solution:**
```bash
# Check certificate expiry
openssl x509 -in /etc/letsencrypt/live/yourdomain.com/cert.pem -noout -dates

# Renew certificate
sudo certbot renew

# Test certificate
curl -vI https://yourdomain.com 2>&1 | grep -i "SSL certificate"
```

---

#### المشكلة: رسالة "Your connection is not private"
**Problem: "Your connection is not private" message**

**الأسباب / Causes:**
- شهادة SSL منتهية / SSL certificate expired
- شهادة ذاتية التوقيع / Self-signed certificate
- عدم تطابق اسم النطاق / Domain name mismatch

**الحل / Solution:**
```bash
# For Let's Encrypt
sudo certbot certonly --nginx -d yourdomain.com

# For self-signed (development only)
openssl req -x509 -newkey rsa:4096 -nodes \
  -keyout key.pem -out cert.pem -days 365 \
  -subj "/CN=localhost"
```

---

### 5. مشاكل الأداء / Performance Issues

#### المشكلة: الخادم بطيء جداً
**Problem: Server is very slow**

**التشخيص / Diagnosis:**
```bash
# Check system resources
top
htop

# Check memory usage
free -h

# Check disk space
df -h

# Check database size
du -h housing.db
```

**الحل / Solution:**
```bash
# 1. Increase Gunicorn workers
# Edit gunicorn_config.py
workers = 4  # Increase based on available CPU

# 2. Add database indexes
python add_database_indexes.py

# 3. Enable caching (add to server.py)
# from flask_caching import Cache
# cache = Cache(app, config={'CACHE_TYPE': 'simple'})

# 4. Optimize queries
# Review and optimize slow queries in database.py
```

---

#### المشكلة: نفاد الذاكرة (Out of Memory)
**Problem: Out of memory errors**

**الحل / Solution:**
```bash
# 1. Reduce Gunicorn workers
# In gunicorn_config.py
workers = 1  # For 512MB RAM

# 2. Add swap space
sudo fallocate -l 2G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile

# 3. Enable PostgreSQL instead of SQLite
# SQLite loads entire database in memory
export DATABASE_URL="postgresql://user:pass@host/db"

# 4. Monitor memory usage
watch -n 1 free -h
```

---

### 6. مشاكل النسخ الاحتياطي / Backup Issues

#### المشكلة: فشل النسخ الاحتياطي التلقائي
**Problem: Automated backup fails**

**التشخيص / Diagnosis:**
```bash
# Test backup manually
./scripts/backup_database.sh

# Check cron logs
grep CRON /var/log/syslog

# Check backup script permissions
ls -la scripts/backup_database.sh
```

**الحل / Solution:**
```bash
# Fix script permissions
chmod +x scripts/backup_database.sh

# Test cron job
# Add to crontab -e:
# 0 2 * * * /opt/housing-system/scripts/backup_database.sh >> /var/log/backup.log 2>&1

# Verify cron is running
sudo systemctl status cron
```

---

### 7. مشاكل النشر / Deployment Issues

#### المشكلة: خطأ 502 Bad Gateway
**Problem: 502 Bad Gateway error**

**الأسباب / Causes:**
- Gunicorn لا يعمل / Gunicorn not running
- منفذ خاطئ / Wrong port
- جدار حماية يمنع الاتصال / Firewall blocking

**الحل / Solution:**
```bash
# 1. Check if Gunicorn is running
ps aux | grep gunicorn

# 2. Check Gunicorn logs
tail -f logs/error.log

# 3. Restart Gunicorn
sudo systemctl restart housing-system

# 4. Check Nginx configuration
sudo nginx -t
sudo systemctl reload nginx

# 5. Check firewall
sudo ufw status
sudo ufw allow 8000/tcp  # If needed
```

---

#### المشكلة: خطأ 500 Internal Server Error
**Problem: 500 Internal Server Error**

**التشخيص / Diagnosis:**
```bash
# Check application logs
tail -100 logs/error.log

# Check Gunicorn logs
journalctl -u housing-system -n 100

# Enable debug mode temporarily (development only!)
export FLASK_ENV=development
export FLASK_DEBUG=True
python server.py
```

**الحل / Solution:**
```bash
# Common fixes:

# 1. Database not initialized
python init_db.py

# 2. Missing environment variables
cp .env.example .env
nano .env  # Edit with correct values

# 3. Missing dependencies
pip install -r requirements.txt

# 4. File permissions
./scripts/set_permissions.sh

# 5. Check for Python errors
python -c "import server"
```

---

### 8. مشاكل Docker

#### المشكلة: Container يتوقف فوراً
**Problem: Container stops immediately**

**التشخيص / Diagnosis:**
```bash
# Check container logs
docker logs housing-system

# Check container status
docker ps -a

# Inspect container
docker inspect housing-system
```

**الحل / Solution:**
```bash
# 1. Check Dockerfile syntax
docker build -t housing-system .

# 2. Run in interactive mode
docker run -it housing-system /bin/bash

# 3. Check environment variables
docker run --env-file .env housing-system

# 4. Rebuild without cache
docker build --no-cache -t housing-system .
```

---

### 9. مشاكل API

#### المشكلة: CORS Error في المتصفح
**Problem: CORS error in browser**

**الحل / Solution:**
```bash
# 1. Add your domain to .env
ALLOWED_ORIGINS=https://yourdomain.com,https://www.yourdomain.com

# 2. Restart server
sudo systemctl restart housing-system

# 3. Verify CORS headers
curl -I -H "Origin: https://yourdomain.com" http://localhost:5000
```

---

#### المشكلة: API تعيد 404 Not Found
**Problem: API returns 404 Not Found**

**التشخيص / Diagnosis:**
```bash
# Check available routes
python3 << EOF
from server import app
for rule in app.url_map.iter_rules():
    print(f"{rule.endpoint}: {rule.rule}")
EOF

# Test API endpoint
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"test","password":"test"}'
```

---

### 10. مشاكل الأمان / Security Issues

#### المشكلة: تسجيل دخول بكلمات مرور افتراضية في الإنتاج
**Problem: Default passwords work in production**

**الحل الفوري / Immediate Solution:**
```bash
# Change all default passwords immediately
python3 << EOF
import database
from werkzeug.security import generate_password_hash

conn = database.get_db_connection()
cursor = conn.cursor()

users = ['admin', 'violations_officer', 'visitors_officer', 'viewer', 'violation_entry']
for user in users:
    new_pass = f"TempSecure{user}2025!"
    hash = generate_password_hash(new_pass)
    cursor.execute("UPDATE users SET password_hash=?, must_change_password=1 WHERE username=?", (hash, user))
    print(f"Changed password for {user} to: {new_pass}")

conn.commit()
conn.close()
print("\n⚠️  Give these passwords to users and ask them to change immediately!")
EOF
```

---

## 🛠️ أدوات التشخيص / Diagnostic Tools

### سكريبت فحص النظام / System Check Script

```bash
#!/bin/bash
# system_check.sh

echo "=== System Check ==="
echo ""

# Check Python version
echo "Python version:"
python3 --version

# Check dependencies
echo ""
echo "Checking dependencies..."
pip list | grep -E "Flask|gunicorn|psycopg2"

# Check database
echo ""
echo "Database status:"
if [ -f "housing.db" ]; then
    echo "✓ SQLite database found"
    ls -lh housing.db
else
    echo "✗ SQLite database not found"
fi

# Check environment
echo ""
echo "Environment variables:"
env | grep -E "FLASK|DATABASE|SECRET" || echo "No Flask env vars set"

# Check ports
echo ""
echo "Port availability:"
netstat -tuln | grep -E ":5000|:8000" || echo "Ports 5000/8000 available"

# Check logs
echo ""
echo "Recent logs:"
if [ -d "logs" ]; then
    ls -lh logs/
    echo ""
    echo "Last 5 errors:"
    tail -5 logs/error.log 2>/dev/null || echo "No errors"
else
    echo "No logs directory"
fi

# Check processes
echo ""
echo "Running processes:"
ps aux | grep -E "gunicorn|python.*server" | grep -v grep || echo "No server running"

echo ""
echo "=== Check Complete ==="
```

---

## 📞 الحصول على المساعدة / Getting Help

### 1. معلومات مفيدة عند طلب المساعدة / Useful Information When Requesting Help

قدّم المعلومات التالية:
Provide the following information:

```bash
# System information
uname -a
python3 --version
pip --version

# Application version
cat README.md | grep Version

# Error logs
tail -50 logs/error.log

# Configuration (hide sensitive data!)
cat .env | grep -v PASSWORD | grep -v TOKEN | grep -v SECRET
```

### 2. قنوات الدعم / Support Channels

- 📧 **Email:** support@university.edu.sa
- 📖 **Documentation:** See repository docs/
- 🐛 **Bug Reports:** GitHub Issues
- 💬 **Discussions:** GitHub Discussions

### 3. قبل الاتصال بالدعم / Before Contacting Support

- [ ] راجع هذا الدليل / Check this guide
- [ ] ابحث في GitHub Issues / Search GitHub Issues
- [ ] تحقق من السجلات / Check logs
- [ ] جرب الحلول الشائعة / Try common solutions
- [ ] اجمع معلومات النظام / Collect system information

---

## 📚 موارد إضافية / Additional Resources

- [PRODUCTION_DEPLOYMENT_GUIDE.md](PRODUCTION_DEPLOYMENT_GUIDE.md) - دليل النشر الإنتاجي
- [SECURITY.md](SECURITY.md) - سياسة الأمان
- [API_DOCUMENTATION.md](API_DOCUMENTATION.md) - توثيق API
- [USER_SECURITY_TRAINING.md](docs/USER_SECURITY_TRAINING.md) - التدريب الأمني

---

**آخر تحديث / Last Updated:** 2025-11-17  
**الإصدار / Version:** 2.0.1
