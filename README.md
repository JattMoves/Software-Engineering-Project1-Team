# ML Model Evaluator

A CLI tool for evaluating machine learning models from Hugging Face Hub based on various quality metrics.

## Overview

This tool helps ACME Corporation's engineering teams evaluate pre-trained ML models for reuse by analyzing:
- License compatibility
- Model size and hardware requirements  
- Documentation quality and ramp-up time
- Maintainer responsiveness (bus factor)
- Performance claims and benchmarks
- Dataset and code availability
- Overall code and dataset quality

## Installation

```bash
./run install
```

## Usage

### Evaluate Models

```bash
./run URL_FILE
```

Where `URL_FILE` contains newline-delimited URLs of models, datasets, or code repositories.

Example URL file:
```
https://huggingface.co/google/gemma-3-270m
https://huggingface.co/datasets/xlangai/AgentNet  
https://github.com/SkyworkAI/Matrix-Game
```

### Run Tests

```bash
./run test
```

## Output Format

The tool outputs NDJSON (newline-delimited JSON) with the following fields for each model:

- `name`: Model name
- `category`: Always "MODEL" 
- `net_score`: Overall quality score (0-1)
- `ramp_up_time`: Ease of getting started (0-1)
- `bus_factor`: Maintainer responsiveness (0-1) 
- `performance_claims`: Evidence of benchmarks (0-1)
- `license`: License compatibility score (0-1)
- `size_score`: Hardware compatibility scores
- `dataset_and_code_score`: Availability of training data/code (0-1)
- `dataset_quality`: Quality of training datasets (0-1)
- `code_quality`: Code maintainability score (0-1)

Each metric includes a corresponding `*_latency` field with calculation time in milliseconds.

## Configuration

Set environment variables:
- `LOG_LEVEL`: 0 (silent), 1 (info), 2 (debug)
- `LOG_FILE`: Path for log output
- `GITHUB_TOKEN`: GitHub API token (optional)
- `HF_TOKEN`: Hugging Face API token (optional)

## License

This project uses the GNU Lesser General Public License v2.1.