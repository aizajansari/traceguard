"""Professional Dark Theme for Forensic Tool"""
import tkinter as tk
from tkinter import ttk

class ForensicTheme:
    """Hacker/Cybersecurity theme colors and styles"""
    
    # Color palette
    BG_DARK = "#0a0a0a"      # Deep black
    BG_MEDIUM = "#0f0f0f"    # Dark gray
    BG_LIGHT = "#1a1a1a"     # Lighter dark
    
    FG_PRIMARY = "#00ff41"   # Matrix green
    FG_SECONDARY = "#00cc33" # Brighter green
    FG_ERROR = "#ff3333"     # Red for errors
    FG_WARNING = "#ffaa00"   # Yellow for warnings
    
    ACCENT = "#003300"       # Dark green accent
    HIGHLIGHT = "#00ff41"    # Bright green highlight
    
    @classmethod
    def apply_theme(cls, root):
        """Apply the hacker theme to the root window"""
        root.configure(bg=cls.BG_DARK)
        
        # Configure ttk styles
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure all ttk widgets
        style.configure('TLabel', background=cls.BG_DARK, foreground=cls.FG_PRIMARY, font=('Consolas', 10))
        style.configure('TLabelframe', background=cls.BG_DARK, foreground=cls.FG_PRIMARY, 
                       bordercolor=cls.FG_PRIMARY, borderwidth=1)
        style.configure('TLabelframe.Label', background=cls.BG_DARK, foreground=cls.FG_PRIMARY, 
                       font=('Consolas', 10, 'bold'))
        style.configure('TButton', background=cls.BG_MEDIUM, foreground=cls.FG_PRIMARY,
                       bordercolor=cls.FG_PRIMARY, borderwidth=1, font=('Consolas', 10, 'bold'))
        style.map('TButton', background=[('active', cls.ACCENT)])
        style.configure('TEntry', fieldbackground=cls.BG_MEDIUM, foreground=cls.FG_PRIMARY,
                       insertcolor=cls.FG_PRIMARY)
        style.configure('TFrame', background=cls.BG_DARK)
        
        return style