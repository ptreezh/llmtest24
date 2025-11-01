#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
调试环境变量加载问题
"""

import os
from dotenv import load_dotenv

# 加载.env文件
load_dotenv()

# 检查所有云服务的API密钥
api_keys = [
    "QINIU_API_KEY",
    "SILICONFLOW_API_KEY", 
    "TOGETHER_API_KEY",
    "OPENROUTER_API_KEY",
    "PPINFRA_API_KEY",
    "GEMINI_API_KEY",
    "DASHSCOPE_API_KEY",
    "GLM_API_KEY",
    "BAIDU_API_KEY",
    "BAIDU_SECRET_KEY"
]

print("🔍 检查环境变量:")
for key in api_keys:
    value = os.getenv(key)
    if value:
        print(f"✅ {key}: {'*' * 10}{value[-4:] if len(value) > 4 else '****'}")
    else:
        print(f"❌ {key}: 未设置")

print(f"\n📁 当前工作目录: {os.getcwd()}")
print(f"📄 .env文件存在: {os.path.exists('.env')}")

if os.path.exists('.env'):
    with open('.env', 'r', encoding='utf-8') as f:
        lines = f.readlines()
    print(f"📝 .env文件行数: {len(lines)}")
    print("📋 .env文件内容预览:")
    for i, line in enumerate(lines[:5]):
        if '=' in line and not line.startswith('#'):
            key = line.split('=')[0]
            print(f"  {i+1}: {key}=***")