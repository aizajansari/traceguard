#!/usr/bin/env python3
"""
TraceGuard - Forensic Metadata Tool
Cross-platform entry point for Windows, Linux, Mac, TailsOS
"""

import sys
import os
import platform

# Add src to path
sys.path.insert(0, os.path.dirname(__file__))

def check_environment():
    """Check if environment is ready"""
    system = platform.system()
    print(f"🛡️ TraceGuard Forensic Tool")
    print(f"📡 System: {system} {platform.release()}")
    print(f"🐍 Python: {platform.python_version()}")
    print("-" * 40)
    
    # Check for exiftool
    exiftool_paths = [
        r"C:\Users\techone\Downloads\exiftool-13.55_64\exiftool-13.55_64\exiftool.exe",  # Windows
        "/usr/bin/exiftool",  # Linux
        "/usr/local/bin/exiftool",  # Mac
        "/home/amnesia/Persistent/exiftool",  # TailsOS
        "exiftool"  # Anywhere in PATH
    ]
    
    exiftool_found = False
    for path in exiftool_paths:
        if os.path.exists(path):
            print(f"✅ exiftool found: {path}")
            exiftool_found = True
            break
    
    if not exiftool_found:
        print("⚠️ exiftool not found - Some features limited")
        print("   Install from: https://exiftool.org/")
    
    return True

def main():
    """Main entry point"""
    try:
        from src.gui.main_window import MainWindow
        app = MainWindow()
        app.run()
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("\nPlease ensure you have installed dependencies:")
        print("  pip install Pillow")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    check_environment()
    main()
