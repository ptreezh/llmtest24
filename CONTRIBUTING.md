# Contributing Guidelines

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
git clone https://github.com/your-username/llm-advanced-testing-suite.git
cd llm-advanced-testing-suite

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Linux/macOS:
source venv/bin/activate
# Windows:
venv\Scripts\activate

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
llm-advanced-testing-suite/
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
    """Test description"""
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
    """Run the test"""
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
