#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
云服务配置和统一调用接口
"""

import os
import requests
import json
import time
from typing import Dict, List, Any, Optional
import os
import sys
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 所有云服务配置
CLOUD_SERVICES = {
    "together": {
        "name": "Together.ai",
        "api_url": "https://api.together.xyz/v1/chat/completions",
        "api_key_env": "TOGETHER_API_KEY",
        "models": ["mistralai/Mixtral-8x7B-Instruct-v0.1", "meta-llama/Llama-3-8b-chat"],
        "test_prompt": "Hello",
        "type": "openai_compatible"
    },
    "openrouter": {
        "name": "OpenRouter",
        "api_url": "https://openrouter.ai/api/v1/chat/completions",
        "api_key_env": "OPENROUTER_API_KEY",
        "models": ["openai/gpt-3.5-turbo", "anthropic/claude-3-opus", "google/gemma-2-9b-it"],
        "test_prompt": "Hello",
        "type": "openai_compatible"
    },
    "ppinfra": {
        "name": "PPInfra",
        "api_url": "https://api.ppinfra.com/v3/openai/chat/completions",
        "api_key_env": "PPINFRA_API_KEY",
        "models": ["qwen/qwen3-235b-a22b-fp8", "minimaxai/minimax-m1-80k"],
        "test_prompt": "Hello",
        "type": "openai_compatible"
    },
    "gemini": {
        "name": "Google Gemini",
        "api_url": "https://generativelanguage.googleapis.com/v1beta/models",
        "api_key_env": "GEMINI_API_KEY",
        "models": ["gemini-1.5-flash", "gemini-1.5-pro", "gemini-2.0-flash-exp"],
        "test_prompt": "Hello",
        "type": "gemini"
    },
    "dashscope": {
        "name": "阿里云DashScope",
        "api_url": "https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions",
        "api_key_env": "DASHSCOPE_API_KEY",
        "models": ["qwen-plus", "qwen-max", "qwen-turbo"],
        "test_prompt": "你好",
        "type": "openai_compatible"
    },
    "glm": {
        "name": "智谱AI GLM",
        "api_url": "https://open.bigmodel.cn/api/paas/v4/chat/completions",
        "api_key_env": "GLM_API_KEY",
        "models": ["glm-4-plus", "glm-4-air", "glm-4-airx", "glm-4-flash"],
        "test_prompt": "你好",
        "type": "openai_compatible"
    }
}

def _call_openai_compatible(config: Dict, model_name: str, messages: List) -> str:
    """调用与OpenAI兼容的API"""
    api_key = os.getenv(config["api_key_env"])
    if not api_key:
        raise ValueError(f"未设置API密钥: {config['api_key_env']}")

    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {api_key}"}
    payload = {"model": model_name, "messages": messages, "max_tokens": 1024}

    response = requests.post(config["api_url"], headers=headers, json=payload, timeout=240)
    response.raise_for_status()
    data = response.json()
    return data["choices"][0]["message"]["content"]

def _call_gemini(config: Dict, model_name: str, messages: List) -> str:
    """调用Google Gemini API"""
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError(f"未设置API密钥: {config['api_key_env']}")

    url = f"{config['api_url']}/{model_name}:generateContent?key={api_key}"
    headers = {"Content-Type": "application/json"}
    
    # Gemini需要不同的格式
    gemini_contents = []
    for msg in messages:
        if msg['role'] == 'system': # Gemini使用system instructions
            continue
        gemini_contents.append({
            "role": "user" if msg["role"] == "user" else "model",
            "parts": [{"text": msg["content"]}]
        })

    payload = {"contents": gemini_contents}
    
    response = requests.post(url, headers=headers, json=payload, timeout=60)
    response.raise_for_status()
    data = response.json()
    return data['candidates'][0]['content']['parts'][0]['text']

def call_cloud_service(service_name: str, model_name: str, prompt: str, system_prompt: Optional[str] = None) -> str:
    """调用云服务 (统一入口)"""
    if service_name not in CLOUD_SERVICES:
        raise ValueError(f"未知服务: {service_name}")

    config = CLOUD_SERVICES[service_name]
    messages = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    messages.append({"role": "user", "content": prompt})
    
    service_type = config.get("type", "openai_compatible")

    try:
        if service_type == "openai_compatible":
            return _call_openai_compatible(config, model_name, messages)
        elif service_type == "gemini":
            return _call_gemini(config, model_name, messages)
        else:
            raise ValueError(f"未知的服务类型: {service_type}")
    except Exception as e:
        print(f"调用 {service_name}/{model_name} 失败: {e}")
        raise # 重新抛出异常，由调用者处理

def check_service_connectivity(service_name: str, config: Dict[str, Any]) -> Dict[str, Any]:
    """检查单个云服务的连通性"""
    # 特殊服务使用专门的检查函数
    if service_name == "gemini":
        return check_gemini_connectivity()
    
    # 标准OpenAI兼容服务
    result = {
        "service": service_name,
        "name": config["name"],
        "available": False,
        "reason": "",
        "models": []
    }
    
    # 检查API密钥
    api_key = os.getenv(config["api_key_env"])
    if not api_key:
        result["reason"] = f"未设置环境变量 {config['api_key_env']}"
        return result
    
    try:
        # 构建请求头
        headers = {"Content-Type": "application/json", "Authorization": f"Bearer {api_key}"}
        
        # 构建测试请求
        url = config["api_url"]
        payload = {
            "model": config["models"][0],
            "messages": [{"role": "user", "content": config["test_prompt"]}],
            "max_tokens": 100
        }
        
        # 发送测试请求
        response = requests.post(url, headers=headers, json=payload, timeout=10)
        
        if response.status_code == 200:
            result["available"] = True
            result["models"] = config["models"]
            result["reason"] = "连接成功"
        elif response.status_code == 401:
            result["reason"] = "API密钥无效"
        elif response.status_code == 429:
            result["available"] = True  # 配额限制但服务可用
            result["models"] = config["models"]
            result["reason"] = "API配额限制，但服务可用"
        else:
            result["reason"] = f"HTTP {response.status_code}: {response.text[:100]}"
            
    except requests.exceptions.Timeout:
        result["reason"] = "连接超时"
    except requests.exceptions.ConnectionError:
        result["reason"] = "网络连接错误"
    except Exception as e:
        result["reason"] = f"未知错误: {str(e)[:100]}"
    
    return result

def check_gemini_connectivity() -> Dict[str, Any]:
    """检查Google Gemini的连通性"""
    return _check_gemini_connectivity()

def _check_gemini_connectivity() -> Dict[str, Any]:
    """实际检查Google Gemini连通性的函数"""
    service_name = "gemini"
    config = CLOUD_SERVICES[service_name]
    result = {
        "service": service_name,
        "name": config["name"],
        "available": False,
        "reason": "",
        "models": []
    }

    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        result["reason"] = "未设置环境变量 GEMINI_API_KEY"
        return result

    try:
        url = f"{config['api_url']}/{config['models'][0]}:generateContent?key={api_key}"
        headers = {"Content-Type": "application/json"}
        payload = {
            "contents": [{
                "role": "user",
                "parts": [{"text": config["test_prompt"]}]
            }]
        }
        response = requests.post(url, headers=headers, json=payload, timeout=10)

        if response.status_code == 200:
            result["available"] = True
            result["models"] = config["models"]
            result["reason"] = "连接成功"
        elif response.status_code == 401:
            result["reason"] = "API密钥无效"
        else:
            result["reason"] = f"HTTP {response.status_code}: {response.text[:100]}"

    except requests.exceptions.Timeout:
        result["reason"] = "连接超时"
    except requests.exceptions.ConnectionError:
        result["reason"] = "网络连接错误"
    except Exception as e:
        result["reason"] = f"未知错误: {str(e)[:100]}"

    return result

def check_all_services() -> Dict[str, Dict[str, Any]]:
    """检查所有云服务的连通性"""
    results = {}
    
    for service_name, config in CLOUD_SERVICES.items():
        print(f"  检查 {config['name']}...")
        results[service_name] = check_service_connectivity(service_name, config)
    
    return results

def get_available_services() -> List[str]:
    """获取所有可用的服务名称列表"""
    return list(CLOUD_SERVICES.keys())

def get_all_models() -> List[Dict[str, str]]:
    """获取所有模型信息"""
    models = []
    for service_name, config in CLOUD_SERVICES.items():
        for model in config["models"]:
            models.append({
                "service": service_name,
                "model": model,
                "key": f"{model}-{service_name}"
            })
    return models

if __name__ == "__main__":
    # 简单的命令行测试
    print("检查所有云服务连通性...")
    results = check_all_services()
    
    for service, result in results.items():
        status = "✅ 可用" if result["available"] else "❌ 不可用"
        print(f"{CLOUD_SERVICES[service]['name']} ({service}): {status}")
        if not result["available"] and "message" in result:
            print(f"  原因: {result['message']}")
        elif not result["available"] and "error" in result:
            print(f"  错误: {result['error']}")
