# 🚀 Build Instructions - VirusTotal IP Analyzer

This document provides comprehensive instructions for building single executable files for Windows and Linux.

## 📋 Prerequisites

### General Requirements
- **Python 3.8+** installed and accessible from command line
- **Git** (optional, for cloning the repository)
- **Internet connection** (for downloading dependencies)

### Windows Requirements
- **Windows 10/11** or **Windows Server 2016+**
- **Python 3.8+** with pip
- **Visual Studio Build Tools** (usually installed with Python)

### Linux Requirements
- **Ubuntu 18.04+**, **CentOS 7+**, or equivalent Linux distribution
- **Python 3.8+** with pip and venv
- **Development tools**: `sudo apt install build-essential` (Ubuntu/Debian)

## 🔧 Quick Build Guide

### Windows Build
```batch
# Simply run the build script
build_windows.bat
```

### Linux Build
```bash
# Make script executable (if not already)
chmod +x build_linux.sh

# Run the build script
./build_linux.sh
```

## 📁 Output Files

After successful build, you'll find:

### Windows
- **Location**: `dist/windows/VirusTotal-IP-Analyzer-Windows.exe`
- **Size**: ~50-80 MB
- **Type**: Single executable file (.exe)
- **Dependencies**: None (all bundled)

### Linux
- **Location**: `dist/linux/virustotal-ip-analyzer-linux`
- **Size**: ~60-90 MB
- **Type**: Single binary executable
- **Dependencies**: None (all bundled)

## 🛠️ Manual Build Process

If you prefer to build manually or need to customize the build:

### 1. Setup Environment
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
pip install pyinstaller
```

### 2. Build Command

**Windows:**
```batch
pyinstaller --onefile --windowed --icon=icon.ico --hidden-import=customtkinter --hidden-import=requests --hidden-import=cryptography --hidden-import=tkinter --add-data "gui;gui" --name "VirusTotal-IP-Analyzer-Windows" --distpath "dist/windows" main.py
```

**Linux:**
```bash
pyinstaller --onefile --icon=icon.ico --hidden-import=customtkinter --hidden-import=requests --hidden-import=cryptography --hidden-import=tkinter --add-data "gui:gui" --name "virustotal-ip-analyzer-linux" --distpath "dist/linux" main.py
```

## 🎯 Build Options Explained

### PyInstaller Flags
- `--onefile`: Creates a single executable file
- `--windowed`: Hides console window (Windows only)
- `--hidden-import`: Ensures modules are included even if not detected
- `--add-data`: Includes additional files/folders
- `--name`: Sets the executable name
- `--distpath`: Sets output directory

### Hidden Imports
These modules are explicitly included because PyInstaller might not detect them automatically:
- `customtkinter`: GUI framework
- `requests`: HTTP client for VirusTotal API
- `cryptography`: For API key encryption
- `tkinter`: Base GUI toolkit

### Icon Support
- **Windows**: The `icon.ico` file is embedded in the .exe and shows in Windows Explorer and taskbar
- **Linux**: Icons are not embedded in executables (PyInstaller limitation), but the build includes the icon flag for consistency
- **macOS**: Icons are supported and embedded in .app bundles

## 🔍 Troubleshooting

### Common Issues

#### "Python not found"
- **Windows**: Install Python from python.org, ensure "Add to PATH" is checked
- **Linux**: Install with `sudo apt install python3 python3-pip python3-venv`

#### "Permission denied" (Linux)
```bash
chmod +x build_linux.sh
chmod +x dist/linux/virustotal-ip-analyzer-linux
```

#### "Module not found" during build
- Ensure all dependencies are installed: `pip install -r requirements.txt`
- Check virtual environment is activated

#### Large executable size
- This is normal for PyInstaller builds (includes Python runtime)
- Typical size: 50-90 MB

#### Build fails on older systems
- Ensure Python 3.8+ is installed
- Update pip: `pip install --upgrade pip`
- Update setuptools: `pip install --upgrade setuptools`

### Advanced Troubleshooting

#### Debug build issues
```bash
# Add verbose flag to see detailed output
pyinstaller --onefile --debug=all main.py
```

#### Check dependencies
```bash
# List all installed packages
pip list

# Check for missing modules
python -c "import customtkinter, requests, cryptography; print('All modules available')"
```

## 📦 Distribution

### Windows Distribution
1. Copy `VirusTotal-IP-Analyzer-Windows.exe` to target system
2. No additional installation required
3. May trigger Windows Defender (add exception if needed)

### Linux Distribution
1. Copy `virustotal-ip-analyzer-linux` to target system
2. Make executable: `chmod +x virustotal-ip-analyzer-linux`
3. Run with: `./virustotal-ip-analyzer-linux`

## 🔒 Security Notes

### Code Signing (Optional)
For production distribution, consider code signing:

**Windows:**
- Use `signtool.exe` with a valid certificate
- Prevents "Unknown Publisher" warnings

**Linux:**
- GPG signing for package integrity
- Consider creating .deb/.rpm packages

### Antivirus False Positives
- PyInstaller executables may trigger antivirus warnings
- This is common and usually safe to ignore
- For distribution, consider submitting to antivirus vendors

## 🧪 Testing Built Executables

### Basic Functionality Test
1. **Launch**: Double-click (Windows) or `./executable` (Linux)
2. **GUI**: Verify dark theme loads correctly
3. **Network Scan**: Test network scanning (no API key needed)
4. **Settings**: Check configuration folder access

### Full Feature Test
1. **API Key**: Set VirusTotal API key
2. **Scan**: Perform full IP scan
3. **Results**: View and interact with results
4. **Export**: Export to CSV
5. **Blocking**: Test IP blocking (requires admin/sudo)

## 📊 Build Performance

### Typical Build Times
- **Windows**: 2-5 minutes
- **Linux**: 2-4 minutes

### System Requirements for Building
- **RAM**: 2GB minimum, 4GB recommended
- **Disk Space**: 500MB free space
- **CPU**: Any modern processor

## 🆘 Support

If you encounter issues:

1. **Check Prerequisites**: Ensure Python 3.8+ is installed
2. **Update Dependencies**: `pip install --upgrade -r requirements.txt`
3. **Clean Build**: Delete `dist/`, `build/`, `*.spec` and rebuild
4. **Check Logs**: Review build output for specific error messages

## 📝 Build Script Features

### Windows Script (`build_windows.bat`)
- ✅ Automatic Python detection
- ✅ Virtual environment management
- ✅ Dependency installation
- ✅ Build success/failure reporting
- ✅ Automatic cleanup
- ✅ File size reporting

### Linux Script (`build_linux.sh`)
- ✅ Colored output for better readability
- ✅ Cross-platform stat command support
- ✅ Automatic executable permissions
- ✅ Error handling and exit codes
- ✅ Build artifact cleanup

Both scripts are designed to be run multiple times safely and will handle existing virtual environments and previous builds automatically.
