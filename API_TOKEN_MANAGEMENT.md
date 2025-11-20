# API Token Management Guide
# دليل إدارة رموز الوصول للواجهة البرمجية

## Overview | نظرة عامة

The API Token system provides secure, long-lived authentication tokens for external API access. Unlike session tokens, API tokens:
- Don't expire unless explicitly set
- Can be revoked at any time
- Track usage statistics
- Support fine-grained permissions

نظام رموز الوصول يوفر رموز مصادقة آمنة وطويلة الأجل للوصول الخارجي للواجهة البرمجية.

---

## Token Types | أنواع الرموز

### 1. Session Tokens | رموز الجلسة
- Created on login
- Short-lived (expire after inactivity)
- Used for web interface

### 2. API Tokens | رموز الوصول
- **Created manually by admins or users**
- Long-lived or permanent
- Used for external integrations
- **Format:** 64-character hexadecimal string
- **Reference:** 560a4728fc1f0fee1f76d1eb67f001d762a941d9 (example token format)

---

## API Endpoints | نقاط النهاية

### 1. List API Tokens

**Endpoint:** `GET /api/tokens`

**Authentication:** Required (session or API token)

**Response:**
```json
{
    "success": true,
    "tokens": [
        {
            "id": 1,
            "name": "Integration Token",
            "user_id": 1,
            "username": "admin",
            "user_role": "admin",
            "description": "For external system integration",
            "permissions": "read,write",
            "is_active": true,
            "is_expired": false,
            "last_used": "2025-11-20T10:30:00",
            "expires_at": null,
            "created_at": "2025-11-20T09:00:00"
        }
    ],
    "count": 1
}
```

**Permissions:**
- **Admin:** See all tokens
- **Other users:** See only their own tokens

---

### 2. Create API Token

**Endpoint:** `POST /api/tokens`

**Authentication:** Required

**Request Body:**
```json
{
    "name": "My Integration Token",
    "description": "For mobile app integration",
    "permissions": "read",
    "user_id": 1,
    "expires_days": 365
}
```

**Fields:**
- `name` (required): Token name/label
- `description` (optional): Token description
- `permissions` (optional): Comma-separated permissions (default: "read")
- `user_id` (optional): User ID (admin only, defaults to current user)
- `expires_days` (optional): Days until expiration (null = never expires)

**Response:**
```json
{
    "success": true,
    "token_id": 1,
    "token": "560a4728fc1f0fee1f76d1eb67f001d762a941d9a1b2c3d4e5f6789012345678",
    "token_hash": "...",
    "name": "My Integration Token",
    "permissions": "read",
    "expires_at": "2026-11-20T09:00:00",
    "message": "API token created successfully",
    "message_ar": "تم إنشاء رمز الوصول بنجاح",
    "warning": "Save this token now. You will not be able to see it again.",
    "warning_ar": "احفظ هذا الرمز الآن. لن تتمكن من رؤيته مرة أخرى."
}
```

⚠️ **Important:** The plain text token is returned only once. Save it securely!

---

### 3. Revoke API Token

**Endpoint:** `DELETE /api/tokens/{token_id}`

**Authentication:** Required

**Response:**
```json
{
    "success": true,
    "message": "API token revoked successfully",
    "message_ar": "تم إلغاء رمز الوصول بنجاح"
}
```

**Permissions:**
- **Token owner:** Can revoke their own tokens
- **Admin:** Can revoke any token

---

### 4. Token Usage Statistics

**Endpoint:** `GET /api/tokens/{token_id}/usage?days=30`

**Authentication:** Required

**Query Parameters:**
- `days` (optional): Number of days to look back (default: 30)

**Response:**
```json
{
    "success": true,
    "token_id": 1,
    "period_days": 30,
    "total_requests": 1250,
    "successful_requests": 1200,
    "failed_requests": 50,
    "avg_response_time_ms": 145.50,
    "endpoints": [
        {
            "endpoint": "/v1/plate-reader",
            "count": 1000
        },
        {
            "endpoint": "/api/parkpow/recognize",
            "count": 250
        }
    ]
}
```

---

## Using API Tokens | استخدام رموز الوصول

### Authentication Header

Include the token in the `Authorization` header:

```
Authorization: Token 560a4728fc1f0fee1f76d1eb67f001d762a941d9a1b2c3d4e5f6789012345678
```

or

```
Authorization: Bearer 560a4728fc1f0fee1f76d1eb67f001d762a941d9a1b2c3d4e5f6789012345678
```

### Example cURL Request

```bash
curl -X POST https://your-domain.com/v1/plate-reader \
  -H "Authorization: Token 560a4728fc1f0fee1f76d1eb67f001d762a941d9a1b2c3d4e5f6789012345678" \
  -H "Content-Type: application/json" \
  -d '{
    "image": "data:image/jpeg;base64,/9j/4AAQ...",
    "camera_id": "entrance_1"
  }'
```

### Python Example

