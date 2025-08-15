#!/usr/bin/env python3
"""
TuxTray Emotion System Test
===========================

This script demonstrates the new 5-state emotion system that responds to
CPU, RAM, and network usage in a comprehensive way.

The 5 emotion states are:
1. 😌 Calm - All resources low (penguin dancing calmly)
2. 🚶 Active - Normal system activity (penguin walking)  
3. 🏃 Busy - Single resource high (penguin running normal speed)
4. 😰 Stressed - Multiple resources high (penguin running frantically)
5. 🥵 Overloaded - System critically stressed (penguin exhausted)
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

def simulate_load(load_type, intensity, duration=10):
    """Simulate different types of system load."""
    threads = []
    
    if load_type == "cpu" and intensity > 0:
        def cpu_worker():
            end_time = time.time() + duration
            while time.time() < end_time:
                # CPU intensive calculation
                sum(i * i for i in range(int(intensity * 1000)))
                time.sleep(0.01)
        
        cpu_count = multiprocessing.cpu_count()
        num_threads = max(1, int(intensity / 100 * cpu_count * 2))
        
        for _ in range(num_threads):
            thread = threading.Thread(target=cpu_worker)
            thread.daemon = True
            thread.start()
            threads.append(thread)
    
    elif load_type == "ram" and intensity > 0:
        def ram_worker():
            # Allocate memory to simulate RAM usage
            try:
                # Allocate memory based on intensity
                memory_mb = int(intensity * 50)  # Scale intensity to MB
                data = bytearray(memory_mb * 1024 * 1024)
                time.sleep(duration)
                del data
            except MemoryError:
                print(f"Warning: Could not allocate {memory_mb}MB of RAM")
                time.sleep(duration)
        
        thread = threading.Thread(target=ram_worker)
        thread.daemon = True
        thread.start()
        threads.append(thread)
    
    return threads

def demonstrate_emotion_states():
    """Demonstrate each emotion state with simulated system loads."""
    config = ConfigManager()
    monitor = SystemMonitor()
    
    print("🐧 TuxTray Emotion System Demonstration")
    print("=" * 50)
    print()
    print("This demo shows how the penguin's emotions change based on")
    print("comprehensive system resource analysis (CPU + RAM + Network)")
    print()
    
    # Display emotion thresholds
    emotion_thresholds = config.get_emotion_thresholds()
    print("📊 Emotion State Definitions:")
    print("-" * 30)
    
    state_descriptions = {
        "calm": "😌 All resources low - penguin dancing peacefully",
        "active": "🚶 Normal activity - penguin walking around",  
        "busy": "🏃 Single resource busy - penguin running normally",
        "stressed": "😰 Multiple resources high - penguin running frantically",
        "overloaded": "🥵 System critical - penguin exhausted and collapsing"
    }
    
    for emotion, desc in state_descriptions.items():
        config_info = emotion_thresholds.get(emotion, {}).get('description', '')
        print(f"  {desc}")
        if config_info:
            print(f"    → {config_info}")
    
    print()
    print("🎬 Starting Emotion Demonstration...")
    print("=" * 50)
    
    # Test scenarios to trigger different emotions
    scenarios = [
        {
            "name": "😌 Baseline - Calm State",
            "description": "System at rest, all resources low",
            "cpu_load": 0,
            "ram_load": 0, 
            "duration": 8,
            "expected": "calm"
        },
        {
            "name": "🚶 Light Activity - Active State", 
            "description": "Moderate system activity",
            "cpu_load": 40,
            "ram_load": 0,
            "duration": 10,
            "expected": "active"
        },
        {
            "name": "🏃 CPU Intensive - Busy State",
            "description": "High CPU usage, single resource busy", 
            "cpu_load": 75,
            "ram_load": 0,
            "duration": 10,
            "expected": "busy"
        },
        {
            "name": "😰 Multi-Resource Load - Stressed State",
            "description": "High CPU and RAM usage simultaneously",
            "cpu_load": 80,
            "ram_load": 60,
            "duration": 12,
            "expected": "stressed"
        },
        {
            "name": "🥵 System Overload - Overloaded State", 
            "description": "Critical CPU usage, system at breaking point",
            "cpu_load": 95,
            "ram_load": 0,
            "duration": 8,
            "expected": "overloaded"
        },
        {
            "name": "😌 Cool Down - Return to Calm",
            "description": "System returning to normal after stress",
            "cpu_load": 0,
            "ram_load": 0,
            "duration": 8,
            "expected": "calm"
        }
    ]
    
    for i, scenario in enumerate(scenarios, 1):
        print(f"\nScenario {i}/6: {scenario['name']}")
        print(f"Description: {scenario['description']}")
        print(f"Load: CPU {scenario['cpu_load']}%, RAM {scenario['ram_load']}%")
        print(f"Expected emotion: {scenario['expected'].upper()}")
        print("─" * 50)
        
        # Start load simulation
        cpu_threads = simulate_load("cpu", scenario['cpu_load'], scenario['duration'])
        ram_threads = simulate_load("ram", scenario['ram_load'], scenario['duration'])
        all_threads = cpu_threads + ram_threads
        
        # Monitor system and emotion states
        start_time = time.time()
        samples = []
        
        while time.time() - start_time < scenario['duration']:
            stats = monitor.get_system_stats()
            analysis = monitor.get_emotion_analysis(stats, emotion_thresholds)
            samples.append(analysis)
            
            elapsed = int(time.time() - start_time)
            
            # Get emoji for current emotion
            emotion_emojis = {
                "calm": "😌", "active": "🚶", "busy": "🏃", 
                "stressed": "😰", "overloaded": "🥵"
            }
            emoji = emotion_emojis.get(analysis['emotion'], "🤔")
            
            # Show real-time status
            status = (f"[{elapsed:2d}s] CPU:{stats.cpu_percent:5.1f}% "
                     f"RAM:{stats.ram_percent:4.1f}% "
                     f"Net:{stats.network_kbps:6.1f}KB/s "
                     f"→ {emoji} {analysis['emotion'].upper()} "
                     f"({analysis['overall_stress']:.0f}% stress)")
            
            print(f"\r{status}", end="", flush=True)
            time.sleep(0.5)
        
        print()  # New line after progress
        
        # Wait for threads to complete
        for thread in all_threads:
            if thread.is_alive():
                thread.join()
        
        # Show scenario summary
        if samples:
            final_emotion = samples[-1]['emotion']
            avg_stress = sum(s['overall_stress'] for s in samples) / len(samples)
            
            success = "✅" if final_emotion == scenario['expected'] else "⚠️"
            print(f"{success} Final emotion: {final_emotion.upper()} (avg stress: {avg_stress:.1f}%)")
            
            if samples[-1]['active_stressors']:
                print(f"   Active stressors: {', '.join(samples[-1]['active_stressors'])}")
        
        time.sleep(2)  # Brief pause between scenarios
    
    print(f"\n{'=' * 50}")
    print("✅ Emotion System Demonstration Complete!")
    print()
    print("🎯 What you should observe in TuxTray:")
    print("   😌 Calm: Penguin dancing peacefully when system is idle")
    print("   🚶 Active: Penguin walking during normal system activity") 
    print("   🏃 Busy: Penguin running when one resource is heavily used")
    print("   😰 Stressed: Penguin running frantically under multi-resource load")
    print("   🥵 Overloaded: Penguin collapsing when system is critically stressed")
    print()
    print("💡 To see this in action with TuxTray:")
    print("   1. Run: python3 main.py")
    print("   2. In another terminal: python3 emotion_test.py")
    print("   3. Watch the penguin in your system tray change emotions!")

if __name__ == "__main__":
    try:
        demonstrate_emotion_states()
    except KeyboardInterrupt:
        print("\n\n⏹️ Demo interrupted by user")
    except Exception as e:
        print(f"\n❌ Error during demo: {e}")
        import traceback
        traceback.print_exc()
