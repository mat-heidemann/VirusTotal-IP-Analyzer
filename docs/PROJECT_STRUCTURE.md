# 📁 Project Structure - VirusTotal IP Analyzer

This document describes the organized folder structure of the VirusTotal IP Analyzer project, including all build scripts, run scripts, and documentation.

## 🏗️ Directory Overview

```
VirusTotal-IP-Analyzer/
├── 📄 main.py                          # Application entry point
├── 📄 requirements.txt                 # Python dependencies
├── 📄 VirusTotal-IP-Analyzer.spec     # PyInstaller build configuration
├── 📄 README.md                       # Main project documentation
├── 📄 TROUBLESHOOTING.md             # Common issues and solutions
├── 📄 .gitignore                      # Git ignore rules
├── 📁 assets/                         # Application assets
│   ├── icon.ico                       # Windows application icon
│   └── icon.png                       # Linux application icon
├── 📁 docs/                          # Documentation files
│   ├── BUILD_INSTRUCTIONS.md          # Detailed build guide
│   ├── PROJECT_STRUCTURE.md           # This file
│   └── README.md                      # Original documentation
├── 📁 scripts/                       # Build and run scripts
│   ├── build_windows.bat              # Windows build script (enhanced)
│   ├── build_linux.sh                 # Linux build script (enhanced)
│   ├── run_windows.bat                # Windows run script (enhanced)
│   ├── run_linux.sh                   # Linux run script (enhanced)
│   └── run.sh                         # Linux run script (simple)
├── 📁 src/                           # Source code directory
│   ├── 📁 core/                      # Core application logic
│   │   ├── api_client.py              # VirusTotal API integration
│   │   ├── cache_manager.py           # Data caching and persistence
│   │   ├── config.py                  # Application configuration
│   │   ├── encryption.py              # API key encryption/decryption
│   │   ├── ip_blocker.py              # Cross-platform IP blocking
│   │   ├── network_scanner.py         # Network connection detection
│   │   └── scanner.py                 # Main scanning coordinator
│   └── 📁 gui/                       # User interface components
│       ├── api_key_dialog.py          # API key management dialog
│       ├── custom_dialogs.py          # Custom themed dialogs
│       ├── main_window.py             # Main application window
│       ├── results_window.py          # Scan results display
│       └── utils.py                   # GUI utility functions
├── 📁 tests/                         # Test files
│   └── test_network_scan.py           # Network scanning tests
├── 📁 dist/                          # Built executables (after building)
│   ├── VirusTotal-IP-Analyzer-Windows.exe  # Windows executable
│   └── linux/
│       └── virustotal-ip-analyzer-linux    # Linux executable
├── 📁 build/                         # PyInstaller build cache (temporary)
└── 📁 venv/                          # Python virtual environment (temporary)
```

## 📋 Directory Descriptions

### 🎨 **assets/**

Contains static resources used by the application:

-   **`icon.ico`**: Windows application icon (embedded in .exe files)
-   **`icon.png`**: Linux application icon (for desktop integration)

### 📚 **docs/**

Comprehensive documentation and guides:

-   **`README.md`**: Original detailed project documentation
-   **`BUILD_INSTRUCTIONS.md`**: Comprehensive build instructions with troubleshooting
-   **`PROJECT_STRUCTURE.md`**: This file describing the project organization

### 🔧 **scripts/**

Enhanced build and run scripts for both platforms:

#### Build Scripts

-   **`build_windows.bat`**: Enhanced Windows build script with:
    -   ASCII-compatible progress indicators
    -   Comprehensive error handling
    -   Automatic environment management
    -   Build verification and cleanup
-   **`build_linux.sh`**: Enhanced Linux build script with:
    -   Colored terminal output with emojis
    -   WSL compatibility and permission handling
    -   Smart virtual environment setup
    -   Comprehensive error handling

#### Run Scripts

