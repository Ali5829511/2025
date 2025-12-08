# Quick Production Setup Guide
# دليل الإعداد السريع للإنتاج

## 🚀 5-Minute Production Setup

This guide provides the fastest path to a production-ready deployment.

يوفر هذا الدليل أسرع طريقة للنشر الجاهز للإنتاج.

---

## Prerequisites / المتطلبات

- Ubuntu/Debian Linux server with root access
- Domain name pointed to your server
- Minimum 2GB RAM, 20GB disk space
- Python 3.8+ installed

---

## Step 1: Install Dependencies (2 minutes)

```bash
# Update system
sudo apt-get update && sudo apt-get upgrade -y

# Install required packages
sudo apt-get install -y python3-pip python3-venv nginx certbot python3-certbot-nginx postgresql postgresql-contrib git

# Install UFW firewall
sudo apt-get install -y ufw
```

---

## Step 2: Clone and Setup Application (1 minute)

```bash
# Clone repository
cd /var/www
sudo git clone https://github.com/Ali5829511/2025.git housing-system
cd housing-system

# Create virtual environment
sudo python3 -m venv venv
sudo venv/bin/pip install --upgrade pip
sudo venv/bin/pip install -r requirements.txt

# Set permissions
sudo chown -R www-data:www-data /var/www/housing-system
```

---

## Step 3: Configure Environment (30 seconds)

```bash
# Create production environment file
sudo cp .env.example .env

# Generate strong SECRET_KEY
python3 -c "import secrets; print('SECRET_KEY=' + secrets.token_hex(32))" | sudo tee -a .env

# Edit environment file
sudo nano .env

# Set these values:
# FLASK_ENV=production
# FLASK_DEBUG=False
# DATABASE_URL=postgresql://housing_user:STRONG_PASSWORD@localhost/housing_db
```

---

## Step 4: Setup PostgreSQL (1 minute)

```bash
# Create database and user
sudo -u postgres psql << EOF
CREATE DATABASE housing_db;
CREATE USER housing_user WITH ENCRYPTED PASSWORD 'YOUR_STRONG_PASSWORD_HERE';
GRANT ALL PRIVILEGES ON DATABASE housing_db TO housing_user;
\q
EOF

# Initialize database
cd /var/www/housing-system
sudo -u www-data venv/bin/python3 init_db.py

# Or migrate from existing SQLite
# sudo -u www-data venv/bin/python3 scripts/migrate_to_postgresql.py
```

---

## Step 5: Configure SSL with Let's Encrypt (30 seconds)

```bash
# Obtain SSL certificate
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com

# Auto-renewal is configured automatically by certbot
```

---

## Step 6: Configure Nginx (30 seconds)

```bash
# Copy configuration (update paths and domain first)
sudo cp docs/deployment/nginx-housing.conf /etc/nginx/sites-available/housing-system

# Edit configuration
sudo nano /etc/nginx/sites-available/housing-system
# Replace:
#   - yourdomain.com with your actual domain
#   - /var/www/housing-system with /var/www/housing-system

# Enable site
sudo ln -s /etc/nginx/sites-available/housing-system /etc/nginx/sites-enabled/
sudo rm /etc/nginx/sites-enabled/default

# Test and reload
sudo nginx -t && sudo systemctl reload nginx
```

---

## Step 7: Setup Systemd Service (30 seconds)

```bash
# Create service file
sudo tee /etc/systemd/system/housing-system.service > /dev/null << 'EOF'
[Unit]
Description=Housing Management System
After=network.target postgresql.service

[Service]
Type=notify
User=www-data
Group=www-data
WorkingDirectory=/var/www/housing-system
Environment="PATH=/var/www/housing-system/venv/bin"
EnvironmentFile=/var/www/housing-system/.env
ExecStart=/var/www/housing-system/venv/bin/gunicorn --config gunicorn_config.py server:app
ExecReload=/bin/kill -s HUP $MAINPID
KillMode=mixed
TimeoutStopSec=5
PrivateTmp=true
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

# Enable and start service
sudo systemctl daemon-reload
sudo systemctl enable housing-system
sudo systemctl start housing-system

# Check status
sudo systemctl status housing-system
```

