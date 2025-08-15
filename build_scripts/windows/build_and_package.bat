@echo off
REM ========================================================
REM TuxTray Complete Windows Build and Package Pipeline
REM ========================================================
REM This script builds both the executable and installer

echo ========================================================
echo TuxTray v2.0.0 - Windows Build Pipeline
echo ========================================================
echo.

REM Get script directory
set BUILD_DIR=%~dp0
set PROJECT_ROOT=%BUILD_DIR%\..\..\

REM Step 1: Build the executable
echo [STEP 1] Building Windows executable...
call "%BUILD_DIR%build_windows.bat"

REM Check if executable build was successful
if not exist "%PROJECT_ROOT%dist\TuxTray\TuxTray.exe" (
    echo [ERROR] Executable build failed! Cannot proceed with installer.
    pause
    exit /b 1
)

echo.
echo [STEP 1] ✅ Executable build completed successfully!
echo.

REM Step 2: Create installer (if Inno Setup is available)
echo [STEP 2] Creating Windows installer...

REM Check if Inno Setup is installed
where iscc >nul 2>nul
if errorlevel 1 (
    echo [WARNING] Inno Setup compiler 'iscc' not found in PATH.
    echo [INFO] Please install Inno Setup from: https://jrsoftware.org/isinfo.php
    echo [INFO] Or manually compile TuxTray_Installer.iss
    echo.
    echo [STEP 2] ⚠️  Installer creation skipped
    goto :finish
)

REM Create installer output directory
if not exist "%PROJECT_ROOT%dist\installer" mkdir "%PROJECT_ROOT%dist\installer"

REM Compile installer
iscc "%BUILD_DIR%TuxTray_Installer.iss"

REM Check if installer was created
if exist "%PROJECT_ROOT%dist\installer\TuxTray-2.0.0-Windows-Setup.exe" (
    echo.
    echo [STEP 2] ✅ Windows installer created successfully!
    echo [INSTALLER] %PROJECT_ROOT%dist\installer\TuxTray-2.0.0-Windows-Setup.exe
    
    REM Get file size
    for %%I in ("%PROJECT_ROOT%dist\installer\TuxTray-2.0.0-Windows-Setup.exe") do set INSTALLER_SIZE=%%~zI
    set /a INSTALLER_SIZE_MB=%INSTALLER_SIZE% / 1048576
    echo [SIZE] Installer size: %INSTALLER_SIZE_MB% MB
    
) else (
    echo.
    echo [STEP 2] ❌ Installer creation failed!
    echo [INFO] Check TuxTray_Installer.iss for errors
)

:finish
echo.
echo ========================================================
echo TuxTray Build Pipeline Complete
echo ========================================================

REM Summary
echo [SUMMARY]
if exist "%PROJECT_ROOT%dist\TuxTray\TuxTray.exe" (
    echo ✅ Standalone executable: dist\TuxTray\TuxTray.exe
)
if exist "%PROJECT_ROOT%dist\installer\TuxTray-2.0.0-Windows-Setup.exe" (
    echo ✅ Windows installer: dist\installer\TuxTray-2.0.0-Windows-Setup.exe
)

echo.
echo [NEXT STEPS]
echo 1. Test the executable: dist\TuxTray\TuxTray.exe
echo 2. Test the installer (if created)
echo 3. Upload to GitHub releases
echo 4. Update documentation with Windows installation instructions
echo.

pause