```python
import requests

API_TOKEN = "560a4728fc1f0fee1f76d1eb67f001d762a941d9a1b2c3d4e5f6789012345678"

# Create API token
response = requests.post(
    'https://your-domain.com/api/tokens',
    headers={
        'Authorization': f'Token {API_TOKEN}',
        'Content-Type': 'application/json'
    },
    json={
        'name': 'Mobile App Token',
        'description': 'For iOS mobile app',
        'permissions': 'read'
    }
)

new_token = response.json()
print(f"New token: {new_token['token']}")

# Use the token for plate recognition
response = requests.post(
    'https://your-domain.com/v1/plate-reader',
    headers={
        'Authorization': f'Token {new_token["token"]}',
        'Content-Type': 'application/json'
    },
    json={
        'image': 'base64_encoded_image',
        'camera_id': 'entrance_1'
    }
)

print(response.json())
```

---

## Security Best Practices | أفضل الممارسات الأمنية

### 1. Token Storage | تخزين الرموز

- **Never commit tokens to version control**
- Store tokens in environment variables or secure vaults
- Use `.env` files for local development (add to `.gitignore`)

```bash
# .env file
API_TOKEN=560a4728fc1f0fee1f76d1eb67f001d762a941d9a1b2c3d4e5f6789012345678
```

### 2. Token Permissions | صلاحيات الرموز

- Use minimum required permissions
- Create separate tokens for different services
- Revoke tokens immediately when no longer needed

### 3. Token Expiration | انتهاء صلاحية الرموز

- Set expiration dates for tokens when possible
- Regularly rotate tokens (e.g., every 90 days)
- Monitor token usage for suspicious activity

### 4. Monitoring | المراقبة

- Regularly check token usage statistics
- Set up alerts for unusual activity
- Review and revoke inactive tokens

---

## Token Lifecycle | دورة حياة الرمز

```
1. Creation (إنشاء)
   ↓
2. Active Use (الاستخدام النشط)
   ↓
3. Monitoring (المراقبة)
   ↓
4. Expiration/Revocation (انتهاء الصلاحية/الإلغاء)
```

### States | الحالات

- **Active:** Token is valid and can be used
- **Inactive:** Token has been revoked
- **Expired:** Token has passed its expiration date

---

## Database Schema | مخطط قاعدة البيانات

### api_tokens Table

| Column | Type | Description |
|--------|------|-------------|
| id | INTEGER | Primary key |
| token | TEXT | SHA256 hash of the token |
| name | TEXT | Token name/label |
| user_id | INTEGER | Owner user ID |
| description | TEXT | Token description |
| permissions | TEXT | Comma-separated permissions |
| is_active | BOOLEAN | Active status |
| last_used | TIMESTAMP | Last usage timestamp |
| expires_at | TIMESTAMP | Expiration date |
| created_at | TIMESTAMP | Creation timestamp |
| created_by | INTEGER | Creator user ID |

### api_token_usage Table

| Column | Type | Description |
|--------|------|-------------|
| id | INTEGER | Primary key |
| token_id | INTEGER | Token ID (foreign key) |
| endpoint | TEXT | API endpoint accessed |
| method | TEXT | HTTP method |
| ip_address | TEXT | Client IP address |
| user_agent | TEXT | Client user agent |
| status_code | INTEGER | HTTP status code |
| request_time | TIMESTAMP | Request timestamp |
| response_time_ms | INTEGER | Response time in milliseconds |

---

## Troubleshooting | استكشاف الأخطاء

### Token Not Working

1. Check if token is active
2. Verify expiration date
3. Ensure correct format in Authorization header
4. Check user account is active

### Usage Not Being Logged

1. Verify token was created through the API
2. Check database connectivity
3. Review server logs for errors

### Permission Denied

1. Verify token permissions
2. Check user role
3. Ensure token hasn't been revoked

---

## Example Workflow | مثال سير العمل

### Setting Up an External Integration

1. **Admin creates API token:**
```bash
POST /api/tokens
{
  "name": "Mobile App Production",
  "description": "Token for production mobile app",
  "permissions": "read,write",
  "expires_days": 365
}
```

2. **Save the returned token securely**

3. **Configure the external system:**
```python
API_TOKEN = os.getenv('API_TOKEN')
headers = {'Authorization': f'Token {API_TOKEN}'}
```

4. **Monitor usage:**
```bash
GET /api/tokens/1/usage?days=7
```

5. **Rotate token before expiration:**
   - Create new token
   - Update external system configuration
   - Revoke old token

---

## Support | الدعم

For issues or questions about API tokens:
- Check server logs for detailed error messages
- Review token usage statistics
- Contact system administrator

للاستفسارات حول رموز الوصول:
- راجع سجلات الخادم للحصول على رسائل خطأ مفصلة
- راجع إحصائيات استخدام الرمز
- تواصل مع مدير النظام

---

## Changelog | سجل التغييرات

- **v1.0** (2025-11-20): Initial API token system implementation
  - Token creation and management
  - Usage tracking and statistics
  - Integration with `/v1/plate-reader` endpoint
  - Reference format: 560a4728fc1f0fee1f76d1eb67f001d762a941d9
