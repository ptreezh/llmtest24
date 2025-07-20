# LLM测评系统完整使用指南

## 📋 系统概述

这是一个全面的LLM测评系统，支持对Pillar 9-19共11个高级能力维度进行系统化评价。

### 🎯 评价维度
- **Pillar 9**: 创意生成 (Creativity)
- **Pillar 10**: 数学推理 (Math & Quantitative Reasoning)
- **Pillar 11**: 安全对齐 (Safety & Ethics)
- **Pillar 12**: 角色扮演 (Persona & Consistency)
- **Pillar 13**: 复杂指令解析 (Complex Instruction Parsing)
- **Pillar 14**: 角色深度 (Persona Depth)
- **Pillar 15**: 协作能力 (Collaboration)
- **Pillar 16**: 涌现分析 (Emergence Analysis)
- **Pillar 17**: 图谱生成 (DAG Generation)
- **Pillar 18**: 容错协调 (Fault Tolerance)
- **Pillar 19**: 网络分析 (Network Analysis)

## 🚀 快速开始

### 1. 环境准备
```bash
# 确保Ollama服务运行
ollama serve

# 拉取测试模型
ollama pull your-model-name

# 安装Python依赖
pip install ollama pandas matplotlib
```

### 2. 配置模型
编辑 `config.py` 文件：
```python
MODEL_TO_TEST = "your-model-name"
```

### 3. 运行测试
```bash
# 方式1: 标准测试
python run_all_tests.py

# 方式2: 增强版测试（推荐）
python run_all_tests_with_output.py

# 方式3: 单独运行评价
python evaluate_results.py
```

## 📊 评价脚本详解

### 核心评价脚本 (`evaluate_results.py`)

**功能特点**:
- ✅ 支持所有11个Pillar的自动评价
- ✅ 多维度评分标准（0-10分）
- ✅ 详细的反馈和改进建议
- ✅ 按类别统计和排名
- ✅ 自动生成等级评定（A-F级）

**评价标准**:
- **优秀 (9-10分)**: 完全满足要求，表现出色
- **良好 (7-8分)**: 基本满足要求，有小瑕疵
- **中等 (5-6分)**: 部分满足要求，有明显不足
- **较差 (3-4分)**: 勉强理解任务，执行效果差
- **很差 (1-2分)**: 基本不理解任务或严重错误
- **无效 (0分)**: 无响应或完全无关

### 深度分析脚本 (`analyze_results.py`)

**功能特点**:
- 📈 响应质量多维度分析
- 📊 统计数据可视化
- 🔍 问题案例识别
- 💾 结构化数据导出

**分析维度**:
- 响应长度统计
- 句子结构分析
- 代码生成能力
- 内容结构化程度
- 完整性评估

### 增强测试脚本 (`run_all_tests_with_output.py`)

**功能特点**:
- 🔄 自动确保所有测试结果保存
- 🔧 自动修复缺少输出保存的测试脚本
- 📝 详细的运行日志
- ⚡ 自动运行评价分析

## 📈 评价报告解读

### 总体等级说明
- **A级 (85-100%)**: 优秀，可用于生产环境
- **B级 (70-84%)**: 良好，可用于大多数场景
- **C级 (55-69%)**: 中等，需要改进
- **D级 (40-54%)**: 较差，需要大幅改进
- **F级 (0-39%)**: 不合格，不建议使用

### 各维度状态标识
- ✅ **优秀**: 80%以上，表现出色
- ⚠️ **中等**: 60-79%，有改进空间
- ❌ **需改进**: 60%以下，急需提升

## 🔧 自定义评价标准

### 修改评价权重
在 `evaluate_results.py` 中修改 `evaluation_criteria` 字典：

```python
"creativity": {
    "name": "创意生成",
    "criteria": [
        "文风模仿准确性",  # 可调整权重
        "创意内容质量", 
        "语言表达流畅性",
        "任务完成度"
    ],
    "max_score": 10  # 可调整总分
}
```

### 添加新的评价维度
1. 在 `evaluation_criteria` 中添加新维度
2. 实现对应的 `evaluate_xxx()` 方法
3. 在 `generate_report()` 中添加调用逻辑

### 自定义评分逻辑
每个 `evaluate_xxx()` 方法返回 `(score, feedback)` 元组：

```python
def evaluate_custom(self, result: Dict) -> Tuple[int, str]:
    response = result["response"].strip()
    score = 0
    feedback = []
    
    # 自定义评分逻辑
    if "关键词" in response:
        score += 3
        feedback.append("✓ 包含关键词")
    
    return min(score, 10), "; ".join(feedback)
```

## 📁 输出文件说明

### 主要输出文件
- `evaluation_report.md`: 主要评价报告
- `comprehensive_analysis_report.md`: 深度分析报告
- `analysis_data.json`: 结构化分析数据
- `testout/`: 所有测试结果文件

### 测试结果文件格式
```
用例编号: case1
类型: 测试类型描述
PROMPT:
测试提示词内容

MODEL RESPONSE:
模型响应内容
```

## 🎯 最佳实践

### 1. 定期测试
- 建议每次模型更新后运行完整测试
- 保存历史测试结果进行趋势分析

### 2. 对比分析
```bash
# 测试不同模型
MODEL_TO_TEST="model-a" python run_all_tests_with_output.py
mv evaluation_report.md evaluation_report_model_a.md

MODEL_TO_TEST="model-b" python run_all_tests_with_output.py
mv evaluation_report.md evaluation_report_model_b.md
```

### 3. 问题诊断
- 关注F级维度，优先改进
- 分析无响应或响应过短的案例
- 检查提示词设计是否合理

### 4. 持续优化
- 根据评价结果调整提示词
- 针对薄弱环节增加训练数据
- 定期更新评价标准

## 🔍 故障排除

### 常见问题
1. **模型未找到**: 检查 `config.py` 中的模型名称
2. **Ollama连接失败**: 确保 `ollama serve` 正在运行
3. **编码错误**: 确保所有文件使用UTF-8编码
4. **权限错误**: 检查输出目录的写入权限

### 调试技巧
```bash
# 检查Ollama状态
ollama list

# 测试单个Pillar
python tests/test_pillar_09_creativity.py

# 查看详细错误
python run_all_tests_with_output.py 2>&1 | tee debug.log
```

## 📞 技术支持

如需技术支持或功能建议，请：
1. 检查本文档的故障排除部分
2. 查看生成的错误日志
3. 提供详细的错误信息和环境配置

---

**版本**: v2.0
**更新时间**: 2025-06-21
**兼容性**: Python 3.7+, Ollama 0.1.0+
