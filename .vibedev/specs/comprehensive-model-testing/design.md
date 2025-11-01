# Feature: Comprehensive Model Testing - Design Document

## Overview
This document outlines the design for a unified testing system that enables comprehensive evaluation of cloud and local LLM models for cognitive independence and cognitive ecosystem capabilities. The system integrates existing test suites and provides a streamlined interface for execution and analysis.

## Architecture

The system follows a modular architecture centered around a main orchestrator script that manages the execution of various specialized test suites.

```mermaid
graph TD
    A[User CLI Input] --> B(main_orchestrator.py);
    B --> C{Parse Arguments};
    C -- --run-independence-tests--> D(run_cloud_independence_test.py);
    C -- --run-ecosystem-tests--> E(run_cognitive_ecosystem_cloud_test.py);
    C -- --test--> F(tests/test_pillar_*.py);
    C -- --workflow--> G(tests/composite_scenarios/*);
    
    D --> H(independence/);
    E --> I(cognitive_ecosystem/);
    F --> J(tests/);
    G --> K(tests/composite_scenarios/);

    H --> L(cloud_services.py);
    I --> L;
    J --> L;
    K --> L;

    L --> M[Cloud LLM APIs];
    L --> N[Local Ollama Models];

    D --> O(Save Independence Results);
    E --> P(Save Ecosystem Results);
    F --> Q(Save Pillar Test Results);
    G --> R(Save Workflow Results);

    O --> S[Results Directory];
    P --> S;
    Q --> S;
    R --> S;
```

**Key Components:**

*   **`main_orchestrator.py`**: The central script that parses command-line arguments and dispatches to the appropriate test execution logic. It acts as the primary user interface for initiating tests.
*   **`run_cloud_independence_test.py`**: A standalone script dedicated to running cloud model independence tests. It handles model discovery, test execution, and result saving.
*   **`run_cognitive_ecosystem_cloud_test.py`**: A standalone script for running cognitive ecosystem tests. It manages model discovery, intensity configuration, test execution, and result saving.
*   **`independence/` module**: Contains the core logic and experiments for cognitive independence testing (e.g., breaking stress, implicit cognition, longitudinal consistency).
*   **`cognitive_ecosystem/` module**: Contains the core logic for cognitive ecosystem testing (e.g., hallucination resistance, cognitive diversity, role consistency).
*   **`tests/` directory**: Houses various "pillar" tests that might be integrated or run independently.
*   **`config.py`**: Stores project-wide configurations, including default models and test settings.
*   **`cloud_services.py`**: Manages interactions with different cloud LLM providers and local model services (like Ollama).
*   **`utils.py`**: Provides common utility functions used across different scripts and modules.

## Components and Interfaces

*   **`main_orchestrator.py`**:
    *   **Interface**: Command-line arguments (`--model`, `--test`, `--workflow`, `--run-independence-tests`, `--run-ecosystem-tests`, `--ecosystem-intensity`).
    *   **Functionality**: Parses arguments, identifies which test suite to run, and invokes the appropriate script or function using `subprocess.run` or direct calls.
*   **`run_cloud_independence_test.py`**:
    *   **Interface**: Command-line argument `--model`.
    *   **Functionality**: Discovers available cloud models, runs independence tests on specified or all models, and saves results.
*   **`run_cognitive_ecosystem_cloud_test.py`**:
    *   **Interface**: Command-line arguments `--model` and `--intensity`.
    *   **Functionality**: Discovers available cloud models, runs ecosystem tests with specified intensity, and saves results.
*   **`independence/` and `cognitive_ecosystem/` modules**:
    *   **Interface**: Internal Python APIs used by the respective test runner scripts.
    *   **Functionality**: Implement specific testing methodologies and metrics.
*   **`cloud_services.py`**:
    *   **Interface**: Python functions (`get_available_services`, `call_cloud_service`).
    *   **Functionality**: Abstract away the complexities of interacting with different LLM providers and local model servers.

## Data Models

*   **Test Configuration**: Stored in `config.py` and potentially overridden by command-line arguments or specific test script configurations.
*   **Test Results**: Saved as JSON files in `testout/` (for independence tests) and `test_results/` (for ecosystem tests). These files contain detailed metrics, scores, and execution status.
*   **Role Prompts**: Stored in `.txt` files within the `role_prompts/` directory, loaded dynamically by test scripts.

## Error Handling

*   **Command Execution Errors**: `subprocess.run` in `main_orchestrator.py` uses `check=True` to raise exceptions for non-zero exit codes from test scripts.
*   **API Call Failures**: Individual test scripts include `try-except` blocks to catch exceptions during LLM API calls, logging errors and returning failure statuses.
*   **Model Availability**: Scripts check for available models and provide informative messages if none are found.
*   **All Cloud APIs Failed**: `main_orchestrator.py` includes logic to detect and log scenarios where all cloud APIs fail during basic pillar tests.
*   **Invalid Arguments**: `argparse` handles validation for command-line arguments (e.g., choices for intensity).

## Testing Strategy

The testing strategy is designed to be flexible and comprehensive:

1.  **Unified Execution**: The `main_orchestrator.py` script serves as a single entry point for running various types of LLM tests.
2.  **Targeted Testing**: Users can specify individual models to test using the `--model` argument, or run tests across all available models.
3.  **Test Suite Selection**: Users can choose to run:
    *   Basic "pillar" tests (default behavior if no specific test is selected).
    *   Specific pillar tests using `--test`.
    *   Complex workflows using `--workflow`.
    *   Cloud independence tests using `--run-independence-tests`.
    *   Cognitive ecosystem tests using `--run-ecosystem-tests` with optional `--ecosystem-intensity`.
4.  **Configurable Intensity**: Ecosystem tests can be run at different intensity levels (light, medium, heavy) to adjust the depth and duration of testing.
5.  **Fallback Mechanism**: The system is designed to fall back to using local Ollama models if cloud models are unavailable, ensuring test continuity.
6.  **Result Management**: Test results are systematically saved in structured formats (JSON) for analysis, with logs generated for each test run.

## Design Decisions and Rationales

*   **Modular Design**: Separating independence tests, ecosystem tests, and general pillar tests into distinct scripts and modules promotes maintainability and allows for easier updates or additions of new test types.
*   **Orchestrator Pattern**: Using `main_orchestrator.py` centralizes test execution, simplifying the user experience and providing a clear command-line interface for managing different testing scenarios.
*   **Argument Parsing**: Employing `argparse` makes the CLI interface robust and user-friendly, providing help messages and validating inputs.
*   **`subprocess.run` for Test Execution**: This allows the orchestrator to launch the standalone test scripts as separate processes, ensuring isolation and proper execution flow, and enabling graceful exit after specific test suites are completed.
*   **JSON for Results**: Standardizing on JSON for saving test results facilitates programmatic analysis and integration with reporting tools.

## User Input for Technical Decisions

*   **Model Selection**: The system defaults to a configured model but allows overriding via `--model`. For ecosystem tests, intensity can also be specified.
*   **Test Scope**: Users can choose to run all tests, specific pillar tests, workflows, or targeted independence/ecosystem tests.

## Future Considerations
- Integration of more sophisticated test result analysis and visualization.
- Enhanced error handling and retry mechanisms for flaky tests or API issues.
- Support for more diverse testing frameworks and LLM providers.
