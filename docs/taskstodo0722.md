# 认知生态系统测试框架 - 详细实施规划

## 一、项目总体架构设计

### 1.1 核心架构层次
```
认知生态系统测试框架
├── 基础设施层 (Infrastructure Layer)
│   ├── 现有Pillar 25框架修复与增强
│   ├── 生态系统核心引擎
│   └── 数据持久化与状态管理
├── 认知检测层 (Cognitive Detection Layer)
│   ├── 共谋性幻觉检测器
│   ├── 认知偏见一致性测试
│   ├── 问题解决风格差异测试
│   └── 纵向人格稳定性测试
├── 生态分析层 (Ecological Analysis Layer)
│   ├── 认知生态位分析器
│   ├── 系统韧性评估器
│   └── 集体智能涌现检测器
└── 对照验证层 (Baseline Validation Layer)
    ├── 香草模型基线系统
    ├── 统计显著性检验
    └── 结果可视化与报告
```

### 1.2 文件结构规划
```
testLLM/
├── tests/
│   ├── test_pillar_25_cognitive_ecosystem.py  # 主测试文件
│   ├── test_pillar_25a_collusive_hallucination.py
│   ├── test_pillar_25b_cognitive_bias_congruence.py
│   ├── test_pillar_25c_problem_solving_styles.py
│   └── test_pillar_25d_longitudinal_personality.py
├── cognitive_ecosystem/  # 新增核心模块
│   ├── __init__.py
│   ├── core/
│   │   ├── ecosystem_engine.py
│   │   ├── cognitive_niche.py
│   │   └── state_manager.py
│   ├── detectors/
│   │   ├── hallucination_detector.py
│   │   ├── bias_detector.py
│   │   ├── style_analyzer.py
│   │   └── personality_tracker.py
│   ├── analyzers/
│   │   ├── niche_analyzer.py
│   │   ├── resilience_assessor.py
│   │   └── emergence_detector.py
│   ├── baselines/
│   │   ├── vanilla_agent.py
│   │   └── statistical_validator.py
│   └── utils/
│       ├── cognitive_metrics.py
│       └── visualization.py
├── independence/  # 现有模块保持
└── config.py  # 扩展配置
```

## 二、详细实施计划

### Phase 1: 基础设施层构建 (Week 1-2)

#### 任务1.1: 修复现有Pillar 25框架 (3天)
**文件**: `tests/test_pillar_25_independence.py`, `independence/experiments/breaking_stress.py`
- 修复导入错误和0分bug
- 完善错误处理机制
- 验证三大实验系统正常运行
- 建立基础测试数据流

#### 任务1.2: 创建生态系统核心引擎 (4天)
**文件**: `cognitive_ecosystem/core/ecosystem_engine.py`
```python
class CognitiveEcosystemEngine:
    def __init__(self, config):
        self.agents = {}  # 角色智能体字典
        self.interaction_history = []  # 交互历史
        self.cognitive_state = {}  # 认知状态追踪
        self.niche_map = {}  # 生态位映射
    
    def register_agent(self, agent_id, role_config):
        """注册认知智能体"""
    
    def simulate_interaction(self, scenario):
        """模拟多智能体交互"""
    
    def analyze_cognitive_diversity(self):
        """分析认知多样性"""
    
    def detect_collective_patterns(self):
        """检测集体认知模式"""
```

#### 任务1.3: 实现认知生态位分析器 (3天)
**文件**: `cognitive_ecosystem/core/cognitive_niche.py`
```python
class CognitiveNiche:
    def __init__(self):
        self.knowledge_domains = set()  # 知识领域
        self.reasoning_patterns = []    # 推理模式
        self.value_orientations = {}    # 价值取向
        self.problem_solving_styles = []  # 问题解决风格
    
    def calculate_niche_overlap(self, other_niche):
        """计算生态位重叠度"""
    
    def measure_niche_breadth(self):
        """测量生态位宽度"""
    
    def identify_unique_contributions(self):
        """识别独特贡献"""
```

