#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试带有adaptive提示词的TestLLM功能
快速验证adaptive提示词是否正确集成
"""

import requests
import time
import os
from typing import Dict, Any

# 导入adaptive提示词模块
try:
    from adaptive_prompts import ADAPTIVE_SYSTEM_PROMPTS
    ADAPTIVE_AVAILABLE = True
    print("✅ Adaptive prompts module loaded successfully")
except ImportError:
    ADAPTIVE_AVAILABLE = False
    print("⚠️ Adaptive prompts module not found")

# 配置
OLLAMA_API_URL = 'http://localhost:11434/api/chat'
TEST_MODEL = 'atlas/intersync-gemma-7b-instruct-function-calling:latest'
API_TIMEOUT = 60

def call_ollama_with_adaptive(model: str, prompt: str, test_context: str = "summary_analysis") -> str:
    """
    使用adaptive提示词调用Ollama API
    """
    print(f"🔍 Testing adaptive prompts for {model}")
    print(f"📝 Context: {test_context}")
    
    # 构建消息列表，支持adaptive提示词
    if ADAPTIVE_AVAILABLE:
        try:
            test_script_name = f"test_pillar_{test_context}.py"
            
            # 检查是否有针对该模型的adaptive提示词
            if model in ADAPTIVE_SYSTEM_PROMPTS and test_script_name in ADAPTIVE_SYSTEM_PROMPTS[model]:
                system_prompt = ADAPTIVE_SYSTEM_PROMPTS[model][test_script_name]
                messages = [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt}
                ]
                print(f"✅ Using adaptive system prompt:")
                print(f"   {system_prompt[:100]}...")
            else:
                messages = [{"role": "user", "content": prompt}]
                print(f"⚠️ No adaptive prompt found for {model} + {test_script_name}")
        except Exception as e:
            print(f"❌ Adaptive prompts failed: {e}")
            messages = [{"role": "user", "content": prompt}]
    else:
        messages = [{"role": "user", "content": prompt}]
    
    payload = {
        "model": model,
        "messages": messages,
        "stream": False,
        "options": {"temperature": 0.1}
    }
    
    try:
        print(f"🚀 Calling {model}...")
        response = requests.post(OLLAMA_API_URL, json=payload, timeout=API_TIMEOUT)
        response.raise_for_status()
        data = response.json()
        content = data.get('message', {}).get('content', '')
        
        if content:
            print(f"✅ Response received: {len(content)} characters")
            return content
        else:
            print(f"⚠️ Empty response")
            return ""
            
    except Exception as e:
        print(f"❌ API call failed: {e}")
        return f"[API Error: {e}]"

def test_adaptive_prompts():
    """
    测试adaptive提示词功能
    """
    print("🧪 Testing Adaptive Prompts for TestLLM")
    print("="*60)
    
    # 测试案例
    test_cases = [
        {
            "context": "summary_analysis",
            "prompt": """
Please analyze the following dialogue segment and extract key information:

Detective: "We found fingerprints on the weapon."
Suspect A: "I never touched that knife!"
Witness: "I saw someone running from the scene around midnight."
Detective: "The victim was found at 11:45 PM."

Please summarize the key facts and evidence.
"""
        },
        {
            "context": "final_reasoning", 
            "prompt": """
Based on the following evidence, determine who is the most likely suspect:

Evidence Summary:
- Fingerprints found on weapon belong to Suspect B
- Suspect A has no alibi for the time of crime
- Suspect B was seen arguing with victim earlier
- Witness saw someone matching Suspect B's description fleeing
- Victim was killed between 11:30-11:45 PM

