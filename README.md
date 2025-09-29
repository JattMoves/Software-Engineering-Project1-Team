# ML Model Evaluator

Ever wondered if that shiny new ML model from Hugging Face is actually worth using in your project? This tool helps you figure that out by analyzing models across multiple dimensions that actually matter for real-world deployment.

## What This Tool Does

We built this for ACME Corporation's engineering teams to evaluate pre-trained ML models before committing to using them. Instead of just looking at model performance, we analyze the stuff that really matters when you're trying to ship something to production:

### The Metrics We Care About
- **License Compatibility**: Can you actually use this model legally in your project?
- **Model Size**: Will this thing fit on your hardware or do you need a data center?
- **Ramp-up Time**: How much documentation exists? Can your team actually figure out how to use it?
- **Bus Factor**: What happens if the maintainer gets hit by a bus? Is this project sustainable?
- **Performance Claims**: Are there actual benchmarks backing up the claims, or is it all marketing?
- **Dataset & Code Availability**: Can you retrain this if needed? Is the training code available?
- **Dataset Quality**: How good is the data this model was trained on?
- **Code Quality**: Is the implementation actually maintainable?

### Why This Matters
- ✅ **122 test cases** that actually work (we've tested them!)
- ✅ **Runs fast** - parallel processing means you're not waiting around
- ✅ **Easy to integrate** - outputs clean JSON that your other tools can consume
- ✅ **Actually helpful logging** - you can see what's happening under the hood
- ✅ **Works with real APIs** - connects to GitHub and Hugging Face to get real data
- ✅ **Handles errors gracefully** - won't crash when the internet is being weird

## Getting Started

### What You Need
- Python 3.8+ (we're not living in the stone age)
- Git (for cloning repos)
- Internet connection (the tool needs to fetch model info)

### Quick Setup
```bash
# Get the code
git clone <repository-url>
cd Software-Engineering-Project1-Team

# Install everything you need
./run install
```

### Manual Installation (if you prefer)
```bash
pip install -r requirements.txt
```

## How to Use It

### Evaluating Models

Just point it at a file with URLs:

```bash
./run your_urls.txt
```

The URL file should have one URL per line. We support:
- Hugging Face models: `https://huggingface.co/username/model-name`
- Hugging Face datasets: `https://huggingface.co/datasets/username/dataset-name`  
- GitHub repos: `https://github.com/username/repository-name`

**Example file:**
```
https://huggingface.co/google/gemma-3-270m
https://huggingface.co/datasets/xlangai/AgentNet  
https://github.com/SkyworkAI/Matrix-Game
```

### Running Tests

```bash
# Run all tests (this is what the autograder does)
./run test

# Or if you want to see what's happening
python -m pytest tests/ -v

# Check test coverage
python -m pytest tests/ --cov=src --cov-report=term-missing
```

**Our test results:**
- **122 test cases** that actually pass
- **80% code coverage** (we're not just testing the happy path)
- **Runs in ~4 seconds** (nobody likes slow tests)
- **Handles edge cases** (because real data is messy)

## What You Get

The tool spits out JSON (one line per model) with scores from 0-1. Higher is better, obviously.

### The Important Stuff
- `name`: What model this is
- `category`: Always "MODEL" (we're not evaluating datasets or code repos for the final score)
- `net_score`: The overall "should I use this?" score

### Individual Scores (0-1, where 1 is perfect)
- `ramp_up_time`: How easy is it to get started?
- `bus_factor`: How sustainable is this project?
- `performance_claims`: Are there real benchmarks or just marketing?
- `license`: Can you actually use this legally?
- `size_score`: Will this fit on your hardware? (includes scores for different platforms)
- `dataset_and_code_score`: Can you retrain this if needed?
- `dataset_quality`: How good is the training data?
- `code_quality`: Is the code actually maintainable?

### Performance Info
Each metric also includes a `*_latency` field showing how long it took to calculate (in milliseconds). Useful for debugging slow evaluations.

### Real Example
```json
{
  "name": "bert-base-uncased",
  "category": "MODEL", 
  "net_score": 0.80,
  "ramp_up_time": 1.0,
  "bus_factor": 1.0,
  "performance_claims": 0.7,
  "license": 1.0,
  "size_score": {"raspberry_pi": 0.0, "jetson_nano": 0.8, "desktop_pc": 1.0, "aws_server": 1.0},
  "dataset_and_code_score": 0.56,
  "dataset_quality": 0.535,
  "code_quality": 0.8,
  "ramp_up_time_latency": 862,
  "bus_factor_latency": 0,
  "performance_claims_latency": 727,
  "license_latency": 727,
  "size_score_latency": 710,
  "dataset_and_code_score_latency": 1019,
  "dataset_quality_latency": 1044,
  "code_quality_latency": 1047
}
```

## Configuration (Optional)

You can set some environment variables if you want more control:

- `LOG_LEVEL`: 0 (quiet), 1 (normal), 2 (verbose debugging)
- `LOG_FILE`: Where to save logs (if you want them)
- `GITHUB_TOKEN`: Your GitHub token (for private repos)
- `HF_TOKEN`: Your Hugging Face token (for private models)

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
│   ├── metrics/           # All the scoring logic
│   ├── models/            # Data structures
│   ├── utils/             # Helper functions
│   └── url_parser.py      # URL parsing magic
├── tests/                 # Our test suite
├── main.py               # The main entry point
├── requirements.txt      # What you need to install
├── run                   # The script that makes everything work
└── README.md            # This file
```

## Dependencies

We use these Python packages (all in requirements.txt):
- `requests` - For talking to APIs
- `GitPython` - For git operations
- `transformers` - Hugging Face model stuff
- `torch` - PyTorch (obviously)
- `huggingface-hub` - More Hugging Face integration
- `pytest` - Testing framework
- `pytest-cov` - Coverage reporting
- `flake8` - Code linting
- `isort` - Import sorting
- `mypy` - Type checking

## Development

### Running Tests
```bash
# Run all tests
python -m pytest tests/ -v

# Check coverage
python -m pytest tests/ --cov=src --cov-report=html

# Run specific test file
python -m pytest tests/test_all_metrics_comprehensive.py -v
```

### Code Quality
```bash
# Lint the code
flake8 src/ tests/

# Sort imports
isort src/ tests/

# Type checking
mypy src/
```

## License

This project uses the GNU Lesser General Public License v2.1.