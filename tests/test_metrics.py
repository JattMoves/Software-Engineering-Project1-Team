# tests/test_metrics.py
"""
Tests for metrics calculation
"""

import pytest
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.metrics.calculator import MetricsCalculator
from src.metrics.license_metric import LicenseMetric
from src.metrics.size_metric import SizeMetric
from src.models.model import ModelInfo

class TestMetrics:
    
    def setup_method(self):
        self.calculator = MetricsCalculator()
        self.license_metric = LicenseMetric()
        self.size_metric = SizeMetric()
    
    def test_license_metric_known_license(self):
        """Test license metric with known license"""
        model_info = ModelInfo(
            name="test/model",
            url="https://huggingface.co/test/model",
            api_data={"license": "apache-2.0"}
        )
        score = self.license_metric.calculate(model_info)
        assert 0.0 <= score <= 1.0
        assert score > 0.5  # Apache 2.0 should score well
    
    def test_license_metric_unknown_license(self):
        """Test license metric with unknown license"""
        model_info = ModelInfo(
            name="test/model", 
            url="https://huggingface.co/test/model",
            api_data={}
        )
        score = self.license_metric.calculate(model_info)
        assert 0.0 <= score <= 1.0
    
    def test_size_metric_calculation(self):
        """Test size metric calculation"""
        model_info = ModelInfo(
            name="test/small-model",
            url="https://huggingface.co/test/small-model", 
            api_data={}
        )
        scores = self.size_metric.calculate(model_info)
        assert isinstance(scores, dict)
        assert "raspberry_pi" in scores
        assert "aws_server" in scores
        for score in scores.values():
            assert 0.0 <= score <= 1.0
    
    def test_metrics_calculator_structure(self):
        """Test metrics calculator returns proper structure"""
        model_info = ModelInfo(
            name="test/model",
            url="https://huggingface.co/test/model",
            api_data={}
        )
        result = self.calculator.calculate_all_metrics(model_info)
        
        # Check required fields
        required_fields = [
            "name", "category", "net_score", "net_score_latency",
            "ramp_up_time", "ramp_up_time_latency",
            "bus_factor", "bus_factor_latency", 
            "performance_claims", "performance_claims_latency",
            "license", "license_latency",
            "size_score", "size_score_latency",
            "dataset_and_code_score", "dataset_and_code_score_latency",
            "dataset_quality", "dataset_quality_latency",
            "code_quality", "code_quality_latency"
        ]
        
        for field in required_fields:
            assert field in result
        
        assert result["category"] == "MODEL"
        assert 0.0 <= result["net_score"] <= 1.0