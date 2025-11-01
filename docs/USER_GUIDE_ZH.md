# LLM高级能力测评套件 - 使用手册

## 1. 环境准备

### 1.1 安装依赖

```bash
# 安装Python依赖
pip install -r config/requirements.txt

# 安装Ollama（用于本地模型测试）
curl -fsSL https://ollama.com/install.sh | sh

# 安装Node.js（用于部分工具脚本）
# 从 https://nodejs.org 下载并安装
```

### 1.2 配置环境变量

创建 `.env` 文件并配置云服务密钥：

```bash
# .env
OPENAI_API_KEY=your_openai_key
GEMINI_API_KEY=your_gemini_key
DASHSCOPE_API_KEY=your_dashscope_key
```

### 1.3 初始化工作空间

```bash
python workspace_init.py
```

## 2. 基本配置

### 2.1 配置测试模型

编辑 `config.py` 文件：

```python
# 主要测试模型
MODEL_TO_TEST = 'qwen2:7b'

# 云服务优先级模型
CLOUD_PRIORITY_MODELS = [
    'gpt-4-turbo',
    'gemini-1.5-pro',
    'qwen-max'
]

# 测试配置
DEFAULT_OPTIONS_CREATIVE = {
    'temperature': 0.7,
    'top_p': 0.9,
    'max_tokens': 2048
}
```

### 2.2 配置测试角色

在 `roles/` 目录下添加角色配置文件，例如 `医生.json`：

```json
{
  "name": "doctor",
  "description": "资深医生，具有丰富的临床经验",
  "expertise": ["内科", "外科", "急诊"],
  "personality": "严谨、专业、富有同情心",
  "communication_style": "清晰、直接、使用专业术语"
}
```

### 2.3 配置测试参数

编辑 `config/test_config.yaml`：

```yaml
independence:
  breaking_stress:
    stress_levels: [1, 2, 3, 4, 5]
    stress_types: ["逻辑矛盾", "情感压力", "权威挑战", "时间压力"]
  implicit_cognition:
    categories: ["文化偏见", "权威服从", "情感倾向", "道德判断"]
  longitudinal_consistency:
    conversation_turns: 10
    memory_persistence_check: true
```

## 3. 运行测试

### 3.1 基础能力测试 (Pillar 1-8)

```bash
# 运行所有基础能力测试
python run_comprehensive_tests.py

# 运行特定能力测试
python tests/test_pillar_01_logic.py
python tests/test_pillar_02_instruction.py
python tests/test_pillar_03_structural.py
```

### 3.2 高级能力测试 (Pillar 9-19)

```bash
# 运行所有高级能力测试
python run_advanced_capability_tests.py

# 运行特定高级能力测试
python run_dynamic_role_switching_test.py
python run_massive_consensus_test.py
```

### 3.3 前沿能力测试 (Pillar 20-24)

```bash
# 运行海量角色共识测试
python run_massive_consensus_test.py

# 运行动态角色切换测试
python run_dynamic_role_switching_test.py

# 运行项目管理集成测试
python tests/test_pillar_22_project_management.py
```

### 3.4 角色独立性测试

```bash
# 运行完整角色独立性测试
python run_pillar_25_independence.py

# 运行快速测试
python run_pillar_25_independence.py --quick

# 运行批量测试
python run_pillar_25_independence.py --batch model1 model2 model3
```

### 3.5 云服务测试

```bash
# 运行云服务独立性测试
python run_cloud_independence_test.py

# 运行认知生态系统云测试
python run_cognitive_ecosystem_cloud_test.py

# 运行批量云测试
python run_extended_cloud_test.py
```

## 4. 结果分析

### 4.1 查看测试输出

测试结果保存在 `testout/` 目录：

```bash
# 查看测试输出文件
ls testout/

# 查看特定模型的测试结果
cat testout/cloud_independence_qwen-max.json
```

### 4.2 生成分析报告

```bash
# 分析独立性测试结果
python analyze_results.py

# 评估增强测试结果
python evaluate_enhanced_results.py

# 生成可视化报告
python visualize_test_results.py
```

### 4.3 结果文件结构

```bash
testout/
├── cloud_independence_<model_name>.json          # 云服务独立性测试结果
├── cloud_independence_test_results_<timestamp>.json  # 批量测试结果
├── run_independence_test_<model>_<timestamp>.json    # 独立性测试详细结果
└── collaboration_case*.txt                         # 协作案例记录
```

## 5. 工具使用

### 5.1 架构映射工具

生成项目架构映射：

```bash
python project_architecture_map.py

# 生成的文件
# - architecture_map.json
# - interface_map.json
```

### 5.2 测试生成器

基于接口映射生成测试代码：

```bash
python enhanced_test_generator.py
```

### 5.3 智能测试运行器

管理测试状态和执行：

```bash
# 查看可用服务
python smart_test_runner.py --list-services

# 查看可用模型
python smart_test_runner.py --list-models

# 运行测试
python smart_test_runner.py --run-tests openai gemini
```

### 5.4 测试状态管理

重置测试状态：

```bash
# 重置所有测试状态
python tools/reset_test_status.py --reset-all

# 重置特定服务状态
python tools/reset_test_status.py --reset-service openai

# 查看测试状态
python tools/reset_test_status.py --show-status
```

## 6. 故障排除

### 6.1 模型连接问题

```bash
# 检查Ollama服务
python debug_model_call.py

# 检查云服务连接
python test_cloud_services.py

# 检查特定云服务
python test_baidu_connectivity.py
```

### 6.2 配置验证

```bash
# 验证系统配置
python run_end_to_end_integration_test.py

# 验证云系统
python validate_cloud_system.py
```

### 6.3 常见问题

**Q: 测试长时间无响应？**
A: 可能是模型处理复杂任务，检查 `testout/` 目录是否有部分结果生成。

**Q: 无法连接云服务？**
A: 检查 `.env` 文件中的API密钥是否正确，运行 `test_cloud_services.py` 验证连接。

**Q: 测试结果不一致？**
A: 检查模型的随机性设置（temperature），建议在测试时使用较低的temperature值。

## 7. 最佳实践

### 7.1 测试策略

- **分层测试**：先运行基础能力测试，再进行高级和前沿能力测试
- **对比测试**：对多个模型进行相同测试，便于比较性能差异
- **重复测试**：对关键测试进行多次运行，确保结果的稳定性

### 7.2 性能优化

- **批量测试**：使用批量测试脚本同时测试多个模型
- **结果缓存**：对已测试的模型结果进行缓存，避免重复测试
- **资源管理**：监控系统资源使用情况，避免资源耗尽

### 7.3 结果解读

- **定量指标**：关注成功率、响应时间等可量化指标
- **定性分析**：深入分析模型的响应质量、创新性和一致性
- **趋势分析**：追踪模型在不同测试中的表现趋势，识别改进方向
