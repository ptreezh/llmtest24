#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import ollama
import sys

def check_models():
    try:
        client = ollama.Client()
        models = client.list()
        print("Available models:")
        for model in models['models']:
            print(f"- {model['name']}")
        
        # 检查目标模型
        target_models = ['deepseek-v3-qiniu', 'qwen3:4b', 'gemma3:latest']
        available_names = [m['name'] for m in models['models']]
        
        print("\nTarget models status:")
        for target in target_models:
            if target in available_names:
                print(f"✅ {target} - Available")
            else:
                print(f"❌ {target} - Not found")
                
    except Exception as e:
        print(f"Error checking models: {e}")
        return False
    
    return True

if __name__ == "__main__":
    check_models()
