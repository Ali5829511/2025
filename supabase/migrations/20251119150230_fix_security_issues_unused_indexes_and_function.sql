/*
  # إصلاح المشاكل الأمنية
  # Fix Security Issues
  
  ## المشاكل المعالجة / Issues Addressed:
  
  ### 1. إزالة الفهارس غير المستخدمة / Remove Unused Indexes
  هذه الفهارس تستهلك مساحة التخزين وتبطئ عمليات الكتابة دون فائدة:
  These indexes consume storage and slow down writes without providing benefit:
  
  - `idx_vehicles_plate` - مكرر مع فهرس UNIQUE الموجود
  - `idx_events_timestamp` - غير مستخدم في الاستعلامات الحالية
  - `idx_events_vehicle` - غير مستخدم في الاستعلامات الحالية
  - `idx_events_camera` - غير مستخدم في الاستعلامات الحالية
  - `idx_events_vehicle_timestamp` - غير مستخدم في الاستعلامات الحالية
  - `idx_violations_vehicle` - غير مستخدم في الاستعلامات الحالية
  - `idx_violations_status` - غير مستخدم في الاستعلامات الحالية
  - `idx_violations_type` - غير مستخدم في الاستعلامات الحالية
  - `idx_settings_key` - مكرر مع فهرس UNIQUE الموجود
  
  ### 2. إصلاح ثغرة search_path في الدالة / Fix Function Search Path Vulnerability
  الدالة `update_updated_at_column` لديها search_path قابل للتغيير مما يشكل خطر أمني
  The `update_updated_at_column` function has a mutable search_path which is a security risk
  
  ## التغييرات / Changes:
  
  1. إزالة جميع الفهارس غير المستخدمة
     Drop all unused indexes
     
  2. إعادة إنشاء الدالة مع search_path ثابت وآمن
     Recreate function with fixed and secure search_path
  
  ## الفوائد الأمنية / Security Benefits:
  
  - تقليل سطح الهجوم الأمني
    Reduce security attack surface
    
  - تحسين الأداء بإزالة الفهارس المكلفة غير المستخدمة
    Improve performance by removing costly unused indexes
    
  - حماية من هجمات search_path injection
    Protect against search_path injection attacks
*/

-- إزالة الفهارس غير المستخدمة / Drop unused indexes
DROP INDEX IF EXISTS idx_vehicles_plate;
DROP INDEX IF EXISTS idx_events_timestamp;
DROP INDEX IF EXISTS idx_events_vehicle;
DROP INDEX IF EXISTS idx_events_camera;
DROP INDEX IF EXISTS idx_events_vehicle_timestamp;
DROP INDEX IF EXISTS idx_violations_vehicle;
DROP INDEX IF EXISTS idx_violations_status;
DROP INDEX IF EXISTS idx_violations_type;
DROP INDEX IF EXISTS idx_settings_key;

-- إعادة إنشاء الدالة مع search_path آمن / Recreate function with secure search_path
DROP FUNCTION IF EXISTS update_updated_at_column() CASCADE;

CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER
LANGUAGE plpgsql
SECURITY DEFINER
SET search_path = pg_catalog, public
AS $$
BEGIN
    NEW.updated_at = now();
    RETURN NEW;
END;
$$;

-- تعليق توضيحي للدالة / Add function comment
COMMENT ON FUNCTION update_updated_at_column() IS 
'Automatically updates the updated_at column to current timestamp. 
Secure function with fixed search_path to prevent injection attacks.';
