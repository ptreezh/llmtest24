# 共享工具函数

import ollama
import os
import shutil
import tempfile
import time
import json
import subprocess
import sys
import requests
from pathlib import Path
from dotenv import load_dotenv
from config.config import OLLAMA_HOST, TEST_WORKSPACE_DIR, LOG_DIR, REPORT_DIR, MODELS_LIST_FILE
from cloud_connection_cache import connection_cache

# 加载环境变量
load_dotenv()

# === 外部API配置 - 从环境变量读取 ===
OPENROUTER_API_URL = os.getenv("OPENROUTER_API_URL", "https://openrouter.ai/api/v1/chat/completions")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

TOGETHER_API_URL = os.getenv("TOGETHER_API_URL", "https://api.together.xyz/v1/chat/completions")
TOGETHER_API_KEY = os.getenv("TOGETHER_API_KEY")

QINIU_API_URL = os.getenv("QINIU_API_URL", "https://api.qnaigc.com/v1/chat/completions")
QINIU_API_KEY = os.getenv("QINIU_API_KEY")
QINIU_GROUP = os.getenv("QINIU_GROUP", "DeepSeek")

PPINFRA_API_URL = os.getenv("PPINFRA_API_URL", "https://api.ppinfra.com/v3/openai/chat/completions")
PPINFRA_API_KEY = os.getenv("PPINFRA_API_KEY")

GEMINI_API_URL = os.getenv("GEMINI_API_URL", "https://generativelanguage.googleapis.com/v1beta/models")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

DASHSCOPE_API_URL = os.getenv("DASHSCOPE_API_URL", "https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions")
DASHSCOPE_API_KEY = os.getenv("DASHSCOPE_API_KEY")

GLM_API_URL = os.getenv("GLM_API_URL", "https://open.bigmodel.cn/api/paas/v4/chat/completions")
GLM_API_KEY = os.getenv("GLM_API_KEY")

BAIDU_API_KEY = os.getenv("BAIDU_API_KEY")
BAIDU_SECRET_KEY = os.getenv("BAIDU_SECRET_KEY")
BAIDU_TOKEN_URL = os.getenv("BAIDU_TOKEN_URL", "https://aip.baidubce.com/oauth/2.0/token")
BAIDU_API_BASE = os.getenv("BAIDU_API_BASE", "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat")
BAIDU_ACCESS_TOKEN = None  # 动态获取
BAIDU_TOKEN_EXPIRE_TIME = 0

def get_baidu_access_token():
    """获取百度云access_token"""
    global BAIDU_ACCESS_TOKEN, BAIDU_TOKEN_EXPIRE_TIME
    
    # 检查token是否还有效（提前5分钟刷新）
    if BAIDU_ACCESS_TOKEN and time.time() < BAIDU_TOKEN_EXPIRE_TIME - 300:
        return BAIDU_ACCESS_TOKEN
    
    url = "https://aip.baidubce.com/oauth/2.0/token"
    params = {
        "grant_type": "client_credentials",
        "client_id": BAIDU_API_KEY,
        "client_secret": BAIDU_SECRET_KEY
    }
    
    try:
        response = requests.post(url, params=params, timeout=30)
        response.raise_for_status()
        data = response.json()
        
        BAIDU_ACCESS_TOKEN = data["access_token"]
        BAIDU_TOKEN_EXPIRE_TIME = time.time() + data.get("expires_in", 2592000)  # 默认30天
        
        print(f"    ✅ 百度云access_token获取成功")
        return BAIDU_ACCESS_TOKEN
        
    except Exception as e:
        print(f"    ❌ 获取百度云access_token失败: {e}")
        return None

