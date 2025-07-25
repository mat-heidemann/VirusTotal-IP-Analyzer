#!/bin/bash

set -e  # Exit on any error

echo "========================================"
echo " VirusTotal IP Analyzer - Linux Build"
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

# === Create venv in temp directory to avoid WSL permission issues ===
echo -e "\n${YELLOW}🔄 Creating virtual environment in temp directory...${NC}"
TEMP_VENV="/tmp/virustotal_build_venv"
rm -rf "$TEMP_VENV"
$PYTHON -m venv "$TEMP_VENV" || {
    echo -e "${RED}❌ Failed to create virtual environment.${NC}"
    exit 1
}

# === Activate venv ===
echo -e "\n${YELLOW}🚀 Activating virtual environment...${NC}"
source "$TEMP_VENV/bin/activate"

# === Ensure pip is available ===
echo -e "\n${YELLOW}📦 Ensuring pip is available...${NC}"
if ! command -v pip &> /dev/null; then
    echo -e "${YELLOW}Installing pip via ensurepip...${NC}"
    set +e  # Temporarily disable exit on error
    $PYTHON -m ensurepip --upgrade
    if [ $? -ne 0 ]; then
        echo -e "${YELLOW}ensurepip failed, trying to install pip manually...${NC}"
        # Download and install pip manually
        curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
        $PYTHON get-pip.py
        rm get-pip.py
    fi
    set -e  # Re-enable exit on error
fi
echo -e "${GREEN}✔ pip available: $(pip --version)${NC}"

# === Install dependencies ===
echo -e "\n${YELLOW}📦 Installing requirements...${NC}"
pip install --upgrade pip
pip install -r requirements.txt

# === Install PyInstaller ===
echo -e "\n${YELLOW}🛠️ Installing PyInstaller...${NC}"
pip install pyinstaller

# === Clean previous build artifacts ===
echo -e "\n${YELLOW}🧹 Cleaning old build files...${NC}"
rm -rf dist/ build/

# === Build executable ===
echo -e "\n${YELLOW}🏗️ Building Linux executable...${NC}"
set +e  # Temporarily disable exit on error for permission issues
pyinstaller \
    --distpath "dist/linux" \
    --workpath "build" \
    --noconfirm \
    --clean \
    VirusTotal-IP-Analyzer.spec
BUILD_EXIT_CODE=$?
set -e  # Re-enable exit on error

# Check if build succeeded despite permission warnings
if [ $BUILD_EXIT_CODE -ne 0 ]; then
    echo -e "${YELLOW}⚠️ PyInstaller reported errors, but checking if executable was created...${NC}"
fi

# === Check result ===
echo -e "\n${YELLOW}🔍 Verifying build...${NC}"
if [ -f "dist/linux/virustotal-ip-analyzer-linux" ]; then
    echo -e "${GREEN}✅ BUILD SUCCESSFUL!${NC}"
    echo "Executable: dist/linux/virustotal-ip-analyzer-linux"
    size=$(stat -c%s "dist/linux/virustotal-ip-analyzer-linux" 2>/dev/null || stat -f%z "dist/linux/virustotal-ip-analyzer-linux" 2>/dev/null)
    echo "Size: $size bytes"
    # Try to set permissions, but don't fail if it doesn't work (WSL issue)
    if chmod +x "dist/linux/virustotal-ip-analyzer-linux" 2>/dev/null; then
        echo -e "${GREEN}✔ Permissions set${NC}"
    else
        echo -e "${YELLOW}⚠️ Could not set permissions (WSL limitation), but file should already be executable${NC}"
    fi
else
    echo -e "${RED}❌ BUILD FAILED!${NC}"
    exit 1
fi

# === Cleanup ===
echo -e "\n${YELLOW}🧹 Cleaning temporary files...${NC}"
rm -rf build/

# === Optional: remove venv ===
echo -e "${YELLOW}🗑️ Removing virtual environment...${NC}"
rm -rf "$TEMP_VENV"

echo -e "\n${GREEN}🎉 Build process completed successfully!${NC}"
