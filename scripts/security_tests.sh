#!/bin/bash
# ==============================================================================
# Security Testing Script - سكريبت اختبار الأمان
# ==============================================================================
# Automated security checks for Housing Management System
# فحوصات أمنية تلقائية لنظام إدارة الإسكان
# ==============================================================================

set -e

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m'

log_info() { echo -e "${GREEN}[✓]${NC} $1"; }
log_warn() { echo -e "${YELLOW}[!]${NC} $1"; }
log_error() { echo -e "${RED}[✗]${NC} $1"; }
log_section() { echo -e "\n${BLUE}===${NC} $1 ${BLUE}===${NC}\n"; }

# Configuration
TARGET_URL="${TARGET_URL:-http://localhost:5000}"
REPORT_FILE="security_test_results_$(date +%Y%m%d_%H%M%S).txt"

# Start report
exec > >(tee -a "$REPORT_FILE")
exec 2>&1

echo "=============================================="
echo "Security Testing Report"
echo "تقرير اختبار الأمان"
echo "=============================================="
echo "Target: $TARGET_URL"
echo "Date: $(date)"
echo "=============================================="
echo ""

# ==============================================================================
# 1. Environment Configuration Check / فحص تكوين البيئة
# ==============================================================================
log_section "1. Environment Configuration Check"

check_env_var() {
    local var_name=$1
    local expected=$2
    local actual="${!var_name}"
    
    if [ "$actual" = "$expected" ]; then
        log_info "$var_name = $expected"
        return 0
    else
        log_error "$var_name = $actual (Expected: $expected)"
        return 1
    fi
}

# Check Flask configuration
if [ -f ".env" ]; then
    log_info "Found .env file"
    
    # Load environment variables
    export $(grep -v '^#' .env | xargs)
    
    # Check critical settings
    check_env_var "FLASK_ENV" "production" || log_warn "FLASK_ENV should be 'production'"
    check_env_var "FLASK_DEBUG" "False" || log_error "FLASK_DEBUG must be False!"
    
    # Check if SECRET_KEY is strong
    if [ -n "$SECRET_KEY" ] && [ "$SECRET_KEY" != "change-this-to-a-random-secret-key-in-production" ]; then
        log_info "SECRET_KEY is set and not default"
    else
        log_error "SECRET_KEY is default or not set!"
    fi
else
    log_warn ".env file not found"
fi

# ==============================================================================
# 2. File Permissions Check / فحص صلاحيات الملفات
# ==============================================================================
log_section "2. File Permissions Check"

check_file_permissions() {
    local file=$1
    local expected=$2
    
    if [ -f "$file" ]; then
        local perms=$(stat -c "%a" "$file" 2>/dev/null || stat -f "%Lp" "$file" 2>/dev/null)
        if [ "$perms" = "$expected" ]; then
            log_info "$file: $perms (OK)"
        else
            log_warn "$file: $perms (Expected: $expected)"
        fi
    fi
}

# Check sensitive files
check_file_permissions ".env" "600"
check_file_permissions ".env.traffic" "600"

# Check database files
for db in *.db; do
    if [ -f "$db" ]; then
        check_file_permissions "$db" "660"
    fi
done

# ==============================================================================
# 3. Password Security Test / اختبار أمان كلمات المرور
# ==============================================================================
log_section "3. Password Security Test"

# Test default passwords
log_info "Testing for default passwords..."

default_users=("admin:Admin@2025" "violations_officer:Violations@2025" "visitors_officer:Visitors@2025")

for user_pass in "${default_users[@]}"; do
    IFS=':' read -r username password <<< "$user_pass"
    
    response=$(curl -s -X POST "$TARGET_URL/api/auth/login" \
        -H "Content-Type: application/json" \
        -d "{\"username\":\"$username\",\"password\":\"$password\"}" \
        -w "\n%{http_code}" 2>/dev/null || echo "000")
    
    http_code=$(echo "$response" | tail -n1)
    
    if [ "$http_code" = "200" ]; then
        log_warn "Default password still works for: $username"
    elif [ "$http_code" = "401" ]; then
        log_info "Default password changed for: $username"
    else
        log_warn "Could not test: $username (HTTP $http_code)"
    fi
