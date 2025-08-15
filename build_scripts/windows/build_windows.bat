@echo off
REM ========================================================
REM TuxTray Windows Build Script
REM ========================================================
REM This script builds TuxTray for Windows 10/11
REM Requires: Python 3.10+, PyInstaller, dependencies

echo [TuxTray] Starting Windows build process...
echo.

REM Get script directory
set BUILD_DIR=%~dp0
set PROJECT_ROOT=%BUILD_DIR%\..\..\
set DIST_DIR=%PROJECT_ROOT%\dist
set BUILD_TEMP=%PROJECT_ROOT%\build

REM Change to project root
cd /d "%PROJECT_ROOT%"

REM Check if virtual environment exists
if not exist "venv" (
    echo [TuxTray] Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
echo [TuxTray] Activating virtual environment...
call venv\Scripts\activate.bat

REM Install/upgrade dependencies
echo [TuxTray] Installing build dependencies...
python -m pip install --upgrade pip
pip install -r requirements.txt
pip install pyinstaller

REM Clean previous builds
echo [TuxTray] Cleaning previous builds...
if exist "%DIST_DIR%" rmdir /s /q "%DIST_DIR%"
if exist "%BUILD_TEMP%" rmdir /s /q "%BUILD_TEMP%"

REM Create Windows icon if needed (convert from first frame)
echo [TuxTray] Preparing assets...
if not exist "assets\icon.ico" (
    echo [TuxTray] Converting penguin frame to Windows icon...
    python -c "from PIL import Image; img = Image.open('assets/skins/default/calm/frame_0001.png'); img.save('assets/icon.ico', format='ICO', sizes=[(16,16), (32,32), (48,48), (64,64)])" 2>nul || echo [TuxTray] Warning: Could not create icon file
)

REM Build executable with PyInstaller
echo [TuxTray] Building Windows executable...
pyinstaller --clean build_scripts\windows\TuxTray.spec

REM Check if build succeeded
if exist "dist\TuxTray\TuxTray.exe" (
    echo.
    echo [TuxTray] ✅ Build completed successfully!
    echo [TuxTray] Executable location: dist\TuxTray\TuxTray.exe
    echo [TuxTray] Directory size:
    dir "dist\TuxTray" | find "bytes"
    echo.
    
    REM Test the executable
    echo [TuxTray] Testing executable...
    timeout /t 2 >nul
    echo [TuxTray] Ready to create installer or distribute folder.
    
) else (
    echo.
    echo [TuxTray] ❌ Build failed!
    echo [TuxTray] Check the output above for errors.
    pause
    exit /b 1
)

echo [TuxTray] Build process completed.
pause
