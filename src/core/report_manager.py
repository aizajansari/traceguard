"""Professional Report Management"""
import shutil
import zipfile
from pathlib import Path
from datetime import datetime, timedelta
from src.config.settings import config

class ReportManager:
    """Manage forensic reports professionally"""
    
    @staticmethod
    def archive_old_reports(days_old=30):
        """Archive reports older than specified days"""
        archive_dir = config.REPORTS_DIR / "archive"
        archive_dir.mkdir(exist_ok=True)
        
        cutoff = datetime.now() - timedelta(days=days_old)
        archived_count = 0
        
        for report in config.REPORTS_DIR.rglob("*.*"):
            if report.suffix in ['.html', '.json', '.pdf']:
                if datetime.fromtimestamp(report.stat().st_mtime) < cutoff:
                    # Create zip archive
                    zip_name = archive_dir / f"archive_{cutoff.strftime('%Y%m')}.zip"
                    with zipfile.ZipFile(zip_name, 'a') as zipf:
                        zipf.write(report, report.relative_to(config.REPORTS_DIR))
                    report.unlink()  # Delete original
                    archived_count += 1
        
        return archived_count
    
    @staticmethod
    def export_report_bundle(case_id, output_path):
        """Export all reports for a case as a bundle"""
        case_dir = config.REPORTS_DIR / "cases" / case_id
        
        if not case_dir.exists():
            return None
        
        # Create zip bundle
        bundle_path = Path(output_path) / f"case_{case_id}_bundle.zip"
        with zipfile.ZipFile(bundle_path, 'w') as zipf:
            for file in case_dir.rglob("*"):
                zipf.write(file, file.relative_to(case_dir.parent))
        
        return bundle_path
    
    @staticmethod
    def get_report_statistics():
        """Get statistics about generated reports"""
        stats = {
            'total_reports': 0,
            'by_type': {'html': 0, 'json': 0, 'pdf': 0},
            'by_month': {},
            'total_size_mb': 0
        }
        
        for report in config.REPORTS_DIR.rglob("*.*"):
            if report.suffix in ['.html', '.json', '.pdf']:
                stats['total_reports'] += 1
                ext = report.suffix[1:].lower()
                stats['by_type'][ext] = stats['by_type'].get(ext, 0) + 1
                
                # Track by month
                month = datetime.fromtimestamp(report.stat().st_mtime).strftime("%Y-%m")
                stats['by_month'][month] = stats['by_month'].get(month, 0) + 1
                
                stats['total_size_mb'] += report.stat().st_size / (1024 * 1024)
        
        return stats
    
    @staticmethod
    def cleanup_temp_reports():
        """Delete reports older than 7 days from temp folder"""
        temp_dir = config.REPORTS_DIR / "temp"
        if temp_dir.exists():
            cutoff = datetime.now() - timedelta(days=7)
            for report in temp_dir.glob("*"):
                if datetime.fromtimestamp(report.stat().st_mtime) < cutoff:
                    report.unlink()