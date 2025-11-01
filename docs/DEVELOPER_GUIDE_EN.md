# LLM Advanced Capability Evaluation Suite - Developer Guide

## 1. Development Environment Setup

### 1.1 Project Structure

```bash
testLLM/
├── core/                  # Core framework
│   ├── config_manager.py  # Configuration management
│   ├── framework.py       # Core framework
│   └── test_orchestrator.py # Test orchestrator
├── tests/                 # Test cases
│   ├── test_pillar_*.py   # Basic capability tests
│   ├── composite_scenarios/ # Composite scenario tests
│   └── generated/         # Generated tests
├── docs/                  # Documentation
├── config/                # Configuration files
├── independence/          # Role independence test module
│   ├── base.py            # Base test class
│   ├── experiments/       # Experiment implementations
│   │   ├── breaking_stress.py
│   │   ├── implicit_cognition.py
│   │   └── longitudinal_consistency.py
│   ├── metrics/           # Metrics calculation
│   └── utils.py           # Utility functions
├── cognitive_ecosystem/   # Cognitive ecosystem module
│   ├── analyzers/         # Analyzers
│   ├── baselines/         # Baseline models
│   ├── core/              # Core components
│   ├── detectors/         # Detectors
│   └── utils/             # Utility functions
├── tools/                 # Tool scripts
├── utils.py               # Global utility functions
└── project_architecture_map.py # Architecture mapping tool
```

### 1.2 Development Dependencies

```bash
# Install development dependencies
pip install -r config/requirements.txt
pip install pytest black flake8 mypy

# Install optional dependencies
pip install pandas matplotlib seaborn openpyxl
```

### 1.3 Environment Variables

Create a `.env` file:

```bash
# API keys
OPENAI_API_KEY=your_key
GEMINI_API_KEY=your_key
DASHSCOPE_API_KEY=your_key

# Development mode
DEV_MODE=true
DEBUG_LOG_LEVEL=DEBUG
```

## 2. Core Architecture

### 2.1 Design Principles

1. **Modular Design**: Each functional module is independent for easy extension and maintenance
2. **Layered Architecture**: Clear hierarchical structure to reduce coupling
3. **Extensibility**: Easy to add new tests and features
4. **Testability**: Code design considers testing requirements

### 2.2 Core Class Design

#### 2.2.1 Base Test Class

The `IndependenceTestBase` class in `independence/base.py`:

```python
class IndependenceTestBase:
    """Base class for all independence tests"""
    
    def __init__(self, config: Dict, model_name: str):
        self.config = config
        self.model_name = model_name
        self.start_time = None
        self.end_time = None
        
    def start_test(self):
        """Start test"""
        self.start_time = datetime.now()
        
    def end_test(self):
        """End test"""
        self.end_time = datetime.now()
        
    def get_test_duration(self) -> float:
        """Get test duration"""
        if self.start_time and self.end_time:
            return (self.end_time - self.start_time).total_seconds()
        return 0.0
        
    def validate_config(self) -> bool:
        """Validate configuration"""
        required_keys = ['model_name', 'test_type']
        return all(key in self.config for key in required_keys)
        
    def _call_model_api(self, prompt: str, system_prompt: str = "") -> str:
        """Call model API"""
        return call_cloud_service(
            self.config.get('service_name', 'ollama'),
            self.model_name,
            prompt,
            system_prompt
        )
        
    def run_experiment(self) -> Dict:
        """Run experiment (must be implemented by subclasses)"""
        raise NotImplementedError("Subclasses must implement this method")
        
    def run_test(self) -> Dict:
        """Run test"""
        self.start_test()
        try:
            result = self.run_experiment()
            result['success'] = True
        except Exception as e:
            result = {
                'success': False,
                'error': str(e),
                'traceback': traceback.format_exc()
            }
        finally:
            self.end_test()
            result['duration'] = self.get_test_duration()
            
        return result
```

#### 2.2.2 Configuration Management

