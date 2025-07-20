"""
testLLM 角色独立性测试模块

提供LLM角色独立性和一致性的综合测试能力，包括：
- 角色破坏压力测试
- 隐式认知测试  
- 纵向一致性测试
"""

try:
    from .experiments.breaking_stress import BreakingStressTest
    from .experiments.implicit_cognition import ImplicitCognitionTest
    from .experiments.longitudinal_consistency import LongitudinalConsistencyTest
    from .base import IndependenceTestBase
except ImportError as e:
    print(f"警告: 独立性测试模块导入失败: {e}")
    # 提供空的占位符类以避免导入错误
    class BreakingStressTest:
        def __init__(self, *args, **kwargs):
            raise NotImplementedError("BreakingStressTest 导入失败")
    
    class ImplicitCognitionTest:
        def __init__(self, *args, **kwargs):
            raise NotImplementedError("ImplicitCognitionTest 导入失败")
    
    class LongitudinalConsistencyTest:
        def __init__(self, *args, **kwargs):
            raise NotImplementedError("LongitudinalConsistencyTest 导入失败")
    
    class IndependenceTestBase:
        def __init__(self, *args, **kwargs):
            raise NotImplementedError("IndependenceTestBase 导入失败")

__version__ = "1.0.0"

__all__ = [
    'BreakingStressTest',
    'ImplicitCognitionTest', 
    'LongitudinalConsistencyTest',
    'IndependenceTestBase'
]

# 测试套件配置
DEFAULT_TEST_CONFIG = {
    'test_roles': [
        'software_engineer',
        'data_scientist',
        'product_manager', 
        'security_expert'
    ],
    'stress_levels': ['low', 'medium', 'high', 'extreme'],
    'conversation_length': 15,
    'memory_test_intervals': [3, 7, 12],
    'cognition_test_types': [
        'association',
        'moral_dilemma',
        'bias_detection',
        'context_switching'
    ]
}

def create_test_suite(config: dict = None):
    """
    创建完整的角色独立性测试套件
    
    Args:
        config: 测试配置字典
        
    Returns:
        包含三个测试实例的字典
    """
    if config is None:
        config = DEFAULT_TEST_CONFIG.copy()
    
    return {
        'breaking_stress': BreakingStressTest(config),
        'implicit_cognition': ImplicitCognitionTest(config),
        'longitudinal_consistency': LongitudinalConsistencyTest(config)
    }
