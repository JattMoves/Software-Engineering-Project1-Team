# tests/test_models.py
"""
Tests for data models
"""

import pytest
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.models.model import ModelInfo, DatasetInfo, CodeInfo, MetricResult

class TestModels:
    
    def test_model_info_creation(self):
        """Test ModelInfo creation"""
        model = ModelInfo(
            name="test/model",
            url="https://huggingface.co/test/model",
            api_data={"test": "data"}
        )
        assert model.name == "test/model"
        assert model.url == "https://huggingface.co/test/model"
        assert model.api_data == {"test": "data"}
        assert model.tags == []  # Default empty list
    
    def test_dataset_info_creation(self):
        """Test DatasetInfo creation"""
        dataset = DatasetInfo(
            name="test/dataset",
            url="https://huggingface.co/datasets/test/dataset",
            api_data={}
        )
        assert dataset.name == "test/dataset"
        assert dataset.tags == []
    
    def test_code_info_creation(self):
        """Test CodeInfo creation"""
        code = CodeInfo(
            name="user/repo",
            url="https://github.com/user/repo", 
            api_data={}
        )
        assert code.name == "user/repo"
        assert code.stars == 0
    
    def test_metric_result_to_dict(self):
        """Test MetricResult serialization"""
        result = MetricResult(value=0.8, latency_ms=1500)
        data = result.to_dict()
        assert data == {"value": 0.8, "latency_ms": 1500}