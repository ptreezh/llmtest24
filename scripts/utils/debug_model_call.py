#!/usr/bin/env python3
"""调试模型调用"""

import ollama
import time
from config import MODEL_TO_TEST, OLLAMA_HOST

def test_model_call():
    print(f"🔍 测试模型调用: {MODEL_TO_TEST}")
    print(f"📡 Ollama主机: {OLLAMA_HOST}")
    
    try:
        print("⏱️ 开始调用模型...")
        start_time = time.time()
        
        response = ollama.chat(
            model=MODEL_TO_TEST,
            messages=[{
                'role': 'user', 
                'content': '你好，请简单介绍一下你自己，说明你的角色定位。'
            }]
        )
        
        end_time = time.time()
        duration = end_time - start_time
        
        print(f"✅ 调用成功！耗时: {duration:.2f}秒")
        print(f"📝 响应内容: {response['message']['content'][:200]}...")
        
        return True
        
    except Exception as e:
        print(f"❌ 调用失败: {e}")
        return False

if __name__ == "__main__":
    test_model_call()