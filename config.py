# 临时配置文件 - 批量测试
MODEL_TO_TEST = 'qwen3:30b-a3b'  # 测试30B大模型

# === Ollama 配置 ===
OLLAMA_HOST = "http://localhost:11434"
OLLAMA_TIMEOUT = 900  # 增加到15分钟，适应大模型推理

# === 模型配置 ===
MODELS_TO_TEST = [
    'qwen3:4b',
    'phi3:mini',
    'qwen:7b-chat'
]
MODELS_LIST_FILE = 'models_list.txt'

# === 默认选项 ===
DEFAULT_OPTIONS_CREATIVE = {
    "temperature": 0.8,
    "top_p": 0.9,
    "max_tokens": 2048,
    "timeout": 180  # 3分钟超时
}

DEFAULT_OPTIONS_DETERMINISTIC = {
    "temperature": 0.0,
    "top_p": 0.1,
    "max_tokens": 2048,
    "timeout": 180  # 3分钟超时
}

# === 目录配置 ===
TEST_WORKSPACE_DIR = 'test_workspace'
LOG_DIR = 'test_logs'
REPORT_DIR = 'test_reports'
TESTOUT_DIR = 'testout'

# === 独立性测试配置 ===
INDEPENDENCE_CONFIG = {
    'model_name': MODEL_TO_TEST,
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
