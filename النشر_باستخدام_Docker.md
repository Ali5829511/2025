# 🐳 النشر باستخدام Docker
# Deployment Using Docker

**الطريقة الأسرع والأسهل للنشر!**

---

## 📋 نظرة عامة

هذا الدليل يوضح كيفية نشر النظام باستخدام Docker وDocker Compose بخطوات بسيطة جداً.

### ✨ المميزات
- ✅ نشر سريع (5 دقائق فقط)
- ✅ لا حاجة لتثبيت Python أو PostgreSQL يدوياً
- ✅ بيئة معزولة وآمنة
- ✅ سهولة الترقية والصيانة
- ✅ يعمل على أي نظام تشغيل

---

## 🚀 المتطلبات

### تثبيت Docker و Docker Compose

#### على Ubuntu/Linux:
```bash
# تثبيت Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# تثبيت Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# إضافة المستخدم الحالي لمجموعة docker
sudo usermod -aG docker $USER
newgrp docker

# التحقق من التثبيت
docker --version
docker-compose --version
```

#### على Windows:
1. حمّل وثبّت [Docker Desktop for Windows](https://www.docker.com/products/docker-desktop)
2. أعد تشغيل الجهاز
3. تأكد من تشغيل Docker Desktop

#### على macOS:
1. حمّل وثبّت [Docker Desktop for Mac](https://www.docker.com/products/docker-desktop)
2. افتح Docker Desktop من Applications
3. تأكد من تشغيله

---

## 🎯 خطوات النشر السريع

### 1. تحميل المشروع

```bash
# استنساخ المشروع
git clone https://github.com/Ali5829511/2025.git
cd 2025
```

### 2. إعداد ملف البيئة (اختياري)

```bash
# إنشاء ملف .env للإعدادات (اختياري)
cat > .env <<EOF
DB_PASSWORD=كلمة_مرور_قوية_لقاعدة_البيانات
SECRET_KEY=$(openssl rand -hex 32)
EOF
```

### 3. بناء وتشغيل النظام

```bash
# بناء وتشغيل جميع الخدمات
docker-compose up -d

# مشاهدة السجلات
docker-compose logs -f
```

### 4. انتظر حتى يكتمل التشغيل

```bash
# التحقق من حالة الخدمات
docker-compose ps

# يجب أن ترى جميع الخدمات بحالة "Up"
```

### 5. الوصول للنظام

افتح المتصفح على:
```
http://localhost
أو
http://YOUR_SERVER_IP
```

---

## 🔐 بيانات الدخول الافتراضية

| المستخدم | اسم المستخدم | كلمة المرور |
|----------|--------------|-------------|
| مدير النظام | admin | Admin@2025 |
| مسؤول المخالفات | violations_officer | Violations@2025 |
| مسؤول الزوار | visitors_officer | Visitors@2025 |
| مستخدم عرض | viewer | Viewer@2025 |
| مسجل المخالفات | violation_entry | Violation@2025 |

⚠️ **مهم جداً:** غيّر هذه الكلمات فوراً بعد أول تسجيل دخول!

---

## 🛠️ أوامر الإدارة

### مشاهدة حالة الخدمات
```bash
docker-compose ps
```

### مشاهدة السجلات
```bash
# جميع السجلات
docker-compose logs -f

# سجلات خدمة معينة
docker-compose logs -f web
docker-compose logs -f db
docker-compose logs -f nginx
```

### إيقاف النظام
```bash
docker-compose stop
```

### تشغيل النظام
```bash
docker-compose start
```

### إعادة تشغيل النظام
```bash
docker-compose restart
```

### إيقاف وحذف الخدمات
```bash
docker-compose down

# حذف مع البيانات (احذر!)
docker-compose down -v
```

### تحديث النظام
```bash
# سحب آخر التحديثات
git pull origin main

# إعادة بناء وتشغيل
docker-compose up -d --build
```

---

## 📊 هيكل الخدمات

### الخدمات المكونة:

#### 1. قاعدة البيانات (PostgreSQL)
- **Container:** `housing_db`
- **المنفذ:** 5432 (داخلي)
- **البيانات:** محفوظة في volume `postgres_data`

#### 2. التطبيق (Flask + Gunicorn)
- **Container:** `housing_web`
- **المنفذ:** 8000 (داخلي)
- **الملفات:** محفوظة في المجلد الحالي

#### 3. Nginx (Reverse Proxy)
- **Container:** `housing_nginx`
- **المنفذ:** 80 (HTTP) و 443 (HTTPS)
- **الوظيفة:** توزيع الطلبات والملفات الثابتة

---

## 🔒 إعدادات الأمان

### 1. تغيير كلمة مرور قاعدة البيانات

```bash
# عدّل ملف .env
nano .env

# غيّر القيمة:
DB_PASSWORD=كلمة_مرور_قوية_جديدة

# أعد بناء الخدمات
docker-compose down
docker-compose up -d
```

### 2. إضافة HTTPS (شهادة SSL)

```bash
# احصل على شهادة من Let's Encrypt
sudo apt install certbot
sudo certbot certonly --standalone -d YOUR_DOMAIN.com

# انسخ الشهادات
mkdir -p ssl
sudo cp /etc/letsencrypt/live/YOUR_DOMAIN.com/fullchain.pem ssl/
sudo cp /etc/letsencrypt/live/YOUR_DOMAIN.com/privkey.pem ssl/

# عدّل nginx.conf لإضافة إعدادات SSL
nano nginx.conf

# أعد تشغيل nginx
docker-compose restart nginx
```

### 3. جدار الحماية

```bash
# السماح بـ HTTP و HTTPS فقط
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw enable
```

---

## 💾 النسخ الاحتياطي والاستعادة

### النسخ الاحتياطي

```bash
# نسخ قاعدة البيانات
docker-compose exec db pg_dump -U housing_user housing_db > backup_$(date +%Y%m%d).sql

# نسخ جميع البيانات
docker run --rm --volumes-from housing_db -v $(pwd):/backup ubuntu tar cvf /backup/db_data_backup.tar /var/lib/postgresql/data
```

### الاستعادة

```bash
# استعادة قاعدة البيانات
cat backup_20251105.sql | docker-compose exec -T db psql -U housing_user housing_db
```

### النسخ الاحتياطي التلقائي

```bash
# إنشاء سكريبت للنسخ الاحتياطي التلقائي
cat > backup.sh <<'EOF'
#!/bin/bash
BACKUP_DIR="/home/backups"
DATE=$(date +%Y%m%d_%H%M%S)
mkdir -p $BACKUP_DIR
docker-compose exec -T db pg_dump -U housing_user housing_db | gzip > $BACKUP_DIR/housing_db_$DATE.sql.gz
find $BACKUP_DIR -name "*.sql.gz" -mtime +30 -delete
EOF

chmod +x backup.sh

# جدولة النسخ اليومي
crontab -e
# أضف: 0 2 * * * /path/to/backup.sh
```

---

## 📈 المراقبة

### مشاهدة استخدام الموارد

```bash
# استخدام CPU والذاكرة
docker stats

# مساحة التخزين
docker system df
```

### التحقق من صحة النظام

```bash
# اختبار API
curl http://localhost/api/health

# اختبار قاعدة البيانات
docker-compose exec db psql -U housing_user -d housing_db -c "SELECT COUNT(*) FROM users;"

# اختبار صفحة التقرير
curl -I http://localhost/system_validation_report.html
```

---

## 🐛 استكشاف الأخطاء

### المشكلة: الخدمات لا تبدأ

```bash
# التحقق من السجلات
docker-compose logs

# التحقق من حالة الخدمات
docker-compose ps

# إعادة البناء
docker-compose down
docker-compose up -d --build
```

### المشكلة: خطأ في قاعدة البيانات

```bash
# الدخول لـ container قاعدة البيانات
docker-compose exec db psql -U housing_user -d housing_db

# التحقق من الاتصال
docker-compose exec web python3 -c "import database; print('OK')"
```

### المشكلة: المنفذ 80 مستخدم

```bash
# إيقاف الخدمة التي تستخدم المنفذ
sudo lsof -i :80
sudo systemctl stop apache2  # أو nginx

# أو تغيير المنفذ في docker-compose.yml
# ports:
#   - "8080:80"
```

### حذف كل شيء وإعادة البدء

```bash
# إيقاف وحذف كل شيء
docker-compose down -v
docker system prune -a

# إعادة البناء والتشغيل
docker-compose up -d --build
```

---

## 🚀 النشر على خادم إنتاج

### 1. على خادم سحابي (AWS, Azure, GCP)

```bash
# على الخادم، ثبّت Docker
curl -fsSL https://get.docker.com | sh

# استنسخ المشروع
git clone https://github.com/Ali5829511/2025.git
cd 2025

# أنشئ ملف .env بإعدادات آمنة
cat > .env <<EOF
DB_PASSWORD=$(openssl rand -base64 32)
SECRET_KEY=$(openssl rand -hex 32)
EOF

# شغّل النظام
docker-compose up -d

# تابع السجلات
docker-compose logs -f
```

### 2. إعداد اسم النطاق

```bash
# عدّل nginx.conf
nano nginx.conf

# غيّر server_name من _ إلى YOUR_DOMAIN.com
server_name YOUR_DOMAIN.com www.YOUR_DOMAIN.com;

# أعد تشغيل nginx
docker-compose restart nginx
```

### 3. إضافة SSL تلقائياً

```bash
# استخدم Certbot في container منفصل
docker run -it --rm --name certbot \
  -v "/etc/letsencrypt:/etc/letsencrypt" \
  -v "/var/lib/letsencrypt:/var/lib/letsencrypt" \
  -p 80:80 -p 443:443 \
  certbot/certbot certonly --standalone -d YOUR_DOMAIN.com

# انسخ الشهادات
mkdir -p ssl
sudo cp /etc/letsencrypt/live/YOUR_DOMAIN.com/* ssl/

# عدّل docker-compose.yml لإضافة volumes للشهادات
# ثم أعد التشغيل
docker-compose restart nginx
```

---

## ✅ قائمة التحقق

قبل الإطلاق الرسمي:

- [ ] تم تغيير كلمات المرور الافتراضية
- [ ] تم إعداد كلمة مرور قوية لقاعدة البيانات
- [ ] تم إعداد SECRET_KEY عشوائي
- [ ] تم تكوين اسم النطاق
- [ ] تم تثبيت شهادة SSL
- [ ] تم إعداد النسخ الاحتياطي التلقائي
- [ ] تم اختبار جميع الوظائف
- [ ] تم تكوين جدار الحماية
- [ ] تم إعداد المراقبة والتنبيهات

---

## 📚 موارد إضافية

- [دليل النشر الكامل](دليل_النشر_الكامل.md)
- [QUICK_START.md](QUICK_START.md)
- [حل_خطأ_500.md](حل_خطأ_500.md)
- [Docker Documentation](https://docs.docker.com/)
- [Docker Compose Documentation](https://docs.docker.com/compose/)

---

## 🎉 تهانينا!

نظامك الآن يعمل في بيئة Docker احترافية! 🚀

**النشر باستخدام Docker يوفر:**
- بيئة معزولة وآمنة
- سهولة الترقية والصيانة
- قابلية التوسع
- إمكانية النقل بين الخوادم

---

**جامعة الإمام محمد بن سعود الإسلامية © 2025**
