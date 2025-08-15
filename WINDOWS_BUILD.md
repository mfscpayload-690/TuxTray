# 🐧 TuxTray Windows Build Guide

## Overview

This guide explains how to build TuxTray for Windows 10/11 and create a professional installer. TuxTray's 5-state emotion system works seamlessly on Windows with native system tray integration.

---

## 🛠️ Prerequisites

### Required Software

1. **Python 3.10 or later** (from [python.org](https://python.org))
   - ✅ Add Python to PATH during installation
   - ✅ Install pip package manager

2. **Git** (from [git-scm.com](https://git-scm.com))
   - For cloning the repository

3. **Inno Setup** (optional, for installer)
   - Download from [jrsoftware.org](https://jrsoftware.org/isinfo.php)
   - Required for creating `.exe` installer

### System Requirements

- **OS**: Windows 10 (version 2004/19041) or Windows 11
- **Architecture**: x64 (64-bit)
- **RAM**: 4GB minimum (8GB recommended)
- **Disk Space**: 500MB for build environment

---

## 🚀 Quick Build Process

### Option 1: Automated Build (Recommended)

```batch
# Clone the repository
git clone https://github.com/mfscpayload-690/TuxTray.git
cd TuxTray

# Run the complete build pipeline
build_scripts\windows\build_and_package.bat
```

This will:
- ✅ Create virtual environment
- ✅ Install dependencies
- ✅ Build standalone executable
- ✅ Create Windows installer (if Inno Setup available)

### Option 2: Manual Build

```batch
# 1. Setup Python environment
python -m venv venv
venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements-windows.txt

# 3. Build executable
pyinstaller --clean build_scripts\windows\TuxTray.spec

# 4. Create installer (if Inno Setup installed)
iscc build_scripts\windows\TuxTray_Installer.iss
```

---

## 📦 Build Outputs

### Standalone Executable
- **Location**: `dist\TuxTray\TuxTray.exe`
- **Size**: ~80-120 MB (includes all dependencies)
- **Usage**: Can be run directly or distributed as a folder

### Windows Installer
- **Location**: `dist\installer\TuxTray-2.0.0-Windows-Setup.exe`
- **Size**: ~40-60 MB (compressed)
- **Features**:
  - Professional installation wizard
  - Start Menu shortcuts
  - Desktop icon (optional)
  - Auto-start option
  - Clean uninstaller
  - Registry integration

---

## 🔧 Build Configuration

### PyInstaller Settings

The `TuxTray.spec` file configures:
- **Console**: Hidden for release builds
- **Icon**: Windows `.ico` format (auto-generated from PNG)
- **Version Info**: Professional executable metadata
- **Dependencies**: Optimized bundle with excluded unused packages
- **Assets**: All penguin animations and configurations included

### Installer Features

The Inno Setup script provides:
- **Windows 10/11 compatibility**
- **Single-file installer**
- **No admin rights required**
- **Automatic startup option**
- **Clean uninstall process**
- **Registry integration**

---

## 🧪 Testing

### Manual Testing Checklist

1. **Installation Test**
   ```batch
   # Run the installer
   dist\installer\TuxTray-2.0.0-Windows-Setup.exe
   
   # Verify installation locations
   # - Program Files\TuxTray\TuxTray.exe
   # - Start Menu shortcut
   # - Desktop icon (if selected)
   ```

2. **Functionality Test**
   - ✅ System tray icon appears
   - ✅ Animations play correctly
   - ✅ Right-click menu works
   - ✅ Emotion modes function
   - ✅ Tooltips show system stats
   - ✅ Application exits cleanly

3. **System Integration Test**
   - ✅ Auto-start works (if enabled)
   - ✅ Taskbar integration
   - ✅ Windows notifications
   - ✅ No console window in production

### Automated Testing

```batch
# Test system monitor functionality
python -m pytest test_tuxtray.py

# Test Windows-specific features
python -c "import sys; print('Platform:', sys.platform)"
python -c "from src.system_monitor import SystemMonitor; m=SystemMonitor(); print(m.get_system_info())"
```

---

## 📋 Troubleshooting

### Common Build Issues

**1. PyInstaller Import Errors**
```
Solution: Add missing imports to hiddenimports in TuxTray.spec
```

**2. Missing Icon File**
```
Error: icon.ico not found
Solution: Build script auto-creates from PNG, or manually convert:
python -c "from PIL import Image; img = Image.open('assets/skins/default/calm/frame_0001.png'); img.save('assets/icon.ico')"
```

**3. Large Executable Size**
```
Solution: Enable UPX compression in TuxTray.spec (requires UPX installed)
```

**4. Antivirus False Positives**
```
Solution: Code-sign the executable or submit to antivirus vendors for whitelisting
```

### Runtime Issues

**1. System Tray Not Available**
```
Check: Windows system tray settings
- Settings > Personalization > Taskbar > Notification area
```

**2. Animations Not Playing**
```
Check: Asset files included in dist folder
Verify: assets/skins/default/ structure is complete
```

**3. High CPU Usage**
```
Solution: Adjust polling interval in config.json
"poll_interval_ms": 1000  # Increase from default 500ms
```

---

## 🎯 Distribution

### Release Checklist

1. **Build Verification**
   - ✅ Executable runs on clean Windows system
   - ✅ Installer works without errors
   - ✅ All features functional

2. **File Preparation**
   ```
   TuxTray-2.0.0-Windows-x64.zip         # Standalone folder
   TuxTray-2.0.0-Windows-Setup.exe       # Installer
   TuxTray-2.0.0-Windows-Portable.exe    # Single-file version (optional)
   ```

3. **GitHub Release**
   - Upload both installer and portable versions
   - Include Windows-specific installation instructions
   - Add system requirements
   - Include changelog

4. **Code Signing (Recommended)**
   ```batch
   # Sign executable with certificate
   signtool sign /f certificate.p12 /p password /t http://timestamp.digicert.com TuxTray.exe
   ```

---

## 🔄 Automated CI/CD (Future)

Consider setting up GitHub Actions for automatic Windows builds:

```yaml
# .github/workflows/windows-build.yml
name: Windows Build
on: [push, pull_request]
jobs:
  build:
    runs-on: windows-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.10'
      - run: pip install -r requirements-windows.txt
      - run: pyinstaller --clean build_scripts/windows/TuxTray.spec
      - uses: actions/upload-artifact@v3
        with:
          name: TuxTray-Windows
          path: dist/TuxTray/
```

---

## 📞 Support

For Windows-specific issues:
1. Check this documentation first
2. Review the [main README](README.md)
3. Open an issue on [GitHub](https://github.com/mfscpayload-690/TuxTray/issues)
4. Include system information and error details

**Windows System Info Command:**
```batch
systeminfo | findstr /B /C:"OS Name" /C:"OS Version" /C:"System Type"
```
