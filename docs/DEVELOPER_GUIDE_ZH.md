# LLM高级能力测评套件 - 开发者手册

## 1. 开发环境设置

### 1.1 项目结构

```bash
testLLM/
├── core/                  # 核心框架
│   ├── config_manager.py  # 配置管理
│   ├── framework.py       # 核心框架
│   └── test_orchestrator.py # 测试编排器
├── tests/                 # 测试用例
│   ├── test_pillar_*.py   # 基础能力测试
│   ├── composite_scenarios/ # 复合场景测试
│   └── generated/         # 生成的测试
├── docs/                  # 文档
├── config/                # 配置文件
├── independence/          # 角色独立性测试模块
│   ├── base.py            # 基础测试类
│   ├── experiments/       # 实验实现
│   │   ├── breaking_stress.py
│   │   ├── implicit_cognition.py
│   │   └── longitudinal_consistency.py
│   ├── metrics/           # 指标计算
│   └── utils.py           # 工具函数
├── cognitive_ecosystem/   # 认知生态系统模块
│   ├── analyzers/         # 分析器
│   ├── baselines/         # 基线模型
│   ├── core/              # 核心组件
│   ├── detectors/         # 探测器
│   └── utils/             # 工具函数
├── tools/                 # 工具脚本
├── utils.py               # 全局工具函数
└── project_architecture_map.py # 架构映射工具
```

### 1.2 开发依赖

```bash
# 安装开发依赖
pip install -r config/requirements.txt
pip install pytest black flake8 mypy

# 安装可选依赖
pip install pandas matplotlib seaborn openpyxl
```

### 1.3 环境变量

创建 `.env` 文件：

```bash
# API密钥
OPENAI_API_KEY=your_key
GEMINI_API_KEY=your_key
DASHSCOPE_API_KEY=your_key

# 开发模式
DEV_MODE=true
DEBUG_LOG_LEVEL=DEBUG
```

## 2. 核心架构

### 2.1 设计原则

1. **模块化设计**：各功能模块独立，便于扩展和维护
2. **分层架构**：清晰的层次结构，降低耦合度
3. **可扩展性**：易于添加新测试和功能
4. **可测试性**：代码设计考虑测试需求

### 2.2 核心类设计

#### 2.2.1 测试基类

`independence/base.py` 中的 `IndependenceTestBase` 类：

```python
class IndependenceTestBase:
    """所有独立性测试的基础类"""
    
    def __init__(self, config: Dict, model_name: str):
        self.config = config
        self.model_name = model_name
        self.start_time = None
        self.end_time = None
        
    def start_test(self):
        """开始测试"""
        self.start_time = datetime.now()
        
    def end_test(self):
        """结束测试"""
        self.end_time = datetime.now()
        
    def get_test_duration(self) -> float:
        """获取测试时长"""
        if self.start_time and self.end_time:
            return (self.end_time - self.start_time).total_seconds()
        return 0.0
        
    def validate_config(self) -> bool:
        """验证配置"""
        required_keys = ['model_name', 'test_type']
        return all(key in self.config for key in required_keys)
        
    def _call_model_api(self, prompt: str, system_prompt: str = "") -> str:
        """调用模型API"""
        return call_cloud_service(
            self.config.get('service_name', 'ollama'),
            self.model_name,
            prompt,
            system_prompt
        )
        
    def run_experiment(self) -> Dict:
        """运行实验（子类必须实现）"""
        raise NotImplementedError("子类必须实现此方法")
        
    def run_test(self) -> Dict:
        """运行测试"""
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

#### 2.2.2 配置管理

`core/config_manager.py` 中的 `ConfigManager` 类：

```python
class ConfigManager:
    """配置管理器"""
    
    def __init__(self, config_file: str = "config/config.py"):
        self.config_file = config_file
        self.config = self._load_config()
        
    def _load_config(self) -> Dict:
        """加载配置"""
        config = {}
        if os.path.exists(self.config_file):
            spec = importlib.util.spec_from_file_location("config", self.config_file)
            config_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(config_module)
            
            # 提取配置变量
            for attr in dir(config_module):
                if attr.isupper():
                    config[attr.lower()] = getattr(config_module, attr)
                    
        return config
        
    def get_available_models(self) -> List[str]:
        """获取可用模型列表"""
        return self.config.get('models_list_file', [])
        
    def get_default_model(self) -> str:
        """获取默认测试模型"""
        return self.config.get('model_to_test', 'qwen2:7b')
        
    def get_testing_config(self) -> Dict:
        """获取测试配置"""
        return self.config.get('default_options_creative', {})
        
    def get_independence_config(self) -> Dict:
        """获取独立性测试配置"""
        return self.config.get('independence_config', {})
        
    def update_config(self, key: str, value: Any):
        """更新配置"""
        self.config[key] = value