#### 任务1.4: 建立状态管理系统 (4天)
**文件**: `cognitive_ecosystem/core/state_manager.py`
- 实现跨会话的角色状态持久化
- 建立交互历史数据库
- 实现状态回滚和快照功能
- 设计高效的状态查询接口

### Phase 2: 四大测试套件实现 (Week 3-5)

#### 任务2.1: 共谋性幻觉检测器 (5天)
**文件**: `cognitive_ecosystem/detectors/hallucination_detector.py`
```python
class CollusiveHallucinationDetector:
    def __init__(self):
        self.known_hallucinations = self._load_hallucination_database()
        self.injection_strategies = [
            'fake_theory_injection',
            'false_historical_fact',
            'non_existent_person',
            'fabricated_research'
        ]
    
    def inject_hallucination(self, scenario_type):
        """注入已知幻觉到测试场景"""
    
    def analyze_collective_response(self, responses):
        """分析集体响应模式"""
    
    def detect_reality_checking(self, agent_responses):
        """检测现实核查行为"""
    
    def calculate_resistance_score(self, results):
        """计算抗幻觉得分"""
```

**具体测试场景设计**:
- 虚假理论注入: "马斯洛的前馈激励理论"
- 错误历史事实: "1969年阿波罗11号在火星着陆"
- 不存在的人物: "著名心理学家Dr. Elena Vasquez的研究"
- 伪造研究: "2023年MIT关于量子意识的突破性发现"

#### 任务2.2: 认知偏见一致性测试 (4天)
**文件**: `cognitive_ecosystem/detectors/bias_detector.py`
```python
class CognitiveBiasDetector:
    def __init__(self):
        self.bias_types = [
            'anchoring_bias',
            'confirmation_bias', 
            'availability_heuristic',
            'representativeness_heuristic'
        ]
    
    def setup_anchoring_trap(self, anchor_value):
        """设置锚定效应陷阱"""
    
    def measure_bias_congruence(self, agent_responses):
        """测量偏见一致性"""
    
    def detect_bias_resistance(self, responses):
        """检测偏见抵抗能力"""
```

#### 任务2.3: 问题解决风格差异测试 (4天)
**文件**: `cognitive_ecosystem/detectors/style_analyzer.py`
```python
class ProblemSolvingStyleAnalyzer:
    def __init__(self):
        self.style_dimensions = [
            'metaphor_generation',
            'knowledge_domain_preference',
            'reasoning_approach',
            'abstraction_level'
        ]
    
    def analyze_metaphor_diversity(self, responses):
        """分析隐喻多样性"""
    
    def measure_knowledge_domain_spread(self, responses):
        """测量知识领域分布"""
    
    def calculate_style_distance_matrix(self, agent_responses):
        """计算风格距离矩阵"""
```

#### 任务2.4: 纵向人格稳定性测试 (5天)
**文件**: `cognitive_ecosystem/detectors/personality_tracker.py`
```python
class PersonalityTracker:
    def __init__(self):
        self.personality_dimensions = [
            'stance_consistency',
            'argument_evolution',
            'memory_integration',
            'learning_adaptation'
        ]
    
    def track_stance_evolution(self, agent_id, topic, timeline):
        """追踪立场演变"""
    
    def measure_memory_integration(self, responses, historical_context):
        """测量记忆整合能力"""
    
    def detect_personality_drift(self, agent_history):
        """检测人格漂移"""
```

### Phase 3: 生态分析层实现 (Week 6-7)

#### 任务3.1: 认知生态位分析器 (4天)
**文件**: `cognitive_ecosystem/analyzers/niche_analyzer.py`
```python
class CognitiveNicheAnalyzer:
    def __init__(self):
        self.niche_metrics = [
            'knowledge_specialization',
            'reasoning_uniqueness', 
            'functional_contribution',
            'interaction_patterns'
        ]
    
    def calculate_niche_differentiation(self, agents):
        """计算生态位分化度"""
    
    def identify_niche_overlap(self, agent_pairs):
        """识别生态位重叠"""
    
    def measure_ecosystem_diversity(self, agent_niches):
        """测量生态系统多样性"""
    
    def detect_functional_redundancy(self, agents):
        """检测功能冗余"""
```