Who is the perpetrator and why?
"""
        }
    ]
    
    results = []
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n--- Test Case {i}: {test_case['context']} ---")
        
        # 测试带adaptive提示词的版本
        print(f"\n🔬 Testing WITH adaptive prompts:")
        adaptive_response = call_ollama_with_adaptive(
            TEST_MODEL, 
            test_case['prompt'], 
            test_case['context']
        )
        
        # 测试不带adaptive提示词的版本
        print(f"\n🔬 Testing WITHOUT adaptive prompts:")
        standard_response = call_ollama_standard(TEST_MODEL, test_case['prompt'])
        
        # 记录结果
        result = {
            "test_case": i,
            "context": test_case['context'],
            "adaptive_response": adaptive_response,
            "standard_response": standard_response,
            "adaptive_length": len(adaptive_response) if adaptive_response else 0,
            "standard_length": len(standard_response) if standard_response else 0
        }
        results.append(result)
        
        print(f"\n📊 Comparison:")
        print(f"   Adaptive response: {result['adaptive_length']} chars")
        print(f"   Standard response: {result['standard_length']} chars")
        
        time.sleep(2)  # 避免API调用过快
    
    # 生成报告
    print(f"\n" + "="*60)
    print(f"📋 Adaptive Prompts Test Report")
    print(f"="*60)
    
    for result in results:
        print(f"\nTest Case {result['test_case']} ({result['context']}):")
        print(f"  Adaptive: {result['adaptive_length']} chars")
        print(f"  Standard: {result['standard_length']} chars")
        
        if result['adaptive_length'] > 0 and result['standard_length'] > 0:
            ratio = result['adaptive_length'] / result['standard_length']
            print(f"  Ratio: {ratio:.2f}x")
            if ratio > 1.2:
                print(f"  ✅ Adaptive prompts produced more detailed response")
            elif ratio < 0.8:
                print(f"  ⚠️ Adaptive prompts produced shorter response")
            else:
                print(f"  📊 Similar response lengths")
        elif result['adaptive_length'] > 0:
            print(f"  ✅ Only adaptive prompts produced response")
        elif result['standard_length'] > 0:
            print(f"  ❌ Only standard prompts produced response")
        else:
            print(f"  ❌ Both failed to produce response")
    
    # 保存详细结果
    with open('adaptive_prompts_test_results.txt', 'w', encoding='utf-8') as f:
        f.write("Adaptive Prompts Test Results\n")
        f.write("="*50 + "\n\n")
        
        for result in results:
            f.write(f"Test Case {result['test_case']}: {result['context']}\n")
            f.write("-" * 40 + "\n")
            f.write(f"ADAPTIVE RESPONSE ({result['adaptive_length']} chars):\n")
            f.write(result['adaptive_response'] + "\n\n")
            f.write(f"STANDARD RESPONSE ({result['standard_length']} chars):\n")
            f.write(result['standard_response'] + "\n\n")
            f.write("="*50 + "\n\n")
    
    print(f"\n💾 Detailed results saved to: adaptive_prompts_test_results.txt")
    print(f"✅ Adaptive prompts test completed!")

def call_ollama_standard(model: str, prompt: str) -> str:
    """
    标准方式调用Ollama API（不使用adaptive提示词）
    """
    payload = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "stream": False,
        "options": {"temperature": 0.1}
    }
    
    try:
        response = requests.post(OLLAMA_API_URL, json=payload, timeout=API_TIMEOUT)
        response.raise_for_status()
        data = response.json()
        content = data.get('message', {}).get('content', '')
        
        if content:
            print(f"✅ Standard response received: {len(content)} characters")
            return content
        else:
            print(f"⚠️ Empty standard response")
            return ""
            
    except Exception as e:
        print(f"❌ Standard API call failed: {e}")
        return f"[API Error: {e}]"

if __name__ == "__main__":
    # 检查模型是否可用
    print(f"🔍 Checking if model {TEST_MODEL} is available...")
    
    try:
        test_response = call_ollama_standard(TEST_MODEL, "Hello")
        if "[API Error:" in test_response:
            print(f"❌ Model {TEST_MODEL} is not available")
            print(f"Please make sure the model is installed and Ollama is running")
        else:
            print(f"✅ Model {TEST_MODEL} is available")
            test_adaptive_prompts()
    except Exception as e:
        print(f"❌ Failed to connect to Ollama: {e}")
        print(f"Please make sure Ollama is running on {OLLAMA_API_URL}")
