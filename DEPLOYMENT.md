# دليل النشر / Deployment Guide

## نظرة عامة / Overview

هذا الدليل يوضح كيفية نشر نظام إدارة إسكان أعضاء هيئة التدريس في بيئة الإنتاج.

This guide explains how to deploy the Faculty Housing Management System in a production environment.

## المتطلبات / Requirements

### الأجهزة / Hardware
- معالج: 2 CPU cores على الأقل / Minimum 2 CPU cores
- ذاكرة RAM: 4 GB على الأقل / Minimum 4 GB RAM
- مساحة التخزين: 20 GB على الأقل / Minimum 20 GB storage

### البرمجيات / Software
- Ubuntu 20.04 LTS أو أحدث / or newer
- Python 3.8 أو أحدث / or higher
- Nginx أو Apache / or Apache
- PostgreSQL أو MySQL / or MySQL
- شهادة SSL صالحة / Valid SSL certificate

## خطوات النشر / Deployment Steps

### 1. إعداد الخادم / Server Setup

```bash
# تحديث النظام / Update system
sudo apt update && sudo apt upgrade -y

# تثبيت Python والتبعيات / Install Python and dependencies
sudo apt install python3 python3-pip python3-venv nginx postgresql -y

# إنشاء مستخدم للتطبيق / Create application user
sudo useradd -m -s /bin/bash housingapp
sudo su - housingapp
```

### 2. نسخ التطبيق / Clone Application

```bash
# نسخ المستودع / Clone repository
git clone https://github.com/Ali5829511/2025.git housing-system
cd housing-system

# إنشاء بيئة افتراضية / Create virtual environment
python3 -m venv venv
source venv/bin/activate

# تثبيت المتطلبات / Install requirements
pip install -r requirements.txt
pip install gunicorn psycopg2-binary
```

### 3. إعداد قاعدة البيانات / Database Setup

```bash
# الدخول إلى PostgreSQL / Access PostgreSQL
sudo -u postgres psql

# إنشاء قاعدة البيانات / Create database
CREATE DATABASE housing_db;
CREATE USER housing_user WITH PASSWORD 'secure_password_here';
GRANT ALL PRIVILEGES ON DATABASE housing_db TO housing_user;
\q
```

### 4. تكوين التطبيق / Application Configuration

```bash
# إنشاء ملف التكوين / Create configuration file
cat > .env << EOF
FLASK_ENV=production
SECRET_KEY=$(python3 -c 'import secrets; print(secrets.token_hex(32))')
DATABASE_URL=postgresql://housing_user:secure_password_here@localhost/housing_db
ALLOWED_HOSTS=your-domain.com
EOF
```

### 5. إنشاء خدمة Systemd / Create Systemd Service

```bash
# إنشاء ملف الخدمة / Create service file
sudo nano /etc/systemd/system/housing.service
```

أضف المحتوى التالي / Add the following content:

```ini
[Unit]
Description=Faculty Housing Management System
After=network.target

[Service]
User=housingapp
Group=www-data
WorkingDirectory=/home/housingapp/housing-system
Environment="PATH=/home/housingapp/housing-system/venv/bin"
ExecStart=/home/housingapp/housing-system/venv/bin/gunicorn --workers 3 --bind 127.0.0.1:8000 main:app

[Install]
WantedBy=multi-user.target
```

```bash
# تفعيل الخدمة / Enable service
sudo systemctl enable housing
sudo systemctl start housing
sudo systemctl status housing
```

### 6. تكوين Nginx / Configure Nginx

```bash
# إنشاء ملف التكوين / Create configuration file
sudo nano /etc/nginx/sites-available/housing
```

أضف المحتوى التالي / Add the following content:

```nginx
server {
    listen 80;
    server_name your-domain.com www.your-domain.com;
    
    # إعادة توجيه HTTP إلى HTTPS
    # Redirect HTTP to HTTPS
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name your-domain.com www.your-domain.com;
    
    # شهادة SSL / SSL certificate
    ssl_certificate /etc/letsencrypt/live/your-domain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/your-domain.com/privkey.pem;
    
    # إعدادات SSL / SSL settings
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;
    ssl_prefer_server_ciphers on;
    
    # الحد الأقصى لحجم الملف / Max file size
    client_max_body_size 10M;
    
    # السجلات / Logs
    access_log /var/log/nginx/housing-access.log;
    error_log /var/log/nginx/housing-error.log;
    
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
    
    # ملفات ثابتة / Static files
    location /static {
        alias /home/housingapp/housing-system/static;
        expires 30d;
    }
}
```

