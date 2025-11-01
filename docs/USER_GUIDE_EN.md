# LLM Advanced Capability Evaluation Suite - User Guide

## 1. Environment Preparation

### 1.1 Install Dependencies

```bash
# Install Python dependencies
pip install -r config/requirements.txt

# Install Ollama (for local model testing)
curl -fsSL https://ollama.com/install.sh | sh

# Install Node.js (for some tool scripts)
# Download and install from https://nodejs.org
```

### 1.2 Configure Environment Variables

Create a `.env` file and configure cloud service keys:

```bash
# .env
OPENAI_API_KEY=your_openai_key
GEMINI_API_KEY=your_gemini_key
DASHSCOPE_API_KEY=your_dashscope_key
```

### 1.3 Initialize Workspace

```bash
python workspace_init.py
```

## 2. Basic Configuration

### 2.1 Configure Test Models

Edit the `config.py` file:

```python
# Main test model
MODEL_TO_TEST = 'qwen2:7b'

# Cloud service priority models
CLOUD_PRIORITY_MODELS = [
    'gpt-4-turbo',
    'gemini-1.5-pro',
    'qwen-max'
]

# Test configuration
DEFAULT_OPTIONS_CREATIVE = {
    'temperature': 0.7,
    'top_p': 0.9,
    'max_tokens': 2048
}
```

### 2.2 Configure Test Roles

Add role configuration files in the `roles/` directory, for example `doctor.json`:

```json
{
  "name": "doctor",
  "description": "Senior doctor with extensive clinical experience",
  "expertise": ["Internal Medicine", "Surgery", "Emergency"],
  "personality": "Rigorous, professional, empathetic",
  "communication_style": "Clear, direct, using professional terminology"
}
```

### 2.3 Configure Test Parameters

Edit `config/test_config.yaml`:

```yaml
independence:
  breaking_stress:
    stress_levels: [1, 2, 3, 4, 5]
    stress_types: ["Logical Contradiction", "Emotional Pressure", "Authority Challenge", "Time Pressure"]
  implicit_cognition:
    categories: ["Cultural Bias", "Authority Obedience", "Emotional Tendency", "Moral Judgment"]
  longitudinal_consistency:
    conversation_turns: 10
    memory_persistence_check: true
```

## 3. Running Tests

### 3.1 Basic Capability Tests (Pillar 1-8)

```bash
# Run all basic capability tests
python run_comprehensive_tests.py

# Run specific capability tests
python tests/test_pillar_01_logic.py
python tests/test_pillar_02_instruction.py
python tests/test_pillar_03_structural.py
```

### 3.2 Advanced Capability Tests (Pillar 9-19)

```bash
# Run all advanced capability tests
python run_advanced_capability_tests.py

# Run specific advanced capability tests
python run_dynamic_role_switching_test.py
python run_massive_consensus_test.py
```

### 3.3 Frontier Capability Tests (Pillar 20-24)

```bash
# Run massive role consensus test
python run_massive_consensus_test.py

# Run dynamic role switching test
python run_dynamic_role_switching_test.py

# Run project management integration test
python tests/test_pillar_22_project_management.py
```

### 3.4 Role Independence Test

```bash
# Run full role independence test
python run_pillar_25_independence.py

# Run quick test
python run_pillar_25_independence.py --quick

# Run batch test
python run_pillar_25_independence.py --batch model1 model2 model3
```

### 3.5 Cloud Service Test

```bash
# Run cloud service independence test
python run_cloud_independence_test.py

# Run cognitive ecosystem cloud test
python run_cognitive_ecosystem_cloud_test.py

# Run extended cloud test
python run_extended_cloud_test.py
```

## 4. Result Analysis

### 4.1 View Test Output

Test results are saved in the `testout/` directory:

```bash
# View test output files
ls testout/

# View test results for a specific model
cat testout/cloud_independence_qwen-max.json
```

### 4.2 Generate Analysis Reports

```bash
# Analyze independence test results
python analyze_results.py

# Evaluate enhanced test results
python evaluate_enhanced_results.py

# Generate visualization report
python visualize_test_results.py
```

### 4.3 Result File Structure

```bash
testout/
├── cloud_independence_<model_name>.json          # Cloud service independence test results
├── cloud_independence_test_results_<timestamp>.json  # Batch test results
├── run_independence_test_<model>_<timestamp>.json    # Detailed independence test results
└── collaboration_case*.txt                         # Collaboration case records
```

## 5. Tool Usage

### 5.1 Architecture Mapping Tool

Generate project architecture mapping:

```bash
python project_architecture_map.py

# Generated files
# - architecture_map.json
# - interface_map.json
```

### 5.2 Test Generator

Generate test code based on interface mapping:

```bash
python enhanced_test_generator.py
```

### 5.3 Smart Test Runner

Manage test status and execution:

```bash
# List available services
python smart_test_runner.py --list-services

# List available models
python smart_test_runner.py --list-models

# Run tests
python smart_test_runner.py --run-tests openai gemini
```

### 5.4 Test Status Management

Reset test status:

```bash
# Reset all test status
python tools/reset_test_status.py --reset-all

# Reset specific service status
python tools/reset_test_status.py --reset-service openai

# View test status
python tools/reset_test_status.py --show-status
```

## 6. Troubleshooting

### 6.1 Model Connection Issues

```bash
# Check Ollama service
python debug_model_call.py

# Check cloud service connectivity
python test_cloud_services.py

# Check specific cloud service
python test_baidu_connectivity.py
```

### 6.2 Configuration Validation

```bash
# Validate system configuration
python run_end_to_end_integration_test.py

# Validate cloud system
python validate_cloud_system.py
```

### 6.3 Common Issues

**Q: Test hangs for a long time without response?**
A: It might be processing a complex task. Check if partial results are generated in the `testout/` directory.

**Q: Cannot connect to cloud service?**
A: Check if the API keys in the `.env` file are correct, and run `test_cloud_services.py` to verify connectivity.

**Q: Inconsistent test results?**
A: Check the model's randomness setting (temperature). It's recommended to use a lower temperature value for testing.

## 7. Best Practices

### 7.1 Testing Strategy

- **Layered Testing**: Run basic capability tests first, then advanced and frontier capability tests
- **Comparative Testing**: Test multiple models with the same tests for performance comparison
- **Repeated Testing**: Run key tests multiple times to ensure result stability

### 7.2 Performance Optimization

- **Batch Testing**: Use batch test scripts to test multiple models simultaneously
- **Result Caching**: Cache results of tested models to avoid retesting
- **Resource Management**: Monitor system resource usage to avoid resource exhaustion

### 7.3 Result Interpretation

- **Quantitative Metrics**: Focus on measurable metrics like success rate and response time
- **Qualitative Analysis**: Deeply analyze the quality, innovation, and consistency of model responses
- **Trend Analysis**: Track model performance trends across different tests to identify improvement directions
