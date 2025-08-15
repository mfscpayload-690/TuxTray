#!/usr/bin/env python3
"""
CPU Stress Test for TuxTray Animation
Generate CPU load to test animation state changes.
"""

import sys
import time
import threading
import multiprocessing
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from src.system_monitor import SystemMonitor
from src.config_manager import ConfigManager

def cpu_stress(duration=10):
    """Generate CPU stress for testing."""
    print(f"🔥 Starting CPU stress test for {duration} seconds...")
    
    def stress_worker():
        """CPU intensive task."""
        end_time = time.time() + duration
        while time.time() < end_time:
            # CPU intensive calculation
            sum(i * i for i in range(10000))
    
    # Start multiple threads to stress CPU
    threads = []
    cpu_count = multiprocessing.cpu_count()
    
    for i in range(cpu_count):
        thread = threading.Thread(target=stress_worker)
        thread.daemon = True
        thread.start()
        threads.append(thread)
    
    return threads

def monitor_animation_states():
    """Monitor system stats and expected animation states."""
    config = ConfigManager()
    monitor = SystemMonitor()
    
    print("📊 Monitoring animation states...")
    print("Legend: 🟢 idle (<30%) | 🟡 walk (30-80%) | 🔴 run (>80%)")
    print()
    
    for i in range(20):  # Monitor for 20 seconds
        stats = monitor.get_system_stats()
        thresholds = config.get_thresholds("cpu")
        state = monitor.determine_animation_state(stats, "cpu", thresholds)
        
        # Determine emoji based on state
        emoji = "🟢" if state == "idle" else "🟡" if state == "walk" else "🔴"
        
        print(f"[{i+1:2d}s] CPU: {stats.cpu_percent:5.1f}% | State: {emoji} {state:<4} | RAM: {stats.ram_percent:4.1f}% | Net: {stats.network_kbps:6.1f} KB/s")
        
        time.sleep(1)

def main():
    """Run stress test and monitor animation states."""
    print("🐧 TuxTray Animation Stress Test")
    print("=" * 50)
    
    print("Phase 1: Baseline monitoring (5 seconds)")
    print("Should show: 🟢 idle state")
    
    monitor_thread = threading.Thread(target=monitor_animation_states)
    monitor_thread.daemon = True
    monitor_thread.start()
    
    # Wait 5 seconds for baseline
    time.sleep(5)
    
    print("\nPhase 2: CPU stress test (10 seconds)")
    print("Should show: 🟡 walk → 🔴 run states")
    
    # Start CPU stress
    stress_threads = cpu_stress(10)
    
    # Wait for stress test to complete
    for thread in stress_threads:
        thread.join()
    
    print("\nPhase 3: Cool down (5 seconds)")
    print("Should show: 🔴 run → 🟡 walk → 🟢 idle states")
    
    # Wait 5 more seconds for cool down
    time.sleep(5)
    
    print("\n✅ Stress test complete!")
    print("If TuxTray is running, you should have seen the penguin change animations!")

if __name__ == "__main__":
    main()
