# Contributor Guide

This guide helps developers contribute to the LLM Advanced Testing Suite.

## Development Setup

### Prerequisites
- Python 3.8 or higher
- Git
- Virtual environment (recommended)

### Initial Setup

```bash
# Fork and clone repository
git clone https://github.com/ptreezh/llmtest24.git
cd llmtest24

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Linux/macOS
# On Windows:
# venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt

# Install pre-commit hooks
pre-commit install
```

## Code Quality

### Code Style
- Use Black for code formatting with 88 character run length
- Use Flake8 for linting
- Use MyPy for type checking
- Follow PEP 8 conventions
- Use Google-style docstrings

### Formatting

```bash
# Format code
black .

# Check formatting
black --check .

# Format only changed files
black $(git diff --name-only --diff-filter=ACMRTUXB HEAD)
```

### Linting

```bash
# Run linting
flake8 . --max-line-length=88 --extend-ignore=E203,W503

# Run type checking
mypy . --ignore-missing-imports --strict-optional --no-strict-optional --warn-redundant-casts --warn-unused-ignores --warn-no-return --warn-unreachable --strict-equality
```

### Testing
- Write unit tests for new features
- Maintain test coverage above 80%
- Use pytest for testing
- Test both success and failure cases

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=. --cov-report=html

# Run specific tests
pytest tests/test_pillar_01_logic.py

# Run with pytest-xdist for parallel testing
pytest -n 4
```

## Project Structure

### Directory Structure

```
llmtest24/
├── core/                    # Core framework
├── tests/                   # Test cases
├── independence/            # Independence testing
├── cognitive_ecosystem/     # Cognitive ecosystem
├── scripts/                 # Utility scripts
├── config/                  # Configuration
├── docs/                    # Documentation
├── results/                 # Results
├── examples/                # Examples
└── tools/                   # Utility tools
```

### Core Framework (`core/`)
- `framework.py`: Main Test Framework class
- `test_orchestrator.py`: Test orchestration
- `config_manager.py`: Configuration management

### Test Cases (`tests/`)
- `test_pillar_XX.py`: Individual test pillars
- `utils.py`: Test utilities
- `composite_scenarios/`: Composite test scenarios

### Independence Testing (`independence/`)
- `base.py`: Base classes for independence tests
- `character_breaking.py`: Stress tests
- `implicit_cognition.py`: Implicit cognition tests
- `longitudinal_consistency.py`: Longitudinal tests
- `metrics/`: Independence metrics

### Cognitive Ecosystem (`cognitive_ecosystem/`)
- `core/`: Core ecosystem engine
- `detectors/`: Various detectors
- `analyzers/`: Analysis components
- `baselines/`: Baseline comparisons

## Adding New Tests

### Test Structure

Each new test should follow this structure:

```python
# tests/test_pillar_xx_feature.py
import pytest
from core.framework import BaseTestPillar

class TestPillarXXFeature(BaseTestPillar):
    """Test pillar for XX feature."""
    
    def __init__(self):
        super().__init__(
            name="Pillar XX: Feature Name",
            description="Description of the test pillar",
            dependencies=["required", "pillars"],
            metrics=["metric1", "metric2"]
        )
    
    def run_test(self, model, config):
        """Execute the test."""
        # Test implementation
        pass
```

### Test Guidelines

1. Keep tests focused on a single capability or behavior
2. Use descriptive names for test methods
3. Include comprehensive assertions
4. Handle model errors gracefully
5. Document test assumptions and limitations

## Pull Request Process

1. Create a feature branch from the main branch
2. Add tests for new functionality
3. Update documentation as needed
4. Ensure all tests pass
5. Submit pull request with clear description

## Code Review Guidelines

- Check code follows established patterns
- Verify tests are comprehensive
- Confirm documentation is clear
- Ensure performance considerations are addressed
- Validate error handling

## Maintainer Guidelines

### Issue Triage
- Label issues appropriately
- Respond to questions within 48 hours
- Close irrelevant issues respectfully

### Release Process
1. Update version in `pyproject.toml`
2. Update changelog
3. Run full test suite
4. Create release tag
5. Publish to PyPI

## Questions?

If you have questions about contributing, feel free to open an issue or reach out to the maintainers.