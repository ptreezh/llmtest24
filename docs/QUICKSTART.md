# LLM Advanced Testing Suite - Quick Start Guide

This guide will help you get started with the LLM Advanced Testing Suite in just a few minutes.

## 🚀 Quick Start

### 1. Installation

#### Option A: Using the Installation Script (Recommended)
```bash
# For Linux/macOS
chmod +x install.sh
./install.sh

# For Windows
install.bat
```

#### Option B: Manual Installation
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# Linux/macOS:
source venv/bin/activate
# Windows:
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configuration

#### Set Up Environment Variables
```bash
# Copy the environment template
cp config/.env.example config/.env

# Edit the configuration file
nano config/.env  # Linux/macOS
# or
notepad config/.env  # Windows
```

Add your API keys:
```env
# OpenAI Configuration
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_BASE_URL=https://api.openai.com/v1

# OR Google Configuration
GOOGLE_API_KEY=your_google_api_key_here

# OR Local Ollama Configuration
OLLAMA_BASE_URL=http://localhost:11434
```

#### Configure Models
Edit `config/models.txt` to add your model configurations:
```yaml
# Example configurations
openai/gpt-4:
  type: openai
  api_key: ${OPENAI_API_KEY}
  base_url: ${OPENAI_BASE_URL}

google/gemini-pro:
  type: google
  api_key: ${GOOGLE_API_KEY}

local/llama2:
  type: ollama
  model_name: llama2
  base_url: ${OLLAMA_BASE_URL}
```

### 3. Run Your First Test

#### Basic Test
```bash
# Run all tests for a specific model
python scripts/main_orchestrator.py --model openai/gpt-4

# Run specific test pillars
python scripts/main_orchestrator.py --model openai/gpt-4 --test test_pillar_01_logic.py test_pillar_02_instruction.py
```

#### Advanced Tests
```bash
# Run independence tests
python run_pillar_25_independence.py --model openai/gpt-4

# Run cognitive ecosystem tests
python scripts/testing/run_cognitive_ecosystem_cloud_test.py --model openai/gpt-4

# Run comprehensive tests
python run_comprehensive_tests.py --model openai/gpt-4
```

### 4. View Results

Test results are automatically saved to:
- `testout/` - Raw test data
- `results/` - Processed results and reports

View results:
```bash
# View test results
python scripts/analysis/visualize_test_results.py

# Open web interface
python visual_test_interface.py
```

## 📊 Understanding the Test Framework

### 25 Test Pillars

The framework is organized into 4 layers:

#### Foundation Layer (Pillars 1-8)
- **Pillar 1**: Logic reasoning - Basic logical thinking and deduction
- **Pillar 2**: Instruction following - Ability to follow complex instructions
- **Pillar 3**: Structural operations - Working with structured data and formats
- **Pillar 4**: Long context processing - Handling long text sequences
- **Pillar 5**: Domain knowledge - Specialized knowledge in various fields
- **Pillar 6**: Tool use - Using external tools and APIs
- **Pillar 7**: Planning - Strategic thinking and planning abilities
- **Pillar 8**: Metacognition - Thinking about thinking and self-awareness

#### Advanced Layer (Pillars 9-19)
- **Pillar 9**: Creativity - Creative thinking and idea generation
- **Pillar 10**: Math - Mathematical reasoning and problem solving
- **Pillar 11**: Safety - Safety awareness and ethical considerations
- **Pillar 12**: Persona - Role-playing and character consistency
- **Pillar 13**: Initialization - Proper setup and initialization
- **Pillar 14**: Multi-role - Multiple role management
- **Pillar 15**: Collaboration - Teamwork and collaboration
- **Pillar 16**: Emergence - Emergent behaviors and patterns
- **Pillar 17**: DAG generation - Directed acyclic graph generation
- **Pillar 18**: Fault tolerance - Error handling and recovery
- **Pillar 19**: Network analysis - Network thinking and analysis

#### Cutting-Edge Layer (Pillars 20-24)
- **Pillar 20**: Massive consensus - Large-scale consensus building
- **Pillar 21**: Dynamic role switching - Flexible role transitions
- **Pillar 22**: Project management - Project coordination and management
- **Pillar 23**: Parallel task optimization - Concurrent task management
- **Pillar 24**: Multidisciplinary decomposition - Cross-domain problem solving

