#!/bin/bash
# 🧹 Branch Cleanup Script / سكريبت تنظيف الفروع
# This script helps delete unnecessary branches from the repository
# هذا السكريبت يساعد على حذف الفروع غير الضرورية من المستودع
#
# Usage / الاستخدام:
#   chmod +x scripts/cleanup_branches.sh
#   ./scripts/cleanup_branches.sh
#
# ⚠️ WARNING: This will permanently delete branches!
# ⚠️ تحذير: سيتم حذف الفروع بشكل دائم!

echo "🧹 Repository Branch Cleanup Script"
echo "======================================"
echo ""

# Branches to keep / الفروع للاحتفاظ بها
KEEP_BRANCHES=(
    "main"
    "copilot/clean-repo-and-branches"
)

# Get all remote branches / الحصول على جميع الفروع البعيدة
echo "📋 Fetching all branches..."
git fetch --all --prune

# List all branches that will be deleted / عرض الفروع التي سيتم حذفها
echo ""
echo "🗑️ Branches to be deleted / الفروع المراد حذفها:"
echo "---------------------------------------------------"

count=0
for branch in $(git branch -r | grep -v HEAD | sed 's/origin\///' ); do
    skip=false
    for keep in "${KEEP_BRANCHES[@]}"; do
        if [[ "$branch" == "$keep" ]]; then
            skip=true
            break
        fi
    done
    
    if [[ "$skip" == false ]]; then
        echo "  - $branch"
        ((count++))
    fi
done

echo ""
echo "📊 Total branches to delete: $count"
echo ""

# Ask for confirmation / طلب التأكيد
read -p "⚠️ Are you sure you want to delete these branches? (yes/no): " confirm

if [[ "$confirm" != "yes" ]]; then
    echo "❌ Aborted. No branches were deleted."
    exit 0
fi

echo ""
echo "🗑️ Deleting branches..."
echo ""

deleted=0
failed=0

for branch in $(git branch -r | grep -v HEAD | sed 's/origin\///' ); do
    skip=false
    for keep in "${KEEP_BRANCHES[@]}"; do
        if [[ "$branch" == "$keep" ]]; then
            skip=true
            break
        fi
    done
    
    if [[ "$skip" == false ]]; then
        echo -n "  Deleting $branch... "
        if git push origin --delete "$branch" 2>/dev/null; then
            echo "✅"
            ((deleted++))
        else
            echo "❌ Failed"
            ((failed++))
        fi
    fi
done

echo ""
echo "======================================"
echo "🎉 Cleanup Complete!"
echo "   ✅ Deleted: $deleted branches"
echo "   ❌ Failed: $failed branches"
echo "   📌 Kept: ${#KEEP_BRANCHES[@]} branches (main, copilot/clean-repo-and-branches)"
echo "======================================"
