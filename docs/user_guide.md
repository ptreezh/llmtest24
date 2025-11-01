# 认知生态系统测试框架用户指南

## 1. 项目概述

欢迎使用认知生态系统测试框架！本框架旨在全面评估大型语言模型（LLM）在认知能力方面的表现，包括但不限于逻辑推理、角色扮演、多智能体协作、共识达成以及对幻觉和偏见的抵抗能力。框架支持多种模型，并提供详细的测试报告和分析。

## 2. 环境设置

### 2.1 前置条件
- Python 3.8+
- Pip 包管理器
- Conda 环境（推荐，用于管理依赖）
- Ollama（用于运行本地模型，如 qwen3:4b, gemma3:latest）
- OpenAI API Key / Anthropic API Key（如果使用这些模型）

### 2.2 安装依赖
项目依赖已在 `requirements.txt` 文件中列出。建议在 Conda 环境中安装：

```bash
# 激活您的 Conda 环境 (例如：open_manus)
conda activate open_manus

# 安装项目依赖
pip install -r requirements.txt
```

### 2.3 模型配置
- **本地模型**: 确保 Ollama 已安装并运行，模型已下载（例如 `qwen3:4b`, `gemma3:latest`）。
- **云端模型**: 根据 `config/test_config.yaml` 中的配置，设置相应的环境变量（如 `OPENAI_API_KEY`, `ANTHROPIC_API_KEY`）。

## 3. 运行测试

### 3.1 使用主编排器 (`main_orchestrator.py`)

`main_orchestrator.py` 是运行测试的主要入口点。您可以通过命令行参数指定要测试的模型、运行特定的 Pillar 测试或运行复杂的工作流。

**基本用法：**

```bash
# 测试指定模型的所有基础 Pillar 测试
python main_orchestrator.py --model <your_model_name>

# 运行特定的 Pillar 测试
python main_orchestrator.py --model <your_model_name> --test test_pillar_01_logic.py test_pillar_02_instruction.py

# 运行工作流测试
python main_orchestrator.py --model <your_model_name> --workflow wiki_collaboration
```

**注意**:
-   目前，Pillar 25 的测试（如 `test_pillar_25a_collusive_hallucination.py`）由于缺少 `run_test` 函数，可能无法被 `main_orchestrator.py` 正确发现和执行。我们计划在后续步骤中解决此问题。

### 3.2 运行单个 Pillar 测试

您也可以直接运行单个 Pillar 测试文件（如果它们包含 `if __name__ == '__main__':` 块）：

```bash
python tests/test_pillar_01_logic.py <your_model_name>
```

## 4. 项目结构概览

```
testLLM/
├── cognitive_ecosystem/  # 核心认知生态系统模块
│   ├── core/             # 核心引擎和生态位
│   ├── detectors/        # 各种认知检测器
│   ├── analyzers/        # 生态分析工具
│   ├── baselines/        # 基线模型和验证器
│   └── utils/            # 通用工具
├── tests/                # 各项能力测试脚本
│   ├── test_pillar_XX_*.py # 各Pillar测试文件
│   └── composite_scenarios/ # 复合场景测试
├── config/               # 配置文件 (roles.yaml, test_config.yaml)
├── docs/                 # 项目文档
├── independence/         # 现有模块
├── roles/                # 角色定义文件 (.json)
├── scripts/              # 辅助脚本
├── testout/              # 测试输出目录
└── main_orchestrator.py    # 主测试运行器
```

## 5. 关键功能与测试

### 5.1 角色管理与共识
- **Pillar 20 (海量角色共识)**: 测试模型在处理大规模角色协作、投票和区块链共识算法方面的能力。
- **角色定义**: 通过 `roles.yaml` 和 `.json` 文件定义不同角色的专业知识、观点和行为风格。

### 5.2 认知能力测试
- **幻觉检测**: 检测模型是否会产生和传播虚假信息。
- **偏见检测**: 评估模型在面对不同情境时是否表现出认知偏见。
- **人格稳定性**: 测试模型在长期交互中是否能保持其设定的角色身份和行为模式。
- **系统韧性**: 评估系统在面对压力（如信息冲击、角色移除）时的表现。
- **集体智能涌现**: 检测群体协作是否能产生超越个体能力的涌现现象。

## 6. 后续计划

1.  **修复 Pillar 25 测试执行问题**: 为 Pillar 25 的 `unittest` 测试文件添加 `run_test` 函数包装器，使其能被 `main_orchestrator.py` 正确调用。
2.  **执行端到端集成测试**: 运行 `main_orchestrator.py`，覆盖更多模型和配置，全面验证框架集成。
3.  **性能优化**: 分析集成测试结果，识别并解决性能瓶颈。

感谢您使用本框架！