---

## Step 8: Configure Firewall (30 seconds)

```bash
# Configure UFW firewall
sudo ufw allow 22/tcp    # SSH
sudo ufw allow 80/tcp    # HTTP
sudo ufw allow 443/tcp   # HTTPS
sudo ufw --force enable

# Verify
sudo ufw status
```

---

## Step 9: Setup Automated Backups (30 seconds)

```bash
# Make backup script executable
sudo chmod +x /var/www/housing-system/scripts/backup_database.sh

# Configure environment for backups
echo "DATABASE_URL=postgresql://housing_user:PASSWORD@localhost/housing_db" | sudo tee -a /etc/environment

# Add daily backup cron job
echo "0 2 * * * www-data /var/www/housing-system/scripts/backup_database.sh" | sudo tee -a /etc/crontab

# Create backups directory
sudo mkdir -p /var/www/housing-system/backups
sudo chown www-data:www-data /var/www/housing-system/backups
```

---

## Step 10: Final Verification (30 seconds)

```bash
# Test application
curl -I https://yourdomain.com

# Check SSL
curl https://yourdomain.com/api/health

# Test login page
curl https://yourdomain.com/

# Check logs
sudo journalctl -u housing-system -n 50

# Run security tests
cd /var/www/housing-system
sudo -u www-data ./scripts/security_tests.sh
```

---

## ✅ Production Checklist

After setup, verify these items:

