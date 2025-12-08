# Production Deployment Checklist
# قائمة التحقق من النشر الإنتاجي

## 🎯 Overview / نظرة عامة

This comprehensive checklist ensures your Housing Management System is production-ready with proper security, performance, and reliability configurations.

هذه القائمة الشاملة تضمن أن نظام إدارة الإسكان جاهز للإنتاج مع تكوينات الأمان والأداء والموثوقية المناسبة.

---

## ✅ Pre-Deployment Checklist / قائمة ما قبل النشر

### 1. Security Configuration / تكوين الأمان

#### 1.1 Password Security / أمان كلمات المرور
- [x] **Change all default passwords** - نظام فرض تغيير كلمات المرور مفعّل
  - ✅ System enforces password change on first login
  - ✅ Default passwords: `Admin@2025`, `Violations@2025`, `Visitors@2025`, `Viewer@2025`, `Violation@2025`
  - ✅ Password requirements: minimum 8 characters
  - **Action Required:** Ensure all users change their passwords on first login

#### 1.2 Environment Variables / متغيرات البيئة
- [ ] **Set SECRET_KEY** - تعيين مفتاح سري قوي
  ```bash
  # Generate strong secret key
  python3 -c "import secrets; print(secrets.token_hex(32))"
  
  # Set in environment
  export SECRET_KEY="your-generated-secret-key-here"
  ```
  
- [ ] **Configure DATABASE_URL** - تكوين قاعدة البيانات
  ```bash
  # For PostgreSQL (recommended for production)
  export DATABASE_URL="postgresql://user:password@host:port/database"
  
  # For MySQL
  export DATABASE_URL="mysql://user:password@host:port/database"
  ```

- [x] **Disable debug mode** - تعطيل وضع التصحيح
  ```bash
  export FLASK_ENV=production
  export FLASK_DEBUG=False
  ```
  ✅ Already configured in all deployment files

#### 1.3 Security Headers / ترويسات الأمان
- [x] **Security headers configured** - ترويسات الأمان مكونة
  - ✅ X-Frame-Options: SAMEORIGIN
  - ✅ X-Content-Type-Options: nosniff
  - ✅ X-XSS-Protection: 1; mode=block
  - ✅ Content-Security-Policy (production only)
  - ✅ Strict-Transport-Security (HTTPS only)
  - ✅ Referrer-Policy: strict-origin-when-cross-origin
  - ✅ Permissions-Policy

### 2. SSL/TLS Configuration / تكوين SSL/TLS

#### 2.1 HTTPS Setup / إعداد HTTPS
- [ ] **Obtain SSL certificate** - الحصول على شهادة SSL
  
  **Option 1: Let's Encrypt (Free)** - خيار 1: Let's Encrypt (مجاني)
  ```bash
  # Install certbot
  sudo apt-get install certbot python3-certbot-nginx
  
  # Obtain certificate
  sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com
  ```
  
  **Option 2: Commercial Certificate** - خيار 2: شهادة تجارية
  - Purchase from: DigiCert, GlobalSign, Comodo, etc.
  - Follow provider's installation instructions

- [ ] **Configure web server for HTTPS** - تكوين خادم الويب لـ HTTPS
  - See `docs/deployment/NGINX_SSL_CONFIG.md` for Nginx configuration
  - Certificate files should be stored securely (permissions 600)
  - Enable HTTP to HTTPS redirect

#### 2.2 SSL Testing / اختبار SSL
- [ ] **Test SSL configuration**
  ```bash
  # Test with OpenSSL
  openssl s_client -connect yourdomain.com:443 -servername yourdomain.com
  
  # Online test
  # Visit: https://www.ssllabs.com/ssltest/
  ```

### 3. Web Server Configuration / تكوين خادم الويب

#### 3.1 WSGI Server / خادم WSGI
- [x] **Gunicorn configured** - Gunicorn مكون
  - ✅ Configuration file: `gunicorn_config.py`
  - ✅ Worker processes optimized
  - ✅ Timeout: 120 seconds
  - ✅ Request limits configured
  
  **Start command:**
  ```bash
  gunicorn --config gunicorn_config.py server:app
  ```

#### 3.2 Reverse Proxy / الوكيل العكسي
- [ ] **Configure Nginx/Apache**
  - See `docs/deployment/NGINX_SSL_CONFIG.md`
  - Enable gzip compression
  - Configure caching headers
  - Set up rate limiting

### 4. Database Configuration / تكوين قاعدة البيانات