```bash
# تفعيل الموقع / Enable site
sudo ln -s /etc/nginx/sites-available/housing /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### 7. الحصول على شهادة SSL / Obtain SSL Certificate

```bash
# تثبيت Certbot / Install Certbot
sudo apt install certbot python3-certbot-nginx -y

# الحصول على الشهادة / Obtain certificate
sudo certbot --nginx -d your-domain.com -d www.your-domain.com

# تجديد تلقائي / Auto-renewal
sudo systemctl enable certbot.timer
```

### 8. إعداد جدار الحماية / Configure Firewall

```bash
# السماح بـ HTTP و HTTPS / Allow HTTP and HTTPS
sudo ufw allow 'Nginx Full'
sudo ufw allow OpenSSH
sudo ufw enable
sudo ufw status
```

### 9. النسخ الاحتياطي / Backup Setup

```bash
# إنشاء سكريبت النسخ الاحتياطي / Create backup script
sudo nano /usr/local/bin/backup-housing.sh
```

أضف المحتوى التالي / Add the following content:

```bash
#!/bin/bash
BACKUP_DIR="/var/backups/housing"
DATE=$(date +%Y%m%d_%H%M%S)

# إنشاء دليل النسخ الاحتياطي / Create backup directory
mkdir -p $BACKUP_DIR

# نسخ قاعدة البيانات / Backup database
sudo -u postgres pg_dump housing_db > $BACKUP_DIR/db_$DATE.sql

# نسخ الملفات / Backup files
tar -czf $BACKUP_DIR/files_$DATE.tar.gz /home/housingapp/housing-system

# حذف النسخ القديمة (أكثر من 30 يوم) / Delete old backups (older than 30 days)
find $BACKUP_DIR -type f -mtime +30 -delete

echo "Backup completed: $DATE"
```

```bash
# جعل السكريبت قابل للتنفيذ / Make script executable
sudo chmod +x /usr/local/bin/backup-housing.sh

# جدولة النسخ الاحتياطي اليومي / Schedule daily backup
sudo crontab -e
# أضف السطر التالي / Add the following line:
0 2 * * * /usr/local/bin/backup-housing.sh
```

### 10. المراقبة / Monitoring

```bash
# تثبيت أدوات المراقبة / Install monitoring tools
sudo apt install htop iotop nethogs -y

# عرض السجلات / View logs
sudo journalctl -u housing -f
sudo tail -f /var/log/nginx/housing-access.log
sudo tail -f /var/log/nginx/housing-error.log
```

## قائمة التحقق النهائية / Final Checklist

قبل الإطلاق، تأكد من:
Before launch, ensure:

- [ ] تم تغيير جميع كلمات المرور الافتراضية / All default passwords changed
- [ ] تم تعطيل وضع التصحيح / Debug mode disabled
- [ ] تم تكوين HTTPS / HTTPS configured
- [ ] تم اختبار النسخ الاحتياطي / Backup tested
- [ ] تم تكوين جدار الحماية / Firewall configured
- [ ] تم اختبار جميع الميزات / All features tested
- [ ] تم مراجعة السجلات / Logs reviewed
- [ ] تم توثيق بيانات الاتصال / Contact information documented

## استكشاف الأخطاء / Troubleshooting

### التطبيق لا يبدأ / Application Won't Start

```bash
# فحص السجلات / Check logs
sudo journalctl -u housing -n 50
sudo systemctl status housing

# إعادة تشغيل الخدمة / Restart service
sudo systemctl restart housing
```

### مشاكل الاتصال بقاعدة البيانات / Database Connection Issues

```bash
# فحص حالة PostgreSQL / Check PostgreSQL status
sudo systemctl status postgresql

# فحص الاتصال / Test connection
psql -U housing_user -d housing_db -h localhost
```

### مشاكل Nginx / Nginx Issues

```bash
# فحص التكوين / Test configuration
sudo nginx -t

# فحص السجلات / Check logs
sudo tail -f /var/log/nginx/error.log
```

## التحديثات / Updates

```bash
# إيقاف الخدمة / Stop service
sudo systemctl stop housing

# سحب التحديثات / Pull updates
cd /home/housingapp/housing-system
git pull origin main

# تحديث التبعيات / Update dependencies
source venv/bin/activate
pip install -r requirements.txt --upgrade

# تشغيل الخدمة / Start service
sudo systemctl start housing
```

## الدعم / Support

للحصول على المساعدة:
For assistance:

- مراجعة الوثائق / Review documentation
- فحص السجلات / Check logs
- التواصل مع فريق تقنية المعلومات / Contact IT team

---

**تم إنشاؤه بواسطة / Created by:** فريق التطوير / Development Team  
**آخر تحديث / Last Updated:** نوفمبر 2025 / November 2025
