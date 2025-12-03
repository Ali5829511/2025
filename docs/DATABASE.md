# توثيق قاعدة البيانات / Database Documentation

## نظرة عامة / Overview

يستخدم نظام إدارة إسكان أعضاء هيئة التدريس قاعدة بيانات SQLite لتخزين جميع البيانات بشكل آمن ومنظم.

The Faculty Housing Management System uses an SQLite database to store all data securely and organized.

## هيكل قاعدة البيانات / Database Schema

### جدول المستخدمين / Users Table

```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,        -- Hashed with pbkdf2:sha256
    name TEXT NOT NULL,
    role TEXT NOT NULL,                 -- admin, violations, visitors
    email TEXT,
    phone TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP,
    is_active INTEGER DEFAULT 1
);
```

### جدول الجلسات / Sessions Table

```sql
CREATE TABLE sessions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    session_token TEXT UNIQUE NOT NULL,  -- Secure random token
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    expires_at TIMESTAMP NOT NULL,       -- Auto-expires after 24 hours
    ip_address TEXT,
    user_agent TEXT,
    FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
);
```

### جدول المباني / Buildings Table

```sql
CREATE TABLE buildings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    building_number TEXT UNIQUE NOT NULL,
    total_floors INTEGER,
    total_units INTEGER,
    address TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### جدول السكان / Residents Table

```sql
CREATE TABLE residents (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    national_id TEXT UNIQUE NOT NULL,
    email TEXT,
    phone TEXT NOT NULL,
    department TEXT,
    job_title TEXT,
    building_id INTEGER,
    unit_number TEXT,
    move_in_date DATE,
    move_out_date DATE,
    is_active INTEGER DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (building_id) REFERENCES buildings (id)
);
```

### جدول المركبات / Vehicles Table

```sql
CREATE TABLE vehicles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    plate_number TEXT UNIQUE NOT NULL,
    owner_id INTEGER NOT NULL,
    vehicle_type TEXT,
    make TEXT,
    model TEXT,
    year INTEGER,
    color TEXT,
    sticker_number TEXT UNIQUE,
    sticker_issued_date DATE,
    sticker_expiry_date DATE,
    is_active INTEGER DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (owner_id) REFERENCES residents (id) ON DELETE CASCADE
);
```

### جدول المخالفات المرورية / Traffic Violations Table

```sql
CREATE TABLE traffic_violations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    vehicle_id INTEGER NOT NULL,
    violation_type TEXT NOT NULL,
    violation_date TIMESTAMP NOT NULL,
    location TEXT,
    description TEXT,
    fine_amount DECIMAL(10, 2),
    status TEXT DEFAULT 'pending',      -- pending, paid, cancelled
    reported_by INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (vehicle_id) REFERENCES vehicles (id),
    FOREIGN KEY (reported_by) REFERENCES users (id)
);
```

### جدول الشكاوى / Complaints Table

```sql
CREATE TABLE complaints (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    resident_id INTEGER NOT NULL,
    category TEXT NOT NULL,
    title TEXT NOT NULL,
    description TEXT NOT NULL,
    priority TEXT DEFAULT 'medium',     -- low, medium, high, urgent
    status TEXT DEFAULT 'open',         -- open, in_progress, resolved, closed
    assigned_to INTEGER,
    resolution TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    resolved_at TIMESTAMP,
    FOREIGN KEY (resident_id) REFERENCES residents (id),
    FOREIGN KEY (assigned_to) REFERENCES users (id)
);
```

### جدول الزوار / Visitors Table

```sql
CREATE TABLE visitors (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    visitor_name TEXT NOT NULL,
    visitor_national_id TEXT,
    visitor_phone TEXT,
    visiting_resident_id INTEGER NOT NULL,
    visit_date DATE NOT NULL,
    entry_time TIMESTAMP,
    exit_time TIMESTAMP,
    purpose TEXT,
    vehicle_plate TEXT,
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (visiting_resident_id) REFERENCES residents (id)
);
```

### جدول الوقائع الأمنية / Security Incidents Table

```sql
CREATE TABLE security_incidents (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    incident_type TEXT NOT NULL,
    incident_date TIMESTAMP NOT NULL,
    location TEXT NOT NULL,
    description TEXT NOT NULL,
    severity TEXT DEFAULT 'medium',     -- low, medium, high, critical
    status TEXT DEFAULT 'reported',     -- reported, investigating, resolved
    reported_by INTEGER NOT NULL,
    resolved_by INTEGER,
    resolution TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    resolved_at TIMESTAMP,
    FOREIGN KEY (reported_by) REFERENCES users (id),
    FOREIGN KEY (resolved_by) REFERENCES users (id)
);
```

### جدول سجل التدقيق / Audit Log Table

```sql
CREATE TABLE audit_log (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    action TEXT NOT NULL,
    table_name TEXT,
    record_id INTEGER,
    old_values TEXT,
    new_values TEXT,
    ip_address TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users (id)
);
```

## الأمان / Security

### تشفير كلمات المرور / Password Hashing

- **الخوارزمية / Algorithm:** pbkdf2:sha256
- **المكتبة / Library:** Werkzeug Security
- **التكرارات / Iterations:** 260,000 (default)
- **الملح / Salt:** عشوائي لكل كلمة مرور / Random per password

### إدارة الجلسات / Session Management

- **الرموز / Tokens:** عشوائية آمنة 32 بايت / Secure random 32 bytes
- **مدة الانتهاء / Expiry:** 24 ساعة / 24 hours
- **التخزين / Storage:** قاعدة البيانات مع معلومات IP و User-Agent / Database with IP and User-Agent info

### سجل التدقيق / Audit Logging

- تسجيل جميع عمليات تسجيل الدخول والخروج / Log all login/logout operations
- تسجيل التغييرات على البيانات الحساسة / Log changes to sensitive data
- تسجيل المحاولات الفاشلة / Log failed attempts
- حفظ عنوان IP للعمليات / Store IP address for operations

### أدوار المستخدمين / User Roles

| الدور / Role | الصلاحيات / Permissions |
|-------------|------------------------|
| **admin** | صلاحيات كاملة - إضافة، تعديل، حذف، عرض / Full access - Create, Update, Delete, View |
| **violations** | المخالفات المرورية والحوادث / Traffic violations and accidents |
| **visitors** | الزوار والشكاوى / Visitors and complaints |
| **viewer** | ✅ **استعلام فقط** - عرض البيانات بدون تعديل / **View Only** - Read data without modifications |

## استخدام واجهة برمجة التطبيقات / API Usage

### تسجيل الدخول / Login

```bash
POST /api/auth/login
Content-Type: application/json

