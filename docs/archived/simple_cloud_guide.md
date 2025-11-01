# 云LLM服务扩展系统使用指南

## 1. 系统概述

这是一个简单易用的云LLM服务扩展系统，让添加新云服务变得超级简单，同时支持智能连通性检测和测试状态管理。

## 2. 快速开始

### 2.1 配置环境变量

在项目根目录创建 `.env` 文件，添加需要测试的云服务API密钥：

```
# 七牛云
QINIU_API_KEY=your_qiniu_api_key_here

# SiliconFlow
SILICONFLOW_API_KEY=your_siliconflow_api_key_here

# Together.ai
TOGETHER_API_KEY=your_together_api_key_here

# OpenRouter
OPENROUTER_API_KEY=your_openrouter_api_key_here

# 百度文心
BAIDU_API_KEY=your_baidu_api_key_here
BAIDU_SECRET_KEY=your_baidu_secret_key_here
```

### 2.2 运行测试

```bash
# 运行智能测试调度器
python smart_test_runner.py

# 查看可用服务列表
python smart_test_runner.py --list-services

# 查看可用模型列表
python smart_test_runner.py --list-models

# 只测试指定服务
python smart_test_runner.py --services qiniu,siliconflow

# 强制重新测试所有模型
python smart_test_runner.py --force-retest
```

### 2.3 管理测试状态

```bash
# 查看当前测试状态
python tools/reset_test_status.py

# 重置所有测试状态
python tools/reset_test_status.py --reset-all

# 重置指定服务的测试状态
python tools/reset_test_status.py --reset-service qiniu

# 重置指定模型的测试状态
python tools/reset_test_status.py --reset-model deepseek-v3-qiniu
```

## 3. 添加新云服务

### 3.1 标准API服务 (3步完成)

1. **添加API密钥**: 在 `.env` 文件中添加 `NEW_SERVICE_API_KEY=xxx`

2. **添加服务配置**: 在 `cloud_services.py` 的 `CLOUD_SERVICES` 字典中添加配置块：

```python
"new_service": {
    "name": "新服务显示名称",
    "api_url": "https://api.newservice.com/v1/chat/completions",
    "api_key_env": "NEW_SERVICE_API_KEY",
    "models": ["model1", "model2", "model3"],
    "test_prompt": "Hello",
    "headers_template": {"Authorization": "Bearer {api_key}"}
}
```

3. **运行测试**: 执行 `python smart_test_runner.py` 自动检测并测试

### 3.2 特殊API服务 (额外1步)

如果新服务的API格式不是标准的OpenAI兼容格式，需要额外添加特殊处理：

1. 在配置中添加 `"special_handler": "service_name"`

2. 在 `call_special_service` 函数中添加特殊处理逻辑：

```python
if service_name == "new_special_service":
    # 特殊服务的处理逻辑
    # ...
    return response_json
```

## 4. 系统架构

### 4.1 核心文件

- `cloud_services.py` - 云服务配置和统一调用接口
- `smart_test_runner.py` - 智能测试调度器
- `test_status.json` - 测试状态文件
- `tools/reset_test_status.py` - 测试状态管理工具

### 4.2 工作流程

1. 智能调度器检查所有云服务的连通性
2. 根据连通性和测试状态决定需要测试的模型
3. 依次测试每个模型并更新测试状态
4. 测试完成后生成测试报告

## 5. 故障排除

### 5.1 连通性问题

- **API密钥错误**: 检查 `.env` 文件中的API密钥是否正确
- **网络连接问题**: 检查网络连接和防火墙设置
- **服务不可用**: 检查云服务是否可用，或者配额是否已用完

### 5.2 测试状态问题

- **状态文件损坏**: 删除 `test_status.json` 文件，系统会自动创建新的
- **状态不一致**: 使用 `--reset-all` 重置所有测试状态

## 6. 支持的云服务

- **七牛云DeepSeek** - 中文大模型服务
- **SiliconFlow** - 国内开源模型服务
- **Together.ai** - 国际开源模型服务
- **OpenRouter** - 多模型聚合服务
- **百度文心** - 百度智能云大模型服务