"""Application Configuration"""
import os
from pathlib import Path

class Config:
    APP_NAME = "Forensic Metadata Tool"
    VERSION = "3.0.0"
    BASE_DIR = Path(__file__).parent.parent.parent
    REPORTS_DIR = BASE_DIR / "reports"
    LOGS_DIR = BASE_DIR / "logs"
    
    REPORTS_DIR.mkdir(exist_ok=True)
    LOGS_DIR.mkdir(exist_ok=True)
    
    EXIFTOOL_PATH = r"C:\Users\techone\Downloads\exiftool-13.55_64\exiftool-13.55_64\exiftool.exe"
    if not os.path.exists(EXIFTOOL_PATH):
        EXIFTOOL_PATH = None

config = Config()
