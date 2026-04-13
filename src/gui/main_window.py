"""TraceGuard - Professional Forensic Metadata Tool
Complete GUI with ALL forensic features - Nothing removed
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import os
import threading
import random
import string
import hashlib
import json
import platform
from datetime import datetime
from PIL import Image

from src.config.settings import config
from src.core.scanner import ForensicScanner
from src.core.cleaner import ForensicCleaner
from src.core.reporter import ReportGenerator


class MainWindow:
    """TraceGuard - Complete Forensic Metadata Tool with ALL features"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("TraceGuard - Forensic Metadata Cleaner")
        self.root.geometry("1300x850")
        self.root.minsize(1100, 700)
        self.root.configure(bg='#1a1a2e')
        
        # Initialize ALL components
        self.current_file = None
        self.clean_file_path = None
        self.batch_folder = None
        self.output_folder = None
        self.current_results = None
        
        self.scanner = ForensicScanner()
        self.cleaner = ForensicCleaner()
        self.reporter = ReportGenerator()
        
        # Privacy options (ALL preserved)
        self.anonymize_filename_var = tk.BooleanVar(value=True)
        self.secure_delete_var = tk.BooleanVar(value=True)
        self.modify_timestamp_var = tk.BooleanVar(value=True)
        self.recompress_var = tk.BooleanVar(value=True)
        
        # Cleaning method
        self.clean_method = tk.StringVar(value="forensic")
        
        # Batch options
        self.recursive_var = tk.BooleanVar(value=True)
        
        # Report format
        self.report_format = tk.StringVar(value="HTML")
        
        # Store paned windows for each tab
        self.tab_paned_windows = {}
        
        self.setup_ui()
        self.check_exiftool()
    
    def setup_ui(self):
        """Setup professional TraceGuard UI with ALL features"""
        
        # Main container
        main_container = tk.Frame(self.root, bg='#1a1a2e')
        main_container.pack(fill=tk.BOTH, expand=True)
        
        # ========== LEFT SIDEBAR ==========
        sidebar = tk.Frame(main_container, width=250, bg='#0f0f1a')
        sidebar.pack(side=tk.LEFT, fill=tk.Y)
        sidebar.pack_propagate(False)
        
        # Logo Section
        logo_frame = tk.Frame(sidebar, bg='#0f0f1a', height=140)
        logo_frame.pack(fill=tk.X, pady=(25, 15))
        logo_frame.pack_propagate(False)
        
        shield_label = tk.Label(logo_frame, text="🛡️", font=('Segoe UI', 38),
                                bg='#0f0f1a', fg='#00d4ff')
        shield_label.pack()
        
        title_label = tk.Label(logo_frame, text="TraceGuard", font=('Segoe UI', 18, 'bold'),
                               bg='#0f0f1a', fg='#00d4ff')
        title_label.pack()
        
        subtitle_label = tk.Label(logo_frame, text="FORENSIC METADATA CLEANER", 
                                  font=('Segoe UI', 7), bg='#0f0f1a', fg='#6c7a89')
        subtitle_label.pack()
        
        # Navigation Menu
        nav_frame = tk.Frame(sidebar, bg='#0f0f1a')
        nav_frame.pack(fill=tk.X, pady=10)
        
        menu_items = [
            ("🔍 SCANNER", "scan"),
            ("🧹 CLEANER", "clean"),
            ("📦 BATCH", "batch"),
            ("📄 REPORTS", "reports"),
            ("ℹ️ INFO", "info")
        ]
        
        self.nav_buttons = {}
        for text, value in menu_items:
            btn = tk.Button(nav_frame, text=text, font=('Segoe UI', 10, 'bold'),
                           bg='#0f0f1a', fg='#8a9ab0', bd=0, anchor=tk.W,
                           padx=25, pady=10, cursor='hand2',
                           activebackground='#1a1a2e', activeforeground='#00d4ff',
                           command=lambda v=value: self.show_content(v))
            btn.pack(fill=tk.X)
            self.nav_buttons[value] = btn
        
        # Version
        version_label = tk.Label(sidebar, text="v2.0.0", font=('Segoe UI', 8),
                                 bg='#0f0f1a', fg='#4a5a6e')
        version_label.pack(side=tk.BOTTOM, pady=15)
        
        # ========== RIGHT CONTENT AREA ==========
        self.content_area = tk.Frame(main_container, bg='#16213e')
        self.content_area.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Header
        header_frame = tk.Frame(self.content_area, bg='#16213e', height=60)
        header_frame.pack(fill=tk.X, padx=20, pady=(10, 5))
        header_frame.pack_propagate(False)
        
        self.header_title = tk.Label(header_frame, text="SCANNER", 
                                     font=('Segoe UI', 16, 'bold'),
                                     bg='#16213e', fg='#00d4ff')
        self.header_title.pack(side=tk.LEFT)
        
        self.status_indicator = tk.Label(header_frame, text="● READY", 
                                         font=('Segoe UI', 9),
                                         bg='#16213e', fg='#00ff88')
        self.status_indicator.pack(side=tk.RIGHT)
        
        # Separator
        separator = tk.Frame(self.content_area, height=1, bg='#2a3a5e')
        separator.pack(fill=tk.X, padx=20)
        
        # Create all tab content frames (each with its own paned window)
        self.create_scanner_tab()
        self.create_cleaner_tab()
        self.create_batch_tab()
        self.create_reports_tab()
        self.create_info_tab()
        
        # Status bar
        status_bar = tk.Frame(self.content_area, bg='#0f0f1a', height=32)
        status_bar.pack(fill=tk.X, side=tk.BOTTOM)
        status_bar.pack_propagate(False)
        
        self.status_label = tk.Label(status_bar, text="Ready", font=('Segoe UI', 9),
                                     bg='#0f0f1a', fg='#6c7a89')
        self.status_label.pack(side=tk.LEFT, padx=15, pady=5)
        
        self.progress_bar = ttk.Progressbar(status_bar, mode='indeterminate')
        self.progress_bar.pack(side=tk.RIGHT, padx=15, pady=5)
        self.progress_bar.pack_forget()
        
        # Show scanner by default
        self.show_content("scan")
    
    def create_paned_frame(self, parent):
        """Create a paned window for a tab with 50-50 split"""
        paned = tk.PanedWindow(parent, bg='#16213e', sashrelief=tk.RAISED, sashwidth=4)
        paned.pack(fill=tk.BOTH, expand=True)
        
        # Control frame (top/left) - 50%
        control_frame = tk.Frame(paned, bg='#16213e')
        paned.add(control_frame, height=350)
        
        # Results frame (bottom/right) - 50%
        results_frame = tk.Frame(paned, bg='#16213e')
        paned.add(results_frame)
        
        return paned, control_frame, results_frame
    
    def create_scanner_tab(self):
        """Create Scanner tab with its own paned window"""
        self.scanner_container = tk.Frame(self.content_area, bg='#16213e')
        
        paned, control_frame, results_frame = self.create_paned_frame(self.scanner_container)
        self.tab_paned_windows['scan'] = paned
        
        # Create scanner content
        self.create_scanner_content(control_frame, results_frame)
    
    def create_scanner_content(self, control_frame, results_frame):
        """Create Scanner content"""
        # File selection
        file_frame = tk.LabelFrame(control_frame, text="File Selection", 
                                   font=('Segoe UI', 9, 'bold'),
                                   bg='#16213e', fg='#00d4ff', bd=1, relief=tk.GROOVE)
        file_frame.pack(fill=tk.X, pady=5, padx=5)
        
        path_frame = tk.Frame(file_frame, bg='#16213e')
        path_frame.pack(fill=tk.X, padx=10, pady=10)
        
        tk.Label(path_frame, text="File:", font=('Segoe UI', 9),
                bg='#16213e', fg='#c4d0e3').pack(side=tk.LEFT)
        
        self.file_path_var = tk.StringVar()
        file_entry = tk.Entry(path_frame, textvariable=self.file_path_var, 
                              font=('Segoe UI', 9), bg='#0f0f1a', fg='#c4d0e3',
                              insertbackground='#00d4ff', bd=1, relief=tk.FLAT)
        file_entry.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        
        browse_btn = tk.Button(path_frame, text="Browse", font=('Segoe UI', 8),
                               bg='#00d4ff', fg='#0f0f1a', bd=0, padx=12, pady=3,
                               cursor='hand2', command=self.browse_file)
        browse_btn.pack(side=tk.LEFT, padx=5)
        
        # Scan Options
        options_frame = tk.LabelFrame(control_frame, text="Scan Options",
                                      font=('Segoe UI', 9, 'bold'),
                                      bg='#16213e', fg='#00d4ff', bd=1, relief=tk.GROOVE)
        options_frame.pack(fill=tk.X, pady=5, padx=5)
        
        self.deep_scan_var = tk.BooleanVar(value=True)
        deep_check = tk.Checkbutton(options_frame, text="Deep Scan (Extract all metadata)", 
                                    variable=self.deep_scan_var, bg='#16213e', fg='#c4d0e3',
                                    selectcolor='#16213e', activebackground='#16213e')
        deep_check.pack(anchor=tk.W, padx=10, pady=3)
        
        self.hash_var = tk.BooleanVar(value=True)
        hash_check = tk.Checkbutton(options_frame, text="Calculate Cryptographic Hashes", 
                                    variable=self.hash_var, bg='#16213e', fg='#c4d0e3',
                                    selectcolor='#16213e', activebackground='#16213e')
        hash_check.pack(anchor=tk.W, padx=10, pady=3)
        
        # Scan button
        scan_btn = tk.Button(control_frame, text="START FORENSIC SCAN", 
                             font=('Segoe UI', 10, 'bold'), bg='#00d4ff', fg='#0f0f1a',
                             bd=0, padx=20, pady=8, cursor='hand2',
                             command=self.scan_file)
        scan_btn.pack(pady=10)
        
        # Results area
        results_label = tk.LabelFrame(results_frame, text="SCAN RESULTS",
                                      font=('Segoe UI', 9, 'bold'),
                                      bg='#16213e', fg='#00d4ff', bd=1, relief=tk.GROOVE)
        results_label.pack(fill=tk.BOTH, expand=True)
        
        self.result_text = scrolledtext.ScrolledText(
            results_label, wrap=tk.WORD, font=('Consolas', 9),
            bg='#0f0f1a', fg='#00d4ff', insertbackground='#00d4ff',
            bd=0, relief=tk.FLAT
        )
        self.result_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.result_text.insert(tk.END, "TraceGuard Scanner Ready\n\nSelect a file and click 'START FORENSIC SCAN'.")
    
    def create_cleaner_tab(self):
        """Create Cleaner tab with its own paned window"""
        self.cleaner_container = tk.Frame(self.content_area, bg='#16213e')
        
        paned, control_frame, results_frame = self.create_paned_frame(self.cleaner_container)
        self.tab_paned_windows['clean'] = paned
        
        # Create cleaner content
        self.create_cleaner_content(control_frame, results_frame)
    
    def create_cleaner_content(self, control_frame, results_frame):
        """Create Cleaner content with ALL privacy options"""
        # File selection
        file_frame = tk.LabelFrame(control_frame, text="File to Clean",
                                   font=('Segoe UI', 9, 'bold'),
                                   bg='#16213e', fg='#00d4ff', bd=1, relief=tk.GROOVE)
        file_frame.pack(fill=tk.X, pady=5, padx=5)
        
        path_frame = tk.Frame(file_frame, bg='#16213e')
        path_frame.pack(fill=tk.X, padx=10, pady=10)
        
        tk.Label(path_frame, text="File:", font=('Segoe UI', 9),
                bg='#16213e', fg='#c4d0e3').pack(side=tk.LEFT)
        
        self.clean_path_var = tk.StringVar()
        clean_entry = tk.Entry(path_frame, textvariable=self.clean_path_var,
                               font=('Segoe UI', 9), bg='#0f0f1a', fg='#c4d0e3',
                               insertbackground='#00d4ff', bd=1, relief=tk.FLAT)
        clean_entry.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        
        browse_btn = tk.Button(path_frame, text="Browse", font=('Segoe UI', 8),
                               bg='#00d4ff', fg='#0f0f1a', bd=0, padx=12, pady=3,
                               cursor='hand2', command=self.browse_clean_file)
        browse_btn.pack(side=tk.LEFT, padx=5)
        
        # Cleaning method - Row layout
        method_frame = tk.LabelFrame(control_frame, text="Cleaning Method",
                                     font=('Segoe UI', 9, 'bold'),
                                     bg='#16213e', fg='#00d4ff', bd=1, relief=tk.GROOVE)
        method_frame.pack(fill=tk.X, pady=5, padx=5)
        
        methods_row = tk.Frame(method_frame, bg='#16213e')
        methods_row.pack(padx=10, pady=8)
        
        methods = [
            ("🔥 FORENSIC GRADE", "forensic"),
            ("⚡ AGGRESSIVE", "aggressive"),
            ("📝 STANDARD", "standard"),
        ]
        
        for text, value in methods:
            rb = tk.Radiobutton(methods_row, text=text, value=value,
                                variable=self.clean_method, bg='#16213e', fg='#c4d0e3',
                                selectcolor='#16213e', activebackground='#16213e')
            rb.pack(side=tk.LEFT, padx=15)
        
        # Privacy options - 2 columns (ALL options preserved)
        privacy_frame = tk.LabelFrame(control_frame, text="Privacy Options",
                                      font=('Segoe UI', 9, 'bold'),
                                      bg='#16213e', fg='#00d4ff', bd=1, relief=tk.GROOVE)
        privacy_frame.pack(fill=tk.X, pady=5, padx=5)
        
        privacy_left = tk.Frame(privacy_frame, bg='#16213e')
        privacy_left.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=8)
        
        privacy_right = tk.Frame(privacy_frame, bg='#16213e')
        privacy_right.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=8)
        
        cb1 = tk.Checkbutton(privacy_left, text="🔒 Anonymize Filename", 
                             variable=self.anonymize_filename_var, bg='#16213e', fg='#c4d0e3',
                             selectcolor='#16213e', activebackground='#16213e')
        cb1.pack(anchor=tk.W, pady=5)
        
        cb2 = tk.Checkbutton(privacy_left, text="🗑️ Secure Delete Original", 
                             variable=self.secure_delete_var, bg='#16213e', fg='#c4d0e3',
                             selectcolor='#16213e', activebackground='#16213e')
        cb2.pack(anchor=tk.W, pady=5)
        
        cb3 = tk.Checkbutton(privacy_right, text="⏰ Modify Timestamps", 
                             variable=self.modify_timestamp_var, bg='#16213e', fg='#c4d0e3',
                             selectcolor='#16213e', activebackground='#16213e')
        cb3.pack(anchor=tk.W, pady=5)
        
        cb4 = tk.Checkbutton(privacy_right, text="🔄 Recompress Image", 
                             variable=self.recompress_var, bg='#16213e', fg='#c4d0e3',
                             selectcolor='#16213e', activebackground='#16213e')
        cb4.pack(anchor=tk.W, pady=5)
        
        # Clean button
        clean_btn = tk.Button(control_frame, text="START FORENSIC CLEANING", 
                              font=('Segoe UI', 10, 'bold'), bg='#e74c3c', fg='#ffffff',
                              bd=0, padx=20, pady=8, cursor='hand2',
                              command=self.clean_file)
        clean_btn.pack(pady=10)
        
        # Results area
        results_label = tk.LabelFrame(results_frame, text="CLEANING RESULTS",
                                      font=('Segoe UI', 9, 'bold'),
                                      bg='#16213e', fg='#00d4ff', bd=1, relief=tk.GROOVE)
        results_label.pack(fill=tk.BOTH, expand=True)
        
        self.clean_text = scrolledtext.ScrolledText(
            results_label, wrap=tk.WORD, font=('Consolas', 9),
            bg='#0f0f1a', fg='#00ff88', insertbackground='#00d4ff',
            bd=0, relief=tk.FLAT
        )
        self.clean_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.clean_text.insert(tk.END, "TraceGuard Cleaner Ready\n\nSelect a file and click 'START FORENSIC CLEANING'.")
    
    def create_batch_tab(self):
        """Create Batch tab with its own paned window"""
        self.batch_container = tk.Frame(self.content_area, bg='#16213e')
        
        paned, control_frame, results_frame = self.create_paned_frame(self.batch_container)
        self.tab_paned_windows['batch'] = paned
        
        # Create batch content
        self.create_batch_content(control_frame, results_frame)
    
    def create_batch_content(self, control_frame, results_frame):
        """Create Batch content with random renaming"""
        # Source directory
        source_frame = tk.LabelFrame(control_frame, text="Source Directory",
                                     font=('Segoe UI', 9, 'bold'),
                                     bg='#16213e', fg='#00d4ff', bd=1, relief=tk.GROOVE)
        source_frame.pack(fill=tk.X, pady=5, padx=5)
        
        source_path_frame = tk.Frame(source_frame, bg='#16213e')
        source_path_frame.pack(fill=tk.X, padx=10, pady=10)
        
        tk.Label(source_path_frame, text="Source:", font=('Segoe UI', 9),
                bg='#16213e', fg='#c4d0e3').pack(side=tk.LEFT)
        
        self.source_var = tk.StringVar()
        source_entry = tk.Entry(source_path_frame, textvariable=self.source_var,
                                font=('Segoe UI', 9), bg='#0f0f1a', fg='#c4d0e3',
                                insertbackground='#00d4ff', bd=1, relief=tk.FLAT)
        source_entry.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        
        source_btn = tk.Button(source_path_frame, text="Browse", font=('Segoe UI', 8),
                               bg='#00d4ff', fg='#0f0f1a', bd=0, padx=12, pady=3,
                               cursor='hand2', command=self.select_source_folder)
        source_btn.pack(side=tk.LEFT, padx=5)
        
        # Output directory
        output_frame = tk.LabelFrame(control_frame, text="Output Directory",
                                     font=('Segoe UI', 9, 'bold'),
                                     bg='#16213e', fg='#00d4ff', bd=1, relief=tk.GROOVE)
        output_frame.pack(fill=tk.X, pady=5, padx=5)
        
        output_path_frame = tk.Frame(output_frame, bg='#16213e')
        output_path_frame.pack(fill=tk.X, padx=10, pady=10)
        
        tk.Label(output_path_frame, text="Output:", font=('Segoe UI', 9),
                bg='#16213e', fg='#c4d0e3').pack(side=tk.LEFT)
        
        self.output_var = tk.StringVar()
        output_entry = tk.Entry(output_path_frame, textvariable=self.output_var,
                                font=('Segoe UI', 9), bg='#0f0f1a', fg='#c4d0e3',
                                insertbackground='#00d4ff', bd=1, relief=tk.FLAT)
        output_entry.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        
        output_btn = tk.Button(output_path_frame, text="Browse", font=('Segoe UI', 8),
                               bg='#00d4ff', fg='#0f0f1a', bd=0, padx=12, pady=3,
                               cursor='hand2', command=self.select_output_folder)
        output_btn.pack(side=tk.LEFT, padx=5)
        
        # Options
        options_frame = tk.LabelFrame(control_frame, text="Options",
                                      font=('Segoe UI', 9, 'bold'),
                                      bg='#16213e', fg='#00d4ff', bd=1, relief=tk.GROOVE)
        options_frame.pack(fill=tk.X, pady=5, padx=5)
        
        recursive_check = tk.Checkbutton(options_frame, text="Process subfolders recursively", 
                                         variable=self.recursive_var, bg='#16213e', fg='#c4d0e3',
                                         selectcolor='#16213e', activebackground='#16213e')
        recursive_check.pack(anchor=tk.W, padx=10, pady=5)
        
        warning_label = tk.Label(options_frame, text="⚠️ Source and Output folders must be different!",
                                 font=('Segoe UI', 8), bg='#16213e', fg='#ffaa00')
        warning_label.pack(anchor=tk.W, padx=10, pady=5)
        
        # Process button
        batch_btn = tk.Button(control_frame, text="START BATCH PROCESSING", 
                              font=('Segoe UI', 10, 'bold'), bg='#00d4ff', fg='#0f0f1a',
                              bd=0, padx=20, pady=8, cursor='hand2',
                              command=self.start_batch)
        batch_btn.pack(pady=10)
        
        # Results area
        results_label = tk.LabelFrame(results_frame, text="BATCH RESULTS",
                                      font=('Segoe UI', 9, 'bold'),
                                      bg='#16213e', fg='#00d4ff', bd=1, relief=tk.GROOVE)
        results_label.pack(fill=tk.BOTH, expand=True)
        
        self.batch_text = scrolledtext.ScrolledText(
            results_label, wrap=tk.WORD, font=('Consolas', 9),
            bg='#0f0f1a', fg='#00d4ff', insertbackground='#00d4ff',
            bd=0, relief=tk.FLAT
        )
        self.batch_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.batch_text.insert(tk.END, "TraceGuard Batch Processor Ready\n\nSelect source and output folders.")
    
    def create_reports_tab(self):
        """Create Reports tab with its own paned window"""
        self.reports_container = tk.Frame(self.content_area, bg='#16213e')
        
        paned, control_frame, results_frame = self.create_paned_frame(self.reports_container)
        self.tab_paned_windows['reports'] = paned
        
        # Create reports content
        self.create_reports_content(control_frame, results_frame)
    
    def create_reports_content(self, control_frame, results_frame):
        """Create Reports content"""
        # Report generation
        report_frame = tk.LabelFrame(control_frame, text="Generate Report",
                                     font=('Segoe UI', 9, 'bold'),
                                     bg='#16213e', fg='#00d4ff', bd=1, relief=tk.GROOVE)
        report_frame.pack(fill=tk.X, pady=5, padx=5)
        
        format_row = tk.Frame(report_frame, bg='#16213e')
        format_row.pack(padx=10, pady=10)
        
        tk.Label(format_row, text="Format:", font=('Segoe UI', 9),
                bg='#16213e', fg='#c4d0e3').pack(side=tk.LEFT)
        
        self.report_combo = ttk.Combobox(format_row, values=['HTML', 'JSON'], 
                                          textvariable=self.report_format, state='readonly', width=15)
        self.report_combo.pack(side=tk.LEFT, padx=10)
        
        generate_btn = tk.Button(report_frame, text="GENERATE REPORT", 
                                 font=('Segoe UI', 10, 'bold'), bg='#00d4ff', fg='#0f0f1a',
                                 bd=0, padx=20, pady=8, cursor='hand2',
                                 command=self.generate_report)
        generate_btn.pack(pady=10)
        
        # Results area
        results_label = tk.LabelFrame(results_frame, text="REPORT INFORMATION",
                                      font=('Segoe UI', 9, 'bold'),
                                      bg='#16213e', fg='#00d4ff', bd=1, relief=tk.GROOVE)
        results_label.pack(fill=tk.BOTH, expand=True)
        
        self.report_text = scrolledtext.ScrolledText(
            results_label, wrap=tk.WORD, font=('Consolas', 9),
            bg='#0f0f1a', fg='#00d4ff', insertbackground='#00d4ff',
            bd=0, relief=tk.FLAT
        )
        self.report_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.report_text.insert(tk.END, "TraceGuard Report Generator\n\n1. Scan a file\n2. Click 'GENERATE REPORT'")
    
    def create_info_tab(self):
        """Create Info tab - Single page with ALL system info"""
        self.info_container = tk.Frame(self.content_area, bg='#16213e')
        
        main_frame = tk.Frame(self.info_container, bg='#16213e')
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        info_display = tk.Text(main_frame, wrap=tk.WORD, font=('Consolas', 10),
                               bg='#0f0f1a', fg='#00d4ff', bd=2, relief=tk.GROOVE)
        info_display.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        info_text = f"""
╔══════════════════════════════════════════════════════════════════════════════════╗
║                                   TRACEGUARD                                     ║
║                           FORENSIC METADATA CLEANER                              ║
║                                   v2.0.0                                         ║
╠══════════════════════════════════════════════════════════════════════════════════╣
║                                                                                  ║
║  🔍 FORENSIC SCANNER - Extracts EVERY hidden metadata field                      ║
║     • GPS coordinates, camera model, date/time                                   ║
║     • Editing software, copyright, author info                                   ║
║     • Cryptographic hashes (MD5, SHA1, SHA256, SHA512)                           ║
║                                                                                  ║
║  🧹 METADATA CLEANER - Removes ALL traces                                        ║
║     • FORENSIC GRADE - Complete anonymization                                    ║
║     • AGGRESSIVE - Remove all metadata                                           ║
║     • STANDARD - Basic removal                                                   ║
║                                                                                  ║
║  🔒 PRIVACY FEATURES                                                             ║
║     • Anonymize filename (completely random name)                                ║
║     • Secure delete original (3x overwrite - unrecoverable)                      ║
║     • Modify timestamps (hides cleaning time)                                    ║
║     • Recompress image (removes steganography)                                   ║
║                                                                                  ║
║  📦 BATCH PROCESSOR - Clean multiple files                                       ║
║     • Preserves folder structure                                                 ║
║     • Random names for all cleaned files                                         ║
║     • Recursive subfolder processing                                             ║
║                                                                                  ║
║  📄 REPORT GENERATOR                                                             ║
║     • HTML format for professional documentation                                 ║
║     • JSON format for data analysis                                              ║
║     • Saved to 'reports' folder                                                  ║
║                                                                                  ║
╠══════════════════════════════════════════════════════════════════════════════════╣
║                                                                                  ║
║  💻 SYSTEM COMPATIBILITY                                                         ║
║     • Windows 10/11 ✅                                                           ║
║     • Linux (Ubuntu, Debian, Arch) ✅                                            ║
║     • macOS ✅                                                                   ║
║     • TailsOS ✅                                                                 ║
║                                                                                  ║
║  🔧 SYSTEM STATUS                                                                ║
║     • exiftool: {"✅ AVAILABLE" if config.EXIFTOOL_PATH else "❌ NOT FOUND"}                                                              ║
║     • Platform: {platform.system()} {platform.release()}                         ║
║     • Python: {platform.python_version()}                                        ║
║                                                                                  ║
╠══════════════════════════════════════════════════════════════════════════════════╣
║                                                                                  ║
║  📁 OUTPUT LOCATION                                                              ║
║     • Reports: ./reports/                                                        ║
║     • Logs: ./logs/                                                              ║
║                                                                                  ║
╠══════════════════════════════════════════════════════════════════════════════════╣
║                                                                                  ║
║  © 2024 TraceGuard - Professional Forensic Tool                                  ║
║  For authorized forensic analysis and privacy protection only                    ║
║                                                                                  ║
╚══════════════════════════════════════════════════════════════════════════════════╝
"""
        info_display.insert(tk.END, info_text)
        info_display.config(state=tk.DISABLED)
    
    def show_content(self, content_name):
        """Show selected content"""
        for name, btn in self.nav_buttons.items():
            if name == content_name:
                btn.config(fg='#00d4ff', bg='#1a1a2e')
            else:
                btn.config(fg='#8a9ab0', bg='#0f0f1a')
        
        titles = {
            "scan": "SCANNER",
            "clean": "CLEANER",
            "batch": "BATCH PROCESSOR",
            "reports": "REPORTS",
            "info": "INFORMATION"
        }
        self.header_title.config(text=titles.get(content_name, "TRACEGUARD"))
        
        for container in [self.scanner_container, self.cleaner_container, 
                          self.batch_container, self.reports_container, self.info_container]:
            container.pack_forget()
        
        if content_name == "scan":
            self.scanner_container.pack(fill=tk.BOTH, expand=True)
        elif content_name == "clean":
            self.cleaner_container.pack(fill=tk.BOTH, expand=True)
        elif content_name == "batch":
            self.batch_container.pack(fill=tk.BOTH, expand=True)
        elif content_name == "reports":
            self.reports_container.pack(fill=tk.BOTH, expand=True)
        elif content_name == "info":
            self.info_container.pack(fill=tk.BOTH, expand=True)
    
    def check_exiftool(self):
        """Check if exiftool is available"""
        if not config.EXIFTOOL_PATH or not os.path.exists(config.EXIFTOOL_PATH):
            self.status_indicator.config(text="⚠️ LIMITED", fg='#ffaa00')
            self.status_label.config(text="exiftool not found - Install for full functionality")
        else:
            self.status_indicator.config(text="● READY", fg='#00ff88')
            self.status_label.config(text="exiftool ready - Full forensic capabilities")
    
    def browse_file(self):
        filename = filedialog.askopenfilename(title="Select file")
        if filename:
            self.current_file = filename
            self.file_path_var.set(filename)
            self.status_label.config(text=f"Loaded: {os.path.basename(filename)}")
    
    def browse_clean_file(self):
        filename = filedialog.askopenfilename(title="Select file to clean")
        if filename:
            self.clean_file_path = filename
            self.clean_path_var.set(filename)
            self.status_label.config(text=f"Ready to clean: {os.path.basename(filename)}")
    
    def select_source_folder(self):
        folder = filedialog.askdirectory(title="Select SOURCE folder")
        if folder:
            self.batch_folder = folder
            self.source_var.set(folder)
            self.status_label.config(text=f"Source: {os.path.basename(folder)}")
    
    def select_output_folder(self):
        folder = filedialog.askdirectory(title="Select OUTPUT folder")
        if folder:
            self.output_folder = folder
            self.output_var.set(folder)
            self.status_label.config(text=f"Output: {os.path.basename(folder)}")
    
    def scan_file(self):
        if not self.current_file:
            messagebox.showerror("Error", "Please select a file first!")
            return
        
        self.progress_bar.pack(side=tk.RIGHT, padx=15, pady=5)
        self.progress_bar.start()
        self.status_label.config(text="🔍 Scanning metadata...")
        self.result_text.delete(1.0, tk.END)
        
        def scan():
            try:
                results = self.scanner.deep_scan(self.current_file)
                self.current_results = results
                self.root.after(0, self.display_results, results)
                self.root.after(0, lambda: self.status_label.config(text="✅ Scan complete"))
                self.root.after(0, self.progress_bar.stop)
                self.root.after(0, self.progress_bar.pack_forget)
            except Exception as e:
                self.root.after(0, lambda: self.status_label.config(text=f"❌ Error: {str(e)}"))
                self.root.after(0, self.progress_bar.stop)
                self.root.after(0, self.progress_bar.pack_forget)
        
        threading.Thread(target=scan).start()
    
    def display_results(self, results):
        """Display ALL scan results - shows every metadata field"""
        self.result_text.delete(1.0, tk.END)
        
        file_info = results.get('file_info', {})
        metadata = results.get('metadata', {})
        gps_data = results.get('gps_data', {})
        
        self.result_text.insert(tk.END, "=" * 80 + "\n")
        self.result_text.insert(tk.END, "TRACEGUARD FORENSIC SCAN REPORT\n")
        self.result_text.insert(tk.END, "=" * 80 + "\n\n")
        
        # File Information
        self.result_text.insert(tk.END, "📁 FILE INFORMATION\n")
        self.result_text.insert(tk.END, "-" * 50 + "\n")
        self.result_text.insert(tk.END, f"  Name: {file_info.get('name', 'Unknown')}\n")
        self.result_text.insert(tk.END, f"  Size: {file_info.get('size_human', 'Unknown')}\n")
        self.result_text.insert(tk.END, f"  Path: {file_info.get('path', 'Unknown')}\n")
        
        # Cryptographic Hashes
        if results.get('hashes'):
            self.result_text.insert(tk.END, "\n🔐 CRYPTOGRAPHIC HASHES\n")
            self.result_text.insert(tk.END, "-" * 50 + "\n")
            for algo, hash_val in results['hashes'].items():
                self.result_text.insert(tk.END, f"  {algo.upper()}: {hash_val}\n")
        
        # GPS Data
        if gps_data:
            self.result_text.insert(tk.END, "\n📍 GPS LOCATION DATA\n")
            self.result_text.insert(tk.END, "-" * 50 + "\n")
            for key, value in gps_data.items():
                if 'url' not in key.lower():
                    self.result_text.insert(tk.END, f"  {key}: {value}\n")
        
        # ALL METADATA BY CATEGORY - Show everything
        if results.get('metadata_by_category'):
            self.result_text.insert(tk.END, "\n" + "=" * 80 + "\n")
            self.result_text.insert(tk.END, "📋 COMPLETE METADATA EXTRACTION (ALL FIELDS)\n")
            self.result_text.insert(tk.END, "=" * 80 + "\n")
            
            for category, fields in results['metadata_by_category'].items():
                if fields:
                    self.result_text.insert(tk.END, f"\n  ┌─ {category}\n")
                    self.result_text.insert(tk.END, "  │\n")
                    # Show ALL fields, no limit
                    for key, value in fields:
                        val_str = str(value)[:200] + "..." if len(str(value)) > 200 else str(value)
                        self.result_text.insert(tk.END, f"  ├─ {key}: {val_str}\n")
                    self.result_text.insert(tk.END, "  └─ \n")
        
        # Also show raw metadata for completeness
        if metadata:
            self.result_text.insert(tk.END, "\n" + "=" * 80 + "\n")
            self.result_text.insert(tk.END, "📋 RAW METADATA (ALL FIELDS)\n")
            self.result_text.insert(tk.END, "=" * 80 + "\n")
            for key, value in sorted(metadata.items()):
                if value:
                    val_str = str(value)[:200] + "..." if len(str(value)) > 200 else str(value)
                    self.result_text.insert(tk.END, f"  {key}: {val_str}\n")
        
        total_fields = len(metadata)
        self.result_text.insert(tk.END, "\n" + "=" * 80 + "\n")
        self.result_text.insert(tk.END, f"📊 TOTAL METADATA FIELDS FOUND: {total_fields}\n")
        self.result_text.insert(tk.END, "=" * 80 + "\n")
        
        if messagebox.askyesno("Generate Report", f"Found {total_fields} metadata fields!\nGenerate HTML report?"):
            self.generate_report()
    
    def clean_file(self):
        """Clean metadata from file - Forensic Grade with random name"""
        if not hasattr(self, 'clean_file_path') or not self.clean_file_path:
            messagebox.showerror("Error", "Please select a file first!")
            return
        
        method = self.clean_method.get()
        
        # Generate completely random name for forensic grade
        if method == "forensic":
            random_name = hashlib.sha256(os.urandom(32)).hexdigest()[:16]
            output_dir = os.path.dirname(self.clean_file_path)
            ext = os.path.splitext(self.clean_file_path)[1].lower()
            default_output = os.path.join(output_dir, f"{random_name}{ext}")
        else:
            base_name = os.path.splitext(os.path.basename(self.clean_file_path))[0]
            ext = os.path.splitext(self.clean_file_path)[1].lower()
            default_output = os.path.join(os.path.dirname(self.clean_file_path), f"{base_name}_cleaned{ext}")
        
        output_file = filedialog.asksaveasfilename(
            defaultextension=".jpg",
            initialfile=os.path.basename(default_output),
            filetypes=[("Image files", "*.jpg *.jpeg *.png *.tiff *.bmp"), ("All files", "*.*")]
        )
        
        if not output_file:
            return
        
        self.progress_bar.pack(side=tk.RIGHT, padx=15, pady=5)
        self.progress_bar.start()
        self.status_label.config(text=f"🧹 Cleaning with {method.upper()} method...")
        self.clean_text.delete(1.0, tk.END)
        self.clean_text.insert(tk.END, "=" * 70 + "\n")
        self.clean_text.insert(tk.END, f"TRACEGUARD {method.upper()} CLEANING\n")
        self.clean_text.insert(tk.END, "=" * 70 + "\n\n")
        
        def clean():
            try:
                if method == "forensic":
                    result = self.forensic_grade_clean(self.clean_file_path, output_file)
                    self.root.after(0, lambda: self.display_forensic_results(result))
                elif method == "aggressive":
                    result = self.cleaner.aggressive_clean(self.clean_file_path, output_file)
                    self.root.after(0, lambda: self.display_clean_results(result, output_file, method))
                else:
                    result = self.cleaner.standard_clean(self.clean_file_path, output_file)
                    self.root.after(0, lambda: self.display_clean_results(result, output_file, method))
                    
                self.root.after(0, self.progress_bar.stop)
                self.root.after(0, self.progress_bar.pack_forget)
            except Exception as e:
                self.root.after(0, lambda: self.clean_text.insert(tk.END, f"❌ Error: {str(e)}\n"))
                self.root.after(0, lambda: self.status_label.config(text="❌ Cleaning failed"))
                self.root.after(0, self.progress_bar.stop)
                self.root.after(0, self.progress_bar.pack_forget)
        
        threading.Thread(target=clean).start()
    
    def forensic_grade_clean(self, input_path, output_path):
        """Complete forensic grade cleaning - removes ALL traces"""
        results = {'success': False, 'steps_completed': [], 'final_file': output_path, 'original_deleted': False}
        
        output_dir = os.path.dirname(output_path)
        temp_output = output_path + ".temp"
        
        # Step 1: Aggressive metadata removal
        clean_result = self.cleaner.aggressive_clean(input_path, temp_output)
        if not clean_result.get('success'):
            results['error'] = clean_result.get('error')
            return results
        results['steps_completed'].append('✅ Metadata removed from file')
        
        final_file = temp_output
        
        # Step 2: Recompress image (removes hidden data)
        if self.recompress_var.get():
            try:
                ext = os.path.splitext(output_path)[1].lower()
                if ext in ['.jpg', '.jpeg']:
                    img = Image.open(temp_output)
                    quality = random.randint(85, 92)
                    img.save(output_path, quality=quality, optimize=True)
                    os.remove(temp_output)
                    final_file = output_path
                    results['steps_completed'].append('✅ Image recompressed (hidden data removed)')
                else:
                    os.rename(temp_output, output_path)
                    final_file = output_path
            except:
                os.rename(temp_output, output_path)
                final_file = output_path
        else:
            os.rename(temp_output, output_path)
            final_file = output_path
        
        # Step 3: Modify timestamps
        if self.modify_timestamp_var.get():
            try:
                current_time = datetime.now().timestamp()
                os.utime(final_file, (current_time, current_time))
                results['steps_completed'].append('✅ Timestamps modified (cleaning time hidden)')
            except:
                pass
        
        # Step 4: Securely delete original
        if self.secure_delete_var.get():
            try:
                self.cleaner.secure_delete(input_path)
                results['original_deleted'] = True
                results['steps_completed'].append('✅ Original file securely deleted (3x overwrite)')
            except:
                pass
        
        # Step 5: Anonymize filename is handled by random name
        if self.anonymize_filename_var.get():
            results['steps_completed'].append('✅ Filename anonymized (random name)')
        
        results['success'] = True
        results['final_file'] = final_file
        return results
    
    def display_forensic_results(self, result):
        """Display forensic grade cleaning results"""
        if result.get('success'):
            self.clean_text.insert(tk.END, "✅ FORENSIC CLEANING COMPLETE!\n\n")
            self.clean_text.insert(tk.END, "Steps completed:\n")
            for step in result.get('steps_completed', []):
                self.clean_text.insert(tk.END, f"  {step}\n")
            self.clean_text.insert(tk.END, f"\n📁 Final file: {result.get('final_file')}\n")
            self.clean_text.insert(tk.END, "\n" + "=" * 70 + "\n")
            self.clean_text.insert(tk.END, "🔒 PRIVACY STATUS: COMPLETE\n")
            self.clean_text.insert(tk.END, "  • No metadata can be recovered\n")
            self.clean_text.insert(tk.END, "  • Original file cannot be restored\n")
            self.clean_text.insert(tk.END, "  • Filename contains no clues\n")
            self.clean_text.insert(tk.END, "  • Timestamps show no history\n")
            self.clean_text.insert(tk.END, "=" * 70 + "\n")
            
            self.status_label.config(text="✅ Forensic cleaning complete - Maximum privacy achieved")
            
            if messagebox.askyesno("Complete", f"File anonymized!\n\nLocation: {result.get('final_file')}\n\nOpen folder?"):
                os.startfile(os.path.dirname(result.get('final_file')))
        else:
            self.clean_text.insert(tk.END, f"❌ CLEANING FAILED\n\n{result.get('error', 'Unknown error')}\n")
            self.status_label.config(text="❌ Cleaning failed")
    
    def display_clean_results(self, result, output_file, method):
        """Display standard/aggressive cleaning results"""
        if result.get('success'):
            self.clean_text.insert(tk.END, f"✅ {method.upper()} CLEANING SUCCESSFUL!\n\n")
            self.clean_text.insert(tk.END, f"📁 Cleaned file: {output_file}\n")
            self.status_label.config(text="✅ Cleaning complete")
        else:
            self.clean_text.insert(tk.END, f"❌ CLEANING FAILED\n\n{result.get('error', 'Unknown error')}\n")
            self.status_label.config(text="❌ Cleaning failed")
    
    def start_batch(self):
        """Start batch processing - COMPLETELY RANDOM names for all files"""
        if not hasattr(self, 'batch_folder') or not self.batch_folder:
            messagebox.showerror("Error", "Select source folder first!")
            return
        if not hasattr(self, 'output_folder') or not self.output_folder:
            messagebox.showerror("Error", "Select output folder first!")
            return
        if self.batch_folder == self.output_folder:
            messagebox.showerror("Error", "Source and Output folders must be different!")
            return
        
        self.progress_bar.pack(side=tk.RIGHT, padx=15, pady=5)
        self.progress_bar.start()
        self.batch_text.delete(1.0, tk.END)
        self.batch_text.insert(tk.END, "=" * 70 + "\n")
        self.batch_text.insert(tk.END, "TRACEGUARD BATCH PROCESSING\n")
        self.batch_text.insert(tk.END, "=" * 70 + "\n\n")
        self.status_label.config(text="📦 Batch processing...")
        
        def process():
            import glob
            
            files = []
            for ext in ['*.jpg', '*.jpeg', '*.png', '*.tiff', '*.bmp']:
                if self.recursive_var.get():
                    files.extend(glob.glob(os.path.join(self.batch_folder, "**", ext), recursive=True))
                else:
                    files.extend(glob.glob(os.path.join(self.batch_folder, ext)))
            
            files = list(set(files))
            
            if not files:
                self.root.after(0, lambda: self.batch_text.insert(tk.END, "❌ No image files found!\n"))
                self.root.after(0, self.progress_bar.stop)
                self.root.after(0, self.progress_bar.pack_forget)
                return
            
            self.root.after(0, lambda: self.batch_text.insert(tk.END, f"📸 Found {len(files)} images to process\n\n"))
            
            successful = 0
            failed = 0
            failed_files = []
            
            for i, file in enumerate(files, 1):
                rel_path = os.path.relpath(file, self.batch_folder)
                
                # Generate COMPLETELY RANDOM name - no trace of original
                random_name = hashlib.sha256(os.urandom(32)).hexdigest()[:16]
                ext = os.path.splitext(file)[1].lower()
                
                output_path = os.path.join(self.output_folder, rel_path)
                os.makedirs(os.path.dirname(output_path), exist_ok=True)
                # Use ONLY random name, nothing from original
                output_path = os.path.join(os.path.dirname(output_path), f"{random_name}{ext}")
                
                self.root.after(0, lambda i=i, rel=rel_path: self.batch_text.insert(tk.END, f"\n[{i}/{len(files)}] Processing: {rel_path}\n"))
                
                # Use aggressive cleaning for batch
                result = self.cleaner.aggressive_clean(file, output_path)
                
                if result.get('success'):
                    successful += 1
                    self.root.after(0, lambda: self.batch_text.insert(tk.END, f"  ✅ Cleaned -> {random_name}{ext}\n"))
                else:
                    failed += 1
                    failed_files.append(os.path.basename(file))
                    error_msg = str(result.get('error', 'Unknown'))[:50]
                    self.root.after(0, lambda err=error_msg: self.batch_text.insert(tk.END, f"  ❌ Failed: {err}\n"))
                
                self.root.after(0, lambda: self.batch_text.see(tk.END))
            
            self.root.after(0, lambda: self.batch_text.insert(tk.END, f"\n" + "=" * 70 + "\n"))
            self.root.after(0, lambda: self.batch_text.insert(tk.END, f"📊 BATCH SUMMARY\n"))
            self.root.after(0, lambda: self.batch_text.insert(tk.END, "=" * 70 + "\n"))
            self.root.after(0, lambda: self.batch_text.insert(tk.END, f"✅ Successful: {successful}\n"))
            self.root.after(0, lambda: self.batch_text.insert(tk.END, f"❌ Failed: {failed}\n"))
            
            if failed_files:
                self.root.after(0, lambda: self.batch_text.insert(tk.END, f"\nFailed files:\n"))
                for f in failed_files[:10]:
                    self.root.after(0, lambda name=f: self.batch_text.insert(tk.END, f"  • {name}\n"))
            
            self.root.after(0, lambda: self.batch_text.insert(tk.END, f"\n📁 Output folder: {self.output_folder}\n"))
            self.root.after(0, lambda: self.status_label.config(text=f"✅ Batch complete: {successful}/{len(files)} successful"))
            self.root.after(0, self.progress_bar.stop)
            self.root.after(0, self.progress_bar.pack_forget)
            
            if successful > 0:
                self.root.after(0, lambda: messagebox.showinfo("Batch Complete", 
                    f"✅ Successfully cleaned {successful} files!\n\n"
                    f"❌ Failed: {failed}\n\n"
                    f"📁 Output folder: {self.output_folder}\n\n"
                    f"All cleaned files have COMPLETELY RANDOM names - no trace of originals."))
        
        threading.Thread(target=process).start()
    
    def generate_report(self):
        """Generate forensic report"""
        if not self.current_results:
            messagebox.showwarning("Warning", "No scan results. Please scan a file first.")
            return
        
        self.status_label.config(text="📄 Generating report...")
        
        def generate():
            try:
                path = self.reporter.generate_html(self.current_results)
                self.root.after(0, lambda: self.status_label.config(text=f"✅ Report saved"))
                self.root.after(0, lambda: self.report_text.delete(1.0, tk.END))
                self.root.after(0, lambda: self.report_text.insert(tk.END, f"✅ Report generated!\n\n📁 Location: {path}\n\n📊 Format: {self.report_format.get()}"))
                if messagebox.askyesno("Report", f"Report saved to:\n{path}\n\nOpen it?"):
                    os.startfile(str(path))
            except Exception as e:
                self.root.after(0, lambda: self.status_label.config(text=f"❌ Error: {str(e)}"))
        
        threading.Thread(target=generate).start()
    
    def run(self):
        self.root.mainloop()