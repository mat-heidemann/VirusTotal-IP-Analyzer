# 🛡️ VirusTotal IP Analyzer

A comprehensive network security tool that scans external IP connections, analyzes them using VirusTotal API, and provides IP blocking capabilities across Windows and Linux systems.

![Python](https://img.shields.io/badge/python-v3.8+-blue.svg)
![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20Linux-lightgrey.svg)
![License](https://img.shields.io/badge/license-GPL%20v3-green.svg)

## ✨ Features

### 🔍 **Network Analysis**
- **Real-time Network Scanning**: Automatically detects external IP connections
- **Cross-platform Support**: Works on Windows and Linux
- **Process Identification**: Shows which processes are connecting to external IPs
- **Smart Filtering**: Ignores local/private IP ranges and focuses on external threats

### 🌐 **VirusTotal Integration**
- **Comprehensive Analysis**: Queries VirusTotal database for IP reputation
- **Detailed Reports**: Shows malicious/suspicious/harmless engine counts
- **Community Votes**: Displays community-driven threat assessments
- **Geolocation Data**: Provides country and ASN information
- **Analysis History**: Shows last analysis dates and historical data

### 🚫 **IP Blocking System**
- **Multi-platform Blocking**: 
  - **Windows**: Uses Windows Firewall (netsh)
  - **Linux**: Uses iptables with sudo privileges
- **Persistent Rules**: Automatically saves firewall rules across reboots
- **Visual Indicators**: Blocked IPs show with 🚫 icons and red highlighting
- **Easy Management**: One-click block/unblock functionality

### 💾 **Data Management**
- **Smart Caching**: Avoids redundant API calls for known IPs
- **CSV Export**: Export results with customizable field selection
- **Persistent Storage**: Maintains scan history and blocked IP lists
- **Encrypted API Keys**: Secure storage using Fernet encryption

### 🎨 **Modern GUI**
- **Dark Theme**: Professional dark interface with CustomTkinter
- **Responsive Design**: Scales properly on different screen sizes
- **Real-time Logging**: Live scan progress with colored status messages
- **Custom Dialogs**: Consistent themed dialogs throughout the application
- **Intuitive Controls**: Easy-to-use interface with clear visual feedback

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

#### Using Run Scripts (Recommended)

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
- Windows: `dist/VirusTotal-IP-Analyzer-Windows.exe`
- Linux: `dist/linux/virustotal-ip-analyzer-linux`

For detailed build instructions, see [docs/BUILD_INSTRUCTIONS.md](docs/BUILD_INSTRUCTIONS.md).

## 📁 Project Structure

```
VirusTotal-IP-Analyzer/
├── main.py                          # Application entry point
├── requirements.txt                 # Python dependencies
├── VirusTotal-IP-Analyzer.spec     # PyInstaller build configuration
├── README.md                       # This file
├── TROUBLESHOOTING.md             # Common issues and solutions
├── assets/                        # Application assets
│   ├── icon.ico                   # Windows icon
│   └── icon.png                   # Linux icon
├── docs/                          # Documentation
│   ├── BUILD_INSTRUCTIONS.md      # Detailed build guide
│   ├── PROJECT_STRUCTURE.md       # Architecture documentation
│   └── README.md                  # Original documentation
├── scripts/                       # Build and run scripts
│   ├── build_windows.bat          # Windows build script
│   ├── build_linux.sh             # Linux build script
│   ├── run_windows.bat             # Windows run script
│   ├── run_linux.sh               # Linux run script (enhanced)
│   └── run.sh                     # Linux run script (simple)
├── src/                           # Source code
│   ├── core/                      # Core functionality
│   │   ├── api_client.py          # VirusTotal API integration
│   │   ├── cache_manager.py       # Data persistence and caching
│   │   ├── config.py              # Application configuration
│   │   ├── encryption.py          # API key encryption/decryption
│   │   ├── ip_blocker.py          # Cross-platform IP blocking
│   │   ├── network_scanner.py     # Network connection detection
│   │   └── scanner.py             # Scan coordination and management
│   └── gui/                       # User interface components
│       ├── api_key_dialog.py      # API key management dialog
│       ├── custom_dialogs.py      # Custom themed dialogs
│       ├── main_window.py         # Main application window
│       ├── results_window.py      # Scan results display
│       └── utils.py               # GUI utility functions
├── tests/                         # Test files
│   └── test_network_scan.py       # Network scanning tests
└── dist/                          # Built executables (after building)
    ├── VirusTotal-IP-Analyzer-Windows.exe  # Windows executable
    └── linux/
        └── virustotal-ip-analyzer-linux    # Linux executable
```

## 📋 Requirements

### System Requirements
- **Python 3.8+** (for source installation)
- **Internet connection** (for VirusTotal API)
- **Administrator/sudo privileges** (for IP blocking features)

### Dependencies
- `customtkinter>=5.2.0` - Modern GUI framework
- `requests>=2.31.0` - HTTP client for API calls
- `cryptography>=41.0.0` - API key encryption

## 🔑 VirusTotal API Key

1. **Get API Key**: Register at [VirusTotal](https://www.virustotal.com/) and get your free API key
2. **Set in Application**: Use the "🔑 Set/Update API Key" button in the GUI
3. **Secure Storage**: API keys are encrypted and stored securely

## 🛠️ Configuration

### Application Settings
- **Windows**: `%APPDATA%\VT_IP_Analyzer\`
- **Linux**: `~/.config/vt-ip-analyzer/`

### Configuration Files
- `encrypted_api_key.key` - Encrypted VirusTotal API key
- `cache.json` - Cached scan results
- `blocked_ips.json` - List of blocked IP addresses

## 🔒 Security Features

### API Key Protection
- **Fernet Encryption**: API keys encrypted using cryptography library
- **Secure Storage**: Keys stored in user-specific directories
- **No Plain Text**: API keys never stored in plain text

### IP Blocking Security
- **System-level Blocking**: Uses OS firewall systems
- **Persistent Rules**: Survives system reboots
- **Audit Trail**: Maintains list of blocked IPs with metadata

## 📊 Usage Examples

### Basic Scan
1. Launch the application
2. Set your VirusTotal API key
3. Click "🚀 Start Scan"
4. Review results in the log and results window

### Advanced Configuration
- **Max IPs**: Limit number of IPs to scan (0 = unlimited)
- **Batch Size**: Number of concurrent API requests
- **Batch Delay**: Delay between batches (respects rate limits)
- **Field Selection**: Choose which data fields to export

### IP Blocking Workflow
1. Run a scan to identify suspicious IPs
2. In the results window, select an IP
3. Click "⛔ Block IP" to add firewall rules
4. Use "🔓 Unblock IP" to remove rules later

## 🐛 Troubleshooting

### Common Issues

**"No external IPs found"**
- Ensure you have active internet connections
- Try running as administrator/sudo
- Check if firewall is blocking network scanning

**"API Key Missing"**
- Get a free API key from VirusTotal.com
- Use the "🔑 Set/Update API Key" button
- Verify the key is valid

**"Permission denied" (Linux)**
- IP blocking requires sudo privileges
- Run: `sudo ./dist/linux/virustotal-ip-analyzer-linux`
- Or use: `sudo python main.py`

**Build Issues**
- Ensure Python 3.8+ is installed
- Update pip: `pip install --upgrade pip`
- See [docs/BUILD_INSTRUCTIONS.md](docs/BUILD_INSTRUCTIONS.md) for details

**Character Encoding Issues (Windows)**
- The build and run scripts use ASCII-compatible characters
- If you see strange characters, ensure you're using Command Prompt or PowerShell

For more detailed troubleshooting, see [TROUBLESHOOTING.md](TROUBLESHOOTING.md).

## 🏗️ Architecture

### Core Components
- **`main.py`** - Application entry point
- **`src/gui/`** - User interface components
- **`src/core/scanner.py`** - Scan coordination and management
- **`src/core/api_client.py`** - VirusTotal API integration
- **`src/core/network_scanner.py`** - Network connection detection
- **`src/core/ip_blocker.py`** - Cross-platform IP blocking
- **`src/core/cache_manager.py`** - Data persistence and caching
- **`src/core/encryption.py`** - API key encryption/decryption
- **`src/core/config.py`** - Application configuration

### Design Principles
- **Modular Architecture**: Clear separation of concerns
- **Cross-platform Compatibility**: Works on Windows and Linux
- **Security First**: Encrypted storage, secure API handling
- **User Experience**: Intuitive GUI with real-time feedback
- **Performance**: Efficient caching and threading

## 📈 Performance

### Optimization Features
- **Smart Caching**: Avoids redundant API calls
- **Threaded Scanning**: Parallel processing for faster scans
- **Rate Limit Handling**: Respects VirusTotal API limits
- **Efficient Storage**: Compressed data storage

### Typical Performance
- **Network Scan**: 1-5 seconds
- **API Queries**: 1-2 seconds per IP (with caching)
- **IP Blocking**: Instant (system firewall rules)
- **Memory Usage**: ~50-100MB

## 🔧 Development

### Available Scripts

| Script | Platform | Purpose |
|--------|----------|---------|
| `scripts/build_windows.bat` | Windows | Build Windows executable |
| `scripts/build_linux.sh` | Linux | Build Linux executable |
| `scripts/run_windows.bat` | Windows | Run from source (enhanced) |
| `scripts/run_linux.sh` | Linux | Run from source (enhanced) |
| `scripts/run.sh` | Linux | Run from source (simple) |

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

## 🤝 Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues for bugs and feature requests.

### Contribution Guidelines
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test on both Windows and Linux if possible
5. Submit a pull request

## 📄 License

This project is licensed under the GNU General Public License v3.0 - see the LICENSE file for details.

## 🙏 Acknowledgments

- **VirusTotal** - For providing the comprehensive threat intelligence API
- **CustomTkinter** - For the modern GUI framework
- **Python Community** - For the excellent libraries and tools

## 📞 Support

For support, please:
1. Check the [TROUBLESHOOTING.md](TROUBLESHOOTING.md) for common issues
2. Review the [docs/BUILD_INSTRUCTIONS.md](docs/BUILD_INSTRUCTIONS.md) for build issues
3. Open an issue on the [project repository](https://github.com/mat-heidemann/VirusTotal-IP-Analyzer)

---

**⚠️ Disclaimer**: This tool is for legitimate security analysis only. Users are responsible for complying with applicable laws and regulations when using IP blocking features.

**🔗 Repository**: https://github.com/mat-heidemann/VirusTotal-IP-Analyzer
