# دليل تكوين الإنتاج
# Production Configuration Guide

**التاريخ / Date:** 2025-11-05  
**الإصدار / Version:** 1.0

---

## 1. تكوين البيئة / Environment Configuration

### 1.1 ملف البيئة / Environment File

أنشئ ملف `.env` في المجلد الرئيسي:
Create `.env` file in the root directory:

```bash
# Flask Configuration
FLASK_ENV=production
FLASK_DEBUG=False
SECRET_KEY=your-very-long-random-secret-key-here-change-this

# Database Configuration
DATABASE_PATH=/var/www/housing/housing.db

# Server Configuration
HOST=0.0.0.0
PORT=5000

# Security Configuration
SESSION_TIMEOUT_HOURS=24
SESSION_COOKIE_SECURE=True
SESSION_COOKIE_HTTPONLY=True
SESSION_COOKIE_SAMESITE=Lax

# Logging
LOG_LEVEL=INFO
LOG_FILE=/var/log/housing/app.log
```

### 1.2 توليد مفتاح سري / Generate Secret Key

```bash
python3 -c "import secrets; print(secrets.token_hex(32))"
```

---

## 2. تثبيت على الخادم / Server Installation

### 2.1 تثبيت المتطلبات / Install Requirements

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Python and dependencies
sudo apt install -y python3 python3-pip python3-venv nginx certbot python3-certbot-nginx

# Create application directory
sudo mkdir -p /var/www/housing
sudo chown $USER:$USER /var/www/housing

# Clone repository
cd /var/www/housing
git clone https://github.com/Ali5829511/2025.git .

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install Python packages
pip install -r requirements.txt
pip install gunicorn

# Create log directory
sudo mkdir -p /var/log/housing
sudo chown $USER:$USER /var/log/housing
```

### 2.2 تهيئة قاعدة البيانات / Initialize Database

```bash
cd /var/www/housing
source venv/bin/activate
python3 database.py
```

**⚠️ مهم: غيّر كلمات المرور الافتراضية!**  
**⚠️ Important: Change default passwords!**

```bash
# Connect to database and update passwords
sqlite3 housing.db

-- Update admin password (example)
UPDATE users SET password_hash = '<new-hashed-password>' WHERE username = 'admin';

-- Exit
.exit
```

أو استخدم واجهة إدارة المستخدمين لتغيير كلمات المرور.  
Or use the user management interface to change passwords.

---

## 3. تكوين Gunicorn / Gunicorn Configuration

### 3.1 إنشاء ملف تكوين / Create Configuration File

```bash
sudo nano /etc/systemd/system/housing.service
```

```ini
[Unit]
Description=Faculty Housing Management System
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/var/www/housing
Environment="PATH=/var/www/housing/venv/bin"
Environment="FLASK_ENV=production"
Environment="FLASK_DEBUG=False"
ExecStart=/var/www/housing/venv/bin/gunicorn \
    --workers 4 \
    --bind 0.0.0.0:5000 \
    --timeout 120 \
    --access-logfile /var/log/housing/access.log \
    --error-logfile /var/log/housing/error.log \
    --log-level info \
    server:app

[Install]
WantedBy=multi-user.target
```

### 3.2 تفعيل وتشغيل الخدمة / Enable and Start Service

```bash
# Set permissions
sudo chown -R www-data:www-data /var/www/housing
sudo chmod -R 755 /var/www/housing

# Reload systemd
sudo systemctl daemon-reload

# Enable service to start on boot
sudo systemctl enable housing

# Start service
sudo systemctl start housing

# Check status
sudo systemctl status housing
```

---

## 4. تكوين Nginx / Nginx Configuration

### 4.1 إنشاء ملف تكوين / Create Configuration File

```bash
sudo nano /etc/nginx/sites-available/housing
```

```nginx
# HTTP to HTTPS redirect
server {
    listen 80;
    listen [::]:80;
    server_name your-domain.edu.sa www.your-domain.edu.sa;
    
    # Redirect to HTTPS
    return 301 https://$server_name$request_uri;
}

