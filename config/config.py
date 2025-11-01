"""
Configuration file for Unified LLM Test Framework
"""

# Default model to test
MODEL_TO_TEST = 'glm/glm-4-plus'

# Ollama service configuration
OLLAMA_HOST = 'http://localhost:11434'

# Testing configuration
TEST_WORKSPACE_DIR = 'test_workspace'
LOG_DIR = 'test_logs'
REPORT_DIR = 'test_reports'

# Model configuration
AVAILABLE_MODELS = ['glm/glm-4-plus', 'gemini/gemini-2.0-flash-exp', 'together/llama3:instruct', 'together/deepseek-coder:6.7b-instruct', 'together/mistral:instruct', 'ppinfra/qwen3-235b-a22b-fp8']

# Independence testing configuration
EMBEDDING_MODEL = 'sentence-transformers/all-MiniLM-L6-v2'
SIMILARITY_THRESHOLD = 0.7
MEMORY_RETENTION_DAYS = 30
BREAKING_THRESHOLD = 0.7
MAX_STRESS_ROUNDS = 10

# Testing options
DEFAULT_OPTIONS_DETERMINISTIC = {
    'temperature': 0.1,
    'num_ctx': 4096,
    'num_predict': 1024
}

DEFAULT_OPTIONS_CREATIVE = {
    'temperature': 0.8,
    'num_ctx': 4096,
    'num_predict': 1024
}

# Model list file
MODELS_LIST_FILE = 'config/models.txt'

# Cloud connection cache file
CLOUD_CONNECTION_CACHE_FILE = 'config/cloud_connection_cache.json'

# Test status file
TEST_STATUS_FILE = 'config/test_status.json'

# Independence testing configuration
INDEPENDENCE_CONFIG = {
    'embedding_model': EMBEDDING_MODEL,
    'similarity_threshold': SIMILARITY_THRESHOLD,
    'memory_retention_days': MEMORY_RETENTION_DAYS,
    'breaking_threshold': BREAKING_THRESHOLD,
    'max_stress_rounds': MAX_STRESS_ROUNDS
}
