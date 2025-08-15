"""
TuxTray - Main Application
==========================

Entry point for the TuxTray application.
This module ties together the configuration, system monitoring, animation, 
and tray icon management to bring the reactive penguin to life.

Author: Aravind Lal
License: MIT
"""

import sys
import signal
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QTimer, QObject, Signal, Slot

from .config_manager import ConfigManager
from .system_monitor import SystemMonitor, SystemStats
from .animation_engine import AnimationEngine
from .tray_manager import TrayManager


class TuxTrayApp(QObject):
    """Main application class for TuxTray."""
    
    def __init__(self, parent=None):
        """Initialize the TuxTray application."""
        super().__init__(parent)
        
        # Initialize core components
        self.config_manager = ConfigManager()
        self.system_monitor = SystemMonitor()
        self.animation_engine = AnimationEngine(self.config_manager)
        self.tray_manager = TrayManager(self.config_manager, self.animation_engine)
        
        # System stats polling timer
        self.poll_timer = QTimer(self)
        self.poll_timer.setInterval(self.config_manager.poll_interval)
        self.poll_timer.timeout.connect(self.update_system_stats)
        
        # Connect signals
        self._connect_signals()
    
    def _connect_signals(self):
        """Connect signals between components."""
        self.tray_manager.quit_requested.connect(self.quit)
        self.tray_manager.animation_mode_changed.connect(
            self._handle_animation_mode_change
        )
        self.tray_manager.skin_changed.connect(self._handle_skin_change)
    
    def start(self):
        """Start the application."""
        print("Starting TuxTray...")
        
        if not self.tray_manager.is_available():
            print("Error: System tray not available. Exiting.", file=sys.stderr)
            return
        
        # Start animation and monitoring
        self.animation_engine.start()
        self.poll_timer.start()
        
        # Initial update
        self.update_system_stats()
        
        # Show startup notification
        self.tray_manager.show_notification(
            "TuxTray is Running",
            "Your penguin is now monitoring system resources."
        )
        print("TuxTray is now running in the system tray.")
    
    @Slot()
    def update_system_stats(self):
        """Poll system stats and update animation."""
        stats = self.system_monitor.get_system_stats()
        
        # Determine new animation state
        mode = self.config_manager.animation_mode
        
        if mode == "emotion" and self.config_manager.emotion_system_enabled:
            # Use emotion system
            emotion_thresholds = self.config_manager.get_emotion_thresholds()
            new_state = self.system_monitor.determine_emotion_state(stats, emotion_thresholds)
        else:
            # Use legacy system
            thresholds = self.config_manager.get_thresholds(mode)
            new_state = self.system_monitor.determine_animation_state(stats, mode, thresholds)
        
        # Update animation if state changed
        if new_state != self.animation_engine.current_animation_name:
            self.animation_engine.set_animation(new_state)
        
        # Update tooltip
        self._update_tooltip(stats, mode)
    
    def _update_tooltip(self, stats: SystemStats, mode: str):
        """Update tray icon tooltip with current stats."""
        if mode == "emotion":
            # Show emotion state and overall system health
            emotion_thresholds = self.config_manager.get_emotion_thresholds()
            analysis = self.system_monitor.get_emotion_analysis(stats, emotion_thresholds)
            stats_text = f"Mood: {analysis['emotion'].title()} ({analysis['overall_stress']}% stress)"
        elif mode == "cpu":
            stats_text = f"CPU: {stats.cpu_percent:.1f}%"
        elif mode == "ram":
            stats_text = f"RAM: {stats.ram_percent:.1f}%"
        elif mode == "network":
            stats_text = f"Network: {stats.network_kbps:.1f} KB/s"
        else:
            stats_text = "Monitoring..."
            
        self.tray_manager.update_tooltip(stats_text)
    
    @Slot(str)
    def _handle_animation_mode_change(self, mode: str):
        """Handle changes in animation mode."""
        print(f"Animation mode changed to: {mode}")
        # Force immediate update to reflect new mode
        self.update_system_stats()
    
    @Slot(str)
    def _handle_skin_change(self, skin_name: str):
        """Handle changes to the penguin skin."""
        print(f"Skin changed to: {skin_name}")
        # Tooltip and other elements will update on next poll
    
    def quit(self):
        """Gracefully quit the application."""
        print("Shutting down TuxTray...")
        
        self.animation_engine.stop()
        self.poll_timer.stop()
        self.config_manager.save_config()
        
        QApplication.instance().quit()


def main():
    """
    Main function to run TuxTray.
    - Initializes QApplication
    - Sets up signal handling for graceful exit
    - Starts the main application logic
    """
    # Ensure proper handling of application identity on Linux
    if sys.platform == "linux":
        try:
            from ctypes import cdll, byref, create_string_buffer
            libc = cdll.LoadLibrary('libc.so.6')
            PR_SET_NAME = 15
            name = create_string_buffer(b"TuxTray")
            libc.prctl(PR_SET_NAME, byref(name), 0, 0, 0)
        except (ImportError, OSError) as e:
            print(f"Could not set process name: {e}")
    
    # Initialize Qt Application
    app = QApplication(sys.argv)
    app.setOrganizationName("TuxTray")
    app.setApplicationName("TuxTray")
    app.setQuitOnLastWindowClosed(False) # Important for tray apps
    
    # Create and start the main application
    tuxtray_app = TuxTrayApp()
    
    # Graceful exit on Ctrl+C
    def sigint_handler(*args):
        print("\nCtrl+C detected, shutting down...")
        tuxtray_app.quit()

    signal.signal(signal.SIGINT, sigint_handler)
    signal.signal(signal.SIGTERM, sigint_handler)
    
    # Use a timer to ensure signals are processed by the Python interpreter
    # This is required for SIGINT to work with Qt applications
    timer = QTimer()
    timer.start(500)
    timer.timeout.connect(lambda: None) # Let the interpreter run
    
    # Start the application
    tuxtray_app.start()
    
    sys.exit(app.exec())


if __name__ == "__main__":
    # This allows running the app directly from the source directory
    from pathlib import Path
    sys.path.insert(0, str(Path(__file__).parent.parent))
    main()
