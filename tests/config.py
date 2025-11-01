#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试配置文件
"""

import os
from pathlib import Path

# 项目根目录
PROJECT_ROOT = Path(__file__).parent.parent

# 默认模型
MODEL_TO_TEST = os.getenv('MODEL_TO_TEST', 'dashscope/qwen:7b-chat')

# 默认选项 - 确定性
DEFAULT_OPTIONS_DETERMINISTIC = {
    'temperature': 0.1,
    'top_p': 0.5,
    'max_tokens': 1024
}

# 默认选项 - 创造性
DEFAULT_OPTIONS_CREATIVE = {
    'temperature': 0.8,
    'top_p': 0.9,
    'max_tokens': 2048
}

# 认知生态系统配置
COGNITIVE_ECOSYSTEM_CONFIG = {
    'niche_detection_threshold': 0.7,
    'interaction_complexity': 3,
    'emergence_detection': True
}

def get_test_config():
    """获取测试配置"""
    return {
        'model_to_test': MODEL_TO_TEST,
        'default_options_deterministic': DEFAULT_OPTIONS_DETERMINISTIC,
        'default_options_creative': DEFAULT_OPTIONS_CREATIVE,
        'cognitive_ecosystem': COGNITIVE_ECOSYSTEM_CONFIG,
        'project_root': PROJECT_ROOT
    }
COGNITIVE_ECOSYSTEM_CONFIG = {
    'model_name': MODEL_TO_TEST,
    'test_agents': 5,
    'conversation_turns': 10,
    'output_dir': 'testout'
}

# 独立性测试配置
INDEPENDENCE_CONFIG = {
    'model_name': MODEL_TO_TEST,
    'output_dir': 'testout',
    'test_roles': [
        'software_engineer',
        'data_scientist',
        'product_manager',
        'security_expert',
        'marketing_specialist',
        'financial_analyst'
    ],
    'stress_levels': ['low', 'medium', 'high', 'extreme'],
    'conversation_length': 15,
    'memory_test_intervals': [3, 7, 12]
}
