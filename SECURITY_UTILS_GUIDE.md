# دليل استخدام أدوات الأمان
# Security Utilities Usage Guide

**التاريخ / Date:** 2025-11-05  
**الملفات / Files:** security-utils.js, security-utils.css

---

## نظرة عامة / Overview

توفر مكتبة أدوات الأمان مجموعة من الدوال لحماية التطبيق من:
- هجمات XSS (Cross-Site Scripting)
- حقن HTML
- مدخلات المستخدم غير الآمنة

The security utilities library provides functions to protect the application from:
- XSS (Cross-Site Scripting) attacks
- HTML injection
- Unsafe user input

---

## التثبيت / Installation

### 1. إضافة الملفات إلى HTML / Add Files to HTML

```html
<!DOCTYPE html>
<html dir="rtl" lang="ar">
<head>
    <!-- ... -->
    
    <!-- Security Utilities CSS -->
    <link rel="stylesheet" href="security-utils.css">
    
    <!-- Security Utilities JS -->
    <script src="security-utils.js"></script>
</head>
<body>
    <!-- ... -->
</body>
</html>
```

---

## الدوال المتاحة / Available Functions

### 1. تعقيم النصوص / Text Sanitization

#### `escapeHtml(text)`

تعقيم النصوص من أحرف HTML الخاصة.  
Escape HTML special characters.

```javascript
// ❌ غير آمن / Unsafe
element.innerHTML = userInput;

// ✅ آمن / Safe
element.innerHTML = escapeHtml(userInput);

// مثال / Example
const userName = '<script>alert("XSS")</script>';
element.innerHTML = escapeHtml(userName);
// النتيجة / Result: &lt;script&gt;alert("XSS")&lt;/script&gt;
```

#### `sanitizeInput(input)`

إزالة جميع وسوم HTML من المدخلات.  
Remove all HTML tags from input.

```javascript
const dirtyInput = 'Hello <b>World</b> <script>alert("XSS")</script>';
const cleanInput = sanitizeInput(dirtyInput);
console.log(cleanInput); // "Hello World "
```

---

### 2. تعيين المحتوى بأمان / Safe Content Setting

#### `setSafeText(element, text)`

تعيين محتوى نصي آمن (مستحسن).  
Set safe text content (recommended).

```javascript
// ❌ غير آمن / Unsafe
element.innerHTML = userData;

// ✅ آمن / Safe
setSafeText(element, userData);

// مثال / Example
const nameCell = document.getElementById('userName');
setSafeText(nameCell, user.name);
```

#### `setSafeHtml(element, html, escape)`

تعيين محتوى HTML (استخدم بحذر).  
Set HTML content (use with caution).

```javascript
// للمحتوى المعقم مسبقاً / For pre-sanitized content
setSafeHtml(element, trustedHtml, false);

// لتعقيم وتعيين / To sanitize and set
setSafeHtml(element, untrustedHtml, true);
```

---

### 3. إنشاء صفوف الجدول بأمان / Safe Table Row Creation

#### `createSafeTableRow(columns)`

إنشاء صف جدول مع بيانات معقمة.  
Create table row with sanitized data.

```javascript
// ❌ غير آمن / Unsafe
row.innerHTML = `
    <td>${user.name}</td>
    <td>${user.email}</td>
`;

// ✅ آمن / Safe
const row = createSafeTableRow([
    user.name,
    user.email,
    { html: `<button onclick="edit(${user.id})">تعديل</button>` }
]);
tbody.appendChild(row);
```

**مثال كامل / Complete Example:**

```javascript
function loadUsers(users) {
    const tbody = document.getElementById('usersTableBody');
    tbody.innerHTML = '';

    users.forEach(user => {
        const row = createSafeTableRow([
            user.username,
            user.fullName,
            user.email,
            { html: `
                <button class="btn btn-warning" onclick="editUser(${user.id})">
                    <i class="fas fa-edit"></i> تعديل
                </button>
                <button class="btn btn-danger" onclick="deleteUser(${user.id})">
                    <i class="fas fa-trash"></i> حذف
                </button>
            ` }
        ]);
        tbody.appendChild(row);
    });
}
```