```

### 2.3 测试框架

#### 2.3.1 测试编排器

`core/test_orchestrator.py` 中的 `TestOrchestrator` 类：

```python
class TestOrchestrator:
    """测试编排器"""
    
    def __init__(self, config_manager: ConfigManager):
        self.config_manager = config_manager
        self.test_status = {}
        
    def execute_test_suite(self, test_suite: str, model_name: str) -> Dict:
        """执行测试套件"""
        if test_suite == "basic":
            return self._execute_basic_tests(model_name)
        elif test_suite == "advanced":
            return self._execute_advanced_tests(model_name)
        elif test_suite == "frontier":
            return self._execute_frontier_tests(model_name)
        elif test_suite == "independence":
            return self._execute_independence_tests(model_name)
        else:
            raise ValueError(f"未知的测试套件: {test_suite}")
            
    def _execute_basic_tests(self, model_name: str) -> Dict:
        """执行基础测试"""
        results = {}
        basic_tests = [
            'test_pillar_01_logic',
            'test_pillar_02_instruction',
            'test_pillar_03_structural',
            # ... 其他基础测试
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
        """执行高级测试"""
        # 实现高级测试执行逻辑
        pass
        
    def _execute_frontier_tests(self, model_name: str) -> Dict:
        """执行前沿测试"""
        # 实现前沿测试执行逻辑
        pass
        
    def _execute_independence_tests(self, model_name: str) -> Dict:
        """执行独立性测试"""
        from independence.experiments.breaking_stress import BreakingStressTest
        from independence.experiments.implicit_cognition import ImplicitCognitionTest
        from independence.experiments.longitudinal_consistency import LongitudinalConsistencyTest
        
        config = self.config_manager.get_independence_config()
        results = {}
        
        # 破功测试
        breaking_test = BreakingStressTest(config, model_name)
        results['breaking_stress'] = breaking_test.run_test()
        
        # 隐式认知测试
        implicit_test = ImplicitCognitionTest(config, model_name)
        results['implicit_cognition'] = implicit_test.run_test()
        
        # 纵向一致性测试
        longitudinal_test = LongitudinalConsistencyTest(config, model_name)
        results['longitudinal_consistency'] = longitudinal_test.run_test()
        
        return results
```

## 3. 扩展开发

### 3.1 添加新测试

#### 3.1.1 创建新测试类

在 `independence/experiments/` 目录下创建新测试文件，例如 `new_test.py`：

```python
from independence.base import IndependenceTestBase
from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)

class NewTest(IndependenceTestBase):
    """新测试类"""
    
    def __init__(self, config: Dict, model_name: str):
        super().__init__(config, model_name)
        self.test_config = config.get('new_test', {})
        
    def _generate_test_prompts(self) -> List[str]:
        """生成测试提示"""
        # 实现提示生成逻辑
        pass
        
    def _analyze_response(self, response: str) -> Dict:
        """分析响应"""
        # 实现响应分析逻辑
        pass
        
    def run_experiment(self) -> Dict:
        """运行实验"""
        logger.info(f"开始执行新测试: {self.model_name}")
        
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
                logger.error(f"测试执行失败: {e}")
                results['error'] = str(e)
                break
                
        # 计算指标
        results['metrics'] = self._calculate_metrics(results)
        
        return results
        
    def _calculate_metrics(self, results: Dict) -> Dict:
        """计算测试指标"""
        # 实现指标计算逻辑
        pass
```

#### 3.1.2 注册新测试

在 `run_pillar_25_independence.py` 中注册新测试：

```python
def run_full_test(model_name: str, output_dir: str):
    """运行完整测试"""
    # ... 其他测试
    
    # 新测试
    new_test = NewTest(config, model_name)
    results['new_test'] = new_test.run_test()
    
    # ... 保存结果
