# 🐧 TuxTray - The Intelligent Penguin System Monitor

<div align="center">

![TuxTray Logo](https://img.shields.io/badge/TuxTray-System%20Monitor-blue?style=for-the-badge&logo=linux&logoColor=white)

**An intelligent animated penguin that lives in your system tray and reacts emotionally to your system's health!**

*From calm dancing when your system is idle to frantic running when resources are stressed — your penguin companion understands your computer better than anyone.*

![Python Version](https://img.shields.io/badge/python-3.10%2B-blue.svg?style=flat-square)
![License](https://img.shields.io/badge/license-MIT-green.svg?style=flat-square)
![Platform](https://img.shields.io/badge/platform-Linux%20%7C%20Windows-lightgrey.svg?style=flat-square)
![Qt Framework](https://img.shields.io/badge/GUI-PySide6%20(Qt6)-brightgreen.svg?style=flat-square)
![Architecture](https://img.shields.io/badge/architecture-Event%20Driven-orange.svg?style=flat-square)

</div>

---

## 🌟 **NEW: Advanced 5-State Emotion System!**

### 🎭 The 5 Penguin Emotions

| Emotion | Trigger | Animation | System State |
|---------|---------|-----------|-------------|
| 😌 **Calm** | All resources low | Dancing peacefully | System at rest |
| 🚶 **Active** | Normal activity | Casual walking | Regular computing |
| 🏃 **Busy** | Single resource high | Running at normal pace | Focused workload |
| 😰 **Stressed** | Multiple resources strained | Running frantically | Heavy multitasking |
| 🥵 **Overloaded** | Critical system stress | Collapsing from exhaustion | System at breaking point |

**Example Scenarios:**
```
CPU 15%, RAM 25%, Network 10 KB/s  → 😌 CALM (dancing)
CPU 45%, RAM 50%, Network 200 KB/s → 🚶 ACTIVE (walking)  
CPU 80%, RAM 80%, Network 600 KB/s → 😰 STRESSED (frantic running)
CPU 95%, RAM 40%, Network 100 KB/s → 🥵 OVERLOADED (collapsing)
```

---

## ✨ Features

### 🎯 Core Functionality
- **🧠 Advanced Emotion System**: 5-state intelligent monitoring (NEW!)
- **Real-time System Monitoring**: CPU, RAM, and network usage tracking
- **Reactive Animations**: Penguin behavior changes based on system load
- **Multiple Animation Modes**:
  - 🎭 **Emotion Mode** (NEW!): Multi-resource emotional intelligence
  - 🖥️ **CPU Mode**: Penguin speed reflects CPU usage
  - 💾 **RAM Mode**: Animation responds to memory consumption
  - 🌐 **Network Mode**: Activity based on network throughput
- **Smart Thresholds**: Configurable thresholds for all monitoring modes
- **System Tray Integration**: Native system tray with context menu
- **Real-time Tooltips**: Hover to see current system stats and stress levels

### 🎨 Visual & UI
- **High-Quality Animations**: Smooth frame-based penguin animations
- **Customizable Skins**: Support for multiple penguin themes
- **Configurable Settings**: Adjustable polling intervals and thresholds
- **Native Integration**: Works seamlessly with your desktop environment

### 🔧 Technical Features
- **Modular Architecture**: Clean separation of concerns
- **Configuration Management**: JSON-based settings with live updates
- **Signal Handling**: Graceful shutdown on system signals
- **Cross-Platform Support**: Linux and Windows compatibility

---

## 🛠️ Tech Stack

- **Language:** Python 3.10+
- **GUI Framework:** PySide6 (Qt6)
- **System Monitoring:** `psutil`
- **Image Processing:** `Pillow`
- **Packaging:** `PyInstaller`
- **Architecture:** Event-driven with Qt signals/slots

---

## 📦 Installation

### Prerequisites

#### Linux (Ubuntu/Debian)
```bash
# Install system dependencies
sudo apt update
sudo apt install python3-pip python3-venv libxcb-cursor0

# For system tray support (if not already installed)
sudo apt install libappindicator3-1
```

#### Linux (Fedora/RHEL)
```bash
sudo dnf install python3-pip python3-virtualenv libxcb-cursor
```

### Installation Methods

#### Method 1: From Source (Recommended for Development)
```bash
# Clone the repository
git clone https://github.com/mfscpayload-690/TuxTray.git
cd TuxTray

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run TuxTray
python3 main.py
```

#### Method 2: Using setup.py
```bash
# Install in development mode
pip install -e .

# Or install normally
pip install .

# Run from anywhere
tuxtray
```

#### Method 3: Standalone Executables
*Coming soon - check the Releases page for pre-built executables*

### 🎨 Premium Assets (Optional)

TuxTray comes with lightweight placeholder animations. For the **full premium experience** with high-quality penguin animations:

```bash
# Download premium assets (46MB)
git clone https://github.com/mfscpayload-690/TuxTray-Assets.git

# Copy to your TuxTray installation
cp TuxTray-Assets/*.gif TuxTray/assets/

# Restart TuxTray to enjoy premium animations!
```

**Premium Assets Include:**
- 🎭 High-quality AI-generated penguin animations
- 🎬 Smooth frame transitions and realistic movements  
- 📐 Multiple animation states (idle, walk, run, overload)
- 🎨 Professional quality suitable for daily use

---

## 🚀 Usage

### Basic Usage
```bash
# Start TuxTray
python3 main.py

# Or if installed via setup.py
tuxtray
```

### System Tray Menu
Right-click the penguin icon in your system tray to access:
- **Animation Modes**: Switch between CPU, RAM, and Network monitoring
- **Skins**: Change penguin appearance (when multiple skins are available)
- **Settings**: Configure thresholds and polling intervals
- **About**: View version and information
- **Quit**: Exit TuxTray

### Keyboard Shortcuts
- `Ctrl+C` in terminal: Graceful shutdown

---

## 📂 Project Structure

```
TuxTray/
├── assets/                     # Animation assets and configuration
│   ├── skins/                  # Penguin skin directories
│   │   └── default/           # Default penguin skin
│   │       ├── idle/          # Idle animation frames
│   │       ├── walk/          # Walking animation frames
│   │       └── run/           # Running animation frames
│   └── config.json            # Animation and threshold configuration
├── src/                       # Source code modules
│   ├── main.py               # Application entry point
│   ├── config_manager.py     # Configuration management
│   ├── system_monitor.py     # System resource monitoring
│   ├── animation_engine.py   # Animation frame management
│   ├── tray_manager.py       # System tray integration
│   └── utils/                # Utility modules
├── build_scripts/            # Build and packaging scripts
├── main.py                   # Main application launcher
├── setup.py                  # Installation script
├── requirements.txt          # Python dependencies
├── test_tuxtray.py          # Unit tests
└── stress_test.py           # Performance testing
```

---

## ⚙️ Configuration

TuxTray uses a JSON configuration file at `assets/config.json`. Key settings include:

### Thresholds
```json
{
  "thresholds": {
    "cpu": { "idle": 30, "walk": 80 },
    "ram": { "idle": 40, "walk": 85 },
    "network": { "idle_kbps": 100, "walk_kbps": 1000 }
  }
}
```

### Settings
```json
{
  "settings": {
    "poll_interval_ms": 500,
    "animation_mode": "cpu",
    "current_skin": "default",
    "tray_icon_size": 32
  }
}
```

---

## 🧪 Testing

```bash
# Run unit tests
python3 -m pytest test_tuxtray.py

# Run stress test to simulate high system load
python3 stress_test.py

# Debug animation performance
python3 debug_animation.py
```

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit pull requests, create issues, or suggest new features.

### Development Setup
```bash
git clone https://github.com/mfscpayload-690/TuxTray.git
cd TuxTray
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python3 main.py
```

### Guidelines
- Follow PEP 8 style guidelines
- Add tests for new features
- Update documentation as needed
- Test on multiple platforms when possible

---

## 📜 License

MIT License - see [LICENSE](LICENSE) for details.

**Copyright © 2025 Aravind Lal**

Free to use, modify, and distribute. Made with ❤️ for the Linux community and system monitoring enthusiasts.

---

## 🙏 Acknowledgments

- Penguin animations generated with AI assistance
- Built with the excellent PySide6 framework
- System monitoring powered by psutil
- Inspired by the Linux penguin mascot Tux