def call_baidu_llm(model_name: str, messages: list, options: dict = None, max_retries: int = 3) -> tuple:
    """调用百度云LLM API"""
    if options is None:
        options = {}
    
    # 获取access_token
    access_token = get_baidu_access_token()
    if not access_token:
        return "[API Error: Failed to get Baidu access token]", None
    
    # 模型映射到对应的API端点
    model_endpoints = {
        "ernie-4.0-8k": "completions_pro",
        "ernie-4.0-8k-preview": "ernie-4.0-8k-preview",
        "ernie-3.5-8k": "completions",
        "ernie-3.5-8k-0205": "ernie-3.5-8k-0205",
        "ernie-bot-turbo": "eb-instant",
        "ernie-bot": "completions",
        "ernie-speed-8k": "ernie_speed",
        "ernie-speed-128k": "ernie-speed-128k",
        "ernie-lite-8k": "ernie-lite-8k",
        "ernie-tiny-8k": "ernie-tiny-8k"
    }
    
    endpoint = model_endpoints.get(model_name, "completions")
    url = f"https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/{endpoint}?access_token={access_token}"
    
    headers = {
        "Content-Type": "application/json"
    }
    
    # 转换消息格式 - 百度云需要特定格式
    baidu_messages = []
    system_content = ""
    
    for msg in messages:
        if msg["role"] == "system":
            system_content = msg["content"]
        elif msg["role"] in ["user", "assistant"]:
            baidu_messages.append({
                "role": msg["role"],
                "content": msg["content"]
            })
    
    payload = {
        "messages": baidu_messages,
        "temperature": options.get("temperature", 0.7),
        "top_p": options.get("top_p", 0.8),
        "penalty_score": options.get("penalty_score", 1.0),
        "max_output_tokens": options.get("max_tokens", 4096),
        "stream": False
    }
    
    # 如果有系统消息，添加到payload中
    if system_content:
        payload["system"] = system_content
    
    for attempt in range(max_retries):
        try:
            print(f"    🔗 Calling 百度云 API: {model_name}")
            
            response = requests.post(url, headers=headers, json=payload, timeout=120)
            response.raise_for_status()
            data = response.json()
            
            # 检查API错误
            if "error_code" in data:
                print(f"    ❌ 百度云API错误: {data.get('error_msg', 'Unknown error')}")
                if attempt < max_retries - 1:
                    time.sleep(2)
                    continue
                else:
                    return f"[API Error: Baidu API error - {data.get('error_msg', 'Unknown')}]", None
            
            # 提取响应内容
            if "result" in data:
                content = data["result"]
                if content and content.strip():
                    print(f"    ✅ 百度云 '{model_name}' success: {len(content)} chars")
                    return content, {"role": "assistant", "content": content}
                else:
                    print(f"    ⚠️ Empty response from 百度云 on attempt {attempt + 1}")
            else:
                print(f"    ⚠️ No result in response: {data}")
                
        except requests.exceptions.HTTPError as e:
            print(f"    ❌ 百度云 HTTP error on attempt {attempt + 1}: {e}")
            if hasattr(e, 'response'):
                print(f"    Response: {e.response.text}")
            if attempt < max_retries - 1:
                time.sleep(2)
                continue
        except Exception as e:
            print(f"    ❌ 百度云 API error on attempt {attempt + 1}: {e}")
            if attempt < max_retries - 1:
                time.sleep(2)
                continue
    
    return f"[API Error: 百度云 failed after {max_retries} attempts]", None

# --- Ollama Client Initialization ---
try:
    # === 外部API配置 ===
    QINIU_API_URL = "https://api.qnaigc.com/v1/chat/completions"
    QINIU_API_KEY = "sk-85a07f1fd99e9ebb760104e7257a8678c0f0e018fd1a22019e4506323b6db0af"
    QINIU_GROUP = "DeepSeek"

    # --- 新增 Together.ai 配置 ---
    TOGETHER_API_URL = "https://api.together.xyz/v1/chat/completions"
    TOGETHER_API_KEY = "08f6372819b36b569686377e08dc82c61d32a984c4ce5a6e3c00f5a92d33a0f6"  # TODO: 替换为你的Together.ai密钥


    client = ollama.Client(host=OLLAMA_HOST)
    # 尝试连接，以便尽早发现问题
    client.list()
    print(f"[INFO] Connected to Ollama at {OLLAMA_HOST}")
except Exception as e:
    print(f"--- FATAL ERROR ---")
    print(f"无法连接到Ollama服务于 {OLLAMA_HOST}")
    print(f"请确保Ollama正在运行，并且config.py中的OLLAMA_HOST配置正确。")
    print(f"错误详情: {e}")
    # Allow proceeding for cases where ollama is not strictly required by all scripts, but exit if critical.
    # For now, we'll allow continuation but warn. For robustness, consider more granular error handling per script.
    pass

