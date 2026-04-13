"""File Operations Handler - File info, size formatting, path utilities"""
import os
import stat
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional


class FileHandler:
    """Handle file operations and information extraction"""
    
    @staticmethod
    def get_file_info(file_path: str) -> Dict:
        """
        Get comprehensive file information
        
        Args:
            file_path: Path to the file
            
        Returns:
            Dictionary with file information
        """
        if not os.path.exists(file_path):
            return {'error': 'File not found'}
        
        stat_result = os.stat(file_path)
        size_bytes = stat_result.st_size
        
        return {
            'name': os.path.basename(file_path),
            'path': os.path.abspath(file_path),
            'directory': os.path.dirname(os.path.abspath(file_path)),
            'size_bytes': size_bytes,
            'size_human': FileHandler._human_readable_size(size_bytes),
            'created': datetime.fromtimestamp(stat_result.st_ctime).strftime('%Y-%m-%d %H:%M:%S'),
            'modified': datetime.fromtimestamp(stat_result.st_mtime).strftime('%Y-%m-%d %H:%M:%S'),
            'accessed': datetime.fromtimestamp(stat_result.st_atime).strftime('%Y-%m-%d %H:%M:%S'),
            'extension': os.path.splitext(file_path)[1].lower(),
            'is_readonly': not os.access(file_path, os.W_OK),
            'is_hidden': FileHandler._is_hidden(file_path)
        }
    
    @staticmethod
    def _human_readable_size(size_bytes: int) -> str:
        """Convert bytes to human readable format"""
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if size_bytes < 1024.0:
                return f"{size_bytes:.1f} {unit}"
            size_bytes /= 1024.0
        return f"{size_bytes:.1f} PB"
    
    @staticmethod
    def _is_hidden(file_path: str) -> bool:
        """Check if file is hidden (Windows and Unix)"""
        name = os.path.basename(file_path)
        if name.startswith('.'):
            return True
        
        # Windows hidden attribute
        if os.name == 'nt':
            try:
                # Get file attributes on Windows
                import ctypes
                FILE_ATTRIBUTE_HIDDEN = 0x2
                result = ctypes.windll.kernel32.GetFileAttributesW(file_path)
                return bool(result & FILE_ATTRIBUTE_HIDDEN)
            except:
                pass
        return False
    
    @staticmethod
    def is_supported_image(file_path: str) -> bool:
        """Check if file is a supported image format"""
        supported_extensions = {'.jpg', '.jpeg', '.png', '.tiff', '.tif', '.bmp', '.gif'}
        ext = os.path.splitext(file_path)[1].lower()
        return ext in supported_extensions
    
    @staticmethod
    def get_file_signature(file_path: str, bytes_count: int = 8) -> Optional[str]:
        """
        Get file signature (magic bytes) for identification
        
        Args:
            file_path: Path to the file
            bytes_count: Number of bytes to read
            
        Returns:
            Hexadecimal string of file signature
        """
        try:
            with open(file_path, 'rb') as f:
                signature = f.read(bytes_count)
                return signature.hex().upper()
        except:
            return None
    
    @staticmethod
    def list_files_in_directory(directory: str, recursive: bool = False, 
                                extensions: Optional[List[str]] = None) -> List[str]:
        """
        List all files in a directory with optional filtering
        
        Args:
            directory: Directory path
            recursive: Include subdirectories
            extensions: List of extensions to filter (e.g., ['.jpg', '.png'])
            
        Returns:
            List of file paths
        """
        if not os.path.exists(directory):
            return []
        
        files = []
        if recursive:
            for root, _, filenames in os.walk(directory):
                for filename in filenames:
                    file_path = os.path.join(root, filename)
                    if extensions:
                        ext = os.path.splitext(filename)[1].lower()
                        if ext in extensions:
                            files.append(file_path)
                    else:
                        files.append(file_path)
        else:
            for filename in os.listdir(directory):
                file_path = os.path.join(directory, filename)
                if os.path.isfile(file_path):
                    if extensions:
                        ext = os.path.splitext(filename)[1].lower()
                        if ext in extensions:
                            files.append(file_path)
                    else:
                        files.append(file_path)
        
        return sorted(files)
    
    @staticmethod
    def ensure_directory(directory: str) -> bool:
        """Ensure directory exists, create if not"""
        try:
            Path(directory).mkdir(parents=True, exist_ok=True)
            return True
        except:
            return False
    
    @staticmethod
    def get_unique_filename(directory: str, base_name: str, extension: str) -> str:
        """Generate a unique filename if file already exists"""
        counter = 1
        filename = f"{base_name}{extension}"
        filepath = os.path.join(directory, filename)
        
        while os.path.exists(filepath):
            filename = f"{base_name}_{counter}{extension}"
            filepath = os.path.join(directory, filename)
            counter += 1
        
        return filepath