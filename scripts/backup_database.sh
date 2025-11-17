#!/bin/bash
# ==============================================================================
# Database Backup Script - نظام النسخ الاحتياطي لقاعدة البيانات
# ==============================================================================
# Automated database backup with rotation and optional S3 upload
# نسخ احتياطي تلقائي لقاعدة البيانات مع التناوب والتحميل إلى S3 (اختياري)
# ==============================================================================

set -e  # Exit on error

# Configuration / التكوين
# ==============================================================================
BACKUP_DIR="${BACKUP_DIR:-./backups}"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
RETENTION_DAYS="${RETENTION_DAYS:-30}"  # Keep backups for 30 days / الاحتفاظ بالنسخ لمدة 30 يوم

# Database configuration / تكوين قاعدة البيانات
DATABASE_URL="${DATABASE_URL:-}"
SQLITE_DB="${SQLITE_DB:-housing.db}"
TRAFFIC_DB="${TRAFFIC_DB:-traffic.db}"

# S3 Configuration (optional) / تكوين S3 (اختياري)
BACKUP_S3_BUCKET="${BACKUP_S3_BUCKET:-}"
AWS_ACCESS_KEY_ID="${AWS_ACCESS_KEY_ID:-}"
AWS_SECRET_ACCESS_KEY="${AWS_SECRET_ACCESS_KEY:-}"

# Colors for output / ألوان للإخراج
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# ==============================================================================
# Functions / الدوال
# ==============================================================================

log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Create backup directory / إنشاء مجلد النسخ الاحتياطية
# ==============================================================================
create_backup_dir() {
    if [ ! -d "$BACKUP_DIR" ]; then
        log_info "Creating backup directory: $BACKUP_DIR"
        log_info "إنشاء مجلد النسخ الاحتياطية: $BACKUP_DIR"
        mkdir -p "$BACKUP_DIR"
    fi
}

# Backup SQLite database / نسخ احتياطي لقاعدة بيانات SQLite
# ==============================================================================
backup_sqlite() {
    local db_file=$1
    local db_name=$(basename "$db_file" .db)
    local backup_file="${BACKUP_DIR}/${db_name}_${TIMESTAMP}.db"
    local compressed_file="${backup_file}.gz"
    
    if [ -f "$db_file" ]; then
        log_info "Backing up SQLite database: $db_file"
        log_info "نسخ احتياطي لقاعدة البيانات: $db_file"
        
        # Create backup using sqlite3 .dump for consistency
        sqlite3 "$db_file" ".backup '$backup_file'"
        
        # Compress backup / ضغط النسخة الاحتياطية
        log_info "Compressing backup..."
        log_info "ضغط النسخة الاحتياطية..."
        gzip -f "$backup_file"
        
        log_info "✅ Backup created: $compressed_file"
        log_info "✅ تم إنشاء النسخة الاحتياطية: $compressed_file"
        
        echo "$compressed_file"
    else
        log_warn "Database file not found: $db_file"
        log_warn "لم يتم العثور على ملف قاعدة البيانات: $db_file"
    fi
}

# Backup PostgreSQL database / نسخ احتياطي لقاعدة بيانات PostgreSQL
# ==============================================================================
backup_postgresql() {
    local backup_file="${BACKUP_DIR}/postgresql_${TIMESTAMP}.sql"
    local compressed_file="${backup_file}.gz"
    
    if [ -n "$DATABASE_URL" ]; then
        log_info "Backing up PostgreSQL database"
        log_info "نسخ احتياطي لقاعدة بيانات PostgreSQL"
        
        # Use pg_dump
        if command -v pg_dump &> /dev/null; then
            pg_dump "$DATABASE_URL" > "$backup_file"
            
            # Compress backup / ضغط النسخة الاحتياطية
            log_info "Compressing backup..."
            log_info "ضغط النسخة الاحتياطية..."
            gzip -f "$backup_file"
            
            log_info "✅ Backup created: $compressed_file"
            log_info "✅ تم إنشاء النسخة الاحتياطية: $compressed_file"
            
            echo "$compressed_file"
        else
            log_error "pg_dump not found. Please install PostgreSQL client tools."
            log_error "لم يتم العثور على pg_dump. يرجى تثبيت أدوات عميل PostgreSQL."
        fi
    else
        log_warn "DATABASE_URL not set, skipping PostgreSQL backup"
        log_warn "DATABASE_URL غير معرف، تخطي النسخ الاحتياطي لـ PostgreSQL"
    fi
}

