#!/usr/bin/env python3
"""
سكريبت لتحديث جميع صفحات HTML بإضافة الملفات المحسّنة
"""
import os
import re
from pathlib import Path

# المجلد الرئيسي
BASE_DIR = Path('/home/ubuntu/2025')

# الملفات المراد إضافتها
ENHANCED_CSS = '<link rel="stylesheet" href="/static/css/enhanced-mobile.css">'
ENHANCED_JS = '<script src="/static/js/enhanced-features.js"></script>'
CHARTJS_CDN = '<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>'

def update_html_file(file_path):
    """تحديث ملف HTML واحد"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # تحقق إذا كان الملف محدّث مسبقاً
        if 'enhanced-mobile.css' in content:
            print(f"⏭️  تخطي {file_path.name} (محدّث مسبقاً)")
            return False
        
        # إضافة CSS قبل </head>
        if '</head>' in content and ENHANCED_CSS not in content:
            content = content.replace('</head>', f'    {ENHANCED_CSS}\n</head>')
        
        # إضافة Chart.js قبل </head>
        if '</head>' in content and CHARTJS_CDN not in content:
            content = content.replace('</head>', f'    {CHARTJS_CDN}\n</head>')
        
        # إضافة JS قبل </body>
        if '</body>' in content and ENHANCED_JS not in content:
            content = content.replace('</body>', f'    {ENHANCED_JS}\n</body>')
        
        # حفظ الملف
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✅ تم تحديث {file_path.name}")
        return True
        
    except Exception as e:
        print(f"❌ خطأ في {file_path.name}: {e}")
        return False

def main():
    """الدالة الرئيسية"""
    print("🚀 بدء تحديث صفحات HTML...")
    print("=" * 60)
    
    # البحث عن جميع ملفات HTML
    html_files = list(BASE_DIR.glob('*.html'))
    html_files += list(BASE_DIR.glob('pages/*.html'))
    
    updated_count = 0
    skipped_count = 0
    error_count = 0
    
    for html_file in html_files:
        result = update_html_file(html_file)
        if result is True:
            updated_count += 1
        elif result is False:
            skipped_count += 1
        else:
            error_count += 1
    
    print("=" * 60)
    print(f"📊 النتائج:")
    print(f"   ✅ تم التحديث: {updated_count} ملف")
    print(f"   ⏭️  تم التخطي: {skipped_count} ملف")
    print(f"   ❌ أخطاء: {error_count} ملف")
    print(f"   📁 الإجمالي: {len(html_files)} ملف")
    print("=" * 60)
    print("✨ اكتمل التحديث!")

if __name__ == '__main__':
    main()