#### 任务3.2: 系统韧性评估器 (4天)
**文件**: `cognitive_ecosystem/analyzers/resilience_assessor.py`
```python
class SystemResilienceAssessor:
    def __init__(self):
        self.stress_tests = [
            'agent_removal_test',
            'information_shock_test',
            'cognitive_load_test',
            'adversarial_input_test'
        ]
    
    def simulate_agent_removal(self, ecosystem, removed_agent):
        """模拟智能体移除实验"""
    
    def apply_information_shock(self, ecosystem, shock_type):
        """施加信息冲击"""
    
    def measure_recovery_capacity(self, pre_shock, post_shock):
        """测量恢复能力"""
    
    def calculate_resilience_score(self, test_results):
        """计算韧性得分"""
```

#### 任务3.3: 集体智能涌现检测器 (4天)
**文件**: `cognitive_ecosystem/analyzers/emergence_detector.py`
```python
class EmergenceDetector:
    def __init__(self):
        self.emergence_indicators = [
            'collective_problem_solving',
            'distributed_reasoning',
            'emergent_consensus',
            'novel_solution_generation'
        ]
    
    def detect_collective_intelligence(self, group_performance, individual_performance):
        """检测集体智能"""
    
    def measure_synergy_effects(self, collaboration_results):
        """测量协同效应"""
    
    def identify_emergent_properties(self, system_behavior):
        """识别涌现属性"""
```

### Phase 4: 对照验证层实现 (Week 8)

#### 任务4.1: 香草模型基线系统 (3天)
**文件**: `cognitive_ecosystem/baselines/vanilla_agent.py`
```python
class VanillaAgent:
    def __init__(self, base_model):
        self.model = base_model
        self.no_role_prompt = True  # 不使用角色提示
    
    def generate_response(self, prompt):
        """生成无角色扮演的基线响应"""
    
    def run_baseline_tests(self, test_scenarios):
        """运行基线对照测试"""
```

#### 任务4.2: 统计验证系统 (2天)
**文件**: `cognitive_ecosystem/baselines/statistical_validator.py`
```python
class StatisticalValidator:
    def __init__(self):
        self.significance_level = 0.05
    
    def compare_with_baseline(self, ecosystem_results, baseline_results):
        """与基线结果比较"""
    
    def calculate_effect_size(self, treatment, control):
        """计算效应量"""
    
    def generate_statistical_report(self, results):
        """生成统计报告"""
```

#### 任务4.3: 可视化与报告系统 (2天)
**文件**: `cognitive_ecosystem/utils/visualization.py`
- 认知生态位可视化图表
- 系统韧性雷达图
- 时间序列人格演变图
- 集体智能涌现趋势图

### Phase 5: 主测试文件集成 (Week 9)

#### 任务5.1: 主测试文件实现 (3天)
**文件**: `tests/test_pillar_25_cognitive_ecosystem.py`
```python
def run_cognitive_ecosystem_test(model_name, config):
    """运行完整的认知生态系统测试"""
    
    # 1. 初始化生态系统
    ecosystem = CognitiveEcosystemEngine(config)
    
    # 2. 注册测试角色
    roles = ['creator', 'analyst', 'critic', 'synthesizer']
    for role in roles:
        ecosystem.register_agent(role, get_role_config(role))
    
    # 3. 运行四大测试套件
    hallucination_results = run_hallucination_tests(ecosystem)
    bias_results = run_bias_tests(ecosystem)
    style_results = run_style_tests(ecosystem)
    personality_results = run_personality_tests(ecosystem)
    
    # 4. 生态分析
    niche_analysis = analyze_cognitive_niches(ecosystem)
    resilience_analysis = assess_system_resilience(ecosystem)
    emergence_analysis = detect_collective_intelligence(ecosystem)
    
    # 5. 基线对照
    baseline_results = run_vanilla_baseline_tests(config)
    statistical_comparison = compare_with_baseline(results, baseline_results)
    
    # 6. 生成综合报告
    return generate_ecosystem_report(all_results)
```

