# API Documentation - توثيق واجهة برمجة التطبيقات
# Housing Management System

## Authentication Endpoints / نقاط المصادقة

### 1. Login / تسجيل الدخول

**Endpoint:** `POST /api/auth/login`

**Description:** Authenticate user and create session / مصادقة المستخدم وإنشاء جلسة

**Request Body:**
```json
{
  "username": "admin",
  "password": "Admin@2025"
}
```

**Success Response (200 OK):**
```json
{
  "success": true,
  "session_token": "secure-random-token",
  "must_change_password": true,
  "user": {
    "id": 1,
    "username": "admin",
    "name": "مدير النظام",
    "role": "admin",
    "email": "admin@university.edu.sa"
  },
  "message": "Login successful - Password change required",
  "message_ar": "تم تسجيل الدخول بنجاح - يجب تغيير كلمة المرور"
}
```

**Error Response (401 Unauthorized):**
```json
{
  "success": false,
  "error": "Invalid credentials",
  "error_ar": "اسم المستخدم أو كلمة المرور غير صحيحة"
}
```

**Notes:**
- Session cookie is set automatically
- `must_change_password` flag indicates if password change is required
- Default passwords must be changed on first login

---

### 2. Change Password / تغيير كلمة المرور

**Endpoint:** `POST /api/auth/change-password`

**Authentication:** Required (session cookie)

**Description:** Change user password / تغيير كلمة مرور المستخدم

**Request Body:**
```json
{
  "current_password": "Admin@2025",
  "new_password": "MyNewSecurePassword123!"
}
```

**Success Response (200 OK):**
```json
{
  "success": true,
  "message": "Password changed successfully",
  "message_ar": "تم تغيير كلمة المرور بنجاح"
}
```

**Error Responses:**

**400 Bad Request - Missing fields:**
```json
{
  "success": false,
  "error": "Current and new password required",
  "error_ar": "كلمة المرور الحالية والجديدة مطلوبة"
}
```

**400 Bad Request - Weak password:**
```json
{
  "success": false,
  "error": "Password must be at least 8 characters",
  "error_ar": "يجب أن تكون كلمة المرور 8 أحرف على الأقل"
}
```

**401 Unauthorized - Wrong current password:**
```json
{
  "success": false,
  "error": "Current password is incorrect",
  "error_ar": "كلمة المرور الحالية غير صحيحة"
}
```

**Password Requirements:**
- Minimum 8 characters
- Recommended: Mix of uppercase, lowercase, numbers, and symbols
- Must be different from current password

**Notes:**
- After successful password change, `must_change_password` flag is cleared
- Password change is logged in audit trail
- User remains logged in after password change

---

### 3. Logout / تسجيل الخروج

**Endpoint:** `POST /api/auth/logout`

**Authentication:** Required (session cookie)

**Description:** Destroy current session / إنهاء الجلسة الحالية

**Request Body:** None

**Success Response (200 OK):**
```json
{
  "success": true,
  "message": "Logged out successfully",
  "message_ar": "تم تسجيل الخروج بنجاح"
}
```

**Notes:**
- Session cookie is cleared automatically
- Session is removed from database
- Logout is logged in audit trail

---

### 4. Validate Session / التحقق من الجلسة

**Endpoint:** `GET /api/auth/validate`

**Authentication:** Required (session cookie)

**Description:** Validate current session / التحقق من صحة الجلسة الحالية

**Success Response (200 OK):**
```json
{
  "success": true,
  "authenticated": true,
  "user": {
    "id": 1,
    "username": "admin",
    "name": "مدير النظام",
    "role": "admin",
    "email": "admin@university.edu.sa"
  }
}
```

**Error Response (401 Unauthorized):**
```json
{
  "success": false,
  "authenticated": false
}
```

**Notes:**
- Used to check if user is still authenticated
- Session expires after 24 hours by default
- Can be configured via SESSION_TIMEOUT_HOURS environment variable

---

## Security Features / الميزات الأمنية

### Password Change Enforcement / فرض تغيير كلمة المرور

When a user with a default password logs in:

1. **Login Response** includes `must_change_password: true`
2. **Client Application** should redirect user to change password page
3. **User cannot proceed** until password is changed
4. **After password change**, `must_change_password` flag is cleared

**Default Accounts:**
- `admin` - Admin@2025
- `violations_officer` - Violations@2025
- `visitors_officer` - Visitors@2025
- `viewer` - Viewer@2025
- `violation_entry` - Violation@2025

### Session Management / إدارة الجلسات

- **Session Duration:** 24 hours (configurable)
- **Session Storage:** Database with secure tokens
- **Auto Cleanup:** Expired sessions removed automatically
- **Security:** HttpOnly, Secure (on HTTPS), SameSite cookies

### Audit Logging / سجل التدقيق

All authentication events are logged:
- Login attempts (success/failure)
- Password changes
- Logout events
- Session validations

**Log Location:** `logs/audit.log`

---

## Example Usage / أمثلة الاستخدام

### JavaScript/Fetch API

