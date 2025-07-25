#!/bin/bash

set -e  # Exit on any error

echo "========================================"
echo " VirusTotal IP Analyzer - Linux Runner"
echo "========================================"

# === Color definitions ===
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

cd "$(dirname "$0")/.."
echo -e "${YELLOW}→ Switched to project root: $(pwd)${NC}"

# === Check if python3 is installed ===
echo -e "\n${YELLOW}🔍 Checking for Python 3...${NC}"
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python 3 is not installed.${NC}"
    exit 1
fi

PYTHON=python3
PYTHON_VERSION=$($PYTHON -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
echo -e "${GREEN}✔ Python $PYTHON_VERSION detected${NC}"

# === Check for working venv ===
echo -e "\n${YELLOW}🔧 Checking if 'venv' module is available...${NC}"
if ! $PYTHON -m venv --help > /dev/null 2>&1; then
    echo -e "${YELLOW}Installing 'python3-venv'...${NC}"
    sudo apt update
    sudo apt install -y python3-venv || {
        echo -e "${RED}❌ Failed to install python3-venv. Aborting.${NC}"
        exit 1
    }
fi

# === Check if virtual environment exists ===
if [ ! -d "venv" ]; then
    echo -e "\n${YELLOW}📦 Virtual environment not found. Creating...${NC}"
    $PYTHON -m venv venv || {
        echo -e "${RED}❌ Failed to create virtual environment.${NC}"
        exit 1
    }
    
    echo -e "\n${YELLOW}🚀 Activating virtual environment...${NC}"
    source venv/bin/activate
    
    echo -e "\n${YELLOW}📦 Installing dependencies...${NC}"
    pip install --upgrade pip
    pip install -r requirements.txt || {
        echo -e "${RED}❌ Failed to install dependencies.${NC}"
        exit 1
    }
    echo -e "${GREEN}✔ Dependencies installed successfully${NC}"
else
    echo -e "\n${YELLOW}🚀 Activating existing virtual environment...${NC}"
    source venv/bin/activate
    echo -e "${GREEN}✔ Virtual environment activated${NC}"
fi

# === Run the application ===
echo -e "\n${GREEN}🎯 Starting VirusTotal IP Analyzer...${NC}"
echo "========================================"
python main.py