---

### 4. التحقق من صحة البيانات / Data Validation

#### `validatePhone(phone)`

التحقق من صحة رقم الهاتف السعودي.  
Validate Saudi phone number.

```javascript
// أمثلة صحيحة / Valid examples
validatePhone('0512345678');        // true
validatePhone('966512345678');      // true
validatePhone('+966512345678');     // true

// أمثلة خاطئة / Invalid examples
validatePhone('1234567890');        // false
validatePhone('05123');             // false
```

#### `validateEmail(email)`

التحقق من صحة البريد الإلكتروني.  
Validate email format.

```javascript
validateEmail('user@university.edu.sa');  // true
validateEmail('invalid-email');           // false
```

#### `validateNationalId(nationalId)`

التحقق من صحة رقم الهوية السعودي.  
Validate Saudi national ID.

```javascript
validateNationalId('1234567890');  // true
validateNationalId('2234567890');  // true
validateNationalId('3234567890');  // false (يجب أن يبدأ بـ 1 أو 2)
```

#### `validateLicensePlate(plate)`

التحقق من صحة لوحة السيارة.  
Validate license plate format.

```javascript
validateLicensePlate('1234 أ ب ج');  // true
validateLicensePlate('123 أ ب');     // true
validateLicensePlate('1234 ABC');    // true
validateLicensePlate('abc123');      // false
```

---

### 5. التنسيق / Formatting

#### `formatDate(date, locale)`

تنسيق التاريخ.  
Format date.

```javascript
const date = new Date('2025-11-05');

formatDate(date, 'ar');  // "٠٥/١١/٢٠٢٥"
formatDate(date, 'en');  // "11/05/2025"
```

#### `formatCurrency(amount)`

تنسيق المبلغ المالي بالريال السعودي.  
Format currency in Saudi Riyal.

```javascript
formatCurrency(1500);      // "١٬٥٠٠٫٠٠ ر.س."
formatCurrency(1234.56);   // "١٬٢٣٤٫٥٦ ر.س."
```

---

### 6. عرض الرسائل / Display Messages

#### `showSafeAlert(message, type)`

عرض رسالة تنبيه آمنة.  
Display safe alert message.

```javascript
// أنواع التنبيهات / Alert types:
showSafeAlert('تم الحفظ بنجاح', 'success');
showSafeAlert('حدث خطأ', 'error');
showSafeAlert('تحذير: تحقق من البيانات', 'warning');
showSafeAlert('معلومة: النظام قيد التحديث', 'info');
```

**خصائص / Features:**
- عرض تلقائي لمدة 5 ثواني
- Auto-display for 5 seconds
- حركة انسيابية (slide in/out)
- Smooth animation (slide in/out)
- موضع ثابت أعلى اليمين
- Fixed position top-right

---

## أمثلة عملية / Practical Examples

### مثال 1: نموذج إضافة مستخدم / Add User Form

```javascript
function addUser() {
    // الحصول على البيانات من النموذج
    // Get data from form
    const username = document.getElementById('username').value;
    const fullName = document.getElementById('fullName').value;
    const email = document.getElementById('email').value;
    const phone = document.getElementById('phone').value;
    
    // التحقق من صحة البيانات
    // Validate data
    if (!validateEmail(email)) {
        showSafeAlert('البريد الإلكتروني غير صحيح', 'error');
        return;
    }
    
    if (!validatePhone(phone)) {
        showSafeAlert('رقم الهاتف غير صحيح', 'error');
        return;
    }
    
    // تعقيم البيانات
    // Sanitize data
    const cleanData = {
        username: sanitizeInput(username),
        fullName: sanitizeInput(fullName),
        email: sanitizeInput(email),
        phone: sanitizeInput(phone)
    };
    
    // حفظ البيانات
    // Save data
    saveUser(cleanData);
    
    showSafeAlert('تم إضافة المستخدم بنجاح', 'success');
}
```

