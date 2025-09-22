# Configuration: logging, API endpoints, hardware targets
import os

LOG_FILE = os.getenv("LOG_FILE", "acmecli.log")
LOG_LEVEL = int(os.getenv("LOG_LEVEL", 0))

HARDWARE_TARGETS = ["raspberry_pi", "jetson_nano", "desktop_pc", "aws_server"]

# Net score weights (modifiable)
METRIC_WEIGHTS = {
    "ramp_up_time": 0.15,
    "bus_factor": 0.15,
    "performance_claims": 0.2,
    "license": 0.1,
    "size_score": 0.1,
    "dataset_and_code_score": 0.1,
    "dataset_quality": 0.1,
    "code_quality": 0.1
}
