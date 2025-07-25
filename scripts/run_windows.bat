@echo off
setlocal enabledelayedexpansion

echo ========================================
echo  VirusTotal IP Analyzer - Windows Runner
echo ========================================

REM Move to the project root directory
cd /d "%~dp0\.."
echo → Switched to project root: %CD%

REM === Check if Python is available ===
echo.
echo [*] Checking for Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo [X] Python is not installed or not in PATH.
    echo Please install Python and ensure it's in your PATH.
    pause
    exit /b 1
)

REM Get Python version
for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
echo [+] Python !PYTHON_VERSION! detected

REM === Check if venv module is available ===
echo.
echo [*] Checking if 'venv' module is available...
python -m venv --help >nul 2>&1
if errorlevel 1 (
    echo [X] Python venv module is not available.
    echo Please ensure you have a complete Python installation.
    pause
    exit /b 1
)

REM === Check if virtual environment exists ===
if not exist "venv\" (
    echo.
    echo [*] Virtual environment not found. Creating...
    python -m venv venv
    if errorlevel 1 (
        echo [X] Failed to create virtual environment.
        echo Please check your Python installation.
        pause
        exit /b 1
    )
    
    echo.
    echo [*] Activating virtual environment...
    call venv\Scripts\activate.bat
    if errorlevel 1 (
        echo [X] Failed to activate virtual environment.
        pause
        exit /b 1
    )
    
    echo.
    echo [*] Installing dependencies...
    echo Upgrading pip...
    pip install --upgrade pip
    if errorlevel 1 (
        echo [X] Failed to upgrade pip.
        pause
        exit /b 1
    )
    
    echo Installing project dependencies...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo [X] Failed to install dependencies.
        echo Please check requirements.txt and your internet connection.
        pause
        exit /b 1
    )
    echo [+] Dependencies installed successfully
) else (
    echo.
    echo [*] Activating existing virtual environment...
    call venv\Scripts\activate.bat
    if errorlevel 1 (
        echo [X] Failed to activate virtual environment.
        pause
        exit /b 1
    )
    echo [+] Virtual environment activated
)

REM === Run the application ===
echo.
echo [+] Starting VirusTotal IP Analyzer...
echo ========================================
python main.py

echo.
pause
