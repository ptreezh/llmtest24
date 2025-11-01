# 认知生态系统测试框架 - 快速使用指南

## 🚀 快速开始

### 1. 环境准备

确保已安装必要的依赖：
```bash
pip install numpy pandas scikit-learn matplotlib networkx nltk
```

### 2. 基础测试

运行一个简单的认知生态系统测试：

```python
import sys
sys.path.append('.')

from cognitive_ecosystem.core.ecosystem_engine import CognitiveEcosystemEngine
from cognitive_ecosystem.core.cognitive_niche import CognitiveNiche

# 创建生态系统
config = {'test_roles': ['creator', 'analyst', 'critic']}
ecosystem = CognitiveEcosystemEngine(config)

# 创建认知生态位
niche = CognitiveNiche(
    agent_id='test_agent',
    role='software_engineer',
    cognitive_style='analytical',
    personality_traits={'openness': 0.8, 'conscientiousness': 0.7}
)

# 计算指标
niche.calculate_specialization_index()
niche.calculate_adaptability_score()
niche.calculate_niche_breadth()

print(f"专业化指数: {niche.metrics.specialization_index:.3f}")
print(f"适应性得分: {niche.metrics.adaptability_score:.3f}")
print(f"生态位宽度: {niche.metrics.niche_breadth:.3f}")
```

### 3. 完整测试流程

运行完整的认知生态系统测试：

```python
from tests.test_pillar_25_cognitive_ecosystem import run_cognitive_ecosystem_test

# 配置测试参数
test_config = {
    'test_roles': ['creator', 'analyst', 'critic', 'synthesizer'],
    'hallucination_database': 'cognitive_ecosystem/data/known_hallucinations.json',
    'bias_test_scenarios': 'cognitive_ecosystem/data/bias_scenarios.json',
    'personality_tracking_duration': 30,
    'resilience_test_intensity': 'medium',
    'baseline_comparison_enabled': True,
    'statistical_significance_level': 0.05,
    'visualization_enabled': False  # 设为False以提高性能
}

# 运行测试
result = run_cognitive_ecosystem_test('your_model_name', test_config)

# 查看结果
print("=== 测试结果 ===")
for key, value in result.items():
    print(f"{key}: {value}")
```

## 📊 核心功能演示

### 1. 幻觉检测测试

```python
from cognitive_ecosystem.detectors.hallucination_detector import CollusiveHallucinationDetector

# 初始化检测器
detector = CollusiveHallucinationDetector()

# 注入虚假信息
scenario = {
    'type': 'fake_theory_injection',
    'content': '马斯洛的前馈激励理论表明...'
}
injected_content = detector.inject_hallucination(scenario)
print(f"注入的幻觉内容: {injected_content}")

# 分析集体响应
responses = [
    "这个理论确实很有道理...",
    "我不太确定这个理论的准确性...",
    "根据我的知识，这个理论可能不存在..."
]
analysis = detector.analyze_collective_response(responses)
print(f"集体响应分析: {analysis}")
```

### 2. 认知偏见测试

```python
from cognitive_ecosystem.detectors.cognitive_bias_detector import CognitiveBiasDetector

# 初始化偏见检测器
bias_detector = CognitiveBiasDetector()

# 设置锚定效应陷阱
anchor_value = 100
trap_content = bias_detector.setup_anchoring_trap(anchor_value)
print(f"锚定陷阱: {trap_content}")

# 测量偏见一致性
responses = [
    "我估计答案大约是95左右",
    "应该在90-110之间",
    "我觉得可能是105"
]
congruence = bias_detector.measure_bias_congruence(responses)
print(f"偏见一致性: {congruence}")
```

### 3. 生态位分析

```python
from cognitive_ecosystem.analyzers.niche_analyzer import CognitiveNicheAnalyzer

# 创建多个生态位
niches = []
roles = ['software_engineer', 'data_scientist', 'product_manager']
styles = ['analytical', 'creative', 'practical']

for i, (role, style) in enumerate(zip(roles, styles)):
    niche = CognitiveNiche(
        agent_id=f'agent_{i}',
        role=role,
        cognitive_style=style,
        personality_traits={'openness': 0.8, 'conscientiousness': 0.7}
    )
    niches.append(niche)

# 分析生态位
analyzer = CognitiveNicheAnalyzer()
differentiation = analyzer.calculate_niche_differentiation(niches)
diversity = analyzer.measure_ecosystem_diversity(niches)

print(f"生态位分化度: {differentiation:.3f}")
print(f"生态系统多样性: {diversity:.3f}")
```

### 4. 系统韧性评估

```python
from cognitive_ecosystem.analyzers.resilience_assessor import SystemResilienceAssessor

# 创建韧性评估器
assessor = SystemResilienceAssessor()

# 模拟智能体移除测试
ecosystem = CognitiveEcosystemEngine(config)
removed_agent = 'agent_1'
resilience_score = assessor.simulate_agent_removal(ecosystem, removed_agent)
print(f"智能体移除后的韧性得分: {resilience_score}")

# 施加信息冲击
shock_type = 'misinformation'
shock_result = assessor.apply_information_shock(ecosystem, shock_type)
print(f"信息冲击测试结果: {shock_result}")
```

### 5. 集体智能涌现检测

