# src/models/model.py
"""
Data models for different types of resources
"""

from dataclasses import dataclass
from typing import Dict, Any, List, Optional

@dataclass
class ModelInfo:
    """Information about a machine learning model"""
    name: str
    url: str
    api_data: Dict[str, Any]
    downloads: int = 0
    likes: int = 0
    last_modified: str = ""
    tags: List[str] = None
    pipeline_tag: str = ""
    library_name: str = ""
    model_index: List[Dict] = None
    
    def __post_init__(self):
        if self.tags is None:
            self.tags = []
        if self.model_index is None:
            self.model_index = []

@dataclass 
class DatasetInfo:
    """Information about a dataset"""
    name: str
    url: str
    api_data: Dict[str, Any]
    downloads: int = 0
    likes: int = 0
    tags: List[str] = None
    
    def __post_init__(self):
        if self.tags is None:
            self.tags = []

@dataclass
class CodeInfo:
    """Information about a code repository"""
    name: str
    url: str
    api_data: Dict[str, Any]
    stars: int = 0
    forks: int = 0
    language: str = ""
    last_updated: str = ""

@dataclass
class MetricResult:
    """Result of a metric calculation"""
    value: float
    latency_ms: int
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'value': self.value,
            'latency_ms': self.latency_ms
        }