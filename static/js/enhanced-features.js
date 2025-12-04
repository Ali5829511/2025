/**
 * Enhanced Features JavaScript
 * ميزات JavaScript محسّنة للأداء والتفاعل
 */

// ========================================
// 1. TOAST NOTIFICATIONS SYSTEM
// ========================================

class ToastManager {
    constructor() {
        this.container = this.createContainer();
    }

    createContainer() {
        let container = document.querySelector('.toast-container');
        if (!container) {
            container = document.createElement('div');
            container.className = 'toast-container';
            document.body.appendChild(container);
        }
        return container;
    }

    show(message, type = 'info', duration = 3000) {
        const toast = document.createElement('div');
        toast.className = `toast ${type}`;
        
        const icons = {
            success: '✓',
            error: '✕',
            warning: '⚠',
            info: 'ℹ'
        };

        toast.innerHTML = `
            <div class="toast-icon">${icons[type] || icons.info}</div>
            <div class="toast-content">
                <div class="toast-message">${message}</div>
            </div>
            <button class="toast-close" onclick="this.parentElement.remove()">×</button>
        `;

        this.container.appendChild(toast);

        if (duration > 0) {
            setTimeout(() => {
                toast.style.animation = 'slideOutRight 0.3s ease-out';
                setTimeout(() => toast.remove(), 300);
            }, duration);
        }

        return toast;
    }

    success(message, duration) {
        return this.show(message, 'success', duration);
    }

    error(message, duration) {
        return this.show(message, 'error', duration);
    }

    warning(message, duration) {
        return this.show(message, 'warning', duration);
    }

    info(message, duration) {
        return this.show(message, 'info', duration);
    }
}

// إنشاء instance عالمي
window.toast = new ToastManager();

// ========================================
// 2. LOADING OVERLAY
// ========================================

class LoadingManager {
    constructor() {
        this.overlay = null;
    }

    show(message = 'جاري التحميل...') {
        if (this.overlay) return;

        this.overlay = document.createElement('div');
        this.overlay.className = 'loading-overlay';
        this.overlay.innerHTML = `
            <div style="text-align: center;">
                <div class="spinner"></div>
                <p style="margin-top: 16px; color: #6b7280;">${message}</p>
            </div>
        `;
        document.body.appendChild(this.overlay);
    }

    hide() {
        if (this.overlay) {
            this.overlay.remove();
            this.overlay = null;
        }
    }
}

window.loading = new LoadingManager();

// ========================================
// 3. MOBILE SIDEBAR TOGGLE
// ========================================

function initMobileSidebar() {
    // إنشاء زر القائمة للجوال
    if (window.innerWidth <= 768 && !document.querySelector('.mobile-menu-btn')) {
        const menuBtn = document.createElement('button');
        menuBtn.className = 'mobile-menu-btn';
        menuBtn.innerHTML = '<i class="fas fa-bars"></i>';
        menuBtn.onclick = toggleSidebar;
        document.body.appendChild(menuBtn);

        // إنشاء overlay
        const overlay = document.createElement('div');
        overlay.className = 'sidebar-overlay';
        overlay.onclick = toggleSidebar;
        document.body.appendChild(overlay);
    }
}

function toggleSidebar() {
    const sidebar = document.querySelector('.sidebar');
    const overlay = document.querySelector('.sidebar-overlay');
    
    if (sidebar && overlay) {
        sidebar.classList.toggle('active');
        overlay.classList.toggle('active');
    }
}

// ========================================
// 4. ENHANCED FORM VALIDATION
// ========================================

function validateForm(formElement) {
    const inputs = formElement.querySelectorAll('[required]');
    let isValid = true;

    inputs.forEach(input => {
        if (!input.value.trim()) {
            isValid = false;
            input.classList.add('is-invalid');
            toast.error(`الرجاء ملء حقل ${input.placeholder || input.name}`);
        } else {
            input.classList.remove('is-invalid');
        }
    });

    return isValid;
}

// ========================================
// 5. AJAX HELPER FUNCTIONS
// ========================================

