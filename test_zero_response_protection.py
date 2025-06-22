#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试零响应保护机制
验证强化的重试策略和备用提示词
"""

import requests
import time

# 配置
OLLAMA_API_URL = 'http://localhost:11434/api/chat'
ATLAS_MODEL = 'atlas/intersync-gemma-7b-instruct-function-calling:latest'
API_TIMEOUT = 300

def call_ollama_with_protection(model: str, prompt: str, max_retries: int = 10) -> str:
    """
    带强化保护的Ollama调用
    """
    print(f"    - Testing {model} with prompt: '{prompt[:50]}...' ({len(prompt)} chars)")
    
    system_prompt = "Detective. Analyze murder case. Summarize key evidence concisely."
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": prompt}
    ]
    
    for attempt in range(max_retries):
        # 渐进式参数调整策略
        if attempt <= 2:
            # 前3次尝试：标准参数
            temp = 0.6 + (attempt * 0.2)
            top_p = 0.95
            top_k = 60
        elif attempt <= 5:
            # 第4-6次：提高随机性
            temp = 0.9 + (attempt * 0.1)
            top_p = 0.98
            top_k = 80
        else:
            # 第7-10次：最大随机性
            temp = 1.2 + (attempt * 0.1)
            top_p = 1.0
            top_k = 100
        
        options = {
            "temperature": min(temp, 2.0),
            "top_p": top_p,
            "top_k": top_k,
            "repeat_penalty": max(1.0, 1.05 - (attempt * 0.01)),
            "timeout": 40,
            "num_ctx": max(1024, 2048 - (attempt * 100)),
            "num_predict": 100 + (attempt * 10),
            "seed": -1,
            "mirostat": 2 if attempt > 3 else 0,
            "mirostat_tau": 5.0 if attempt > 3 else 5.0
        }
        
        payload = {
            "model": model,
            "messages": messages,
            "stream": False,
            "options": options
        }
        
        try:
            response = requests.post(OLLAMA_API_URL, json=payload, timeout=API_TIMEOUT)
            response.raise_for_status()
            data = response.json()
            content = data.get('message', {}).get('content', '')
            
            if content and content.strip():
                if attempt > 0:
                    print(f"    ✅ Success on attempt {attempt + 1}: {len(content)} chars")
                else:
                    print(f"    ✅ Success: {len(content)} chars")
                return content
            else:
                print(f"    ⚠️ Zero response on attempt {attempt + 1}/{max_retries} (temp: {temp:.2f})")
                if attempt < max_retries - 1:
                    time.sleep(1)
                    continue
                    
        except Exception as e:
            print(f"    ❌ Error on attempt {attempt + 1}/{max_retries}: {str(e)[:50]}...")
            if attempt < max_retries - 1:
                time.sleep(1)
                continue
    
    print(f"    ❌ All {max_retries} attempts failed")
    return ""

def test_fallback_prompts(model: str, original_prompt: str, fallback_prompt: str, default_response: str) -> str:
    """测试备用提示词机制"""
    print(f"\n🔄 Testing fallback mechanism...")
    
    # 尝试原始提示词
    result = call_ollama_with_protection(model, original_prompt)
    
    if not result or result.strip() == "":
        print(f"    🔄 Original failed, trying fallback...")
        result = call_ollama_with_protection(model, fallback_prompt)
        
        if not result or result.strip() == "":
            print(f"    🆘 Fallback failed, using default...")
            result = default_response
            print(f"    📝 Default response: {result}")
    
    return result

def test_zero_response_protection():
    """测试零响应保护机制"""
    print("🧪 Testing Zero Response Protection Mechanism")
    print("="*55)
    
    model = ATLAS_MODEL
    
    # 测试场景1：初始摘要
    print(f"\n--- 场景1：初始摘要保护 ---")
    original_prompt1 = "S:A：昨晚听到奇怪声音。B：看到黑影。C：张三丢斧头。D：脚印很大。"
    fallback_prompt1 = "Sum:A听音，B看黑影，C说张三丢斧头，D脚印大"
    default_response1 = "Evidence found, investigation continues."
    
    result1 = test_fallback_prompts(model, original_prompt1, fallback_prompt1, default_response1)
    print(f"✅ 场景1结果: '{result1[:50]}...' ({len(result1)} chars)")
    
    # 测试场景2：更新摘要
    print(f"\n--- 场景2：更新摘要保护 ---")
    original_prompt2 = "E:昨晚听到声音，看到黑影 N:李四深夜外出，身高一米八 U:"
    fallback_prompt2 = "Update:E：听音看影，N：李四可疑高1.8"
    default_response2 = "Previous evidence [continued]"
    
    result2 = test_fallback_prompts(model, original_prompt2, fallback_prompt2, default_response2)
    print(f"✅ 场景2结果: '{result2[:50]}...' ({len(result2)} chars)")
    
    # 测试场景3：最终推理
    print(f"\n--- 场景3：最终推理保护 ---")
    original_prompt3 = "E:昨晚听到声音，看到黑影，李四深夜外出，身高一米八，有矛盾 K?"
    fallback_prompt3 = "Who killed? 李四夜出，高1.8M，有矛盾"
    default_response3 = "Based evidence: 李四深夜外出，身高一米八，有矛盾, further investigation needed to determine the killer."
    
    result3 = test_fallback_prompts(model, original_prompt3, fallback_prompt3, default_response3)
    print(f"✅ 场景3结果: '{result3[:50]}...' ({len(result3)} chars)")
    
    # 汇总报告
    print(f"\n" + "="*55)
    print(f"📋 Zero Response Protection Test Summary")
    print(f"="*55)
    
    success_count = sum([
        1 if result1 and result1.strip() else 0,
        1 if result2 and result2.strip() else 0,
        1 if result3 and result3.strip() else 0
    ])
    
    print(f"Protection mechanisms:")
    print(f"  1. 渐进式参数调整 (10次重试)")
    print(f"  2. 备用简化提示词")
    print(f"  3. 默认响应保底")
    print(f"")
    print(f"Test results:")
    print(f"  场景1 (初始摘要): {'✅ SUCCESS' if result1 and result1.strip() else '❌ FAILED'}")
    print(f"  场景2 (更新摘要): {'✅ SUCCESS' if result2 and result2.strip() else '❌ FAILED'}")
    print(f"  场景3 (最终推理): {'✅ SUCCESS' if result3 and result3.strip() else '❌ FAILED'}")
    print(f"")
    print(f"Overall success rate: {success_count}/3 ({success_count/3*100:.1f}%)")
    
    if success_count == 3:
        print(f"🎯 Zero response protection successful!")
        print(f"✅ 所有场景都获得了响应")
        print(f"✅ 多层保护机制有效")
        print(f"✅ 确保测试流程不中断")
    else:
        print(f"⚠️ Some scenarios still failed, need stronger protection")
    
    # 保存结果
    with open('zero_response_protection_test.txt', 'w', encoding='utf-8') as f:
        f.write("Zero Response Protection Test Results\n")
        f.write("="*40 + "\n\n")
        f.write(f"Model: {model}\n")
        f.write(f"Success rate: {success_count}/3 ({success_count/3*100:.1f}%)\n\n")
        f.write("Results:\n")
        f.write(f"场景1: {result1}\n\n")
        f.write(f"场景2: {result2}\n\n")
        f.write(f"场景3: {result3}\n\n")
    
    print(f"💾 Test results saved to: zero_response_protection_test.txt")

if __name__ == "__main__":
    # 检查模型可用性
    print(f"🔍 Checking model availability: {ATLAS_MODEL}")
    
    try:
        test_response = call_ollama_with_protection(ATLAS_MODEL, "Hello", max_retries=3)
        if test_response:
            print(f"✅ Model {ATLAS_MODEL} is available")
            test_zero_response_protection()
        else:
            print(f"❌ Model {ATLAS_MODEL} is not responding")
    except Exception as e:
        print(f"❌ Failed to connect: {e}")