#### 4.1 Database Migration / ترحيل قاعدة البيانات
- [ ] **Migrate to PostgreSQL or MySQL** (Optional but recommended)
  
  **Using migration script:**
  ```bash
  # Backup current SQLite database
  ./scripts/backup_database.sh
  
  # Run migration
  python3 scripts/migrate_to_postgresql.py
  
  # Or for MySQL
  python3 scripts/migrate_to_mysql.py
  ```
  
  **Manual migration:**
  ```bash
  # Export from SQLite
  sqlite3 housing.db .dump > housing_dump.sql
  
  # Import to PostgreSQL
  psql -U username -d database -f housing_dump.sql
  ```

#### 4.2 Database Security / أمان قاعدة البيانات
- [ ] **Secure database credentials**
  - Use strong passwords (16+ characters)
  - Store credentials in environment variables
  - Enable SSL for database connections
  
- [ ] **Configure database access**
  - Restrict network access to database server
  - Use firewall rules
  - Enable database audit logging

#### 4.3 Automated Backups / النسخ الاحتياطية التلقائية
- [x] **Backup script available** - سكريبت النسخ الاحتياطي متوفر
  - ✅ Script: `scripts/backup_database.sh`
  - ✅ Supports SQLite and PostgreSQL
  - ✅ Compression enabled
  - ✅ S3 upload support

- [ ] **Schedule automated backups**
  
  **Using cron (Linux):**
  ```bash
  # Edit crontab
  crontab -e
  
  # Add daily backup at 2 AM
  0 2 * * * /var/www/housing-system/scripts/backup_database.sh
  
  # Add weekly backup on Sunday
  0 3 * * 0 /var/www/housing-system/scripts/backup_database.sh
  ```
  
  **Using systemd timer (Linux):**
  ```bash
  # Create timer file
  sudo nano /etc/systemd/system/housing-backup.timer
  
  # Enable and start
  sudo systemctl enable housing-backup.timer
  sudo systemctl start housing-backup.timer
  ```

- [ ] **Configure backup retention**
  ```bash
  # Set retention period (days)
  export RETENTION_DAYS=30
  ```

- [ ] **Test backup restoration**
  ```bash
  # Test restore from backup
  gunzip -c backups/housing_20240101_120000.db.gz > housing_restored.db
  sqlite3 housing_restored.db "SELECT COUNT(*) FROM users;"
  ```

### 5. Firewall Configuration / تكوين جدار الحماية

#### 5.1 Server Firewall / جدار حماية الخادم
- [ ] **Configure UFW (Ubuntu/Debian)**
  ```bash
  # Enable firewall
  sudo ufw enable
  
  # Allow SSH
  sudo ufw allow 22/tcp
  
  # Allow HTTP/HTTPS
  sudo ufw allow 80/tcp
  sudo ufw allow 443/tcp
  
  # Allow PostgreSQL (if database on same server)
  sudo ufw allow from trusted_ip to any port 5432
  
  # Check status
  sudo ufw status verbose
  ```

- [ ] **Configure firewalld (RHEL/CentOS)**
  ```bash
  # Start firewall
  sudo systemctl start firewalld
  sudo systemctl enable firewalld
  
  # Allow services
  sudo firewall-cmd --permanent --add-service=http
  sudo firewall-cmd --permanent --add-service=https
  sudo firewall-cmd --permanent --add-service=ssh
  
  # Reload
  sudo firewall-cmd --reload
  ```

#### 5.2 Application Firewall / جدار حماية التطبيق
- [ ] **Configure rate limiting in Nginx**
  ```nginx
  # In nginx.conf
  limit_req_zone $binary_remote_addr zone=login:10m rate=5r/m;
  limit_req_zone $binary_remote_addr zone=api:10m rate=30r/m;
  ```

### 6. File Permissions / صلاحيات الملفات

#### 6.1 Application Files / ملفات التطبيق
- [ ] **Set proper file permissions**
  ```bash
  # Application files
  chmod 755 /var/www/housing-system
  find /var/www/housing-system -type f -name "*.py" -exec chmod 644 {} \;
  find /var/www/housing-system -type f -name "*.sh" -exec chmod 755 {} \;
  
  # Environment files (sensitive)
  chmod 600 /var/www/housing-system/.env*
  
  # Database files
  chmod 660 /var/www/housing-system/*.db
  
  # Logs directory
  chmod 750 /var/www/housing-system/logs
  chmod 640 /var/www/housing-system/logs/*.log
  
  # Uploads directory
  chmod 755 /var/www/housing-system/uploads
  ```

