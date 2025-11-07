# نظام إدارة إسكان أعضاء هيئة التدريس
# Faculty Housing Management System

[![Docker Pulls](https://img.shields.io/docker/pulls/ali517/housing-management)](https://hub.docker.com/r/ali517/housing-management)
[![Docker Image Size](https://img.shields.io/docker/image-size/ali517/housing-management/latest)](https://hub.docker.com/r/ali517/housing-management)
[![Version](https://img.shields.io/badge/Version-2.0.1-blue)](https://github.com/Ali5829511/2025)

نظام شامل لإدارة إسكان أعضاء هيئة التدريس في جامعة الإمام محمد بن سعود الإسلامية.

A comprehensive system for managing faculty housing at Imam Mohammad Ibn Saud Islamic University.

---

## 🚀 Quick Start / البدء السريع

### استخدام Docker Compose (موصى به) / Using Docker Compose (Recommended)

```bash
# إنشاء ملف docker-compose.yml / Create docker-compose.yml
curl -O https://raw.githubusercontent.com/Ali5829511/2025/main/docker-compose.yml

# تشغيل النظام / Start the system
docker-compose up -d

# الوصول للنظام / Access the system
# افتح المتصفح على / Open browser at: http://localhost
```

### استخدام Docker مباشرة / Using Docker Directly

```bash
# سحب الصورة / Pull the image
docker pull ali517/housing-management:latest

# تشغيل مع SQLite (للتجربة) / Run with SQLite (for testing)
docker run -d \
  --name housing-system \
  -p 8000:8000 \
  -e FLASK_ENV=production \
  -e FLASK_DEBUG=False \
  -v housing_data:/app/data \
  ali517/housing-management:latest
```

---

## 📋 المميزات / Features

- 🏢 **إدارة المباني والشقق** / Buildings and Apartments Management
- 👥 **إدارة السكان** / Residents Management  
- 🚗 **إدارة المواقف والملصقات** / Parking and Stickers Management
- 🚦 **إدارة المخالفات المرورية** / Traffic Violations Management
- 🚨 **إدارة الحوادث المرورية** / Traffic Accidents Management
- 🔒 **إدارة الأمن والوقائع الأمنية** / Security Incidents Management
- 📝 **إدارة الشكاوى** / Complaints Management
- 👁️ **إدارة الزوار** / Visitors Management
- 📊 **تقارير شاملة وإحصائيات** / Comprehensive Reports and Statistics
- 👮 **صلاحيات متعددة المستويات** / Multi-level User Permissions
- 📷 **تمييز لوحات السيارات تلقائياً** / Automatic License Plate Recognition

---

## 🏷️ العلامات المتاحة / Available Tags

| Tag | Description | الوصف |
|-----|-------------|--------|
| `latest` | آخر إصدار مستقر / Latest stable release | للإنتاج |
| `stable` | إصدار مستقر / Stable release | للإنتاج |
| `v2.0.1` | إصدار محدد / Specific version | للإنتاج |
| `v2.0` | إصدار رئيسي / Major version | للإنتاج |
| `dev` | إصدار تطويري / Development version | للتطوير |

---

## ⚙️ متغيرات البيئة / Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `FLASK_ENV` | بيئة Flask / Flask environment | `production` |
| `FLASK_DEBUG` | وضع التصحيح / Debug mode | `False` |
| `DATABASE_TYPE` | نوع قاعدة البيانات / Database type | `sqlite` |
| `DATABASE_HOST` | عنوان قاعدة البيانات / Database host | `localhost` |
| `DATABASE_PORT` | منفذ قاعدة البيانات / Database port | `5432` |
| `DATABASE_NAME` | اسم قاعدة البيانات / Database name | `housing_db` |
| `DATABASE_USER` | مستخدم قاعدة البيانات / Database user | `housing_user` |
| `DATABASE_PASSWORD` | كلمة مرور قاعدة البيانات / Database password | - |
| `SECRET_KEY` | مفتاح سري للجلسات / Secret key for sessions | - |

---

## 🔐 بيانات الدخول الافتراضية / Default Login Credentials

| المستخدم / User | Username | Password | الصلاحيات / Permissions |
|-----------------|----------|----------|-------------------------|
| مدير النظام / Admin | `admin` | `Admin@2025` | كاملة / Full |
| مسؤول المخالفات / Violations | `violations_officer` | `Violations@2025` | محدودة / Limited |
| مسؤول الزوار / Visitors | `visitors_officer` | `Visitors@2025` | محدودة / Limited |
| مستخدم عرض / Viewer | `viewer` | `Viewer@2025` | عرض فقط / View only |

⚠️ **مهم:** غيّر هذه الكلمات فوراً بعد التثبيت!
⚠️ **Important:** Change these passwords immediately after installation!

---

## 📦 استخدام مع Docker Compose / Using with Docker Compose

### ملف docker-compose.yml كامل / Complete docker-compose.yml

```yaml
version: '3.8'

services:
  db:
    image: postgres:14-alpine
    container_name: housing_db
    restart: always
    environment:
      POSTGRES_DB: housing_db
      POSTGRES_USER: housing_user
      POSTGRES_PASSWORD: ${DB_PASSWORD:-ChangeThisPassword123!}
    volumes:
      - postgres_data:/var/lib/postgresql/data
    networks:
      - housing_network

  web:
    image: ali517/housing-management:latest
    container_name: housing_web
    restart: always
    environment:
      - FLASK_ENV=production
      - FLASK_DEBUG=False
      - DATABASE_TYPE=postgresql
      - DATABASE_HOST=db
      - DATABASE_PORT=5432
      - DATABASE_NAME=housing_db
      - DATABASE_USER=housing_user
      - DATABASE_PASSWORD=${DB_PASSWORD:-ChangeThisPassword123!}
      - SECRET_KEY=${SECRET_KEY:-generate-a-strong-secret-key-here}
    ports:
      - "8000:8000"
    depends_on:
      - db
    networks:
      - housing_network

  nginx:
    image: nginx:alpine
    container_name: housing_nginx
    restart: always
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
    depends_on:
      - web
    networks:
      - housing_network

volumes:
  postgres_data:

networks:
  housing_network:
    driver: bridge
```

---

## 🛠️ البناء المحلي / Local Build

```bash
# استنساخ المستودع / Clone repository
git clone https://github.com/Ali5829511/2025.git
cd 2025

# بناء الصورة / Build image
docker build -t housing-management:local .

# تشغيل / Run
docker run -d -p 8000:8000 housing-management:local
```

---

## 📊 الحجم والأداء / Size and Performance

- **حجم الصورة / Image Size**: ~300 MB
- **منصات مدعومة / Supported Platforms**: linux/amd64, linux/arm64
- **وقت البدء / Startup Time**: ~5-10 ثواني / seconds
- **استخدام الذاكرة / Memory Usage**: ~256 MB (قاعدة بيانات منفصلة / separate database)

---

## 🔗 روابط / Links

- **GitHub Repository**: https://github.com/Ali5829511/2025
- **Documentation**: https://github.com/Ali5829511/2025/blob/main/README.md
- **Docker Hub Guide**: https://github.com/Ali5829511/2025/blob/main/DOCKER_HUB_GUIDE.md
- **Issues**: https://github.com/Ali5829511/2025/issues

---

## 📝 الترخيص / License

جميع الحقوق محفوظة © جامعة الإمام محمد بن سعود الإسلامية 2025  
All rights reserved © Imam Mohammad Ibn Saud Islamic University 2025

---

## 📞 الدعم / Support

للحصول على الدعم:  
For support:

- 📖 راجع [الوثائق](https://github.com/Ali5829511/2025/blob/main/README.md)
- 🐛 افتح [Issue](https://github.com/Ali5829511/2025/issues)
- 💬 تواصل مع فريق التطوير / Contact development team
