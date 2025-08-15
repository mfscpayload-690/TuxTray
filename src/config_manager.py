"""
Configuration Manager for TuxTray
Handles loading and saving of application settings and skin configurations.
"""

import json
import os
from pathlib import Path
from typing import Dict, Any, Optional


class ConfigManager:
    """Manages TuxTray configuration and skin metadata."""
    
    def __init__(self, config_path: Optional[str] = None):
        """Initialize the configuration manager."""
        if config_path is None:
            # Default to assets/config.json relative to project root
            self.config_path = Path(__file__).parent.parent / "assets" / "config.json"
        else:
            self.config_path = Path(config_path)
        
        self.config = self._load_config()
    
    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from JSON file."""
        try:
            with open(self.config_path, 'r') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Warning: Could not load config from {self.config_path}: {e}")
            return self._get_default_config()
    
    def _get_default_config(self) -> Dict[str, Any]:
        """Return default configuration if config file is missing."""
        return {
            "skins": {},
            "thresholds": {
                "cpu": {"idle": 30, "walk": 80},
                "ram": {"idle": 40, "walk": 85},
                "network": {"idle_kbps": 100, "walk_kbps": 1000}
            },
            "emotion_thresholds": {
                "calm": {"cpu_max": 20, "ram_max": 30, "network_max_kbps": 50},
                "active": {"cpu_range": [20, 60], "ram_range": [30, 70], "network_range_kbps": [50, 500]},
                "busy": {"single_resource_threshold": 60},
                "stressed": {"multiple_resources_threshold": 70, "cpu_high": 70, "ram_high": 75, "network_high_kbps": 800},
                "overloaded": {"cpu_critical": 90, "ram_critical": 90, "network_critical_kbps": 2000, "any_critical_threshold": 85}
            },
            "settings": {
                "poll_interval_ms": 500,
                "animation_mode": "emotion",
                "current_skin": "default",
                "tray_icon_size": 32,
                "emotion_system_enabled": True
            }
        }
    
    def save_config(self) -> bool:
        """Save current configuration to file."""
        try:
            os.makedirs(self.config_path.parent, exist_ok=True)
            with open(self.config_path, 'w') as f:
                json.dump(self.config, f, indent=4)
            return True
        except Exception as e:
            print(f"Error saving config: {e}")
            return False
    
    def get_setting(self, key: str, default: Any = None) -> Any:
        """Get a setting value."""
        return self.config.get("settings", {}).get(key, default)
    
    def set_setting(self, key: str, value: Any) -> None:
        """Set a setting value."""
        if "settings" not in self.config:
            self.config["settings"] = {}
        self.config["settings"][key] = value
    
    def get_skin_info(self, skin_name: str) -> Optional[Dict[str, Any]]:
        """Get information about a specific skin."""
        return self.config.get("skins", {}).get(skin_name)
    
    def get_available_skins(self) -> Dict[str, str]:
        """Get list of available skins with their display names."""
        skins = {}
        for skin_id, skin_data in self.config.get("skins", {}).items():
            skins[skin_id] = skin_data.get("name", skin_id.title())
        return skins
    
    def get_thresholds(self, mode: str) -> Dict[str, int]:
        """Get thresholds for a specific monitoring mode."""
        return self.config.get("thresholds", {}).get(mode, {})
    
    def get_animation_config(self, skin: str, animation: str) -> Dict[str, Any]:
        """Get animation configuration for a specific skin and animation type."""
        skin_data = self.get_skin_info(skin)
        if skin_data:
            return skin_data.get("animations", {}).get(animation, {})
        return {}
    
    @property
    def current_skin(self) -> str:
        """Get the currently selected skin."""
        return self.get_setting("current_skin", "default")
    
    @current_skin.setter
    def current_skin(self, skin_name: str) -> None:
        """Set the currently selected skin."""
        self.set_setting("current_skin", skin_name)
    
    @property
    def animation_mode(self) -> str:
        """Get the current animation mode."""
        return self.get_setting("animation_mode", "cpu")
    
    @animation_mode.setter
    def animation_mode(self, mode: str) -> None:
        """Set the animation mode."""
        if mode in ["cpu", "ram", "network", "emotion"]:
            self.set_setting("animation_mode", mode)
    
    @property
    def poll_interval(self) -> int:
        """Get the polling interval in milliseconds."""
        return self.get_setting("poll_interval_ms", 500)
    
    @property
    def tray_icon_size(self) -> int:
        """Get the tray icon size."""
        return self.get_setting("tray_icon_size", 32)
    
    def get_emotion_thresholds(self) -> Dict[str, Dict[str, Any]]:
        """Get emotion-based thresholds."""
        return self.config.get("emotion_thresholds", {})
    
    def set_emotion_thresholds(self, thresholds: Dict[str, Dict[str, Any]]) -> None:
        """Set emotion-based thresholds."""
        self.config["emotion_thresholds"] = thresholds
    
    @property
    def emotion_system_enabled(self) -> bool:
        """Check if emotion system is enabled."""
        return self.get_setting("emotion_system_enabled", True)
    
    @emotion_system_enabled.setter
    def emotion_system_enabled(self, enabled: bool) -> None:
        """Enable or disable emotion system."""
        self.set_setting("emotion_system_enabled", enabled)
    
    def get_available_emotions(self) -> list:
        """Get list of available emotion states."""
        return list(self.get_emotion_thresholds().keys())