```

### 3.2 扩展认知生态系统

#### 3.2.1 添加新探测器

在 `cognitive_ecosystem/detectors/` 目录下创建新探测器，例如 `new_detector.py`：

```python
from typing import Dict, List
import logging

logger = logging.getLogger(__name__)

class NewDetector:
    """新探测器"""
    
    def __init__(self, config: Dict = None):
        self.config = config or {}
        self.detection_history = []
        
    def detect_new_pattern(self, responses: List[str]) -> Dict:
        """检测新模式"""
        result = {
            'detected': False,
            'confidence': 0.0,
            'evidence': [],
            'analysis': {}
        }
        
        # 实现检测逻辑
        # ...
        
        self.detection_history.append(result)
        return result
        
    def get_detection_statistics(self) -> Dict:
        """获取检测统计"""
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

#### 3.2.2 注册新探测器

在 `cognitive_ecosystem/__init__.py` 中注册新探测器：

```python
# 导入新探测器
from cognitive_ecosystem.detectors.new_detector import NewDetector

# 在适当位置使用新探测器
```

### 3.3 自定义分析器

#### 3.3.1 创建新分析器

在 `cognitive_ecosystem/analyzers/` 目录下创建新分析器，例如 `custom_analyzer.py`：

```python
from typing import Dict, List
import numpy as np
import logging

logger = logging.getLogger(__name__)

class CustomAnalyzer:
    """自定义分析器"""
    
    def __init__(self, config: Dict = None):
        self.config = config or {}
        
    def analyze_response_quality(self, responses: List[str]) -> Dict:
        """分析响应质量"""
        metrics = {
            'readability': [],
            'coherence': [],
            'relevance': [],
            'creativity': []
        }
        
        for response in responses:
            # 计算可读性
            readability = self._calculate_readability(response)
            metrics['readability'].append(readability)
            
            # 计算连贯性
            coherence = self._calculate_coherence(response)
            metrics['coherence'].append(coherence)
            
            # ... 其他指标
            
        # 计算平均值
        avg_metrics = {k: np.mean(v) for k, v in metrics.items()}
        avg_metrics['std_metrics'] = {k: np.std(v) for k, v in metrics.items()}
        
        return avg_metrics
        
    def _calculate_readability(self, text: str) -> float:
        """计算可读性分数"""
        # 实现可读性计算
        pass
        
    def _calculate_coherence(self, text: str) -> float:
        """计算连贯性分数"""
        # 实现连贯性计算
        pass
```

## 4. 测试开发

### 4.1 单元测试

#### 4.1.1 测试基础类

在 `tests/` 目录下创建测试文件 `test_independence_base.py`：

```python
import unittest
from unittest.mock import Mock, patch
from independence.base import IndependenceTestBase

class MockTest(IndependenceTestBase):
    """用于测试的模拟类"""
    
    def run_experiment(self):
        return {"test": "result"}

class TestIndependenceTestBase(unittest.TestCase):
    
    def setUp(self):
        self.config = {"test_type": "mock"}
        self.model_name = "test-model"
        self.test_instance = MockTest(self.config, self.model_name)
        
    def test_initialization(self):
        """测试初始化"""
        self.assertEqual(self.test_instance.config, self.config)
        self.assertEqual(self.test_instance.model_name, self.model_name)
        self.assertIsNone(self.test_instance.start_time)
        self.assertIsNone(self.test_instance.end_time)
        
    def test_validate_config_valid(self):
        """测试有效配置验证"""
        result = self.test_instance.validate_config()
        self.assertTrue(result)
        
    def test_validate_config_invalid(self):
        """测试无效配置验证"""
        invalid_test = MockTest({}, self.model_name)
        result = invalid_test.validate_config()
        self.assertFalse(result)
        
    @patch('independence.base.call_cloud_service')
    def test_call_model_api(self, mock_call):
        """测试模型API调用"""
        mock_call.return_value = "test response"
        result = self.test_instance._call_model_api("test prompt")
        self.assertEqual(result, "test response")
        mock_call.assert_called_once()
        
    def test_run_test_success(self):
        """测试成功执行"""
        result = self.test_instance.run_test()
        self.assertTrue(result['success'])
        self.assertIn('duration', result)
        self.assertGreaterEqual(result['duration'], 0)
        
    def test_run_test_failure(self):
        """测试失败执行"""
        # 模拟run_experiment抛出异常
        with patch.object(self.test_instance, 'run_experiment') as mock_exp:
            mock_exp.side_effect = Exception("Test error")
            result = self.test_instance.run_test()
            self.assertFalse(result['success'])
            self.assertIn('error', result)
            self.assertIn('traceback', result)
```