# --- 外部API调用函数 ---
def call_qiniu_deepseek(messages: list, options: dict = None, max_retries: int = 3) -> tuple:
    """
    调用七牛云 DeepSeek (OpenAI兼容) API
    Args:
        messages: 消息列表，格式为 [{"role": "user", "content": "..."}]
        options: 选项参数（温度等）
        max_retries: 最大重试次数
    Returns:
        tuple: (content, response_message)
    """
    headers = {
        "Authorization": f"Bearer {QINIU_API_KEY}",
        "Content-Type": "application/json"
    }

    # 提取用户消息内容
    user_content = ""
    for msg in messages:
        if msg["role"] == "user":
            user_content += msg["content"] + "\n"

    payload = {
        "model": "deepseek-v3",
        "messages": messages,
        "max_tokens": 1024,
        "temperature": options.get("temperature", 0.7) if options else 0.7,
    }

    for attempt in range(max_retries):
        try:
            response = requests.post(QINIU_API_URL, headers=headers, json=payload, timeout=240)
            response.raise_for_status()
            data = response.json()
            content = data['choices'][0]['message']['content']

            if content and content.strip():
                print(f"    ✅ Qiniu DeepSeek success: {len(content)} chars")
                # 构造与Ollama兼容的响应格式
                response_message = {
                    "role": "assistant",
                    "content": content
                }
                return content, response_message
            else:
                print(f"    ⚠️ Empty response from Qiniu DeepSeek on attempt {attempt + 1}")

        except Exception as e:
            print(f"    ❌ Qiniu DeepSeek API error on attempt {attempt + 1}: {e}")
            if attempt < max_retries - 1:
                time.sleep(2)
                continue

    error_msg = f"[API Error: Qiniu DeepSeek API failed after {max_retries} attempts]"
    return error_msg, None

def call_togetherai(model_name: str, messages: list, options: dict = None, max_retries: int = 3) -> tuple:
    """
    调用 Together.ai (OpenAI兼容) API
    Args:
        model_name: 要在Together.ai上调用的模型名称 (如 'mistralai/Mixtral-8x7B-Instruct-v0.1')
        messages: 消息列表
        options: 选项参数 (温度等)
        max_retries: 最大重试次数
    Returns:
        tuple: (content, response_message)
    """
    headers = {
        "Authorization": f"Bearer {TOGETHER_API_KEY}",
        "Content-Type": "application/json",
    }
    if options is None:
        options = {}
    payload = {
        "model": model_name,
        "messages": messages,
        "max_tokens": options.get("max_tokens", 4096),
        "temperature": options.get("temperature", 0.7),
        "top_p": options.get("top_p", 0.7),
        "top_k": options.get("top_k", 50),
        "repetition_penalty": options.get("repetition_penalty", 1)
    }
    for attempt in range(max_retries):
        try:
            response = requests.post(TOGETHER_API_URL, headers=headers, json=payload, timeout=120)
            response.raise_for_status()
            data = response.json()
            content = data['choices'][0]['message']['content']
            if content and content.strip():
                print(f"    ✅ Together.ai '{model_name}' success: {len(content)} chars")
                response_message = {
                    "role": "assistant",
                    "content": content
                }
                return content, response_message
            else:
                print(f"    ⚠️ Empty response from Together.ai on attempt {attempt + 1}")
        except requests.exceptions.HTTPError as e:
            print(f"    ❌ Together.ai API HTTP error on attempt {attempt + 1}: {e.response.status_code} {e.response.reason}")
            print(f"    Response Body: {e.response.text}")
            if attempt < max_retries - 1:
                time.sleep(2)
                continue
        except Exception as e:
            print(f"    ❌ Together.ai API error on attempt {attempt + 1}: {e}")
            if attempt < max_retries - 1:
                time.sleep(2)
                continue
    error_msg = f"[API Error: Together.ai API failed for model '{model_name}' after {max_retries} attempts]"
    return error_msg, None

