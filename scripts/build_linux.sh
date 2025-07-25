#!/bin/bash

echo "========================================"
echo " VirusTotal IP Analyzer - Linux Build"
echo "========================================"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}ERROR: Python3 is not installed or not in PATH${NC}"
    exit 1
fi

echo -e "${YELLOW}Python version:${NC}"
python3 --version

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo -e "${YELLOW}Creating virtual environment...${NC}"
    python3 -m venv venv
fi

# Activate virtual environment
echo -e "${YELLOW}Activating virtual environment...${NC}"
source venv/bin/activate

# Install dependencies
echo -e "${YELLOW}Installing dependencies...${NC}"
pip install -r requirements.txt

# Install PyInstaller
echo -e "${YELLOW}Installing PyInstaller...${NC}"
pip install pyinstaller

# Clean previous builds
echo -e "${YELLOW}Cleaning previous builds...${NC}"
rm -rf dist/
rm -rf build/
rm -f *.spec

# Build executable
echo -e "${YELLOW}Building Linux executable...${NC}"
pyinstaller \
    --onefile \
    --icon=icon.ico \
    --hidden-import=customtkinter \
    --hidden-import=requests \
    --hidden-import=cryptography \
    --hidden-import=tkinter \
    --add-data "src:src" \
    --add-data "assets/icon.ico:assets" \
    --name "virustotal-ip-analyzer-linux" \
    --distpath "dist/linux" \
    main.py

# Check if build was successful
if [ -f "dist/linux/virustotal-ip-analyzer-linux" ]; then
    echo ""
    echo -e "${GREEN}========================================"
    echo " BUILD SUCCESSFUL!"
    echo "========================================${NC}"
    echo "Executable created: dist/linux/virustotal-ip-analyzer-linux"
    
    # Get file size
    size=$(stat -c%s "dist/linux/virustotal-ip-analyzer-linux" 2>/dev/null || stat -f%z "dist/linux/virustotal-ip-analyzer-linux" 2>/dev/null)
    echo "Size: $size bytes"
    
    # Make executable
    chmod +x "dist/linux/virustotal-ip-analyzer-linux"
    echo "Permissions: Executable set"
    
    echo ""
    echo "You can now distribute this single binary file!"
    echo "To run: ./dist/linux/virustotal-ip-analyzer-linux"
    echo ""
else
    echo ""
    echo -e "${RED}========================================"
    echo " BUILD FAILED!"
    echo "========================================${NC}"
    echo "Check the output above for errors."
    exit 1
fi

# Clean up build artifacts
echo -e "${YELLOW}Cleaning up build artifacts...${NC}"
rm -rf build/
rm -f *.spec

echo -e "${GREEN}Build process completed!${NC}"
