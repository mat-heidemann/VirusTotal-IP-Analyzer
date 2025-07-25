# 📁 Project Structure - VirusTotal IP Analyzer

This document describes the organized folder structure of the VirusTotal IP Analyzer project.

## 🏗️ Directory Overview

```
VirusTotal IP Analyzer/
├── 📁 assets/                 # Static assets and resources
│   └── icon.ico              # Application icon
├── 📁 docs/                  # Documentation files
│   ├── BUILD_INSTRUCTIONS.md # Detailed build instructions
│   ├── PROJECT_STRUCTURE.md  # This file
│   └── README.md             # Main project documentation
├── 📁 scripts/               # Build and utility scripts
│   ├── build_linux.sh       # Linux build script
│   ├── build_windows.bat    # Windows build script
│   └── run.sh               # Quick run script
├── 📁 src/                   # Source code directory
│   ├── 📁 core/             # Core application logic
│   │   ├── __init__.py
│   │   ├── api_client.py    # VirusTotal API integration
│   │   ├── cache_manager.py # Data caching and persistence
│   │   ├── config.py        # Application configuration
│   │   ├── encryption.py    # API key encryption
│   │   ├── ip_blocker.py    # Cross-platform IP blocking
│   │   ├── network_scanner.py # Network connection detection
│   │   └── scanner.py       # Main scanning coordinator
│   ├── 📁 gui/              # User interface components
│   │   ├── __init__.py
│   │   ├── api_key_dialog.py # API key input dialog
│   │   ├── custom_dialogs.py # Custom themed dialogs
│   │   ├── main_window.py   # Main application window
│   │   ├── results_window.py # Results display window
│   │   └── utils.py         # GUI utility functions
│   ├── 📁 utils/            # General utility functions
│   │   └── __init__.py
│   └── __init__.py
├── 📁 tests/                 # Test files
│   └── test_network_scan.py # Network scanning tests
├── 📁 venv/                  # Python virtual environment
├── main.py                   # Application entry point
└── requirements.txt          # Python dependencies
```

## 📋 Directory Descriptions

### 🎨 **assets/**
Contains static resources used by the application:
- **`icon.ico`**: Application icon used in executables and GUI

### 📚 **docs/**
Documentation and guides:
- **`README.md`**: Main project documentation with features and usage
- **`BUILD_INSTRUCTIONS.md`**: Comprehensive build instructions
- **`PROJECT_STRUCTURE.md`**: This file describing the project organization

### 🔧 **scripts/**
Build and utility scripts:
- **`build_linux.sh`**: Automated Linux build script with PyInstaller
- **`build_windows.bat`**: Automated Windows build script with PyInstaller
- **`run.sh`**: Quick script to run the application from source

### 💻 **src/**
Main source code directory organized by functionality:

#### **src/core/**
Core application logic and business functionality:
- **`api_client.py`**: VirusTotal API integration and HTTP client
- **`cache_manager.py`**: Data persistence, caching, and storage management
- **`config.py`**: Application configuration, paths, and constants
- **`encryption.py`**: API key encryption and secure storage
- **`ip_blocker.py`**: Cross-platform IP blocking (Windows/Linux/macOS)
- **`network_scanner.py`**: Network connection detection and IP discovery
- **`scanner.py`**: Main scanning coordinator and workflow management

#### **src/gui/**
User interface components and dialogs:
- **`main_window.py`**: Main application window and primary GUI
- **`results_window.py`**: Results display window with IP blocking controls
- **`api_key_dialog.py`**: API key input and management dialog
- **`custom_dialogs.py`**: Custom themed message boxes and dialogs
- **`utils.py`**: GUI utility functions and helpers

#### **src/utils/**
General utility functions (reserved for future expansion)

### 🧪 **tests/**
Test files and testing utilities:
- **`test_network_scan.py`**: Network scanning functionality tests

## 🚀 **Entry Points**

### Primary Entry Point
- **`main.py`**: Main application entry point that imports and runs the GUI

### Build Scripts
- **`scripts/build_linux.sh`**: Creates Linux executable
- **`scripts/build_windows.bat`**: Creates Windows executable

### Quick Run
- **`scripts/run.sh`**: Activates venv and runs the application

## 🔄 **Import Structure**

The new modular structure uses proper Python package imports:

```python
# Core modules
from src.core.config import DEFAULT_OUTPUT_PATH
from src.core.encryption import EncryptionManager
from src.core.scanner import IPScanner

# GUI modules
from src.gui.main_window import VirusTotalIPAnalyzer
from src.gui.custom_dialogs import show_error, show_info
```

## 📦 **Package Organization**

### **Core Package** (`src.core`)
Contains all business logic and core functionality:
- **API Integration**: VirusTotal API client and communication
- **Data Management**: Caching, persistence, and configuration
- **Security**: Encryption and secure storage
- **Network Operations**: IP scanning and blocking
- **Workflow**: Scan coordination and management

### **GUI Package** (`src.gui`)
Contains all user interface components:
- **Main Interface**: Primary application window
- **Dialogs**: Input dialogs and message boxes
- **Results Display**: Scan results and IP management
- **Utilities**: GUI helpers and theming

## 🛠️ **Development Benefits**

### **Improved Organization**
- **Clear Separation**: Business logic separated from UI code
- **Modular Design**: Each module has a single responsibility
- **Easy Navigation**: Logical folder structure for quick file location

### **Better Maintainability**
- **Isolated Changes**: Modifications to one area don't affect others
- **Clear Dependencies**: Import structure shows component relationships
- **Easier Testing**: Modular structure enables better unit testing

### **Professional Structure**
- **Industry Standard**: Follows Python packaging best practices
- **Scalable**: Easy to add new features and modules
- **Documentation**: Clear structure with comprehensive documentation

## 🔧 **Build System Integration**

The build scripts automatically handle the new structure:
- **Automatic Discovery**: PyInstaller finds all modules in `src/`
- **Proper Packaging**: GUI package included with `--add-data`
- **Icon Integration**: Assets folder properly referenced
- **Clean Builds**: Scripts handle cleanup and organization

## 📈 **Future Expansion**

The organized structure supports easy expansion:
- **New Core Modules**: Add to `src/core/` for business logic
- **New GUI Components**: Add to `src/gui/` for interface elements
- **Utility Functions**: Add to `src/utils/` for shared utilities
- **Additional Tests**: Add to `tests/` for comprehensive testing
- **Documentation**: Add to `docs/` for project documentation

This structure provides a solid foundation for continued development and maintenance of the VirusTotal IP Analyzer.
