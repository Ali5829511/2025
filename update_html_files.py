#!/usr/bin/env python3
"""
Update HTML files to include mobile enhancements and proper logo paths
تحديث ملفات HTML لإضافة تحسينات الجوال والمسارات الصحيحة للشعار
"""

import os
import re
from pathlib import Path

def update_html_file(filepath):
    """Update a single HTML file"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # 1. Update logo paths
        # Replace university_logo.png with static/images/university_logo.png
        content = re.sub(
            r'src=["\']university_logo\.png["\']',
            'src="static/images/university_logo.png"',
            content
        )
        
        # 2. Add mobile-responsive CSS if not present
        if 'mobile-responsive.css' not in content and '</head>' in content:
            if 'responsive-style.css' in content:
                # Add after responsive-style.css
                content = content.replace(
                    '<link rel="stylesheet" href="static/css/responsive-style.css">',
                    '<link rel="stylesheet" href="static/css/responsive-style.css">\n    <link rel="stylesheet" href="static/css/mobile-responsive.css">'
                )
            else:
                # Add before </head>
                content = content.replace(
                    '</head>',
                    '    <link rel="stylesheet" href="static/css/mobile-responsive.css">\n</head>'
                )
        
        # 3. Add mobile-enhancements.js if not present
        if 'mobile-enhancements.js' not in content and '</body>' in content:
            content = content.replace(
                '</body>',
                '    <script src="static/js/mobile-enhancements.js"></script>\n</body>'
            )
        
        # 4. Ensure proper viewport meta tag
        if '<meta name="viewport"' not in content:
            head_tag = '<head>'
            if head_tag in content:
                content = content.replace(
                    head_tag,
                    head_tag + '\n    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=5.0, user-scalable=yes">'
                )
        
        # Write back if changed
        if content != original_content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        return False
    
    except Exception as e:
        print(f"❌ Error updating {filepath}: {e}")
        return False

def main():
    """Main function"""
    print("🔄 Updating HTML files...")
    print("=" * 60)
    
    # Get all HTML files in current directory
    html_files = list(Path('.').glob('*.html'))
    
    updated_count = 0
    skipped_count = 0
    
    for html_file in sorted(html_files):
        if update_html_file(str(html_file)):
            print(f"✅ Updated: {html_file.name}")
            updated_count += 1
        else:
            print(f"⏭️  Skipped: {html_file.name}")
            skipped_count += 1
    
    print("=" * 60)
    print(f"\n📊 Summary:")
    print(f"   ✅ Updated: {updated_count} files")
    print(f"   ⏭️  Skipped: {skipped_count} files")
    print(f"   📁 Total: {len(html_files)} files")
    print("\n✨ HTML files have been updated successfully!")

if __name__ == '__main__':
    main()
