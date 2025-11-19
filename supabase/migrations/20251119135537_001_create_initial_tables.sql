/*
  # إنشاء جداول النظام الأساسية
  # Create Initial System Tables
  
  1. جداول جديدة / New Tables
    - `users` - المستخدمون مع تشفير كلمات المرور
    - `sessions` - جلسات المستخدمين الآمنة
    - `buildings` - المباني
    - `apartments` - الشقق
    - `residents` - السكان
    - `vehicles` - المركبات
    - `parking_spots` - مواقف السيارات
    - `stickers` - ملصقات المركبات
    - `traffic_violations` - المخالفات المرورية
    - `security_incidents` - الوقائع الأمنية
    - `complaints` - الشكاوى
    - `visitors` - الزوار
    - `licenses` - التراخيص
    - `audit_log` - سجل التدقيق
  
  2. الأمان / Security
    - تفعيل RLS على جميع الجداول
    - سياسات للمستخدمين المصادقين فقط
*/

-- جدول المستخدمين / Users table
CREATE TABLE IF NOT EXISTS users (
    id BIGSERIAL PRIMARY KEY,
    username TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    name TEXT NOT NULL,
    role TEXT NOT NULL,
    email TEXT,
    phone TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    last_login TIMESTAMPTZ,
    is_active BOOLEAN DEFAULT TRUE,
    must_change_password BOOLEAN DEFAULT FALSE
);

-- جدول الجلسات / Sessions table
CREATE TABLE IF NOT EXISTS sessions (
    id BIGSERIAL PRIMARY KEY,
    user_id BIGINT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    session_token TEXT UNIQUE NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    expires_at TIMESTAMPTZ NOT NULL,
    ip_address TEXT,
    user_agent TEXT
);

