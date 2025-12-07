# Nginx SSL/HTTPS Configuration Guide
# دليل تكوين Nginx لـ SSL/HTTPS

## Overview / نظرة عامة

This guide provides complete Nginx configuration for serving the Housing Management System over HTTPS with SSL/TLS encryption.

يوفر هذا الدليل تكوين Nginx الكامل لخدمة نظام إدارة الإسكان عبر HTTPS مع تشفير SSL/TLS.

---

## Prerequisites / المتطلبات الأساسية

- Nginx installed / Nginx مثبت
- SSL certificate obtained / شهادة SSL محصل عليها
- Domain name configured / اسم النطاق مكون
- Application running on port 5000 (Gunicorn) / التطبيق يعمل على المنفذ 5000

---

## Configuration Files / ملفات التكوين

### 1. Main Nginx Configuration with SSL / تكوين Nginx الرئيسي مع SSL

Create file: `/etc/nginx/sites-available/housing-system`

```nginx
# ==============================================================================
# Housing Management System - Nginx SSL Configuration
# نظام إدارة الإسكان - تكوين Nginx لـ SSL
# ==============================================================================

# Rate limiting zones / مناطق تحديد المعدل
limit_req_zone $binary_remote_addr zone=login_limit:10m rate=5r/m;
limit_req_zone $binary_remote_addr zone=api_limit:10m rate=30r/m;
limit_req_zone $binary_remote_addr zone=general_limit:10m rate=100r/m;

# Upstream application server / خادم التطبيق الأعلى
upstream housing_app {
    server 127.0.0.1:5000 fail_timeout=10s max_fails=3;
    # For multiple workers, add more servers:
    # server 127.0.0.1:5001 fail_timeout=10s max_fails=3;
    # server 127.0.0.1:5002 fail_timeout=10s max_fails=3;
    keepalive 32;
}

# Traffic system upstream (if needed)
upstream traffic_app {
    server 127.0.0.1:5001 fail_timeout=10s max_fails=3;
    keepalive 16;
}

# ==============================================================================
# HTTP Server - Redirect to HTTPS
# خادم HTTP - إعادة التوجيه إلى HTTPS
# ==============================================================================
server {
    listen 80;
    listen [::]:80;
    server_name yourdomain.com www.yourdomain.com;
    
    # Let's Encrypt challenge location
    location /.well-known/acme-challenge/ {
        root /var/www/certbot;
        allow all;
    }
    
    # Redirect all other traffic to HTTPS
    location / {
        return 301 https://$server_name$request_uri;
    }
}

# ==============================================================================
# HTTPS Server - Main Application
# خادم HTTPS - التطبيق الرئيسي
# ==============================================================================
server {
    listen 443 ssl http2;
    listen [::]:443 ssl http2;
    server_name yourdomain.com www.yourdomain.com;
    
    # Root directory
    root /var/www/housing-system;
    
    # ==============================================================================
    # SSL/TLS Configuration
    # تكوين SSL/TLS
    # ==============================================================================
    
    # SSL Certificate and Key
    # شهادة SSL والمفتاح
    ssl_certificate /etc/letsencrypt/live/yourdomain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/yourdomain.com/privkey.pem;
    
    # Diffie-Hellman parameters for DHE cipher suites
    ssl_dhparam /etc/nginx/ssl/dhparam.pem;
    
    # SSL Protocols and Ciphers
    # بروتوكولات وأصفار SSL
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers 'ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384:ECDHE-ECDSA-CHACHA20-POLY1305:ECDHE-RSA-CHACHA20-POLY1305:DHE-RSA-AES128-GCM-SHA256:DHE-RSA-AES256-GCM-SHA384';
    ssl_prefer_server_ciphers on;
    
    # SSL Session Settings
    # إعدادات جلسة SSL
    ssl_session_cache shared:SSL:10m;
    ssl_session_timeout 10m;
    ssl_session_tickets off;
    
    # OCSP Stapling
    ssl_stapling on;
    ssl_stapling_verify on;
    ssl_trusted_certificate /etc/letsencrypt/live/yourdomain.com/chain.pem;
    resolver 8.8.8.8 8.8.4.4 valid=300s;
    resolver_timeout 5s;
    
    # ==============================================================================
    # Security Headers
    # ترويسات الأمان
    # ==============================================================================
    
    # HSTS (HTTP Strict Transport Security)
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains; preload" always;
    
    # Prevent clickjacking
    add_header X-Frame-Options "SAMEORIGIN" always;
    
    # Prevent MIME type sniffing
    add_header X-Content-Type-Options "nosniff" always;
    
    # XSS Protection
    add_header X-XSS-Protection "1; mode=block" always;
    
    # Referrer Policy
    add_header Referrer-Policy "strict-origin-when-cross-origin" always;
    
    # Permissions Policy
    add_header Permissions-Policy "geolocation=(), microphone=(), camera=()" always;
    
    # Content Security Policy
    # Note: 'unsafe-inline' and 'unsafe-eval' are used for compatibility with existing inline scripts
    # For enhanced security in production, consider:
    # 1. Moving inline scripts to external files
    # 2. Using CSP nonces for necessary inline scripts
    # 3. Removing 'unsafe-eval' if not required by dependencies
    add_header Content-Security-Policy "default-src 'self'; script-src 'self' 'unsafe-inline' 'unsafe-eval'; style-src 'self' 'unsafe-inline'; img-src 'self' data: https:; font-src 'self' data:; connect-src 'self'; frame-ancestors 'self';" always;
    
    # ==============================================================================
    # Logging
    # السجلات
    # ==============================================================================
    
    access_log /var/log/nginx/housing-access.log;
    error_log /var/log/nginx/housing-error.log warn;
    
    # ==============================================================================
    # Compression
    # الضغط
    # ==============================================================================
    
    gzip on;
    gzip_vary on;
    gzip_proxied any;
    gzip_comp_level 6;
    gzip_types text/plain text/css text/xml text/javascript application/json application/javascript application/xml+rss application/rss+xml font/truetype font/opentype application/vnd.ms-fontobject image/svg+xml;
    gzip_disable "msie6";
    
    # ==============================================================================
    # Client Settings
    # إعدادات العميل
    # ==============================================================================
    
    client_max_body_size 50M;
    client_body_buffer_size 128k;
    client_header_timeout 60s;
    client_body_timeout 60s;
    
    # ==============================================================================
    # Static Files
    # الملفات الثابتة
    # ==============================================================================
    
    # Static files with long cache
    location ~* \.(jpg|jpeg|png|gif|ico|css|js|svg|woff|woff2|ttf|eot)$ {
        expires 1y;
        add_header Cache-Control "public, immutable";
        access_log off;
        
        # Try files from static directory first
        try_files $uri @app;
    }
    
    # Static directory
    location /static/ {
        alias /var/www/housing-system/static/;
        expires 1y;
        add_header Cache-Control "public, immutable";
        access_log off;
    }
    
    # Uploads directory
    location /uploads/ {
        alias /var/www/housing-system/uploads/;
        expires 30d;
        add_header Cache-Control "public";
    }
    
    # ==============================================================================
    # API Routes with Rate Limiting
    # مسارات API مع تحديد المعدل
    # ==============================================================================
    
    # Login endpoint - strict rate limit
    location /api/auth/login {
        limit_req zone=login_limit burst=3 nodelay;
        limit_req_status 429;
        
        proxy_pass http://housing_app;
        include /etc/nginx/proxy_params;
    }
    
    # API endpoints - moderate rate limit
    location /api/ {
        limit_req zone=api_limit burst=10 nodelay;
        limit_req_status 429;
        
        proxy_pass http://housing_app;
        include /etc/nginx/proxy_params;
    }
    
    # ==============================================================================
    # Application Proxy
    # وكيل التطبيق
    # ==============================================================================
    
    location / {
        limit_req zone=general_limit burst=20 nodelay;
        
        # Try static files first, then proxy to app
        try_files $uri @app;
    }
    
    location @app {
        proxy_pass http://housing_app;
        include /etc/nginx/proxy_params;
    }
    
    # ==============================================================================
    # Health Check Endpoint
    # نقطة فحص الصحة
    # ==============================================================================
    
    location /api/health {
        access_log off;
        proxy_pass http://housing_app;
        proxy_http_version 1.1;
        proxy_set_header Connection "";
        proxy_connect_timeout 5s;
        proxy_send_timeout 5s;
        proxy_read_timeout 5s;
    }
    
    # ==============================================================================
    # Traffic System (Optional Subdomain/Path)
    # نظام المرور (نطاق فرعي/مسار اختياري)
    # ==============================================================================
    
    # Option 1: Subdomain
    # location / {
    #     proxy_pass http://traffic_app;
    #     include /etc/nginx/proxy_params;
    # }
    
    # Option 2: Path-based
    location /traffic/ {
        proxy_pass http://traffic_app/;
        include /etc/nginx/proxy_params;
    }
    
    # ==============================================================================
    # Security: Block sensitive files
    # الأمان: حظر الملفات الحساسة
    # ==============================================================================
    
    # Deny access to hidden files
    location ~ /\. {
        deny all;
        access_log off;
        log_not_found off;
    }
    
    # Deny access to sensitive files
    location ~* \.(env|git|gitignore|py|pyc|db|sql|log|conf)$ {
        deny all;
        access_log off;
        log_not_found off;
    }
    
    # ==============================================================================
    # Error Pages
    # صفحات الأخطاء
    # ==============================================================================
    
    error_page 404 /404.html;
    error_page 500 502 503 504 /50x.html;
    
    location = /404.html {
        internal;
        root /usr/share/nginx/html;
    }
    
    location = /50x.html {
        internal;
        root /usr/share/nginx/html;
    }
}
```