# HTTPS server
server {
    listen 443 ssl http2;
    listen [::]:443 ssl http2;
    server_name your-domain.edu.sa www.your-domain.edu.sa;
    
    # SSL Configuration
    ssl_certificate /etc/letsencrypt/live/your-domain.edu.sa/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/your-domain.edu.sa/privkey.pem;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;
    ssl_prefer_server_ciphers on;
    
    # Security Headers
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header Referrer-Policy "strict-origin-when-cross-origin" always;
    
    # Logging
    access_log /var/log/nginx/housing_access.log;
    error_log /var/log/nginx/housing_error.log;
    
    # Root directory
    root /var/www/housing;
    
    # Max upload size
    client_max_body_size 10M;
    
    # Proxy to Gunicorn
    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # Timeouts
        proxy_connect_timeout 60s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;
    }
    
    # Static files (if needed)
    location ~* \.(jpg|jpeg|png|gif|ico|css|js|svg|pdf)$ {
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
}
```

### 4.2 تفعيل التكوين / Enable Configuration

```bash
# Create symbolic link
sudo ln -s /etc/nginx/sites-available/housing /etc/nginx/sites-enabled/

# Test configuration
sudo nginx -t

# Restart Nginx
sudo systemctl restart nginx
```

---

## 5. تكوين SSL / SSL Configuration

### 5.1 الحصول على شهادة Let's Encrypt / Get Let's Encrypt Certificate

```bash
# Stop Nginx temporarily
sudo systemctl stop nginx

# Get certificate
sudo certbot certonly --standalone -d your-domain.edu.sa -d www.your-domain.edu.sa

# Start Nginx
sudo systemctl start nginx
```

### 5.2 التجديد التلقائي / Auto-Renewal

```bash
# Test renewal
sudo certbot renew --dry-run

# Add to crontab for auto-renewal
sudo crontab -e

# Add this line:
0 3 * * * certbot renew --quiet --post-hook "systemctl reload nginx"
```

---

## 6. تكوين جدار الحماية / Firewall Configuration

### 6.1 UFW (Ubuntu)

```bash
# Enable UFW
sudo ufw enable

# Allow SSH
sudo ufw allow 22/tcp

# Allow HTTP and HTTPS
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp

# Check status
sudo ufw status
```

### 6.2 Fail2ban (حماية من هجمات القوة الغاشمة / Brute Force Protection)

```bash
# Install Fail2ban
sudo apt install -y fail2ban

# Create custom config
sudo nano /etc/fail2ban/jail.local
```

```ini
[DEFAULT]
bantime = 3600
findtime = 600
maxretry = 5

[nginx-http-auth]
enabled = true
port = http,https
logpath = /var/log/nginx/housing_error.log
```

```bash
# Restart Fail2ban
sudo systemctl restart fail2ban
```

---

## 7. النسخ الاحتياطي / Backup Configuration

### 7.1 سكريبت النسخ الاحتياطي / Backup Script

```bash
sudo nano /usr/local/bin/housing-backup.sh
```

```bash
#!/bin/bash

# Configuration
BACKUP_DIR="/var/backups/housing"
DB_PATH="/var/www/housing/housing.db"
DATE=$(date +%Y%m%d_%H%M%S)

# Create backup directory
mkdir -p $BACKUP_DIR

# Backup database
sqlite3 $DB_PATH ".backup '$BACKUP_DIR/housing_$DATE.db'"

# Compress old backups
find $BACKUP_DIR -name "*.db" -mtime +1 -exec gzip {} \;

# Delete backups older than 30 days
find $BACKUP_DIR -name "*.db.gz" -mtime +30 -delete

echo "Backup completed: housing_$DATE.db"
```

```bash
# Make executable
sudo chmod +x /usr/local/bin/housing-backup.sh

