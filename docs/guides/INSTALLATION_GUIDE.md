# دليل التثبيت الكامل - نظام المخالفات المرورية
# Complete Installation Guide - Traffic Violations System

<div dir="rtl">

## 📋 المتطلبات الأساسية

- Python 3.8 أو أحدث
- pip (مدير حزم Python)
- (اختياري) Docker و Docker Compose
- (اختياري) Nginx لعكس الوكيل
- (اختياري) systemd لإدارة الخدمة

</div>

---

## 🚀 التثبيت السريع (Quick Install)

### Option 1: Using Make (Recommended)

```bash
# Install and setup
make -f Makefile.traffic setup

# Start server
make -f Makefile.traffic run
```

### Option 2: Using Start Script

```bash
chmod +x start_traffic.sh
./start_traffic.sh
```

### Option 3: Manual Installation

```bash
# 1. Install dependencies
pip install flask flask-cors python-dotenv requests pillow gunicorn

# 2. Initialize database
python3 init_traffic_db.py

# 3. Start server
PORT=10000 gunicorn --config gunicorn_traffic_config.py traffic_app:app
```

---

## 🐳 Docker Installation

### Using Docker Compose (Easiest)

```bash
# Start containers
docker-compose -f docker-compose.traffic-standalone.yml up -d

# View logs
docker-compose -f docker-compose.traffic-standalone.yml logs -f

# Stop containers
docker-compose -f docker-compose.traffic-standalone.yml down
```

### Using Docker Manually

```bash
# Build image
docker build -f Dockerfile.traffic -t traffic-system .

# Run container
docker run -d -p 10000:10000 \
  -e PORT=10000 \
  -e PLATE_RECOGNIZER_API_TOKEN=your_token \
  --name traffic-app \
  traffic-system

# View logs
docker logs -f traffic-app

# Stop container
docker stop traffic-app
```

---

## 🌐 Production Deployment

### 1. System Service (systemd)

```bash
# Copy service file
sudo cp traffic-system.service /etc/systemd/system/

# Edit paths and user in service file
sudo nano /etc/systemd/system/traffic-system.service

# Enable and start service
sudo systemctl enable traffic-system
sudo systemctl start traffic-system

# Check status
sudo systemctl status traffic-system

# View logs
sudo journalctl -u traffic-system -f
```

### 2. Nginx Reverse Proxy

```bash
# Copy nginx configuration
sudo cp nginx.traffic.conf /etc/nginx/sites-available/traffic

# Edit domain name
sudo nano /etc/nginx/sites-available/traffic

# Enable site
sudo ln -s /etc/nginx/sites-available/traffic /etc/nginx/sites-enabled/

# Test configuration
sudo nginx -t

# Reload nginx
sudo systemctl reload nginx
```

### 3. SSL with Let's Encrypt

```bash
# Install certbot
sudo apt-get install certbot python3-certbot-nginx

# Obtain certificate
sudo certbot --nginx -d traffic.example.com

# Auto-renewal is configured automatically
```

---

## ☁️ Cloud Platform Deployment

### Render.com

1. Push code to GitHub
2. Connect repository to Render
3. Use `render.traffic.yaml` for configuration
4. Set environment variables in Render dashboard
5. Deploy!

```bash
# Or use Render CLI
render deploy
```

### Heroku

```bash
# Login to Heroku
heroku login

# Create app
heroku create my-traffic-app

# Set environment variables
heroku config:set PORT=10000
heroku config:set PLATE_RECOGNIZER_API_TOKEN=your_token

# Deploy
git push heroku main
```

### Railway

```bash
# Install Railway CLI
npm install -g @railway/cli

# Login
railway login

# Initialize project
railway init

# Deploy
railway up
```

### DigitalOcean App Platform

1. Connect GitHub repository
2. Select `Dockerfile.traffic` for build
3. Set environment variables
4. Deploy!

---

## 🔧 Configuration

### Environment Variables

Create `.env.traffic` or set system environment variables:

```bash
# Required
PORT=10000

# Optional
FLASK_DEBUG=false
FLASK_ENV=production
PLATE_RECOGNIZER_API_TOKEN=your_token_here
GUNICORN_WORKERS=4
GUNICORN_TIMEOUT=120
```

### Application Configuration

Edit `gunicorn_traffic_config.py` for advanced settings:

```python
# Number of workers
workers = 4

# Timeout
timeout = 120

# Binding
bind = "0.0.0.0:10000"
```

