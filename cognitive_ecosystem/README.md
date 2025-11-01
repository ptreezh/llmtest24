# 认知生态系统测试框架

## 概述

认知生态系统测试框架是一个用于测试大语言模型认知多样性和集体智能的综合框架。该框架通过模拟多智能体认知生态系统，评估模型在角色扮演、认知独立性、集体决策等方面的能力。

## 核心特性

### 🧠 四层架构设计
- **基础设施层**: 核心引擎和状态管理
- **认知检测层**: 幻觉、偏见、风格、人格检测
- **生态分析层**: 生态位、韧性、涌现分析
- **对照验证层**: 基线对照和统计验证

### 🔬 四大测试套件
1. **共谋性幻觉检测**: 检测智能体是否会集体认同虚假信息
2. **认知偏见一致性测试**: 评估认知偏见的传播和抵抗能力
3. **问题解决风格差异测试**: 分析不同角色的思维模式差异
4. **纵向人格稳定性测试**: 追踪角色人格的长期一致性

### 📊 生态分析功能
- **认知生态位分析**: 量化每个智能体的认知特征和专业领域
- **系统韧性评估**: 测试生态系统对压力和干扰的抵抗能力
- **集体智能涌现检测**: 识别群体智能超越个体能力的现象

## 快速开始

### 安装依赖

```bash
pip install numpy pandas scikit-learn matplotlib networkx nltk
```

### 基本使用

```python
from cognitive_ecosystem.core.ecosystem_engine import CognitiveEcosystemEngine
from cognitive_ecosystem.core.cognitive_niche import CognitiveNiche

# 1. 创建生态系统
config = {
    'test_roles': ['creator', 'analyst', 'critic', 'synthesizer'],
    'model_name': 'your_model_name'
}
ecosystem = CognitiveEcosystemEngine(config)

# 2. 创建认知生态位
niche = CognitiveNiche(
    agent_id='agent_1',
    role='software_engineer',
    cognitive_style='analytical',
    personality_traits={'openness': 0.8, 'conscientiousness': 0.7}
)

# 3. 计算生态位指标
niche.calculate_specialization_index()
niche.calculate_adaptability_score()
niche.calculate_niche_breadth()

print(f"专业化指数: {niche.metrics.specialization_index:.3f}")
print(f"适应性得分: {niche.metrics.adaptability_score:.3f}")
print(f"生态位宽度: {niche.metrics.niche_breadth:.3f}")
```

### 运行完整测试

```python
from tests.test_pillar_25_cognitive_ecosystem import run_cognitive_ecosystem_test

# 配置测试参数
test_config = {
    'test_roles': ['creator', 'analyst', 'critic', 'synthesizer'],
    'hallucination_database': 'cognitive_ecosystem/data/known_hallucinations.json',
    'bias_test_scenarios': 'cognitive_ecosystem/data/bias_scenarios.json',
    'personality_tracking_duration': 30,
    'resilience_test_intensity': 'high',
    'baseline_comparison_enabled': True,
    'statistical_significance_level': 0.05,
    'visualization_enabled': True
}

# 运行测试
result = run_cognitive_ecosystem_test('your_model_name', test_config)
print(result)
```

## 核心组件详解

### 1. 生态系统引擎 (CognitiveEcosystemEngine)

生态系统的核心管理器，负责智能体注册、交互模拟和状态管理。

```python
from cognitive_ecosystem.core.ecosystem_engine import CognitiveEcosystemEngine

# 初始化引擎
ecosystem = CognitiveEcosystemEngine(config)

# 注册智能体
ecosystem.register_agent('agent_1', agent_instance, role_config)

# 模拟交互
scenario = {'name': 'problem_solving', 'description': '解决复杂问题'}
result = ecosystem.simulate_interaction(scenario)

# 分析认知多样性
diversity = ecosystem.analyze_cognitive_diversity()
```

### 2. 认知生态位 (CognitiveNiche)

表示智能体在认知空间中的位置和特征。

```python
from cognitive_ecosystem.core.cognitive_niche import CognitiveNiche

# 创建生态位
niche = CognitiveNiche(
    agent_id='analyst_1',
    role='data_scientist',
    cognitive_style='analytical',
    personality_traits={
        'openness': 0.9,
        'conscientiousness': 0.8,
        'extraversion': 0.6,
        'agreeableness': 0.7,
        'neuroticism': 0.3
    }
)

# 更新指标
other_niches = [...]  # 其他生态位列表
niche.update_metrics(other_niches)

# 获取摘要
summary = niche.get_niche_summary()
```

