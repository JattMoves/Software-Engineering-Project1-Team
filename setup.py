from setuptools import setup, find_packages

setup(
    name="ml-model-evaluator",
    version="1.0.0",
    description="CLI tool for evaluating ML models from Hugging Face",
    packages=find_packages(),
    python_requires=">=3.8",
    install_requires=[
        "requests>=2.25.0",
        "GitPython>=3.1.0", 
        "transformers>=4.20.0",
        "torch>=1.12.0",
        "huggingface-hub>=0.15.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0", 
            "flake8>=5.0.0",
            "isort>=5.0.0",
            "mypy>=1.0.0",
        ]
    },
    entry_points={
        "console_scripts": [
            "ml-evaluator=main:main",
        ],
    },
)