---

## 🧪 Testing

### Manual Test

```bash
# Start server
make -f Makefile.traffic run

# In another terminal
curl http://localhost:10000/health
```

### Automated Test

```bash
# Run test suite
make -f Makefile.traffic test

# Or directly
python3 test_traffic_health.py http://localhost:10000
```

### Load Testing (Optional)

```bash
# Install Apache Bench
sudo apt-get install apache2-utils

# Test 1000 requests with 10 concurrent
ab -n 1000 -c 10 http://localhost:10000/health
```

---

## 📊 Monitoring

### Health Check

```bash
# Quick check
make -f Makefile.traffic health

# Continuous monitoring
make -f Makefile.traffic monitor
```

### Logs

```bash
# With systemd
sudo journalctl -u traffic-system -f

# With Docker
docker logs -f traffic-app

# With Gunicorn (direct)
tail -f /var/log/traffic-app/*.log
```

### Metrics (Optional)

Install Prometheus and Grafana for advanced monitoring:

```bash
# Add to requirements.txt
prometheus-flask-exporter

# Configure in traffic_app.py
from prometheus_flask_exporter import PrometheusMetrics
metrics = PrometheusMetrics(app)
```

---

## 🔒 Security Checklist

- [ ] Change default ports if needed
- [ ] Set strong SECRET_KEY
- [ ] Enable HTTPS with valid certificate
- [ ] Configure firewall (ufw/iptables)
- [ ] Regular security updates
- [ ] Backup database regularly
- [ ] Use environment variables for secrets
- [ ] Enable CORS only for trusted domains
- [ ] Implement rate limiting
- [ ] Monitor for suspicious activity

---

## 🔄 Maintenance

### Backup Database

```bash
# Manual backup
cp traffic.db traffic_backup_$(date +%Y%m%d).db

# Automated backup (cron)
0 2 * * * cp /opt/traffic-system/traffic.db /backup/traffic_$(date +\%Y\%m\%d).db
```

### Update System

```bash
# Pull latest code
git pull origin main

# Install new dependencies
pip install -r requirements.txt

# Restart service
sudo systemctl restart traffic-system
```

### Database Migration

```bash
# Backup first!
cp traffic.db traffic_backup.db

# Run migration script
python3 migrate_database.py

# Verify
python3 verify_database.py
```

---

## 🐛 Troubleshooting

### Server Won't Start

```bash
# Check Python version
python3 --version

# Check dependencies
pip list | grep -E 'flask|gunicorn'

# Check database
ls -la traffic.db

# Check logs
tail -f *.log
```

### Port Already in Use

```bash
# Find process
sudo lsof -i :10000

# Kill process
sudo kill -9 <PID>
```

### Database Locked

```bash
# Check for running processes
ps aux | grep traffic

# Stop all instances
pkill -f traffic_app

# Remove lock
rm -f traffic.db-journal
```

### Permission Denied

```bash
# Fix ownership
sudo chown -R $USER:$USER .

# Fix permissions
chmod +x start_traffic.sh
chmod 644 traffic.db
```

---

## 📚 Additional Resources

- [TRAFFIC_README.md](TRAFFIC_README.md) - System documentation
- [TRAFFIC_DEPLOYMENT_FIX.md](TRAFFIC_DEPLOYMENT_FIX.md) - Deployment fix details
- [TRAFFIC_FIX_ARABIC.md](TRAFFIC_FIX_ARABIC.md) - Arabic summary
- [.env.traffic](.env.traffic) - Environment variables template

---

## 💡 Tips

1. **Use Makefile** - Simplifies common tasks
2. **Monitor Health** - Regular health checks prevent issues
3. **Backup Regularly** - Automated daily backups recommended
4. **Use Docker** - Easier deployment and updates
5. **Enable HTTPS** - Essential for production
6. **Set Resource Limits** - Prevent resource exhaustion
7. **Log Rotation** - Prevent disk space issues
8. **Test Before Deploy** - Always test in staging first

---

## 🆘 Support

For help:

1. Check [Troubleshooting](#-troubleshooting) section
2. Review logs: `sudo journalctl -u traffic-system -n 100`
3. Test health: `curl http://localhost:10000/health`
4. Check system status: `make -f Makefile.traffic check`

---

**Installation Guide Version**: 1.0.0  
**Last Updated**: 2025-11-11  
**Status**: ✅ Production Ready
