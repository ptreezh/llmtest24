#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
检查SiliconFlow可用模型
"""

import os
import requests
from dotenv import load_dotenv

load_dotenv()

def get_siliconflow_models():
    """获取SiliconFlow可用模型列表"""
    api_key = os.getenv("SILICONFLOW_API_KEY")
    if not api_key:
        print("❌ 未设置SILICONFLOW_API_KEY")
        return
    
    try:
        url = "https://api.siliconflow.cn/v1/models"
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        
        print("🔍 获取SiliconFlow模型列表...")
        response = requests.get(url, headers=headers, timeout=10)
        
        print(f"📡 响应状态码: {response.status_code}")
        
        if response.status_code == 200:
            models = response.json()
            print("✅ 可用模型:")
            if "data" in models:
                for model in models["data"]:
                    print(f"  - {model.get('id', 'Unknown')}")
            else:
                print(f"📝 响应内容: {response.text}")
        else:
            print(f"❌ 获取失败: {response.text}")
            
    except Exception as e:
        print(f"❌ 错误: {e}")

if __name__ == "__main__":
    get_siliconflow_models()