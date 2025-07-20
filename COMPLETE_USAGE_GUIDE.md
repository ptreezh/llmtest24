# testLLM2 完整使用指南

## 🎯 系统概述

testLLM2是一个全面的LLM高级能力测评系统，支持Pillar 9-19共11个维度的自动化测试、评价和分析。

### ✨ 核心特性
- ✅ **全面覆盖**: 11个高级能力维度
- ✅ **自动重试**: 智能检测和重试失败测试
- ✅ **多层分析**: 从概览到详细的评价报告
- ✅ **编码安全**: 完善的编码错误处理
- ✅ **易于扩展**: 模块化设计

## 🚀 快速开始

### 1. 环境准备
```bash
# 启动Ollama服务
ollama serve

# 确认模型可用
ollama list

# 配置测试模型
# 编辑 config.py: MODEL_TO_TEST = "your-model-name"
```

### 2. 一键运行 (推荐)
```bash
# 使用安全测试运行器 (处理编码问题)
python safe_test_runner.py

# 或使用增强版测试运行器 (包含重试机制)
python enhanced_test_runner.py
```

### 3. 查看结果
```bash
# 生成评价报告
python evaluate_results.py

# 生成深度分析
python analyze_results.py

# 查看报告文件
# - evaluation_report.md: 标准评价报告
# - comprehensive_analysis_report.md: 深度分析报告
```

## 🛠️ 工具详解

### 核心测试工具

#### 1. `safe_test_runner.py` - 安全测试运行器
**用途**: 处理编码问题的安全测试执行
```bash
python safe_test_runner.py
```
**特点**:
- 自动处理Unicode编码错误
- 超时保护 (5分钟)
- 详细的错误日志

#### 2. `enhanced_test_runner.py` - 增强测试运行器  
**用途**: 包含智能重试的高级测试执行
```bash
python enhanced_test_runner.py
```
**特点**:
- 自动重试机制 (最多3次)
- 上下文管理
- 失败恢复策略

#### 3. `run_all_tests_with_output.py` - 完整测试套件
**用途**: 确保所有测试结果都被保存
```bash
python run_all_tests_with_output.py
```

### 分析评价工具

#### 1. `evaluate_results.py` - 标准评价分析
**用途**: 生成详细的评价报告和改进建议
```bash
python evaluate_results.py
```
**输出**: `evaluation_report.md`

#### 2. `analyze_results.py` - 深度统计分析
**用途**: 生成统计数据和质量分析
```bash
python analyze_results.py  
```
**输出**: `comprehensive_analysis_report.md`, `analysis_data.json`

### 问题修复工具

#### 1. `retry_failed_tests.py` - 失败测试重试
**用途**: 自动检测和重试失败的测试
```bash
python retry_failed_tests.py
```
**特点**:
- 自动检测无响应测试
- 智能重试策略
- 备份原始结果

#### 2. `fix_encoding_issues.py` - 编码问题修复
**用途**: 修复测试脚本中的编码问题
```bash
python fix_encoding_issues.py
```

#### 3. `quick_fix_encoding.py` - 快速语法修复
**用途**: 快速修复语法错误
```bash
python quick_fix_encoding.py
```

### 演示和帮助工具

#### 1. `demo_evaluation.py` - 完整流程演示
**用途**: 交互式演示整个测试流程
```bash
python demo_evaluation.py
```

## 📊 测试维度说明

| Pillar | 维度名称 | 主要测试内容 | 评价重点 |
|--------|----------|--------------|----------|
| 9 | 创意生成 | 文风模仿、广告创作 | 创意质量、文风准确性 |
| 10 | 数学推理 | 数学问题求解 | 逻辑推理、计算准确性 |
| 11 | 安全对齐 | 有害请求处理 | 安全意识、拒绝策略 |
| 12 | 角色扮演 | 多轮角色对话 | 角色一致性、情境适应 |
| 13 | 指令解析 | 复杂任务分解 | 理解准确性、执行能力 |
| 14 | 角色深度 | 专业角色能力 | 专业知识、任务执行 |
| 15 | 协作能力 | 团队协作场景 | 协作意识、任务流转 |
| 16 | 涌现分析 | 冲突问题分析 | 问题识别、解决方案 |
| 17 | 图谱生成 | DAG图谱创建 | 语法正确性、逻辑结构 |
| 18 | 容错协调 | 项目风险应对 | 影响分析、应对计划 |
| 19 | 网络分析 | 关键路径计算 | 计算能力、风险识别 |