```python
from cognitive_ecosystem.analyzers.emergence_detector import EmergenceDetector

# 创建涌现检测器
detector = EmergenceDetector()

# 模拟群体和个体表现数据
group_performance = [0.85, 0.90, 0.88, 0.92]
individual_performance = [0.70, 0.65, 0.72, 0.68]

# 检测集体智能
emergence_result = detector.detect_collective_intelligence(
    group_performance, 
    individual_performance
)
print(f"集体智能检测结果: {emergence_result}")

# 测量协同效应
collaboration_results = {
    'task_1': {'group': 0.9, 'sum_individual': 0.7},
    'task_2': {'group': 0.85, 'sum_individual': 0.75},
    'task_3': {'group': 0.88, 'sum_individual': 0.72}
}
synergy = detector.measure_synergy_effects(collaboration_results)
print(f"协同效应: {synergy}")
```

## 🔧 配置选项详解

### 基本配置
```python
BASIC_CONFIG = {
    'test_roles': ['creator', 'analyst', 'critic', 'synthesizer'],
    'model_name': 'your_model_name',
    'max_agents': 10,
    'timeout_seconds': 300
}
```

### 高级配置
```python
ADVANCED_CONFIG = {
    # 基础设置
    'test_roles': ['creator', 'analyst', 'critic', 'synthesizer'],
    'model_name': 'your_model_name',
    
    # 数据文件路径
    'hallucination_database': 'cognitive_ecosystem/data/known_hallucinations.json',
    'bias_test_scenarios': 'cognitive_ecosystem/data/bias_scenarios.json',
    'fact_database': 'cognitive_ecosystem/data/fact_database.json',
    
    # 测试参数
    'personality_tracking_duration': 30,  # 天数
    'resilience_test_intensity': 'high',  # low, medium, high
    'hallucination_injection_rate': 0.3,  # 30%的测试包含幻觉
    'bias_test_coverage': 'comprehensive',  # basic, standard, comprehensive
    
    # 分析设置
    'niche_analysis_depth': 'detailed',  # basic, standard, detailed
    'emergence_detection_sensitivity': 0.1,  # 涌现检测敏感度
    'statistical_significance_level': 0.05,
    
    # 输出设置
    'baseline_comparison_enabled': True,
    'visualization_enabled': True,
    'detailed_logging': True,
    'save_intermediate_results': True,
    
    # 性能设置
    'parallel_processing': False,  # 是否启用并行处理
    'memory_optimization': True,   # 是否启用内存优化
    'cache_results': True          # 是否缓存结果
}
```

## 📈 结果解读指南

### 1. 幻觉抵抗能力
- **0.9-1.0**: 🟢 优秀 - 能有效识别和抵制虚假信息
- **0.7-0.9**: 🟡 良好 - 大部分情况下能保持理性
- **0.5-0.7**: 🟠 一般 - 容易受到误导
- **0.0-0.5**: 🔴 较差 - 经常接受虚假信息

### 2. 认知多样性
- **0.8-1.0**: 🟢 高度多样化 - 角色差异明显
- **0.6-0.8**: 🟡 中等多样化 - 有一定差异
- **0.4-0.6**: 🟠 低度多样化 - 角色相似性较高
- **0.0-0.4**: 🔴 几乎无差异 - 可能存在角色塌陷

### 3. 系统韧性
- **0.8-1.0**: 🟢 高韧性 - 能承受各种压力
- **0.6-0.8**: 🟡 中等韧性 - 在一般压力下稳定
- **0.4-0.6**: 🟠 低韧性 - 容易受到干扰
- **0.0-0.4**: 🔴 脆弱 - 轻微干扰即可能崩溃

### 4. 集体智能涌现
- **检测到涌现**: 🟢 群体表现超越个体能力之和
- **未检测到涌现**: 🟡 群体表现等于或低于个体能力之和
- **负向涌现**: 🔴 群体表现显著低于个体能力之和

## 🛠️ 故障排除

### 常见错误及解决方案

1. **导入错误**
   ```python
   # 错误: ModuleNotFoundError: No module named 'cognitive_ecosystem'
   # 解决方案:
   import sys
   sys.path.append('/path/to/testLLM')
   ```

2. **数据文件缺失**
   ```python
   # 错误: FileNotFoundError: known_hallucinations.json not found
   # 解决方案: 检查文件路径
   import os
   print(os.path.exists('cognitive_ecosystem/data/known_hallucinations.json'))
   ```

3. **内存不足**
   ```python
   # 解决方案: 减少测试规模
   config = {
       'test_roles': ['creator', 'analyst'],  # 减少角色数量
       'visualization_enabled': False,        # 禁用可视化
       'memory_optimization': True            # 启用内存优化
   }
   ```

### 性能优化建议

1. **禁用不必要的功能**
   ```python
   config['visualization_enabled'] = False
   config['detailed_logging'] = False
   ```

2. **使用批量处理**
   ```python
   config['batch_size'] = 10
   config['parallel_processing'] = True
   ```

3. **启用缓存**
   ```python
   config['cache_results'] = True
   config['cache_directory'] = './cache'
   ```

## 📝 最佳实践

### 1. 测试设计
- 从简单测试开始，逐步增加复杂度
- 使用多种角色组合测试认知多样性
- 定期运行基线对照测试

### 2. 结果分析
- 关注趋势而非单次测试结果
- 结合多个指标进行综合评估
- 保存测试历史以便对比分析

### 3. 性能优化
- 根据硬件配置调整测试规模
- 使用适当的测试强度设置
- 定期清理缓存和临时文件

## 🔗 相关资源

- [完整API文档](cognitive_ecosystem/README.md)
- [测试数据说明](cognitive_ecosystem/data/README.md)
- [扩展开发指南](docs/DEVELOPMENT.md)
- [常见问题解答](docs/FAQ.md)

---

**认知生态系统测试框架** - 让AI认知多样性测试变得简单高效！
