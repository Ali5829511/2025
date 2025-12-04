# نظام إدارة المخالفات المرورية
# Traffic Violations Management System

<div dir="rtl">

## 🚀 نظرة عامة

نظام متكامل لإدارة المخالفات المرورية مع دعم التعرف الآلي على لوحات السيارات باستخدام Plate Recognizer API.

### المميزات الرئيسية

✅ إدارة المخالفات المرورية بشكل كامل
✅ التعرف التلقائي على لوحات السيارات من الصور
✅ قاعدة بيانات متكاملة للسيارات والمخالفات
✅ واجهة عربية سهلة الاستخدام
✅ API متكامل للتطبيقات الخارجية
✅ نظام صحة (Health Checks) للمراقبة
✅ خادم إنتاجي مع Gunicorn

</div>

---

## 📋 Quick Start

### Local Development

```bash
# Install dependencies
pip install -r requirements.txt

# Initialize database
python init_traffic_db.py

# Run development server
python traffic_app.py
```

The application will be available at `http://localhost:5001`

### Production Deployment

```bash
# With Gunicorn (Recommended)
gunicorn --config gunicorn_traffic_config.py traffic_app:app

# Or with environment variables
PORT=10000 gunicorn --config gunicorn_traffic_config.py traffic_app:app
```

---

## 🔧 Configuration

### Environment Variables

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `PORT` | Server port | 5001 | No |
| `FLASK_DEBUG` | Debug mode | False | No |
| `PLATE_RECOGNIZER_API_TOKEN` | API token for plate recognition | - | Optional |

### Files

- `traffic_app.py` - Main application
- `gunicorn_traffic_config.py` - Production server configuration
- `init_traffic_db.py` - Database initialization
- `traffic.db` - SQLite database (auto-created)

---

## 🌐 API Endpoints

### Health Check

```http
GET /health
GET /api/health
```

Response:
```json
{
    "status": "healthy",
    "service": "Traffic Violations Management System",
    "database": "connected",
    "timestamp": "2025-11-11T21:40:56.460175"
}
```

### Violations

```http
GET /api/violations
```

Get all violations with car details.

```http
POST /api/add-violation
Content-Type: application/json

{
    "plate_number": "ABC1234",
    "violation_type": "سرعة زائدة",
    "violation_date": "2025-11-11",
    "fine_amount": 500,
    "officer_name": "أحمد",
    "image_path": "/static/uploads/violations/image.jpg"
}
```

### Cars

```http
GET /api/cars
```

Get all registered cars.

### Upload Violation Image

```http
POST /api/upload-violation
Content-Type: multipart/form-data

image: [file]
```

Response includes automatic plate recognition if API token is configured.

### Plate Recognizer Status

```http
GET /api/plate-recognizer/status
```

Check if Plate Recognizer API is configured and working.

---

## 🐳 Docker Deployment

```bash
# Build image
docker build -f Dockerfile.traffic -t traffic-violations-system .

# Run container
docker run -p 10000:10000 \
  -e PORT=10000 \
  -e PLATE_RECOGNIZER_API_TOKEN=your_token \
  traffic-violations-system
```

---

## ☁️ Cloud Deployment

### Render.com

Use the provided `render.traffic.yaml`:

```yaml
services:
  - type: web
    name: traffic-violations-system
    env: python
    startCommand: gunicorn --config gunicorn_traffic_config.py traffic_app:app
    healthCheckPath: /health
```

Deploy with:
```bash
render deploy
```

### Heroku / Railway

The `Procfile.traffic` is configured:

```
web: gunicorn --config gunicorn_traffic_config.py traffic_app:app
```

---

## 📊 Database Schema

### Cars Table
- `car_id` (INTEGER, PRIMARY KEY)
- `plate_number` (TEXT, UNIQUE)
- `owner_name` (TEXT)
- `model` (TEXT)
- `year` (INTEGER)
- `color` (TEXT)

### Violations Table
- `violation_id` (INTEGER, PRIMARY KEY)
- `car_id` (INTEGER, FOREIGN KEY)
- `violation_type` (TEXT)
- `violation_date` (TEXT)
- `fine_amount` (REAL)
- `officer_name` (TEXT)
- `image_path` (TEXT)

---

## 🔒 Security

### Features

✅ **CORS enabled** - Secure cross-origin requests
✅ **SQL injection protection** - Parameterized queries
✅ **File upload validation** - Only allowed image types
✅ **Error message sanitization** - No stack trace exposure
✅ **Secure file naming** - Werkzeug secure_filename

### Best Practices

- API tokens stored in environment variables
- Database connection properly closed
- Graceful error handling
- Request timeout configured (120s)

---

## 🧪 Testing

### Manual Testing

```bash
# Start server
PORT=10000 python traffic_app.py

# Test health endpoint
curl http://localhost:10000/health

# Test violations API
curl http://localhost:10000/api/violations

# Test with Gunicorn
gunicorn --config gunicorn_traffic_config.py traffic_app:app
curl http://localhost:10000/health
```

### Expected Results

- Health check returns HTTP 200
- JSON response with status "healthy"
- Database connection confirmed
- All API endpoints accessible

---

## 🐛 Troubleshooting

### Port Already in Use

```bash
# Find process using port
lsof -i :10000

# Kill process
kill -9 <PID>
```

### Database Not Found

```bash
# Initialize database
python init_traffic_db.py
```

### Plate Recognizer Not Working

1. Check API token is set: `echo $PLATE_RECOGNIZER_API_TOKEN`
2. Test API: `curl http://localhost:10000/api/plate-recognizer/status`
3. Verify token at https://app.platerecognizer.com

### Workers Timing Out

Increase timeout in `gunicorn_traffic_config.py`:

```python
timeout = 180  # Increase from 120 to 180
```

---

## 📚 Documentation

- [Complete Deployment Fix Guide](TRAFFIC_DEPLOYMENT_FIX.md)
- [System Requirements](requirements.txt)
- [Docker Configuration](Dockerfile.traffic)
- [Render Configuration](render.traffic.yaml)

---

## 🤝 Contributing

Contributions are welcome! Please ensure:

1. Code follows existing style
2. All tests pass
3. Security checks pass
4. Documentation is updated

---

## 📄 License

This project is part of the University Housing Management System.

---

## 📞 Support

For issues or questions:
1. Check [TRAFFIC_DEPLOYMENT_FIX.md](TRAFFIC_DEPLOYMENT_FIX.md)
2. Review application logs
3. Test health endpoint
4. Verify environment variables

---

<div dir="rtl">

## 🎯 الميزات القادمة

- [ ] تصدير التقارير PDF
- [ ] إحصائيات المخالفات
- [ ] إشعارات البريد الإلكتروني
- [ ] تطبيق موبايل
- [ ] لوحة تحكم إدارية متقدمة

</div>

---

**Version**: 1.0.0  
**Last Updated**: 2025-11-11  
**Status**: ✅ Production Ready