#### 任务5.2: 配置系统扩展 (2天)
**文件**: `config.py`
```python
COGNITIVE_ECOSYSTEM_CONFIG = {
    'test_roles': [
        'creator', 'analyst', 'critic', 'synthesizer'
    ],
    'hallucination_database': 'data/known_hallucinations.json',
    'bias_test_scenarios': 'data/bias_scenarios.json',
    'personality_tracking_duration': 30,  # 天数
    'resilience_test_intensity': 'high',
    'baseline_comparison_enabled': True,
    'statistical_significance_level': 0.05,
    'visualization_enabled': True
}
```

#### 任务5.3: 端到端测试验证 (2天)
- 完整测试流程验证
- 性能优化
- 错误处理完善
- 文档编写

## 三、关键技术规范

### 3.1 认知多样性量化指标
```python
def calculate_cognitive_diversity_index(agents):
    """
    计算认知多样性指数 (CDI)
    CDI = (生态位分化度 × 0.3) + (功能互补度 × 0.3) + 
          (风格差异度 × 0.2) + (知识领域分布 × 0.2)
    """
    pass
```

### 3.2 集体智能涌现检测算法
```python
def detect_emergence(group_performance, sum_individual_performance):
    """
    涌现检测: 群体表现 > 个体表现之和
    涌现指数 = (群体表现 - 个体表现之和) / 个体表现之和
    """
    pass
```

### 3.3 系统韧性评估模型
```python
def calculate_resilience_score(pre_stress, post_stress, recovery_time):
    """
    韧性得分 = (恢复程度 × 0.5) + (恢复速度 × 0.3) + (适应能力 × 0.2)
    """
    pass
```

## 四、成功标准与验收条件

### 4.1 功能完整性标准
- [ ] 四大测试套件全部实现并通过单元测试
- [ ] 生态系统引擎能够管理多智能体交互
- [ ] 香草模型基线对照系统正常运行
- [ ] 统计显著性检验功能完备

### 4.2 性能标准
- [ ] 单次完整测试时间 < 30分钟
- [ ] 支持至少10个并发智能体
- [ ] 内存使用 < 2GB
- [ ] 测试结果可重现性 > 95%

### 4.3 质量标准
- [ ] 代码覆盖率 > 80%
- [ ] 所有公共API有完整文档
- [ ] 通过所有预定义的集成测试
- [ ] 生成的报告清晰易懂

### 4.4 创新性验证标准
- [ ] 能够区分真实认知异构性与角色扮演
- [ ] 检测出至少3种不同类型的共谋性幻觉
- [ ] 识别出显著的认知生态位分化
- [ ] 观察到可测量的集体智能涌现现象

---

## Implementation Checklist:

1. [x] 修复现有Pillar 25框架的导入错误和0分bug
2. [x] 创建cognitive_ecosystem目录结构和核心模块
3. [x] 实现CognitiveEcosystemEngine核心引擎
4. [x] 实现CognitiveNiche生态位分析器
5. [x] 建立StateManager状态管理系统
6. [x] 实现CollusiveHallucinationDetector共谋性幻觉检测器
7. [x] 创建已知幻觉数据库和注入策略
8. [x] 实现CognitiveBiasDetector认知偏见检测器
9. [x] 实现ProblemSolvingStyleAnalyzer风格分析器
10. [x] 实现PersonalityTracker纵向人格追踪器
11. [x] 实现CognitiveNicheAnalyzer生态位分析器
12. [x] 实现SystemResilienceAssessor系统韧性评估器
13. [x] 实现EmergenceDetector集体智能涌现检测器
14. [x] 实现VanillaAgent香草模型基线系统
15. [x] 实现StatisticalValidator统计验证系统
16. [x] 创建可视化和报告生成系统
17. [x] 实现主测试文件test_pillar_25_cognitive_ecosystem.py
18. [x] 扩展config.py添加生态系统配置
19. [x] 进行端到端集成测试和性能优化
20. [x] 编写完整的使用文档和API文档