## 🎯 最佳实践工作流

### 标准测试流程
```bash
# 1. 运行测试
python safe_test_runner.py

# 2. 检查失败测试并重试
python retry_failed_tests.py

# 3. 生成评价报告
python evaluate_results.py

# 4. 生成深度分析
python analyze_results.py

# 5. 查看结果
cat evaluation_report.md
```

### 问题排查流程
```bash
# 1. 检查编码问题
python fix_encoding_issues.py

# 2. 快速修复语法错误
python quick_fix_encoding.py

# 3. 重新运行测试
python safe_test_runner.py

# 4. 如果仍有问题，使用演示脚本
python demo_evaluation.py
```

## ⚠️ 常见问题解决

### 1. 测试无响应问题
**现象**: 某些测试返回空响应或很短的响应
**原因**: 
- 上下文累积过长 (多轮对话)
- 模型状态不稳定
- 网络或服务问题

**解决方案**:
```bash
# 自动重试失败测试
python retry_failed_tests.py

# 使用增强测试运行器
python enhanced_test_runner.py
```

### 2. 编码错误问题
**现象**: `UnicodeDecodeError` 或语法错误
**解决方案**:
```bash
# 修复编码问题
python fix_encoding_issues.py

# 快速修复语法
python quick_fix_encoding.py
```

### 3. Ollama连接问题
**现象**: 无法连接到Ollama服务
**解决方案**:
```bash
# 检查服务状态
ollama list

# 重启服务
ollama serve

# 检查模型配置
cat config.py
```

## 📈 评价标准

### 评分等级
- **A级 (85-100%)**: 优秀，可用于生产环境
- **B级 (70-84%)**: 良好，可用于大多数场景
- **C级 (55-69%)**: 中等，需要改进
- **D级 (40-54%)**: 较差，需要大幅改进
- **F级 (0-39%)**: 不合格，不建议使用

### 单项评分 (0-10分)
- **9-10分**: 优秀，完全满足要求
- **7-8分**: 良好，基本满足要求
- **5-6分**: 中等，部分满足要求
- **3-4分**: 较差，勉强理解任务
- **1-2分**: 很差，基本不理解
- **0分**: 无效，无响应或完全无关

## 🔧 自定义和扩展

### 添加新的测试维度
1. 在 `tests/` 目录创建新的测试脚本
2. 在 `user_prompts/` 目录添加提示文件
3. 在 `evaluate_results.py` 中添加评价逻辑
4. 更新配置和文档

### 修改评价标准
编辑 `evaluate_results.py` 中的评价方法:
```python
def evaluate_custom(self, result: Dict) -> Tuple[int, str]:
    # 自定义评价逻辑
    pass
```

### 调整重试策略
编辑 `enhanced_test_runner.py` 中的参数:
```python
runner = EnhancedTestRunner(
    max_retries=5,      # 增加重试次数
    timeout_seconds=120, # 增加超时时间
    retry_delay=10      # 增加重试间隔
)
```

## 📚 文档资源

- `README_EVALUATION.md`: 详细使用说明
- `evaluation_criteria.md`: 评价标准详解
- `test_failure_analysis.md`: 失败原因分析
- `COMPLETE_USAGE_GUIDE.md`: 本完整指南

## 🎉 总结

testLLM2提供了一套完整、可靠、易用的LLM测评解决方案。通过合理使用各种工具和遵循最佳实践，您可以获得准确、全面的模型性能评估结果。

**记住**: 测试的可靠性和一致性比单次的高分更重要！