The `ConfigManager` class in `core/config_manager.py`:

```python
class ConfigManager:
    """Configuration manager"""
    
    def __init__(self, config_file: str = "config/config.py"):
        self.config_file = config_file
        self.config = self._load_config()
        
    def _load_config(self) -> Dict:
        """Load configuration"""
        config = {}
        if os.path.exists(self.config_file):
            spec = importlib.util.spec_from_file_location("config", self.config_file)
            config_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(config_module)
            
            # Extract configuration variables
            for attr in dir(config_module):
                if attr.isupper():
                    config[attr.lower()] = getattr(config_module, attr)
                    
        return config
        
    def get_available_models(self) -> List[str]:
        """Get available model list"""
        return self.config.get('models_list_file', [])
        
    def get_default_model(self) -> str:
        """Get default test model"""
        return self.config.get('model_to_test', 'qwen2:7b')
        
    def get_testing_config(self) -> Dict:
        """Get testing configuration"""
        return self.config.get('default_options_creative', {})
        
    def get_independence_config(self) -> Dict:
        """Get independence test configuration"""
        return self.config.get('independence_config', {})
        
    def update_config(self, key: str, value: Any):
        """Update configuration"""
        self.config[key] = value
```

### 2.3 Test Framework

#### 2.3.1 Test Orchestrator

The `TestOrchestrator` class in `core/test_orchestrator.py`:

```python
class TestOrchestrator:
    """Test orchestrator"""
    
    def __init__(self, config_manager: ConfigManager):
        self.config_manager = config_manager
        self.test_status = {}
        
    def execute_test_suite(self, test_suite: str, model_name: str) -> Dict:
        """Execute test suite"""
        if test_suite == "basic":
            return self._execute_basic_tests(model_name)
        elif test_suite == "advanced":
            return self._execute_advanced_tests(model_name)
        elif test_suite == "frontier":
            return self._execute_frontier_tests(model_name)
        elif test_suite == "independence":
            return self._execute_independence_tests(model_name)
        else:
            raise ValueError(f"Unknown test suite: {test_suite}")
            
    def _execute_basic_tests(self, model_name: str) -> Dict:
        """Execute basic tests"""
        results = {}
        basic_tests = [
            'test_pillar_01_logic',
            'test_pillar_02_instruction',
            'test_pillar_03_structural',
            # ... other basic tests
        ]
        
        for test_name in basic_tests:
            try:
                test_module = importlib.import_module(f"tests.{test_name}")
                if hasattr(test_module, 'run_test'):
                    results[test_name] = test_module.run_test(model_name)
            except Exception as e:
                results[test_name] = {
                    'success': False,
                    'error': str(e)
                }
                
        return results
        
    def _execute_advanced_tests(self, model_name: str) -> Dict:
        """Execute advanced tests"""
        # Implement advanced test execution logic
        pass
        
    def _execute_frontier_tests(self, model_name: str) -> Dict:
        """Execute frontier tests"""
        # Implement frontier test execution logic
        pass
        
    def _execute_independence_tests(self, model_name: str) -> Dict:
        """Execute independence tests"""
        from independence.experiments.breaking_stress import BreakingStressTest
        from independence.experiments.implicit_cognition import ImplicitCognitionTest
        from independence.experiments.longitudinal_consistency import LongitudinalConsistencyTest
        
        config = self.config_manager.get_independence_config()
        results = {}
        
        # Breaking stress test
        breaking_test = BreakingStressTest(config, model_name)
        results['breaking_stress'] = breaking_test.run_test()
        
        # Implicit cognition test
        implicit_test = ImplicitCognitionTest(config, model_name)
        results['implicit_cognition'] = implicit_test.run_test()
        
        # Longitudinal consistency test
        longitudinal_test = LongitudinalConsistencyTest(config, model_name)
        results['longitudinal_consistency'] = longitudinal_test.run_test()
        
        return results
```

## 3. Extension Development

### 3.1 Adding New Tests