#### 4.1.2 测试实验类

在 `tests/generated/` 目录下创建测试文件 `test_new_test.py`：

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
        """测试初始化"""
        self.assertEqual(self.test_instance.config, self.config)
        self.assertEqual(self.test_instance.model_name, self.model_name)
        self.assertEqual(self.test_instance.test_config, self.config['new_test'])
        
    @patch('independence.experiments.new_test.NewTest._generate_test_prompts')
    @patch('independence.experiments.new_test.NewTest._call_model_api')
    @patch('independence.experiments.new_test.NewTest._analyze_response')
    def test_run_experiment_success(self, mock_analyze, mock_call, mock_prompts):
        """测试成功执行实验"""
        # 设置模拟返回值
        mock_prompts.return_value = ['prompt1', 'prompt2']
        mock_call.return_value = 'response'
        mock_analyze.return_value = {'analysis': 'result'}
        
        result = self.test_instance.run_experiment()
        
        # 验证结果
        self.assertTrue(result['success'])
        self.assertEqual(len(result['prompts']), 2)
        self.assertEqual(len(result['responses']), 2)
        self.assertEqual(len(result['analysis']), 2)
        self.assertIn('metrics', result)
        
    def test_run_experiment_failure(self):
        """测试执行失败"""
        with patch.object(self.test_instance, '_generate_test_prompts') as mock_prompts:
            mock_prompts.side_effect = Exception("Generation error")
            result = self.test_instance.run_experiment()
            self.assertFalse(result['success'])
            self.assertIn('error', result)
```

### 4.2 集成测试

#### 4.2.1 测试编排器

在 `tests/` 目录下创建测试文件 `test_test_orchestrator.py`：

```python
import unittest
from unittest.mock import Mock, patch
from core.test_orchestrator import TestOrchestrator
from core.config_manager import ConfigManager

class TestTestOrchestrator(unittest.TestCase):
    
    def setUp(self):
        # 创建模拟的ConfigManager
        self.mock_config_manager = Mock(spec=ConfigManager)
        self.mock_config_manager.get_independence_config.return_value = {}
        
        self.orchestrator = TestOrchestrator(self.mock_config_manager)
        
    @patch('core.test_orchestrator.importlib.import_module')
    def test_execute_basic_tests(self, mock_import):
        """测试执行基础测试"""
        # 模拟导入模块
        mock_module = Mock()
        mock_module.run_test.return_value = {'result': 'success'}
        mock_import.return_value = mock_module
        
        results = self.orchestrator._execute_basic_tests('test-model')
        
        # 验证调用
        self.assertGreater(len(results), 0)
        mock_import.assert_called()
        
    @patch('independence.experiments.breaking_stress.BreakingStressTest')
    @patch('independence.experiments.implicit_cognition.ImplicitCognitionTest')
    @patch('independence.experiments.longitudinal_consistency.LongitudinalConsistencyTest')
    def test_execute_independence_tests(self, mock_longitudinal, 
                                      mock_implicit, mock_breaking):
        """测试执行独立性测试"""
        # 设置模拟返回值
        mock_breaking.return_value.run_test.return_value = {'breaking': 'result'}
        mock_implicit.return_value.run_test.return_value = {'implicit': 'result'}
        mock_longitudinal.return_value.run_test.return_value = {'longitudinal': 'result'}
        
        results = self.orchestrator._execute_independence_tests('test-model')
        
        # 验证结果
        self.assertIn('breaking_stress', results)
        self.assertIn('implicit_cognition', results)
        self.assertIn('longitudinal_consistency', results)
        
        # 验证调用
        mock_breaking.assert_called_once()
        mock_implicit.assert_called_once()
        mock_longitudinal.assert_called_once()
```

## 5. 调试与日志

### 5.1 调试工具

#### 5.1.1 调试模型调用

使用 `debug_model_call.py` 脚本：

```python
# debug_model_call.py
import ollama
import time
from config import MODEL_TO_TEST