### 2. Proxy Parameters File / ملف معاملات الوكيل

Create file: `/etc/nginx/proxy_params`

```nginx
# ==============================================================================
# Proxy Parameters for Application
# معاملات الوكيل للتطبيق
# ==============================================================================

proxy_http_version 1.1;

# Connection settings
proxy_set_header Connection "";
proxy_set_header Upgrade $http_upgrade;
proxy_set_header Connection "upgrade";

# Forward client information
proxy_set_header Host $host;
proxy_set_header X-Real-IP $remote_addr;
proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
proxy_set_header X-Forwarded-Proto $scheme;
proxy_set_header X-Forwarded-Host $host;
proxy_set_header X-Forwarded-Port $server_port;

# Timeouts
proxy_connect_timeout 60s;
proxy_send_timeout 60s;
proxy_read_timeout 60s;

# Buffering
proxy_buffering on;
proxy_buffer_size 4k;
proxy_buffers 8 4k;
proxy_busy_buffers_size 8k;

# Error handling
proxy_next_upstream error timeout invalid_header http_500 http_502 http_503 http_504;
proxy_next_upstream_tries 2;
```

---

## SSL Certificate Setup / إعداد شهادة SSL

### Option 1: Let's Encrypt (Free) - خيار 1: Let's Encrypt (مجاني)

