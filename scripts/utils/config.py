"""
主配置文件
"""

# === 默认测试模型 ===
# 用于 --mode full (未指定 --model 时)
MODEL_TO_TEST = 'together/meta-llama/Llama-3-8b-chat'

# === 批量测试模型列表 ===
# 用于 --mode batch
MODELS_TO_TEST = [
    # Together.ai
    'together/meta-llama/Llama-3-8b-chat',
    'together/mistralai/Mixtral-8x7B-Instruct-v0.1',

    # OpenRouter
    'openrouter/google/gemma-2-9b-it',
    'openrouter/anthropic/claude-3-opus',

    # Gemini
    'gemini/gemini-1.5-flash',

    # DashScope (Alibaba)
    'dashscope/qwen-plus',

    # GLM (Zhipu AI)
    'glm/glm-4-plus',

    # Baidu
    'baidu/ernie-4.0-8k',
]

# === Ollama 配置 (本地备用) ===
OLLAMA_HOST = "http://localhost:11434"
OLLAMA_TIMEOUT = 900  # 增加到15分钟，适应大模型推理

# === 默认选项 ===
DEFAULT_OPTIONS_CREATIVE = {
    "temperature": 0.8,
    "top_p": 0.9,
    "max_tokens": 2048,
    "timeout": 240  # 4分钟超时
}

DEFAULT_OPTIONS_DETERMINISTIC = {
    "temperature": 0.0,
    "top_p": 0.1,
    "max_tokens": 2048,
    "timeout": 240  # 4分钟超时
}

# === 目录配置 ===
TEST_WORKSPACE_DIR = 'test_workspace'
LOG_DIR = 'test_logs'
REPORT_DIR = 'test_reports'
TESTOUT_DIR = 'testout'
MODELS_LIST_FILE = 'models.txt'

# === 独立性测试配置 ===
INDEPENDENCE_CONFIG = {
    'model_name': MODEL_TO_TEST,  # 使用云端优先模型
    'output_dir': TESTOUT_DIR,
    'test_roles': [
        'software_engineer',
        'data_scientist', 
        'product_manager',
        'security_expert'
    ],
    'stress_levels': ['low', 'medium', 'high', 'extreme'],
    'conversation_length': 15,
    'memory_test_intervals': [3, 7, 12],
    'breaking_threshold': 0.5,
    'experiments': {
        'breaking_stress': {
            'enabled': True,
            'max_pressure_level': 10,
            'cognitive_load_tests': True
        },
        'implicit_cognition': {
            'enabled': True,
            'association_tests': True,
            'bias_detection': True
        },
        'longitudinal_consistency': {
            'enabled': True,
            'conversation_length': 15,
            'memory_intervals': [3, 7, 12]
        }
    }
}

# === Cognitive Ecosystem Test Config ===
COGNITIVE_ECOSYSTEM_CONFIG = {
    'test_roles': [
        'creator', 'analyst', 'critic', 'synthesizer'
    ],
    'hallucination_database': 'cognitive_ecosystem/data/known_hallucinations.json',
    'bias_test_scenarios': 'cognitive_ecosystem/data/bias_scenarios.json',
    'personality_tracking_duration': 30,  # days
    'resilience_test_intensity': 'high',
    'baseline_comparison_enabled': True,
    'statistical_significance_level': 0.05,
    'visualization_enabled': True
}