-   **`run_windows.bat`**: Enhanced Windows run script with:
    -   Automatic virtual environment creation/activation
    -   Dependency installation and management
    -   ASCII-compatible status indicators
    -   Comprehensive error handling
-   **`run_linux.sh`**: Enhanced Linux run script with:
    -   Colored output and professional interface
    -   Automatic dependency management
    -   Error handling and recovery
    -   WSL compatibility
-   **`run.sh`**: Simple Linux run script (original version)

### 💻 **src/**

Main source code directory organized by functionality:

#### **src/core/**

Core application logic and business functionality:

-   **`api_client.py`**: VirusTotal API integration and HTTP client
    -   API key management and validation
    -   Rate limiting and error handling
    -   IP reputation queries and data parsing
-   **`cache_manager.py`**: Data persistence, caching, and storage management
    -   JSON-based caching system
    -   Scan result persistence
    -   Configuration data storage
-   **`config.py`**: Application configuration, paths, and constants
    -   Cross-platform path management
    -   Default settings and constants
    -   Configuration file locations
-   **`encryption.py`**: API key encryption and secure storage
    -   Fernet-based encryption for API keys
    -   Secure key generation and storage
    -   Cross-platform security implementation
-   **`ip_blocker.py`**: Cross-platform IP blocking functionality
    -   Windows Firewall integration (netsh)
    -   Linux iptables integration
    -   Persistent rule management
-   **`network_scanner.py`**: Network connection detection and IP discovery
    -   Active connection scanning
    -   Process identification
    -   External IP filtering
-   **`scanner.py`**: Main scanning coordinator and workflow management
    -   Scan orchestration and threading
    -   Progress reporting and callbacks
    -   Error handling and recovery

#### **src/gui/**

User interface components and dialogs:

-   **`main_window.py`**: Main application window and primary GUI
    -   Dark theme interface with CustomTkinter
    -   Real-time logging and progress display
    -   Configuration management interface
-   **`results_window.py`**: Results display window with IP blocking controls
    -   Tabular results display
    -   IP blocking/unblocking functionality
    -   CSV export capabilities
-   **`api_key_dialog.py`**: API key input and management dialog
    -   Secure API key input
    -   Key validation and testing
    -   Encrypted storage integration
-   **`custom_dialogs.py`**: Custom themed message boxes and dialogs
    -   Consistent dark theme dialogs
    -   Error and information messages
    -   User confirmation dialogs
-   **`utils.py`**: GUI utility functions and helpers
    -   Theme management utilities
    -   Common GUI operations
    -   Helper functions for interface elements

### 🧪 **tests/**

Test files and testing utilities:

-   **`test_network_scan.py`**: Network scanning functionality tests
    -   Unit tests for network scanning
    -   Mock testing for API integration
    -   Cross-platform compatibility tests

### 📦 **dist/**

Built executables (created after building):

-   **`VirusTotal-IP-Analyzer-Windows.exe`**: Windows standalone executable
-   **`linux/virustotal-ip-analyzer-linux`**: Linux standalone executable

### 🔧 **build/** (Temporary)

PyInstaller build cache and temporary files:

-   Created during build process
-   Automatically cleaned up by build scripts
-   Contains intermediate build artifacts

### 🐍 **venv/** (Temporary)

Python virtual environment:

-   Created by run scripts if needed
-   Contains isolated Python dependencies
-   Automatically managed by scripts

## 🚀 **Entry Points**

### Primary Entry Point

-   **`main.py`**: Main application entry point that initializes and runs the GUI

### Build Scripts

-   **`scripts/build_windows.bat`**: Creates Windows executable with comprehensive error handling
-   **`scripts/build_linux.sh`**: Creates Linux executable with WSL compatibility

### Run Scripts

-   **`scripts/run_windows.bat`**: Runs from source on Windows with environment management
-   **`scripts/run_linux.sh`**: Runs from source on Linux with colored output
-   **`scripts/run.sh`**: Simple Linux run script for basic usage

