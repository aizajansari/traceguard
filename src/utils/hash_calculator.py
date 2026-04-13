"""Cryptographic Hash Calculator - MD5, SHA1, SHA256, SHA512"""
import hashlib
from typing import Dict


class HashCalculator:
    """Calculate multiple cryptographic hashes for file integrity"""
    
    @staticmethod
    def calculate_all(file_path: str, chunk_size: int = 8192) -> Dict[str, str]:
        """
        Calculate MD5, SHA1, SHA256, SHA512 hashes of a file
        
        Args:
            file_path: Path to the file
            chunk_size: Size of chunks to read (default 8KB)
            
        Returns:
            Dictionary with hash names and their values
        """
        hashes = {
            'md5': hashlib.md5(),
            'sha1': hashlib.sha1(),
            'sha256': hashlib.sha256(),
            'sha512': hashlib.sha512()
        }
        
        try:
            with open(file_path, 'rb') as f:
                for chunk in iter(lambda: f.read(chunk_size), b''):
                    for hash_obj in hashes.values():
                        hash_obj.update(chunk)
            
            return {name: h.hexdigest() for name, h in hashes.items()}
        except Exception as e:
            return {name: f"Error: {e}" for name in hashes}
    
    @staticmethod
    def calculate_md5(file_path: str) -> str:
        """Calculate MD5 hash only (fastest)"""
        hash_md5 = hashlib.md5()
        with open(file_path, 'rb') as f:
            for chunk in iter(lambda: f.read(4096), b''):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()
    
    @staticmethod
    def calculate_sha256(file_path: str) -> str:
        """Calculate SHA256 hash (most secure)"""
        sha256 = hashlib.sha256()
        with open(file_path, 'rb') as f:
            for chunk in iter(lambda: f.read(4096), b''):
                sha256.update(chunk)
        return sha256.hexdigest()
    
    @staticmethod
    def verify_integrity(file_path: str, expected_hash: str, algorithm: str = 'sha256') -> bool:
        """Verify file integrity against expected hash"""
        if algorithm == 'md5':
            actual_hash = HashCalculator.calculate_md5(file_path)
        elif algorithm == 'sha256':
            actual_hash = HashCalculator.calculate_sha256(file_path)
        else:
            hashes = HashCalculator.calculate_all(file_path)
            actual_hash = hashes.get(algorithm, '')
        
        return actual_hash.lower() == expected_hash.lower()