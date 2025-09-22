# dataset_code metric
from models.resource import Resource
from utils.timing import measure_latency
import random

@measure_latency
def compute(resource: Resource) -> float:
    return random.uniform(0, 1)