#### Install Certbot / تثبيت Certbot

```bash
# Ubuntu/Debian
sudo apt-get update
sudo apt-get install certbot python3-certbot-nginx

# CentOS/RHEL
sudo yum install certbot python3-certbot-nginx

# Fedora
sudo dnf install certbot python3-certbot-nginx
```

#### Obtain Certificate / الحصول على الشهادة

```bash
# Stop Nginx temporarily
sudo systemctl stop nginx

# Obtain certificate
sudo certbot certonly --standalone -d yourdomain.com -d www.yourdomain.com

# Or with Nginx plugin (if Nginx is running)
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com

# Start Nginx
sudo systemctl start nginx
```

#### Generate DH Parameters / إنشاء معاملات DH

```bash
# Generate strong DH parameters (takes several minutes)
sudo mkdir -p /etc/nginx/ssl
sudo openssl dhparam -out /etc/nginx/ssl/dhparam.pem 2048
```

#### Auto-renewal / التجديد التلقائي

```bash
# Test renewal
sudo certbot renew --dry-run

# Certbot adds auto-renewal to cron or systemd timer automatically
# Check with:
sudo systemctl list-timers | grep certbot
```

### Option 2: Self-Signed Certificate (Testing Only) - خيار 2: شهادة موقعة ذاتياً (للاختبار فقط)

