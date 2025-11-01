## Build & Test

- **Install dependencies**: `pip install -r config/requirements.txt`
- **Run all tests**: `pytest`
- **Run tests in a specific file**: `pytest tests/test_pillar_14_persona_depth.py`
- **Run a specific test**: `pytest tests/test_pillar_14_persona_depth.py::test_persona_depth_evaluation`
- **Run the main orchestrator**: `python scripts/main_orchestrator.py --model <model_name>`
- **Run independence tests**: `python run_pillar_25_independence.py`
- **Run cognitive ecosystem tests**: `python scripts/testing/run_cognitive_ecosystem_cloud_test.py`
- **Run comprehensive tests**: `python run_comprehensive_tests.py`

## Lint & Formatting

- **Check formatting**: `black --check .`
- **Format code**: `black .`
- **Linting**: `flake8 .`
- **Type checking**: `mypy .`

## Code Style

- **Imports**: Use `import module` or `from module import name`. Avoid `from module import *`. Group stdlib, third-party, and local imports.
- **Formatting**: Use `black` for consistent formatting. Max line length of 88 characters.
- **Types**: Use type hints for all function signatures.
- **Naming**: Use `snake_case` for variables and functions. Use `PascalCase` for classes.
- **Error Handling**: Use `try...except` blocks for code that may raise exceptions. Be specific about the exceptions you catch.
- **Docstrings**: Use Google-style docstrings for all public modules, classes, and functions.
- **Logging**: Use the `logging` module for logging.
- **Configuration**: Use `config/config.py` for configuration management.
- **File Structure**: Follow the existing modular structure. Place tests in the `tests/` directory.
- **Testing**: All tests must be executable and pass 100% of integration tests. Never simulate functionality.

## Mandatory Workflow Rules

**CRITICAL**: Always follow the mandatory workflow in `.clinerules/`:
1. **Task Reception Phase**: Mandatory component scanning and task assumption validation
2. **Deep Analysis Phase**: Code-level verification and functionality testing
3. **Execution Planning Phase**: Strategy adjustment based on verified findings
4. **Execution Phase**: Continuous verification with pre/post execution checks
5. **Completion Phase**: Final quality gates including functionality, integration, and performance verification

**Zero Tolerance**: Never skip mandatory steps. Quality and accuracy are more important than speed.
