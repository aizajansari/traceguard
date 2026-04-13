import os
import subprocess
import random
import string
import hashlib
from datetime import datetime
from src.config.settings import config

class ForensicCleaner:
    """Advanced cleaner with privacy protection"""
    
    @staticmethod
    def aggressive_clean(input_path, output_path):
        """Remove ALL metadata - supports JPG, PNG, etc."""
        if not config.EXIFTOOL_PATH:
            return {'success': False, 'error': 'exiftool not found'}
        
        # Get file extension
        ext = os.path.splitext(output_path)[1].lower()
        
        try:
            # For PNG files, use different approach
            if ext == '.png':
                # Use exiftool to remove all metadata from PNG
                cmd = [config.EXIFTOOL_PATH, '-all=', '-overwrite_original', input_path, '-o', output_path]
            else:
                # For JPEG and others
                cmd = [config.EXIFTOOL_PATH, '-all=', input_path, '-o', output_path]
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            
            if result.returncode == 0 and os.path.exists(output_path):
                return {'success': True, 'output': output_path}
            
            # Fallback: use PIL for PNG if exiftool fails
            if ext == '.png':
                try:
                    from PIL import Image
                    img = Image.open(input_path)
                    # Save without metadata
                    img.save(output_path, format='PNG', optimize=True)
                    return {'success': True, 'output': output_path}
                except:
                    pass
            
            return {'success': False, 'error': result.stderr or 'Cleaning failed'}
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    @staticmethod
    def standard_clean(input_path, output_path):
        """Standard cleaning"""
        return ForensicCleaner.aggressive_clean(input_path, output_path)
    
    @staticmethod
    def secure_delete(file_path, passes=3):
        """Securely delete file by overwriting before deletion"""
        if not os.path.exists(file_path):
            return False
        
        try:
            file_size = os.path.getsize(file_path)
            
            for pass_num in range(passes):
                with open(file_path, 'r+b') as f:
                    f.write(os.urandom(file_size))
                    f.flush()
                    os.fsync(f.fileno())
                
                if pass_num == passes - 1:
                    with open(file_path, 'r+b') as f:
                        f.write(b'\x00' * file_size)
                        f.flush()
            
            os.remove(file_path)
            return True
            
        except Exception as e:
            try:
                os.remove(file_path)
            except:
                pass
            return False