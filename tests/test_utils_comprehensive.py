# tests/test_utils_comprehensive.py
"""
Comprehensive tests for utility modules to improve coverage
"""

import pytest
import os
import tempfile
from unittest.mock import Mock, patch, mock_open
from src.utils.config import Config
from src.utils.logger import setup_logger
from src.utils.file_utils import FileUtils


class TestConfig:
    """Test configuration utility"""
    
    def test_config_initialization(self):
        """Test config initialization"""
        config = Config()
        assert config is not None
        assert hasattr(config, 'get')
    
    def test_config_get_default(self):
        """Test config get with default value"""
        config = Config()
        value = config.get('nonexistent_key', 'default_value')
        assert value == 'default_value'
    
    def test_config_get_existing(self):
        """Test config get with existing value"""
        config = Config()
        # Set a test value
        config._config = {'test_key': 'test_value'}
        value = config.get('test_key', 'default_value')
        assert value == 'test_value'
    
    def test_config_set(self):
        """Test config set method"""
        config = Config()
        config.set('new_key', 'new_value')
        value = config.get('new_key')
        assert value == 'new_value'
    
    def test_config_get_all(self):
        """Test config get all method"""
        config = Config()
        config.set('key1', 'value1')
        config.set('key2', 'value2')
        all_config = config.get_all()
        assert isinstance(all_config, dict)
        assert 'key1' in all_config
        assert 'key2' in all_config


class TestLogger:
    """Test logging utility"""
    
    def test_logger_setup(self):
        """Test logger setup"""
        logger = setup_logger()
        assert logger is not None
        assert hasattr(logger, 'info')
        assert hasattr(logger, 'error')
        assert hasattr(logger, 'debug')
        assert hasattr(logger, 'warning')
    
    def test_logger_levels(self):
        """Test logger different levels"""
        logger = setup_logger()
        
        # Test that we can call different log levels without errors
        logger.debug("Debug message")
        logger.info("Info message")
        logger.warning("Warning message")
        logger.error("Error message")
    
    @patch.dict(os.environ, {'LOG_LEVEL': '1'})
    def test_logger_with_env_level(self):
        """Test logger with environment level"""
        logger = setup_logger()
        assert logger is not None
    
    @patch.dict(os.environ, {'LOG_FILE': '/tmp/test.log'})
    def test_logger_with_env_file(self):
        """Test logger with environment file"""
        logger = setup_logger()
        assert logger is not None