def call_openrouter(model_name: str, messages: list, options: dict = None, max_retries: int = 3) -> tuple:
    """
    调用 OpenRouter (OpenAI兼容) API
    Args:
        model_name: OpenRouter上的模型名 (如 'mistralai/mixtral-8x7b-instruct')
        messages: 消息列表
        options: 选项参数 (温度等)
        max_retries: 最大重试次数
    Returns:
        tuple: (content, response_message)
    """
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
    }
    if options is None:
        options = {}
    payload = {
        "model": model_name,
        "messages": messages,
        "max_tokens": options.get("max_tokens", 4096),
        "temperature": options.get("temperature", 0.7),
        "top_p": options.get("top_p", 0.7),
        "top_k": options.get("top_k", 50),
        "repetition_penalty": options.get("repetition_penalty", 1)
    }
    for attempt in range(max_retries):
        try:
            response = requests.post(OPENROUTER_API_URL, headers=headers, json=payload, timeout=120)
            response.raise_for_status()
            data = response.json()
            content = data['choices'][0]['message']['content']
            if content and content.strip():
                print(f"    ✅ OpenRouter '{model_name}' success: {len(content)} chars")
                response_message = {
                    "role": "assistant",
                    "content": content
                }
                return content, response_message
            else:
                print(f"    ⚠️ Empty response from OpenRouter on attempt {attempt + 1}")
        except requests.exceptions.HTTPError as e:
            print(f"    ❌ OpenRouter API HTTP error on attempt {attempt + 1}: {e.response.status_code} {e.response.reason}")
            print(f"    Response Body: {e.response.text}")
            if attempt < max_retries - 1:
                time.sleep(2)
                continue
        except Exception as e:
            print(f"    ❌ OpenRouter API error on attempt {attempt + 1}: {e}")
            if attempt < max_retries - 1:
                time.sleep(2)
                continue
    error_msg = f"[API Error: OpenRouter API failed for model '{model_name}' after {max_retries} attempts]"
    return error_msg, None

def call_multi_cloud_smart(model_name, messages, options=None, max_retries=3):
    """
    智能云端调用 - 基于连接缓存优化服务选择顺序
    """
    # 获取可用的API函数映射
    api_mapping = {
        'openrouter': lambda: call_openrouter(model_name, messages, options, max_retries),
        'together': lambda: call_togetherai(model_name, messages, options, max_retries),
    }
    
    # 获取优化后的服务顺序
    available_services = list(api_mapping.keys())
    preferred_services = connection_cache.get_preferred_services(available_services)
    
    print(f"🔄 智能云端调用顺序: {preferred_services}")
    
    for service_name in preferred_services:
        # 检查是否应该跳过
        if connection_cache.should_skip_service(service_name):
            continue
            
        try:
            print(f"🌐 尝试服务: {service_name}")
            api_func = api_mapping[service_name]
            content, response_message = api_func()
            
            if content and not str(content).startswith("[API Error"):
                print(f"✅ {service_name} 连接成功")
                connection_cache.mark_service_success(service_name)
                return content, response_message
            else:
                print(f"❌ {service_name} 返回错误: {content}")
                connection_cache.mark_service_failed(service_name, "API返回错误")
                
        except Exception as e:
            print(f"❌ {service_name} 连接异常: {e}")
            connection_cache.mark_service_failed(service_name, str(e))
    
    # 全部失败
    print("❌ 所有云端服务都失败")
    return "[API Error: All cloud APIs failed]", None

# 保持原函数作为备用
def call_multi_cloud(model_name, messages, options=None, max_retries=3):
    """
    原版多云调用函数 - 保持向后兼容
    """
    return call_multi_cloud_smart(model_name, messages, options, max_retries)

def call_ppinfra(model_name: str, messages: list, options: dict = None, max_retries: int = 3) -> tuple:
    """调用 PPInfra (OpenAI兼容) API"""
    headers = {
        "Authorization": f"Bearer {PPINFRA_API_KEY}",
        "Content-Type": "application/json",
    }
    if options is None:
        options = {}
    payload = {
        "model": model_name,
        "messages": messages,
        "max_tokens": options.get("max_tokens", 4096),
        "temperature": options.get("temperature", 0.7),
    }
    for attempt in range(max_retries):
        try:
            response = requests.post(PPINFRA_API_URL, headers=headers, json=payload, timeout=120)
            response.raise_for_status()
            data = response.json()
            content = data['choices'][0]['message']['content']
            if content and content.strip():
                print(f"    ✅ PPInfra '{model_name}' success: {len(content)} chars")
                return content, {"role": "assistant", "content": content}
        except Exception as e:
            print(f"    ❌ PPInfra '{model_name}' error on attempt {attempt + 1}: {e}")
            if attempt < max_retries - 1:
                time.sleep(2)
    return f"[API Error: PPInfra failed after {max_retries} attempts]", None