#### 3.1.1 Create New Test Class

Create a new test file under the `independence/experiments/` directory, for example `new_test.py`:

```python
from independence.base import IndependenceTestBase
from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)

class NewTest(IndependenceTestBase):
    """New test class"""
    
    def __init__(self, config: Dict, model_name: str):
        super().__init__(config, model_name)
        self.test_config = config.get('new_test', {})
        
    def _generate_test_prompts(self) -> List[str]:
        """Generate test prompts"""
        # Implement prompt generation logic
        pass
        
    def _analyze_response(self, response: str) -> Dict:
        """Analyze response"""
        # Implement response analysis logic
        pass
        
    def run_experiment(self) -> Dict:
        """Run experiment"""
        logger.info(f"Starting new test: {self.model_name}")
        
        results = {
            'prompts': [],
            'responses': [],
            'analysis': [],
            'metrics': {}
        }
        
        prompts = self._generate_test_prompts()
        
        for prompt in prompts:
            try:
                response = self._call_model_api(prompt)
                analysis = self._analyze_response(response)
                
                results['prompts'].append(prompt)
                results['responses'].append(response)
                results['analysis'].append(analysis)
                
            except Exception as e:
                logger.error(f"Test execution failed: {e}")
                results['error'] = str(e)
                break
                
        # Calculate metrics
        results['metrics'] = self._calculate_metrics(results)
        
        return results
        
    def _calculate_metrics(self, results: Dict) -> Dict:
        """Calculate test metrics"""
        # Implement metrics calculation logic
        pass
```

#### 3.1.2 Register New Test

Register the new test in `run_pillar_25_independence.py`:

```python
def run_full_test(model_name: str, output_dir: str):
    """Run full test"""
    # ... other tests
    
    # New test
    new_test = NewTest(config, model_name)
    results['new_test'] = new_test.run_test()
    
    # ... save results
```

### 3.2 Extending Cognitive Ecosystem

#### 3.2.1 Add New Detector

Create a new detector under the `cognitive_ecosystem/detectors/` directory, for example `new_detector.py`:

```python
from typing import Dict, List
import logging

logger = logging.getLogger(__name__)

class NewDetector:
    """New detector"""
    
    def __init__(self, config: Dict = None):
        self.config = config or {}
        self.detection_history = []
        
    def detect_new_pattern(self, responses: List[str]) -> Dict:
        """Detect new patterns"""
        result = {
            'detected': False,
            'confidence': 0.0,
            'evidence': [],
            'analysis': {}
        }
        
        # Implement detection logic
        # ...
        
        self.detection_history.append(result)
        return result
        
    def get_detection_statistics(self) -> Dict:
        """Get detection statistics"""
        if not self.detection_history:
            return {}
            
        total_detections = len(self.detection_history)
        positive_detections = sum(1 for d in self.detection_history if d['detected'])
        
        return {
            'total_tests': total_detections,
            'positive_rate': positive_detections / total_detections,
            'average_confidence': sum(d['confidence'] for d in self.detection_history) / total_detections
        }
```

#### 3.2.2 Register New Detector

Register the new detector in `cognitive_ecosystem/__init__.py`:

```python
# Import new detector
from cognitive_ecosystem.detectors.new_detector import NewDetector

# Use new detector in appropriate places
```

### 3.3 Custom Analyzers

#### 3.3.1 Create New Analyzer

Create a new analyzer under the `cognitive_ecosystem/analyzers/` directory, for example `custom_analyzer.py`:

