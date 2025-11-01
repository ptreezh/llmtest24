"""
认知检测器模块

包含四大核心检测器：
- 共谋性幻觉检测器
- 认知偏见检测器  
- 问题解决风格分析器
- 纵向人格追踪器
"""

from .hallucination_detector import CollusiveHallucinationDetector
from .cognitive_bias_detector import CognitiveBiasDetector
from .style_analyzer import ProblemSolvingStyleAnalyzer
from .personality_tracker import PersonalityTracker

__all__ = [
    'CollusiveHallucinationDetector',
    'CognitiveBiasDetector', 
    'ProblemSolvingStyleAnalyzer',
    'PersonalityTracker'
]