```bash
# Generate self-signed certificate
sudo mkdir -p /etc/nginx/ssl
sudo openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
  -keyout /etc/nginx/ssl/housing-selfsigned.key \
  -out /etc/nginx/ssl/housing-selfsigned.crt

# Update nginx configuration to use these files
# ssl_certificate /etc/nginx/ssl/housing-selfsigned.crt;
# ssl_certificate_key /etc/nginx/ssl/housing-selfsigned.key;
```

### Option 3: Commercial Certificate - خيار 3: شهادة تجارية

1. Generate CSR (Certificate Signing Request):
```bash
sudo openssl req -new -newkey rsa:2048 -nodes \
  -keyout /etc/nginx/ssl/yourdomain.com.key \
  -out /etc/nginx/ssl/yourdomain.com.csr
```

2. Submit CSR to certificate authority (DigiCert, GlobalSign, etc.)
3. Download certificate files
4. Install certificate:
```bash
sudo cp fullchain.crt /etc/nginx/ssl/yourdomain.com.crt
sudo cp yourdomain.com.key /etc/nginx/ssl/
sudo chmod 600 /etc/nginx/ssl/*.key
```

---

## Installation Steps / خطوات التثبيت

### 1. Copy Configuration / نسخ التكوين

```bash
# Copy main configuration
sudo cp nginx-housing.conf /etc/nginx/sites-available/housing-system

# Copy proxy parameters
sudo cp proxy_params /etc/nginx/

# Update paths in configuration
sudo nano /etc/nginx/sites-available/housing-system
# Change:
# - yourdomain.com to your actual domain
# - /var/www/housing-system to your application path
# - SSL certificate paths if different
```

### 2. Enable Site / تفعيل الموقع

```bash
# Create symbolic link
sudo ln -s /etc/nginx/sites-available/housing-system /etc/nginx/sites-enabled/

# Remove default site (optional)
sudo rm /etc/nginx/sites-enabled/default
```

### 3. Test Configuration / اختبار التكوين

```bash
# Test Nginx configuration
sudo nginx -t

# If test passes, reload Nginx
sudo systemctl reload nginx
```

### 4. Verify SSL / التحقق من SSL

```bash
# Test locally
curl -I https://yourdomain.com

# Check SSL with OpenSSL
openssl s_client -connect yourdomain.com:443 -servername yourdomain.com

# Online SSL test
# Visit: https://www.ssllabs.com/ssltest/analyze.html?d=yourdomain.com
```

---

## Firewall Configuration / تكوين جدار الحماية

```bash
# Ubuntu/Debian (UFW)
sudo ufw allow 'Nginx Full'
sudo ufw allow 22/tcp
sudo ufw enable

# CentOS/RHEL (firewalld)
sudo firewall-cmd --permanent --add-service=http
sudo firewall-cmd --permanent --add-service=https
sudo firewall-cmd --permanent --add-service=ssh
sudo firewall-cmd --reload
```

---

## Monitoring and Maintenance / المراقبة والصيانة

### Check Nginx Status / فحص حالة Nginx

```bash
# Service status
sudo systemctl status nginx

# Check logs
sudo tail -f /var/log/nginx/housing-access.log
sudo tail -f /var/log/nginx/housing-error.log

# Check connections
sudo netstat -tulpn | grep nginx
```

