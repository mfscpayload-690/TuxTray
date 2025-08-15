"""
Animation Engine for TuxTray
Handles loading and cycling through animation frames for the penguin mascot.
"""

import os
import time
from pathlib import Path
from typing import List, Dict, Optional, Tuple
from PySide6.QtGui import QPixmap, QIcon
from PySide6.QtCore import QTimer, QObject, Signal, Qt

from .config_manager import ConfigManager


class Animation:
    """Represents a single animation sequence."""
    
    def __init__(self, name: str, frames: List[QPixmap], fps: int = 24, loop: bool = True):
        """
        Initialize an animation.
        
        Args:
            name: Animation name (idle, walk, run)
            frames: List of QPixmap frames
            fps: Frames per second
            loop: Whether animation should loop
        """
        self.name = name
        self.frames = frames
        self.fps = fps
        self.loop = loop
        self.frame_duration_ms = int(1000 / fps) if fps > 0 else 42  # ~24fps default
        self.current_frame = 0
        self.last_frame_time = 0
    
    def get_current_frame(self) -> QPixmap:
        """Get the current animation frame."""
        if not self.frames:
            return QPixmap()
        return self.frames[self.current_frame]
    
    def advance_frame(self) -> bool:
        """
        Advance to next frame if enough time has passed.
        
        Returns:
            True if frame was advanced, False otherwise
        """
        current_time = int(time.time() * 1000)  # milliseconds
        
        if current_time - self.last_frame_time >= self.frame_duration_ms:
            if self.frames:
                self.current_frame = (self.current_frame + 1) % len(self.frames)
                self.last_frame_time = current_time
                return True
        
        return False
    
    def reset(self) -> None:
        """Reset animation to first frame."""
        self.current_frame = 0
        self.last_frame_time = int(time.time() * 1000)