### مثال 2: عرض بيانات الجدول / Display Table Data

```javascript
function displayResidents(residents) {
    const tbody = document.getElementById('residentsTable');
    tbody.innerHTML = '';
    
    residents.forEach(resident => {
        const row = createSafeTableRow([
            resident.name,
            resident.nationalId,
            formatPhone(resident.phone),
            resident.building + ' - ' + resident.apartment,
            formatDate(resident.moveInDate, 'ar'),
            { html: `
                <button class="btn btn-primary" onclick="viewResident(${resident.id})">
                    عرض
                </button>
                <button class="btn btn-warning" onclick="editResident(${resident.id})">
                    تعديل
                </button>
            ` }
        ]);
        tbody.appendChild(row);
    });
}
```

### مثال 3: بحث مع عرض نتائج آمنة / Search with Safe Results

```javascript
function searchResidents(query) {
    // تعقيم استعلام البحث
    // Sanitize search query
    const cleanQuery = sanitizeInput(query);
    
    // البحث
    // Search
    const results = performSearch(cleanQuery);
    
    // عرض النتائج بأمان
    // Display results safely
    const resultsDiv = document.getElementById('searchResults');
    resultsDiv.innerHTML = '';
    
    if (results.length === 0) {
        setSafeText(resultsDiv, 'لا توجد نتائج');
        return;
    }
    
    results.forEach(result => {
        const item = document.createElement('div');
        item.className = 'search-result-item';
        setSafeText(item, result.name + ' - ' + result.apartment);
        item.onclick = () => viewResident(result.id);
        resultsDiv.appendChild(item);
    });
}
```

---

## قائمة فحص الأمان / Security Checklist

عند كتابة كود JavaScript جديد، تحقق من:  
When writing new JavaScript code, check:

- [ ] ✅ استخدام `setSafeText()` بدلاً من `innerHTML` للنصوص
- [ ] ✅ Use `setSafeText()` instead of `innerHTML` for text
- [ ] ✅ تعقيم جميع مدخلات المستخدم
- [ ] ✅ Sanitize all user input
- [ ] ✅ التحقق من صحة البيانات قبل الحفظ
- [ ] ✅ Validate data before saving
- [ ] ✅ استخدام `createSafeTableRow()` لصفوف الجدول
- [ ] ✅ Use `createSafeTableRow()` for table rows
- [ ] ✅ عدم تنفيذ كود من مصادر غير موثوقة
- [ ] ✅ Never execute code from untrusted sources

---

## الترقية من الكود القديم / Upgrading from Old Code

### قبل / Before:
```javascript
// ❌ غير آمن
function loadUsers(users) {
    const tbody = document.getElementById('usersTableBody');
    tbody.innerHTML = '';

    users.forEach(user => {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td>${user.username}</td>
            <td>${user.fullName}</td>
            <td>${user.email}</td>
        `;
        tbody.appendChild(row);
    });
}
```

### بعد / After:
```javascript
// ✅ آمن
function loadUsers(users) {
    const tbody = document.getElementById('usersTableBody');
    tbody.innerHTML = '';

    users.forEach(user => {
        const row = createSafeTableRow([
            user.username,
            user.fullName,
            user.email
        ]);
        tbody.appendChild(row);
    });
}
```

---

## الدعم / Support

للمساعدة أو الإبلاغ عن مشكلات:  
For help or to report issues:

- مراجعة الملف: COMPREHENSIVE_REVIEW_REPORT.md
- Review file: COMPREHENSIVE_REVIEW_REPORT.md
- فريق تقنية المعلومات
- IT Team

---

**آخر تحديث / Last Updated:** 2025-11-05  
**الإصدار / Version:** 1.0
