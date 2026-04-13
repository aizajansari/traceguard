"""GPS Coordinate Converter - DMS to Decimal and vice versa"""
import re
from typing import Optional, Tuple, Dict


class GPSConverter:
    """Convert GPS coordinates between different formats"""
    
    @staticmethod
    def dms_to_decimal(coord_str: str, ref: str = 'N') -> Optional[float]:
        """
        Convert DMS (Degrees/Minutes/Seconds) to decimal degrees
        
        Examples:
            "40 deg 42' 46.80\"" -> 40.713
            "74 deg 0' 21.60\"" -> 74.006
        
        Args:
            coord_str: DMS coordinate string
            ref: Reference direction (N, S, E, W)
            
        Returns:
            Decimal degrees as float, or None if parsing fails
        """
        if not coord_str:
            return None
        
        # Pattern: "40 deg 42' 46.80\""
        pattern = r'(\d+)\s*deg\s*(\d+)\'\s*([\d.]+)"'
        match = re.search(pattern, str(coord_str))
        
        if match:
            degrees = float(match.group(1))
            minutes = float(match.group(2))
            seconds = float(match.group(3))
            
            decimal = degrees + (minutes / 60.0) + (seconds / 3600.0)
            
            # Handle South and West (negative coordinates)
            if ref in ['S', 'W']:
                decimal = -decimal
            
            return round(decimal, 6)
        
        return None
    
    @staticmethod
    def decimal_to_dms(decimal: float) -> Tuple[int, int, float, str]:
        """
        Convert decimal degrees to DMS format
        
        Args:
            decimal: Decimal degrees (e.g., 40.713)
            
        Returns:
            Tuple of (degrees, minutes, seconds, direction)
        """
        direction = 'N' if decimal >= 0 else 'S'
        abs_decimal = abs(decimal)
        
        degrees = int(abs_decimal)
        minutes = int((abs_decimal - degrees) * 60)
        seconds = (abs_decimal - degrees - minutes/60) * 3600
        
        return (degrees, minutes, round(seconds, 2), direction)
    
    @staticmethod
    def format_dms(degrees: int, minutes: int, seconds: float, direction: str) -> str:
        """Format DMS coordinates as readable string"""
        return f"{degrees}° {minutes}' {seconds}\" {direction}"
    
    @staticmethod
    def get_google_maps_url(lat: float, lon: float) -> str:
        """Generate Google Maps URL from coordinates"""
        return f"https://www.google.com/maps?q={lat},{lon}"
    
    @staticmethod
    def get_openstreetmap_url(lat: float, lon: float) -> str:
        """Generate OpenStreetMap URL from coordinates"""
        return f"https://www.openstreetmap.org/?mlat={lat}&mlon={lon}"
    
    @staticmethod
    def get_what3words_url(lat: float, lon: float) -> str:
        """Generate what3words URL (requires API key for actual words)"""
        return f"https://what3words.com/{lat},{lon}"
    
    @staticmethod
    def parse_exif_gps(exif_data: Dict) -> Dict:
        """
        Parse GPS data from EXIF dictionary
        
        Args:
            exif_data: Dictionary containing EXIF GPS tags
            
        Returns:
            Dictionary with parsed GPS coordinates and map links
        """
        result = {}
        
        # Extract GPS coordinates
        if 'GPSLatitude' in exif_data and 'GPSLongitude' in exif_data:
            lat = GPSConverter.dms_to_decimal(
                exif_data.get('GPSLatitude', ''),
                exif_data.get('GPSLatitudeRef', 'N')
            )
            lon = GPSConverter.dms_to_decimal(
                exif_data.get('GPSLongitude', ''),
                exif_data.get('GPSLongitudeRef', 'E')
            )
            
            if lat and lon:
                result['latitude'] = lat
                result['longitude'] = lon
                result['latitude_dms'] = GPSConverter.decimal_to_dms(lat)
                result['longitude_dms'] = GPSConverter.decimal_to_dms(lon)
                result['google_maps'] = GPSConverter.get_google_maps_url(lat, lon)
                result['openstreetmap'] = GPSConverter.get_openstreetmap_url(lat, lon)
        
        # Extract altitude
        if 'GPSAltitude' in exif_data:
            result['altitude'] = exif_data['GPSAltitude']
            result['altitude_ref'] = exif_data.get('GPSAltitudeRef', 'Above Sea Level')
        
        # Extract timestamp
        if 'GPSTimeStamp' in exif_data:
            result['timestamp'] = exif_data['GPSTimeStamp']
        
        return result