```python
from typing import Dict, List
import numpy as np
import logging

logger = logging.getLogger(__name__)

class CustomAnalyzer:
    """Custom analyzer"""
    
    def __init__(self, config: Dict = None):
        self.config = config or {}
        
    def analyze_response_quality(self, responses: List[str]) -> Dict:
        """Analyze response quality"""
        metrics = {
            'readability': [],
            'coherence': [],
            'relevance': [],
            'creativity': []
        }
        
        for response in responses:
            # Calculate readability
            readability = self._calculate_readability(response)
            metrics['readability'].append(readability)
            
            # Calculate coherence
            coherence = self._calculate_coherence(response)
            metrics['coherence'].append(coherence)
            
            # ... other metrics
            
        # Calculate averages
        avg_metrics = {k: np.mean(v) for k, v in metrics.items()}
        avg_metrics['std_metrics'] = {k: np.std(v) for k, v in metrics.items()}
        
        return avg_metrics
        
    def _calculate_readability(self, text: str) -> float:
        """Calculate readability score"""
        # Implement readability calculation
        pass
        
    def _calculate_coherence(self, text: str) -> float:
        """Calculate coherence score"""
        # Implement coherence calculation
        pass
```

## 4. Test Development

### 4.1 Unit Testing

#### 4.1.1 Test Base Class

Create a test file `test_independence_base.py` under the `tests/` directory:

```python
import unittest
from unittest.mock import Mock, patch
from independence.base import IndependenceTestBase

class MockTest(IndependenceTestBase):
    """Mock class for testing"""
    
    def run_experiment(self):
        return {"test": "result"}

class TestIndependenceTestBase(unittest.TestCase):
    
    def setUp(self):
        self.config = {"test_type": "mock"}
        self.model_name = "test-model"
        self.test_instance = MockTest(self.config, self.model_name)
        
    def test_initialization(self):
        """Test initialization"""
        self.assertEqual(self.test_instance.config, self.config)
        self.assertEqual(self.test_instance.model_name, self.model_name)
        self.assertIsNone(self.test_instance.start_time)
        self.assertIsNone(self.test_instance.end_time)
        
    def test_validate_config_valid(self):
        """Test valid configuration validation"""
        result = self.test_instance.validate_config()
        self.assertTrue(result)
        
    def test_validate_config_invalid(self):
        """Test invalid configuration validation"""
        invalid_test = MockTest({}, self.model_name)
        result = invalid_test.validate_config()
        self.assertFalse(result)
        
    @patch('independence.base.call_cloud_service')
    def test_call_model_api(self, mock_call):
        """Test model API call"""
        mock_call.return_value = "test response"
        result = self.test_instance._call_model_api("test prompt")
        self.assertEqual(result, "test response")
        mock_call.assert_called_once()
        
    def test_run_test_success(self):
        """Test successful execution"""
        result = self.test_instance.run_test()
        self.assertTrue(result['success'])
        self.assertIn('duration', result)
        self.assertGreaterEqual(result['duration'], 0)
        
    def test_run_test_failure(self):
        """Test failed execution"""
        # Mock run_experiment to raise exception
        with patch.object(self.test_instance, 'run_experiment') as mock_exp:
            mock_exp.side_effect = Exception("Test error")
            result = self.test_instance.run_test()
            self.assertFalse(result['success'])
            self.assertIn('error', result)
            self.assertIn('traceback', result)
```

#### 4.1.2 Test Experiment Class

Create a test file `test_new_test.py` under the `tests/generated/` directory:

```python
import unittest
from unittest.mock import Mock, patch
from independence.experiments.new_test import NewTest

class TestNewTest(unittest.TestCase):
    
    def setUp(self):
        self.config = {
            'new_test': {
                'param1': 'value1'
            }
        }
        self.model_name = 'test-model'
        self.test_instance = NewTest(self.config, self.model_name)
        
    def test_initialization(self):
        """Test initialization"""
        self.assertEqual(self.test_instance.config, self.config)
        self.assertEqual(self.test_instance.model_name, self.model_name)
        self.assertEqual(self.test_instance.test_config, self.config['new_test'])
        
    @patch('independence.experiments.new_test.NewTest._generate_test_prompts')
    @patch('independence.experiments.new_test.NewTest._call_model_api')
    @patch('independence.experiments.new_test.NewTest._analyze_response')
    def test_run_experiment_success(self, mock_analyze, mock_call, mock_prompts):
        """Test successful experiment execution"""
        # Set up mock return values
        mock_prompts.return_value = ['prompt1', 'prompt2']
        mock_call.return_value = 'response'
        mock_analyze.return_value = {'analysis': 'result'}
        
        result = self.test_instance.run_experiment()
        
        # Verify results
        self.assertTrue(result['success'])
        self.assertEqual(len(result['prompts']), 2)
        self.assertEqual(len(result['responses']), 2)
        self.assertEqual(len(result['analysis']), 2)
        self.assertIn('metrics', result)
        
    def test_run_experiment_failure(self):
        """Test experiment execution failure"""
        with patch.object(self.test_instance, '_generate_test_prompts') as mock_prompts:
            mock_prompts.side_effect = Exception("Generation error")
            result = self.test_instance.run_experiment()
            self.assertFalse(result['success'])
            self.assertIn('error', result)
```

