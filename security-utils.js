/**
 * Security Utilities for Faculty Housing Management System
 * أدوات الأمان لنظام إدارة إسكان أعضاء هيئة التدريس
 * 
 * This file provides security functions to prevent XSS and other vulnerabilities
 * يوفر هذا الملف دوال الأمان لمنع XSS والثغرات الأخرى
 */

/**
 * Escape HTML special characters to prevent XSS attacks
 * تعقيم الأحرف الخاصة لمنع هجمات XSS
 * 
 * @param {string} text - The text to escape
 * @returns {string} - The escaped text
 */
function escapeHtml(text) {
    if (text === null || text === undefined) {
        return '';
    }
    
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

/**
 * Sanitize user input by removing potentially dangerous characters
 * تعقيم مدخلات المستخدم بإزالة الأحرف الخطرة المحتملة
 * 
 * @param {string} input - The input to sanitize
 * @returns {string} - The sanitized input
 */
function sanitizeInput(input) {
    if (!input) return '';
    
    // Remove any HTML tags
    // إزالة أي وسوم HTML
    return input.replace(/<[^>]*>/g, '');
}

/**
 * Safely set text content in an element
 * تعيين محتوى نصي بشكل آمن في عنصر
 * 
 * @param {HTMLElement} element - The element to set text in
 * @param {string} text - The text to set
 */
function setSafeText(element, text) {
    if (!element) return;
    element.textContent = text || '';
}

/**
 * Safely set HTML content in an element (use with caution)
 * تعيين محتوى HTML بشكل آمن في عنصر (استخدم بحذر)
 * 
 * @param {HTMLElement} element - The element to set HTML in
 * @param {string} html - The HTML to set (should already be sanitized)
 */
function setSafeHtml(element, html) {
    if (!element) return;
    element.innerHTML = escapeHtml(html);
}

/**
 * Create a table row with safe data
 * إنشاء صف جدول مع بيانات آمنة
 * 
 * @param {Array} columns - Array of column data
 * @returns {HTMLTableRowElement} - The created row
 */
function createSafeTableRow(columns) {
    const row = document.createElement('tr');
    
    columns.forEach(columnData => {
        const cell = document.createElement('td');
        
        if (typeof columnData === 'object' && columnData.html) {
            // If HTML is explicitly needed, use it (should be pre-sanitized)
            // إذا كان HTML مطلوب بشكل صريح، استخدمه (يجب أن يكون معقماً مسبقاً)
            cell.innerHTML = columnData.html;
        } else {
            // Otherwise, use safe text content
            // وإلا، استخدم محتوى نصي آمن
            cell.textContent = columnData;
        }
        
        row.appendChild(cell);
    });
    
    return row;
}

/**
 * Validate and sanitize URL to prevent javascript: protocol
 * التحقق من صحة وتعقيم URL لمنع بروتوكول javascript:
 * 
 * @param {string} url - The URL to validate
 * @returns {string} - The sanitized URL or empty string if invalid
 */
function sanitizeUrl(url) {
    if (!url) return '';
    
    // Remove leading/trailing whitespace
    // إزالة المسافات البادئة/الزائدة
    url = url.trim();
    
    // Check for dangerous protocols
    // التحقق من البروتوكولات الخطرة
    const dangerousProtocols = ['javascript:', 'data:', 'vbscript:'];
    const lowerUrl = url.toLowerCase();
    
    for (const protocol of dangerousProtocols) {
        if (lowerUrl.startsWith(protocol)) {
            console.warn('Dangerous URL protocol detected:', url);
            return '';
        }
    }
    
    return url;
}

/**
 * Validate phone number format (Saudi format)
 * التحقق من صحة تنسيق رقم الهاتف (تنسيق سعودي)
 * 
 * @param {string} phone - The phone number to validate
 * @returns {boolean} - True if valid, false otherwise
 */
function validatePhone(phone) {
    if (!phone) return false;
    
    // Saudi phone format: 05XXXXXXXX or +9665XXXXXXXX
    // تنسيق الهاتف السعودي
    const phoneRegex = /^(05\d{8}|(\+?966)?5\d{8})$/;
    return phoneRegex.test(phone.replace(/\s/g, ''));
}

/**
 * Validate email format
 * التحقق من صحة تنسيق البريد الإلكتروني
 * 
 * @param {string} email - The email to validate
 * @returns {boolean} - True if valid, false otherwise
 */
function validateEmail(email) {
    if (!email) return false;
    
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
}

/**
 * Validate national ID format (Saudi format)
 * التحقق من صحة تنسيق رقم الهوية (تنسيق سعودي)
 * 
 * @param {string} nationalId - The national ID to validate
 * @returns {boolean} - True if valid, false otherwise
 */
function validateNationalId(nationalId) {
    if (!nationalId) return false;
    
    // Saudi national ID is 10 digits starting with 1 or 2
    // رقم الهوية السعودي 10 أرقام يبدأ بـ 1 أو 2
    const idRegex = /^[12]\d{9}$/;
    return idRegex.test(nationalId);
}

/**
 * Validate license plate format (Saudi format)
 * التحقق من صحة تنسيق لوحة السيارة (تنسيق سعودي)
 * 
 * @param {string} plate - The license plate to validate
 * @returns {boolean} - True if valid, false otherwise
 */
function validateLicensePlate(plate) {
    if (!plate) return false;
    
    // Saudi format: 3-4 digits followed by 1-3 Arabic letters
    // التنسيق السعودي: 3-4 أرقام متبوعة بـ 1-3 حروف عربية
    // Example: 1234 أ ب ج or 123 أ ب
    const plateRegex = /^[\u0600-\u06FF\s]*\d{3,4}[\u0600-\u06FF\s]+$/;
    return plateRegex.test(plate) || /^\d{1,4}\s*[A-Z]{1,3}$/.test(plate);
}

/**
 * Format date to Arabic/English format
 * تنسيق التاريخ إلى صيغة عربية/إنجليزية
 * 
 * @param {Date|string} date - The date to format
 * @param {string} locale - The locale ('ar' or 'en')
 * @returns {string} - The formatted date
 */
function formatDate(date, locale = 'ar') {
    if (!date) return '';
    
    const dateObj = date instanceof Date ? date : new Date(date);
    
    if (isNaN(dateObj.getTime())) return '';
    
    const options = {
        year: 'numeric',
        month: '2-digit',
        day: '2-digit'
    };
    
    return dateObj.toLocaleDateString(locale === 'ar' ? 'ar-SA' : 'en-US', options);
}

/**
 * Format currency to Saudi Riyal
 * تنسيق العملة إلى ريال سعودي
 * 
 * @param {number} amount - The amount to format
 * @returns {string} - The formatted amount
 */
function formatCurrency(amount) {
    if (amount === null || amount === undefined || isNaN(amount)) return '0.00 ريال';
    
    return new Intl.NumberFormat('ar-SA', {
        style: 'currency',
        currency: 'SAR',
        minimumFractionDigits: 2
    }).format(amount);
}

/**
 * Show a safe alert message
 * عرض رسالة تنبيه آمنة
 * 
 * @param {string} message - The message to show
 * @param {string} type - The alert type ('success', 'error', 'warning', 'info')
 */
function showSafeAlert(message, type = 'info') {
    // Create alert element
    // إنشاء عنصر التنبيه
    const alert = document.createElement('div');
    alert.className = `alert alert-${type}`;
    alert.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        padding: 15px 20px;
        border-radius: 5px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.2);
        z-index: 10000;
        max-width: 400px;
        animation: slideIn 0.3s ease-out;
    `;
    
    // Set safe text content
    // تعيين محتوى نصي آمن
    alert.textContent = message;
    
    // Add to body
    // إضافة إلى الصفحة
    document.body.appendChild(alert);
    
    // Auto remove after 5 seconds
    // إزالة تلقائية بعد 5 ثواني
    setTimeout(() => {
        alert.style.animation = 'slideOut 0.3s ease-in';
        setTimeout(() => alert.remove(), 300);
    }, 5000);
}

// Add CSS for animations
// إضافة CSS للحركات
const style = document.createElement('style');
style.textContent = `
    @keyframes slideIn {
        from {
            transform: translateX(100%);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
    
    @keyframes slideOut {
        from {
            transform: translateX(0);
            opacity: 1;
        }
        to {
            transform: translateX(100%);
            opacity: 0;
        }
    }
    
    .alert {
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        direction: rtl;
        text-align: right;
    }
    
    .alert-success {
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        color: #155724;
    }
    
    .alert-error, .alert-danger {
        background-color: #f8d7da;
        border: 1px solid #f5c6cb;
        color: #721c24;
    }
    
    .alert-warning {
        background-color: #fff3cd;
        border: 1px solid #ffeaa7;
        color: #856404;
    }
    
    .alert-info {
        background-color: #d1ecf1;
        border: 1px solid #bee5eb;
        color: #0c5460;
    }
`;
document.head.appendChild(style);

// Export functions for use in other scripts
// تصدير الدوال للاستخدام في سكريبتات أخرى
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        escapeHtml,
        sanitizeInput,
        setSafeText,
        setSafeHtml,
        createSafeTableRow,
        sanitizeUrl,
        validatePhone,
        validateEmail,
        validateNationalId,
        validateLicensePlate,
        formatDate,
        formatCurrency,
        showSafeAlert
    };
}