### 3. 检测器模块

#### 共谋性幻觉检测器
```python
from cognitive_ecosystem.detectors.hallucination_detector import CollusiveHallucinationDetector

detector = CollusiveHallucinationDetector()

# 注入幻觉
scenario = {'type': 'fake_theory_injection', 'content': '虚假理论'}
injected_content = detector.inject_hallucination(scenario)

# 分析响应
responses = ['response1', 'response2', 'response3']
analysis = detector.analyze_collective_response(responses)
```

#### 认知偏见检测器
```python
from cognitive_ecosystem.detectors.cognitive_bias_detector import CognitiveBiasDetector

detector = CognitiveBiasDetector()

# 设置锚定陷阱
trap = detector.setup_anchoring_trap(100)

# 测量偏见一致性
responses = ['response1', 'response2']
congruence = detector.measure_bias_congruence(responses)
```

### 4. 分析器模块

#### 生态位分析器
```python
from cognitive_ecosystem.analyzers.niche_analyzer import CognitiveNicheAnalyzer

analyzer = CognitiveNicheAnalyzer()

# 计算生态位分化度
niches = [niche1, niche2, niche3]
differentiation = analyzer.calculate_niche_differentiation(niches)

# 测量生态系统多样性
diversity = analyzer.measure_ecosystem_diversity(niches)
```

#### 韧性评估器
```python
from cognitive_ecosystem.analyzers.resilience_assessor import SystemResilienceAssessor

assessor = SystemResilienceAssessor()

# 模拟智能体移除
resilience = assessor.simulate_agent_removal(ecosystem, 'agent_1')

# 施加信息冲击
shock_result = assessor.apply_information_shock(ecosystem, 'misinformation')
```

#### 涌现检测器
```python
from cognitive_ecosystem.analyzers.emergence_detector import EmergenceDetector

detector = EmergenceDetector()

# 检测集体智能
group_performance = [0.8, 0.9, 0.85]
individual_performance = [0.7, 0.6, 0.65]
emergence = detector.detect_collective_intelligence(group_performance, individual_performance)
```

### 5. 基线对照系统

#### 香草智能体
```python
from cognitive_ecosystem.baselines.vanilla_agent import VanillaAgent

# 创建基线智能体
vanilla = VanillaAgent(base_model)

# 生成基线响应
response = vanilla.generate_response("测试提示")

# 运行基线测试
scenarios = [scenario1, scenario2]
results = vanilla.run_baseline_tests(scenarios)
```

#### 统计验证器
```python
from cognitive_ecosystem.baselines.statistical_validator import StatisticalValidator

validator = StatisticalValidator()

# 与基线比较
ecosystem_results = [0.8, 0.9, 0.85]
baseline_results = [0.6, 0.7, 0.65]
comparison = validator.compare_with_baseline(ecosystem_results, baseline_results)

# 计算效应量
effect_size = validator.calculate_effect_size(ecosystem_results, baseline_results)
```

## 配置选项

### 测试配置
```python
COGNITIVE_ECOSYSTEM_CONFIG = {
    'test_roles': ['creator', 'analyst', 'critic', 'synthesizer'],
    'hallucination_database': 'cognitive_ecosystem/data/known_hallucinations.json',
    'bias_test_scenarios': 'cognitive_ecosystem/data/bias_scenarios.json',
    'personality_tracking_duration': 30,  # 天数
    'resilience_test_intensity': 'high',  # low, medium, high
    'baseline_comparison_enabled': True,
    'statistical_significance_level': 0.05,
    'visualization_enabled': True
}
```

### 认知风格选项
- `analytical`: 分析型
- `creative`: 创造型
- `practical`: 实用型
- `systematic`: 系统型
- `intuitive`: 直觉型
- `collaborative`: 协作型
- `critical`: 批判型
- `balanced`: 平衡型

### 角色类型
- `software_engineer`: 软件工程师
- `data_scientist`: 数据科学家
- `product_manager`: 产品经理
- `security_expert`: 安全专家
- `marketing_specialist`: 市场专员
- `financial_analyst`: 金融分析师