def test_model_call():
    """测试模型调用"""
    print(f"测试模型: {MODEL_TO_TEST}")
    
    start_time = time.time()
    try:
        response = ollama.chat(
            model=MODEL_TO_TEST,
            messages=[{'role': 'user', 'content': 'Hello, are you working?'}]
        )
        end_time = time.time()
        
        print(f"✓ 模型调用成功")
        print(f"响应: {response['message']['content']}")
        print(f"响应时间: {end_time - start_time:.2f}秒")
        
    except Exception as e:
        end_time = time.time()
        print(f"✗ 模型调用失败: {e}")
        print(f"耗时: {end_time - start_time:.2f}秒")

if __name__ == "__main__":
    test_model_call()
```

#### 5.1.2 调试连接性

使用 `test_connectivity.py` 脚本：

```python
# test_connectivity.py
import os
import requests
from dotenv import load_dotenv

load_dotenv()

def test_qiniu_connectivity_alternative(verbose=False):
    """测试七牛云连接性"""
    url = "https://api.deepseek.com/v1/models"
    api_key = os.getenv("QINIU_API_KEY")
    
    if not api_key:
        print("⚠️  QINIU_API_KEY 未设置")
        return False
        
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            if verbose:
                print(f"✓ 七牛云连接成功: {response.json()}")
            return True
        else:
            if verbose:
                print(f"✗ 七牛云连接失败: {response.status_code}")
            return False
    except Exception as e:
        if verbose:
            print(f"✗ 七牛云连接异常: {e}")
        return False

if __name__ == "__main__":
    test_qiniu_connectivity_alternative(verbose=True)
```

### 5.2 日志配置

在 `config.py` 中配置日志：

```python
import logging
import sys
from pathlib import Path

# 创建日志目录
log_dir = Path("logs")
log_dir.mkdir(exist_ok=True)

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_dir / 'app.log'),
        logging.StreamHandler(sys.stdout)
    ]
)

# 获取日志记录器
logger = logging.getLogger(__name__)
```

### 5.3 调试技巧

#### 5.3.1 使用断点调试

在代码中添加断点：

```python
import pdb

def some_function():
    # 代码执行到此处会暂停
    pdb.set_trace()
    
    # 或者使用条件断点
    if some_condition:
        pdb.set_trace()
        
    # 继续执行...
```

#### 5.3.2 详细日志记录

在关键位置添加详细日志：

```python
import logging

logger = logging.getLogger(__name__)

def complex_function(data):
    logger.debug(f"开始处理数据: {len(data)} 项")
    
    try:
        # 处理逻辑
        result = process_data(data)
        logger.info(f"数据处理完成: {len(result)} 结果")
        return result
    except Exception as e:
        logger.error(f"数据处理失败: {e}", exc_info=True)
        raise
```

## 6. 最佳实践

### 6.1 代码规范

#### 6.1.1 命名规范

- **变量和函数**: 使用小写字母和下划线 `snake_case`
- **类名**: 使用驼峰命名法 `PascalCase`
- **常量**: 使用大写字母和下划线 `UPPER_CASE`
- **私有成员**: 以单下划线开头 `_private_method`

#### 6.1.2 代码格式化

使用 `black` 格式化代码：

```bash
# 格式化单个文件
black my_script.py

# 格式化整个项目
black .

# 检查格式但不修改
black --check .
```

#### 6.1.3 类型注解

为函数和变量添加类型注解：

```python
from typing import Dict, List, Optional

def process_test_results(
    results: List[Dict], 
    threshold: float = 0.8
) -> Dict[str, float]:
    """处理测试结果"""
    success_count = sum(1 for r in results if r.get('success', False))
    total_count = len(results)
    
    return {
        'success_rate': success_count / total_count if total_count > 0 else 0,
        'threshold_met': success_count / total_count >= threshold
    }
```

### 6.2 性能优化

#### 6.2.1 异步处理

对于I/O密集型操作，使用异步处理：

```python
import asyncio
import aiohttp

class AsyncTestRunner:
    """异步测试运行器"""
    
    async def _call_model_async(self, session: aiohttp.ClientSession, 
                               prompt: str) -> str:
        """异步调用模型"""
        async with session.post(
            "https://api.example.com/v1/completions",
            json={"prompt": prompt}
        ) as response:
            data = await response.json()
            return data["choices"][0]["text"]
            
    async def run_tests_concurrently(self, prompts: List[str]) -> List[str]:
        """并发运行测试"""
        async with aiohttp.ClientSession() as session:
            tasks = [
                self._call_model_async(session, prompt) 
                for prompt in prompts
            ]
            return await asyncio.gather(*tasks)
