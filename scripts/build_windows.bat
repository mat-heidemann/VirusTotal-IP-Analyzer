@echo off
echo ========================================
echo  VirusTotal IP Analyzer - Windows Build
echo ========================================

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    pause
    exit /b 1
)

REM Check if virtual environment exists
if not exist "venv\" (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Install dependencies
echo Installing dependencies...
pip install -r requirements.txt

REM Install PyInstaller
echo Installing PyInstaller...
pip install pyinstaller

REM Clean previous builds
echo Cleaning previous builds...
if exist "dist\" rmdir /s /q dist
if exist "build\" rmdir /s /q build
if exist "*.spec" del *.spec

REM Build executable
echo Building Windows executable...
pyinstaller ^
    --onefile ^
    --windowed ^
    --icon=icon.ico ^
    --hidden-import=customtkinter ^
    --hidden-import=requests ^
    --hidden-import=cryptography ^
    --hidden-import=tkinter ^
    --add-data "src;src" ^
    --add-data "assets\icon.ico;assets" ^
    --name "VirusTotal-IP-Analyzer-Windows" ^
    --distpath "dist/windows" ^
    main.py

REM Check if build was successful
if exist "dist\windows\VirusTotal-IP-Analyzer-Windows.exe" (
    echo.
    echo ========================================
    echo  BUILD SUCCESSFUL!
    echo ========================================
    echo Executable created: dist\windows\VirusTotal-IP-Analyzer-Windows.exe
    echo Size: 
    for %%A in ("dist\windows\VirusTotal-IP-Analyzer-Windows.exe") do echo %%~zA bytes
    echo.
    echo You can now distribute this single .exe file!
    echo.
) else (
    echo.
    echo ========================================
    echo  BUILD FAILED!
    echo ========================================
    echo Check the output above for errors.
)

REM Clean up build artifacts
echo Cleaning up build artifacts...
if exist "build\" rmdir /s /q build
if exist "*.spec" del *.spec

echo.
pause
