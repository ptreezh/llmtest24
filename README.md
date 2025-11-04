# LLM Advanced Testing Suite

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

## Version History

- 1.0.1 (2025-11-04)
  - Replaced all character icons with CSS汉字替代方案 in the documentation
  - Updated all repository links from template placeholders to actual repository URL
  - Fixed formatting issues in CONTRIBUTOR_GUIDE.md

- 1.0.0 (2025-01-15)
  - Initial release
  - 25 structured test pillars for LLM evaluation
  - Cognitive ecosystem testing framework
  - Role independence testing suite

---

Made with ❤️ by the LLM Advanced Testing Suite team
