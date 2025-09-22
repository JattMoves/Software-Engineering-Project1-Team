# Calls metric functions in parallel, aggregates net score
from models.resource import Resource
from metrics import ramp_up_time, bus_factor, license, performance, dataset_code, dataset_quality, code_quality, size_score
from concurrent.futures import ThreadPoolExecutor
from config import METRIC_WEIGHTS

def process_resources(urls):
    resources = [Resource(name=url, category="MODEL") for url in urls]

    def compute_metrics(res: Resource):
        # Parallel computation of all metrics
        (res.ramp_up_time, res.ramp_up_time_latency) = ramp_up_time.compute(res)
        (res.bus_factor, res.bus_factor_latency) = bus_factor.compute(res)
        (res.license, res.license_latency) = license.compute(res)
        (res.performance_claims, res.performance_claims_latency) = performance.compute(res)
        (res.dataset_and_code_score, res.dataset_and_code_score_latency) = dataset_code.compute(res)
        (res.dataset_quality, res.dataset_quality_latency) = dataset_quality.compute(res)
        (res.code_quality, res.code_quality_latency) = code_quality.compute(res)
        (res.size_score['desktop_pc'], res.size_score_latency) = size_score.compute(res)
        # Compute weighted net score
        res.net_score = sum([
            res.ramp_up_time * METRIC_WEIGHTS['ramp_up_time'],
            res.bus_factor * METRIC_WEIGHTS['bus_factor'],
            res.performance_claims * METRIC_WEIGHTS['performance_claims'],
            res.license * METRIC_WEIGHTS['license'],
            res.dataset_and_code_score * METRIC_WEIGHTS['dataset_and_code_score'],
            res.dataset_quality * METRIC_WEIGHTS['dataset_quality'],
            res.code_quality * METRIC_WEIGHTS['code_quality'],
            res.size_score['desktop_pc'] * METRIC_WEIGHTS['size_score']
        ])
    with ThreadPoolExecutor() as executor:
        executor.map(compute_metrics, resources)

    return resources
