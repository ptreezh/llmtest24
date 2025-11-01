#!/usr/bin/env python3
"""
检查云服务连通性的脚本
"""

import os
import sys
import requests
import json
from typing import Dict, Any
from pathlib import Path
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

def _check_openai_compatible_service(config: Dict[str, Any]) -> Dict[str, Any]:
    """检查与OpenAI兼容的服务连通性"""
    result = {
        "available": False,
        "name": config["name"],
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
        headers = {
            "Content-Type": "application/json", 
            "Authorization": f"Bearer {api_key}"
        }
        
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

def _check_gemini_service(config: Dict[str, Any]) -> Dict[str, Any]:
    """检查Google Gemini服务连通性"""
    result = {
        "available": False,
        "name": config["name"],
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
        service_type = config.get("type", "openai_compatible")
        
        if service_type == "openai_compatible":
            results[service_name] = _check_openai_compatible_service(config)
        elif service_type == "gemini":
            results[service_name] = _check_gemini_service(config)
        else:
            results[service_name] = {
                "available": False,
                "name": config["name"],
                "reason": f"未知的服务类型: {service_type}",
                "models": []
            }
    
    return results

def main():
    """主函数"""
    # 确保环境变量已加载
    load_dotenv()
    print("检查所有云服务连通性...")
    service_results = check_all_services()
    
    for service, result in service_results.items():
        status = "✅ 可用" if result["available"] else "❌ 不可用"
        print(f"{result['name']} ({service}): {status}")
        if not result["available"] and "reason" in result:
            print(f"  原因: {result['reason']}")

if __name__ == "__main__":
    main()