### Certificate Renewal / تجديد الشهادة

```bash
# Check certificate expiry
sudo certbot certificates

# Renew certificates
sudo certbot renew

# Reload Nginx after renewal
sudo systemctl reload nginx
```

### Log Rotation / دوران السجلات

Create file: `/etc/logrotate.d/housing-nginx`

```
/var/log/nginx/housing-*.log {
    daily
    rotate 14
    compress
    delaycompress
    notifempty
    missingok
    sharedscripts
    postrotate
        [ -f /var/run/nginx.pid ] && kill -USR1 `cat /var/run/nginx.pid`
    endscript
}
```

---

## Troubleshooting / استكشاف الأخطاء

### Common Issues / المشاكل الشائعة

#### 1. 502 Bad Gateway

```bash
# Check if application is running
sudo systemctl status housing-system

# Check Gunicorn logs
sudo journalctl -u housing-system -n 50

# Verify upstream connection
curl http://localhost:5000/api/health
```

#### 2. SSL Certificate Errors

```bash
# Verify certificate files exist
ls -l /etc/letsencrypt/live/yourdomain.com/

# Check certificate validity
openssl x509 -in /etc/letsencrypt/live/yourdomain.com/cert.pem -text -noout

# Regenerate certificate
sudo certbot --force-renewal -d yourdomain.com
```

#### 3. Rate Limiting Issues

```bash
# Check Nginx error log
sudo tail -f /var/log/nginx/housing-error.log

# Adjust rate limits in configuration if needed
# Reload Nginx after changes
sudo systemctl reload nginx
```

#### 4. Permission Denied

```bash
# Check Nginx user
ps aux | grep nginx

# Fix static file permissions
sudo chown -R www-data:www-data /var/www/housing-system/static
sudo chmod -R 755 /var/www/housing-system/static
```

---

## Performance Tuning / تحسين الأداء

### Nginx Worker Configuration / تكوين عمال Nginx

Add to `/etc/nginx/nginx.conf`:

```nginx
# Optimize for your server
worker_processes auto;
worker_rlimit_nofile 65535;

events {
    worker_connections 4096;
    use epoll;
    multi_accept on;
}
```

### Enable HTTP/2 Push / تفعيل HTTP/2 Push

```nginx
# In server block
http2_push_preload on;

# In location
location / {
    http2_push /static/css/main.css;
    http2_push /static/js/main.js;
    # ... rest of configuration
}
```

---

## Security Best Practices / أفضل ممارسات الأمان

1. **Keep Nginx Updated** / حافظ على تحديث Nginx
   ```bash
   sudo apt-get update && sudo apt-get upgrade nginx
   ```

2. **Regular SSL Certificate Renewal** / تجديد شهادة SSL بانتظام
   - Let's Encrypt certificates expire every 90 days
   - Auto-renewal should be configured

3. **Monitor Access Logs** / مراقبة سجلات الوصول
   ```bash
   # Watch for suspicious activity
   sudo tail -f /var/log/nginx/housing-access.log | grep -E "404|500|POST"
   ```

4. **Implement Fail2ban** / تنفيذ Fail2ban
   ```bash
   sudo apt-get install fail2ban
   # Configure to ban IPs with repeated failed login attempts
   ```

5. **Regular Backups** / النسخ الاحتياطية المنتظمة
   - Backup Nginx configuration: `/etc/nginx/`
   - Backup SSL certificates: `/etc/letsencrypt/`

---

## Additional Resources / موارد إضافية

- [Nginx Official Documentation](https://nginx.org/en/docs/)
- [Let's Encrypt Documentation](https://letsencrypt.org/docs/)
- [Mozilla SSL Configuration Generator](https://ssl-config.mozilla.org/)
- [SSL Labs SSL Test](https://www.ssllabs.com/ssltest/)
- [SecurityHeaders.com](https://securityheaders.com/)

---

**Last Updated:** December 2025
**Version:** 1.0
