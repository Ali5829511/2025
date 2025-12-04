/**
 * Mobile Enhancements for Faculty Housing Management System
 * تحسينات الأجهزة المحمولة لنظام إدارة إسكان أعضاء هيئة التدريس
 */

// Detect device type
const isMobile = () => {
    return /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent);
};

const isTablet = () => {
    return /iPad|Android(?!.*Mobile)/i.test(navigator.userAgent);
};

const isDesktop = () => {
    return !isMobile() && !isTablet();
};

// Add device class to body
document.addEventListener('DOMContentLoaded', () => {
    if (isMobile()) {
        document.body.classList.add('is-mobile');
    } else if (isTablet()) {
        document.body.classList.add('is-tablet');
    } else {
        document.body.classList.add('is-desktop');
    }

    // Initialize mobile enhancements
    initMobileMenu();
    initTouchOptimizations();
    initPullToRefresh();
    initOrientationChange();
    initViewportOptimization();
});

/**
 * Mobile Menu Toggle
 */
function initMobileMenu() {
    const menuToggle = document.querySelector('.menu-toggle');
    const navMenu = document.querySelector('nav ul');

    if (menuToggle && navMenu) {
        menuToggle.addEventListener('click', () => {
            navMenu.classList.toggle('active');
            menuToggle.classList.toggle('active');
        });

        // Close menu when clicking on a link
        navMenu.querySelectorAll('a').forEach(link => {
            link.addEventListener('click', () => {
                navMenu.classList.remove('active');
                menuToggle.classList.remove('active');
            });
        });

        // Close menu when clicking outside
        document.addEventListener('click', (e) => {
            if (!e.target.closest('nav') && !e.target.closest('.menu-toggle')) {
                navMenu.classList.remove('active');
                menuToggle.classList.remove('active');
            }
        });
    }
}

/**
 * Touch Optimizations
 */
function initTouchOptimizations() {
    if (!isMobile()) return;

    // Increase touch target size for buttons
    const buttons = document.querySelectorAll('button, a.btn, .btn');
    buttons.forEach(button => {
        const style = window.getComputedStyle(button);
        const height = parseInt(style.height);
        if (height < 44) {
            button.style.minHeight = '44px';
            button.style.padding = '12px 20px';
        }
    });

    // Add touch feedback
    document.addEventListener('touchstart', function(e) {
        if (e.target.matches('button, a.btn, .btn, input, select, textarea')) {
            e.target.style.opacity = '0.8';
        }
    });

    document.addEventListener('touchend', function(e) {
        if (e.target.matches('button, a.btn, .btn, input, select, textarea')) {
            e.target.style.opacity = '1';
        }
    });
}

/**
 * Pull to Refresh
 */
function initPullToRefresh() {
    if (!isMobile()) return;

    let startY = 0;
    let currentY = 0;
    let pulling = false;

    document.addEventListener('touchstart', (e) => {
        if (window.scrollY === 0) {
            startY = e.touches[0].clientY;
            pulling = true;
        }
    });

    document.addEventListener('touchmove', (e) => {
        if (!pulling) return;

        currentY = e.touches[0].clientY;
        const diff = currentY - startY;

        if (diff > 100) {
            // Show pull to refresh indicator
            showPullToRefreshIndicator();
        }
    });

    document.addEventListener('touchend', () => {
        if (pulling && currentY - startY > 100) {
            location.reload();
        }
        pulling = false;
    });
}

/**
 * Show Pull to Refresh Indicator
 */
function showPullToRefreshIndicator() {
    let indicator = document.getElementById('pull-refresh-indicator');
    if (!indicator) {
        indicator = document.createElement('div');
        indicator.id = 'pull-refresh-indicator';
        indicator.style.cssText = `
            position: fixed;
            top: 10px;
            left: 50%;
            transform: translateX(-50%);
            background: #1e5a7d;
            color: white;
            padding: 10px 20px;
            border-radius: 20px;
            font-size: 12px;
            z-index: 999;
            animation: slideDown 0.3s ease;
        `;
        indicator.textContent = '↓ اسحب للتحديث';
        document.body.appendChild(indicator);

        setTimeout(() => {
            indicator.remove();
        }, 2000);
    }
}

/**
 * Orientation Change Handler
 */
