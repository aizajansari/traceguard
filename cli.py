#!/usr/bin/env python3
"""
TraceGuard CLI - Command Line Version for TailsOS
No GUI required - works on minimal systems
"""

import os
import sys
import subprocess
import json
import hashlib
from datetime import datetime

sys.path.insert(0, os.path.dirname(__file__))

from src.config.settings import config
from src.core.scanner import ForensicScanner
from src.core.cleaner import ForensicCleaner

def print_banner():
    print("=" * 60)
    print("  TRACEGUARD - FORENSIC METADATA TOOL (CLI Mode)")
    print("=" * 60)
    print()

def scan_file(filepath):
    print(f"\n[SCANNING] {filepath}")
    print("-" * 40)
    
    scanner = ForensicScanner()
    results = scanner.deep_scan(filepath)
    
    file_info = results.get('file_info', {})
    metadata = results.get('metadata', {})
    gps_data = results.get('gps_data', {})
    
    print(f"\nFile: {file_info.get('name', 'Unknown')}")
    print(f"Size: {file_info.get('size_human', 'Unknown')}")
    
    if gps_data:
        print(f"\n[GPS LOCATION]")
        if 'GPSLatitude' in gps_data:
            print(f"  Latitude: {gps_data['GPSLatitude']}")
        if 'GPSLongitude' in gps_data:
            print(f"  Longitude: {gps_data['GPSLongitude']}")
        if 'google_maps_url' in gps_data:
            print(f"  Map: {gps_data['google_maps_url']}")
    
    if metadata:
        print(f"\n[METADATA FOUND] - {len(metadata)} fields")
        for key, value in list(metadata.items())[:20]:
            if value and not key.startswith('File'):
                print(f"  {key}: {str(value)[:80]}")
    
    return results

def clean_file(filepath, output_path=None):
    print(f"\n[CLEANING] {filepath}")
    print("-" * 40)
    
    if not output_path:
        name = os.path.splitext(os.path.basename(filepath))[0]
        ext = os.path.splitext(filepath)[1]
        output_path = os.path.join(os.path.dirname(filepath), f"{name}_cleaned{ext}")
    
    cleaner = ForensicCleaner()
    result = cleaner.aggressive_clean(filepath, output_path)
    
    if result.get('success'):
        print(f"✅ Cleaning successful!")
        print(f"   Output: {output_path}")
        return True
    else:
        print(f"❌ Cleaning failed: {result.get('error', 'Unknown')}")
        return False

def batch_clean(source_dir, output_dir):
    import glob
    
    print(f"\n[BATCH CLEANING]")
    print(f"  Source: {source_dir}")
    print(f"  Output: {output_dir}")
    print("-" * 40)
    
    os.makedirs(output_dir, exist_ok=True)
    
    files = []
    for ext in ['*.jpg', '*.jpeg', '*.png']:
        files.extend(glob.glob(os.path.join(source_dir, "**", ext), recursive=True))
    
    files = list(set(files))
    
    if not files:
        print("No image files found!")
        return
    
    print(f"Found {len(files)} images\n")
    
    successful = 0
    for i, file in enumerate(files, 1):
        rel_path = os.path.relpath(file, source_dir)
        output_path = os.path.join(output_dir, rel_path)
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        output_path = os.path.splitext(output_path)[0] + ".jpg"
        
        print(f"[{i}/{len(files)}] {rel_path}")
        cleaner = ForensicCleaner()
        result = cleaner.aggressive_clean(file, output_path)
        
        if result.get('success'):
            successful += 1
            print(f"      ✅ Done")
        else:
            print(f"      ❌ Failed")
    
    print(f"\n✅ Complete: {successful}/{len(files)} successful")

def main():
    print_banner()
    
    while True:
        print("\n" + "=" * 40)
        print("  MENU")
        print("=" * 40)
        print("1. Scan a single file")
        print("2. Clean a single file")
        print("3. Batch clean folder")
        print("4. Exit")
        print("-" * 40)
        
        choice = input("Select option (1-4): ").strip()
        
        if choice == '1':
            filepath = input("Enter file path: ").strip()
            if os.path.exists(filepath):
                scan_file(filepath)
            else:
                print("File not found!")
        
        elif choice == '2':
            filepath = input("Enter file path: ").strip()
            if os.path.exists(filepath):
                clean_file(filepath)
            else:
                print("File not found!")
        
        elif choice == '3':
            source = input("Enter source folder: ").strip()
            output = input("Enter output folder: ").strip()
            if os.path.exists(source):
                batch_clean(source, output)
            else:
                print("Source folder not found!")
        
        elif choice == '4':
            print("Goodbye!")
            break
        
        else:
            print("Invalid choice!")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nGoodbye!")