```

#### 6.2.2 缓存机制

使用缓存避免重复计算：

```python
from functools import lru_cache

class ResultAnalyzer:
    """结果分析器"""
    
    @lru_cache(maxsize=128)
    def analyze_response_length(self, text: str) -> Dict:
        """分析响应长度（缓存结果）"""
        words = text.split()
        sentences = text.split('.')
        
        return {
            'word_count': len(words),
            'sentence_count': len(sentences),
            'avg_word_length': sum(len(word) for word in words) / len(words) if words else 0
        }
```

### 6.3 安全考虑

#### 6.3.1 输入验证

对用户输入进行验证：

```python
import re
from typing import Dict

def validate_model_name(model_name: str) -> bool:
    """验证模型名称"""
    # 只允许字母、数字、连字符和冒号
    pattern = r'^[a-zA-Z0-9\-:]+$'
    return bool(re.match(pattern, model_name))

def sanitize_input(user_input: str) -> str:
    """清理用户输入"""
    # 移除潜在的危险字符
    dangerous_chars = ['<', '>', '{', '}', '[', ']', '`', '$']
    for char in dangerous_chars:
        user_input = user_input.replace(char, '')
    return user_input.strip()
```

#### 6.3.2 错误处理

完善的错误处理机制：

```python
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

def safe_execute(func, *args, **kwargs) -> Dict[str, Any]:
    """安全执行函数"""
    try:
        result = func(*args, **kwargs)
        return {
            'success': True,
            'result': result,
            'error': None
        }
    except ConnectionError as e:
        logger.error(f"连接错误: {e}")
        return {
            'success': False,
            'result': None,
            'error': 'connection_error',
            'message': str(e)
        }
    except TimeoutError as e:
        logger.error(f"超时错误: {e}")
        return {
            'success': False,
            'result': None,
            'error': 'timeout',
            'message': str(e)
        }
    except Exception as e:
        logger.exception(f"未预期的错误: {e}")
        return {
            'success': False,
            'result': None,
            'error': 'unexpected_error',
            'message': str(e)
        }
```

## 7. 版本控制

### 7.1 Git工作流

#### 7.1.1 分支策略

```bash
# 创建功能分支
git checkout -b feature/new-test

# 开发完成后提交
git add .
git commit -m "feat: 添加新测试功能"

# 推送到远程
git push origin feature/new-test

# 创建Pull Request
# 在GitHub/GitLab上创建PR，请求合并到develop分支
```

#### 7.1.2 提交信息规范

使用约定式提交（Conventional Commits）：

```
<type>(<scope>): <subject>

<body>

<footer>
```

**类型（type）**:
- `feat`: 新功能
- `fix`: 修复bug
- `docs`: 文档更新
- `style`: 代码格式调整
- `refactor`: 代码重构
- `test`: 测试相关
- `chore`: 构建过程或辅助工具的变动

**示例**:
```
feat(independence): 添加破功测试增强功能

- 增加了更多压力场景
- 优化了结果分析算法
- 添加了新的评估指标

Closes #123
```

### 7.2 发布流程

#### 7.2.1 版本号规范

使用语义化版本控制（SemVer）：

```
MAJOR.MINOR.PATCH
```

- **MAJOR**: 不兼容的API更改
- **MINOR**: 向后兼容的功能添加
- **PATCH**: 向后兼容的问题修复

#### 7.2.2 发布步骤

```bash
# 1. 确保代码是最新的
git checkout main
git pull origin main

# 2. 创建发布分支
git checkout -b release/v1.2.0

# 3. 更新版本号
# 修改 version.py 或其他版本文件

# 4. 更新CHANGELOG
# 添加新版本的变更日志

# 5. 提交发布准备
git add .
git commit -m "chore: 准备v1.2.0发布"

# 6. 推送到远程
git push origin release/v1.2.0

# 7. 创建Pull Request到main分支

# 8. 合并后打标签
git checkout main
git pull origin main
git tag -a v1.2.0 -m "版本v1.2.0"
git push origin v1.2.0

# 9. 创建GitHub Release
