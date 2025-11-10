"""
Script to add violation entry user to existing database
سكريبت لإضافة مستخدم تسجيل المخالفات إلى قاعدة البيانات الموجودة
"""

import database

def add_violation_entry_user():
    """Add violation entry user if not exists"""
    
    print("=" * 60)
    print("Adding Violation Entry User / إضافة مستخدم تسجيل المخالفات")
    print("=" * 60)
    
    # Check if user already exists
    conn = database.get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT COUNT(*) FROM users WHERE username = 'violation_entry'")
    exists = cursor.fetchone()[0] > 0
    
    if exists:
        print("⚠️  Violation entry user already exists / المستخدم موجود بالفعل")
        conn.close()
        return
    
    # Create violation entry user
    # ⚠️ SECURITY WARNING: These are default credentials for initial setup only
    # ⚠️ تحذير أمني: هذه بيانات افتراضية للإعداد الأولي فقط
    # Change the password immediately after first login in production
    # غيّر كلمة المرور فوراً بعد أول تسجيل دخول في بيئة الإنتاج
    username = 'violation_entry'
    password = 'Violation@2025'
    name = 'مسجل المخالفات'
    role = 'violation_entry'
    email = 'violation.entry@university.edu.sa'
    
    user_id = database.create_user(username, password, name, role, email)
    
    if user_id:
        print("✅ Violation entry user created successfully / تم إنشاء المستخدم بنجاح")
        print("=" * 60)
        print("Violation Entry User Credentials / بيانات مستخدم تسجيل المخالفات:")
        print("=" * 60)
        print(f"Username / اسم المستخدم: {username}")
        print(f"Password / كلمة المرور: {password}")
        print(f"Role / الصلاحية: {role}")
        print("=" * 60)
        print("📝 This user will be redirected to violation form on login")
        print("📝 سيتم توجيه هذا المستخدم مباشرة لنموذج تسجيل المخالفة")
        print("=" * 60)
        print("✅ Features / المميزات:")
        print("   - Quick access to violation form / وصول سريع لنموذج المخالفة")
        print("   - Can register traffic violations / يمكنه تسجيل المخالفات المرورية")
        print("   - View violation history / عرض سجل المخالفات")
        print("   - Print violation reports / طباعة تقارير المخالفات")
        print("=" * 60)
        
        # Log the creation
        database.log_audit(
            user_id,
            'Violation entry user account created',
            table_name='users',
            record_id=user_id
        )
    else:
        print("❌ Failed to create violation entry user / فشل إنشاء المستخدم")
    
    conn.close()

if __name__ == '__main__':
    add_violation_entry_user()
