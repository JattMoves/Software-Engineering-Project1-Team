# tests/test_main.py
"""
Tests for main application logic
"""

import pytest
import tempfile
import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from main import MLEvaluator

class TestMLEvaluator:
    
    def setup_method(self):
        self.evaluator = MLEvaluator()
    
    def test_evaluator_initialization(self):
        """Test MLEvaluator initializes correctly"""
        assert self.evaluator.config is not None
        assert self.evaluator.url_parser is not None
        assert self.evaluator.metrics_calculator is not None
    
    def test_process_empty_file(self):
        """Test processing empty URL file"""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, encoding='ascii') as f:
            f.write("")
            temp_path = f.name
        
        try:
            result = self.evaluator.process_urls_file(temp_path)
            assert result == 0  # Should succeed with empty file
        finally:
            os.unlink(temp_path)
    
    def test_process_nonexistent_file(self):
        """Test processing non-existent file"""
        result = self.evaluator.process_urls_file("nonexistent_file.txt")
        assert result == 1  # Should fail
    
    def test_process_sample_urls(self):
        """Test processing sample URLs"""
        urls = [
            "https://huggingface.co/google/gemma-3-270m\n",
            "https://huggingface.co/datasets/xlangai/AgentNet\n",
            "https://github.com/SkyworkAI/Matrix-Game\n"
        ]
        
        with tempfile.NamedTemporaryFile(mode='w', delete=False, encoding='ascii') as f:
            f.writelines(urls)
            temp_path = f.name
        
        try:
            result = self.evaluator.process_urls_file(temp_path)
            assert result == 0  # Should succeed
        finally:
            os.unlink(temp_path)