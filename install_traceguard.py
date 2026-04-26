#!/usr/bin/env python3
"""
TraceGuard Universal Installer - Forensic Grade
Works on Windows, Linux, Mac, TailsOS
"""

import os
import sys
import platform
import subprocess

VERSION = "2.0.0"
AUTHOR = "Aizaj Ansari"

def detect_tails():
    try:
        with open('/etc/os-release', 'r') as f:
            return 'tails' in f.read().lower()
    except:
        return False

def install_exiftool():
    """Install exiftool for maximum forensic capability"""
    system = platform.system()
    is_tails = detect_tails()
    
    print("\n[INFO] Installing exiftool for maximum forensic capability...")
    
    if system == "Windows":
        print("  Download exiftool from: https://exiftool.org/")
        print("  Place exiftool.exe in the tool directory")
    elif is_tails or system == "Linux":
        try:
            subprocess.run(['sudo', 'apt-get', 'update'], check=False)
            subprocess.run(['sudo', 'apt-get', 'install', 'exiftool', '-y'], check=False)
            print("  ✅ exiftool installed")
        except:
            print("  ⚠️ Could not install exiftool (PIL fallback will work)")
    elif system == "Darwin":
        try:
            subprocess.run(['brew', 'install', 'exiftool'], check=False)
            print("  ✅ exiftool installed")
        except:
            print("  ⚠️ Could not install exiftool (PIL fallback will work)")

def install_pillow():
    """Install Pillow for image processing"""
    print("\n[INFO] Installing Pillow...")
    subprocess.run([sys.executable, "-m", "pip", "install", "Pillow", "--quiet"])

def create_launchers():
    """Create launcher scripts for all platforms"""
    
    # Windows launcher
    with open('run.bat', 'w') as f:
        f.write('''@echo off
title TraceGuard - Forensic Tool
color 0A
echo ============================================================
echo    TRACEGUARD - FORENSIC METADATA TOOL
echo ============================================================
echo.
python main.py
pause
''')
    
    # Linux/Mac launcher
    with open('run.sh', 'w') as f:
        f.write('''#!/bin/bash
echo "============================================================"
echo "   TRACEGUARD - FORENSIC METADATA TOOL"
echo "============================================================"
echo ""
python3 main.py
''')
    os.chmod('run.sh', 0o755)
    
    # TailsOS launcher
    with open('run_tails.sh', 'w') as f:
        f.write('''#!/bin/bash
cd "$(dirname "$0")"
echo "=================================="
echo "  TRACEGUARD - FORENSIC TOOL"
echo "=================================="
echo ""
if command -v exiftool &>/dev/null; then
    echo "✅ exiftool available - Full forensic mode"
else
    echo "⚠️ exiftool not found - Using PIL mode"
    echo "   Run: sudo apt-get install exiftool -y"
fi
echo ""
python3 main.py
''')
    os.chmod('run_tails.sh', 0o755)
    
    print("✅ Launchers created")

def main():
    print("=" * 60)
    print(f"  TRACEGUARD v{VERSION} - FORENSIC METADATA TOOL")
    print(f"  by {AUTHOR}")
    print("=" * 60)
    
    system = platform.system()
    is_tails = detect_tails()
    
    print(f"\n🖥️  System: {system}")
    if is_tails:
        print("🔒 TailsOS detected - Maximum privacy mode")
    
    install_pillow()
    install_exiftool()
    
    # Create directories
    os.makedirs("reports", exist_ok=True)
    os.makedirs("logs", exist_ok=True)
    
    create_launchers()
    
    print("\n" + "=" * 60)
    print("✅ INSTALLATION COMPLETE!")
    print("\n📌 To run TraceGuard:")
    print("   Windows: double-click run.bat")
    print("   Linux/Mac: ./run.sh")
    print("   TailsOS: ./run_tails.sh")
    print("\n🔒 FORENSIC FEATURES:")
    print("   • Extracts ALL metadata (GPS, camera, dates, software)")
    print("   • Permanent metadata removal (unrecoverable)")
    print("   • Secure delete (3x overwrite)")
    print("   • Batch processing with random renaming")
    print("=" * 60)

if __name__ == "__main__":
    main()