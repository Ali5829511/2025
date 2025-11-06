#!/bin/bash
echo "🔍 Final Deployment Verification"
echo "================================"
echo ""

errors=0

# Check all configuration files exist
echo "✓ Checking configuration files..."
files=("render.yaml" "gunicorn_config.py" "database_adapter.py" "init_db.py" 
       "railway.json" "nixpacks.toml" "Procfile" "runtime.txt")

for file in "${files[@]}"; do
    if [ -f "$file" ]; then
        echo "  ✅ $file"
    else
        echo "  ❌ $file MISSING"
        ((errors++))
    fi
done

# Check documentation files
echo ""
echo "✓ Checking documentation..."
docs=("RENDER_DEPLOYMENT.md" "CLOUD_HOSTING_OPTIONS.md" 
      "دليل_النشر_السحابي.md" "DEPLOYMENT_SUMMARY.md")

for doc in "${docs[@]}"; do
    if [ -f "$doc" ]; then
        echo "  ✅ $doc"
    else
        echo "  ❌ $doc MISSING"
        ((errors++))
    fi
done

# Check Python files syntax
echo ""
echo "✓ Checking Python syntax..."
python_files=("gunicorn_config.py" "database_adapter.py" "init_db.py")
for pyfile in "${python_files[@]}"; do
    if python3 -m py_compile "$pyfile" 2>/dev/null; then
        echo "  ✅ $pyfile syntax valid"
    else
        echo "  ❌ $pyfile syntax error"
        ((errors++))
    fi
done

# Check YAML syntax
echo ""
echo "✓ Checking YAML syntax..."
if python3 -c "import yaml; yaml.safe_load(open('render.yaml'))" 2>/dev/null; then
    echo "  ✅ render.yaml valid"
else
    echo "  ❌ render.yaml invalid"
    ((errors++))
fi

# Check requirements.txt
echo ""
echo "✓ Checking requirements.txt..."
if grep -q "gunicorn" requirements.txt && grep -q "psycopg2-binary" requirements.txt; then
    echo "  ✅ Production dependencies included"
else
    echo "  ❌ Missing production dependencies"
    ((errors++))
fi

# Final summary
echo ""
echo "================================"
if [ $errors -eq 0 ]; then
    echo "✅ ALL CHECKS PASSED!"
    echo ""
    echo "🚀 System is ready for deployment!"
    echo ""
    echo "Next steps:"
    echo "1. Read: دليل_النشر_السحابي.md"
    echo "2. Choose: Render.com (recommended)"
    echo "3. Deploy: Follow RENDER_DEPLOYMENT.md"
    echo ""
    exit 0
else
    echo "❌ $errors ERROR(S) FOUND"
    echo "Please fix the errors before deploying"
    exit 1
fi
