# Feature: Comprehensive Model Testing

## Introduction
This feature aims to enable comprehensive testing of cloud and local LLM models for their cognitive independence and cognitive ecosystem capabilities. It provides a unified way to execute these tests, allowing developers to evaluate model performance under various conditions and configurations.

## Requirements

1.  **Run Cloud Independence Tests for Specific Models**
    *   **User Story**: As a developer, I want to be able to run cloud independence tests for specific models, so that I can evaluate their performance in isolation.
    *   **Acceptance Criteria**:
        1.  **Given** a specified cloud model, **when** the independence tests are executed, **then** the tests should run successfully for that model.
        2.  **Given** a specified cloud model, **when** the independence tests are executed, **then** the results should be saved in a structured format (e.g., JSON).
        3.  **Given** no model is specified, **when** independence tests are initiated, **then** the system should prompt the user to select models or run for all available models.

2.  **Run Cognitive Ecosystem Tests with Configurable Intensity**
    *   **User Story**: As a developer, I want to be able to run cognitive ecosystem tests for specific models with configurable intensity, so that I can evaluate their collective intelligence and diversity.
    *   **Acceptance Criteria**:
        1.  **Given** a specified cloud model and intensity level (light, medium, heavy), **when** the ecosystem tests are executed, **then** the tests should run successfully for that model and intensity.
        2.  **Given** a specified cloud model and intensity level, **when** the ecosystem tests are executed, **then** the results should be saved in a structured format (e.g., JSON).
        3.  **Given** no model or intensity is specified, **when** ecosystem tests are initiated, **then** the system should prompt the user for these inputs.

3.  **Unified Test Execution via Orchestrator**
    *   **User Story**: As a developer, I want to be able to use the `main_orchestrator.py` script to trigger either independence or ecosystem tests for specific models, so that I can manage all testing activities from a single entry point.
    *   **Acceptance Criteria**:
        1.  **Given** the `--run-independence-tests <MODEL_NAME>` argument, **when** `main_orchestrator.py` is executed, **then** it should correctly invoke the independence tests for the specified model.
        2.  **Given** the `--run-ecosystem-tests <MODEL_NAME>` and `--ecosystem-intensity <INTENSITY>` arguments, **when** `main_orchestrator.py` is executed, **then** it should correctly invoke the ecosystem tests for the specified model and intensity.
        3.  **Given** no specific test arguments (`--run-independence-tests`, `--run-ecosystem-tests`, `--test`, `--workflow`) are provided, **when** `main_orchestrator.py` is executed, **then** it should default to running basic pillar tests.

4.  **Fallback to Local Ollama Models**
    *   **User Story**: As a developer, I want the system to handle cases where cloud models are unavailable by allowing the use of local Ollama models for testing, so that testing can proceed even without cloud access.
    *   **Acceptance Criteria**:
        1.  **Given** no cloud models are available, **when** a test is initiated (either independence or ecosystem), **then** the system should attempt to use a local Ollama model if configured or available.
        2.  **Given** a local Ollama model is used, **when** tests are executed, **then** the results should be comparable to cloud model tests where applicable.

## Considerations for Expansion
- Error handling for invalid model names or unavailable services.
- Robust handling of API rate limits and connection errors during cloud model tests.
- Clear distinction and organization of test results based on model and test type.
- Potential for parallel execution of tests for efficiency.
