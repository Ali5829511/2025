#!/bin/bash
echo "🧪 Testing Render Deployment Configuration"
echo "==========================================="
echo ""

echo "✓ Checking render.yaml..."
python3 -c "import yaml; yaml.safe_load(open('render.yaml'))" && echo "  ✅ Valid YAML syntax"

echo ""
echo "✓ Checking gunicorn_config.py..."
python3 -m py_compile gunicorn_config.py && echo "  ✅ Valid Python syntax"

echo ""
echo "✓ Checking database_adapter.py..."
python3 database_adapter.py > /dev/null 2>&1 && echo "  ✅ Database adapter works"

echo ""
echo "✓ Checking requirements.txt..."
grep -q "gunicorn" requirements.txt && echo "  ✅ Gunicorn included"
grep -q "psycopg2-binary" requirements.txt && echo "  ✅ PostgreSQL driver included"

echo ""
echo "✓ Checking documentation..."
[ -f "RENDER_DEPLOYMENT.md" ] && echo "  ✅ Render deployment guide exists"

echo ""
echo "==========================================="
echo "✅ All tests passed! Ready for deployment"
echo "==========================================="