def call_gemini(model_name: str, messages: list, options: dict = None, max_retries: int = 3) -> tuple:
    """调用 Google Gemini API"""
    headers = {
        "x-goog-api-key": GEMINI_API_KEY,
        "Content-Type": "application/json",
    }
    if options is None:
        options = {}
    
    # 修正模型名称映射
    model_mapping = {
        "gemini-1.5-flash-latest": "gemini-1.5-flash",
        "gemini-1.5-pro-latest": "gemini-1.5-pro", 
        "gemini-1.5-flash": "gemini-1.5-flash",
        "gemini-1.5-pro": "gemini-1.5-pro",
        "gemini-2.0-flash-exp": "gemini-2.0-flash-exp"
    }
    
    actual_model = model_mapping.get(model_name, model_name)
    
    # 转换消息格式为Gemini格式
    contents = []
    system_instruction = None
    
    for i, msg in enumerate(messages):
        if msg["role"] == "system":
            system_instruction = msg["content"]
        elif msg["role"] == "user":
            contents.append({
                "role": "user",
                "parts": [{"text": msg["content"]}]
            })
        elif msg["role"] == "assistant":
            contents.append({
                "role": "model", 
                "parts": [{"text": msg["content"]}]
            })
    
    # 构建请求payload
    payload = {
        "contents": contents,
        "generationConfig": {
            "temperature": options.get("temperature", 0.7),
            "maxOutputTokens": options.get("max_tokens", 4096),
            "topP": options.get("top_p", 0.95),
            "topK": options.get("top_k", 40),
        }
    }
    
    # 如果有系统指令，添加到payload中
    if system_instruction:
        payload["systemInstruction"] = {
            "parts": [{"text": system_instruction}]
        }
    
    for attempt in range(max_retries):
        try:
            url = f"{GEMINI_API_URL}/{actual_model}:generateContent"
            print(f"    🔗 Calling Gemini API: {url}")
            
            response = requests.post(url, headers=headers, json=payload, timeout=120)
            
            # 检查配额限制
            if response.status_code == 429:
                print(f"    ⚠️ Gemini API配额已用完，跳过此模型")
                return "[API Error: Gemini quota exceeded - skipping]", None
            
            if response.status_code != 200:
                print(f"    ❌ HTTP {response.status_code}: {response.text}")
                response.raise_for_status()
            
            data = response.json()
            
            if 'candidates' not in data or not data['candidates']:
                print(f"    ⚠️ No candidates in response")
                continue
                
            candidate = data['candidates'][0]
            if 'content' not in candidate or 'parts' not in candidate['content']:
                print(f"    ⚠️ Invalid response structure")
                continue
                
            content = candidate['content']['parts'][0]['text']
            
            if content and content.strip():
                print(f"    ✅ Gemini '{model_name}' success: {len(content)} chars")
                return content, {"role": "assistant", "content": content}
            else:
                print(f"    ⚠️ Empty response from Gemini on attempt {attempt + 1}")
                
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 429:
                print(f"    ⚠️ Gemini API配额限制，跳过测试")
                return "[API Error: Gemini quota exceeded]", None
            print(f"    ❌ Gemini HTTP error on attempt {attempt + 1}: {e}")
            if attempt < max_retries - 1:
                time.sleep(2)
                continue
        except Exception as e:
            print(f"    ❌ Gemini API error on attempt {attempt + 1}: {e}")
            if attempt < max_retries - 1:
                time.sleep(2)
                continue
    
    return f"[API Error: Gemini failed after {max_retries} attempts]", None

def call_dashscope(model_name: str, messages: list, options: dict = None, max_retries: int = 3) -> tuple:
    """调用 阿里云DashScope (OpenAI兼容) API"""
    headers = {
        "Authorization": f"Bearer {DASHSCOPE_API_KEY}",
        "Content-Type": "application/json",
    }
    if options is None:
        options = {}
    
    payload = {
        "model": model_name,
        "messages": messages,
        "max_tokens": options.get("max_tokens", 4096),
        "temperature": options.get("temperature", 0.7),
        "top_p": options.get("top_p", 0.9),
    }
    
    for attempt in range(max_retries):
        try:
            response = requests.post(DASHSCOPE_API_URL, headers=headers, json=payload, timeout=120)
            response.raise_for_status()
            data = response.json()
            content = data['choices'][0]['message']['content']
            if content and content.strip():
                print(f"    ✅ DashScope '{model_name}' success: {len(content)} chars")
                return content, {"role": "assistant", "content": content}
            else:
                print(f"    ⚠️ Empty response from DashScope on attempt {attempt + 1}")
        except requests.exceptions.HTTPError as e:
            print(f"    ❌ DashScope HTTP error on attempt {attempt + 1}: {e.response.status_code} {e.response.reason}")
            print(f"    Response Body: {e.response.text}")
            if attempt < max_retries - 1:
                time.sleep(2)
                continue
        except Exception as e:
            print(f"    ❌ DashScope API error on attempt {attempt + 1}: {e}")
            if attempt < max_retries - 1:
                time.sleep(2)
                continue
    
    return f"[API Error: DashScope failed after {max_retries} attempts]", None