-- جدول المباني / Buildings table
CREATE TABLE IF NOT EXISTS buildings (
    id BIGSERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    building_number TEXT UNIQUE NOT NULL,
    total_floors INTEGER,
    total_units INTEGER,
    address TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- جدول الشقق / Apartments table
CREATE TABLE IF NOT EXISTS apartments (
    id BIGSERIAL PRIMARY KEY,
    building_id BIGINT NOT NULL REFERENCES buildings(id),
    unit_number TEXT NOT NULL,
    floor_number INTEGER,
    unit_type TEXT DEFAULT 'شقة',
    is_occupied BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE(building_id, unit_number)
);

-- جدول السكان / Residents table
CREATE TABLE IF NOT EXISTS residents (
    id BIGSERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    national_id TEXT UNIQUE NOT NULL,
    email TEXT,
    phone TEXT NOT NULL,
    department TEXT,
    job_title TEXT,
    building_id BIGINT REFERENCES buildings(id),
    unit_number TEXT,
    move_in_date DATE,
    move_out_date DATE,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- جدول المركبات / Vehicles table
CREATE TABLE IF NOT EXISTS vehicles (
    id BIGSERIAL PRIMARY KEY,
    plate_number TEXT UNIQUE NOT NULL,
    owner_id BIGINT NOT NULL REFERENCES residents(id) ON DELETE CASCADE,
    vehicle_type TEXT,
    make TEXT,
    model TEXT,
    year INTEGER,
    color TEXT,
    sticker_number TEXT UNIQUE,
    sticker_issued_date DATE,
    sticker_expiry_date DATE,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- جدول مواقف السيارات / Parking spots table
CREATE TABLE IF NOT EXISTS parking_spots (
    id BIGSERIAL PRIMARY KEY,
    spot_number TEXT UNIQUE NOT NULL,
    parking_area TEXT NOT NULL,
    building_id BIGINT REFERENCES buildings(id),
    apartment_id BIGINT REFERENCES apartments(id),
    is_occupied BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- جدول الملصقات / Stickers table
CREATE TABLE IF NOT EXISTS stickers (
    id BIGSERIAL PRIMARY KEY,
    sticker_number TEXT UNIQUE NOT NULL,
    resident_id BIGINT NOT NULL REFERENCES residents(id) ON DELETE CASCADE,
    plate_number TEXT NOT NULL,
    vehicle_type TEXT,
    issue_date DATE NOT NULL,
    expiry_date DATE,
    status TEXT DEFAULT 'active',
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- جدول المخالفات المرورية / Traffic violations table
CREATE TABLE IF NOT EXISTS traffic_violations (
    id BIGSERIAL PRIMARY KEY,
    vehicle_id BIGINT NOT NULL REFERENCES vehicles(id),
    violation_type TEXT NOT NULL,
    violation_date TIMESTAMPTZ NOT NULL,
    location TEXT,
    description TEXT,
    fine_amount DECIMAL(10, 2),
    status TEXT DEFAULT 'pending',
    reported_by BIGINT REFERENCES users(id),
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- جدول الوقائع الأمنية / Security incidents table
CREATE TABLE IF NOT EXISTS security_incidents (
    id BIGSERIAL PRIMARY KEY,
    incident_type TEXT NOT NULL,
    incident_date TIMESTAMPTZ NOT NULL,
    location TEXT NOT NULL,
    description TEXT NOT NULL,
    severity TEXT DEFAULT 'medium',
    status TEXT DEFAULT 'reported',
    reported_by BIGINT NOT NULL REFERENCES users(id),
    resolved_by BIGINT REFERENCES users(id),
    resolution TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    resolved_at TIMESTAMPTZ
);

-- جدول الشكاوى / Complaints table
CREATE TABLE IF NOT EXISTS complaints (
    id BIGSERIAL PRIMARY KEY,
    resident_id BIGINT NOT NULL REFERENCES residents(id),
    category TEXT NOT NULL,
    title TEXT NOT NULL,
    description TEXT NOT NULL,
    priority TEXT DEFAULT 'medium',
    status TEXT DEFAULT 'open',
    assigned_to BIGINT REFERENCES users(id),
    resolution TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    resolved_at TIMESTAMPTZ
);

-- جدول الزوار / Visitors table
CREATE TABLE IF NOT EXISTS visitors (
    id BIGSERIAL PRIMARY KEY,
    visitor_name TEXT NOT NULL,
    visitor_national_id TEXT,
    visitor_phone TEXT,
    visiting_resident_id BIGINT NOT NULL REFERENCES residents(id),
    visit_date DATE NOT NULL,
    entry_time TIMESTAMPTZ,
    exit_time TIMESTAMPTZ,
    purpose TEXT,
    vehicle_plate TEXT,
    notes TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- جدول التراخيص / Licenses table
CREATE TABLE IF NOT EXISTS licenses (
    id BIGSERIAL PRIMARY KEY,
    license_number TEXT UNIQUE NOT NULL,
    license_type TEXT NOT NULL,
    holder_name TEXT NOT NULL,
    national_id TEXT,
    issue_date DATE NOT NULL,
    expiry_date DATE NOT NULL,
    status TEXT DEFAULT 'pending',
    notes TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- جدول سجل التدقيق / Audit log table
CREATE TABLE IF NOT EXISTS audit_log (
    id BIGSERIAL PRIMARY KEY,
    user_id BIGINT REFERENCES users(id),
    action TEXT NOT NULL,
    table_name TEXT,
    record_id BIGINT,
    old_values TEXT,
    new_values TEXT,
    ip_address TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- تفعيل RLS على جميع الجداول / Enable RLS on all tables
ALTER TABLE users ENABLE ROW LEVEL SECURITY;
ALTER TABLE sessions ENABLE ROW LEVEL SECURITY;
ALTER TABLE buildings ENABLE ROW LEVEL SECURITY;
ALTER TABLE apartments ENABLE ROW LEVEL SECURITY;
ALTER TABLE residents ENABLE ROW LEVEL SECURITY;
ALTER TABLE vehicles ENABLE ROW LEVEL SECURITY;
ALTER TABLE parking_spots ENABLE ROW LEVEL SECURITY;
ALTER TABLE stickers ENABLE ROW LEVEL SECURITY;
ALTER TABLE traffic_violations ENABLE ROW LEVEL SECURITY;
ALTER TABLE security_incidents ENABLE ROW LEVEL SECURITY;
ALTER TABLE complaints ENABLE ROW LEVEL SECURITY;
ALTER TABLE visitors ENABLE ROW LEVEL SECURITY;
ALTER TABLE licenses ENABLE ROW LEVEL SECURITY;
ALTER TABLE audit_log ENABLE ROW LEVEL SECURITY;

-- سياسات الأمان (مؤقتة - للمصادقة) / Security policies (temporary - for authenticated users)
-- سنضيف سياسات أكثر تفصيلاً لاحقاً

CREATE POLICY "Allow authenticated users to read users"
  ON users FOR SELECT
  TO authenticated
  USING (true);

CREATE POLICY "Allow authenticated users to manage sessions"
  ON sessions FOR ALL
  TO authenticated
  USING (true);

CREATE POLICY "Allow authenticated users to read buildings"
  ON buildings FOR SELECT
  TO authenticated
  USING (true);

CREATE POLICY "Allow authenticated users to read apartments"
  ON apartments FOR SELECT
  TO authenticated
  USING (true);

CREATE POLICY "Allow authenticated users to manage residents"
  ON residents FOR ALL
  TO authenticated
  USING (true);

CREATE POLICY "Allow authenticated users to manage vehicles"
  ON vehicles FOR ALL
  TO authenticated
  USING (true);

CREATE POLICY "Allow authenticated users to manage parking_spots"
  ON parking_spots FOR ALL
  TO authenticated
  USING (true);

CREATE POLICY "Allow authenticated users to manage stickers"
  ON stickers FOR ALL
  TO authenticated
  USING (true);

CREATE POLICY "Allow authenticated users to manage traffic_violations"
  ON traffic_violations FOR ALL
  TO authenticated
  USING (true);

CREATE POLICY "Allow authenticated users to manage security_incidents"
  ON security_incidents FOR ALL
  TO authenticated
  USING (true);

CREATE POLICY "Allow authenticated users to manage complaints"
  ON complaints FOR ALL
  TO authenticated
  USING (true);

CREATE POLICY "Allow authenticated users to manage visitors"
  ON visitors FOR ALL
  TO authenticated
  USING (true);

CREATE POLICY "Allow authenticated users to manage licenses"
  ON licenses FOR ALL
  TO authenticated
  USING (true);

CREATE POLICY "Allow authenticated users to read audit_log"
  ON audit_log FOR SELECT
  TO authenticated
  USING (true);