# Add to crontab (daily at 2 AM)
sudo crontab -e

# Add this line:
0 2 * * * /usr/local/bin/housing-backup.sh >> /var/log/housing/backup.log 2>&1
```

### 7.2 استعادة من نسخة احتياطية / Restore from Backup

```bash
# Stop application
sudo systemctl stop housing

# Restore database
cp /var/backups/housing/housing_20231105_020000.db /var/www/housing/housing.db

# Set permissions
sudo chown www-data:www-data /var/www/housing/housing.db

# Start application
sudo systemctl start housing
```

---

## 8. المراقبة والسجلات / Monitoring and Logs

### 8.1 عرض السجلات / View Logs

```bash
# Application logs
sudo journalctl -u housing -f

# Nginx access logs
sudo tail -f /var/log/nginx/housing_access.log

# Nginx error logs
sudo tail -f /var/log/nginx/housing_error.log

# Application error logs
sudo tail -f /var/log/housing/error.log
```

### 8.2 تدوير السجلات / Log Rotation

```bash
sudo nano /etc/logrotate.d/housing
```

```
/var/log/housing/*.log {
    daily
    rotate 14
    compress
    delaycompress
    notifempty
    create 0640 www-data www-data
    sharedscripts
    postrotate
        systemctl reload housing > /dev/null 2>&1 || true
    endscript
}
```

---

## 9. الأمان الإضافي / Additional Security

### 9.1 تعطيل root login عبر SSH

```bash
sudo nano /etc/ssh/sshd_config
```

```
PermitRootLogin no
PasswordAuthentication no
```

```bash
sudo systemctl restart ssh
```

### 9.2 تحديثات تلقائية للأمان / Automatic Security Updates

```bash
sudo apt install -y unattended-upgrades
sudo dpkg-reconfigure -plow unattended-upgrades
```

---

## 10. قائمة فحص النشر / Deployment Checklist

### قبل النشر / Before Deployment
- [ ] تغيير جميع كلمات المرور الافتراضية
- [ ] تعيين FLASK_DEBUG=False
- [ ] توليد SECRET_KEY جديد وآمن
- [ ] تكوين HTTPS مع شهادة SSL
- [ ] إعداد جدار الحماية
- [ ] تكوين النسخ الاحتياطي التلقائي
- [ ] إعداد Fail2ban
- [ ] تكوين تدوير السجلات
- [ ] اختبار النظام في بيئة staging
- [ ] مراجعة صلاحيات الملفات

### بعد النشر / After Deployment
- [ ] التحقق من عمل النظام
- [ ] اختبار تسجيل الدخول
- [ ] التحقق من HTTPS
- [ ] اختبار النسخ الاحتياطي
- [ ] مراقبة السجلات
- [ ] إعداد المراقبة والتنبيهات

---

## 11. استكشاف الأخطاء / Troubleshooting

### مشكلة: الخدمة لا تعمل / Service Not Starting

```bash
# Check service status
sudo systemctl status housing

# Check logs
sudo journalctl -u housing -n 50

# Check if port is in use
sudo netstat -tulpn | grep 5000
```

### مشكلة: خطأ في قاعدة البيانات / Database Error

```bash
# Check database permissions
ls -la /var/www/housing/housing.db

# Fix permissions
sudo chown www-data:www-data /var/www/housing/housing.db
sudo chmod 644 /var/www/housing/housing.db
```

### مشكلة: خطأ 502 Bad Gateway

```bash
# Check if Gunicorn is running
ps aux | grep gunicorn

# Restart services
sudo systemctl restart housing
sudo systemctl restart nginx
```

---

## 12. معلومات الاتصال / Contact Information

للدعم الفني / For Technical Support:
- فريق تقنية المعلومات بالجامعة
- IT Team at the University
- البريد الإلكتروني / Email: it-support@university.edu.sa

---

**آخر تحديث / Last Updated:** 2025-11-05  
**الإصدار / Version:** 1.0
