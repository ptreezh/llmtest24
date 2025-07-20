# LLM Role Independence Testing Framework

一个用于测试大语言模型角色独立性和一致性的综合测试框架。

## 功能特性

- **角色破坏测试 (Character Breaking Test)**: 测试模型在面对角色破坏性提示时的抵抗能力
- **隐式认知测试 (Implicit Cognition Test)**: 评估模型对角色身份的隐式理解和维持
- **纵向一致性测试 (Longitudinal Consistency Test)**: 检验模型在长期对话中的角色一致性
- **内存管理**: 跟踪和分析角色一致性的历史记录
- **文本分析**: 深度分析响应的语言学特征和一致性
- **多格式报告**: 支持JSON、CSV、Excel和HTML格式的测试报告

## 安装

```bash
pip install -r requirements.txt
```

## 快速开始

```python
from testLLM import TestRunner, ConfigManager

# 初始化配置
config = ConfigManager('config/test_config.yaml')

# 创建测试运行器
runner = TestRunner(config)

# 运行测试
results = runner.run_comprehensive_test(
    models=['gpt-4', 'claude-3'],
    roles=['software_engineer', 'data_scientist']
)

# 生成报告
runner.generate_report(results, 'output/test_report')
```

## 配置

在 `config/test_config.yaml` 中配置测试参数：

```yaml
models:
  gpt-4:
    api_key: "your-api-key"
    base_url: "https://api.openai.com/v1"
  
test_settings:
  character_breaking:
    max_attempts: 5
    severity_levels: [1, 2, 3]
  
  implicit_cognition:
    question_types: ["identity", "expertise", "background"]
  
  longitudinal_consistency:
    session_length: 10
    consistency_threshold: 0.7

output:
  formats: ["json", "html", "excel"]
  directory: "results"
```

## 测试类型

### 1. 角色破坏测试
测试模型抵抗角色破坏性提示的能力，包括：
- 直接身份质疑
- 角色转换请求
- 元认知诱导

### 2. 隐式认知测试
评估模型对角色的隐式理解：
- 专业知识一致性
- 行为模式匹配
- 价值观对齐

### 3. 纵向一致性测试
检验长期对话中的一致性：
- 记忆连贯性
- 风格稳定性
- 观点一致性

## 输出格式

框架支持多种输出格式：

- **JSON**: 结构化数据，便于程序处理
- **CSV**: 表格数据，便于数据分析
- **Excel**: 多工作表报告，包含汇总和详细数据
- **HTML**: 可视化报告，便于查看和分享

## 扩展性

框架采用模块化设计，支持：
- 自定义测试类型
- 新的模型适配器
- 自定义评估指标
- 插件式报告生成器

## 许可证

MIT License

## 贡献

欢迎提交Issue和Pull Request来改进这个框架。