done

# ==============================================================================
# 4. SSL/TLS Configuration Test / اختبار تكوين SSL/TLS
# ==============================================================================
log_section "4. SSL/TLS Configuration Test"

if [[ "$TARGET_URL" == https://* ]]; then
    log_info "Testing SSL/TLS configuration..."
    
    # Test SSL connection
    if command -v openssl &> /dev/null; then
        domain=$(echo "$TARGET_URL" | sed -e 's|^https://||' -e 's|/.*||')
        
        ssl_info=$(echo | openssl s_client -connect "$domain:443" -servername "$domain" 2>/dev/null | openssl x509 -noout -dates 2>/dev/null)
        
        if [ $? -eq 0 ]; then
            log_info "SSL certificate is valid"
            echo "$ssl_info" | while read line; do
                echo "  $line"
            done
        else
            log_error "SSL certificate test failed"
        fi
        
        # Check SSL protocols
        log_info "Testing SSL protocols..."
        
        # Test SSLv3 (should fail)
        if echo | openssl s_client -connect "$domain:443" -ssl3 2>&1 | grep -q "connect:errno"; then
            log_info "SSLv3 is disabled (good)"
        else
            log_error "SSLv3 is enabled (vulnerability!)"
        fi
        
        # Test TLS 1.2 (should work)
        if echo | openssl s_client -connect "$domain:443" -tls1_2 2>&1 | grep -q "Cipher"; then
            log_info "TLS 1.2 is supported"
        else
            log_warn "TLS 1.2 is not supported"
        fi
    else
        log_warn "OpenSSL not found, skipping SSL tests"
    fi
else
    log_warn "Target is not HTTPS - SSL/TLS tests skipped"
fi

# ==============================================================================
# 5. HTTP Security Headers Test / اختبار ترويسات الأمان HTTP
# ==============================================================================
log_section "5. HTTP Security Headers Test"

log_info "Checking security headers..."

headers=$(curl -s -I "$TARGET_URL" 2>/dev/null || echo "")

check_header() {
    local header=$1
    if echo "$headers" | grep -qi "^$header:"; then
        log_info "$header is set"
        echo "$headers" | grep -i "^$header:" | sed 's/^/  /'
    else
        log_warn "$header is not set"
    fi
}

check_header "Strict-Transport-Security"
check_header "X-Content-Type-Options"
check_header "X-Frame-Options"
check_header "X-XSS-Protection"
check_header "Content-Security-Policy"

# ==============================================================================
# 6. SQL Injection Test / اختبار حقن SQL
# ==============================================================================
log_section "6. SQL Injection Test (Basic)"

log_info "Testing for basic SQL injection vulnerabilities..."

sql_payloads=(
    "' OR '1'='1"
    "admin'--"
    "' OR 1=1--"
    "'; DROP TABLE users--"
)

for payload in "${sql_payloads[@]}"; do
    response=$(curl -s -X POST "$TARGET_URL/api/auth/login" \
        -H "Content-Type: application/json" \
        -d "{\"username\":\"$payload\",\"password\":\"test\"}" \
        -w "\n%{http_code}" 2>/dev/null || echo "000")
    
    http_code=$(echo "$response" | tail -n1)
    
    if [ "$http_code" = "401" ]; then
        log_info "SQL injection blocked: $payload"
    elif [ "$http_code" = "500" ]; then
        log_error "SQL injection caused server error: $payload"
    else
        log_warn "Unexpected response for: $payload (HTTP $http_code)"
    fi
done

# ==============================================================================
# 7. XSS Test / اختبار XSS
# ==============================================================================
log_section "7. Cross-Site Scripting (XSS) Test"

log_info "Testing for XSS vulnerabilities..."

xss_payloads=(
    "<script>alert('XSS')</script>"
    "<img src=x onerror=alert('XSS')>"
    "javascript:alert('XSS')"
)

for payload in "${xss_payloads[@]}"; do
    response=$(curl -s -X POST "$TARGET_URL/api/auth/login" \
        -H "Content-Type: application/json" \
        -d "{\"username\":\"test\",\"password\":\"$payload\"}" 2>/dev/null || echo "")
    
    if echo "$response" | grep -q "$payload"; then
        log_error "Possible XSS vulnerability: payload reflected"
    else
        log_info "XSS payload sanitized or blocked"
    fi
done

# ==============================================================================
# 8. Authentication & Session Test / اختبار المصادقة والجلسات
# ==============================================================================
log_section "8. Authentication & Session Test"

log_info "Testing authentication endpoints..."

# Test login endpoint
response=$(curl -s -X POST "$TARGET_URL/api/auth/login" \
    -H "Content-Type: application/json" \
    -d '{"username":"test","password":"test"}' \
    -w "\n%{http_code}" 2>/dev/null || echo "000")

http_code=$(echo "$response" | tail -n1)

if [ "$http_code" = "401" ]; then
    log_info "Login endpoint returns 401 for invalid credentials"
elif [ "$http_code" = "200" ]; then
    log_warn "Login succeeded with test credentials"
else
    log_warn "Unexpected login response: HTTP $http_code"
fi

# Test protected endpoint without auth
response=$(curl -s -X GET "$TARGET_URL/api/auth/validate" \
    -w "\n%{http_code}" 2>/dev/null || echo "000")

http_code=$(echo "$response" | tail -n1)

if [ "$http_code" = "401" ]; then
    log_info "Protected endpoint requires authentication"
else
    log_warn "Protected endpoint accessible without auth: HTTP $http_code"
fi

# ==============================================================================
# 9. Rate Limiting Test / اختبار تحديد المعدل
# ==============================================================================
log_section "9. Rate Limiting Test"

log_info "Testing for rate limiting..."

success_count=0
for i in {1..20}; do
    response=$(curl -s -X POST "$TARGET_URL/api/auth/login" \
        -H "Content-Type: application/json" \
        -d '{"username":"test","password":"test"}' \
        -w "\n%{http_code}" 2>/dev/null || echo "000")
    
    http_code=$(echo "$response" | tail -n1)
    
    if [ "$http_code" = "429" ]; then
        log_info "Rate limiting detected after $i attempts"
        success_count=$i
        break
    fi
done

if [ $success_count -eq 0 ]; then
    log_warn "No rate limiting detected (20 requests allowed)"
else
    log_info "Rate limiting works correctly"
fi

# ==============================================================================
# 10. Backup Files Check / فحص ملفات النسخ الاحتياطي
# ==============================================================================
log_section "10. Backup Files Check"

log_info "Checking for backup files..."

backup_patterns=(".bak" ".old" ".backup" "~" ".swp" ".tmp")

found_backups=0
for pattern in "${backup_patterns[@]}"; do
    files=$(find . -name "*$pattern" -type f 2>/dev/null | grep -v "backups/" | head -5)
    if [ -n "$files" ]; then
        log_warn "Found backup files with pattern '$pattern':"
        echo "$files" | sed 's/^/  /'
        found_backups=1
    fi
done

if [ $found_backups -eq 0 ]; then
    log_info "No backup files found in application directory"
fi

# ==============================================================================
# Summary / الملخص
# ==============================================================================
log_section "Security Test Summary"

echo ""
echo "=============================================="
echo "Test completed successfully"
echo "اكتمل الاختبار بنجاح"
echo "=============================================="
echo ""
echo "Report saved to: $REPORT_FILE"
echo "تم حفظ التقرير في: $REPORT_FILE"
echo ""
echo "⚠️  Review all warnings and errors"
echo "⚠️  راجع جميع التحذيرات والأخطاء"
echo ""
echo "For production deployment:"
echo "للنشر الإنتاجي:"
echo "  1. Fix all errors (✗)"
echo "  2. Review all warnings (!)"
echo "  3. Ensure HTTPS is enabled"
echo "  4. Change all default passwords"
echo "  5. Enable rate limiting"
echo "  6. Configure security headers"
echo "=============================================="

exit 0