### Immediate Actions
- [ ] Change default admin password on first login
- [ ] Verify SSL certificate is working (https://yourdomain.com)
- [ ] Test database connectivity
- [ ] Verify backup script runs successfully
- [ ] Check all services are running

### Within 24 Hours
- [ ] Change all default user passwords
- [ ] Review and configure monitoring
- [ ] Set up log rotation
- [ ] Test backup restoration
- [ ] Configure email notifications (optional)

### Within 1 Week
- [ ] Conduct security audit
- [ ] Train users on security practices
- [ ] Document custom configurations
- [ ] Set up additional monitoring/alerts
- [ ] Review access logs

---

## 🔧 Quick Commands Reference

### Service Management
```bash
# Start service
sudo systemctl start housing-system

# Stop service
sudo systemctl stop housing-system

# Restart service
sudo systemctl restart housing-system

# View logs
sudo journalctl -u housing-system -f

# Check status
sudo systemctl status housing-system
```

### Nginx Management
```bash
# Test configuration
sudo nginx -t

# Reload (graceful)
sudo systemctl reload nginx

# Restart
sudo systemctl restart nginx

# View logs
sudo tail -f /var/log/nginx/housing-error.log
```

### Database Management
```bash
# Connect to database
sudo -u postgres psql housing_db

# Backup database manually
/var/www/housing-system/scripts/backup_database.sh

# Check database size
sudo -u postgres psql -c "SELECT pg_size_pretty(pg_database_size('housing_db'));"
```

### SSL Certificate Management
```bash
# Renew certificates
sudo certbot renew

# Check certificate expiry
sudo certbot certificates

# Test auto-renewal
sudo certbot renew --dry-run
```

---

## 🆘 Troubleshooting

### Service Won't Start
```bash
# Check logs
sudo journalctl -u housing-system -n 100

# Check if port is in use
sudo netstat -tulpn | grep 5000

# Verify Python environment
cd /var/www/housing-system
sudo -u www-data venv/bin/python3 -c "import flask; print(flask.__version__)"
```

### Database Connection Issues
```bash
# Check PostgreSQL is running
sudo systemctl status postgresql

# Test connection
sudo -u postgres psql -c "\conninfo"

# Check permissions
sudo -u postgres psql -c "\du"
```

### SSL Certificate Issues
```bash
# Check certificate files
sudo ls -la /etc/letsencrypt/live/yourdomain.com/

# Test SSL connection
openssl s_client -connect yourdomain.com:443 -servername yourdomain.com

# Regenerate certificate
sudo certbot --force-renewal -d yourdomain.com
```

### 502 Bad Gateway
```bash
# Check if Gunicorn is running
sudo systemctl status housing-system

# Check Nginx configuration
sudo nginx -t

# Verify port 5000 is listening
sudo netstat -tulpn | grep 5000

# Check application logs
sudo journalctl -u housing-system -n 50
```

---

## 📊 Monitoring Commands

### System Resources
```bash
# Check disk space
df -h

# Check memory usage
free -h

# Check CPU usage
top -bn1 | head -20

# Check service memory
sudo systemctl status housing-system | grep Memory
```

### Application Health
```bash
# Health check endpoint
curl https://yourdomain.com/api/health

# Check response time
time curl -I https://yourdomain.com

# Monitor access in real-time
sudo tail -f /var/log/nginx/housing-access.log
```

### Database Health
```bash
# Check active connections
sudo -u postgres psql housing_db -c "SELECT count(*) FROM pg_stat_activity;"

# Check database size
sudo -u postgres psql -c "SELECT pg_size_pretty(pg_database_size('housing_db'));"

# Check slow queries
sudo -u postgres psql housing_db -c "SELECT query, calls, total_time FROM pg_stat_statements ORDER BY total_time DESC LIMIT 10;"
```

---

## 🔒 Security Hardening (Optional but Recommended)

### Fail2ban Setup
```bash
# Install Fail2ban
sudo apt-get install fail2ban

# Create housing-specific jail
sudo tee /etc/fail2ban/jail.d/housing.conf > /dev/null << 'EOF'
[nginx-housing]
enabled = true
port = http,https
filter = nginx-housing
logpath = /var/log/nginx/housing-access.log
maxretry = 5
bantime = 3600
EOF

# Restart Fail2ban
sudo systemctl restart fail2ban
```

### Additional PostgreSQL Security
```bash
# Edit PostgreSQL configuration
sudo nano /etc/postgresql/*/main/pg_hba.conf

# Change peer authentication to md5 for local connections
# local   all             all                                     md5

# Restart PostgreSQL
sudo systemctl restart postgresql
```

### Rate Limiting with Nginx
Already configured in the Nginx configuration file. To adjust:
```bash
sudo nano /etc/nginx/sites-available/housing-system
# Modify limit_req_zone directives
sudo nginx -t && sudo systemctl reload nginx
```

---

## 📝 Important Notes

1. **Passwords**: All default passwords must be changed on first login
2. **SSL Certificates**: Let's Encrypt certificates auto-renew
3. **Backups**: Daily at 2 AM, retained for 30 days
4. **Logs**: Rotated automatically by logrotate
5. **Updates**: Check for updates monthly
6. **Security**: Run security tests quarterly

---

## 📞 Support Resources

- Full Documentation: `/var/www/housing-system/docs/`
- Production Checklist: `docs/deployment/PRODUCTION_CHECKLIST.md`
- Nginx SSL Config: `docs/deployment/NGINX_SSL_CONFIG.md`
- Security Guide: `docs/SECURITY.md`
- User Training: `docs/USER_SECURITY_TRAINING.md`

---

## 🎯 Post-Deployment

After successful deployment:

1. ✅ Test all functionality at https://yourdomain.com
2. ✅ Verify SSL certificate (A+ rating at ssllabs.com)
3. ✅ Force password changes for all users
4. ✅ Set up monitoring and alerts
5. ✅ Schedule regular security audits
6. ✅ Document any custom changes
7. ✅ Train users on the system

---

**Deployment Time: ~5-10 minutes**
**Total Setup Time: ~30 minutes including verification**

**Last Updated:** December 2025
