#!/bin/bash
# ==============================================================================
# File Permissions Setup Script - سكريبت إعداد صلاحيات الملفات
# ==============================================================================
# Set secure file permissions for production deployment
# تعيين صلاحيات آمنة للملفات للنشر الإنتاجي
# ==============================================================================

set -e  # Exit on error

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if running as root
if [ "$EUID" -eq 0 ]; then 
    log_warn "Running as root. Be careful with permissions."
    log_warn "تعمل كمستخدم جذر. كن حذراً مع الصلاحيات."
fi

# Get application directory
APP_DIR="${1:-$(pwd)}"
cd "$APP_DIR" || exit 1

log_info "========================================"
log_info "Setting File Permissions"
log_info "تعيين صلاحيات الملفات"
log_info "Directory: $APP_DIR"
log_info "========================================"

# Set ownership (if running as root)
# تعيين الملكية (إذا كنت تعمل كمستخدم جذر)
if [ "$EUID" -eq 0 ]; then
    APP_USER="${APP_USER:-www-data}"
    APP_GROUP="${APP_GROUP:-www-data}"
    
    log_info "Setting ownership to $APP_USER:$APP_GROUP"
    log_info "تعيين الملكية إلى $APP_USER:$APP_GROUP"
    chown -R "$APP_USER:$APP_GROUP" "$APP_DIR" || log_warn "Could not change ownership"
fi

# Set directory permissions / صلاحيات المجلدات
log_info "Setting directory permissions..."
log_info "تعيين صلاحيات المجلدات..."
find "$APP_DIR" -type d -exec chmod 755 {} \; 2>/dev/null || log_warn "Some directory permissions could not be set"

# Set Python file permissions / صلاحيات ملفات Python
log_info "Setting Python file permissions (644)..."
log_info "تعيين صلاحيات ملفات Python (644)..."
find "$APP_DIR" -type f -name "*.py" -exec chmod 644 {} \; 2>/dev/null || log_warn "Some Python file permissions could not be set"

# Set shell script permissions / صلاحيات سكريبتات Shell
log_info "Setting shell script permissions (755)..."
log_info "تعيين صلاحيات سكريبتات Shell (755)..."
find "$APP_DIR" -type f -name "*.sh" -exec chmod 755 {} \; 2>/dev/null || log_warn "Some script permissions could not be set"

# Set sensitive file permissions / صلاحيات الملفات الحساسة
log_info "Setting sensitive file permissions (600)..."
log_info "تعيين صلاحيات الملفات الحساسة (600)..."

# Environment files
for env_file in .env .env.* config/*.conf; do
    if [ -f "$env_file" ]; then
        chmod 600 "$env_file" 2>/dev/null && log_info "  ✓ $env_file" || log_warn "  ✗ $env_file"
    fi
done

# Database files / ملفات قاعدة البيانات
log_info "Setting database file permissions (660)..."
log_info "تعيين صلاحيات ملفات قاعدة البيانات (660)..."
for db_file in *.db; do
    if [ -f "$db_file" ]; then
        chmod 660 "$db_file" 2>/dev/null && log_info "  ✓ $db_file" || log_warn "  ✗ $db_file"
    fi
done

# Upload directories / مجلدات التحميل
log_info "Setting upload directory permissions..."
log_info "تعيين صلاحيات مجلدات التحميل..."
for upload_dir in uploads uploads/* static/uploads static/uploads/*; do
    if [ -d "$upload_dir" ]; then
        chmod 755 "$upload_dir" 2>/dev/null && log_info "  ✓ $upload_dir (755)" || log_warn "  ✗ $upload_dir"
    fi
done

# Files in upload directories
find uploads/ static/uploads/ -type f -exec chmod 644 {} \; 2>/dev/null || log_warn "Could not set upload file permissions"

# Log directories / مجلدات السجلات
if [ -d "logs" ]; then
    log_info "Setting log directory permissions..."
    log_info "تعيين صلاحيات مجلد السجلات..."
    chmod 755 logs/ 2>/dev/null || log_warn "Could not set log directory permissions"
    find logs/ -type f -exec chmod 640 {} \; 2>/dev/null || log_warn "Could not set log file permissions"
fi

# Backup directory / مجلد النسخ الاحتياطية
if [ -d "backups" ]; then
    log_info "Setting backup directory permissions..."
    log_info "تعيين صلاحيات مجلد النسخ الاحتياطية..."
    chmod 700 backups/ 2>/dev/null || log_warn "Could not set backup directory permissions"
    find backups/ -type f -exec chmod 600 {} \; 2>/dev/null || log_warn "Could not set backup file permissions"
fi

# Static files / الملفات الثابتة
log_info "Setting static file permissions..."
log_info "تعيين صلاحيات الملفات الثابتة..."
find static/ -type f -exec chmod 644 {} \; 2>/dev/null || log_warn "Could not set static file permissions"

# HTML/CSS/JS files
find . -type f \( -name "*.html" -o -name "*.css" -o -name "*.js" \) -exec chmod 644 {} \; 2>/dev/null || log_warn "Could not set web file permissions"

# Documentation files
find . -type f \( -name "*.md" -o -name "*.txt" \) -exec chmod 644 {} \; 2>/dev/null || log_warn "Could not set documentation permissions"

# Remove write permissions from configuration files
log_info "Securing configuration files..."
log_info "تأمين ملفات التكوين..."
for config_file in gunicorn_config.py nginx.conf *.yaml *.yml; do
    if [ -f "$config_file" ]; then
        chmod 644 "$config_file" 2>/dev/null && log_info "  ✓ $config_file" || log_warn "  ✗ $config_file"
    fi
done

# Set execute permissions for main scripts
log_info "Setting execute permissions for main scripts..."
log_info "تعيين صلاحيات التنفيذ للسكريبتات الرئيسية..."
for script in run.sh start.sh deploy.sh setup_*.sh clear_database.sh; do
    if [ -f "$script" ]; then
        chmod 755 "$script" 2>/dev/null && log_info "  ✓ $script" || log_warn "  ✗ $script"
    fi
done

# Summary / الملخص
log_info "========================================"
log_info "✅ Permissions set successfully"
log_info "✅ تم تعيين الصلاحيات بنجاح"
log_info "========================================"
log_info ""
log_info "Permission Summary:"
log_info "ملخص الصلاحيات:"
log_info "  - Directories:        755 (rwxr-xr-x)"
log_info "  - Python files:       644 (rw-r--r--)"
log_info "  - Shell scripts:      755 (rwxr-xr-x)"
log_info "  - Sensitive files:    600 (rw-------)"
log_info "  - Database files:     660 (rw-rw----)"
log_info "  - Upload directories: 755 (rwxr-xr-x)"
log_info "  - Upload files:       644 (rw-r--r--)"
log_info "  - Log files:          640 (rw-r-----)"
log_info "  - Backup files:       600 (rw-------)"
log_info ""
log_info "🔒 Security Notes:"
log_info "🔒 ملاحظات أمنية:"
log_info "  - .env files are protected (600)"
log_info "  - ملفات .env محمية (600)"
log_info "  - Database files have restricted access (660)"
log_info "  - ملفات قاعدة البيانات لها وصول محدود (660)"
log_info "  - Backups are private (600)"
log_info "  - النسخ الاحتياطية خاصة (600)"
log_info "========================================"

exit 0
