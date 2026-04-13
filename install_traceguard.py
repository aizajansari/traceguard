"""
TraceGuard Universal Installer
Works on Windows, Linux, Mac, TailsOS
Run: python install_traceguard.py
"""

import os
import sys
import platform
import subprocess
from pathlib import Path

# ============================================================================
# CONFIGURATION
# ============================================================================

VERSION = "2.0.0"

# Simple colors that work on Windows
if platform.system() == "Windows":
    # No colors on Windows to avoid encoding issues
    RED = GREEN = YELLOW = BLUE = CYAN = RESET = ''
else:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    RESET = '\033[0m'

def print_header(text):
    print(f"\n{CYAN}{'='*60}{RESET}")
    print(f"{CYAN}{text.center(60)}{RESET}")
    print(f"{CYAN}{'='*60}{RESET}\n")

def print_success(text):
    print(f"{GREEN}[SUCCESS] {text}{RESET}")

def print_error(text):
    print(f"{RED}[ERROR] {text}{RESET}")

def print_info(text):
    print(f"{BLUE}[INFO] {text}{RESET}")

def print_warning(text):
    print(f"{YELLOW}[WARNING] {text}{RESET}")

def get_system():
    system = platform.system()
    if system == "Windows":
        return "windows"
    elif system == "Linux":
        return "linux"
    elif system == "Darwin":
        return "mac"
    return "unknown"

# ============================================================================
# INSTALLATION FUNCTIONS
# ============================================================================

def check_python():
    print_info("Checking Python installation...")
    version = sys.version_info
    if version.major >= 3 and version.minor >= 8:
        print_success(f"Python {version.major}.{version.minor}.{version.micro} found")
        return True
    print_error(f"Python {version.major}.{version.minor} detected. Python 3.8+ required")
    return False

def install_pillow():
    print_info("Installing Pillow (image processing library)...")
    try:
        result = subprocess.run([sys.executable, "-m", "pip", "install", "Pillow"], 
                               capture_output=True, text=True)
        if result.returncode == 0:
            print_success("Pillow installed successfully")
            return True
        else:
            print_warning(f"Could not install Pillow: {result.stderr[:200]}")
            return False
    except Exception as e:
        print_warning(f"Could not install Pillow: {e}")
        return False

def check_exiftool():
    print_info("Checking for exiftool...")
    
    exiftool_paths = ["exiftool", "/usr/bin/exiftool", "/usr/local/bin/exiftool",
                      "C:\\exiftool\\exiftool.exe", "C:\\Program Files\\exiftool\\exiftool.exe"]
    
    for path in exiftool_paths:
        try:
            result = subprocess.run([path, "-ver"], capture_output=True, text=True)
            if result.returncode == 0:
                print_success(f"exiftool found (version {result.stdout.strip()})")
                return True
        except:
            pass
    
    print_warning("exiftool not found - Some features limited")
    system = get_system()
    if system == "windows":
        print_info("Download from: https://exiftool.org/exiftool-13.55_64.zip")
        print_info("Extract exiftool.exe and place in the tool directory")
    elif system == "linux":
        print_info("Run: sudo apt-get install exiftool -y")
    elif system == "mac":
        print_info("Run: brew install exiftool")
    return False

def create_launcher_scripts():
    """Create launcher scripts in the current directory"""
    print_info("Creating launcher scripts...")
    
    # Windows batch file - using simple ASCII
    bat_content = '''@echo off
title TraceGuard - Forensic Metadata Tool
color 0A
echo ============================================================
echo    TRACEGUARD - FORENSIC METADATA TOOL
echo ============================================================
echo.
echo Starting TraceGuard...
echo.
python main.py
if errorlevel 1 (
    echo.
    echo [ERROR] Failed to start. Please check dependencies.
    echo Run: pip install Pillow
    echo.
    pause
)
'''
    with open("run.bat", "w", encoding='utf-8') as f:
        f.write(bat_content)
    
    # Linux/Mac shell script
    sh_content = '''#!/bin/bash
echo "============================================================"
echo "   TRACEGUARD - FORENSIC METADATA TOOL"
echo "============================================================"
echo ""
echo "Starting TraceGuard..."
echo ""
if command -v python3 &>/dev/null; then
    python3 main.py
elif command -v python &>/dev/null; then
    python main.py
else
    echo "[ERROR] Python not found"
    exit 1
fi
echo ""
echo "TraceGuard closed."
'''
    with open("run.sh", "w", encoding='utf-8') as f:
        f.write(sh_content)
    
    # Make shell script executable on Unix systems
    if get_system() != "windows":
        os.chmod("run.sh", 0o755)
    
    print_success("Launcher scripts created (run.bat for Windows, run.sh for Linux/Mac)")

