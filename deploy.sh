#!/bin/bash
################################################################################
# سكريبت النشر السريع لنظام إدارة الإسكان
# Quick Deployment Script for Housing Management System
################################################################################

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Print functions
print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_header() {
    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo -e "${BLUE}$1${NC}"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
}

################################################################################
# Main Menu
################################################################################

show_menu() {
    clear
    echo "╔═══════════════════════════════════════════════════════════╗"
    echo "║                                                           ║"
    echo "║         نظام إدارة إسكان أعضاء هيئة التدريس            ║"
    echo "║       Faculty Housing Management System                  ║"
    echo "║                                                           ║"
    echo "║              سكريبت النشر السريع                        ║"
    echo "║            Quick Deployment Script                       ║"
    echo "║                                                           ║"
    echo "╚═══════════════════════════════════════════════════════════╝"
    echo ""
    echo "اختر طريقة النشر / Choose deployment method:"
    echo ""
    echo "  1) 🐳 النشر باستخدام Docker (الأسرع والأسهل)"
    echo "     Deploy with Docker (Fastest & Easiest)"
    echo ""
    echo "  2) 🚀 النشر التقليدي (Nginx + Gunicorn)"
    echo "     Traditional Deployment (Nginx + Gunicorn)"
    echo ""
    echo "  3) ⚡ تطوير محلي فقط (Development Only)"
    echo "     Local Development Only"
    echo ""
    echo "  4) 🔧 استكشاف الأخطاء"
    echo "     Troubleshooting"
    echo ""
    echo "  5) ❌ خروج / Exit"
    echo ""
    read -p "اختيارك / Your choice [1-5]: " choice
}

################################################################################
# Docker Deployment
################################################################################

deploy_docker() {
    print_header "🐳 النشر باستخدام Docker"
    
    # Check if Docker is installed
    if ! command -v docker &> /dev/null; then
        print_warning "Docker غير مثبت / Docker is not installed"
        read -p "هل تريد تثبيت Docker؟ / Install Docker? (y/n): " install_docker
        if [[ $install_docker == "y" ]]; then
            print_info "جاري تثبيت Docker..."
            curl -fsSL https://get.docker.com -o get-docker.sh
            sudo sh get-docker.sh
            sudo usermod -aG docker $USER
            print_success "تم تثبيت Docker بنجاح!"
            print_warning "يرجى إعادة تسجيل الدخول أو تشغيل: newgrp docker"
            exit 0
        else
            print_error "لا يمكن المتابعة بدون Docker"
            return 1
        fi
    fi
    
    # Check if docker-compose is installed
    if ! command -v docker-compose &> /dev/null; then
        print_info "جاري تثبيت Docker Compose..."
        sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
        sudo chmod +x /usr/local/bin/docker-compose
        print_success "تم تثبيت Docker Compose بنجاح!"
    fi
    
    # Create .env file if not exists
    if [ ! -f .env ]; then
        print_info "جاري إنشاء ملف .env..."
        cat > .env <<EOF
DB_PASSWORD=$(openssl rand -base64 32)
SECRET_KEY=$(openssl rand -hex 32)
EOF
        print_success "تم إنشاء ملف .env"
    fi
    
    # Build and start containers
    print_info "جاري بناء وتشغيل الخدمات..."
    docker-compose up -d --build
    
    # Wait for services to be ready
    print_info "انتظر حتى تصبح الخدمات جاهزة..."
    sleep 10
    
    # Check services status
    print_info "التحقق من حالة الخدمات..."
    docker-compose ps
    
    print_success "تم النشر بنجاح!"
    echo ""
    print_info "الوصول للنظام:"
    echo "  🌐 http://localhost"
    echo "  📊 http://localhost/system_validation_report.html"
    echo ""
    print_info "للمراقبة:"
    echo "  📋 docker-compose logs -f"
    echo ""
    print_info "للإيقاف:"
    echo "  🛑 docker-compose stop"
}

################################################################################
# Traditional Deployment
################################################################################