### 4.2 Integration Testing

#### 4.2.1 Test Orchestrator

Create a test file `test_test_orchestrator.py` under the `tests/` directory:

```python
import unittest
from unittest.mock import Mock, patch
from core.test_orchestrator import TestOrchestrator
from core.config_manager import ConfigManager

class TestTestOrchestrator(unittest.TestCase):
    
    def setUp(self):
        # Create mock ConfigManager
        self.mock_config_manager = Mock(spec=ConfigManager)
        self.mock_config_manager.get_independence_config.return_value = {}
        
        self.orchestrator = TestOrchestrator(self.mock_config_manager)
        
    @patch('core.test_orchestrator.importlib.import_module')
    def test_execute_basic_tests(self, mock_import):
        """Test executing basic tests"""
        # Mock module import
        mock_module = Mock()
        mock_module.run_test.return_value = {'result': 'success'}
        mock_import.return_value = mock_module
        
        results = self.orchestrator._execute_basic_tests('test-model')
        
        # Verify calls
        self.assertGreater(len(results), 0)
        mock_import.assert_called()
        
    @patch('independence.experiments.breaking_stress.BreakingStressTest')
    @patch('independence.experiments.implicit_cognition.ImplicitCognitionTest')
    @patch('independence.experiments.longitudinal_consistency.LongitudinalConsistencyTest')
    def test_execute_independence_tests(self, mock_longitudinal, 
                                      mock_implicit, mock_breaking):
        """Test executing independence tests"""
        # Set up mock return values
        mock_breaking.return_value.run_test.return_value = {'breaking': 'result'}
        mock_implicit.return_value.run_test.return_value = {'implicit': 'result'}
        mock_longitudinal.return_value.run_test.return_value = {'longitudinal': 'result'}
        
        results = self.orchestrator._execute_independence_tests('test-model')
        
        # Verify results
        self.assertIn('breaking_stress', results)
        self.assertIn('implicit_cognition', results)
        self.assertIn('longitudinal_consistency', results)
        
        # Verify calls
        mock_breaking.assert_called_once()
        mock_implicit.assert_called_once()
        mock_longitudinal.assert_called_once()
```

## 5. Debugging and Logging

### 5.1 Debugging Tools

#### 5.1.1 Debug Model Calls

Use the `debug_model_call.py` script:

```python
# debug_model_call.py
import ollama
import time
from config import MODEL_TO_TEST

def test_model_call():
    """Test model call"""
    print(f"Testing model: {MODEL_TO_TEST}")
    
    start_time = time.time()
    try:
        response = ollama.chat(
            model=MODEL_TO_TEST,
            messages=[{'role': 'user', 'content': 'Hello, are you working?'}]
        )
        end_time = time.time()
        
        print(f"✓ Model call successful")
        print(f"Response: {response['message']['content']}")
        print(f"Response time: {end_time - start_time:.2f} seconds")
        
    except Exception as e:
        end_time = time.time()
        print(f"✗ Model call failed: {e}")
        print(f"Duration: {end_time - start_time:.2f} seconds")

if __name__ == "__main__":
    test_model_call()
```