def verify_files():
    """Verify all required files exist"""
    required_files = ["main.py", "src/gui/main_window.py", "src/core/scanner.py", 
                      "src/core/cleaner.py", "src/core/reporter.py", "src/config/settings.py"]
    
    missing = []
    for file in required_files:
        if not os.path.exists(file):
            missing.append(file)
    
    if missing:
        print_warning("Some files are missing:")
        for f in missing:
            print(f"   - {f}")
        return False
    
    print_success("All required files found")
    return True

def create_directories():
    """Create required directories"""
    print_info("Creating directories...")
    dirs = ['reports', 'logs']
    for d in dirs:
        Path(d).mkdir(parents=True, exist_ok=True)
    print_success("Directories created (reports/, logs/)")

def print_usage_instructions():
    """Print usage instructions"""
    print_header("INSTALLATION COMPLETE")
    
    system = get_system()
    
    print(f"\n{GREEN}TraceGuard is ready to use!{RESET}\n")
    
    print("=" * 60)
    print("  HOW TO RUN TRACEGUARD")
    print("=" * 60)
    
    if system == "windows":
        print(f"""
  Method 1 (Easiest):
    Double-click: run.bat

  Method 2 (Command Line):
    Open Command Prompt in this folder
    Type: python main.py
""")
    else:
        print(f"""
  Method 1 (Easiest):
    ./run.sh

  Method 2 (Terminal):
    cd {os.getcwd()}
    python3 main.py
""")
    
    # TailsOS specific
    if "amnesia" in os.getcwd() or system == "linux":
        print("\n" + "=" * 60)
        print("  TAILSOS USERS")
        print("=" * 60)
        print(f"""
  Important for TailsOS:
    
    1. Make sure you're in Persistent storage
    2. Current location: {os.getcwd()}
    3. Run: ./run.sh
    4. Save outputs to: /home/amnesia/Persistent/
""")
    
    print("\n" + "=" * 60)
    print("  NEXT STEPS")
    print("=" * 60)
    print(f"""
  1. Install exiftool (recommended):
     Download from: https://exiftool.org/

  2. Run TraceGuard:
     Use the instructions above

  3. Start analyzing:
     Load an image file
     Click "START FORENSIC SCAN"
""")
    
    print(f"\n{GREEN}Thank you for installing TraceGuard!{RESET}\n")

# ============================================================================
# MAIN
# ============================================================================

def main():
    """Main installation function"""
    print_header("TRACEGUARD UNIVERSAL INSTALLER")
    
    system = get_system()
    print_info(f"Detected system: {system.upper()}")
    print_info(f"Python version: {platform.python_version()}")
    print_info(f"Installation directory: {os.getcwd()}")
    
    # Check Python
    if not check_python():
        print_error("Installation failed. Python 3.8+ required.")
        input("\nPress Enter to exit...")
        return False
    
    # Install Pillow
    install_pillow()
    
    # Check exiftool
    check_exiftool()
    
    # Create directories
    create_directories()
    
    # Create launcher scripts
    create_launcher_scripts()
    
    # Verify files
    verify_files()
    
    # Print instructions
    print_usage_instructions()
    
    # Ask to run now
    print_info("Do you want to run TraceGuard now?")
    response = input("Run TraceGuard? (y/n): ").lower()
    
    if response == 'y' or response == 'yes':
        print_info("Starting TraceGuard...\n")
        if system == "windows":
            os.system("python main.py")
        else:
            os.system("python3 main.py")
    
    return True

if __name__ == "__main__":
    try:
        main()
        input("\nPress Enter to exit...")
    except KeyboardInterrupt:
        print("\n\nInstallation cancelled.")
    except Exception as e:
        print_error(f"Unexpected error: {e}")
        input("\nPress Enter to exit...")