{
    "username": "admin",
    "password": "Admin@2025"
}

# Response:
{
    "success": true,
    "user": {
        "id": 1,
        "username": "admin",
        "name": "مدير النظام",
        "role": "admin",
        "email": "admin@university.edu.sa"
    },
    "message": "Login successful"
}
```

### التحقق من الجلسة / Validate Session

```bash
GET /api/auth/validate

# Response:
{
    "success": true,
    "authenticated": true,
    "user": {
        "id": 1,
        "username": "admin",
        "name": "مدير النظام",
        "role": "admin"
    }
}
```

### تسجيل الخروج / Logout

```bash
POST /api/auth/logout

# Response:
{
    "success": true,
    "message": "Logged out successfully"
}
```

### تغيير كلمة المرور / Change Password

```bash
POST /api/auth/change-password
Content-Type: application/json

{
    "current_password": "Admin@2025",
    "new_password": "NewPassword@2025"
}

# Response:
{
    "success": true,
    "message": "Password changed successfully"
}
```

## النسخ الاحتياطي / Backup

### نسخ احتياطي يدوي / Manual Backup

```bash
# نسخ ملف قاعدة البيانات / Copy database file
cp housing.db housing_backup_$(date +%Y%m%d_%H%M%S).db

# أو استخدام أداة SQLite / Or use SQLite tool
sqlite3 housing.db ".backup housing_backup.db"
```

### النسخ الاحتياطي التلقائي / Automated Backup

```bash
# إضافة إلى crontab للنسخ الاحتياطي اليومي
# Add to crontab for daily backup
0 2 * * * cd /path/to/project && sqlite3 housing.db ".backup backups/housing_$(date +\%Y\%m\%d).db"
```

## الصيانة / Maintenance

### تنظيف الجلسات المنتهية / Cleanup Expired Sessions

```python
# يتم تلقائياً عند بدء الخادم
# Done automatically on server start
from auth import cleanup_expired_sessions
deleted = cleanup_expired_sessions()
```

### تحسين قاعدة البيانات / Optimize Database

```bash
sqlite3 housing.db "VACUUM;"
```

### عرض الإحصائيات / View Statistics

```bash
sqlite3 housing.db "SELECT COUNT(*) FROM users;"
sqlite3 housing.db "SELECT COUNT(*) FROM sessions WHERE expires_at > datetime('now');"
```

## الترحيل إلى PostgreSQL / Migration to PostgreSQL

للحصول على أداء أفضل في الإنتاج، يمكن الترحيل إلى PostgreSQL:

For better performance in production, you can migrate to PostgreSQL:

1. تصدير البيانات / Export data:
```bash
sqlite3 housing.db .dump > housing_dump.sql
```

2. تحويل إلى PostgreSQL / Convert to PostgreSQL:
```bash
# تعديل الملف لإزالة خصائص SQLite / Modify file to remove SQLite specifics
# ثم استيراد إلى PostgreSQL / Then import to PostgreSQL
psql -U username -d housing_db -f housing_dump.sql
```

## الدعم / Support

للمساعدة أو الاستفسارات حول قاعدة البيانات:

For help or questions about the database:

- مراجعة documentation في ملفات `database.py` و `auth.py`
- Review documentation in `database.py` and `auth.py` files
- التواصل مع فريق التطوير
- Contact development team

---

**آخر تحديث / Last Updated:** نوفمبر 2025 / November 2025
