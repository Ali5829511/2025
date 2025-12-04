#!/bin/bash
# ==============================================================================
# سكريبت تنظيف الفروع / Branch Cleanup Script
# ==============================================================================
# 
# الوصف: يقوم هذا السكريبت بحذف الفروع القديمة والمدموجة من المستودع
# Description: This script deletes old and merged branches from the repository
#
# الاستخدام / Usage:
#   chmod +x scripts/cleanup_branches.sh
#   ./scripts/cleanup_branches.sh
#
# ==============================================================================

set -e

# الألوان للإخراج
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# قائمة الفروع المحمية التي لن يتم حذفها
PROTECTED_BRANCHES=(
    "main"
    "copilot/clean-repo-and-branches"
    "copilot/clean-repo-and-branches-again"
)

# دالة لطباعة رسائل ملونة
print_header() {
    echo ""
    echo -e "${BLUE}========================================${NC}"
    echo -e "${BLUE}$1${NC}"
    echo -e "${BLUE}========================================${NC}"
    echo ""
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

print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

# دالة للتحقق مما إذا كان الفرع محمياً
is_protected() {
    local branch=$1
    for protected in "${PROTECTED_BRANCHES[@]}"; do
        if [ "$branch" == "$protected" ]; then
            return 0
        fi
    done
    return 1
}

# التحقق من أننا في مستودع git
if ! git rev-parse --is-inside-work-tree > /dev/null 2>&1; then
    print_error "هذا السكريبت يجب أن يُشغّل داخل مستودع Git"
    print_error "This script must be run inside a Git repository"
    exit 1
fi

print_header "🧹 سكريبت تنظيف الفروع / Branch Cleanup Script"

# جلب أحدث المعلومات من المستودع البعيد
print_info "جاري جلب أحدث المعلومات من المستودع البعيد..."
git fetch --all --prune

# الحصول على جميع الفروع البعيدة
print_info "جاري تحليل الفروع..."
branches=$(git branch -r | grep -v HEAD | grep -v '\->' | sed 's/origin\///' | tr -d ' ')

# إحصائيات
total_branches=0
protected_count=0
to_delete_count=0

# قوائم الفروع
declare -a branches_to_delete=()
declare -a protected_branches_found=()

# تصنيف الفروع
for branch in $branches; do
    ((total_branches++))
    if is_protected "$branch"; then
        ((protected_count++))
        protected_branches_found+=("$branch")
    else
        ((to_delete_count++))
        branches_to_delete+=("$branch")
    fi
done

# عرض الإحصائيات
print_header "📊 إحصائيات الفروع / Branch Statistics"
echo "إجمالي الفروع / Total branches: $total_branches"
echo "فروع محمية / Protected branches: $protected_count"
echo "فروع للحذف / Branches to delete: $to_delete_count"

# عرض الفروع المحمية
print_header "🔒 الفروع المحمية / Protected Branches"
for branch in "${protected_branches_found[@]}"; do
    echo "  ✅ $branch"
done

# عرض الفروع التي سيتم حذفها
print_header "🗑️  الفروع التي سيتم حذفها / Branches to Delete"
if [ ${#branches_to_delete[@]} -eq 0 ]; then
    print_info "لا توجد فروع للحذف"
    print_info "No branches to delete"
    exit 0
fi

# تجميع الفروع حسب النوع
echo ""
echo -e "${YELLOW}فروع Copilot:${NC}"
for branch in "${branches_to_delete[@]}"; do
    if [[ "$branch" == copilot/* ]]; then
        echo "  - $branch"
    fi
done

echo ""
echo -e "${YELLOW}فروع Revert:${NC}"
for branch in "${branches_to_delete[@]}"; do
    if [[ "$branch" == revert-* ]]; then
        echo "  - $branch"
    fi
done

echo ""
echo -e "${YELLOW}فروع أخرى:${NC}"
for branch in "${branches_to_delete[@]}"; do
    if [[ ! "$branch" == copilot/* ]] && [[ ! "$branch" == revert-* ]]; then
        echo "  - $branch"
    fi
done

# طلب التأكيد
echo ""
print_warning "سيتم حذف $to_delete_count فرع!"
print_warning "$to_delete_count branches will be deleted!"
echo ""
read -p "هل تريد المتابعة؟ / Do you want to continue? (y/N): " confirm

if [ "$confirm" != "y" ] && [ "$confirm" != "Y" ]; then
    print_error "تم الإلغاء / Cancelled"
    exit 0
fi

# تنفيذ الحذف
print_header "🗑️  جاري حذف الفروع / Deleting Branches"

deleted_count=0
failed_count=0

for branch in "${branches_to_delete[@]}"; do
    echo -n "حذف / Deleting: $branch... "
    if git push origin --delete "$branch" 2>/dev/null; then
        print_success "تم"
        ((deleted_count++))
    else
        print_error "فشل"
        ((failed_count++))
    fi
done

# تنظيف المراجع المحلية
print_header "🧹 تنظيف المراجع المحلية / Cleaning Local References"
git fetch --prune

# ملخص النتائج
print_header "📋 ملخص النتائج / Results Summary"
print_success "تم حذف / Deleted: $deleted_count فرع"
if [ $failed_count -gt 0 ]; then
    print_error "فشل حذف / Failed to delete: $failed_count فرع"
fi
print_info "الفروع المتبقية / Remaining branches: $(git branch -r | grep -v HEAD | wc -l)"

echo ""
print_success "🎉 اكتمل تنظيف الفروع! / Branch cleanup completed!"
echo ""
