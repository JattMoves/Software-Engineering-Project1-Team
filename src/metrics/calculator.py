# src/metrics/calculator.py
"""
Main metrics calculator that coordinates all metric calculations
"""

import time
import json
import tempfile
import os
import shutil
from typing import Dict, Any, Optional
from concurrent.futures import ThreadPoolExecutor, as_completed
import multiprocessing

from ..models.model import ModelInfo, MetricResult
from ..utils.logger import setup_logger
from .license_metric import LicenseMetric
from .size_metric import SizeMetric
from .rampup_metric import RampUpMetric
from .busfactor_metric import BusFactorMetric
from .performance_metric import PerformanceMetric
from .dataset_code_metric import DatasetCodeMetric
from .dataset_quality_metric import DatasetQualityMetric
from .code_quality_metric import CodeQualityMetric

class MetricsCalculator:
    """Coordinates calculation of all metrics for a model"""
    
    def __init__(self):
        self.logger = setup_logger()
        self.max_workers = min(8, multiprocessing.cpu_count())
        
        # Initialize metric calculators
        self.license_metric = LicenseMetric()
        self.size_metric = SizeMetric()
        self.rampup_metric = RampUpMetric()
        self.busfactor_metric = BusFactorMetric()
        self.performance_metric = PerformanceMetric()
        self.dataset_code_metric = DatasetCodeMetric()
        self.dataset_quality_metric = DatasetQualityMetric()
        self.code_quality_metric = CodeQualityMetric()
    
    def calculate_all_metrics(self, model_info: ModelInfo) -> Dict[str, Any]:
        """Calculate all metrics for a model in parallel"""
        
        metrics = {}
        metric_tasks = []
        
        # Define all metric calculation tasks
        tasks = [
            ('license', self.license_metric.calculate, model_info),
            ('size_score', self.size_metric.calculate, model_info),
            ('ramp_up_time', self.rampup_metric.calculate, model_info),
            ('bus_factor', self.busfactor_metric.calculate, model_info),
            ('performance_claims', self.performance_metric.calculate, model_info),
            ('dataset_and_code_score', self.dataset_code_metric.calculate, model_info),
            ('dataset_quality', self.dataset_quality_metric.calculate, model_info),
            ('code_quality', self.code_quality_metric.calculate, model_info),
        ]
        
        # Execute metrics in parallel
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            future_to_metric = {
                executor.submit(self._calculate_metric_with_timing, task[1], task[2]): task[0] 
                for task in tasks
            }
            
            for future in as_completed(future_to_metric):
                metric_name = future_to_metric[future]
                try:
                    result = future.result()
                    if metric_name == 'size_score':
                        # Special handling for size score which returns a dict
                        metrics[metric_name] = result['value']
                        metrics[f"{metric_name}_latency"] = result['latency_ms']
                    else:
                        metrics[metric_name] = result.value
                        metrics[f"{metric_name}_latency"] = result.latency_ms
                except Exception as e:
                    self.logger.error(f"Failed to calculate {metric_name}: {str(e)}")
                    # Provide default values on failure
                    if metric_name == 'size_score':
                        metrics[metric_name] = {
                            "raspberry_pi": 0.0,
                            "jetson_nano": 0.0,
                            "desktop_pc": 0.5,
                            "aws_server": 1.0
                        }
                    else:
                        metrics[metric_name] = 0.0
                    metrics[f"{metric_name}_latency"] = 1000  # 1 second default
        
        # Calculate net score
        net_score_start = time.time()
        net_score = self._calculate_net_score(metrics)
        net_score_latency = max(1, int((time.time() - net_score_start) * 1000))
        
        # Build final result
        result = {
            "name": model_info.name,
            "category": "MODEL",
            "net_score": net_score,
            "net_score_latency": net_score_latency,
            "ramp_up_time": metrics.get("ramp_up_time", 0.0),
            "ramp_up_time_latency": metrics.get("ramp_up_time_latency", 1000),
            "bus_factor": metrics.get("bus_factor", 0.0),
            "bus_factor_latency": metrics.get("bus_factor_latency", 1000),
            "performance_claims": metrics.get("performance_claims", 0.0),
            "performance_claims_latency": metrics.get("performance_claims_latency", 1000),
            "license": metrics.get("license", 0.0),
            "license_latency": metrics.get("license_latency", 1000),
            "size_score": metrics.get("size_score", {
                "raspberry_pi": 0.0,
                "jetson_nano": 0.0,
                "desktop_pc": 0.5,
                "aws_server": 1.0
            }),
            "size_score_latency": metrics.get("size_score_latency", 1000),
            "dataset_and_code_score": metrics.get("dataset_and_code_score", 0.0),
            "dataset_and_code_score_latency": metrics.get("dataset_and_code_score_latency", 1000),
            "dataset_quality": metrics.get("dataset_quality", 0.0),
            "dataset_quality_latency": metrics.get("dataset_quality_latency", 1000),
            "code_quality": metrics.get("code_quality", 0.0),
            "code_quality_latency": metrics.get("code_quality_latency", 1000)
        }
        
        return result
    
    def _calculate_metric_with_timing(self, metric_func, model_info: ModelInfo):
        """Calculate a metric and measure its execution time"""
        start_time = time.time()
        try:
            result_value = metric_func(model_info)
            end_time = time.time()
            latency_ms = int((end_time - start_time) * 1000)
            
            if isinstance(result_value, dict):
                # For size_score which returns a dict
                return {
                    'value': result_value,
                    'latency_ms': latency_ms
                }
            else:
                return MetricResult(value=result_value, latency_ms=latency_ms)
        except Exception as e:
            end_time = time.time()
            latency_ms = int((end_time - start_time) * 1000)
            self.logger.error(f"Metric calculation failed: {str(e)}")
            return MetricResult(value=0.0, latency_ms=latency_ms)
    
    def _calculate_net_score(self, metrics: Dict[str, Any]) -> float:
        """Calculate weighted net score based on Sarah's priorities"""
        
        # Weights based on Sarah's priorities
        # She cares about: documentation quality, responsiveness, dataset/code availability
        weights = {
            'license': 0.15,           # Legal compliance is important
            'ramp_up_time': 0.20,      # Easy adoption is key priority  
            'bus_factor': 0.10,        # Maintainer responsiveness
            'performance_claims': 0.15, # Evidence of quality
            'dataset_and_code_score': 0.20, # Key requirement
            'dataset_quality': 0.10,   # Data quality matters
            'code_quality': 0.10       # Code maintainability
            # size_score not included in net score as it's hardware-specific
        }
        
        total_score = 0.0
        total_weight = 0.0
        
        for metric, weight in weights.items():
            if metric in metrics and isinstance(metrics[metric], (int, float)):
                total_score += metrics[metric] * weight
                total_weight += weight
        
        if total_weight == 0:
            return 0.0
        
        return min(1.0, max(0.0, total_score / total_weight))