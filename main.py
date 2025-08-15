#!/usr/bin/env python3
"""
TuxTray - Main Entry Point
==========================

Run TuxTray system tray application.
"""

import sys
from pathlib import Path

# Add the src directory to Python path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from src.main import main

if __name__ == "__main__":
    main()
