#!/bin/bash
# Quick start script for Traffic Violations System
# سكريبت بدء سريع لنظام المخالفات المرورية

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}============================================================${NC}"
echo -e "${BLUE}🚀 نظام إدارة المخالفات المرورية - بدء سريع${NC}"
echo -e "${BLUE}🚀 Traffic Violations System - Quick Start${NC}"
echo -e "${BLUE}============================================================${NC}"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python 3 is not installed. Please install Python 3.8 or later.${NC}"
    exit 1
fi

echo -e "${GREEN}✅ Python found: $(python3 --version)${NC}"

# Check if pip is installed
if ! command -v pip3 &> /dev/null && ! command -v pip &> /dev/null; then
    echo -e "${RED}❌ pip is not installed. Please install pip.${NC}"
    exit 1
fi

echo -e "${GREEN}✅ pip found${NC}"

# Install dependencies
echo -e "\n${YELLOW}📦 Installing dependencies...${NC}"
pip3 install -q flask flask-cors python-dotenv requests pillow gunicorn colorama 2>&1 | grep -v "already satisfied" || true
echo -e "${GREEN}✅ Dependencies installed${NC}"

# Initialize database
echo -e "\n${YELLOW}🗄️  Initializing database...${NC}"
if [ -f "traffic.db" ]; then
    echo -e "${YELLOW}⚠️  Database already exists. Skipping initialization.${NC}"
else
    python3 init_traffic_db.py
    echo -e "${GREEN}✅ Database initialized${NC}"
fi

# Set default port
PORT=${PORT:-10000}

echo -e "\n${BLUE}============================================================${NC}"
echo -e "${GREEN}✅ Setup complete!${NC}"
echo -e "${BLUE}============================================================${NC}"
echo ""
echo -e "${YELLOW}Choose how to start the server:${NC}"
echo ""
echo -e "  1️⃣  ${GREEN}Development mode (Flask)${NC}"
echo -e "      python3 traffic_app.py"
echo ""
echo -e "  2️⃣  ${GREEN}Production mode (Gunicorn) - RECOMMENDED${NC}"
echo -e "      PORT=$PORT gunicorn --config gunicorn_traffic_config.py traffic_app:app"
echo ""
echo -e "  3️⃣  ${GREEN}Run health check tests${NC}"
echo -e "      python3 test_traffic_health.py http://localhost:$PORT"
echo ""
echo -e "${BLUE}============================================================${NC}"
echo ""

# Ask user what to do
read -p "$(echo -e ${YELLOW}Would you like to start the server now? [y/N]: ${NC})" -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo ""
    echo -e "${GREEN}🚀 Starting server in production mode...${NC}"
    echo ""
    PORT=$PORT gunicorn --config gunicorn_traffic_config.py traffic_app:app
fi
