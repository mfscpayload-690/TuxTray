#!/usr/bin/env python3
"""
Test script for TuxTray components
"""

import sys
import os
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

def test_imports():
    """Test that all modules can be imported."""
    try:
        from src.config_manager import ConfigManager
        from src.system_monitor import SystemMonitor
        from src.animation_engine import AnimationEngine
        from src.tray_manager import TrayManager
        from src.main import TuxTrayApp
        print("✓ All imports successful")
        return True
    except ImportError as e:
        print(f"✗ Import error: {e}")
        return False

def test_config():
    """Test configuration manager."""
    try:
        from src.config_manager import ConfigManager
        config = ConfigManager()
        
        print(f"✓ Config loaded: {config.current_skin}")
        print(f"✓ Animation mode: {config.animation_mode}")
        print(f"✓ Available skins: {list(config.get_available_skins().keys())}")
        return True
    except Exception as e:
        print(f"✗ Config test failed: {e}")
        return False

def test_system_monitor():
    """Test system monitoring."""
    try:
        from src.system_monitor import SystemMonitor
        monitor = SystemMonitor()
        stats = monitor.get_system_stats()
        
        print(f"✓ System stats: CPU={stats.cpu_percent:.1f}%, RAM={stats.ram_percent:.1f}%")
        return True
    except Exception as e:
        print(f"✗ System monitor test failed: {e}")
        return False

def test_assets():
    """Test that animation assets exist."""
    assets_path = Path(__file__).parent / "assets" / "skins" / "default"
    
    animations = ["idle", "walk", "run"]
    for anim in animations:
        anim_path = assets_path / anim
        if anim_path.exists():
            frame_count = len(list(anim_path.glob("*.png")))
            print(f"✓ {anim} animation: {frame_count} frames")
        else:
            print(f"✗ Missing animation: {anim}")
            return False
    
    return True

def test_gui_availability():
    """Test if GUI components can be initialized."""
    try:
        from PySide6.QtWidgets import QApplication, QSystemTrayIcon
        
        # Create minimal app to test Qt
        app = QApplication([])
        
        if QSystemTrayIcon.isSystemTrayAvailable():
            print("✓ System tray is available")
        else:
            print("✗ System tray is not available (this is expected in some environments)")
        
        print("✓ Qt GUI components available")
        app.quit()
        return True
    except Exception as e:
        print(f"✗ GUI test failed: {e}")
        return False

def main():
    """Run all tests."""
    print("🐧 TuxTray Component Test Suite")
    print("=" * 40)
    
    tests = [
        ("Imports", test_imports),
        ("Configuration", test_config),
        ("System Monitor", test_system_monitor),
        ("Animation Assets", test_assets),
        ("GUI Availability", test_gui_availability),
    ]
    
    passed = 0
    for test_name, test_func in tests:
        print(f"\n{test_name}:")
        if test_func():
            passed += 1
    
    print(f"\n" + "=" * 40)
    print(f"Tests passed: {passed}/{len(tests)}")
    
    if passed == len(tests):
        print("🎉 All tests passed! TuxTray is ready to run.")
        return 0
    else:
        print("❌ Some tests failed. Please check the errors above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