#### 5.1.2 Debug Connectivity

Use the `test_connectivity.py` script:

```python
# test_connectivity.py
import os
import requests
from dotenv import load_dotenv

load_dotenv()

def test_qiniu_connectivity_alternative(verbose=False):
    """Test Qiniu cloud connectivity"""
    url = "https://api.deepseek.com/v1/models"
    api_key = os.getenv("QINIU_API_KEY")
    
    if not api_key:
        print("⚠️  QINIU_API_KEY not set")
        return False
        
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            if verbose:
                print(f"✓ Qiniu cloud connectivity successful: {response.json()}")
            return True
        else:
            if verbose:
                print(f"✗ Qiniu cloud connectivity failed: {response.status_code}")
            return False
    except Exception as e:
        if verbose:
            print(f"✗ Qiniu cloud connectivity exception: {e}")
        return False

if __name__ == "__main__":
    test_qiniu_connectivity_alternative(verbose=True)
```

### 5.2 Logging Configuration

Configure logging in `config.py`:

```python
import logging
import sys
from pathlib import Path

# Create log directory
log_dir = Path("logs")
log_dir.mkdir(exist_ok=True)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_dir / 'app.log'),
        logging.StreamHandler(sys.stdout)
    ]
)

# Get logger
logger = logging.getLogger(__name__)
```

### 5.3 Debugging Techniques

#### 5.3.1 Using Breakpoint Debugging

Add breakpoints in code:

```python
import pdb

def some_function():
    # Code execution will pause here
    pdb.set_trace()
    
    # Or use conditional breakpoints
    if some_condition:
        pdb.set_trace()
        
    # Continue execution...
```

#### 5.3.2 Detailed Logging

Add detailed logging at key points:

```python
import logging

logger = logging.getLogger(__name__)

def complex_function(data):
    logger.debug(f"Starting data processing: {len(data)} items")
    
    try:
        # Processing logic
        result = process_data(data)
        logger.info(f"Data processing completed: {len(result)} results")
        return result
    except Exception as e:
        logger.error(f"Data processing failed: {e}", exc_info=True)
        raise
```

## 6. Best Practices

### 6.1 Code Standards

#### 6.1.1 Naming Conventions

- **Variables and functions**: Use lowercase with underscores `snake_case`
- **Class names**: Use PascalCase
- **Constants**: Use uppercase with underscores `UPPER_CASE`
- **Private members**: Start with single underscore `_private_method`

#### 6.1.2 Code Formatting

Use `black` to format code:

```bash
# Format single file
black my_script.py

# Format entire project
black .

# Check format without modifying
black --check .
```

#### 6.1.3 Type Annotations

Add type annotations to functions and variables:

```python
from typing import Dict, List, Optional

def process_test_results(
    results: List[Dict], 
    threshold: float = 0.8
) -> Dict[str, float]:
    """Process test results"""
    success_count = sum(1 for r in results if r.get('success', False))
    total_count = len(results)
    
    return {
        'success_rate': success_count / total_count if total_count > 0 else 0,
        'threshold_met': success_count / total_count >= threshold
    }
```

### 6.2 Performance Optimization

#### 6.2.1 Asynchronous Processing

For I/O intensive operations, use asynchronous processing:

```python
import asyncio
import aiohttp

class AsyncTestRunner:
    """Asynchronous test runner"""
    
    async def _call_model_async(self, session: aiohttp.ClientSession, 
                               prompt: str) -> str:
        """Asynchronously call model"""
        async with session.post(
            "https://api.example.com/v1/completions",
            json={"prompt": prompt}
        ) as response:
            data = await response.json()
            return data["choices"][0]["text"]
            
    async def run_tests_concurrently(self, prompts: List[str]) -> List[str]:
        """Run tests concurrently"""
        async with aiohttp.ClientSession() as session:
            tasks = [
                self._call_model_async(session, prompt) 
                for prompt in prompts
            ]
            return await asyncio.gather(*tasks)
```