```javascript
// Login
async function login(username, password) {
  const response = await fetch('/api/auth/login', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    credentials: 'include', // Important for cookies
    body: JSON.stringify({ username, password })
  });
  
  const data = await response.json();
  
  if (data.success) {
    if (data.must_change_password) {
      // Redirect to change password page
      window.location.href = '/change-password.html';
    } else {
      // Redirect to dashboard
      window.location.href = '/dashboard.html';
    }
  } else {
    alert(data.error_ar || data.error);
  }
}

// Change Password
async function changePassword(currentPassword, newPassword) {
  const response = await fetch('/api/auth/change-password', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    credentials: 'include',
    body: JSON.stringify({
      current_password: currentPassword,
      new_password: newPassword
    })
  });
  
  const data = await response.json();
  
  if (data.success) {
    alert(data.message_ar || data.message);
    window.location.href = '/dashboard.html';
  } else {
    alert(data.error_ar || data.error);
  }
}

// Logout
async function logout() {
  const response = await fetch('/api/auth/logout', {
    method: 'POST',
    credentials: 'include'
  });
  
  const data = await response.json();
  
  if (data.success) {
    window.location.href = '/index.html';
  }
}

// Check if logged in
async function checkAuth() {
  const response = await fetch('/api/auth/validate', {
    credentials: 'include'
  });
  
  const data = await response.json();
  
  if (!data.authenticated) {
    window.location.href = '/index.html';
  }
  
  return data.user;
}
```

### Python/Requests

```python
import requests

# Login
def login(username, password):
    response = requests.post(
        'https://yourdomain.com/api/auth/login',
        json={'username': username, 'password': password}
    )
    
    data = response.json()
    
    if data['success']:
        session_token = response.cookies.get('session_token')
        print(f"Logged in as {data['user']['name']}")
        
        if data.get('must_change_password'):
            print("⚠️  Password change required!")
            return None
        
        return session_token
    else:
        print(f"Login failed: {data['error']}")
        return None

# Change Password
def change_password(session_token, current_password, new_password):
    cookies = {'session_token': session_token}
    
    response = requests.post(
        'https://yourdomain.com/api/auth/change-password',
        json={
            'current_password': current_password,
            'new_password': new_password
        },
        cookies=cookies
    )
    
    data = response.json()
    
    if data['success']:
        print("✅ Password changed successfully")
        return True
    else:
        print(f"❌ Password change failed: {data['error']}")
        return False

# Logout
def logout(session_token):
    cookies = {'session_token': session_token}
    
    response = requests.post(
        'https://yourdomain.com/api/auth/logout',
        cookies=cookies
    )
    
    data = response.json()
    
    if data['success']:
        print("✅ Logged out successfully")
        return True
    
    return False
```

### cURL Examples

```bash
# Login
curl -X POST https://yourdomain.com/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"Admin@2025"}' \
  -c cookies.txt

# Change Password
curl -X POST https://yourdomain.com/api/auth/change-password \
  -H "Content-Type: application/json" \
  -d '{"current_password":"Admin@2025","new_password":"MyNewPassword123!"}' \
  -b cookies.txt

# Validate Session
curl -X GET https://yourdomain.com/api/auth/validate \
  -b cookies.txt

# Logout
curl -X POST https://yourdomain.com/api/auth/logout \
  -b cookies.txt
```

---

## Error Codes / رموز الأخطاء

| Code | Description | Arabic |
|------|-------------|---------|
| 200 | Success | نجح |
| 400 | Bad Request - Invalid input | طلب غير صالح |
| 401 | Unauthorized - Invalid credentials or session | غير مصرح |
| 403 | Forbidden - Insufficient permissions | محظور |
| 500 | Internal Server Error | خطأ في الخادم |

---

## Security Best Practices / أفضل الممارسات الأمنية

### For Developers / للمطورين

1. **Always use HTTPS** in production / استخدم HTTPS دائماً في الإنتاج
2. **Include credentials** in fetch requests / ضمّن بيانات الاعتماد في الطلبات
3. **Handle must_change_password** flag properly / تعامل مع علامة must_change_password بشكل صحيح
4. **Implement client-side validation** / نفّذ التحقق من جانب العميل
5. **Clear sensitive data** from memory / امسح البيانات الحساسة من الذاكرة
6. **Use secure session storage** / استخدم تخزين جلسات آمن
7. **Implement auto-logout** on inactivity / نفّذ تسجيل خروج تلقائي عند عدم النشاط
8. **Log security events** / سجل الأحداث الأمنية

### For Users / للمستخدمين

1. **Change default passwords** immediately / غيّر كلمات المرور الافتراضية فوراً
2. **Use strong passwords** (8+ characters) / استخدم كلمات مرور قوية
3. **Never share credentials** / لا تشارك بيانات الدخول أبداً
4. **Logout when finished** / سجل خروج عند الانتهاء
5. **Report suspicious activity** / أبلغ عن أي نشاط مشبوه

---

## Rate Limiting / تحديد المعدل

To prevent brute force attacks, consider implementing rate limiting:

```python
# Example: Using Flask-Limiter
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["100 per hour"]
)

@app.route('/api/auth/login', methods=['POST'])
@limiter.limit("5 per minute")  # Max 5 login attempts per minute
def login():
    # ... login logic
```

---

## Monitoring / المراقبة

Monitor these metrics for security:

- **Failed login attempts** / محاولات تسجيل الدخول الفاشلة
- **Password change events** / أحداث تغيير كلمة المرور
- **Session creation/destruction** / إنشاء/إنهاء الجلسات
- **Unusual access patterns** / أنماط وصول غير عادية
- **API error rates** / معدلات أخطاء API

**Log Files:**
- `logs/security.log` - Security events
- `logs/audit.log` - Audit trail
- `logs/error.log` - Application errors

---

## Support / الدعم

For API support or questions:
- 📧 Email: api-support@university.edu.sa
- 📖 Documentation: See `PRODUCTION_DEPLOYMENT_GUIDE.md`
- 🔒 Security: See `SECURITY.md`

---

**Version:** 2.0.1  
**Last Updated:** 2025-11-17  
**Status:** ✅ Production Ready
