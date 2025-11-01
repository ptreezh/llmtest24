#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
测试云服务连通性
"""

import os
import requests
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

def test_qiniu_connectivity_alternative():
    """测试七牛云连通性 - 尝试不同的API端点"""
    api_key = os.getenv("QINIU_API_KEY")
    if not api_key:
        print("❌ 七牛云: 未设置API密钥")
        return False
    
    # 尝试不同的端点和模型
    endpoints_to_try = [
        {
            "url": "https://api.qnaigc.com/v1/chat/completions",
            "model": "deepseek-v3"
        },
        {
            "url": "https://api.qnaigc.com/v1/chat/completions", 
            "model": "deepseek-chat"
        }
    ]
    
    for endpoint in endpoints_to_try:
        try:
            headers = {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            }
            data = {
                "model": endpoint["model"],
                "messages": [{"role": "user", "content": "你好"}],
                "max_tokens": 100
            }
            
            print(f"🔍 测试七牛云连通性 (模型: {endpoint['model']})...")
            response = requests.post(endpoint["url"], headers=headers, json=data, timeout=10)
            
            print(f"📡 响应状态码: {response.status_code}")
            print(f"📝 响应内容: {response.text[:200]}...")
            
            if response.status_code == 200:
                print(f"✅ 七牛云: 连接成功 (模型: {endpoint['model']})")
                return True
            elif response.status_code == 401:
                print("❌ 七牛云: API密钥无效")
                continue
            elif response.status_code == 403:
                print("❌ 七牛云: 访问被拒绝，可能是API密钥权限问题")
                continue
            elif response.status_code == 429:
                print("⚠️ 七牛云: API配额限制")
                return True
            else:
                print(f"❌ 七牛云: HTTP {response.status_code}")
                continue
                
        except Exception as e:
            print(f"❌ 七牛云: 错误 {e}")
            continue
    
    print("❌ 七牛云: 所有端点都测试失败")
    return False

if __name__ == "__main__":
    print("🚀 开始测试云服务连通性...")
    print("=" * 50)
    
    # 测试几个主要服务
    test_qiniu_connectivity_alternative()
    
    print("=" * 50)
    print("🏁 测试完成")
