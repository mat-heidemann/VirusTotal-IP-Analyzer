# 🚀 Build Instructions - VirusTotal IP Analyzer

This document provides comprehensive instructions for building single executable files for Windows and Linux using the enhanced build scripts.

## 📋 Prerequisites

### General Requirements
- **Python 3.8+** installed and accessible from command line
- **Git** (optional, for cloning the repository)
- **Internet connection** (for downloading dependencies)

### Windows Requirements
- **Windows 10/11** or **Windows Server 2016+**
- **Python 3.8+** with pip and venv module
- **Visual Studio Build Tools** (usually installed with Python)

### Linux Requirements
- **Ubuntu 18.04+**, **CentOS 7+**, or equivalent Linux distribution
- **Python 3.8+** with pip and venv
- **Development tools**: `sudo apt install build-essential` (Ubuntu/Debian)
- **WSL Support**: Full compatibility with Windows Subsystem for Linux

## 🔧 Quick Build Guide

### Windows Build
```batch
# Simply run the enhanced build script
scripts\build_windows.bat
```

### Linux Build
```bash
# Make script executable and run
chmod +x scripts/build_linux.sh
bash scripts/build_linux.sh
```

## 📁 Output Files

After successful build, you'll find:

### Windows
- **Location**: `dist/VirusTotal-IP-Analyzer-Windows.exe`
- **Size**: ~50-80 MB
- **Type**: Single executable file (.exe)
- **Dependencies**: None (all bundled)
- **Console**: Hidden (windowed mode)

### Linux
- **Location**: `dist/linux/virustotal-ip-analyzer-linux`
- **Size**: ~56 KB (optimized build)
- **Type**: ELF 64-bit LSB executable
- **Dependencies**: None (all bundled)
- **Permissions**: Automatically set as executable

## 🛠️ Enhanced Build Scripts

### Windows Script Features (`scripts/build_windows.bat`)
- ✅ **Comprehensive Status Reporting**: ASCII-compatible progress indicators
- ✅ **Robust Error Handling**: Detailed error messages with troubleshooting hints
- ✅ **Automatic Environment Management**: Creates/manages virtual environments
- ✅ **Dependency Validation**: Checks Python, pip, and venv availability
- ✅ **Build Verification**: Confirms executable creation and reports file size
- ✅ **Automatic Cleanup**: Removes temporary build files
- ✅ **User-Friendly Output**: Clear progress indicators and success/failure messages

### Linux Script Features (`scripts/build_linux.sh`)
- ✅ **Colored Output**: Professional colored terminal output with emojis
- ✅ **WSL Compatibility**: Handles Windows Subsystem for Linux limitations
- ✅ **Smart Environment Setup**: Creates virtual environment in `/tmp` for WSL compatibility
- ✅ **Permission Handling**: Gracefully handles WSL permission limitations
- ✅ **Comprehensive Error Handling**: Detailed error messages and recovery suggestions
- ✅ **Build Verification**: Confirms ELF executable creation with file type detection
- ✅ **Automatic Cleanup**: Removes temporary files and virtual environments

## 🎯 Unified Build Configuration

Both platforms use the same **`VirusTotal-IP-Analyzer.spec`** file for consistent builds:

### Key Features
- **Platform Detection**: Automatically detects Windows vs Linux
- **Optimized Settings**: Platform-specific optimizations
- **Icon Handling**: Proper icon embedding for Windows
- **Data Files**: Includes all necessary assets and GUI components
- **Hidden Imports**: Ensures all dependencies are included

### Spec File Highlights
```python
# Platform-aware executable naming
exe_name = 'VirusTotal-IP-Analyzer-Windows.exe' if is_windows else 'virustotal-ip-analyzer-linux'

# Platform-specific console settings
console = False if is_windows else True

# Icon handling
icon = 'assets/icon.ico' if is_windows else None
```

## 🔍 Build Process Details

### 1. Environment Setup
- **Virtual Environment**: Created automatically in appropriate location
- **Dependencies**: Installed from `requirements.txt`
- **PyInstaller**: Installed automatically during build process

### 2. Build Execution
- **Spec File**: Uses unified `.spec` configuration
- **Platform Detection**: Automatically configures for target platform
- **Asset Inclusion**: Bundles icons, GUI files, and other resources
- **Optimization**: Applies platform-specific optimizations

### 3. Verification
- **File Creation**: Confirms executable was created successfully
- **File Type**: Verifies correct executable format (PE for Windows, ELF for Linux)
- **Size Reporting**: Shows final executable size
- **Permission Setting**: Sets executable permissions (Linux)

## 🛡️ Error Handling and Recovery

### Windows Build Issues
```
[X] Python is not installed or not in PATH.
```
**Solution**: Install Python from python.org, ensure "Add to PATH" is checked

```
[X] Python venv module is not available.
```
**Solution**: Reinstall Python with full standard library or run `pip install virtualenv`

```
[X] Failed to install requirements.
```
**Solution**: Check internet connection, update pip with `pip install --upgrade pip`

