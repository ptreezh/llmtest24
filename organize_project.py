#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
LLM Advanced Testing Suite - Project Organization Script
This script organizes the project for open source release.
"""

import os
import shutil
import json
from pathlib import Path
import subprocess

def print_header():
    """Print organization header"""
    print("=" * 60)
    print("LLM Advanced Testing Suite - Project Organization")
    print("=" * 60)
    print()

def create_readme():
    """Create comprehensive README"""
    print("Creating comprehensive README...")
    
    readme_content = """# LLM Advanced Testing Suite

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Code Style: Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

A comprehensive testing framework for evaluating Large Language Models (LLMs) across advanced cognitive capabilities, particularly their potential as "cognitive engines".

## Overview

This project provides a systematic approach to assess LLM capabilities through 25 structured test pillars, ranging from fundamental reasoning to cutting-edge cognitive ecosystem behaviors. The framework is designed for researchers, developers, and organizations to evaluate and compare LLM performance across multiple dimensions.

## Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/ptreezh/llmtest24.git
cd llmtest24

# Install dependencies
pip install -r requirements.txt

# Set up environment
cp config/.env.example config/.env
# Edit config/.env with your API keys and model configurations
```

### Basic Usage

```bash
# Run all tests for a specific model
python scripts/main_orchestrator.py --model your_model_name

# Run specific test pillars
python scripts/main_orchestrator.py --model your_model_name --test test_pillar_01_logic.py test_pillar_02_instruction.py

# Run independence tests
python run_pillar_25_independence.py

# Run cognitive ecosystem tests
python scripts/testing/run_cognitive_ecosystem_cloud_test.py
```

## Test Framework Architecture

### 25 Test Pillars

The framework is organized into 4 layers:

1. **Foundation Layer (Pillars 1-8)**
   - Logic reasoning, instruction following, structural operations
   - Long context processing, domain knowledge, tool usage
   - Planning, metacognition, creativity, safety

2. **Advanced Layer (Pillars 9-19)**
   - Role playing, multi-role collaboration, task graph generation
   - Fault tolerance, workflow management, network analysis
   - Massive consensus, dynamic role switching

3. **Cutting-Edge Layer (Pillars 20-24)**
   - Project management, parallel task optimization
   - Multidisciplinary decomposition, cognitive ecosystem

4. **Cognitive Ecosystem (Pillar 25)**
   - Role independence, cognitive diversity, collective intelligence

### Key Features

- **Multi-Model Support**: Compatible with OpenAI, Anthropic, Google, Ollama, and other model providers
- **Comprehensive Metrics**: Quantitative and qualitative evaluation across multiple dimensions
- **Scientific Methodology**: Hypothesis-driven testing with controlled variables
- **Extensible Design**: Modular architecture for adding new test capabilities
- **Rich Analytics**: Detailed reporting and visualization of test results

## Project Structure

```
llmtest24/
├── core/                    # Core testing framework
├── tests/                   # Test cases and utilities
├── independence/            # Role independence testing
├── cognitive_ecosystem/     # Cognitive ecosystem testing
├── scripts/                 # Testing scripts and utilities
├── config/                  # Configuration files
├── docs/                    # Documentation
├── results/                 # Test results and reports
├── testout/                 # Test output data
└── examples/                # Usage examples
```

## Documentation

- [Project Overview](docs/PROJECT_OVERVIEW.md)
- [Developer Guide](docs/DEVELOPER_GUIDE_EN.md)
- [Architecture Documentation](docs/PROJECT_ARCHITECTURE_EN.md)
- [User Guide](docs/USER_GUIDE_EN.md)
- [API Reference](docs/API_REFERENCE.md)
- [Quick Start Guide](docs/QUICKSTART.md)
- [Contributor Guide](CONTRIBUTOR_GUIDE.md)

## Configuration

### Environment Setup

```bash
# Copy environment template
cp config/.env.example config/.env

# Edit with your configuration
nano config/.env
```

### Model Configuration

Edit `config/models.txt` to add your model configurations:

```yaml
# Example model configuration
openai/gpt-4:
  type: openai
  api_key: ${OPENAI_API_KEY}
  base_url: https://api.openai.com/v1

local/llama2:
  type: ollama
  model_name: llama2
  base_url: http://localhost:11434
```

## Running Tests

### Single Test Execution

```bash
# Run a specific test pillar
pytest tests/test_pillar_01_logic.py

# Run with specific model
python scripts/main_orchestrator.py --model openai/gpt-4 --test test_pillar_01_logic.py

# Run independence tests
python run_pillar_25_independence.py --model your_model
```

### Batch Testing

```bash
# Run all tests for a model
python scripts/main_orchestrator.py --model your_model

# Run comprehensive tests
python run_comprehensive_tests.py

# Run cloud-based testing
python scripts/testing/run_cloud_independence_test.py
```

## Results and Analysis

Test results are automatically saved to:
- `testout/` - Raw test output data
- `results/` - Processed results and reports
- `test_reports/` - Summary reports

### Viewing Results

```bash
# View test results
python scripts/analysis/visualize_test_results.py

# Generate comprehensive report
python results/report_generator.py

# Open web interface
python visual_test_interface.py
```

## Contributing

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md) for details.

### Development Setup

```bash
# Install development dependencies
pip install -r requirements-dev.txt

# Run linting
black .
flake8 .

# Run tests
pytest
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Thanks to all contributors who have helped build this comprehensive testing framework
- Inspired by the latest research in LLM evaluation and cognitive science
- Built with the support of the AI research community

## Support

