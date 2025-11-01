"""
认知生态系统测试框架

这是一个用于测试大语言模型认知多样性和集体智能的综合框架。
框架包含四个核心层次：
- 基础设施层：核心引擎和状态管理
- 认知检测层：幻觉、偏见、风格、人格检测
- 生态分析层：生态位、韧性、涌现分析
- 对照验证层：基线对照和统计验证
"""

__version__ = "1.0.0"
__author__ = "Cognitive Ecosystem Team"

# 核心组件导入
from .core.ecosystem_engine import CognitiveEcosystemEngine
from .core.cognitive_niche import CognitiveNiche
from .core.state_manager import StateManager

# 检测器导入
from .detectors.hallucination_detector import CollusiveHallucinationDetector
from .detectors.cognitive_bias_detector import CognitiveBiasDetector
from .detectors.style_analyzer import ProblemSolvingStyleAnalyzer
from .detectors.personality_tracker import PersonalityTracker

# 分析器导入
from .analyzers.niche_analyzer import CognitiveNicheAnalyzer
from .analyzers.resilience_assessor import SystemResilienceAssessor
from .analyzers.emergence_detector import EmergenceDetector

# 基线和验证导入
from .baselines.vanilla_agent import VanillaAgent
from .baselines.statistical_validator import StatisticalValidator

# 工具导入
from .utils import calculate_cognitive_diversity_index, detect_emergence, calculate_resilience_score
from .utils.visualization import Visualization

__all__ = [
    'CognitiveEcosystemEngine',
    'CognitiveNiche',
    'StateManager',
    'CollusiveHallucinationDetector',
    'CognitiveBiasDetector',
    'ProblemSolvingStyleAnalyzer',
    'PersonalityTracker',
    'CognitiveNicheAnalyzer',
    'SystemResilienceAssessor',
    'EmergenceDetector',
    'VanillaAgent',
    'StatisticalValidator',
    'calculate_cognitive_diversity_index',
    'detect_emergence',
    'calculate_resilience_score',
    'Visualization'
]
