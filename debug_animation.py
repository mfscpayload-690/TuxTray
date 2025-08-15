#!/usr/bin/env python3
"""
Debug Animation Engine
Test animation cycling and system monitoring integration.
"""

import sys
import time
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QTimer

from src.config_manager import ConfigManager
from src.system_monitor import SystemMonitor
from src.animation_engine import AnimationEngine

def main():
    """Debug the animation system."""
    print("🐧 TuxTray Animation Debug")
    print("=" * 40)
    
    app = QApplication(sys.argv)
    
    # Initialize components
    config = ConfigManager()
    monitor = SystemMonitor()
    engine = AnimationEngine(config)
    
    print(f"Available skins: {engine.get_available_skins()}")
    print(f"Available animations: {engine.get_available_animations()}")
    print()
    
    # Test system monitoring
    stats = monitor.get_system_stats()
    print(f"Current stats:")
    print(f"  CPU: {stats.cpu_percent:.1f}%")
    print(f"  RAM: {stats.ram_percent:.1f}%")
    print(f"  Network: {stats.network_kbps:.1f} KB/s")
    print()
    
    # Test animation state determination
    cpu_thresholds = config.get_thresholds("cpu")
    cpu_state = monitor.determine_animation_state(stats, "cpu", cpu_thresholds)
    
    ram_thresholds = config.get_thresholds("ram")
    ram_state = monitor.determine_animation_state(stats, "ram", ram_thresholds)
    
    network_thresholds = config.get_thresholds("network")
    network_state = monitor.determine_animation_state(stats, "network", network_thresholds)
    
    print(f"Animation states based on current usage:")
    print(f"  CPU mode: {cpu_state} (thresholds: {cpu_thresholds})")
    print(f"  RAM mode: {ram_state} (thresholds: {ram_thresholds})")
    print(f"  Network mode: {network_state} (thresholds: {network_thresholds})")
    print()
    
    # Frame change counter
    frame_count = {'count': 0, 'last_animation': ''}
    
    def on_frame_change(pixmap):
        frame_count['count'] += 1
        current_anim = engine.current_animation_name if engine.current_animation else 'None'
        if current_anim != frame_count['last_animation']:
            print(f"Animation changed to: {current_anim}")
            frame_count['last_animation'] = current_anim
        
        if frame_count['count'] % 30 == 0:  # Every 30 frames
            print(f"Frame update #{frame_count['count']}: {current_anim} ({pixmap.width()}x{pixmap.height()})")
    
    # Connect frame change signal
    engine.frame_changed.connect(on_frame_change)
    
    print("Starting animation test...")
    print("Will test: idle → walk → run → idle")
    print("Press Ctrl+C to stop")
    print()
    
    # Start animation engine
    engine.start()
    
    # Schedule animation changes
    def test_sequence():
        print("Setting animation to: idle")
        engine.set_animation("idle")
        
        QTimer.singleShot(3000, lambda: (
            print("Setting animation to: walk"),
            engine.set_animation("walk")
        ))
        
        QTimer.singleShot(6000, lambda: (
            print("Setting animation to: run"), 
            engine.set_animation("run")
        ))
        
        QTimer.singleShot(9000, lambda: (
            print("Setting animation to: idle"),
            engine.set_animation("idle")
        ))
        
        QTimer.singleShot(12000, app.quit)
    
    # Start test sequence
    QTimer.singleShot(1000, test_sequence)
    
    # Run for 12 seconds
    try:
        sys.exit(app.exec())
    except KeyboardInterrupt:
        print("Test interrupted by user")
        engine.stop()

if __name__ == "__main__":
    main()