- 📧 Email: support@example.com
- 💬 Discord: [Join our community](https://discord.gg/example)
- 🐛 Issues: [GitHub Issues](https://github.com/ptreezh/llmtest24/issues)

## Roadmap

- [ ] Enhanced web interface for test management
- [ ] Real-time collaboration features
- [ ] Integration with popular MLOps platforms
- [ ] Advanced visualization and analytics
- [ ] Support for more model providers
- [ ] Automated test generation

---

Made with ❤️ by the LLM Advanced Testing Suite team
"""
    
    with open("README.md", "w", encoding="utf-8") as f:
        f.write(readme_content)
    
    print("README.md created")

def create_license():
    """Create LICENSE file"""
    print("Creating LICENSE file...")
    
    license_content = """MIT License

Copyright (c) 2025 LLM Advanced Testing Suite Team

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
    
    with open("LICENSE", "w", encoding="utf-8") as f:
        f.write(license_content)
    
    print("LICENSE file created")

def create_contributing():
    """Create CONTRIBUTING.md"""
    print("Creating CONTRIBUTING.md...")
    
    contributing_content = """# Contributing Guidelines

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md) for details.

## How to Contribute

### Reporting Bugs
- Use the GitHub Issues page to report bugs
- Provide detailed information about the issue
- Include steps to reproduce the problem
- Attach relevant logs or error messages

### Suggesting Features
- Create an issue with a clear description of the feature
- Explain the use case and expected behavior
- Discuss potential implementation approaches

### Submitting Changes

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Add tests for new functionality
5. Ensure all tests pass
6. Run linting and formatting checks
7. Commit your changes (`git commit -m 'Add amazing feature'`)
8. Push to the branch (`git push origin feature/amazing-feature`)
9. Open a Pull Request

## Development Workflow

### Prerequisites
- Python 3.8+
- Git
- Virtual environment (recommended)

### Setup Development Environment

```bash
# Clone the repository
git clone https://github.com/ptreezh/llmtest24.git
cd llmtest24

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Linux/macOS:
source venv/bin/activate
# Windows:
venv\\Scripts\\activate

# Install dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt

# Install pre-commit hooks
pre-commit install
```

### Code Style

We use several tools to maintain code quality:

- **Black**: Code formatting
- **Flake8**: Linting
- **MyPy**: Type checking

```bash
# Format code
black .

# Run linting
flake8 .

# Run type checking
mypy .
```

### Testing

We use pytest for testing:

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=. --cov-report=html

# Run specific test
pytest tests/test_pillar_01_logic.py

# Run specific test function
pytest tests/test_pillar_01_logic.py::test_logic_evaluation
```

## Project Structure

```
llmtest24/
├── core/                    # Core testing framework
├── tests/                   # Test cases
├── independence/            # Role independence testing
├── cognitive_ecosystem/     # Cognitive ecosystem testing
├── scripts/                 # Testing scripts
├── config/                  # Configuration files
├── docs/                    # Documentation
├── results/                 # Test results
└── examples/                # Usage examples
```

## Adding New Tests

### Test Structure

Each test should follow the structure:

```python
# tests/test_pillar_xx_name.py
import pytest
from tests.utils import run_single_test, print_assessment_criteria

def test_name_evaluation():
    \"\"\"Test description\"\"\"
    pillar_name = "pillar_xx"
    prompt = "Test prompt"
    model = "test_model"
    
    # Run the test
    result = run_single_test(pillar_name, prompt, model)
    
    # Assert results
    assert result['success'] is True
    assert result['score'] > 0.5
```

### Test Configuration

Add test configuration to `config/test_config.yaml`:

```yaml
test_pillar_xx:
  description: "Test description"
  criteria:
    - criterion_1
    - criterion_2
  weights:
    criterion_1: 0.5
    criterion_2: 0.5
```

### Test Implementation

Implement the test logic in the appropriate pillar file:

```python
# tests/test_pillar_xx_name.py
def run_test(pillar_name, prompt, model_name, **kwargs):
    \"\"\"Run the test\"\"\"
    # Implement test logic
    return {
        "success": True,
        "score": calculated_score,
        "details": {
            "response_quality": response_quality,
            "accuracy": accuracy,
            "completeness": completeness
        },
        "metadata": {
            "test_duration": duration,
            "tokens_used": tokens_used,
            "model_response": model_response
        }
    }
```

## Documentation

### Documentation Standards
- Use Markdown format
- Follow existing structure
- Include code examples
- Keep documentation updated with code changes

### Documentation Files
- `README.md`: Project overview
- `docs/`: Detailed documentation
- `CONTRIBUTING.md`: Contribution guidelines
- `API_REFERENCE.md`: API documentation

### Writing Documentation
- Use clear and concise language
- Include examples for complex features
- Document both usage and implementation details
- Update documentation when changing code

## Release Process

### Versioning

We follow semantic versioning (SemVer):

- `MAJOR`: Breaking changes
- `MINOR`: New features
- `PATCH`: Bug fixes

### Release Checklist

1. Update version in `pyproject.toml`
2. Update `CHANGELOG.md`
3. Run all tests and ensure they pass
4. Update documentation
5. Create release branch
6. Tag the release
7. Push to GitHub
8. Create GitHub release

### Changelog Format

Follow Keep a Changelog format:

```markdown
## [Unreleased]

### Added
- New feature
- New test

### Changed
- Improvement

### Fixed
- Bug fix

## [1.0.0] - 2025-01-15

### Added
- Initial release
```

## Community

### Communication Channels
- GitHub Issues: Bug reports and feature requests
- GitHub Discussions: General discussion
- Email: support@example.com

### Code of Conduct
- Be respectful and inclusive
- Focus on constructive feedback
- Help others learn and contribute
- Follow the code of conduct

### Getting Help
- Read the documentation first
- Search existing issues
- Ask in GitHub Discussions
- Contact maintainers

## Performance

### Optimization Tips
- Profile code before optimizing
- Use appropriate algorithms
- Minimize I/O operations
- Use caching where appropriate
- Optimize memory usage

### Performance Testing
- Use local testing for performance
- Use appropriate datasets
- Monitor resource usage
- Compare performance before and after changes

## Security

### Security Best Practices
- Validate all inputs
- Use parameterized queries
- Handle errors appropriately
- Log security-relevant events
- Use secure dependencies

### Dependency Management
- Regularly update dependencies
- Check for vulnerabilities
- Use version pinning for critical dependencies
- Review dependencies before adding

## Troubleshooting

### Common Issues
- Import errors: Check Python path
- Module not found: Check dependencies
- Test failures: Check test environment
- Performance issues: Profile code

### Debugging Tips
- Use logging for debugging
- Add debug statements carefully
- Use debuggers for complex issues
- Isolate problems before fixing

## Contributor Recognition

### Contributor Levels
- **Contributor**: Regular contributions
- **Maintainer**: Active code contributions
- **Core Team**: Project leadership

### Recognition Methods
- Contributor list in README
- Recognition in releases
- Shoutouts in community channels
- Opportunities for leadership roles

## Final Checklist Before Submitting

### Code Quality
- [ ] Code follows project style guidelines
- [ ] All tests are passing
- [ ] Code is properly documented
- [ ] No security vulnerabilities
- [ ] Performance impact is considered

### Documentation
- [ ] Documentation is updated
- [ ] Examples are provided
- [ ] API documentation is updated
- [ ] README is updated if needed

### Testing
- [ ] New features are tested
- [ ] Existing functionality is not broken
- [ ] Integration tests are passing
- [ ] Edge cases are covered

### Release
- [ ] Version number is updated
- [ ] Changelog is updated
- [ ] Release branch is created
- [ ] Pull request is created
- [ ] Review comments are addressed

---

Thank you for contributing to the LLM Advanced Testing Suite!
"""
    
    with open("CONTRIBUTING.md", "w", encoding="utf-8") as f:
        f.write(contributing_content)
    
    print("CONTRIBUTING.md created")

def create_changelog():
    """Create CHANGELOG.md"""
    print("Creating CHANGELOG.md...")
    
    changelog_content = """# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Cognitive ecosystem testing framework
- Role independence testing suite
- Enhanced visual test interface
- Comprehensive scoring system
- Multi-model support (OpenAI, Anthropic, Google, Ollama, etc.)

### Changed
- Improved test orchestration system
- Enhanced result analysis and visualization
- Better error handling and logging
- Optimized performance for large-scale testing

### Fixed
- Memory management issues in long-running tests
- Model connection timeout handling
- Test result consistency across different environments

## [1.0.0] - 2025-01-15

### Added
- Initial release of LLM Advanced Testing Suite
- 25 structured test pillars covering comprehensive LLM capabilities
- Core testing framework with modular architecture
- Support for multiple model providers
- Comprehensive documentation and examples
- Web-based test interface
- Automated test result analysis

### Features
- **Foundation Layer (Pillars 1-8)**: Logic reasoning, instruction following, structural operations, long context processing, domain knowledge, tool usage, planning, metacognition, creativity, safety
- **Advanced Layer (Pillars 9-19)**: Role playing, multi-role collaboration, task graph generation, fault tolerance, workflow management, network analysis, massive consensus, dynamic role switching
- **Cutting-Edge Layer (Pillars 20-24)**: Project management, parallel task optimization, multidisciplinary decomposition, cognitive ecosystem
- **Cognitive Ecosystem (Pillar 25)**: Role independence, cognitive diversity, collective intelligence

### Technical Details
- Python 3.8+ compatibility
- Comprehensive dependency management
- Extensible plugin architecture
- Scientific methodology with controlled variables
- Rich analytics and reporting capabilities

### Documentation
- Project overview and quick start guide
- Developer guide with API documentation
- Architecture documentation
- User guide for different use cases
- Cognitive ecosystem guide
- Scoring explanation

### Configuration
- Environment-based configuration
- Model service configuration
- Test customization options
- Role and prompt management

### Testing
- Unit tests for core functionality
- Integration tests for complex scenarios
- Performance tests for large-scale testing
- Compatibility tests across different environments

## [0.9.0] - 2024-12-20

### Added
- Beta release of the testing framework
- Basic test pillars 1-15
- Model integration with OpenAI and Ollama
- Basic result visualization
- Initial documentation

### Changed
- Refactored core architecture for better modularity
- Improved test execution performance
- Enhanced error handling

### Fixed
- Import issues in test modules
- Memory leaks in long-running tests
- Configuration file parsing errors

## [0.8.0] - 2024-11-15

### Added
- Alpha release with basic testing capabilities
- Support for local model testing
- Simple test result reporting
- Basic documentation

### Changed
- Initial framework development
- Test case structure definition
- Configuration system implementation

## [0.1.0] - 2024-10-01

### Added
- Project initialization
- Basic project structure
- Initial research and planning
- Technology stack selection

---

## Versioning

This project follows [Semantic Versioning](https://semver.org/spec/v2.0.0.html):

- **Major (X.0.0)**: Incompatible API changes
- **Minor (X.Y.0)**: New functionality in a backward compatible manner
- **Patch (X.Y.Z)**: Backward compatible bug fixes

## Release Process

1. Update version numbers in `pyproject.toml`
2. Update this changelog
3. Run all tests and ensure they pass
4. Update documentation
5. Create release branch
6. Tag the release
7. Push to GitHub
8. Create GitHub release

## Support

For questions or issues, please:
- Check the [documentation](https://llmtest24.readthedocs.io)
- Search existing [GitHub issues](https://github.com/ptreezh/llmtest24/issues)
- Create a new issue if needed
"""
    
    with open("CHANGELOG.md", "w", encoding="utf-8") as f:
        f.write(changelog_content)
    
    print("CHANGELOG.md created")

def create_requirements():
    """Create requirements files"""
    print("Creating requirements files...")
    
    # requirements.txt
    requirements_content = """# Core dependencies
requests>=2.31.0
pydantic>=2.0.0
python-dotenv>=1.0.0
pyyaml>=6.0

# Data processing
pandas>=2.0.0
numpy>=1.24.0

# Optional dependencies for enhanced functionality
openpyxl>=3.1.0  # For Excel export
matplotlib>=3.7.0  # For visualization
seaborn>=0.12.0  # For advanced plotting

# Web interface
streamlit>=1.0.0  # For the visual test interface

# Logging and monitoring
structlog>=23.1.0

# Optional: Cloud model services
# Install these based on your needs:
# openai>=1.0.0        # For OpenAI models
# anthropic>=0.3.0     # For Anthropic models  
# google-generativeai>=0.3.0  # For Google models
# ollama>=0.1.0       # For local Ollama models
"""
    
    with open("requirements.txt", "w", encoding="utf-8") as f:
        f.write(requirements_content)
    
    # requirements-dev.txt
    dev_requirements_content = """# Development dependencies
pytest>=7.4.0
pytest-cov>=4.1.0
pytest-mock>=3.10.0
black>=23.0.0
flake8>=6.0.0
mypy>=1.5.0
pre-commit>=3.0.0
isort>=5.12.0

# Documentation
sphinx>=5.0.0
sphinx-rtd-theme>=1.0.0
myst-parser>=1.0.0

# Type checking
types-requests>=2.31.0
types-PyYAML>=6.0.0

# Testing utilities
pytest-xdist>=3.0.0  # Parallel testing
pytest-benchmark>=4.0.0  # Performance testing
"""
    
    with open("requirements-dev.txt", "w", encoding="utf-8") as f:
        f.write(dev_requirements_content)
    
    # requirements-optional.txt
    optional_requirements_content = """# Optional dependencies for specific model providers
# OpenAI models
openai>=1.0.0

# Anthropic models
anthropic>=0.3.0

# Google models
google-generativeai>=0.3.0

# Local Ollama models
ollama>=0.1.0

# Azure OpenAI
azure-identity>=1.13.0
azure-openai>=1.0.0

# AWS Bedrock
boto3>=1.28.0

# HuggingFace
transformers>=4.35.0
torch>=2.0.0

# Additional visualization
plotly>=5.0.0
dash>=2.0.0

# Advanced data processing
scikit-learn>=1.3.0
networkx>=3.1.0

# Natural language processing
nltk>=3.8.0
spacy>=3.7.0

# Async support
aiohttp>=3.8.0
asyncio-mqtt>=0.13.0

# Database (for advanced features)
sqlalchemy>=2.0.0
psycopg2-binary>=2.9.0

# Monitoring and logging
prometheus-client>=0.19.0
grafana-api>=1.0.3
"""
    
    with open("requirements-optional.txt", "w", encoding="utf-8") as f:
        f.write(optional_requirements_content)
    
    print("Requirements files created")

def create_gitignore():
    """Create .gitignore file"""
    print("Creating .gitignore file...")
    
    gitignore_content = """# Byte-compiled / optimized / DLL files
__pycache__/
*.py[cod]
*$py.class

# C extensions
*.so

# Distribution / packaging
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
pip-wheel-metadata/
share/python-wheels/
*.egg-info/
.installed.cfg
*.egg
MANIFEST

# PyInstaller
#  Usually these files are written by a python script from a template
#  before PyInstaller builds the exe, so as to inject date/other infos into it.
*.manifest
*.spec

# Installer logs
pip-log.txt
pip-delete-this-directory.txt

# Unit test / coverage reports
htmlcov/
.tox/
.nox/
.coverage
.coverage.*
.cache
nosetests.xml
coverage.xml
*.cover
*.py,cover
.hypothesis/
.pytest_cache/

# Translations
*.mo
*.pot

# Django stuff:
*.log
local_settings.py
db.sqlite3
db.sqlite3-journal

# Flask stuff:
instance/
.webassets-cache

# Scrapy stuff:
.scrapy

# Sphinx documentation
docs/_build/

# PyBuilder
target/

# Jupyter Notebook
.ipynb_checkpoints

# IPython
profile_default/
ipython_config.py

# pyenv
.python-version

# PEP 582; used by PDM, PEP 582 compatible tools and python itself
__pypackages__/

# Celery stuff
celerybeat-schedule
celerybeat.pid

# SageMath parsed files
*.sage.py

# Environments
.env
.venv
env/
ENV/
env.bak/
venv.bak/

# Spyder project settings
.spyderproject
.spyproject

# Rope project settings
.ropeproject

# mkdocs documentation
/site

# mypy
.mypy_cache/
.dmypy.json
dmypy.json

# Pyre type checker
.pyre/

# pytype static analyzer
.pytype/

# Crush
.crush/
.crushrules/

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
.DS_Store?
._*
.Spotlight-V100
.Trashes
ehthumbs.db
Thumbs.db

# Project specific
testout/
results/
test_logs/
memory_db/
data/
*.tmp
*.temp
*.log

# Docker
.dockerignore
docker-compose.override.yml

# GitHub
.github/workflows/secrets

# Temporary files
*.tmp
*.temp
*.log

# Model files (if any)
*.model
*.bin
*.pt
*.pth

# Cache directories
.cache/
__pycache__/

# Node.js (if any)
node_modules/
npm-debug.log*
yarn-debug.log*
yarn-error.log*

# Rust (if any)
Cargo.lock
target/

# Go (if any)
go.sum

# Java (if any)
*.jar
*.war
*.nar
*.ear
*.zip
*.tar.gz
*.rar
*.7z

# C/C++ (if any)
*.o
*.a
*.so
*.dylib
*.dll
*.exe
*.msi
*.dmg
*.pkg
*.deb
*.rpm
*.apk
*.ipa
*.app
*.appx
*.msix
*.snap
*.flatpak
*.snapcraft.yaml

# Other
*.pdf
*.doc
*.docx
*.xls
*.xlsx
*.ppt
*.pptx
*.odt
*.ods
*.odp
*.rtf
*.tex
*.epub
*.mobi
*.djvu
*.cbz
*.cbr
*.cb7
*.cbt
*.cba
*.pdfx
*.xps
*.oxps
"""
    
    with open(".gitignore", "w", encoding="utf-8") as f:
        f.write(gitignore_content)
    
    print(".gitignore file created")

def create_docker_files():
    """Create Docker configuration files"""
    print("Creating Docker configuration files...")
    
    # Dockerfile
    dockerfile_content = """FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \\
    git \\
    curl \\
    wget \\
    && rm -rf /var/lib/apt/lists/*

# Copy requirements files
COPY requirements.txt requirements-dev.txt requirements-optional.txt ./

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Install optional dependencies
RUN pip install --no-cache-dir -r requirements-optional.txt

# Copy project files
COPY . .

# Create virtual environment
RUN python -m venv venv
ENV PATH="/app/venv/bin:$PATH"

# Create directories
RUN mkdir -p testout results test_logs memory_db docs/build examples

# Set environment variables
ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1

# Create a user
RUN useradd -m appuser && chown -R appuser:appuser /app
USER appuser

# Expose the port for web interface
EXPOSE 8501

# Default command
CMD ["python", "visual_test_interface.py"]
"""
    
    with open("Dockerfile", "w", encoding="utf-8") as f:
        f.write(dockerfile_content)
    
    # docker-compose.yml
    compose_content = """version: '3.8'

services:
  llm-testing-suite:
    image: llmtest24:latest
    container_name: llm-testing-suite
    environment:
      - PYTHONPATH=/app
      - PYTHONUNBUFFERED=1
    ports:
      - "8501:8501"
    volumes:
      - ./testout:/app/testout
      - ./results:/app/results
      - ./test_logs:/app/test_logs
      - ./memory_db:/app/memory_db
      - ./docs:/app/docs
    working_dir: /app
    command: python visual_test_interface.py
    restart: unless-stopped

  llm-testing-suite-api:
    image: llmtest24:latest
    container_name: llm-testing-suite-api
    environment:
      - PYTHONPATH=/app
      - PYTHONUNBUFFERED=1
    ports:
      - "8000:8000"
    volumes:
      - ./testout:/app/testout
      - ./results:/app/results
      - ./test_logs:/app/test_logs
      - ./memory_db:/app/memory_db
    working_dir: /app
    command: python -c "from fastapi import FastAPI; app = FastAPI(); @app.get('/'); def read_root(): return {'message': 'LLM Testing Suite API'}; import uvicorn; uvicorn.run(app, host='0.0.0.0', port=8000)"
    restart: unless-stopped

  llm-testing-suite-worker:
    image: llmtest24:latest
    container_name: llm-testing-suite-worker
    environment:
      - PYTHONPATH=/app
      - PYTHONUNBUFFERED=1
    volumes:
      - ./testout:/app/testout
      - ./results:/app/results
      - ./test_logs:/app/test_logs
      - ./memory_db:/app/memory_db
    working_dir: /app
    command: python -c "while True: print('Worker is running...'); import time; time.sleep(60)"
    restart: unless-stopped

volumes:
  testout:
    driver: local
  results:
    driver: local
  test_logs:
    driver: local
  memory_db:
    driver: local
  docs:
    driver: local
"""
    
    with open("docker-compose.yml", "w", encoding="utf-8") as f:
        f.write(compose_content)
    
    # .dockerignore
    dockerignore_content = """# Python cache and build files
__pycache__/
*.py[cod]
*$py.class
*.so

# Python build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg
MANIFEST

# Virtual environments
venv/
env/
ENV/
env.bak/
venv.bak/

# Testing and output directories
testout/
results/
test_logs/
memory_db/
data/

# IDE and editor files
.vscode/
.idea/
*.swp
*.swo

# OS generated files
.DS_Store
.DS_Store?
._*
.Spotlight-V100
.Trashes
ehthumbs.db
Thumbs.db

# Git files
.git/
.gitignore

# Documentation (docs will be copied separately)
docs/source/
docs/build/

# Temporary files
*.tmp
*.temp
*.log

# Environment files (except template)
config/.env
.env

# Development files
requirements-dev.txt
requirements-optional.txt
.pytest_cache/
.coverage
htmlcov/
.tox/
.nox/

# Jupyter Notebook files
.ipynb_checkpoints/
*.ipynb

# Database files
*.db
*.sqlite
*.sqlite3

# Archive files
*.tar
*.tar.gz
*.tar.bz2
*.tar.xz
*.zip
*.rar
*.7z

# Backup files
*.bak
*.backup
*.old

# Node.js (if any)
node_modules/
npm-debug.log*
yarn-debug.log*
yarn-error.log*

# Rust (if any)
Cargo.lock
target/

# Go (if any)
go.sum

# Java (if any)
*.jar
*.war
*.nar
*.ear
"""
    
    with open(".dockerignore", "w", encoding="utf-8") as f:
        f.write(dockerignore_content)
    
    print("Docker configuration files created")

def create_github_workflows():
    """Create GitHub Actions workflows"""
    print("Creating GitHub Actions workflows...")
    
    # Create .github/workflows directory
    Path(".github/workflows").mkdir(parents=True, exist_ok=True)
    
    # CI/CD workflow
    ci_cd_content = """name: CI/CD

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: [3.8, 3.9, "3.10", "3.11"]
    
    steps:
    - name: Checkout code
      uses: actions/checkout@v4
    
    - name: Setup Python
      uses: actions/setup-python@v4
      with:
        python-version: ${{ matrix.python-version }}
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
        pip install -r requirements-dev.txt
    
    - name: Lint with Black
      run: |
        black --check . --line-length=88
    
    - name: Lint with Flake8
      run: |
        flake8 . --max-line-length=88 --extend-ignore=E203,W503
    
    - name: Type-check with MyPy
      run: |
        mypy . --ignore-missing-imports --strict-optional --no-strict-optional --warn-redundant-casts --warn-unused-ignores --warn-no-return --warn-unreachable --strict-equality
    
    - name: Test with Pytest
      run: |
        pytest --cov=. --cov-report=xml --cov-report=term-missing --cov-report=html
    
    - name: Upload coverage Report
      uses: actions/upload-artifact@v3
      with:
        name: coverage-report
        path: htmlcov/
    
    - name: Upload coverage to Codecov
      uses: codecov/codecov-action@v3
      with:
        file: ./coverage.xml
        flags: unittests,fail_ci_if_error

  build-docker:
    runs-on: ubuntu-latest
    needs: test
    
    steps:
    - name: Setup Docker Buildx
      uses: docker/setup-buildx-action@v2
    
    - name: Login to DockerHub
      uses: docker/login-action@v2
      with:
        username: ${{ secrets.DOCKERHUB_USERNAME }}
        password: ${{ secrets.DOCKERHUB_PASSWORD }}
    
    - name: Build and push Docker image
      uses: docker/build-push-action@v4
      with:
        context: .
        push: true
        tags: |
          ${{ secrets.DOCKERHUB_USERNAME }}/llmtest24:latest
          ${{ secrets.DOCKERHUB_USERNAME }}/llmtest24:${{ github.sha }}

  security-scanning:
    runs-on: ubuntu-latest
    needs: build-docker
    
    steps:
    - name: Run Trivy Docker Scanner
      uses: aquasecurity/trivy-action@master
      with:
        scan-type: image
        input-ref: ${{ secrets.DOCKERHUB_USERNAME }}/llmtest24:latest
        format: sarif
        output: trivy-results.sarif
    
    - name: Upload Trivy Scan Result
      uses: github/codeql-action/upload-sarif@v2
      with:
        sarif_file: trivy-results.sarif

  documentation-build:
    runs-on: ubuntu-latest
    needs: test
    
    steps:
    - name: Checkout code
      uses: actions/checkout@v4
    
    - name: Setup Python
      uses: actions/setup-python@v4
      with:
        python-version: "3.10"
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
        pip install -r requirements-dev.txt
    
    - name: Build Documentation
      run: |
        cd docs
        make html
    
    - name: Upload Documentation Artifacts
      uses: actions/upload-artifact@v3
      with:
        name: documentation
        path: docs/build/html

  release:
    runs-on: ubuntu-latest
    needs: [test, build-docker, security-scanning, documentation-build]
    if: github.event_name == 'release' && github.event.action == 'published'
    
    steps:
    - name: Download Artifacts
      uses: actions/download-artifact@v3
      with:
        pattern: coverage-report
        name: coverage-report
        path: coverage-report
    
    - name: Download Documentation Artifacts
      uses: actions/download-artifact@v3
      with:
        pattern: documentation
        name: documentation
        path: docs/build/html
    
    - name: Create Release Note
      run: |
        echo "## Release Notes" > release_notes.md
        echo "" >> release_notes.md
        echo "### Changes in ${{ github.ref_name }}" >> release_notes.md
        echo "" >> release_notes.md
        echo "#### Features" >> release_notes.md
        echo "- Added new test capabilities" >> release_notes.md
        echo "- Improved test framework performance" >> release_notes.md
        echo "- Enhanced documentation" >> release_notes.md
        echo "" >> release_notes.md
        echo "#### Bug Fixes" >> release_notes.md
        echo "- Fixed import issues" >> release_notes.md
        echo "- Improved error handling" >> release_notes.md
        echo "" >> release_notes.md
        echo "#### Performance" >> release_notes.md
        echo "- Optimized memory usage" >> release_notes.md
        echo "- Reduced test execution time" >> release_notes.md
    
    - name: Upload Release Asset
      uses: actions/upload-release-asset@v1
      with:
        upload_url: ${{ github.event.release.upload_url }}
        asset_path: ./release_notes.md
        asset_name: release_notes.md
        asset_content_type: text/plain
"""
    
    with open(".github/workflows/ci-cd.yml", "w", encoding="utf-8") as f:
        f.write(ci_cd_content)
    
    # Documentation workflow
    docs_content = """name: Documentation

on:
  push:
    branches: [main]

jobs:
  build:
    runs-on: ubuntu-latest
    
    steps:
    - name: Checkout code
      uses: actions/checkout@v4
    
    - name: Setup Python
      uses: actions/setup-python@v4
      with:
        python-version: "3.10"
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
        pip install -r requirements-dev.txt
    
    - name: Build Documentation
      run: |
        cd docs
        make html
    
    - name: Deploy to GitHub Pages
      uses: peaceiris/actions-gh-pages@v3
      with:
        github_token: ${{ secrets.GITHUB_TOKEN }}
        publish_dir: ./docs/build/html
"""
    
    with open(".github/workflows/docs.yml", "w", encoding="utf-8") as f:
        f.write(docs_content)
    
    print("GitHub Actions workflows created")

def create_example_files():
    """Create example files"""
    print("Creating example files...")
    
    # Create examples directory
    Path("examples").mkdir(exist_ok=True)
    
    # example_usage.py
    example_content = '''#!/usr/bin/env python3
"""
LLM Advanced Testing Suite - Example Usage Script
This script demonstrates how to use the testing framework for various scenarios.
"""

import os
import sys
import json
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from scripts.utils.utils import run_single_test, print_assessment_criteria
from config.config import MODEL_TO_TEST

def example_basic_test():
    """Example of running a basic test"""
    print("Example 1: Basic Logic Test")
    print("-" * 40)
    pillar_name = "pillar_01_logic"
    prompt = "If all roses are flowers and some flowers fade quickly, can we conclude that some roses fade quickly? Explain your reasoning step by step."
    model = MODEL_TO_TEST
    
    try:
        result = run_single_test(pillar_name, prompt, model)
        print(f"Test completed successfully")
        print(f"Score: {result.get('score', 'N/A')}")
        print(f"Response: {result.get('model_response', 'N/A')[:200]}...")
        print()
    except Exception as e:
        print(f"Test failed: {e}")
        print()

def example_role_playing_test():
    """Example of running a role-playing test"""
    print("Example 2: Role-Playing Test")
    print("-" * 40)
    pillar_name = "pillar_12_persona"
    prompt = "You are an experienced software architect with 15 years of experience. Explain the key principles of microservices architecture to a junior developer. Include practical examples and common pitfalls to avoid."
    model = MODEL_TO_TEST
    
    try:
        result = run_single_test(pillar_name, prompt, model)
        print(f"Test completed successfully")
        print(f"Score: {result.get('score', 'N/A')}")
        print(f"Response: {result.get('model_response', 'N/A')[:200]}...")
        print()
    except Exception as e:
        print(f"Test failed: {e}")
        print()

def example_creativity_test():
    """Example of running a creativity test"""
    print("Example 3: Creativity Test")
    print("-" * 40)
    pillar_name = "pillar_09_creativity"
    prompt = "Generate 5 innovative business ideas that combine artificial intelligence with sustainable agriculture. For each idea, explain the problem it solves, how it works, and its potential impact."
    model = MODEL_TO_TEST
    
    try:
        result = run_single_test(pillar_name, prompt, model)
        print(f"Test completed successfully")
        print(f"Score: {result.get('score', 'N/A')}")
        print(f"Response: {result.get('model_response', 'N/A')[:200]}...")
        print()
    except Exception as e:
        print(f"Test failed: {e}")
        print()

def main():
    """Run all examples"""
    print("LLM Advanced Testing Suite - Example Usage")
    print("=" * 50)
    print()
    
    # Check if model is configured
    if not MODEL_TO_TEST:
        print("No model configured. Please set MODEL_TO_TEST in config/config.py")
        return
    
    print(f"Using model: {MODEL_TO_TEST}")
    print()
    
    # Run examples
    examples = [
        example_basic_test,
        example_role_playing_test,
        example_creativity_test,
    ]
    
    for example in examples:
        try:
            example()
        except KeyboardInterrupt:
            print("\\nExample interrupted by user")
            break
        except Exception as e:
            print(f"Unexpected error in {example.__name__}: {e}")
    
    print()
    print("All examples completed!")
    print()
    print("Tips:")
    print("- Check the test results in the 'testout/' directory")
    print("- View detailed analysis in 'results/' directory")
    print("- Modify prompts and parameters to test different scenarios")
    print("- Use 'python scripts/main_orchestrator.py --help' for more options")

if __name__ == "__main__":
    main()
'''
    
    with open("examples/example_usage.py", "w", encoding="utf-8") as f:
        f.write(example_content)
    
    print("Example files created")

def create_pre_commit():
    """Create pre-commit configuration"""
    print("Creating pre-commit configuration...")
    
    precommit_content = """repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.4.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-added-large-files
      - id: check-case-conflict
      - id: check-merge-conflict
      - id: debug-statements
      - id: mixed-line-ending

  - repo: https://github.com/psf/black
    rev: 23.1.0
    hooks:
      - id: black
        language_version: python3.8
        args: [--line-length=88]

  - repo: https://github.com/pycqa/flake8
    rev: 6.0.0
    hooks:
      - id: flake8
        args: [--max-line-length=88, --extend-ignore=E203,W503]

  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.1.1
    hooks:
      - id: mypy
        additional_dependencies: [types-requests, types-PyYAML]
        args: [--ignore-missing-imports, --strict-optional, --no-strict-optional, --warn-redundant-casts, --warn-unused-ignores, --warn-no-return, --warn-unreachable, --strict-equality]

  - repo: https://github.com/pycqa/isort
    rev: 5.12.0
    hooks:
      - id: isort
        args: [--profile=black, --line-length=88]

  - repo: https://github.com/pre-commit/mirrors-prettier
    rev: v3.0.0-alpha.9-for-vscode
    hooks:
      - id: prettier
        types_or: [yaml, markdown, json]
        args: [--prose-wrap=always]

  - repo: https://github.com/pycqa/bandit
    rev: 1.7.4
    hooks:
      - id: bandit
        args: [-r, -x, tests/]

  - repo: https://github.com/Lucas-C/pre-commit-hooks-safety
    rev: v1.3.2
    hooks:
      - id: python-safety-dependencies-check
        files: requirements.*\\.txt$

  - repo: https://github.com/shellcheck-py/shellcheck-py
    rev: v0.9.0.2
    hooks:
      - id: shellcheck
        args: [-e, SC1091]
"""
    
    with open(".pre-commit-config.yaml", "w", encoding="utf-8") as f:
        f.write(precommit_content)
    
    print("Pre-commit configuration created")

def create_makefile():
    """Create Makefile for development"""
    print("Creating Makefile...")
    
    makefile_content = """# Makefile for LLM Advanced Testing Suite

.PHONY: help install install-dev install-optional test test-coverage test-unit test-integration lint format type-check security-check build clean docs serve-docs release deploy

help:  ## Show this help message
	@echo "LLM Advanced Testing Suite Development Commands:"
	@echo ""
	@awk 'BEGIN {FS = ":.*##"; printf "%-20s %s\\n", "Target", "Description"} /^[a-zA-Z_-]+:.*?##/ { printf "%-20s %s\\n", $$1, $$2 }' $(MAKEFILE_LIST)

install:  ## Install dependencies
	pip install -r requirements.txt

install-dev:  ## Install development dependencies
	pip install -r requirements.txt
	pip install -r requirements-dev.txt
	pre-commit install

install-optional:  ## Install optional dependencies
	pip install -r requirements-optional.txt

test:  ## Run all tests
	pytest

test-coverage:  ## Run tests with coverage
	pytest --cov=. --cov-report=html --cov-report=term-missing

test-unit:  ## Run unit tests
	pytest -m unit

test-integration:  ## Run integration tests
	pytest -m integration

test-fast:  ## Run tests without coverage
	pytest --no-cov

lint:  ## Run linting
	flake8 . --max-line-length=88 --extend-ignore=E203,W503
	black --check . --line-length=88
	isort --check-only --profile=black --line-length=88

format:  ## Format code
	black . --line-length=88
	isort --profile=black --line-length=88

type-check:  ## Run type checking
	mypy . --ignore-missing-imports --strict-optional --no-strict-optional --warn-redundant-casts --warn-unused-ignores --warn-no-return --warn-unreachable --strict-equality

security-check:  ## Run security checks
	bandit -r .
	safety check

build:  ## Build package
	python -m build

clean:  ## Clean build artifacts
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	rm -rf .pytest_cache/
	rm -rf .mypy_cache/
	rm -rf .coverage
	rm -rf htmlcov/
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

docs:  ## Build documentation
	cd docs && make html

serve-docs:  ## Serve documentation locally
	cd docs/build/html && python -m http.server 8000

release:  ## Create release
	@echo "Creating release..."
	@echo "Please ensure:"
	@echo "1. All tests are passing"
	@echo "2. Documentation is updated"
	@echo "3. Version is updated in pyproject.toml"
	@echo "4. Changelog is updated"
	@read -p "Press Enter to continue or Ctrl+C to abort..."
	python -m build
	twine upload dist/*

deploy:  ## Deploy to production
	@echo "Deploying to production..."
	@echo "Please ensure:"
	@echo "1. All tests are passing"
	@echo "2. Documentation is built"
	@echo "3. Docker image is built"
	@read -p "Press Enter to continue or Ctrl+C to abort..."
	docker build -t llmtest24:latest .
	docker push llmtest24:latest

docker-build:  ## Build Docker image
	docker build -t llmtest24:latest .

docker-run:  ## Run Docker container
	docker run -p 8501:8501 -v $(PWD)/testout:/app/testout -v $(PWD)/results:/app/results llmtest24:latest

docker-compose-up:  ## Start Docker Compose
	docker-compose up -d

docker-compose-down:  ## Stop Docker Compose
	docker-compose down

setup:  ## Initial setup
	python install.py
	pre-commit install

check:  ## Run all checks
	$(MAKE) lint
	$(MAKE) type-check
	$(MAKE) security-check
	$(MAKE) test

ci:  ## Run CI checks locally
	$(MAKE) check
	$(MAKE) test-coverage

all:  ## Run all checks and tests
	$(MAKE) check
	$(MAKE) test-coverage
	$(MAKE) docs
"""
    
    with open("Makefile", "w", encoding="utf-8") as f:
        f.write(makefile_content)
    
    print("Makefile created")

def final_summary():
    """Print final summary"""
    print("Project organization completed!")
    print()
    print("Summary of created files:")
    print("  - README.md - Project overview and quick start")
    print("  - LICENSE - MIT license")
    print("  - CONTRIBUTING.md - Contribution guidelines")
    print("  - CHANGELOG.md - Version history")
    print("  - requirements.txt - Core dependencies")
    print("  - requirements-dev.txt - Development dependencies")
    print("  - requirements-optional.txt - Optional dependencies")
    print("  - .gitignore - Git ignore rules")
    print("  - .pre-commit-config.yaml - Pre-commit hooks")
    print("  - Makefile - Development commands")
    print("  - examples/example_usage.py - Usage examples")
    print("  - Dockerfile - Docker configuration")
    print("  - docker-compose.yml - Docker Compose configuration")
    print("  - .github/workflows/ - GitHub Actions workflows")
    print("  - docs/ - Documentation files")
    print()
    print("Next steps:")
    print("1. Review and customize the configuration files")
    print("2. Set up your model API keys in config/.env")
    print("3. Test the installation with the provided scripts")
    print("4. Run the example usage script")
    print("5. Start contributing to the project!")
    print()
    print("Documentation:")
    print("  - README.md - Project overview")
    print("  - docs/ - Detailed documentation")
    print("  - CONTRIBUTING.md - Development guidelines")
    print("  - docs/API_REFERENCE.md - API documentation")
    print("  - docs/QUICKSTART.md - Quick start guide")
    print()
    print("The project is now ready for open source release!")

def main():
    """Main organization function"""
    print_header()
    
    create_readme()
    create_license()
    create_contributing()
    create_changelog()
    create_requirements()
    create_gitignore()
    create_docker_files()
    create_github_workflows()
    create_example_files()
    create_pre_commit()
    create_makefile()
    
    final_summary()

if __name__ == "__main__":
    main()