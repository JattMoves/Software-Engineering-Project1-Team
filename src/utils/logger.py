# src/utils/logger.py
"""
Logging configuration
"""

import logging
import os
from typing import Optional

def setup_logger(name: Optional[str] = None) -> logging.Logger:
    """Setup logger with proper configuration"""
    
    logger = logging.getLogger(name or __name__)
    
    # Prevent duplicate handlers
    if logger.handlers:
        return logger
    
    # Get log level from environment
    log_level = int(os.environ.get('LOG_LEVEL', '0'))
    
    if log_level == 0:  # Silent
        logger.setLevel(logging.CRITICAL + 1)  # Effectively disable
        return logger
    elif log_level == 1:  # Informational
        logger.setLevel(logging.INFO)
    elif log_level == 2:  # Debug
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.INFO)
    
    # Create formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # File handler if LOG_FILE is specified
    log_file = os.environ.get('LOG_FILE')
    if log_file:
        try:
            file_handler = logging.FileHandler(log_file)
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)
        except Exception:
            pass  # Fallback to console only
    
    # Console handler for debugging (only if log level > 0)
    if log_level > 0:
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
    
    return logger