# Plate Reader API v1 Documentation
# دليل واجهة برمجة تمييز اللوحات الإصدار 1

## Overview | نظرة عامة

Django REST framework compatible API endpoint for license plate recognition from images.

واجهة برمجية متوافقة مع Django REST framework لتمييز لوحات المركبات من الصور.

---

## Endpoint | نقطة النهاية

```
/v1/plate-reader
```

### Supported Methods | الطرق المدعومة

- **GET** - Get API information and status
- **POST** - Submit image for plate recognition
- **HEAD** - Get headers only
- **OPTIONS** - CORS preflight

---

## Authentication | المصادقة

All requests require authentication via the `Authorization` header:

```
Authorization: Token <your-api-token>
```

or

```
Authorization: Bearer <your-api-token>
```

### Getting a Token | الحصول على رمز الدخول

1. Login to the system with your credentials
2. Your authentication token will be provided
3. Include it in all API requests

### Authentication Errors | أخطاء المصادقة

If authentication fails, you'll receive:

```json
{
    "detail": "Authentication credentials were not provided.",
    "status_code": 403
}
```

---

## GET Request | طلب GET

Returns API information and capabilities.

### Example Request | مثال الطلب

```bash
curl -X GET https://your-domain.com/v1/plate-reader \
  -H "Authorization: Token YOUR_TOKEN_HERE"
```

### Example Response | مثال الاستجابة

```json
{
    "status": "active",
    "version": "v1",
    "endpoint": "/v1/plate-reader",
    "methods": ["GET", "POST"],
    "description": "Image Plate Reader API",
    "description_ar": "واجهة برمجية لتمييز لوحات المركبات من الصور",
    "authentication": "Token required in Authorization header",
    "post_format": {
        "image": "Base64 encoded image string or image URL",
        "camera_id": "Optional camera identifier"
    },
    "response_format": {
        "success": "boolean",
        "results": "array of detected plates",
        "message": "status message"
    }
}
```

---

## POST Request | طلب POST

Submit an image for license plate recognition.

### Request Body | محتوى الطلب

```json
{
    "image": "base64_encoded_image_data_or_url",
    "camera_id": "optional_camera_identifier"
}
```

#### Fields | الحقول

- **image** (required): Base64 encoded image string or image URL
- **camera_id** (optional): Identifier for the camera that captured the image

### Example Request | مثال الطلب

```bash
curl -X POST https://your-domain.com/v1/plate-reader \
  -H "Authorization: Token YOUR_TOKEN_HERE" \
  -H "Content-Type: application/json" \
  -d '{
    "image": "data:image/jpeg;base64,/9j/4AAQSkZJRg...",
    "camera_id": "entrance_gate_1"
  }'
```

### Success Response | استجابة النجاح

**Status Code:** 200 OK

```json
{
    "success": true,
    "message": "Plate recognized successfully",
    "message_ar": "تم تمييز اللوحة بنجاح",
    "results": [
        {
            "plate": "ABC1234",
            "plate_number": "ABC1234",
            "confidence": 0.95,
            "region": "SA",
            "vehicle_info": {
                "id": 123,
                "plate_number": "ABC1234",
                "vehicle_type": "سيدان",
                "make": "تويوتا",
                "model": "كامري",
                "color": "أبيض",
                "owner_name": "محمد أحمد",
                "unit_number": "A-101",
                "building_name": "مبنى A",
                "owner_phone": "+966501234567"
            }
        }
    ]
}
```

### Error Responses | استجابات الخطأ

#### 400 Bad Request

```json
{
    "detail": "Image field is required",
    "status_code": 400
}
```

#### 403 Forbidden

```json
{
    "detail": "Authentication credentials were not provided.",
    "status_code": 403
}
```

#### 500 Internal Server Error

```json
{
    "detail": "Internal server error during plate recognition",
    "status_code": 500
}
```

---

## Response Fields | حقول الاستجابة

### Plate Recognition Result | نتيجة تمييز اللوحة

| Field | Type | Description |
|-------|------|-------------|
| `success` | boolean | Whether recognition succeeded |
| `message` | string | Status message in English |
| `message_ar` | string | Status message in Arabic |
| `results` | array | Array of detected plates |

