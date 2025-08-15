"""
System Monitor for TuxTray
Monitors system resources (CPU, RAM, Network) using psutil.
"""

import psutil
import time
from typing import Dict, Tuple, Optional
from dataclasses import dataclass


@dataclass
class SystemStats:
    """Container for system statistics."""
    cpu_percent: float
    ram_percent: float
    network_kbps: float
    timestamp: float


class SystemMonitor:
    """Monitors system resources for TuxTray animation control."""
    
    def __init__(self):
        """Initialize the system monitor."""
        self._last_network_io: Optional[Tuple[int, int]] = None
        self._last_network_time: Optional[float] = None
        self._cpu_percent_cache = 0.0
        
        # Initialize network baseline
        self._init_network_baseline()
    
    def _init_network_baseline(self) -> None:
        """Initialize network monitoring baseline."""
        try:
            net_io = psutil.net_io_counters()
            if net_io:
                self._last_network_io = (net_io.bytes_sent, net_io.bytes_recv)
                self._last_network_time = time.time()
        except (AttributeError, OSError):
            # Network monitoring not available
            self._last_network_io = None
            self._last_network_time = None
    
    def get_cpu_usage(self) -> float:
        """
        Get current CPU usage as percentage.
        Uses cached value to avoid blocking calls.
        """
        try:
            # Use non-blocking call with cached value
            cpu_percent = psutil.cpu_percent(interval=None)
            if cpu_percent > 0:
                self._cpu_percent_cache = cpu_percent
            return self._cpu_percent_cache
        except Exception as e:
            print(f"Error getting CPU usage: {e}")
            return self._cpu_percent_cache
    
    def get_ram_usage(self) -> float:
        """Get current RAM usage as percentage."""
        try:
            memory = psutil.virtual_memory()
            return memory.percent
        except Exception as e:
            print(f"Error getting RAM usage: {e}")
            return 0.0
    
    def get_network_usage(self) -> float:
        """
        Get current network usage in KB/s.
        Returns combined upload + download speed.
        """
        try:
            net_io = psutil.net_io_counters()
            current_time = time.time()
            
            if (net_io is None or 
                self._last_network_io is None or 
                self._last_network_time is None):
                return 0.0
            
            # Calculate bytes transferred since last check
            bytes_sent = net_io.bytes_sent - self._last_network_io[0]
            bytes_recv = net_io.bytes_recv - self._last_network_io[1]
            total_bytes = bytes_sent + bytes_recv
            
            # Calculate time elapsed
            time_elapsed = current_time - self._last_network_time
            
            # Update baseline for next calculation
            self._last_network_io = (net_io.bytes_sent, net_io.bytes_recv)
            self._last_network_time = current_time
            
            # Convert to KB/s
            if time_elapsed > 0:
                kbps = (total_bytes / 1024) / time_elapsed
                return max(0, kbps)  # Ensure non-negative
            
            return 0.0
            
        except Exception as e:
            print(f"Error getting network usage: {e}")
            return 0.0
    
    def get_system_stats(self) -> SystemStats:
        """Get all system statistics at once."""
        return SystemStats(
            cpu_percent=self.get_cpu_usage(),
            ram_percent=self.get_ram_usage(),
            network_kbps=self.get_network_usage(),
            timestamp=time.time()
        )
    
    def determine_animation_state(self, stats: SystemStats, mode: str, 
                                thresholds: Dict[str, int]) -> str:
        """
        Determine which animation to play based on system stats and mode.
        
        Args:
            stats: Current system statistics
            mode: Monitoring mode ('cpu', 'ram', 'network', 'emotion')
            thresholds: Threshold values for the mode
            
        Returns:
            Animation state: 'idle', 'walk', 'run' (legacy) or emotion state
        """
        if mode == "emotion":
            return self.determine_emotion_state(stats, thresholds)
        
        # Legacy mode support
        if mode == "cpu":
            usage = stats.cpu_percent
            idle_threshold = thresholds.get("idle", 30)
            walk_threshold = thresholds.get("walk", 80)
        
        elif mode == "ram":
            usage = stats.ram_percent
            idle_threshold = thresholds.get("idle", 40)
            walk_threshold = thresholds.get("walk", 85)
        
        elif mode == "network":
            usage = stats.network_kbps
            idle_threshold = thresholds.get("idle_kbps", 100)
            walk_threshold = thresholds.get("walk_kbps", 1000)
        
        else:
            return "idle"
        
        # Determine animation state based on usage
        if usage >= walk_threshold:
            return "run"
        elif usage >= idle_threshold:
            return "walk"
        else:
            return "idle"
    
    def determine_emotion_state(self, stats: SystemStats, 
                              emotion_thresholds: Dict[str, Dict]) -> str:
        """
        Determine penguin emotion based on comprehensive system analysis.
        
        Args:
            stats: Current system statistics
            emotion_thresholds: Emotion-based threshold configuration
            
        Returns:
            Emotion state: 'calm', 'active', 'busy', 'stressed', or 'overloaded'
        """
        cpu = stats.cpu_percent
        ram = stats.ram_percent
        network = stats.network_kbps
        
        # Check for overloaded state first (highest priority)
        overload_config = emotion_thresholds.get('overloaded', {})
        any_critical_threshold = overload_config.get('any_critical_threshold', 85)
        
        if (cpu >= overload_config.get('cpu_critical', 90) or
            ram >= overload_config.get('ram_critical', 90) or
            network >= overload_config.get('network_critical_kbps', 2000) or
            cpu >= any_critical_threshold or
            ram >= any_critical_threshold):
            return "overloaded"
        
        # Check for stressed state (multiple resources high)
        stressed_config = emotion_thresholds.get('stressed', {})
        high_resources = 0
        if cpu >= stressed_config.get('cpu_high', 70):
            high_resources += 1
        if ram >= stressed_config.get('ram_high', 75):
            high_resources += 1
        if network >= stressed_config.get('network_high_kbps', 800):
            high_resources += 1
            
        if high_resources >= 2:
            return "stressed"
        
        # Check for busy state (single resource high)
        busy_config = emotion_thresholds.get('busy', {})
        single_threshold = busy_config.get('single_resource_threshold', 60)
        if cpu >= single_threshold or ram >= single_threshold or network >= single_threshold*10:  # network scaled
            return "busy"
        
        # Check for calm state (all resources low)
        calm_config = emotion_thresholds.get('calm', {})
        if (cpu <= calm_config.get('cpu_max', 20) and
            ram <= calm_config.get('ram_max', 30) and
            network <= calm_config.get('network_max_kbps', 50)):
            return "calm"
        
        # Default to active state (normal activity)
        return "active"
    
    def get_emotion_analysis(self, stats: SystemStats, 
                           emotion_thresholds: Dict[str, Dict]) -> Dict[str, any]:
        """
        Get detailed emotion analysis for debugging and user information.
        
        Args:
            stats: Current system statistics
            emotion_thresholds: Emotion-based threshold configuration
            
        Returns:
            Dictionary with emotion state and analysis details
        """
        emotion = self.determine_emotion_state(stats, emotion_thresholds)
        
        # Calculate resource stress levels (0-100)
        cpu_stress = min(100, stats.cpu_percent)
        ram_stress = min(100, stats.ram_percent)
        network_stress = min(100, stats.network_kbps / 20)  # Scale network to 0-100
        
        overall_stress = (cpu_stress + ram_stress + network_stress) / 3
        
        return {
            "emotion": emotion,
            "overall_stress": round(overall_stress, 1),
            "resource_levels": {
                "cpu": round(cpu_stress, 1),
                "ram": round(ram_stress, 1),
                "network": round(network_stress, 1)
            },
            "active_stressors": self._identify_active_stressors(stats),
            "description": emotion_thresholds.get(emotion, {}).get('description', f'System in {emotion} state')
        }
    
    def _identify_active_stressors(self, stats: SystemStats) -> list:
        """Identify which resources are causing system stress."""
        stressors = []
        
        if stats.cpu_percent > 70:
            stressors.append(f"High CPU ({stats.cpu_percent:.1f}%)")
        if stats.ram_percent > 75:
            stressors.append(f"High RAM ({stats.ram_percent:.1f}%)")
        if stats.network_kbps > 800:
            stressors.append(f"High Network ({stats.network_kbps:.1f} KB/s)")
            
        return stressors
    
    def get_system_info(self) -> Dict[str, str]:
        """Get basic system information for debugging."""
        try:
            return {
                "platform": psutil.WINDOWS and "Windows" or (
                    psutil.MACOS and "macOS" or "Linux"
                ),
                "cpu_count": str(psutil.cpu_count()),
                "memory_total": f"{psutil.virtual_memory().total / (1024**3):.1f} GB",
                "python_version": f"{psutil.version_info}",
            }
        except Exception as e:
            return {"error": str(e)}


# Utility function for testing
def main():
    """Test the system monitor functionality."""
    monitor = SystemMonitor()
    
    print("TuxTray System Monitor Test")
    print("=" * 30)
    print(f"System Info: {monitor.get_system_info()}")
    print()
    
    try:
        for i in range(5):
            stats = monitor.get_system_stats()
            print(f"Sample {i+1}:")
            print(f"  CPU: {stats.cpu_percent:.1f}%")
            print(f"  RAM: {stats.ram_percent:.1f}%")
            print(f"  Network: {stats.network_kbps:.1f} KB/s")
            
            # Test animation state determination
            cpu_state = monitor.determine_animation_state(
                stats, "cpu", {"idle": 30, "walk": 80}
            )
            print(f"  Animation state (CPU mode): {cpu_state}")
            print()
            
            time.sleep(1)
            
    except KeyboardInterrupt:
        print("Test interrupted by user")


if __name__ == "__main__":
    main()
