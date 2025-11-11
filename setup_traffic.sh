#!/bin/bash
# Traffic System Quick Start Script
# سكريبت البدء السريع لنظام المخالفات

echo "🚀 Starting Traffic Violations System Setup..."
echo ""

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

echo "✅ Python found: $(python3 --version)"

# Install dependencies
echo ""
echo "📦 Installing dependencies..."
pip3 install flask flask-cors python-dotenv requests pillow -q

if [ $? -eq 0 ]; then
    echo "✅ Dependencies installed successfully"
else
    echo "❌ Failed to install dependencies"
    exit 1
fi

# Initialize database
echo ""
echo "🗄️ Initializing database..."
python3 init_traffic_db.py

if [ $? -eq 0 ]; then
    echo "✅ Database initialized successfully"
else
    echo "❌ Failed to initialize database"
    exit 1
fi

# Check for .env file
echo ""
if [ -f .env ]; then
    echo "✅ .env file found"
else
    echo "⚠️ .env file not found. Creating from template..."
    cp .env.traffic.example .env
    echo "📝 Please edit .env file and add your PLATE_RECOGNIZER_API_TOKEN"
fi

# Start application
echo ""
echo "🎉 Setup completed successfully!"
echo ""
echo "To start the application, run:"
echo "  python3 traffic_app.py"
echo ""
echo "Then open your browser at:"
echo "  http://localhost:5001"
echo ""
echo "📖 For more information, see:"
echo "  - TRAFFIC_COMPLETE_README.md"
echo "  - QUICK_START_TRAFFIC.md"
echo "  - TRAFFIC_DEPLOYMENT_GUIDE.md"
echo ""
