#!/usr/bin/env python3
"""
TraceGuard - Forensic Metadata Tool
Auto-detects GUI availability, falls back to CLI on TailsOS
"""

import sys
import os

def check_gui():
    """Check if GUI (tkinter) is available"""
    try:
        import tkinter
        return True
    except ImportError:
        return False

def run_cli():
    """Run CLI version when GUI not available"""
    cli_path = os.path.join(os.path.dirname(__file__), 'cli.py')
    if os.path.exists(cli_path):
        with open(cli_path, 'r') as f:
            code = f.read()
        exec(code)
    else:
        print("CLI mode not found. Please ensure cli.py exists.")
        print("Run: python3 cli.py")

def main():
    # Add src to path
    sys.path.insert(0, os.path.dirname(__file__))
    
    print("=" * 50)
    print("  TRACEGUARD - FORENSIC METADATA TOOL")
    print("=" * 50)
    
    if check_gui():
        print("GUI mode available. Loading...")
        try:
            from src.gui.main_window import MainWindow
            app = MainWindow()
            app.run()
        except Exception as e:
            print(f"GUI Error: {e}")
            print("Falling back to CLI mode...")
            run_cli()
    else:
        print("GUI not available (tkinter missing)")
        print("Using CLI mode...\n")
        run_cli()

if __name__ == "__main__":
    main()