function initOrientationChange() {
    window.addEventListener('orientationchange', () => {
        setTimeout(() => {
            // Adjust layout after orientation change
            const tables = document.querySelectorAll('table');
            tables.forEach(table => {
                if (table.offsetWidth > window.innerWidth) {
                    table.parentElement.classList.add('table-responsive');
                }
            });
        }, 100);
    });
}

/**
 * Viewport Optimization
 */
function initViewportOptimization() {
    // Ensure viewport meta tag exists
    let viewport = document.querySelector('meta[name="viewport"]');
    if (!viewport) {
        viewport = document.createElement('meta');
        viewport.name = 'viewport';
        viewport.content = 'width=device-width, initial-scale=1.0, maximum-scale=5.0, user-scalable=yes';
        document.head.appendChild(viewport);
    }

    // Prevent zoom on input focus (iOS)
    if (isMobile()) {
        const inputs = document.querySelectorAll('input, select, textarea');
        inputs.forEach(input => {
            input.addEventListener('focus', () => {
                viewport.content = 'width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no';
            });

            input.addEventListener('blur', () => {
                viewport.content = 'width=device-width, initial-scale=1.0, maximum-scale=5.0, user-scalable=yes';
            });
        });
    }
}

/**
 * Utility Functions
 */

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

// Throttle function
function throttle(func, limit) {
    let inThrottle;
    return function(...args) {
        if (!inThrottle) {
            func.apply(this, args);
            inThrottle = true;
            setTimeout(() => inThrottle = false, limit);
        }
    };
}

// Show loading indicator
function showLoading(message = 'جاري التحميل...') {
    let loader = document.getElementById('loading-indicator');
    if (!loader) {
        loader = document.createElement('div');
        loader.id = 'loading-indicator';
        loader.style.cssText = `
            position: fixed;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            background: white;
            padding: 30px;
            border-radius: 12px;
            box-shadow: 0 10px 40px rgba(0, 0, 0, 0.3);
            z-index: 1001;
            text-align: center;
        `;
        document.body.appendChild(loader);
    }

    loader.innerHTML = `
        <div class="spinner" style="margin: 0 auto 15px;"></div>
        <p>${message}</p>
    `;
    loader.style.display = 'block';
}

// Hide loading indicator
function hideLoading() {
    const loader = document.getElementById('loading-indicator');
    if (loader) {
        loader.style.display = 'none';
    }
}

// Show toast notification
function showToast(message, type = 'info', duration = 3000) {
    const toast = document.createElement('div');
    toast.className = `toast toast-${type}`;
    toast.style.cssText = `
        position: fixed;
        bottom: 20px;
        right: 20px;
        background: ${getToastColor(type)};
        color: white;
        padding: 15px 20px;
        border-radius: 8px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
        z-index: 1000;
        animation: slideUp 0.3s ease;
        max-width: 300px;
        word-wrap: break-word;
        direction: rtl;
    `;
    toast.textContent = message;
    document.body.appendChild(toast);

    setTimeout(() => {
        toast.style.animation = 'slideDown 0.3s ease';
        setTimeout(() => toast.remove(), 300);
    }, duration);
}

function getToastColor(type) {
    const colors = {
        'success': '#27ae60',
        'error': '#e74c3c',
        'warning': '#f39c12',
        'info': '#3498db'
    };
    return colors[type] || colors['info'];
}

// Add CSS animations
const style = document.createElement('style');
style.textContent = `
    @keyframes slideUp {
        from {
            transform: translateY(100px);
            opacity: 0;
        }
        to {
            transform: translateY(0);
            opacity: 1;
        }
    }

    @keyframes slideDown {
        from {
            transform: translateY(-100px);
            opacity: 0;
        }
        to {
            transform: translateY(0);
            opacity: 1;
        }
    }

    @keyframes spin {
        to {
            transform: rotate(360deg);
        }
    }

    .spinner {
        display: inline-block;
        width: 30px;
        height: 30px;
        border: 3px solid #f3f3f3;
        border-top: 3px solid #1e5a7d;
        border-radius: 50%;
        animation: spin 1s linear infinite;
    }
`;
document.head.appendChild(style);

// Export functions for use in other scripts
window.MobileEnhancements = {
    isMobile,
    isTablet,
    isDesktop,
    showLoading,
    hideLoading,
    showToast,
    debounce,
    throttle
};