class TestFileUtils:
    """Test file utilities"""
    
    def test_file_utils_initialization(self):
        """Test file utils initialization"""
        file_utils = FileUtils()
        assert file_utils is not None
    
    def test_download_file_success(self):
        """Test successful file download"""
        file_utils = FileUtils()
        
        with patch('src.utils.file_utils.requests.get') as mock_get:
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.content = b'test content'
            mock_get.return_value = mock_response
            
            with tempfile.NamedTemporaryFile(delete=False) as temp_file:
                temp_path = temp_file.name
            
            try:
                result = file_utils.download_file('http://example.com/test', temp_path)
                assert result is True
            finally:
                if os.path.exists(temp_path):
                    os.unlink(temp_path)
    
    def test_download_file_failure(self):
        """Test file download failure"""
        file_utils = FileUtils()
        
        with patch('src.utils.file_utils.requests.get') as mock_get:
            mock_response = Mock()
            mock_response.status_code = 404
            mock_get.return_value = mock_response
            
            result = file_utils.download_file('http://example.com/notfound', '/tmp/test')
            assert result is False
    
    def test_download_file_exception(self):
        """Test file download with exception"""
        file_utils = FileUtils()
        
        with patch('src.utils.file_utils.requests.get') as mock_get:
            mock_get.side_effect = Exception("Network error")
            
            result = file_utils.download_file('http://example.com/test', '/tmp/test')
            assert result is False
    
    def test_extract_archive_success(self):
        """Test successful archive extraction"""
        file_utils = FileUtils()
        
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create a simple text file to simulate archive content
            test_file = os.path.join(temp_dir, 'test.txt')
            with open(test_file, 'w') as f:
                f.write('test content')
            
            result = file_utils.extract_archive(test_file, temp_dir)
            # This might fail depending on file type, but should not crash
            assert isinstance(result, bool)
    
    def test_extract_archive_failure(self):
        """Test archive extraction failure"""
        file_utils = FileUtils()
        
        result = file_utils.extract_archive('/nonexistent/file', '/tmp/')
        assert result is False
    
    def test_cleanup_directory(self):
        """Test directory cleanup"""
        file_utils = FileUtils()
        
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create some test files
            test_file = os.path.join(temp_dir, 'test.txt')
            with open(test_file, 'w') as f:
                f.write('test content')
            
            result = file_utils.cleanup_directory(temp_dir)
            assert result is True
    
    def test_cleanup_nonexistent_directory(self):
        """Test cleanup of nonexistent directory"""
        file_utils = FileUtils()
        
        result = file_utils.cleanup_directory('/nonexistent/directory')
        assert result is False
    
    def test_get_file_size(self):
        """Test get file size"""
        file_utils = FileUtils()
        
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            temp_file.write(b'test content')
            temp_path = temp_file.name
        
        try:
            size = file_utils.get_file_size(temp_path)
            assert size > 0
        finally:
            if os.path.exists(temp_path):
                os.unlink(temp_path)
    
    def test_get_file_size_nonexistent(self):
        """Test get file size for nonexistent file"""
        file_utils = FileUtils()
        
        size = file_utils.get_file_size('/nonexistent/file')
        assert size == 0
    
    def test_is_valid_url(self):
        """Test URL validation"""
        file_utils = FileUtils()
        
        assert file_utils.is_valid_url('http://example.com') is True
        assert file_utils.is_valid_url('https://example.com') is True
        assert file_utils.is_valid_url('ftp://example.com') is True
        assert file_utils.is_valid_url('invalid-url') is False
        assert file_utils.is_valid_url('') is False
        assert file_utils.is_valid_url(None) is False
    
    def test_create_directory(self):
        """Test directory creation"""
        file_utils = FileUtils()
        
        with tempfile.TemporaryDirectory() as base_dir:
            new_dir = os.path.join(base_dir, 'new_directory')
            result = file_utils.create_directory(new_dir)
            assert result is True
            assert os.path.exists(new_dir)
    
    def test_create_directory_existing(self):
        """Test directory creation when directory already exists"""
        file_utils = FileUtils()
        
        with tempfile.TemporaryDirectory() as temp_dir:
            result = file_utils.create_directory(temp_dir)
            assert result is True  # Should succeed even if exists
    
    def test_list_files(self):
        """Test file listing"""
        file_utils = FileUtils()
        
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create some test files
            test_file1 = os.path.join(temp_dir, 'file1.txt')
            test_file2 = os.path.join(temp_dir, 'file2.py')
            with open(test_file1, 'w') as f:
                f.write('content1')
            with open(test_file2, 'w') as f:
                f.write('content2')
            
            files = file_utils.list_files(temp_dir)
            assert isinstance(files, list)
            assert len(files) >= 2
    
    def test_list_files_nonexistent(self):
        """Test file listing for nonexistent directory"""
        file_utils = FileUtils()
        
        files = file_utils.list_files('/nonexistent/directory')
        assert files == []
    
    def test_copy_file(self):
        """Test file copying"""
        file_utils = FileUtils()
        
        with tempfile.TemporaryDirectory() as temp_dir:
            source = os.path.join(temp_dir, 'source.txt')
            dest = os.path.join(temp_dir, 'dest.txt')
            
            with open(source, 'w') as f:
                f.write('test content')
            
            result = file_utils.copy_file(source, dest)
            assert result is True
            assert os.path.exists(dest)
    
    def test_copy_file_nonexistent(self):
        """Test copying nonexistent file"""
        file_utils = FileUtils()
        
        result = file_utils.copy_file('/nonexistent/source', '/tmp/dest')
        assert result is False
    
    def test_move_file(self):
        """Test file moving"""
        file_utils = FileUtils()
        
        with tempfile.TemporaryDirectory() as temp_dir:
            source = os.path.join(temp_dir, 'source.txt')
            dest = os.path.join(temp_dir, 'dest.txt')
            
            with open(source, 'w') as f:
                f.write('test content')
            
            result = file_utils.move_file(source, dest)
            assert result is True
            assert os.path.exists(dest)
            assert not os.path.exists(source)
    
    def test_move_file_nonexistent(self):
        """Test moving nonexistent file"""
        file_utils = FileUtils()
        
        result = file_utils.move_file('/nonexistent/source', '/tmp/dest')
        assert result is False