### Plate Data Object | بيانات اللوحة

| Field | Type | Description |
|-------|------|-------------|
| `plate` | string | Detected plate number |
| `plate_number` | string | Detected plate number (duplicate) |
| `confidence` | float | Recognition confidence (0.0-1.0) |
| `region` | string | Region/country code |
| `vehicle_info` | object | Vehicle and owner information (if found in database) |

### Vehicle Info Object | معلومات المركبة

| Field | Type | Description |
|-------|------|-------------|
| `id` | integer | Vehicle database ID |
| `plate_number` | string | Registered plate number |
| `vehicle_type` | string | Type of vehicle |
| `make` | string | Vehicle manufacturer |
| `model` | string | Vehicle model |
| `color` | string | Vehicle color |
| `owner_name` | string | Owner's name |
| `unit_number` | string | Residential unit number |
| `building_name` | string | Building name |
| `owner_phone` | string | Owner's contact phone |

---

## Rate Limiting | حد المعدل

Currently no rate limiting is enforced. Please use the API responsibly.

حاليًا لا يوجد حد لمعدل الاستخدام. يرجى استخدام الواجهة بمسؤولية.

---

## CORS Support | دعم CORS

The API supports CORS for cross-origin requests. Preflight OPTIONS requests are handled automatically.

---

## Integration Example | مثال التكامل

### Python Example | مثال بايثون

```python
import requests
import base64

# Read and encode image
with open('car_image.jpg', 'rb') as f:
    image_data = base64.b64encode(f.read()).decode('utf-8')
    image_base64 = f'data:image/jpeg;base64,{image_data}'

# Make API request
response = requests.post(
    'https://your-domain.com/v1/plate-reader',
    headers={
        'Authorization': 'Token YOUR_TOKEN_HERE',
        'Content-Type': 'application/json'
    },
    json={
        'image': image_base64,
        'camera_id': 'entrance_gate_1'
    }
)

# Process response
if response.status_code == 200:
    data = response.json()
    if data['success']:
        for result in data['results']:
            print(f"Detected plate: {result['plate']}")
            print(f"Confidence: {result['confidence']}")
            if result['vehicle_info']:
                print(f"Owner: {result['vehicle_info']['owner_name']}")
else:
    print(f"Error: {response.json()['detail']}")
```

### JavaScript Example | مثال جافاسكربت

```javascript
// Convert image file to base64
function imageToBase64(file) {
    return new Promise((resolve, reject) => {
        const reader = new FileReader();
        reader.onload = () => resolve(reader.result);
        reader.onerror = reject;
        reader.readAsDataURL(file);
    });
}

// Make API request
async function recognizePlate(imageFile, cameraId) {
    const imageBase64 = await imageToBase64(imageFile);
    
    const response = await fetch('https://your-domain.com/v1/plate-reader', {
        method: 'POST',
        headers: {
            'Authorization': 'Token YOUR_TOKEN_HERE',
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            image: imageBase64,
            camera_id: cameraId
        })
    });
    
    const data = await response.json();
    
    if (response.ok && data.success) {
        data.results.forEach(result => {
            console.log(`Detected plate: ${result.plate}`);
            console.log(`Confidence: ${result.confidence}`);
            if (result.vehicle_info) {
                console.log(`Owner: ${result.vehicle_info.owner_name}`);
            }
        });
    } else {
        console.error(`Error: ${data.detail}`);
    }
}
```

---

## Notes | ملاحظات

1. **Image Format**: Supports JPEG, PNG, and other common image formats
2. **Image Size**: Recommended maximum size is 10MB
3. **Base64 Encoding**: Include the data URI prefix (e.g., `data:image/jpeg;base64,`)
4. **Response Time**: Typical response time is 1-3 seconds depending on image size
5. **Logging**: All API requests are logged for audit purposes

---

## Support | الدعم

For issues or questions, contact the system administrator.

للاستفسارات أو المشاكل، يرجى التواصل مع مدير النظام.

---

## Version History | سجل الإصدارات

- **v1.0** (2025-11-20): Initial release with GET and POST support