# Upload to S3 / التحميل إلى S3
# ==============================================================================
upload_to_s3() {
    local file=$1
    
    if [ -n "$BACKUP_S3_BUCKET" ] && [ -n "$AWS_ACCESS_KEY_ID" ] && [ -n "$AWS_SECRET_ACCESS_KEY" ]; then
        log_info "Uploading backup to S3: $BACKUP_S3_BUCKET"
        log_info "تحميل النسخة الاحتياطية إلى S3: $BACKUP_S3_BUCKET"
        
        if command -v aws &> /dev/null; then
            aws s3 cp "$file" "s3://${BACKUP_S3_BUCKET}/backups/$(basename $file)"
            log_info "✅ Uploaded to S3 successfully"
            log_info "✅ تم التحميل إلى S3 بنجاح"
        else
            log_warn "AWS CLI not installed. Install with: pip install awscli"
            log_warn "AWS CLI غير مثبت. ثبته باستخدام: pip install awscli"
        fi
    fi
}

# Clean old backups / تنظيف النسخ الاحتياطية القديمة
# ==============================================================================
cleanup_old_backups() {
    log_info "Cleaning up backups older than $RETENTION_DAYS days"
    log_info "تنظيف النسخ الاحتياطية الأقدم من $RETENTION_DAYS يوم"
    
    find "$BACKUP_DIR" -name "*.db.gz" -type f -mtime +$RETENTION_DAYS -delete
    find "$BACKUP_DIR" -name "*.sql.gz" -type f -mtime +$RETENTION_DAYS -delete
    
    log_info "✅ Cleanup completed"
    log_info "✅ اكتمل التنظيف"
}

# Verify backup / التحقق من النسخة الاحتياطية
# ==============================================================================
verify_backup() {
    local file=$1
    
    log_info "Verifying backup: $file"
    log_info "التحقق من النسخة الاحتياطية: $file"
    
    if [ -f "$file" ]; then
        # Check file size
        local size=$(stat -f%z "$file" 2>/dev/null || stat -c%s "$file" 2>/dev/null)
        if [ "$size" -gt 0 ]; then
            log_info "✅ Backup verified: $size bytes"
            log_info "✅ تم التحقق من النسخة الاحتياطية: $size بايت"
            return 0
        else
            log_error "❌ Backup file is empty"
            log_error "❌ ملف النسخة الاحتياطية فارغ"
            return 1
        fi
    else
        log_error "❌ Backup file not found"
        log_error "❌ لم يتم العثور على ملف النسخة الاحتياطية"
        return 1
    fi
}

# ==============================================================================
# Main Script / السكريبت الرئيسي
# ==============================================================================

main() {
    log_info "========================================"
    log_info "Starting Database Backup"
    log_info "بدء النسخ الاحتياطي لقاعدة البيانات"
    log_info "Timestamp: $TIMESTAMP"
    log_info "========================================"
    
    # Create backup directory
    create_backup_dir
    
    # Backup SQLite databases
    if [ -f "$SQLITE_DB" ]; then
        backup_file=$(backup_sqlite "$SQLITE_DB")
        if verify_backup "$backup_file"; then
            upload_to_s3 "$backup_file"
        fi
    fi
    
    if [ -f "$TRAFFIC_DB" ]; then
        backup_file=$(backup_sqlite "$TRAFFIC_DB")
        if verify_backup "$backup_file"; then
            upload_to_s3 "$backup_file"
        fi
    fi
    
    # Backup PostgreSQL if configured
    if [ -n "$DATABASE_URL" ]; then
        backup_file=$(backup_postgresql)
        if [ -n "$backup_file" ] && verify_backup "$backup_file"; then
            upload_to_s3 "$backup_file"
        fi
    fi
    
    # Cleanup old backups
    cleanup_old_backups
    
    log_info "========================================"
    log_info "✅ Backup completed successfully"
    log_info "✅ اكتمل النسخ الاحتياطي بنجاح"
    log_info "========================================"
}

# Run main function
main

exit 0
