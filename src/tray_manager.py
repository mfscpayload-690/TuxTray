"""
Tray Manager for TuxTray
Handles system tray icon, context menu, and Linux desktop integration.
"""

import sys
from typing import Optional, Dict, Callable
from PySide6.QtWidgets import (QSystemTrayIcon, QMenu, 
                               QApplication, QMessageBox)
from PySide6.QtGui import QIcon, QPixmap, QAction, QActionGroup
from PySide6.QtCore import QObject, Signal

from .config_manager import ConfigManager
from .animation_engine import AnimationEngine


class TrayManager(QObject):
    """Manages the system tray icon and context menu for TuxTray."""
    
    # Signals
    quit_requested = Signal()
    animation_mode_changed = Signal(str)
    skin_changed = Signal(str)
    
    def __init__(self, config_manager: ConfigManager, 
                 animation_engine: AnimationEngine, parent=None):
        """Initialize the tray manager."""
        super().__init__(parent)
        
        self.config = config_manager
        self.animation_engine = animation_engine
        self.tray_icon: Optional[QSystemTrayIcon] = None
        self.context_menu: Optional[QMenu] = None
        
        # Action groups for radio button behavior
        self.animation_mode_group: Optional[QActionGroup] = None
        self.skin_group: Optional[QActionGroup] = None
        
        # Check if system tray is available
        if not QSystemTrayIcon.isSystemTrayAvailable():
            print("Warning: System tray is not available on this system")
            return
        
        self._create_tray_icon()
        self._create_context_menu()
        self._connect_signals()
    
    def _create_tray_icon(self) -> None:
        """Create the system tray icon."""
        self.tray_icon = QSystemTrayIcon(self)
        
        # Set initial icon (will be updated by animation)
        initial_pixmap = self.animation_engine.get_current_frame()
        if not initial_pixmap.isNull():
            self.tray_icon.setIcon(QIcon(initial_pixmap))
        else:
            # Fallback to default icon if animation isn't ready
            self._set_fallback_icon()
        
        # Set tooltip
        self.tray_icon.setToolTip("TuxTray - CPU Usage Monitor")
        
        # Show the tray icon
        self.tray_icon.show()
    
    def _set_fallback_icon(self) -> None:
        """Set a fallback icon when animation frames aren't available."""
        # Create a simple colored square as fallback
        fallback_pixmap = QPixmap(32, 32)
        fallback_pixmap.fill(0x2196F3)  # Blue color
        
        if self.tray_icon:
            self.tray_icon.setIcon(QIcon(fallback_pixmap))
    
    def _create_context_menu(self) -> None:
        """Create the right-click context menu."""
        if not self.tray_icon:
            return
        
        self.context_menu = QMenu()
        
        # Animation Mode submenu
        mode_menu = QMenu("Animation Mode", self.context_menu)
        self.animation_mode_group = QActionGroup(self)
        self.animation_mode_group.setExclusive(True)
        
        current_mode = self.config.animation_mode
        
        # Add animation mode options
        for mode, display_name in [
            ("emotion", "🎭 Emotion Mode (All Resources)"),
            ("cpu", "💻 CPU Usage"),
            ("ram", "🧠 RAM Usage"),
            ("network", "🌐 Network Activity")
        ]:
            action = QAction(display_name, self)
            action.setCheckable(True)
            action.setChecked(mode == current_mode)
            action.setData(mode)  # Store mode identifier
            
            self.animation_mode_group.addAction(action)
            mode_menu.addAction(action)
        
        # Connect animation mode group
        self.animation_mode_group.triggered.connect(self._on_animation_mode_changed)
        
        # Penguin Skin submenu
        skin_menu = QMenu("Penguin Skin", self.context_menu)
        self.skin_group = QActionGroup(self)
        self.skin_group.setExclusive(True)
        
        self._populate_skin_menu(skin_menu)
        
        # Connect skin group
        self.skin_group.triggered.connect(self._on_skin_changed)
        
        # Separator
        self.context_menu.addSeparator()
        
        # Add main menu items
        self.context_menu.addMenu(mode_menu)
        self.context_menu.addMenu(skin_menu)
        
        self.context_menu.addSeparator()
        
        # About action
        about_action = QAction("About TuxTray", self)
        about_action.triggered.connect(self._show_about)
        self.context_menu.addAction(about_action)
        
        self.context_menu.addSeparator()
        
        # Quit action
        quit_action = QAction("Quit", self)
        quit_action.triggered.connect(self.quit_requested.emit)
        self.context_menu.addAction(quit_action)
        
        # Set the context menu
        self.tray_icon.setContextMenu(self.context_menu)
    
    def _populate_skin_menu(self, skin_menu: QMenu) -> None:
        """Populate the skin selection menu."""
        available_skins = self.config.get_available_skins()
        current_skin = self.config.current_skin
        
        if not available_skins:
            # No skins available
            no_skins_action = QAction("No skins available", self)
            no_skins_action.setEnabled(False)
            skin_menu.addAction(no_skins_action)
            return
        
        # Add skin options
        for skin_id, skin_name in available_skins.items():
            action = QAction(skin_name, self)
            action.setCheckable(True)
            action.setChecked(skin_id == current_skin)
            action.setData(skin_id)  # Store skin identifier
            
            self.skin_group.addAction(action)
            skin_menu.addAction(action)
    
    def _connect_signals(self) -> None:
        """Connect animation engine signals."""
        # Update tray icon when animation frame changes
        self.animation_engine.frame_changed.connect(self._on_frame_changed)
        
        # Handle tray icon activation (left-click)
        if self.tray_icon:
            self.tray_icon.activated.connect(self._on_tray_activated)
    
    def _on_frame_changed(self, pixmap: QPixmap) -> None:
        """Handle animation frame changes."""
        if self.tray_icon and not pixmap.isNull():
            self.tray_icon.setIcon(QIcon(pixmap))
    
    def _on_tray_activated(self, reason: QSystemTrayIcon.ActivationReason) -> None:
        """Handle tray icon activation."""
        if reason == QSystemTrayIcon.ActivationReason.DoubleClick:
            # Double-click could show a settings dialog in the future
            self._show_about()
    
    def _on_animation_mode_changed(self, action: QAction) -> None:
        """Handle animation mode change."""
        mode = action.data()
        if mode and mode != self.config.animation_mode:
            self.config.animation_mode = mode
            self.config.save_config()
            self.animation_mode_changed.emit(mode)
            
            # Update tooltip
            mode_names = {
                "emotion": "Emotion-Based Monitor",
                "cpu": "CPU Usage Monitor",
                "ram": "RAM Usage Monitor", 
                "network": "Network Activity Monitor"
            }
            tooltip = f"TuxTray - {mode_names.get(mode, 'System Monitor')}"
            
            if self.tray_icon:
                self.tray_icon.setToolTip(tooltip)
    
    def _on_skin_changed(self, action: QAction) -> None:
        """Handle skin change."""
        skin_id = action.data()
        if skin_id and skin_id != self.config.current_skin:
            if self.animation_engine.set_skin(skin_id):
                self.config.save_config()
                self.skin_changed.emit(skin_id)
                
                # Show notification
                if self.tray_icon:
                    skin_info = self.config.get_skin_info(skin_id)
                    skin_name = skin_info.get("name", skin_id) if skin_info else skin_id
                    self.tray_icon.showMessage(
                        "TuxTray",
                        f"Changed to {skin_name}",
                        QSystemTrayIcon.MessageIcon.Information,
                        2000
                    )
    
    def _show_about(self) -> None:
        """Show about dialog."""
        about_text = """
        <h3>🐧 TuxTray</h3>
        <p>An ultra-cute system tray penguin that reacts to your system's resource usage!</p>
        
        <p><b>Current Status:</b><br>
        Animation Mode: {}<br>
        Current Skin: {}<br>
        Polling Interval: {}ms</p>
        
        <p><b>Features:</b></p>
        <ul>
        <li>Real-time system monitoring</li>
        <li>Animated penguin mascot</li>
        <li>Multiple animation modes</li>
        <li>Customizable skins</li>
        </ul>
        
        <p>Made with ❤️ for Linux nerds.<br>
        <small>MIT License © 2025 Aravind Lal</small></p>
        """.format(
            self.config.animation_mode.upper(),
            self.config.get_available_skins().get(self.config.current_skin, "Unknown"),
            self.config.poll_interval
        )
        
        msg_box = QMessageBox()
        msg_box.setWindowTitle("About TuxTray")
        msg_box.setText(about_text)
        msg_box.setIcon(QMessageBox.Icon.Information)
        
        # Set the penguin icon for the message box
        current_frame = self.animation_engine.get_current_frame()
        if not current_frame.isNull():
            msg_box.setIconPixmap(current_frame.scaled(64, 64))
        
        msg_box.exec()
    
    def show_notification(self, title: str, message: str, 
                         duration: int = 3000) -> None:
        """Show a system tray notification."""
        if self.tray_icon:
            self.tray_icon.showMessage(
                title, message,
                QSystemTrayIcon.MessageIcon.Information,
                duration
            )
    
    def update_tooltip(self, stats_text: str) -> None:
        """Update the tray icon tooltip with current stats."""
        if self.tray_icon:
            base_tooltip = f"TuxTray - {self.config.animation_mode.upper()} Mode"
            full_tooltip = f"{base_tooltip}\n{stats_text}"
            self.tray_icon.setToolTip(full_tooltip)
    
    def is_available(self) -> bool:
        """Check if system tray is available."""
        return QSystemTrayIcon.isSystemTrayAvailable() and self.tray_icon is not None
    
    def refresh_skin_menu(self) -> None:
        """Refresh the skin menu (call when new skins are added)."""
        if self.context_menu and self.skin_group:
            # Find and remove old skin menu
            for action in self.context_menu.actions():
                if action.menu() and action.menu().title() == "Penguin Skin":
                    self.context_menu.removeAction(action)
                    action.menu().deleteLater()
                    break
            
            # Clear old skin actions
            for action in self.skin_group.actions():
                self.skin_group.removeAction(action)
                action.deleteLater()
            
            # Create new skin menu
            skin_menu = QMenu("Penguin Skin", self.context_menu)
            self._populate_skin_menu(skin_menu)
            
            # Insert before the separator
            actions = self.context_menu.actions()
            if len(actions) >= 2:
                self.context_menu.insertMenu(actions[1], skin_menu)


# Testing function
def main():
    """Test the tray manager."""
    import sys
    from PySide6.QtWidgets import QApplication
    
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)  # Keep running when no windows open
    
    if not QSystemTrayIcon.isSystemTrayAvailable():
        print("System tray is not available on this system")
        return
    
    config = ConfigManager()
    animation_engine = AnimationEngine(config)
    tray_manager = TrayManager(config, animation_engine)
    
    if not tray_manager.is_available():
        print("Failed to create tray icon")
        return
    
    # Connect quit signal
    tray_manager.quit_requested.connect(app.quit)
    
    # Start animation
    animation_engine.start()
    
    print("TuxTray is running. Right-click the tray icon for options.")
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
