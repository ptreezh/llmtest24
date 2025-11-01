#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
专门测试百度文心连接
"""

import os
import requests
import json
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

def test_baidu_connectivity(verbose=True):
    """详细测试百度文心连接"""
    print("🔍 测试百度文心连接...")
    
    # 检查环境变量
    api_key = os.getenv("BAIDU_API_KEY")
    secret_key = os.getenv("BAIDU_SECRET_KEY")
    
    if not api_key:
        print("❌ 未设置BAIDU_API_KEY环境变量")
        return False
    
    if not secret_key:
        print("❌ 未设置BAIDU_SECRET_KEY环境变量")
        return False
    
    print(f"✅ 环境变量检查通过")
    print(f"  - BAIDU_API_KEY: {api_key[:5]}...{api_key[-5:] if len(api_key) > 10 else ''}")
    print(f"  - BAIDU_SECRET_KEY: {secret_key[:5]}...{secret_key[-5:] if len(secret_key) > 10 else ''}")
    
    # 获取access_token
    token_url = "https://aip.baidubce.com/oauth/2.0/token"
    params = {
        "grant_type": "client_credentials",
        "client_id": api_key,
        "client_secret": secret_key
    }
    
    try:
        print(f"🔄 正在获取access_token...")
        response = requests.post(token_url, params=params, timeout=10)
        
        print(f"📡 响应状态码: {response.status_code}")
        
        if response.status_code != 200:
            print(f"❌ 获取access_token失败: HTTP {response.status_code}")
            print(f"  响应内容: {response.text}")
            return False
        
        token_data = response.json()
        if verbose:
            print(f"📝 响应内容: {json.dumps(token_data, ensure_ascii=False, indent=2)}")
        
        if "access_token" not in token_data:
            print(f"❌ access_token响应异常，未找到access_token字段")
            return False
        
        access_token = token_data["access_token"]
        print(f"✅ 成功获取access_token: {access_token[:10]}...")
        
        # 测试模型API
        model = "ernie-4.0-8k"  # 使用默认模型
        url = f"https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/completions_pro?access_token={access_token}"
        
        headers = {
            "Content-Type": "application/json"
        }
        
        payload = {
            "messages": [{"role": "user", "content": "你好"}],
            "temperature": 0.7,
            "top_p": 0.9,
        }
        
        print(f"🔄 正在测试模型API (模型: {model})...")
        model_response = requests.post(url, headers=headers, json=payload, timeout=30)
        
        print(f"📡 响应状态码: {model_response.status_code}")
        
        if model_response.status_code != 200:
            print(f"❌ 模型API调用失败: HTTP {model_response.status_code}")
            print(f"  响应内容: {model_response.text}")
            return False
        
        model_data = model_response.json()
        if verbose:
            print(f"📝 响应内容: {json.dumps(model_data, ensure_ascii=False, indent=2)[:500]}...")
        
        print(f"✅ 百度文心连接测试成功!")
        return True
        
    except Exception as e:
        print(f"❌ 连接错误: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_baidu_connectivity()