#### 6.2.2 Caching Mechanism

Use caching to avoid redundant calculations:

```python
from functools import lru_cache

class ResultAnalyzer:
    """Result analyzer"""
    
    @lru_cache(maxsize=128)
    def analyze_response_length(self, text: str) -> Dict:
        """Analyze response length (cached result)"""
        words = text.split()
        sentences = text.split('.')
        
        return {
            'word_count': len(words),
            'sentence_count': len(sentences),
            'avg_word_length': sum(len(word) for word in words) / len(words) if words else 0
        }
```

### 6.3 Security Considerations

#### 6.3.1 Input Validation

Validate user input:

```python
import re
from typing import Dict

def validate_model_name(model_name: str) -> bool:
    """Validate model name"""
    # Allow only letters, numbers, hyphens and colons
    pattern = r'^[a-zA-Z0-9\-:]+$'
    return bool(re.match(pattern, model_name))

def sanitize_input(user_input: str) -> str:
    """Sanitize user input"""
    # Remove potentially dangerous characters
    dangerous_chars = ['<', '>', '{', '}', '[', ']', '`', '$']
    for char in dangerous_chars:
        user_input = user_input.replace(char, '')
    return user_input.strip()
```

#### 6.3.2 Error Handling

Implement comprehensive error handling:

```python
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

def safe_execute(func, *args, **kwargs) -> Dict[str, Any]:
    """Safely execute function"""
    try:
        result = func(*args, **kwargs)
        return {
            'success': True,
            'result': result,
            'error': None
        }
    except ConnectionError as e:
        logger.error(f"Connection error: {e}")
        return {
            'success': False,
            'result': None,
            'error': 'connection_error',
            'message': str(e)
        }
    except TimeoutError as e:
        logger.error(f"Timeout error: {e}")
        return {
            'success': False,
            'result': None,
            'error': 'timeout',
            'message': str(e)
        }
    except Exception as e:
        logger.exception(f"Unexpected error: {e}")
        return {
            'success': False,
            'result': None,
            'error': 'unexpected_error',
            'message': str(e)
        }
```

## 7. Version Control

### 7.1 Git Workflow

#### 7.1.1 Branching Strategy

```bash
# Create feature branch
git checkout -b feature/new-test

# Commit after development
git add .
git commit -m "feat: add new test functionality"

# Push to remote
git push origin feature/new-test

# Create Pull Request
# Create PR on GitHub/GitLab to merge into develop branch
```

#### 7.1.2 Commit Message Convention

Use Conventional Commits:

```
<type>(<scope>): <subject>

<body>

<footer>
```

**Types**:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation update
- `style`: Code formatting adjustment
- `refactor`: Code refactoring
- `test`: Testing related
- `chore`: Build process or auxiliary tool changes

**Example**:
```
feat(independence): add enhanced breaking stress test

- Added more stress scenarios
- Optimized result analysis algorithm
- Added new evaluation metrics

Closes #123
```

### 7.2 Release Process

#### 7.2.1 Version Number Convention

Use Semantic Versioning (SemVer):

```
MAJOR.MINOR.PATCH
```

- **MAJOR**: Incompatible API changes
- **MINOR**: Backward compatible feature additions
- **PATCH**: Backward compatible bug fixes

#### 7.2.2 Release Steps

```bash
# 1. Ensure code is up-to-date
git checkout main
git pull origin main

# 2. Create release branch
git checkout -b release/v1.2.0

# 3. Update version number
# Modify version.py or other version file

# 4. Update CHANGELOG
# Add changelog for new version

# 5. Commit release preparation
git add .
git commit -m "chore: prepare v1.2.0 release"

# 6. Push to remote
git push origin release/v1.2.0

# 7. Create Pull Request to main branch

# 8. After merging, tag
git checkout main
git pull origin main
git tag -a v1.2.0 -m "Version v1.2.0"
git push origin v1.2.0

# 9. Create GitHub Release
