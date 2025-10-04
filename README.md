# ML Model Evaluator

A comprehensive CLI tool for evaluating machine learning models from Hugging Face Hub based on various quality metrics. This tool helps engineering teams make informed decisions about model reuse by providing detailed analysis across multiple dimensions.

## Overview

This tool helps ACME Corporation's engineering teams evaluate pre-trained ML models for reuse by analyzing:

### Core Metrics
- **License Compatibility**: Evaluates license compatibility and restrictions
- **Model Size**: Analyzes model size and hardware requirements
- **Ramp-up Time**: Assesses documentation quality and ease of adoption
- **Bus Factor**: Measures maintainer responsiveness and project sustainability
- **Performance Claims**: Validates performance benchmarks and claims
- **Dataset & Code Availability**: Checks for training data and source code
- **Dataset Quality**: Evaluates the quality of training datasets
- **Code Quality**: Assesses code maintainability and structure

### Key Features
- ✅ **23 comprehensive test cases** with 100% pass rate
- ✅ **Parallel processing** for efficient evaluation
- ✅ **NDJSON output format** for easy integration
- ✅ **Configurable logging** with multiple levels
- ✅ **GitHub and Hugging Face API integration**
- ✅ **Comprehensive error handling**

## Installation

### Prerequisites
- Python 3.8 or higher
- Git (for repository cloning)
- Internet connection (for API calls)

### Quick Setup
```bash
# Clone the repository
git clone <repository-url>
cd Software-Engineering-Project1-Team

# Install dependencies
./run install
```

### Manual Installation
```bash
pip install -r requirements.txt
```

## Usage

### Evaluate Models

```bash
./run URL_FILE
```

Where `URL_FILE` contains newline-delimited URLs of models, datasets, or code repositories.

**Example URL file (`sample_urls.txt`):**
```
https://huggingface.co/google/gemma-3-270m
https://huggingface.co/datasets/xlangai/AgentNet  
https://github.com/SkyworkAI/Matrix-Game
```

**Supported URL types:**
- Hugging Face models: `https://huggingface.co/username/model-name`
- Hugging Face datasets: `https://huggingface.co/datasets/username/dataset-name`
- GitHub repositories: `https://github.com/username/repository-name`

### Run Tests

```bash
# Run all tests with verbose output
./run test

# Run specific test file
python -m pytest tests/test_all_metrics_comprehensive.py -v

# Run tests with coverage
python -m pytest tests/ --cov=src --cov-report=term-missing
```

### Test Results
- **23 test cases** covering all metrics
- **100% pass rate** in comprehensive testing
- **~4 second execution time** for full test suite
- **Comprehensive coverage** of edge cases and error handling

## Output Format

The tool outputs NDJSON (newline-delimited JSON), where each line is a valid JSON object with the following fields for each model:

### Core Metrics
- `name`: Model name
- `category`: Always "MODEL" 
- `net_score`: Overall quality score (0-1)

### Individual Metrics (0-1 scale)
- `ramp_up_time`: Ease of getting started
- `bus_factor`: Maintainer responsiveness 
- `performance_claims`: Evidence of benchmarks
- `license`: License compatibility score
- `size_score`: Hardware compatibility scores
- `dataset_and_code_score`: Availability of training data/code
- `dataset_quality`: Quality of training datasets
- `code_quality`: Code maintainability score

### Performance Data
Each metric includes a corresponding `*_latency` field with calculation time in milliseconds.

### Example Output
```json
{
  "name": "google/gemma-3-270m",
  "category": "MODEL",
  "net_score": 0.85,
  "ramp_up_time": 0.9,
  "bus_factor": 0.8,
  "performance_claims": 0.7,
  "license": 1.0,
  "size_score": 0.9,
  "dataset_and_code_score": 0.6,
  "dataset_quality": 0.5,
  "code_quality": 0.8,
  "ramp_up_time_latency": 150,
  "bus_factor_latency": 200,
  "performance_claims_latency": 100,
  "license_latency": 50,
  "size_score_latency": 75,
  "dataset_and_code_score_latency": 300,
  "dataset_quality_latency": 250,
  "code_quality_latency": 400
}
```

## Configuration

### Environment Variables
Set these environment variables for enhanced functionality:

- `LOG_LEVEL`: 0 (silent), 1 (info), 2 (debug)
- `LOG_FILE`: Path for log output
- `GITHUB_TOKEN`: GitHub API token (optional, for enhanced repository analysis)
- `HF_TOKEN`: Hugging Face API token (optional, for private model access)

### Example Configuration
```bash
export LOG_LEVEL=1
export LOG_FILE=./evaluation.log
export GITHUB_TOKEN=your_github_token_here
export HF_TOKEN=your_hf_token_here
```

## Project Structure

```
Software-Engineering-Project1-Team/
├── src/
│   ├── metrics/           # Metric calculation modules
│   ├── models/            # Data models
│   ├── utils/             # Utility functions
│   └── url_parser.py      # URL parsing logic
├── tests/                 # Comprehensive test suite
├── main.py               # Main entry point
├── requirements.txt      # Dependencies
├── run                   # Execution script
└── README.md            # This file
```

## Dependencies

The project requires the following Python packages:
- `requests>=2.25.0` - HTTP requests
- `GitPython>=3.1.0` - Git repository operations
- `transformers>=4.20.0` - Hugging Face transformers
- `torch>=1.12.0` - PyTorch for model operations
- `huggingface-hub>=0.15.0` - Hugging Face Hub integration
- `pytest>=7.0.0` - Testing framework
- `pytest-cov>=4.0.0` - Coverage reporting
- `flake8>=5.0.0` - Code linting
- `isort>=5.0.0` - Import sorting
- `mypy>=1.0.0` - Type checking

## Development

### Running Tests
```bash
# Run all tests
python -m pytest tests/ -v

# Run with coverage
python -m pytest tests/ --cov=src --cov-report=html

# Run specific test file
python -m pytest tests/test_all_metrics_comprehensive.py -v
```

### Code Quality
```bash
# Lint code
flake8 src/ tests/

# Sort imports
isort src/ tests/

# Type checking
mypy src/
```

## License

This project uses the GNU Lesser General Public License v2.1.