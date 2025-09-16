# 🛡️ VirusTotal IP Analyzer

A comprehensive network security tool that scans external IP connections, analyzes them using VirusTotal API, and provides IP blocking capabilities across Windows and Linux systems.

![Python](https://img.shields.io/badge/python-v3.8+-blue.svg)
![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20Linux-lightgrey.svg)
![License](https://img.shields.io/badge/license-GPL%20v3-green.svg)

## 🚀 Quick Start

### Option 1: Use Pre-built Executables

1. **Download** the appropriate executable from the `dist/` folder:

    - **Windows**: `dist/VirusTotal-IP-Analyzer-Windows.exe`
    - **Linux**: `dist/linux/virustotal-ip-analyzer-linux`

2. **Run** the executable:

    - **Windows**: Double-click the .exe file
    - **Linux**: `./dist/linux/virustotal-ip-analyzer-linux`

3. **Set API Key**: Click "🔑 Set/Update API Key" and enter your VirusTotal API key

4. **Start Scanning**: Click "🚀 Start Scan" to begin analysis

### Option 2: Run from Source

#### Using Run Scripts

**Windows:**

```cmd
# Double-click or run from command prompt
scripts\run_windows.bat
```

**Linux:**

```bash
# Make executable and run
chmod +x scripts/run_linux.sh
bash scripts/run_linux.sh
```

#### Manual Setup

```bash
# Clone the repository
git clone https://github.com/mat-heidemann/VirusTotal-IP-Analyzer
cd VirusTotal-IP-Analyzer

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the application
python main.py
```

## 🔧 Building Executables

### Windows

```batch
# Run the build script
scripts\build_windows.bat
```

### Linux

```bash
# Make executable and run
chmod +x scripts/build_linux.sh
bash scripts/build_linux.sh
```

**Output locations:**

-   Windows: `dist/VirusTotal-IP-Analyzer-Windows.exe`
-   Linux: `dist/linux/virustotal-ip-analyzer-linux`

For detailed build instructions, see [docs/BUILD_INSTRUCTIONS.md](docs/BUILD_INSTRUCTIONS.md).

## 📁 Project Structure

```
VirusTotal-IP-Analyzer/
├── main.py                                 # Application entry point
├── requirements.txt                        # Python dependencies
├── VirusTotal-IP-Analyzer.spec             # PyInstaller build configuration
├── README.md                               # This file
├── TROUBLESHOOTING.md                      # Common issues and solutions
├── assets/                                 # Application assets
│   ├── icon.ico                            # Windows icon
│   └── icon.png                            # Linux icon
├── docs/                                   # Documentation
│   ├── BUILD_INSTRUCTIONS.md               # Detailed build guide
│   ├── PROJECT_STRUCTURE.md                # Architecture documentation
│   └── README.md                           # Original documentation
├── scripts/                                # Build and run scripts
│   ├── build_windows.bat                   # Windows build script
│   ├── build_linux.sh                      # Linux build script
│   ├── run_windows.bat                     # Windows run script
│   ├── run_linux.sh                        # Linux run script (enhanced)
│   └── run.sh                              # Linux run script (simple)
├── src/                                    # Source code
│   ├── core/                               # Core functionality
│   │   ├── api_client.py                   # VirusTotal API integration
│   │   ├── cache_manager.py                # Data persistence and caching
│   │   ├── config.py                       # Application configuration
│   │   ├── encryption.py                   # API key encryption/decryption
│   │   ├── ip_blocker.py                   # Cross-platform IP blocking
│   │   ├── network_scanner.py              # Network connection detection
│   │   └── scanner.py                      # Scan coordination and management
│   └── gui/                                # User interface components
│       ├── api_key_dialog.py               # API key management dialog
│       ├── custom_dialogs.py               # Custom themed dialogs
│       ├── main_window.py                  # Main application window
│       ├── results_window.py               # Scan results display
│       └── utils.py                        # GUI utility functions
├── tests/                                  # Test files
│   └── test_network_scan.py                # Network scanning tests
└── dist/                                   # Built executables (after building)
    ├── VirusTotal-IP-Analyzer-Windows.exe  # Windows executable
    └── linux/
        └── virustotal-ip-analyzer-linux    # Linux executable
```

## 📋 Requirements

### System Requirements

-   **Python 3.8+** (for source installation)
-   **Internet connection** (for VirusTotal API)
-   **Administrator/sudo privileges** (for IP blocking features)

### Dependencies

-   `customtkinter>=5.2.0` - Modern GUI framework
-   `requests>=2.31.0` - HTTP client for API calls
-   `cryptography>=41.0.0` - API key encryption

## 🔑 VirusTotal API Key

1. **Get API Key**: Register at [VirusTotal](https://www.virustotal.com/) and get your free API key
2. **Set in Application**: Use the "🔑 Set/Update API Key" button in the GUI
3. **Secure Storage**: API keys are encrypted and stored securely

## 🛠️ Configuration

### Application Settings

-   **Windows**: `%APPDATA%\VT_IP_Analyzer\`
-   **Linux**: `~/.config/vt-ip-analyzer/`

### Configuration Files

-   `encrypted_api_key.key` - Encrypted VirusTotal API key
-   `cache.json` - Cached scan results
-   `blocked_ips.json` - List of blocked IP addresses

## 🔧 Development

### Available Scripts

| Script                      | Platform | Purpose                    |
| --------------------------- | -------- | -------------------------- |
| `scripts/build_windows.bat` | Windows  | Build Windows executable   |
| `scripts/build_linux.sh`    | Linux    | Build Linux executable     |
| `scripts/run_windows.bat`   | Windows  | Run from source (enhanced) |
| `scripts/run_linux.sh`      | Linux    | Run from source (enhanced) |

### Development Setup

```bash
git clone https://github.com/mat-heidemann/VirusTotal-IP-Analyzer
cd VirusTotal-IP-Analyzer
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
python main.py
```

### Building Process

The build process uses PyInstaller with a unified `.spec` file that handles both Windows and Linux builds:

1. **Creates virtual environment** in appropriate location
2. **Installs dependencies** including PyInstaller
3. **Builds executable** using platform-specific settings
4. **Handles permissions** and WSL limitations
5. **Provides detailed feedback** throughout the process

## 📄 License

This project is licensed under the GNU General Public License v3.0 - see the LICENSE file for details.

## 📞 Support

For support, please:

1. Check the [TROUBLESHOOTING.md](TROUBLESHOOTING.md) for common issues
2. Review the [docs/BUILD_INSTRUCTIONS.md](docs/BUILD_INSTRUCTIONS.md) for build issues
3. Open an issue on the [project repository](https://github.com/mat-heidemann/VirusTotal-IP-Analyzer)

---

**⚠️ Disclaimer**: This tool is for legitimate security analysis only. Users are responsible for complying with applicable laws and regulations when using IP blocking features.

**🔗 Repository**: https://github.com/mat-heidemann/VirusTotal-IP-Analyzer