async function fetchData(url, options = {}) {
    try {
        loading.show();
        const response = await fetch(url, {
            headers: {
                'Content-Type': 'application/json',
                ...options.headers
            },
            ...options
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();
        loading.hide();
        return data;
    } catch (error) {
        loading.hide();
        toast.error('حدث خطأ في الاتصال بالخادم');
        console.error('Fetch error:', error);
        throw error;
    }
}

// ========================================
// 6. TABLE ENHANCEMENTS
// ========================================

function makeTableResponsive(tableElement) {
    if (window.innerWidth <= 768) {
        tableElement.classList.add('mobile-table');
        
        // إضافة data-label لكل خلية
        const headers = Array.from(tableElement.querySelectorAll('thead th')).map(th => th.textContent);
        tableElement.querySelectorAll('tbody tr').forEach(row => {
            Array.from(row.querySelectorAll('td')).forEach((cell, index) => {
                cell.setAttribute('data-label', headers[index]);
            });
        });
    }
}

// تطبيق على جميع الجداول
function initResponsiveTables() {
    document.querySelectorAll('table').forEach(table => {
        if (!table.classList.contains('no-responsive')) {
            makeTableResponsive(table);
        }
    });
}

// ========================================
// 7. SEARCH AND FILTER
// ========================================

function initTableSearch(searchInputId, tableId) {
    const searchInput = document.getElementById(searchInputId);
    const table = document.getElementById(tableId);
    
    if (!searchInput || !table) return;

    searchInput.addEventListener('input', function() {
        const searchTerm = this.value.toLowerCase();
        const rows = table.querySelectorAll('tbody tr');
        
        rows.forEach(row => {
            const text = row.textContent.toLowerCase();
            row.style.display = text.includes(searchTerm) ? '' : 'none';
        });
    });
}

// ========================================
// 8. PULL TO REFRESH (للجوال)
// ========================================

function initPullToRefresh() {
    if (window.innerWidth > 768) return;

    let startY = 0;
    let currentY = 0;
    let pulling = false;

    document.addEventListener('touchstart', e => {
        if (window.scrollY === 0) {
            startY = e.touches[0].pageY;
            pulling = true;
        }
    });

    document.addEventListener('touchmove', e => {
        if (!pulling) return;
        currentY = e.touches[0].pageY;
        const diff = currentY - startY;
        
        if (diff > 80) {
            // تفعيل التحديث
            location.reload();
        }
    });

    document.addEventListener('touchend', () => {
        pulling = false;
    });
}

// ========================================
// 9. AUTO-SAVE FORMS
// ========================================

function initAutoSave(formId, storageKey) {
    const form = document.getElementById(formId);
    if (!form) return;

    // استعادة البيانات المحفوظة
    const saved = localStorage.getItem(storageKey);
    if (saved) {
        try {
            const data = JSON.parse(saved);
            Object.keys(data).forEach(key => {
                const input = form.querySelector(`[name="${key}"]`);
                if (input) input.value = data[key];
            });
        } catch (e) {
            console.error('Error loading saved data:', e);
        }
    }

    // حفظ تلقائي
    form.addEventListener('input', debounce(() => {
        const formData = new FormData(form);
        const data = {};
        formData.forEach((value, key) => {
            data[key] = value;
        });
        localStorage.setItem(storageKey, JSON.stringify(data));
    }, 500));

    // مسح البيانات عند الإرسال
    form.addEventListener('submit', () => {
        localStorage.removeItem(storageKey);
    });
}

// ========================================
// 10. UTILITY FUNCTIONS
// ========================================

// Debounce function
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// Format numbers
function formatNumber(num) {
    return new Intl.NumberFormat('ar-SA').format(num);
}

// Format dates
function formatDate(date) {
    return new Intl.DateTimeFormat('ar-SA', {
        year: 'numeric',
        month: 'long',
        day: 'numeric'
    }).format(new Date(date));
}

// Copy to clipboard
async function copyToClipboard(text) {
    try {
        await navigator.clipboard.writeText(text);
        toast.success('تم النسخ بنجاح');
    } catch (err) {
        toast.error('فشل النسخ');
    }
}

// Export table to CSV
function exportTableToCSV(tableId, filename = 'data.csv') {
    const table = document.getElementById(tableId);
    if (!table) return;

    let csv = [];
    const rows = table.querySelectorAll('tr');
    
    rows.forEach(row => {
        const cols = row.querySelectorAll('td, th');
        const rowData = Array.from(cols).map(col => {
            return '"' + col.textContent.replace(/"/g, '""') + '"';
        });
        csv.push(rowData.join(','));
    });

    const csvContent = csv.join('\n');
    const blob = new Blob(['\ufeff' + csvContent], { type: 'text/csv;charset=utf-8;' });
    const link = document.createElement('a');
    link.href = URL.createObjectURL(blob);
    link.download = filename;
    link.click();
    
    toast.success('تم تصدير البيانات بنجاح');
}

// Print page
function printPage() {
    window.print();
}

// ========================================
// 11. INITIALIZATION
// ========================================

document.addEventListener('DOMContentLoaded', function() {
    // تهيئة الميزات
    initMobileSidebar();
    initResponsiveTables();
    initPullToRefresh();

    // إضافة أحداث عامة
    document.querySelectorAll('form').forEach(form => {
        form.addEventListener('submit', function(e) {
            if (!validateForm(this)) {
                e.preventDefault();
            }
        });
    });

    // تحسين الأداء: lazy loading للصور
    if ('IntersectionObserver' in window) {
        const imageObserver = new IntersectionObserver((entries, observer) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const img = entry.target;
                    img.src = img.dataset.src;
                    img.classList.remove('lazy');
                    imageObserver.unobserve(img);
                }
            });
        });

        document.querySelectorAll('img[data-src]').forEach(img => {
            imageObserver.observe(img);
        });
    }

    console.log('✅ Enhanced features initialized');
});

// ========================================
// 12. PERFORMANCE MONITORING
// ========================================

if (window.performance) {
    window.addEventListener('load', () => {
        setTimeout(() => {
            const perfData = window.performance.timing;
            const pageLoadTime = perfData.loadEventEnd - perfData.navigationStart;
            console.log(`📊 Page load time: ${pageLoadTime}ms`);
        }, 0);
    });
}