def call_glm(model_name: str, messages: list, options: dict = None, max_retries: int = 3) -> tuple:
    """调用 智谱AI GLM (OpenAI兼容) API"""
    headers = {
        "Authorization": f"Bearer {GLM_API_KEY}",
        "Content-Type": "application/json",
    }
    if options is None:
        options = {}
    
    payload = {
        "model": model_name,
        "messages": messages,
        "max_tokens": options.get("max_tokens", 4096),
        "temperature": options.get("temperature", 0.7),
        "top_p": options.get("top_p", 0.9),
        "stream": False
    }
    
    for attempt in range(max_retries):
        try:
            response = requests.post(GLM_API_URL, headers=headers, json=payload, timeout=120)
            response.raise_for_status()
            data = response.json()
            content = data['choices'][0]['message']['content']
            if content and content.strip():
                print(f"    ✅ GLM '{model_name}' success: {len(content)} chars")
                return content, {"role": "assistant", "content": content}
            else:
                print(f"    ⚠️ Empty response from GLM on attempt {attempt + 1}")
        except requests.exceptions.HTTPError as e:
            print(f"    ❌ GLM HTTP error on attempt {attempt + 1}: {e.response.status_code} {e.response.reason}")
            print(f"    Response Body: {e.response.text}")
            if attempt < max_retries - 1:
                time.sleep(2)
                continue
        except Exception as e:
            print(f"    ❌ GLM API error on attempt {attempt + 1}: {e}")
            if attempt < max_retries - 1:
                time.sleep(2)
                continue
    
    return f"[API Error: GLM failed after {max_retries} attempts]", None

# --- Test Execution Core ---
def run_single_test(pillar_name: str, prompt: str, model: str, options: dict, messages: list = None, test_script_name: str = None):
    """
    执行单次测试并打印结果的核心函数。
    Args:
        pillar_name: 当前测试的Pillar名称。
        prompt: 当前轮次的输入Prompt。
        model: 要测试的模型名称。
        options: Ollama API的选项。
        messages: 用于多轮对话的历史消息列表。
        test_script_name: 当前正在执行的测试脚本名（用于日志记录）。
    Returns:
        Tuple[str, dict]: 模型的响应内容和完整的响应消息对象。
    """
    print("\n" + "="*80)
    print(f"  Pillar: {pillar_name}")
    if test_script_name:
        print(f"  Script: {test_script_name}")
    print("="*80)
    
    current_messages = messages.copy() if messages else []
    
    if prompt:
        print(f"\n[Prompt]")
        print(prompt)
        current_messages.append({'role': 'user', 'content': prompt})
    else: # 用于多轮对话的场景，第一轮prompt在外部处理
        print(f"\n[Multi-turn Context Provided]")

    print(f"\n[Model: {model}] [Options: {options}]")
    print("--- MODEL RESPONSE (RAW) ---")
    
    try:
        start_time = time.time()

        # --- 新增自动多云API轮询逻辑 ---
        if model.startswith("auto/"):
            actual_model_name = model.split('/', 1)[1]
            print(f"    Auto-trying all cloud APIs for model: {actual_model_name}")
            content, response_message = call_multi_cloud(actual_model_name, current_messages, options)
            if content == "[API Error: All cloud APIs failed]":
                print("所有云API均失败。\n")
                return content, response_message
        elif model.startswith("openrouter/"):
            actual_model_name = model.split('/', 1)[1]
            print(f"    Routing to OpenRouter with model: {actual_model_name}")
            content, response_message = call_openrouter(actual_model_name, current_messages, options)
        elif model.startswith("together/"):
            actual_model_name = model.split('/', 1)[1]
            print(f"    Routing to Together.ai with model: {actual_model_name}")
            content, response_message = call_togetherai(actual_model_name, current_messages, options)
        elif model == "deepseek-v3-qiniu":
            print("    Routing to Qiniu DeepSeek API")
            content, response_message = call_qiniu_deepseek(current_messages, options)
        elif model.startswith("ppinfra/"):
            actual_model_name = model.split('/', 1)[1]
            print(f"    Routing to PPInfra with model: {actual_model_name}")
            content, response_message = call_ppinfra(actual_model_name, current_messages, options)
        elif model.startswith("gemini/"):
            actual_model_name = model.split('/', 1)[1]
            print(f"    Routing to Gemini with model: {actual_model_name}")
            content, response_message = call_gemini(actual_model_name, current_messages, options)
        elif model.startswith("dashscope/"):
            actual_model_name = model.split('/', 1)[1]
            print(f"    Routing to DashScope with model: {actual_model_name}")
            content, response_message = call_dashscope(actual_model_name, current_messages, options)
        elif model.startswith("glm/"):
            actual_model_name = model.split('/', 1)[1]
            print(f"    Routing to GLM with model: {actual_model_name}")
            content, response_message = call_glm(actual_model_name, current_messages, options)
        elif model.startswith("baidu/"):
            actual_model_name = model.split('/', 1)[1]
            print(f"    Routing to 百度云 with model: {actual_model_name}")
            content, response_message = call_baidu_llm(actual_model_name, current_messages, options)
        else:
            print("    Routing to local Ollama")
            response = client.chat(
                model=model,
                messages=current_messages,
                options=options
            )
            content = response['message']['content']
            response_message = response['message']
        # --- END ---

        end_time = time.time()

        print(content)

        print("--- END OF RESPONSE ---")
        duration = end_time - start_time
        print(f"Response generated in: {duration:.2f} seconds.")

        return content, response_message # 返回内容和完整的消息对象以供多轮测试使用

    except Exception as e:
        print(f"!!! ERROR during API call: {e}")
        return f"ERROR: {e}", None