## 输出结果解读

### 测试结果结构
```python
{
    'model_name': 'test_model',
    'hallucination_tests': {
        'resistance_score': 0.85,  # 抗幻觉得分 (0-1)
        'detection_rate': 0.92,   # 幻觉检测率
        'false_positive_rate': 0.08  # 误报率
    },
    'bias_tests': {
        'congruence_ratio': 0.3,   # 偏见一致性比例
        'resistance_score': 0.7,   # 偏见抵抗得分
        'bias_types': ['anchoring', 'confirmation']  # 检测到的偏见类型
    },
    'style_tests': {
        'style_diversity': 0.7,    # 风格多样性得分
        'metaphor_diversity': 0.6, # 隐喻多样性
        'domain_spread': 0.8       # 知识领域分布
    },
    'personality_tests': {
        'consistency_score': 0.9,  # 人格一致性得分
        'stability_index': 0.85,   # 稳定性指数
        'drift_detected': False    # 是否检测到人格漂移
    },
    'ecological_analysis': {
        'niche_differentiation': 0.75,  # 生态位分化度
        'system_resilience': 0.8,       # 系统韧性
        'emergence_detected': True,     # 是否检测到涌现
        'collective_intelligence': 0.9  # 集体智能得分
    }
}
```

### 指标解释

#### 抗幻觉得分 (0-1)
- **0.9-1.0**: 优秀，能有效识别和抵制虚假信息
- **0.7-0.9**: 良好，大部分情况下能保持理性
- **0.5-0.7**: 一般，容易受到误导
- **0.0-0.5**: 较差，经常接受虚假信息

#### 认知多样性得分 (0-1)
- **0.8-1.0**: 高度多样化，角色差异明显
- **0.6-0.8**: 中等多样化，有一定差异
- **0.4-0.6**: 低度多样化，角色相似性较高
- **0.0-0.4**: 几乎无差异，可能存在角色塌陷

#### 系统韧性得分 (0-1)
- **0.8-1.0**: 高韧性，能承受各种压力
- **0.6-0.8**: 中等韧性，在一般压力下稳定
- **0.4-0.6**: 低韧性，容易受到干扰
- **0.0-0.4**: 脆弱，轻微干扰即可能崩溃

## 故障排除

### 常见问题

1. **导入错误**
   ```
   ModuleNotFoundError: No module named 'cognitive_ecosystem'
   ```
   解决方案：确保项目根目录在Python路径中
   ```python
   import sys
   sys.path.append('/path/to/testLLM')
   ```

2. **数据文件缺失**
   ```
   FileNotFoundError: known_hallucinations.json not found
   ```
   解决方案：检查数据文件是否存在于`cognitive_ecosystem/data/`目录

3. **内存使用过高**
   - 减少并发智能体数量
   - 禁用可视化功能
   - 使用较小的测试数据集

4. **测试超时**
   - 降低测试强度设置
   - 减少测试持续时间
   - 使用更快的模型

### 性能优化建议

1. **批量处理**: 对于大量测试，使用批量处理模式
2. **缓存机制**: 启用结果缓存以避免重复计算
3. **并行执行**: 在多核系统上启用并行测试
4. **内存管理**: 定期清理不需要的对象

## 扩展开发

### 添加新的检测器

```python
from cognitive_ecosystem.detectors.base_detector import BaseDetector

class CustomDetector(BaseDetector):
    def __init__(self):
        super().__init__()
        # 初始化代码
    
    def detect(self, responses):
        # 检测逻辑
        return detection_result
```

### 添加新的分析器

```python
from cognitive_ecosystem.analyzers.base_analyzer import BaseAnalyzer

class CustomAnalyzer(BaseAnalyzer):
    def __init__(self):
        super().__init__()
        # 初始化代码
    
    def analyze(self, ecosystem_data):
        # 分析逻辑
        return analysis_result
```

## 许可证

本项目采用MIT许可证。详见LICENSE文件。

## 贡献指南

欢迎贡献代码！请遵循以下步骤：

1. Fork本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启Pull Request

## 联系方式

如有问题或建议，请通过以下方式联系：

- 项目Issues: [GitHub Issues](https://github.com/your-repo/issues)
- 邮箱: your-email@example.com

---

**认知生态系统测试框架** - 探索AI认知多样性的前沿工具