#### 6.2 Ownership / الملكية
- [ ] **Set proper ownership**
  ```bash
  # Change owner to application user
  sudo chown -R app_user:app_group /var/www/housing-system
  
  # For Nginx/Apache
  sudo chown -R app_user:www-data /var/www/housing-system/static
  sudo chown -R app_user:www-data /var/www/housing-system/uploads
  ```

### 7. Logging and Monitoring / السجلات والمراقبة

#### 7.1 Application Logging / سجلات التطبيق
- [x] **Logging configured** - السجلات مكونة
  - ✅ Configuration: `config/logging_config.py`
  - ✅ Security audit log
  - ✅ Error logging
  - ✅ Access logging

- [ ] **Configure log rotation**
  ```bash
  # Create logrotate configuration
  sudo nano /etc/logrotate.d/housing-system
  
  # Add configuration
  /var/www/housing-system/logs/*.log {
      daily
      rotate 30
      compress
      delaycompress
      notifempty
      missingok
      create 640 app_user app_group
  }
  ```

#### 7.2 System Monitoring / مراقبة النظام
- [ ] **Set up monitoring**
  
  **Option 1: Prometheus + Grafana**
  ```bash
  # Install prometheus-flask-exporter
  pip install prometheus-flask-exporter
  
  # Add to server.py
  from prometheus_flask_exporter import PrometheusMetrics
  metrics = PrometheusMetrics(app)
  ```
  
  **Option 2: Cloud monitoring**
  - AWS CloudWatch
  - Google Cloud Monitoring
  - Azure Monitor
  - Datadog

#### 7.3 Error Tracking / تتبع الأخطاء
- [ ] **Configure error tracking** (Optional)
  ```bash
  # Install Sentry
  pip install sentry-sdk[flask]
  
  # Add to server.py
  import sentry_sdk
  sentry_sdk.init(dsn="your-sentry-dsn")
  ```

### 8. Performance Optimization / تحسين الأداء

#### 8.1 Caching / التخزين المؤقت
- [ ] **Configure Redis caching** (Optional)
  ```bash
  # Install Redis
  sudo apt-get install redis-server
  
  # Install Python Redis client
  pip install redis flask-caching
  ```

#### 8.2 Static Files / الملفات الثابتة
- [ ] **Configure static file serving**
  - Serve static files through Nginx
  - Enable gzip compression
  - Set far-future cache headers

### 9. Security Testing / اختبار الأمان

#### 9.1 Automated Security Tests / اختبارات الأمان التلقائية
- [x] **Security testing script available** - سكريبت اختبار الأمان متوفر
  - ✅ Script: `scripts/security_tests.sh`

- [ ] **Run security tests**
  ```bash
  # Run automated tests
  ./scripts/security_tests.sh
  
  # Review results
  cat security_test_results_*.txt
  ```

#### 9.2 Penetration Testing / اختبار الاختراق
- [ ] **Perform penetration testing**
  
  **Tools:**
  - OWASP ZAP
  - Burp Suite
  - Nmap
  - SQLMap
  
  **Areas to test:**
  - [ ] SQL Injection
  - [ ] Cross-Site Scripting (XSS)
  - [ ] Cross-Site Request Forgery (CSRF)
  - [ ] Authentication bypass
  - [ ] Session management
  - [ ] File upload vulnerabilities

#### 9.3 Vulnerability Scanning / فحص الثغرات
- [ ] **Scan for vulnerabilities**
  ```bash
  # Check Python dependencies
  pip install safety
  safety check
  
  # Check for outdated packages
  pip list --outdated
  ```

### 10. Documentation / التوثيق

#### 10.1 System Documentation / توثيق النظام
- [ ] **Update documentation**
  - [ ] API documentation
  - [ ] Deployment procedures
  - [ ] Backup and recovery procedures
  - [ ] Troubleshooting guide
  - [ ] Security policies

#### 10.2 User Training / تدريب المستخدمين
- [x] **Security training documentation available**
  - ✅ Document: `docs/USER_SECURITY_TRAINING.md`

- [ ] **Conduct user training**
  - [ ] Password security
  - [ ] Phishing awareness
  - [ ] Data handling procedures
  - [ ] Incident reporting

---

## 🚀 Deployment Steps / خطوات النشر

### Step 1: Pre-Deployment / ما قبل النشر

```bash
# 1. Clone repository
git clone https://github.com/Ali5829511/2025.git
cd 2025

# 2. Create virtual environment
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate  # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure environment
cp .env.example .env
nano .env  # Edit configuration
```

### Step 2: Database Setup / إعداد قاعدة البيانات