def print_assessment_criteria(criteria: str):
    """
    格式化并打印评估标准。
    """
    print("\n[Assessment Criteria]")
    print(criteria.strip())
    print("="*80)

# --- Environment Management ---
def setup_test_environment(subdir_name: str = None) -> str:
    """为层级三/工作流测试创建临时工作目录"""
    base_dir = TEST_WORKSPACE_DIR
    if subdir_name:
        base_dir = os.path.join(base_dir, subdir_name)
        
    if os.path.exists(base_dir):
        shutil.rmtree(base_dir)
    os.makedirs(base_dir)
    print(f"\n*** [SETUP] Created temporary workspace for tests: {base_dir} ***")
    return base_dir

def cleanup_test_environment(work_dir: str):
    """清理层级三/工作流测试的临时工作目录"""
    if os.path.exists(work_dir):
        shutil.rmtree(work_dir)
        print(f"\n*** [CLEANUP] Removed temporary workspace: {work_dir} ***")

def ensure_log_dir():
    """确保日志目录存在"""
    if not os.path.exists(LOG_DIR):
        os.makedirs(LOG_DIR)
        print(f"[INFO] Created log directory: {LOG_DIR}")

def ensure_report_dir():
    """确保报告目录存在"""
    if not os.path.exists(REPORT_DIR):
        os.makedirs(REPORT_DIR)
        print(f"[INFO] Created report directory: {REPORT_DIR}")

# --- File Operations ---
def save_file(filepath, content):
    """保存文件到指定路径"""
    try:
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, 'w', encoding='utf-8', newline='\n') as f:
            f.write(content)
        print(f"[INFO] Saved file: {filepath}")
    except Exception as e:
        print(f"[ERROR] Failed to save file {filepath}: {e}")
        
