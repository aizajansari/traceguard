"""Path management"""
from datetime import datetime
from pathlib import Path
from src.config.settings import config


class PathManager:
    """Manage application paths"""
    
    @staticmethod
    def get_report_path(format="html"):
        """Generate report path with timestamp"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        return config.REPORTS_DIR / f"forensic_report_{timestamp}.{format}"
    
    @staticmethod
    def get_log_path():
        """Get log file path"""
        timestamp = datetime.now().strftime("%Y%m%d")
        return config.LOGS_DIR / f"forensic_tool_{timestamp}.log"