#!/usr/bin/env python3
"""
Final TuxTray Animation Test
Demonstrates all animation features working together.
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

def simulate_cpu_load(target_percent, duration=5):
    """Simulate specific CPU load percentage."""
    def worker():
        end_time = time.time() + duration
        while time.time() < end_time:
            # Adjust work intensity based on target percentage
            work_intensity = int(target_percent * 1000)
            sum(i * i for i in range(work_intensity))
            time.sleep(0.01)  # Small sleep to allow CPU measurement
    
    # Calculate number of threads needed
    cpu_count = multiprocessing.cpu_count()
    num_threads = max(1, int(target_percent / 100 * cpu_count * 2))
    
    threads = []
    for _ in range(num_threads):
        thread = threading.Thread(target=worker)
        thread.daemon = True
        thread.start()
        threads.append(thread)
    
    return threads

def main():
    """Demonstrate TuxTray animation states."""
    print("🐧 TuxTray Final Animation Test")
    print("=" * 50)
    print("This test will simulate different CPU loads to demonstrate")
    print("how TuxTray penguin should animate in response.")
    print()
    
    config = ConfigManager()
    monitor = SystemMonitor()
    
    # Show current thresholds
    thresholds = config.get_thresholds("cpu")
    print(f"Animation Thresholds (CPU mode):")
    print(f"  🟢 Idle: < {thresholds['idle']}%")
    print(f"  🟡 Walk: {thresholds['idle']}% - {thresholds['walk']}%")
    print(f"  🔴 Run:  > {thresholds['walk']}%")
    print()
    
    # Test scenarios
    scenarios = [
        ("🟢 Idle State", 10, 5, "Penguin should be calmly sitting"),
        ("🟡 Walk State", 50, 8, "Penguin should be waddle-walking"),
        ("🔴 Run State", 90, 8, "Penguin should be running frantically"),
        ("🟢 Cool Down", 5, 5, "Penguin should return to idle")
    ]
    
    print("🎬 Starting Animation Demonstration...")
    print("=" * 50)
    
    for i, (name, target_cpu, duration, description) in enumerate(scenarios, 1):
        print(f"\nScenario {i}: {name}")
        print(f"Target CPU: {target_cpu}% for {duration} seconds")
        print(f"Expected: {description}")
        print(f"{'─' * 40}")
        
        # Start CPU simulation
        if target_cpu > 20:
            threads = simulate_cpu_load(target_cpu, duration)
        else:
            threads = []
        
        # Monitor for the duration
        start_time = time.time()
        while time.time() - start_time < duration:
            stats = monitor.get_system_stats()
            state = monitor.determine_animation_state(stats, "cpu", thresholds)
            
            # Get emoji for state
            emoji = "🟢" if state == "idle" else "🟡" if state == "walk" else "🔴"
            
            elapsed = int(time.time() - start_time)
            print(f"[{elapsed:2d}s] CPU: {stats.cpu_percent:5.1f}% → {emoji} {state.upper()}", end="\r")
            
            time.sleep(0.5)
        
        # Wait for threads to finish
        for thread in threads:
            if thread.is_alive():
                thread.join()
        
        print()  # New line after progress
        time.sleep(1)  # Brief pause between scenarios
    
    print(f"\n{'=' * 50}")
    print("✅ Animation test complete!")
    print()
    print("🎯 What you should have seen:")
    print("   1. 🟢 Penguin idle/sitting (low CPU)")
    print("   2. 🟡 Penguin walking/waddling (medium CPU)")
    print("   3. 🔴 Penguin running frantically (high CPU)")
    print("   4. 🟢 Penguin returning to calm idle state")
    print()
    print("💡 To see this in action:")
    print("   1. Run: source venv/bin/activate && python3 main.py")
    print("   2. In another terminal, run: python3 final_test.py")
    print("   3. Watch your system tray penguin change animations!")

if __name__ == "__main__":
    main()