```bash
# Option 1: SQLite (Development/Small deployments)
python3 init_db.py

# Option 2: PostgreSQL (Recommended for production)
export DATABASE_URL="postgresql://user:password@host/database"
python3 scripts/migrate_to_postgresql.py

# Option 3: MySQL
export DATABASE_URL="mysql://user:password@host/database"
python3 scripts/migrate_to_mysql.py
```

### Step 3: SSL Certificate / شهادة SSL

```bash
# Using Let's Encrypt
sudo certbot --nginx -d yourdomain.com

# Using self-signed (for testing only)
openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
  -keyout /etc/ssl/private/housing-selfsigned.key \
  -out /etc/ssl/certs/housing-selfsigned.crt
```

### Step 4: Web Server Configuration / تكوين خادم الويب

```bash
# Copy Nginx configuration
sudo cp docs/deployment/nginx-ssl.conf /etc/nginx/sites-available/housing
sudo ln -s /etc/nginx/sites-available/housing /etc/nginx/sites-enabled/

# Test configuration
sudo nginx -t

# Reload Nginx
sudo systemctl reload nginx
```

### Step 5: Application Service / خدمة التطبيق

```bash
# Copy systemd service file
sudo cp housing-system.service /etc/systemd/system/

# Reload systemd
sudo systemctl daemon-reload

# Enable and start service
sudo systemctl enable housing-system
sudo systemctl start housing-system

# Check status
sudo systemctl status housing-system
```

### Step 6: Configure Backups / تكوين النسخ الاحتياطية

```bash
# Make backup script executable
chmod +x scripts/backup_database.sh

# Add to crontab
crontab -e
# Add: 0 2 * * * /var/www/housing-system/scripts/backup_database.sh

# Test backup
./scripts/backup_database.sh
```

### Step 7: Security Hardening / تقوية الأمان

```bash
# Run security tests
./scripts/security_tests.sh

# Set file permissions
chmod 600 .env*
chmod 755 scripts/*.sh
chmod 644 *.py

# Configure firewall
sudo ufw enable
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw allow 22/tcp
```

### Step 8: Final Verification / التحقق النهائي

```bash
# Test application
curl -I https://yourdomain.com

# Test SSL
openssl s_client -connect yourdomain.com:443

# Check logs
tail -f logs/app.log

# Verify backup
ls -lh backups/
```

---

## 📊 Post-Deployment Monitoring / المراقبة بعد النشر

### Daily Checks / الفحوصات اليومية
- [ ] Check application health endpoint
- [ ] Review error logs
- [ ] Monitor disk space
- [ ] Check backup completion

### Weekly Checks / الفحوصات الأسبوعية
- [ ] Review security logs
- [ ] Update system packages
- [ ] Test backup restoration
- [ ] Review user activity

### Monthly Checks / الفحوصات الشهرية
- [ ] Update application dependencies
- [ ] Review and rotate logs
- [ ] Security audit
- [ ] Performance review

---

## 🆘 Emergency Procedures / إجراءات الطوارئ

### Database Corruption / تلف قاعدة البيانات
```bash
# Restore from latest backup
gunzip -c backups/latest_backup.db.gz > housing.db
sudo systemctl restart housing-system
```

### SSL Certificate Expiry / انتهاء صلاحية شهادة SSL
```bash
# Renew Let's Encrypt certificate
sudo certbot renew

# Reload Nginx
sudo systemctl reload nginx
```

### Service Failure / فشل الخدمة
```bash
# Check service status
sudo systemctl status housing-system

# View logs
sudo journalctl -u housing-system -n 100

# Restart service
sudo systemctl restart housing-system
```

---

## 📞 Support and Resources / الدعم والموارد

### Documentation / التوثيق
- `docs/deployment/PRODUCTION_DEPLOYMENT_GUIDE.md`
- `docs/deployment/NGINX_SSL_CONFIG.md`
- `docs/SECURITY.md`
- `docs/USER_SECURITY_TRAINING.md`

### Scripts / السكريبتات
- `scripts/backup_database.sh` - Automated backup
- `scripts/security_tests.sh` - Security testing
- `scripts/migrate_to_postgresql.py` - PostgreSQL migration
- `scripts/migrate_to_mysql.py` - MySQL migration

### External Resources / موارد خارجية
- [OWASP Security Guidelines](https://owasp.org/)
- [Flask Security Best Practices](https://flask.palletsprojects.com/en/latest/security/)
- [Gunicorn Documentation](https://docs.gunicorn.org/)
- [Nginx Documentation](https://nginx.org/en/docs/)
- [Let's Encrypt](https://letsencrypt.org/)

---

**Last Updated:** December 2025
**Version:** 2.0