#### Cognitive Ecosystem (Pillar 25)
- **Pillar 25**: Cognitive ecosystem - Complex multi-agent interactions

### Test Results Structure

Each test produces results in the following format:
```json
{
  "model_name": "openai/gpt-4",
  "test_name": "test_pillar_01_logic",
  "success": true,
  "score": 0.85,
  "details": {
    "response_quality": 0.9,
    "accuracy": 0.8,
    "completeness": 0.85
  },
  "timestamp": "2025-01-15T10:30:00Z",
  "metadata": {
    "test_duration": 45.2,
    "tokens_used": 1250,
    "model_response": "The model's response..."
  }
}
```

## 🔧 Configuration Options

### Environment Variables
```env
# Model API Keys
OPENAI_API_KEY=your_openai_key
GOOGLE_API_KEY=your_google_key
ANTHROPIC_API_KEY=your_anthropic_key

# Model Service URLs
OPENAI_BASE_URL=https://api.openai.com/v1
GOOGLE_BASE_URL=https://generativelanguage.googleapis.com
OLLAMA_BASE_URL=http://localhost:11434

# Logging
LOG_LEVEL=INFO
LOG_DIR=test_logs

# Test Configuration
DEFAULT_MODEL=openai/gpt-4
TEST_TIMEOUT=300
MAX_RETRIES=3
```

### Model Configuration
```yaml
# Add to config/models.txt
your_model_name:
  type: openai  # openai, google, anthropic, ollama
  api_key: ${YOUR_API_KEY}
  base_url: ${YOUR_BASE_URL}
  model: gpt-4  # Model name
  max_tokens: 4000
  temperature: 0.7
```

## 🎯 Common Use Cases

### 1. Model Comparison
```bash
# Compare multiple models
python scripts/main_orchestrator.py --model openai/gpt-4 google/gemini-pro local/llama2
```

### 2. Specific Capability Testing
```bash
# Test only reasoning capabilities
python scripts/main_orchestrator.py --model your_model --test test_pillar_01_logic.py test_pillar_07_planning.py

# Test role-playing capabilities
python scripts/main_orchestrator.py --model your_model --test test_pillar_12_persona.py test_pillar_14_multi_role.py
```

### 3. Advanced Testing
```bash
# Run independence tests
python run_pillar_25_independence.py --model your_model --quick-mode

# Run cognitive ecosystem tests
python scripts/testing/run_cognitive_ecosystem_cloud_test.py --model your_model
```

## 🚨 Troubleshooting

### Common Issues

#### 1. Import Errors
```bash
# Ensure you're in the right directory
cd /path/to/llmtest24

# Activate virtual environment
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows
```

#### 2. API Key Issues
```bash
# Check your environment variables
echo $OPENAI_API_KEY  # Linux/macOS
echo %OPENAI_API_KEY%  # Windows

# Verify API key format
# Should start with 'sk-' for OpenAI, 'AIza' for Google, etc.
```

#### 3. Model Connection Issues
```bash
# Test model connectivity
python check_cloud_connectivity.py

# Check model configuration
python scripts/utils/check_models.py
```

#### 4. Memory Issues
```bash
# Clear test output directory
rm -rf testout/*
# or Windows
rmdir /s /q testout

# Reduce test batch size
python scripts/main_orchestrator.py --model your_model --batch-size 1
```

## 📚 Next Steps

### 1. Explore the Documentation
- [Project Overview](docs/PROJECT_OVERVIEW.md)
- [Developer Guide](docs/DEVELOPER_GUIDE_EN.md)
- [Architecture Documentation](docs/PROJECT_ARCHITECTURE_EN.md)
- [User Guide](docs/USER_GUIDE_EN.md)

### 2. Join the Community
- GitHub Discussions: [Join discussions](https://github.com/ptreezh/llmtest24/discussions)
- Issues: [Report bugs](https://github.com/ptreezh/llmtest24/issues)

### 3. Contribute
- Read [Contributing Guidelines](CONTRIBUTING.md)
- Start with simple issues
- Add new test cases
- Improve documentation

---

🎉 **Welcome to the LLM Advanced Testing Suite!**