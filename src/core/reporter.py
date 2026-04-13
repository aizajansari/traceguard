"""Report Generator - Shows ALL metadata"""
from datetime import datetime
from pathlib import Path
from src.config.settings import config
from src.config.paths import PathManager


class ReportGenerator:
    """Generate professional forensic reports with ALL metadata"""
    
    @staticmethod
    def generate_html(results: dict) -> str:
        """Generate HTML report showing EVERY metadata field"""
        
        file_info = results.get('file_info', {})
        gps_data = results.get('gps_data', {})
        metadata_by_category = results.get('metadata_by_category', {})
        anomalies = results.get('anomalies', [])
        hashes = results.get('hashes', {})
        total_fields = len(results.get('metadata', {}))
        
        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Forensic Metadata Report - {file_info.get('name', 'Unknown')}</title>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 0;
            padding: 20px;
            background: #f0f0f0;
        }}
        .container {{
            max-width: 1400px;
            margin: 0 auto;
            background: white;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            overflow: hidden;
        }}
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
        }}
        .header h1 {{
            margin: 0;
            font-size: 28px;
        }}
        .header p {{
            margin: 10px 0 0;
            opacity: 0.9;
        }}
        .content {{
            padding: 30px;
        }}
        .section {{
            margin-bottom: 30px;
            border-left: 4px solid #667eea;
            padding-left: 20px;
        }}
        .section h2 {{
            color: #667eea;
            margin-top: 0;
            font-size: 22px;
        }}
        .section h3 {{
            color: #764ba2;
            margin: 15px 0 10px;
            font-size: 18px;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 10px 0;
        }}
        th, td {{
            padding: 10px;
            text-align: left;
            border-bottom: 1px solid #ddd;
        }}
        th {{
            background-color: #f5f5f5;
            font-weight: bold;
            color: #333;
        }}
        td:first-child {{
            font-weight: bold;
            width: 250px;
            color: #555;
        }}
        .badge {{
            display: inline-block;
            padding: 3px 8px;
            border-radius: 3px;
            font-size: 11px;
            font-weight: bold;
        }}
        .badge-high {{
            background: #dc3545;
            color: white;
        }}
        .badge-medium {{
            background: #ffc107;
            color: #333;
        }}
        .badge-low {{
            background: #28a745;
            color: white;
        }}
        .footer {{
            background: #f8f9fa;
            padding: 15px;
            text-align: center;
            font-size: 12px;
            color: #666;
            border-top: 1px solid #ddd;
        }}
        .summary-box {{
            background: #f8f9fa;
            padding: 15px;
            border-radius: 5px;
            margin: 20px 0;
        }}
        code {{
            background: #f4f4f4;
            padding: 2px 5px;
            border-radius: 3px;
            font-family: 'Consolas', monospace;
            font-size: 12px;
        }}
    </style>
</head>
<body>
<div class="container">
    <div class="header">
        <h1>Forensic Metadata Analysis Report</h1>
        <p>Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        <p>Tool: {config.APP_NAME} v{config.VERSION}</p>
    </div>
    
    <div class="content">
        <!-- File Information -->
        <div class="section">
            <h2>File Information</h2>
            <table>
"""
        
        for key, value in file_info.items():
            html += f"<tr><td>{key}</td><td>{value}</td></tr>"
        
        html += """
            </table>
        </div>
        
        <!-- Cryptographic Hashes -->
        <div class="section">
            <h2>Cryptographic Hashes</h2>
            <table>
"""
        
        for algo, hash_val in hashes.items():
            html += f"<tr><td>{algo.upper()}</td><td><code>{hash_val}</code></td></tr>"
        
        html += """
            </table>
        </div>
"""
        
        # GPS Data
        if gps_data:
            html += """
        <div class="section">
            <h2>GPS Location Data</h2>
            <table>
"""
            for key, value in gps_data.items():
                if 'url' in key.lower():
                    html += f'<tr><td>{key}</td><td><a href="{value}" target="_blank">{value}</a></td></tr>'
                else:
                    html += f"<tr><td>{key}</td><td>{value}</td></tr>"
            
            html += """
            </table>
        </div>
"""
        
        # ALL METADATA by category
        html += """
        <div class="section">
            <h2>Complete Metadata Extraction</h2>
            <p>Total fields found: <strong>""" + str(total_fields) + """</strong></p>
"""
        
        for category, fields in metadata_by_category.items():
            if fields:
                html += f"""
            <h3>{category}</h3>
            <table>
"""
                for key, value in fields:
                    # Escape HTML special characters
                    value = str(value).replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
                    html += f"<tr><td>{key}</td><td>{value}</td></tr>"
                
                html += """
            </table>
"""
        
        html += """
        </div>
"""
        
        # Anomalies
        if anomalies:
            html += """
        <div class="section">
            <h2>Detected Anomalies & Privacy Risks</h2>
            <table>
"""
            for anomaly in anomalies:
                severity = anomaly.get('severity', 'LOW')
                html += f"""
                <tr>
                    <td><span class="badge badge-{severity.lower()}">{severity}</span></td>
                    <td><strong>{anomaly.get('type', 'Unknown')}</strong><br>{anomaly.get('description', '')}</td>
                </tr>
"""
            
            html += """
            </table>
        </div>
"""
        
        # Summary
        html += f"""
        <div class="summary-box">
            <h3>Analysis Summary</h3>
            <table>
                <tr><td>Total Metadata Fields</td><td>{total_fields}</td></tr>
                <tr><td>GPS Data Present</td><td>{'Yes' if gps_data else 'No'}</td></tr>
                <tr><td>Anomalies Detected</td><td>{len(anomalies)}</td></tr>
                <tr><td>File Size</td><td>{file_info.get('size_human', 'Unknown')}</td></tr>
            </table>
        </div>
        
        <div class="summary-box">
            <h3>Privacy Recommendation</h3>
            <p>This report shows {total_fields} metadata fields embedded in the file.</p>
            <p>To protect your privacy, use the "Cleaner" tab to remove all metadata before sharing this file.</p>
        </div>
    </div>
    
    <div class="footer">
        <p>Report generated by {config.APP_NAME} v{config.VERSION} | Forensic analysis tool</p>
        <p>This report is for forensic and investigative purposes only</p>
    </div>
</div>
</body>
</html>
"""
        
        report_path = PathManager.get_report_path("html")
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(html)
        
        return str(report_path)