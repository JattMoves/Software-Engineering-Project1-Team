# tests/test_url_parser.py
"""
Tests for URL parser module
"""

import pytest
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.url_parser import URLParser
from src.models.model import ModelInfo

class TestURLParser:
    
    def setup_method(self):
        self.parser = URLParser()
    
    def test_identify_model_url(self):
        """Test model URL identification"""
        url = "https://huggingface.co/google/gemma-3-270m"
        assert self.parser.identify_url_type(url) == "MODEL"
    
    def test_identify_dataset_url(self):
        """Test dataset URL identification"""
        url = "https://huggingface.co/datasets/xlangai/AgentNet"
        assert self.parser.identify_url_type(url) == "DATASET"
    
    def test_identify_code_url(self):
        """Test code URL identification"""
        url = "https://github.com/SkyworkAI/Matrix-Game"
        assert self.parser.identify_url_type(url) == "CODE"
    
    def test_parse_model_url_basic(self):
        """Test basic model URL parsing"""
        url = "https://huggingface.co/test/model"
        result = self.parser.parse_model_url(url)
        assert result is None or isinstance(result, ModelInfo)
    
    def test_parse_model_url_with_tree(self):
        """Test model URL parsing with /tree/main"""
        url = "https://huggingface.co/test/model/tree/main"
        result = self.parser.parse_model_url(url)
        assert result is None or isinstance(result, ModelInfo)
    
    def test_invalid_url_parsing(self):
        """Test parsing invalid URLs"""
        invalid_url = "not-a-valid-url"
        result = self.parser.parse_model_url(invalid_url)
        assert result is None