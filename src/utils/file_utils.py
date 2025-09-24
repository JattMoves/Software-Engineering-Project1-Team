# src/utils/file_utils.py
"""
File handling utilities
"""

import tempfile
import os
import shutil
import requests
from pathlib import Path
from typing import Optional, Dict, Any
from .logger import setup_logger

class FileUtils:
    """Utilities for file operations"""
    
    def __init__(self):
        self.logger = setup_logger()
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'ACME-ML-Evaluator/1.0'
        })
    
    def download_file(self, url: str, max_size: int = 10 * 1024 * 1024) -> Optional[str]:
        """Download a file and return temporary path"""
        try:
            response = self.session.get(url, stream=True, timeout=30)
            response.raise_for_status()
            
            # Check content length
            content_length = response.headers.get('content-length')
            if content_length and int(content_length) > max_size:
                self.logger.warning(f"File too large: {content_length} bytes")
                return None
            
            # Create temporary file
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.tmp')
            
            downloaded = 0
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    temp_file.write(chunk)
                    downloaded += len(chunk)
                    
                    if downloaded > max_size:
                        temp_file.close()
                        os.unlink(temp_file.name)
                        self.logger.warning(f"File too large during download: {downloaded} bytes")
                        return None
            
            temp_file.close()
            return temp_file.name
            
        except Exception as e:
            self.logger.error(f"Failed to download {url}: {str(e)}")
            return None
    
    def cleanup_temp_file(self, filepath: str) -> None:
        """Clean up temporary file"""
        try:
            if filepath and os.path.exists(filepath):
                os.unlink(filepath)
        except Exception as e:
            self.logger.error(f"Failed to cleanup {filepath}: {str(e)}")
    
    def read_text_file(self, filepath: str, max_size: int = 1024 * 1024) -> Optional[str]:
        """Read text file with size limit"""
        try:
            if not os.path.exists(filepath):
                return None
            
            file_size = os.path.getsize(filepath)
            if file_size > max_size:
                self.logger.warning(f"Text file too large: {file_size} bytes")
                return None
            
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                return f.read()
                
        except Exception as e:
            self.logger.error(f"Failed to read {filepath}: {str(e)}")
            return None