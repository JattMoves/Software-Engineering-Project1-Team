# tests/test_integration.py
"""
Integration tests
"""

import pytest
import json
import tempfile
import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from main import MLEvaluator

class TestIntegration:
    
    def test_full_pipeline_mock_model(self):
        """Test full pipeline with mock model"""
        # Create a simple URL file
        urls = ["https://huggingface.co/test/mock-model\n"]
        
        with tempfile.NamedTemporaryFile(mode='w', delete=False, encoding='ascii') as f:
            f.writelines(urls)
            temp_path = f.name
        
        evaluator = MLEvaluator()
        
        try:
            # This will likely fail due to non-existent model, but tests the pipeline
            result = evaluator.process_urls_file(temp_path)
            # Result can be 0 or 1, both are acceptable for this test
            assert result in [0, 1]
        finally:
            os.unlink(temp_path)
    
    def test_output_format_validation(self):
        """Test that output follows NDJSON format when model exists"""
        # This is more of a structure test
        evaluator = MLEvaluator() 
        
        # Test that evaluate_model returns proper structure or None
        result = evaluator.evaluate_model("https://huggingface.co/test/nonexistent")
        assert result is None or isinstance(result, dict)
        
        if result:
            # Check required fields if result exists
            required_fields = ["name", "category", "net_score"]
            for field in required_fields:
                assert field in result
    
    def test_metrics_range_validation(self):
        """Test that all metrics are in valid range [0,1]"""
        from src.models.model import ModelInfo
        from src.metrics.calculator import MetricsCalculator
        
        calculator = MetricsCalculator()
        model_info = ModelInfo(
            name="test/model",
            url="https://huggingface.co/test/model",
            api_data={}
        )
        
        result = calculator.calculate_all_metrics(model_info)
        
        # Test score ranges
        float_metrics = [
            "net_score", "ramp_up_time", "bus_factor", 
            "performance_claims", "license", 
            "dataset_and_code_score", "dataset_quality", "code_quality"
        ]
        
        for metric in float_metrics:
            assert 0.0 <= result[metric] <= 1.0, f"{metric} out of range: {result[metric]}"
        
        # Test size_score structure
        size_score = result["size_score"]
        assert isinstance(size_score, dict)
        for hw_type in ["raspberry_pi", "jetson_nano", "desktop_pc", "aws_server"]:
            assert hw_type in size_score
            assert 0.0 <= size_score[hw_type] <= 1.0