class AnimationEngine(QObject):
    """Manages all animations and frame cycling for TuxTray."""
    
    # Signal emitted when animation frame changes
    frame_changed = Signal(QPixmap)
    
    def __init__(self, config_manager: ConfigManager, parent=None):
        """Initialize the animation engine."""
        super().__init__(parent)
        
        self.config = config_manager
        self.animations: Dict[str, Dict[str, Animation]] = {}  # skin -> animation -> Animation
        self.current_skin = ""
        self.current_animation_name = "idle"
        self.current_animation: Optional[Animation] = None
        
        # Animation timer
        self.timer = QTimer(self)
        self.timer.timeout.connect(self._update_frame)
        self.timer.setInterval(16)  # ~60 FPS update rate
        
        # Load initial skin
        self._load_skin(self.config.current_skin)
    
    def _get_assets_path(self) -> Path:
        """Get the path to the assets directory."""
        return Path(__file__).parent.parent / "assets"
    
    def _load_animation_frames(self, skin_path: Path, animation_name: str, 
                             icon_size: int = 32) -> List[QPixmap]:
        """
        Load animation frames from disk.
        
        Args:
            skin_path: Path to the skin directory
            animation_name: Name of the animation (idle, walk, run)
            icon_size: Size to scale the icons to
            
        Returns:
            List of QPixmap frames
        """
        animation_path = skin_path / animation_name
        frames = []
        
        if not animation_path.exists():
            print(f"Warning: Animation path not found: {animation_path}")
            return frames
        
        # Get all PNG files and sort them
        frame_files = sorted([f for f in animation_path.iterdir() 
                            if f.suffix.lower() == '.png'])
        
        for frame_file in frame_files:
            try:
                pixmap = QPixmap(str(frame_file))
                if not pixmap.isNull():
                    # Scale to tray icon size while maintaining aspect ratio
                    scaled_pixmap = pixmap.scaled(
                        icon_size, icon_size,
                        Qt.KeepAspectRatio,
                        Qt.SmoothTransformation
                    )
                    frames.append(scaled_pixmap)
                else:
                    print(f"Warning: Could not load frame: {frame_file}")
            except Exception as e:
                print(f"Error loading frame {frame_file}: {e}")
        
        print(f"Loaded {len(frames)} frames for {skin_path.name}/{animation_name}")
        return frames
    
    def _load_skin(self, skin_name: str) -> bool:
        """
        Load all animations for a specific skin.
        
        Args:
            skin_name: Name of the skin to load
            
        Returns:
            True if skin was loaded successfully
        """
        skin_path = self._get_assets_path() / "skins" / skin_name
        
        if not skin_path.exists():
            print(f"Warning: Skin path not found: {skin_path}")
            return False
        
        skin_info = self.config.get_skin_info(skin_name)
        if not skin_info:
            print(f"Warning: No config found for skin: {skin_name}")
            return False
        
        animations = {}
        icon_size = self.config.tray_icon_size
        
        # Load each animation type
        for anim_name, anim_config in skin_info.get("animations", {}).items():
            frames = self._load_animation_frames(skin_path, anim_name, icon_size)
            
            if frames:
                fps = anim_config.get("fps", 24)
                loop = anim_config.get("loop", True)
                
                animation = Animation(anim_name, frames, fps, loop)
                animations[anim_name] = animation
            else:
                print(f"Warning: No frames loaded for {skin_name}/{anim_name}")
        
        if animations:
            self.animations[skin_name] = animations
            self.current_skin = skin_name
            print(f"Successfully loaded skin: {skin_name} with {len(animations)} animations")
            return True
        
        return False
    
    def set_skin(self, skin_name: str) -> bool:
        """
        Change the current skin.
        
        Args:
            skin_name: Name of the new skin
            
        Returns:
            True if skin was changed successfully
        """
        if skin_name not in self.animations:
            if not self._load_skin(skin_name):
                return False
        
        self.current_skin = skin_name
        self.config.current_skin = skin_name
        
        # Reset current animation to the new skin
        self.set_animation(self.current_animation_name)
        return True
    
    def set_animation(self, animation_name: str) -> bool:
        """
        Change the current animation.
        
        Args:
            animation_name: Name of the animation (idle, walk, run)
            
        Returns:
            True if animation was changed successfully
        """
        if self.current_skin not in self.animations:
            return False
        
        skin_animations = self.animations[self.current_skin]
        
        if animation_name in skin_animations:
            # Reset the new animation
            new_animation = skin_animations[animation_name]
            new_animation.reset()
            
            self.current_animation = new_animation
            self.current_animation_name = animation_name
            
            # Emit the first frame
            self.frame_changed.emit(new_animation.get_current_frame())
            return True
        
        print(f"Warning: Animation '{animation_name}' not found in skin '{self.current_skin}'")
        return False
    
    def start(self) -> None:
        """Start the animation timer."""
        if not self.timer.isActive():
            # Set initial animation if none is set
            if not self.current_animation:
                # Try emotion-based animations first, fallback to legacy
                if not (self.set_animation("calm") or 
                        self.set_animation("active") or
                        self.set_animation("idle")):
                    print("Warning: No animations available")
            
            self.timer.start()
    
    def stop(self) -> None:
        """Stop the animation timer."""
        self.timer.stop()
    
    def _update_frame(self) -> None:
        """Internal method called by timer to update animation frames."""
        if self.current_animation:
            if self.current_animation.advance_frame():
                # Emit signal when frame changes
                self.frame_changed.emit(self.current_animation.get_current_frame())
    
    def get_current_frame(self) -> QPixmap:
        """Get the current animation frame."""
        if self.current_animation:
            return self.current_animation.get_current_frame()
        return QPixmap()
    
    def get_available_skins(self) -> List[str]:
        """Get list of available skins."""
        return list(self.animations.keys())
    
    def get_available_animations(self, skin_name: Optional[str] = None) -> List[str]:
        """Get list of available animations for a skin."""
        if skin_name is None:
            skin_name = self.current_skin
        
        if skin_name in self.animations:
            return list(self.animations[skin_name].keys())
        return []
    
    def reload_skin(self, skin_name: Optional[str] = None) -> bool:
        """
        Reload a skin from disk (useful for development).
        
        Args:
            skin_name: Skin to reload, or current skin if None
            
        Returns:
            True if skin was reloaded successfully
        """
        if skin_name is None:
            skin_name = self.current_skin
        
        # Remove from cache
        if skin_name in self.animations:
            del self.animations[skin_name]
        
        # Reload
        return self._load_skin(skin_name)


# Testing function
def main():
    """Test the animation engine."""
    import sys
    from PySide6.QtWidgets import QApplication
    
    app = QApplication(sys.argv)
    
    config = ConfigManager()
    engine = AnimationEngine(config)
    
    def on_frame_change(pixmap):
        print(f"Frame changed: {pixmap.size().width()}x{pixmap.size().height()}")
    
    engine.frame_changed.connect(on_frame_change)
    
    print("Starting animation test...")
    engine.start()
    
    # Test animation changes
    QTimer.singleShot(2000, lambda: engine.set_animation("walk"))
    QTimer.singleShot(4000, lambda: engine.set_animation("run"))
    QTimer.singleShot(6000, lambda: engine.set_animation("idle"))
    QTimer.singleShot(8000, app.quit)
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