deploy_traditional() {
    print_header "🚀 النشر التقليدي"
    
    print_info "هذا الخيار يتطلب إعداد يدوي متقدم"
    print_info "راجع دليل النشر الكامل: دليل_النشر_الكامل.md"
    echo ""
    read -p "هل تريد المتابعة؟ / Continue? (y/n): " continue_trad
    
    if [[ $continue_trad != "y" ]]; then
        return
    fi
    
    # Check Python
    if ! command -v python3 &> /dev/null; then
        print_error "Python 3 غير مثبت"
        return 1
    fi
    
    # Install dependencies
    print_info "جاري تثبيت المتطلبات..."
    pip3 install -r requirements.txt
    pip3 install gunicorn psycopg2-binary
    
    # Create database
    print_info "جاري إنشاء قاعدة البيانات..."
    python3 database.py
    
    print_success "تم إعداد البيئة الأساسية"
    echo ""
    print_warning "للنشر الكامل، اتبع الخطوات في:"
    echo "  📖 دليل_النشر_الكامل.md"
    echo ""
    print_info "للتشغيل المؤقت:"
    echo "  python3 server.py"
}

################################################################################
# Local Development
################################################################################

setup_development() {
    print_header "⚡ إعداد بيئة التطوير المحلي"
    
    # Check Python
    if ! command -v python3 &> /dev/null; then
        print_error "Python 3 غير مثبت"
        return 1
    fi
    
    print_info "إصدار Python: $(python3 --version)"
    
    # Create virtual environment
    if [ ! -d "venv" ]; then
        print_info "جاري إنشاء البيئة الافتراضية..."
        python3 -m venv venv
        print_success "تم إنشاء البيئة الافتراضية"
    fi
    
    # Activate virtual environment
    print_info "تفعيل البيئة الافتراضية..."
    source venv/bin/activate
    
    # Install requirements
    print_info "جاري تثبيت المتطلبات..."
    pip install --upgrade pip
    pip install -r requirements.txt
    
    # Create database
    print_info "جاري إنشاء قاعدة البيانات..."
    python3 database.py
    
    print_success "تم إعداد بيئة التطوير بنجاح!"
    echo ""
    print_info "لتشغيل الخادم:"
    echo "  source venv/bin/activate"
    echo "  python3 server.py"
    echo ""
    print_info "الوصول للنظام:"
    echo "  🌐 http://localhost:5000"
}

################################################################################
# Troubleshooting
################################################################################

troubleshoot() {
    print_header "🔧 استكشاف الأخطاء"
    
    echo "اختر المشكلة / Choose issue:"
    echo ""
    echo "  1) خطأ 500 / Error 500"
    echo "  2) مشكلة في قاعدة البيانات / Database issue"
    echo "  3) مشكلة في Docker / Docker issue"
    echo "  4) رجوع / Back"
    echo ""
    read -p "اختيارك / Your choice: " issue_choice
    
    case $issue_choice in
        1)
            print_info "راجع دليل حل خطأ 500:"
            echo "  📖 حل_خطأ_500.md"
            echo ""
            print_info "الحلول السريعة:"
            echo "  1. pip install -r requirements.txt"
            echo "  2. python3 database.py"
            echo "  3. python3 server.py"
            ;;
        2)
            print_info "التحقق من قاعدة البيانات..."
            if [ -f "housing.db" ]; then
                print_success "ملف قاعدة البيانات موجود"
                sqlite3 housing.db "SELECT COUNT(*) FROM users;" 2>/dev/null && \
                    print_success "قاعدة البيانات تعمل بشكل صحيح" || \
                    print_warning "قد تحتاج لإعادة إنشاء قاعدة البيانات: python3 database.py"
            else
                print_warning "ملف قاعدة البيانات غير موجود"
                print_info "تشغيل: python3 database.py"
            fi
            ;;
        3)
            print_info "التحقق من Docker..."
            docker --version && print_success "Docker مثبت" || print_error "Docker غير مثبت"
            docker-compose --version && print_success "Docker Compose مثبت" || print_error "Docker Compose غير مثبت"
            
            if command -v docker &> /dev/null; then
                print_info "حالة الخدمات:"
                docker-compose ps 2>/dev/null || print_info "لا توجد خدمات قيد التشغيل"
            fi
            ;;
    esac
    
    echo ""
    read -p "اضغط Enter للمتابعة..."
}

################################################################################
# Main Loop
################################################################################

main() {
    while true; do
        show_menu
        
        case $choice in
            1)
                deploy_docker
                read -p "اضغط Enter للمتابعة..."
                ;;
            2)
                deploy_traditional
                read -p "اضغط Enter للمتابعة..."
                ;;
            3)
                setup_development
                read -p "اضغط Enter للمتابعة..."
                ;;
            4)
                troubleshoot
                ;;
            5)
                print_info "شكراً لاستخدامك النظام!"
                exit 0
                ;;
            *)
                print_error "خيار غير صحيح"
                sleep 2
                ;;
        esac
    done
}

# Run main function
main