### Linux Build Issues
```
❌ Python 3 is not installed.
```
**Solution**: Install with `sudo apt install python3 python3-pip python3-venv`

```
⚠️ Could not set permissions (WSL limitation)
```
**Solution**: This is normal in WSL, the file is still executable

```
❌ Failed to create virtual environment.
```
**Solution**: Ensure python3-venv is installed: `sudo apt install python3-venv`

## 🚀 Manual Build Process

If you need to customize the build or troubleshoot issues:

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

### 2. Build Using Spec File
```bash
# Use the unified spec file
pyinstaller --distpath "dist" --workpath "build" --noconfirm --clean VirusTotal-IP-Analyzer.spec
```

## 📦 Distribution

### Windows Distribution
1. **Single File**: Copy `dist/VirusTotal-IP-Analyzer-Windows.exe` to target system
2. **No Installation**: No additional installation required
3. **Antivirus**: May trigger Windows Defender (add exception if needed)
4. **Dependencies**: All dependencies bundled, no Python installation required

### Linux Distribution
1. **Single File**: Copy `dist/linux/virustotal-ip-analyzer-linux` to target system
2. **Permissions**: File is automatically executable
3. **Dependencies**: All dependencies bundled, no Python installation required
4. **Compatibility**: Works on most modern Linux distributions

## 🧪 Testing Built Executables

### Automated Testing
The build scripts automatically perform basic validation:
- **File Creation**: Confirms executable exists
- **File Type**: Verifies correct executable format
- **Size Check**: Reports file size for validation

### Manual Testing
1. **Launch Test**: 
   - Windows: Double-click the .exe file
   - Linux: Run `./dist/linux/virustotal-ip-analyzer-linux`
2. **GUI Test**: Verify the dark theme interface loads
3. **Network Test**: Test network scanning functionality
4. **API Test**: Set VirusTotal API key and perform scan

## 📊 Build Performance

### Typical Build Times
- **Windows**: 3-5 minutes (including dependency installation)
- **Linux**: 2-4 minutes (including dependency installation)
- **WSL**: 3-6 minutes (due to filesystem overhead)

### System Requirements for Building
- **RAM**: 2GB minimum, 4GB recommended
- **Disk Space**: 1GB free space (for virtual environment and build artifacts)
- **CPU**: Any modern processor (build is I/O intensive)

## 🔒 Security Considerations

### Code Signing (Production)
For production distribution, consider:
- **Windows**: Use `signtool.exe` with valid certificate
- **Linux**: GPG signing for package integrity

### Antivirus Compatibility
- PyInstaller executables may trigger false positives
- Consider submitting to antivirus vendors for whitelisting
- Users may need to add exceptions

## 🆘 Troubleshooting

### Build Script Debugging
Both scripts provide detailed output. If issues persist:

1. **Check Prerequisites**: Ensure Python 3.8+ is properly installed
2. **Update Tools**: Run `pip install --upgrade pip setuptools`
3. **Clean Build**: Delete `dist/`, `build/`, and `venv/` directories
4. **Manual Build**: Try the manual build process above
5. **Check Logs**: Review the detailed build output for specific errors

### Common Solutions
- **Permission Issues**: Run as administrator (Windows) or with sudo (Linux)
- **Network Issues**: Check firewall and proxy settings
- **Space Issues**: Ensure adequate disk space (1GB minimum)
- **Python Issues**: Verify Python version with `python --version`

## 📝 Build Script Comparison

| Feature | Windows Script | Linux Script |
|---------|---------------|--------------|
| Progress Indicators | ASCII (`[*]`, `[+]`, `[X]`) | Colored Emojis |
| Error Handling | Comprehensive | Comprehensive |
| WSL Support | N/A | Full Support |
| Virtual Environment | Local `venv/` | Temp `/tmp/` |
| Cleanup | Automatic | Automatic |
| File Verification | Size + Existence | Size + Type + Existence |
| User Feedback | Detailed | Detailed + Colored |

## 🔄 Continuous Integration

For automated builds, both scripts support:
- **Exit Codes**: Proper success/failure exit codes
- **Logging**: Detailed output for CI systems
- **Cleanup**: Automatic cleanup of build artifacts
- **Verification**: Built-in executable verification

Example CI usage:
```bash
# Linux CI
chmod +x scripts/build_linux.sh
bash scripts/build_linux.sh
if [ $? -eq 0 ]; then echo "Build successful"; else echo "Build failed"; exit 1; fi

# Windows CI
scripts\build_windows.bat
if %errorlevel% equ 0 (echo Build successful) else (echo Build failed & exit /b 1)
```

## 📞 Support

For build-related issues:
1. **Check this guide** for common solutions
2. **Review build output** for specific error messages
3. **Try manual build** if scripts fail
4. **Open issue** on the project repository with build logs

---

**Note**: The build scripts are designed to be run multiple times safely and will handle existing virtual environments and previous builds automatically.
