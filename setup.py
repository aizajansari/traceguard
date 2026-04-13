#!/usr/bin/env python3
"""
TraceGuard - Cross-Platform Installation Script
Works on Windows, Linux, Mac, TailsOS
"""

import os
import sys
import platform
import subprocess
import urllib.request
import zipfile
import tarfile

def get_system():
    """Detect operating system"""
    system = platform.system()
    if system == "Windows":
        return "windows"
    elif system == "Linux":
        return "linux"
    elif system == "Darwin":
        return "mac"
    else:
        return "unknown"

def install_python_dependencies():
    """Install Python packages"""
    print("\n📦 Installing Python dependencies...")
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "Pillow"], check=True)
        print("✅ Pillow installed successfully!")
        return True
    except Exception as e:
        print(f"⚠️ Could not install Pillow: {e}")
        print("   Please run manually: pip install Pillow")
        return False

def check_exiftool():
    """Check if exiftool is available"""
    print("\n🔧 Checking exiftool...")
    
    # Common paths to check
    exiftool_paths = [
        "exiftool",
        "/usr/bin/exiftool",
        "/usr/local/bin/exiftool",
        "/home/amnesia/Persistent/exiftool",
        "C:\\exiftool\\exiftool.exe",
        "C:\\Program Files\\exiftool\\exiftool.exe"
    ]
    
    for path in exiftool_paths:
        try:
            result = subprocess.run([path, "-ver"], capture_output=True, text=True)
            if result.returncode == 0:
                print(f"✅ exiftool found: {path} (version {result.stdout.strip()})")
                return True
        except:
            pass
    
    print("⚠️ exiftool not found")
    print("\n📥 To install exiftool:")
    
    system = get_system()
    if system == "windows":
        print("   1. Download from: https://exiftool.org/exiftool-13.55_64.zip")
        print("   2. Extract and place exiftool.exe in the tool directory")
    elif system == "linux":
        print("   Run: sudo apt-get install exiftool -y")
    elif system == "mac":
        print("   Run: brew install exiftool")
    else:
        print("   Download from: https://exiftool.org/")
    
    return False

def create_directories():
    """Create required directories"""
    print("\n📁 Creating directories...")
    dirs = ['reports', 'logs']
    for d in dirs:
        os.makedirs(d, exist_ok=True)
        print(f"   ✅ {d}/")
    return True

def main():
    print("=" * 60)
    print("🛡️  TRACEGUARD - CROSS-PLATFORM INSTALLATION")
    print("=" * 60)
    
    system = get_system()
    print(f"\n💻 Detected System: {system.upper()}")
    print(f"🐍 Python: {platform.python_version()}")
    
    # Create directories
    create_directories()
    
    # Install dependencies
    install_python_dependencies()
    
    # Check exiftool
    check_exiftool()
    
    print("\n" + "=" * 60)
    print("✅ INSTALLATION COMPLETE!")
    print("\n📌 Next steps:")
    print("   • Run: python main.py")
    print("   • Or use the launcher script for your OS")
    print("=" * 60)

if __name__ == "__main__":
    main()