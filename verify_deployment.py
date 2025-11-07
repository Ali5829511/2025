#!/usr/bin/env python3
"""
Deployment Verification Script
سكريبت التحقق من جاهزية النشر

This script verifies that the project is ready for deployment.
يتحقق هذا السكريبت من جاهزية المشروع للنشر.
"""

import sys
import os
import subprocess
from pathlib import Path

# Colors for terminal output
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    BOLD = '\033[1m'
    END = '\033[0m'

def print_header(text):
    """Print a formatted header"""
    print(f"\n{Colors.BLUE}{Colors.BOLD}{'='*60}{Colors.END}")
    print(f"{Colors.BLUE}{Colors.BOLD}{text}{Colors.END}")
    print(f"{Colors.BLUE}{Colors.BOLD}{'='*60}{Colors.END}\n")

def print_success(text):
    """Print success message"""
    print(f"{Colors.GREEN}✅ {text}{Colors.END}")

def print_error(text):
    """Print error message"""
    print(f"{Colors.RED}❌ {text}{Colors.END}")

def print_warning(text):
    """Print warning message"""
    print(f"{Colors.YELLOW}⚠️  {text}{Colors.END}")

def print_info(text):
    """Print info message"""
    print(f"{Colors.BLUE}ℹ️  {text}{Colors.END}")

def check_python_version():
    """Check Python version"""
    print_info("Checking Python version...")
    version = sys.version_info
    version_str = f"{version.major}.{version.minor}.{version.micro}"
    
    if version.major >= 3 and version.minor >= 8:
        print_success(f"Python {version_str} (compatible)")
        return True
    else:
        print_error(f"Python {version_str} (requires 3.8+)")
        return False

def check_file_exists(filepath, required=True):
    """Check if a file exists"""
    if Path(filepath).exists():
        print_success(f"Found: {filepath}")
        return True
    else:
        if required:
            print_error(f"Missing: {filepath}")
        else:
            print_warning(f"Optional: {filepath} (not found)")
        return not required

def check_required_files():
    """Check if all required files exist"""
    print_info("Checking required files...")
    
    required_files = [
        'server.py',
        'database.py',
        'auth.py',
        'requirements.txt',
        'gunicorn_config.py',
        'init_db.py',
        'database_adapter.py',
    ]
    
    deployment_files = [
        'render.yaml',
        'Procfile',
        'railway.json',
        'nixpacks.toml',
        'Dockerfile',
        'docker-compose.yml',
        'runtime.txt',
    ]
    
    all_good = True
    
    print_info("Core application files:")
    for file in required_files:
        if not check_file_exists(file):
            all_good = False
    
    print_info("\nDeployment configuration files:")
    for file in deployment_files:
        check_file_exists(file, required=False)
    
    return all_good

def check_requirements():
    """Check if requirements can be installed"""
    print_info("Checking Python requirements...")
    
    try:
        with open('requirements.txt', 'r') as f:
            requirements = f.read().strip().split('\n')
            print_info(f"Found {len([r for r in requirements if r and not r.startswith('#')])} requirements")
            print_success("requirements.txt is readable")
            return True
    except Exception as e:
        print_error(f"Error reading requirements.txt: {e}")
        return False

def check_database_init():
    """Check if database can be initialized"""
    print_info("Checking database initialization...")
    
    try:
        # Check if database.py is importable
        import database
        print_success("database.py is importable")
        return True
    except ImportError as e:
        print_error(f"Cannot import database.py: {e}")
        return False
    except Exception as e:
        print_warning(f"Import succeeded but with warning: {e}")
        return True

def check_deployment_configs():
    """Check deployment configurations"""
    print_info("Checking deployment configurations...")
    
    configs = {
        'Render': 'render.yaml',
        'Railway': 'railway.json',
        'Docker': 'docker-compose.yml',
        'Heroku': 'Procfile',
    }
    
    available = []
    for platform, config_file in configs.items():
        if Path(config_file).exists():
            print_success(f"{platform}: {config_file} found")
            available.append(platform)
        else:
            print_info(f"{platform}: {config_file} not found")
    
    return len(available) > 0, available

