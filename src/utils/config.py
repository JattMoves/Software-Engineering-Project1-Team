# src/utils/config.py
"""
Configuration management
"""

import os
from typing import Dict, Any

class Config:
    """Configuration settings"""
    
    def __init__(self):
        self.log_level = int(os.environ.get('LOG_LEVEL', '0'))
        self.log_file = os.environ.get('LOG_FILE')
        self.github_token = os.environ.get('GITHUB_TOKEN')
        self.hf_token = os.environ.get('HF_TOKEN')
        
        # Default timeouts and limits
        self.request_timeout = 30
        self.max_workers = 8
        self.max_file_size = 10 * 1024 * 1024  # 10MB
    
    def get_headers(self) -> Dict[str, str]:
        """Get HTTP headers with authentication if available"""
        headers = {
            'User-Agent': 'ACME-ML-Evaluator/1.0'
        }
        
        if self.github_token:
            headers['Authorization'] = f'token {self.github_token}'
        
        if self.hf_token:
            headers['Authorization'] = f'Bearer {self.hf_token}'
        
        return headers