def read_file(filepath):
    """读取文件内容"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        print(f"[ERROR] File not found: {filepath}")
        return None
    except Exception as e:
        print(f"[ERROR] Failed to read file {filepath}: {e}")
        return None

# --- Subprocess Execution ---
def execute_bash_script(script_path: str, cwd: str = None) -> str:
    """
    执行bash脚本并返回其标准输出。
    Args:
        script_path: bash脚本的完整路径。
        cwd: 命令执行的工作目录。
    Returns:
        str: 脚本的标准输出。
    """
    print(f"\n--- EXECUTING BASH SCRIPT: {script_path} ---")
    try:
        # Make the script executable
        subprocess.run(['chmod', '+x', script_path], check=True, cwd=cwd)
        result = subprocess.run(
            ['/bin/bash', script_path],
            capture_output=True,
            text=True,
            check=True,
            encoding='utf-8',
            cwd=cwd
        )
        output = result.stdout
        if result.stderr:
            print(f"[STDERR] from {script_path}:\n{result.stderr}")
        print(f"--- END OF BASH SCRIPT OUTPUT ---")
        return output

    except FileNotFoundError:
        return f"ERROR: Bash script not found at {script_path}"
    except subprocess.CalledProcessError as e:
        error_msg = f"ERROR: Bash script execution failed for {script_path}. Return code: {e.returncode}\n"
        error_msg += f"STDOUT:\n{e.stdout}\n"
        error_msg += f"STDERR:\n{e.stderr}\n"
        print(error_msg)
        return f"ERROR: Script execution failed."
    except Exception as e:
        return f"ERROR: An unexpected error occurred during script execution: {e}"

def check_ollama_dependency():
    """检查并安装ollama Python包"""
    try:
        __import__('ollama')
        print("[SETUP] 'ollama' python package is already installed.")
    except ImportError:
        print("[SETUP] 'ollama' python package not found. Attempting to install...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "ollama"])
            print("[SETUP] 'ollama' installed successfully.")
        except subprocess.CalledProcessError:
            print("[ERROR] Failed to install 'ollama'. Please install it manually using 'pip install ollama'.")
            print("[INFO] On Windows, you may need to run this script from a terminal with Administrator privileges.")
            sys.exit(1)
    # Check if ollama service is running after dependency check
    try:
        client.list()
        print(f"[INFO] Ollama service is reachable at {OLLAMA_HOST}")
    except Exception as e:
        print(f"[WARN] Could not reach Ollama service at {OLLAMA_HOST}. Ensure Ollama is running.")
        # Allow continuation but warn; specific tests might fail.
        pass

# --- Helper for modifying test scripts ---
def modify_test_script(script_content: str, model_name: str) -> str:
    """
    修改测试脚本内容，将 MODEL_TO_TEST 替换为指定的模型名称。
    """
    lines = script_content.splitlines()
    modified_lines = []
    for line in lines:
        if line.strip().startswith('MODEL_TO_TEST'):
            modified_lines.append(f"MODEL_TO_TEST = '{model_name}'")
        else:
            modified_lines.append(line)
    return "\n".join(modified_lines)

# --- Enhanced Test Execution with Retry Logic ---
def run_single_test_with_retry(pillar_name: str, prompt: str, model: str, options: dict,
                              messages: list = None, test_script_name: str = None,
                              max_retries: int = 3, retry_delay: int = 2):
    """
    带重试机制的测试执行函数，处理零响应和API错误
    """
    for attempt in range(max_retries):
        try:
            content, response_message = run_single_test(
                pillar_name, prompt, model, options, messages, test_script_name
            )

            # 检查是否为零响应或无效响应
            if not content or content.strip() == "" or "ERROR:" in content:
                if attempt < max_retries - 1:
                    print(f"[RETRY] Attempt {attempt + 1} failed, retrying in {retry_delay} seconds...")
                    time.sleep(retry_delay)
                    continue
                else:
                    print(f"[FAIL] All {max_retries} attempts failed for {pillar_name}")
                    return content, response_message
            else:
                if attempt > 0:
                    print(f"[SUCCESS] Test succeeded on attempt {attempt + 1}")
                return content, response_message

        except Exception as e:
            if attempt < max_retries - 1:
                print(f"[RETRY] Attempt {attempt + 1} failed with error: {e}, retrying...")
                time.sleep(retry_delay)
                continue
            else:
                print(f"[FAIL] All {max_retries} attempts failed with error: {e}")
                return f"ERROR: {e}", None

    return "ERROR: Max retries exceeded", None

# --- Adaptive Prompts Integration ---
def get_adaptive_prompt(model_name: str, base_prompt: str, prompt_type: str = "default"):
    """
    根据模型类型和提示类型获取自适应提示词
    """
    try:
        from adaptive_prompts import ADAPTIVE_SYSTEM_PROMPTS

        # 检查是否为atlas模型（需要特殊处理）
        if "atlas" in model_name.lower():
            if prompt_type in ADAPTIVE_SYSTEM_PROMPTS.get("atlas", {}):
                system_prompt = ADAPTIVE_SYSTEM_PROMPTS["atlas"][prompt_type]
                # 对atlas模型进行长度限制
                if len(base_prompt) > 360:  # 基于用户偏好的放宽限制
                    base_prompt = base_prompt[:360] + "..."
                return system_prompt, base_prompt

        # 其他模型使用通用自适应提示
        if prompt_type in ADAPTIVE_SYSTEM_PROMPTS.get("general", {}):
            system_prompt = ADAPTIVE_SYSTEM_PROMPTS["general"][prompt_type]
            return system_prompt, base_prompt

    except ImportError:
        print("[WARN] adaptive_prompts module not found, using default prompts")
    except Exception as e:
        print(f"[WARN] Error loading adaptive prompts: {e}")

    # 回退到默认行为
    return None, base_prompt
