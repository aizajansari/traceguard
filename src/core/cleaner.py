"""Forensic Grade Metadata Cleaner - Maximum Security"""
import os
import subprocess
import random
import hashlib
from datetime import datetime
from src.config.settings import config

class ForensicCleaner:
    """Ultimate forensic cleaner - removes ALL traces"""
    
    @staticmethod
    def aggressive_clean(input_path, output_path):
        """Remove ALL metadata - forensic grade"""
        
        # Method 1: Try exiftool (best)
        if config.EXIFTOOL_PATH and os.path.exists(config.EXIFTOOL_PATH):
            try:
                # Remove ALL metadata groups
                cmd = [config.EXIFTOOL_PATH, '-all=', '-overwrite_original', 
                       '-exif=', '-gps=', '-iptc=', '-xmp=', 
                       '-makerNotes=', '-comment=', '-thumbnailimage=',
                       input_path, '-o', output_path]
                result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
                if result.returncode == 0 and os.path.exists(output_path):
                    return {'success': True, 'output': output_path, 'method': 'exiftool'}
            except:
                pass
        
        # Method 2: PIL fallback (always works)
        try:
            from PIL import Image
            img = Image.open(input_path)
            ext = os.path.splitext(output_path)[1].lower()
            
            # Remove all metadata by saving fresh
            if ext in ['.jpg', '.jpeg']:
                img.save(output_path, 'JPEG', quality=92, optimize=True, progressive=True)
            elif ext == '.png':
                img.save(output_path, 'PNG', optimize=True)
            else:
                img.save(output_path)
            
            if os.path.exists(output_path):
                return {'success': True, 'output': output_path, 'method': 'pil'}
            return {'success': False, 'error': 'Save failed'}
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    @staticmethod
    def secure_delete(file_path, passes=3):
        """Forensic grade secure deletion (3x overwrite)"""
        if not os.path.exists(file_path):
            return False
        
        try:
            file_size = os.path.getsize(file_path)
            
            # Pass 1: Random data
            with open(file_path, 'wb') as f:
                f.write(os.urandom(file_size))
                f.flush()
                os.fsync(f.fileno())
            
            # Pass 2: Another random pattern
            with open(file_path, 'wb') as f:
                f.write(os.urandom(file_size))
                f.flush()
                os.fsync(f.fileno())
            
            # Pass 3: Zeros
            with open(file_path, 'wb') as f:
                f.write(b'\x00' * file_size)
                f.flush()
                os.fsync(f.fileno())
            
            os.remove(file_path)
            return True
        except:
            try:
                os.remove(file_path)
            except:
                pass
            return False