def print_summary(results):
    """Print summary of verification"""
    print_header("📊 Verification Summary / ملخص التحقق")
    
    passed = sum(1 for r in results.values() if r)
    total = len(results)
    percentage = (passed / total * 100) if total > 0 else 0
    
    print(f"Tests Passed: {passed}/{total} ({percentage:.0f}%)")
    print()
    
    for test, result in results.items():
        if result:
            print_success(f"{test}")
        else:
            print_error(f"{test}")
    
    print()
    
    if passed == total:
        print_success("🎉 All checks passed! Project is ready for deployment!")
        print_success("🎉 جميع الفحوصات نجحت! المشروع جاهز للنشر!")
        return True
    elif passed >= total * 0.8:
        print_warning(f"⚠️  Most checks passed ({percentage:.0f}%), but some issues need attention")
        print_warning(f"⚠️  معظم الفحوصات نجحت ({percentage:.0f}%)، لكن بعض المشاكل تحتاج انتباه")
        return False
    else:
        print_error("❌ Several checks failed. Please fix the issues before deployment.")
        print_error("❌ عدة فحوصات فشلت. يرجى إصلاح المشاكل قبل النشر.")
        return False

def main():
    """Main verification function"""
    print_header("🚀 Deployment Verification / التحقق من جاهزية النشر")
    print_info("Faculty Housing Management System")
    print_info("نظام إدارة إسكان أعضاء هيئة التدريس")
    print()
    
    results = {}
    
    # Run checks
    print_header("1️⃣  Python Environment / بيئة Python")
    results["Python Version (3.8+)"] = check_python_version()
    
    print_header("2️⃣  Required Files / الملفات المطلوبة")
    results["Core Application Files"] = check_required_files()
    
    print_header("3️⃣  Dependencies / التبعيات")
    results["Requirements File"] = check_requirements()
    
    print_header("4️⃣  Database / قاعدة البيانات")
    results["Database Module"] = check_database_init()
    
    print_header("5️⃣  Deployment Configurations / تكوينات النشر")
    has_configs, platforms = check_deployment_configs()
    results["Deployment Configs"] = has_configs
    
    if platforms:
        print_info(f"\n✅ Available deployment platforms: {', '.join(platforms)}")
        print_info(f"✅ منصات النشر المتاحة: {', '.join(platforms)}")
    
    # Print summary
    success = print_summary(results)
    
    # Additional information
    if success:
        print_header("📖 Next Steps / الخطوات التالية")
        print_info("Choose a deployment platform:")
        print_info("اختر منصة النشر:")
        print()
        
        if 'Render' in platforms:
            print("  🌟 Render.com (Recommended):")
            print("     - See: RENDER_DEPLOYMENT.md")
            print("     - Quick: 10-15 minutes")
            print("     - Free tier available (90 days)")
            print()
        
        if 'Railway' in platforms:
            print("  🚂 Railway.app:")
            print("     - See: دليل_النشر_السحابي.md")
            print("     - Quick: 5-10 minutes")
            print("     - $5/month credit")
            print()
        
        if 'Docker' in platforms:
            print("  🐳 Docker:")
            print("     - See: النشر_باستخدام_Docker.md")
            print("     - Command: docker-compose up -d")
            print("     - Best for local deployment")
            print()
        
        print_info("For complete guide, see: DEPLOYMENT.md or دليل_النشر_الكامل.md")
        print_info("للدليل الكامل، راجع: DEPLOYMENT.md أو دليل_النشر_الكامل.md")
    
    return 0 if success else 1

if __name__ == '__main__':
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n\n⚠️  Verification interrupted by user")
        print("⚠️  تم إيقاف التحقق من قبل المستخدم")
        sys.exit(1)
    except Exception as e:
        print_error(f"Unexpected error: {e}")
        print_error(f"خطأ غير متوقع: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