## 🔄 **Import Structure**

The modular structure uses proper Python package imports:

```python
# Core modules
from src.core.config import get_config_dir, DEFAULT_SETTINGS
from src.core.encryption import EncryptionManager
from src.core.scanner import IPScanner
from src.core.api_client import VirusTotalClient

# GUI modules
from src.gui.main_window import VirusTotalIPAnalyzer
from src.gui.custom_dialogs import show_error, show_info
from src.gui.results_window import ResultsWindow
```

## 📦 **Package Organization**

### **Core Package** (`src.core`)

Contains all business logic and core functionality:

-   **API Integration**: VirusTotal API client and communication
-   **Data Management**: Caching, persistence, and configuration
-   **Security**: Encryption and secure storage
-   **Network Operations**: IP scanning and blocking
-   **Workflow**: Scan coordination and management

### **GUI Package** (`src.gui`)

Contains all user interface components:

-   **Main Interface**: Primary application window with dark theme
-   **Dialogs**: Input dialogs and custom message boxes
-   **Results Display**: Scan results with IP management controls
-   **Utilities**: GUI helpers and theming functions

## 🛠️ **Build System Integration**

### **Unified Spec File**

-   **`VirusTotal-IP-Analyzer.spec`**: Single configuration file for both platforms
-   **Platform Detection**: Automatically configures for Windows or Linux
-   **Asset Inclusion**: Properly bundles icons and GUI components
-   **Optimization**: Platform-specific build optimizations

### **Enhanced Build Scripts**

Both build scripts provide:

-   **Environment Management**: Automatic virtual environment creation
-   **Dependency Installation**: Automated pip and PyInstaller setup
-   **Error Handling**: Comprehensive error detection and recovery
-   **Build Verification**: Confirms successful executable creation
-   **Cleanup**: Automatic removal of temporary files

## 🔧 **Development Benefits**

### **Improved Organization**

-   **Clear Separation**: Business logic separated from UI code
-   **Modular Design**: Each module has a single responsibility
-   **Easy Navigation**: Logical folder structure for quick file location
-   **Professional Structure**: Follows Python packaging best practices

### **Better Maintainability**

-   **Isolated Changes**: Modifications to one area don't affect others
-   **Clear Dependencies**: Import structure shows component relationships
-   **Easier Testing**: Modular structure enables better unit testing
-   **Documentation**: Comprehensive documentation for all components

### **Enhanced Build Process**

-   **Cross-Platform**: Single codebase builds on both Windows and Linux
-   **Automated**: Scripts handle all aspects of building and running
-   **Error Recovery**: Robust error handling and troubleshooting
-   **User-Friendly**: Clear progress indicators and status messages

## 📈 **Script Features Comparison**

| Feature                | Windows Scripts             | Linux Scripts        |
| ---------------------- | --------------------------- | -------------------- |
| Progress Indicators    | ASCII (`[*]`, `[+]`, `[X]`) | Colored Emojis       |
| Error Handling         | Comprehensive               | Comprehensive        |
| Environment Management | Automatic                   | Automatic            |
| WSL Support            | N/A                         | Full Support         |
| Virtual Environment    | Local `venv/`               | Temp `/tmp/` (build) |
| Cleanup                | Automatic                   | Automatic            |
| User Feedback          | Detailed                    | Detailed + Colored   |
| Permission Handling    | Standard                    | WSL-aware            |

## 🔄 **Workflow Integration**

### **Development Workflow**

1. **Setup**: Use run scripts to set up development environment
2. **Development**: Modify source code in `src/` directory
3. **Testing**: Run tests from `tests/` directory
4. **Building**: Use build scripts to create executables
5. **Distribution**: Share executables from `dist/` directory

### **User Workflow**

1. **Download**: Get pre-built executables from `dist/`
2. **Run**: Execute directly or use run scripts for source
3. **Configure**: Set VirusTotal API key through GUI
4. **Scan**: Perform IP analysis and blocking
