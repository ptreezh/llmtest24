# 全局配置文件

# --- 主要配置 ---

# 请将此处的模型名称替换为您希望测评的、已通过 `ollama pull` 下载的模型
# 例如: 'gemma2:9b', 'qwen2:7b', 'llama3:8b', 'mixtral:8x7b'
# 在执行main_orchestrator.py时，此项将被命令行参数覆盖。

MODEL_TO_TEST = 'qwen2:7b'

# --- 高级配置 ---

# 如果您的 Ollama 服务不在本地或使用了不同端口，请修改此项
OLLAMA_HOST = 'http://localhost:11434'

# 为每个请求设置默认的Ollama选项
# temperature=0.0 用于需要确定性输出的任务（如推理、代码）
# temperature=0.7 用于需要创造性的任务
DEFAULT_OPTIONS_DETERMINISTIC = {'temperature': 0.0}
DEFAULT_OPTIONS_CREATIVE = {'temperature': 0.7}

# 测试工作目录设置
TEST_WORKSPACE_DIR = 'test_workspace'
LOG_DIR = 'test_logs'
REPORT_DIR = 'test_reports'

# 批量测试模型列表文件 (可选)
MODELS_LIST_FILE = 'models.txt'
