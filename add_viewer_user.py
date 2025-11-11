"""
Script to add viewer user to existing database
سكريبت لإضافة مستخدم استعلام فقط إلى قاعدة البيانات الموجودة
"""

import database

def add_viewer_user():
    """Add viewer user if not exists"""
    
    print("=" * 60)
    print("Adding Viewer User / إضافة مستخدم الاستعلام")
    print("=" * 60)
    
    # Check if viewer user already exists
    conn = database.get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT COUNT(*) FROM users WHERE username = 'viewer'")
    exists = cursor.fetchone()[0] > 0
    
    if exists:
        print("⚠️  Viewer user already exists / المستخدم موجود بالفعل")
        conn.close()
        return
    
    # Create viewer user
    # ⚠️ SECURITY WARNING: These are default credentials for initial setup only
    # ⚠️ تحذير أمني: هذه بيانات افتراضية للإعداد الأولي فقط
    # Change the password immediately after first login in production
    # غيّر كلمة المرور فوراً بعد أول تسجيل دخول في بيئة الإنتاج
    username = 'viewer'
    password = 'Viewer@2025'
    name = 'مستخدم استعلام فقط'
    role = 'viewer'
    email = 'viewer@university.edu.sa'
    
    user_id = database.create_user(username, password, name, role, email)
    
    if user_id:
        print("✅ Viewer user created successfully / تم إنشاء المستخدم بنجاح")
        print("=" * 60)
        print("Viewer User Credentials / بيانات مستخدم الاستعلام:")
        print("=" * 60)
        print(f"Username / اسم المستخدم: {username}")
        print(f"Password / كلمة المرور: {password}")
        print(f"Role / الصلاحية: {role} (View Only / استعلام فقط)")
        print("=" * 60)
        print("⚠️  This user can only VIEW data, cannot add/edit/delete")
        print("⚠️  هذا المستخدم يمكنه الاستعلام فقط، لا يمكنه إضافة/تعديل/حذف")
        print("=" * 60)
        
        # Log the creation
        database.log_audit(
            user_id,
            'Viewer user account created',
            table_name='users',
            record_id=user_id
        )
    else:
        print("❌ Failed to create viewer user / فشل إنشاء المستخدم")
    
    conn.close()

if __name__ == '__main__':
    add_viewer_user()
