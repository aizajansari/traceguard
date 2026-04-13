"""Advanced Metadata Scanner - Shows ALL metadata fields"""
import os
import json
import subprocess
from typing import Dict, Any
from src.config.settings import config
from src.utils.hash_calculator import HashCalculator
from src.utils.gps_converter import GPSConverter
from src.utils.file_handler import FileHandler


class ForensicScanner:
    """Advanced metadata scanner - extracts EVERYTHING"""
    
    def __init__(self):
        self.hash_calc = HashCalculator()
        self.gps_conv = GPSConverter()
        self.file_handler = FileHandler()
    
    def deep_scan(self, file_path: str) -> Dict[str, Any]:
        """Perform comprehensive forensic scan - shows ALL metadata"""
        
        results = {
            'file_info': self.file_handler.get_file_info(file_path),
            'hashes': self.hash_calc.calculate_all(file_path),
            'metadata': {},
            'all_metadata_fields': [],  # New: List of all field names
            'metadata_by_category': {},  # New: Categorized metadata
            'gps_data': None,
            'anomalies': []
        }
        
        # Extract metadata if exiftool available
        if config.EXIFTOOL_PATH:
            raw_metadata = self._extract_metadata(file_path)
            results['metadata'] = raw_metadata
            
            # Get all field names
            results['all_metadata_fields'] = list(raw_metadata.keys())
            
            # Categorize all metadata
            results['metadata_by_category'] = self._categorize_all_metadata(raw_metadata)
            
            # Extract GPS
            results['gps_data'] = self._extract_gps(raw_metadata)
            
            # Detect anomalies
            results['anomalies'] = self._detect_anomalies(raw_metadata)
        
        return results
    
    def _extract_metadata(self, file_path: str) -> dict:
        """Extract ALL metadata using exiftool"""
        try:
            result = subprocess.run(
                [config.EXIFTOOL_PATH, '-j', file_path],
                capture_output=True, text=True, timeout=30
            )
            
            if result.returncode == 0 and result.stdout:
                data = json.loads(result.stdout)
                return data[0] if data else {}
            return {}
        except Exception as e:
            return {'error': str(e)}
    
    def _categorize_all_metadata(self, metadata: dict) -> dict:
        """Categorize ALL metadata fields into groups"""
        
        categories = {
            '📷 CAMERA & DEVICE INFO': [],
            '📍 GPS & LOCATION': [],
            '📅 DATE & TIME': [],
            '⚙️ CAMERA SETTINGS': [],
            '🖥️ SOFTWARE & EDITING': [],
            '📁 FILE PROPERTIES': [],
            '©️ COPYRIGHT & AUTHOR': [],
            '🔧 TECHNICAL DETAILS': [],
            '📝 OTHER METADATA': []
        }
        
        # Keywords for categorization
        category_keywords = {
            '📷 CAMERA & DEVICE INFO': ['Make', 'Model', 'Camera', 'Lens', 'Serial', 'Device', 'Manufacturer'],
            '📍 GPS & LOCATION': ['GPS', 'Latitude', 'Longitude', 'Altitude', 'Position', 'Location'],
            '📅 DATE & TIME': ['Date', 'Time', 'DateTime', 'Timestamp', 'Create', 'Modify', 'Original'],
            '⚙️ CAMERA SETTINGS': ['ISO', 'FNumber', 'Exposure', 'Focal', 'Aperture', 'Shutter', 'WhiteBalance', 'Flash'],
            '🖥️ SOFTWARE & EDITING': ['Software', 'Creator', 'Editor', 'Processor', 'Tool', 'History'],
            '📁 FILE PROPERTIES': ['File', 'Size', 'Type', 'Format', 'Dimension', 'Width', 'Height', 'Resolution'],
            '©️ COPYRIGHT & AUTHOR': ['Copyright', 'Rights', 'Artist', 'Author', 'Owner', 'Credit'],
            '🔧 TECHNICAL DETAILS': ['Bits', 'Color', 'Profile', 'Compression', 'Quality', 'Version']
        }
        
        for key, value in metadata.items():
            if not value or key == 'SourceFile':
                continue
                
            categorized = False
            for category, keywords in category_keywords.items():
                if any(kw.lower() in key.lower() for kw in keywords):
                    categories[category].append((key, str(value)[:150]))
                    categorized = True
                    break
            
            if not categorized:
                categories['📝 OTHER METADATA'].append((key, str(value)[:150]))
        
        # Remove empty categories
        return {k: v for k, v in categories.items() if v}
    
    def _extract_gps(self, metadata: dict) -> dict:
        """Extract and parse GPS data"""
        gps_data = {}
        
        gps_fields = ['GPSLatitude', 'GPSLongitude', 'GPSAltitude', 'GPSPosition',
                      'GPSLatitudeRef', 'GPSLongitudeRef', 'GPSAltitudeRef',
                      'GPSDateStamp', 'GPSTimeStamp', 'GPSVersionID']
        
        for field in gps_fields:
            if field in metadata and metadata[field]:
                gps_data[field] = metadata[field]
        
        # Convert to decimal
        if 'GPSLatitude' in gps_data and 'GPSLongitude' in gps_data:
            lat = self.gps_conv.dms_to_decimal(
                gps_data['GPSLatitude'],
                metadata.get('GPSLatitudeRef', 'N')
            )
            lon = self.gps_conv.dms_to_decimal(
                gps_data['GPSLongitude'],
                metadata.get('GPSLongitudeRef', 'E')
            )
            
            if lat and lon:
                gps_data['decimal_latitude'] = lat
                gps_data['decimal_longitude'] = lon
                gps_data['google_maps_url'] = self.gps_conv.get_google_maps_url(lat, lon)
        
        return gps_data
    
    def _detect_anomalies(self, metadata: dict) -> list:
        """Detect anomalies in metadata"""
        anomalies = []
        
        # Check for GPS (privacy risk)
        if any('GPS' in k for k in metadata.keys()):
            anomalies.append({
                'severity': 'HIGH',
                'type': 'GPS_DATA_FOUND',
                'description': 'GPS coordinates found in metadata - location privacy at risk'
            })
        
        # Check for editing software
        editing_software = ['Photoshop', 'Lightroom', 'GIMP', 'Paint.NET', 'Pixelmator', 'AfterShot']
        for software in editing_software:
            if any(software.lower() in str(v).lower() for v in metadata.values()):
                anomalies.append({
                    'severity': 'MEDIUM',
                    'type': 'EDITING_SOFTWARE_DETECTED',
                    'description': f'Image appears to have been edited with {software}'
                })
                break
        
        # Check for multiple dates
        date_fields = [v for k, v in metadata.items() if 'Date' in k and v]
        if len(set(date_fields)) > 3:
            anomalies.append({
                'severity': 'LOW',
                'type': 'INCONSISTENT_DATES',
                'description': 'Multiple inconsistent dates found in metadata'
            })
        
        # Check for software that might indicate manipulation
        suspicious_software = ['DeepFake', 'AI Generated', 'StableDiffusion', 'DALL-E']
        for sw in suspicious_software:
            if any(sw.lower() in str(v).lower() for v in metadata.values()):
                anomalies.append({
                    'severity': 'HIGH',
                    'type': 'AI_GENERATED_CONTENT',
                    'description': f'Image may be AI-generated or manipulated with {sw}'
                })
                break
        
        return anomalies