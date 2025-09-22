# Resource dataclass (model/dataset/code)
from dataclasses import dataclass, field
from typing import Dict

@dataclass
class Resource:
    name: str
    category: str  # MODEL, DATASET, CODE
    net_score: float = 0.0
    net_score_latency: int = 0
    ramp_up_time: float = 0.0
    ramp_up_time_latency: int = 0
    bus_factor: float = 0.0
    bus_factor_latency: int = 0
    performance_claims: float = 0.0
    performance_claims_latency: int = 0
    license: float = 0.0
    license_latency: int = 0
    size_score: Dict[str, float] = field(default_factory=dict)
    size_score_latency: int = 0
    dataset_and_code_score: float = 0.0
    dataset_and_code_score_latency: int = 0
    dataset_quality: float = 0.0
    dataset_quality_latency: int = 0
    code_quality: float = 0.0
    code_quality_latency: int = 0

    def to_ndjson(self) -> str:
        import json
        return json.dumps(self.__dict__)
