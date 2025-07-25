@echo off
setlocal enabledelayedexpansion

echo ========================================
echo  VirusTotal IP Analyzer - Windows Build
echo ========================================

REM === Color definitions (Windows doesn't support colors in basic cmd, but we'll use clear messaging) ===

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

REM === Remove any previous broken venv ===
echo.
echo [*] Recreating virtual environment...
if exist "venv\" (
    echo Removing existing virtual environment...
    rmdir /s /q venv
)

echo Creating new virtual environment...
python -m venv venv
if errorlevel 1 (
    echo [X] Failed to create virtual environment.
    echo Please check your Python installation.
    pause
    exit /b 1
)

REM === Activate virtual environment ===
echo.
echo [*] Activating virtual environment...
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo [X] Failed to activate virtual environment.
    pause
    exit /b 1
)

REM === Ensure pip is available ===
echo.
echo [*] Ensuring pip is available...
pip --version >nul 2>&1
if errorlevel 1 (
    echo [X] pip is not available in the virtual environment.
    pause
    exit /b 1
)

for /f "tokens=2" %%i in ('pip --version 2^>^&1') do set PIP_VERSION=%%i
echo [+] pip !PIP_VERSION! available

REM === Install dependencies ===
echo.
echo [*] Installing requirements...
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
    echo [X] Failed to install requirements.
    echo Please check requirements.txt and your internet connection.
    pause
    exit /b 1
)

REM === Install PyInstaller ===
echo.
echo [*] Installing PyInstaller...
pip install pyinstaller
if errorlevel 1 (
    echo [X] Failed to install PyInstaller.
    pause
    exit /b 1
)

REM === Clean previous build artifacts ===
echo.
echo [*] Cleaning old build files...
if exist "dist\" (
    echo Removing dist directory...
    rmdir /s /q dist
)
if exist "build\" (
    echo Removing build directory...
    rmdir /s /q build
)
if exist "main.spec" (
    echo Removing old spec file...
    del main.spec
)

REM === Build executable ===
echo.
echo [*] Building Windows executable...
pyinstaller --distpath "dist" --workpath "build" --noconfirm --clean VirusTotal-IP-Analyzer.spec
set BUILD_EXIT_CODE=!errorlevel!

REM Check if build succeeded despite any warnings
if !BUILD_EXIT_CODE! neq 0 (
    echo [!] PyInstaller reported errors, but checking if executable was created...
)

REM === Check result ===
echo.
echo [*] Verifying build...
if exist "dist\VirusTotal-IP-Analyzer-Windows.exe" (
    echo [+] BUILD SUCCESSFUL!
    echo Executable: dist\VirusTotal-IP-Analyzer-Windows.exe
    
    REM Get file size
    for %%A in ("dist\VirusTotal-IP-Analyzer-Windows.exe") do (
        set FILE_SIZE=%%~zA
        echo Size: !FILE_SIZE! bytes
    )
    
    echo [+] Windows executable created successfully
    echo.
    echo This is the final production version. No console window will appear.
    echo You can now distribute the generated .exe file.
) else (
    echo [X] BUILD FAILED!
    echo The executable was not created. Please check the output above for error details.
    pause
    exit /b 1
)

REM === Cleanup ===
echo.
echo [*] Cleaning temporary files...
if exist "build\" (
    echo Removing build directory...
    rmdir /s /q build
)

REM === Optional: remove venv ===
echo [*] Removing virtual environment...
if exist "venv\" (
    rmdir /s /q venv
)

echo.
echo [+] Build process completed successfully!
echo.
pause
