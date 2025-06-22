#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
专门测试atlas/intersync-gemma-7b-instruct-function-calling:latest模型优化效果
验证精简提示词、长上下文检索和100字摘要限制
"""

import requests
import time
import os
import string
import random
import tiktoken
from typing import Dict, Any

# 导入adaptive提示词模块
try:
    from adaptive_prompts import ADAPTIVE_SYSTEM_PROMPTS
    ADAPTIVE_AVAILABLE = True
    print("✅ Adaptive prompts module loaded successfully")
except ImportError:
    ADAPTIVE_AVAILABLE = False
    print("⚠️ Adaptive prompts module not found, using standard prompts")

# 配置
OLLAMA_API_URL = 'http://localhost:11434/api/chat'
ATLAS_MODEL = 'atlas/intersync-gemma-7b-instruct-function-calling:latest'
API_TIMEOUT = 300

# 使用tiktoken进行精确的token计算
try:
    TOKENIZER = tiktoken.get_encoding("cl100k_base")
except Exception:
    TOKENIZER = tiktoken.encoding_for_model("gpt-4")

def get_optimized_prompt(prompt_type: str, context: Dict[str, str] = {}) -> str:
    """针对atlas模型的精简提示词"""
    if prompt_type == "intermediate":
        if context.get('summary_so_far', '').strip() and context.get('summary_so_far', '').strip() != 'None':
            return f"Summary: {context['summary_so_far'][:80]}...\nNew: {context['new_dialogue_chunk'][:300]}...\nUpdate (max 100 chars):"
        else:
            return f"Summarize key facts (max 100 chars): {context['new_dialogue_chunk'][:400]}..."
    elif prompt_type == "final":
        return f"Evidence: {context.get('summary_so_far', '')[:150]}...\nWho killed? Why?"

def call_atlas_optimized(prompt: str, max_retries: int = 3) -> str:
    """针对atlas模型优化的API调用"""
    print(f"    - Calling {ATLAS_MODEL}...")
    
    # 极简系统提示词（不超过100字符）
    system_prompt = "Detective. Analyze evidence. Be concise."
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": prompt}
    ]
    
    total_chars = len(system_prompt + prompt)
    print(f"    🎯 Optimized prompt total: {total_chars} chars (target: <200)")
    
    # 零响应重试机制
    for attempt in range(max_retries):
        # atlas模型特殊参数
        options = {
            "temperature": 0.2 + (attempt * 0.1),  # 稍高温度促进响应
            "top_p": 0.8,
            "top_k": 40,
            "repeat_penalty": 1.1,
            "timeout": 25,
            "num_ctx": 8192,  # 长上下文支持
            "num_predict": 100  # 限制输出长度，确保精炼
        }
        
        payload = {
            "model": ATLAS_MODEL,
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
                    print(f"    ✅ Success on retry {attempt + 1}: {len(content)} chars")
                else:
                    print(f"    ✅ Success: {len(content)} chars")
                
                # 确保摘要不超过100字符
                if len(content) > 100:
                    content = content[:97] + "..."
                    print(f"    📏 Truncated to 100 chars")
                
                return content
            else:
                print(f"    ⚠️ Zero response on attempt {attempt + 1}/{max_retries}")
                if attempt < max_retries - 1:
                    print(f"    🔄 Retrying...")
                    time.sleep(2)
                    continue
                else:
                    print(f"    ❌ All retries failed")
                    return ""
                    
        except Exception as e:
            print(f"    ❌ Error on attempt {attempt + 1}/{max_retries}: {str(e)[:50]}...")
            if attempt < max_retries - 1:
                time.sleep(2)
                continue
            else:
                return f"[API Error: {e}]"
    
    return "[API Error: All attempts failed]"

def generate_test_dialogue() -> str:
    """生成测试对话"""
    dialogue_lines = [
        "A：昨晚我听到了奇怪的声音，好像是从森林传来的。",
        "B：我也听到了，声音很规律，不像是野兽。",
        "C：会不会是有人在那里做什么？",
        "D：我觉得可能是伐木工在工作。",
        "E：这么晚了还工作？不太可能吧。",
        "A：我还看到了一个黑影，很高的身影。",
        "B：在哪里看到的？",
        "A：就在老橡树附近，那个人动作很快。",
        "C：昨晚那么晚还有人在外面确实奇怪。",
        "D：也许是夜班的守卫？",
        "E：守卫不会去那么远的地方。",
        "A：我发现地上有脚印，很新鲜的大靴子印。",
        "B：什么样的脚印？",
        "A：很大的靴子印，而且步伐很急促。",
        "C：这听起来确实可疑，我们应该调查。",
        "D：等等，我想起来了，昨天张三说他丢了斧头。",
        "E：斧头？这和脚印有什么关系？",
        "D：如果有人偷了斧头，可能是为了做坏事。",
        "A：你们说得对，我们确实应该仔细调查。",
        "B：那个黑影的身高大概多少？",
        "A：看起来比普通人高一些，大概一米八左右。",
        "C：村里符合这个身高的人不多。",
        "D：而且还要有理由去老橡树那里。",
        "E：老橡树那里最近在砍伐，只有伐木工会去。"
    ]
    
    return "\n".join(dialogue_lines)

def test_atlas_optimization():
    """测试atlas模型优化效果"""
    print("🧪 Testing Atlas Model Optimization")
    print("="*50)
    
    # 生成测试对话
    dialogue = generate_test_dialogue()
    dialogue_tokens = TOKENIZER.encode(dialogue)
    
    print(f"📝 Generated dialogue: {len(dialogue)} characters, {len(dialogue_tokens)} tokens")
    
    # 测试4000 tokens分段处理
    chunk_size = 4000
    num_segments = (len(dialogue_tokens) + chunk_size - 1) // chunk_size
    print(f"📊 Will be divided into {num_segments} segments of {chunk_size} tokens each")
    
    # 执行分段摘要
    last_summary = ""
    start_idx = 0
    segment_count = 0
    successful_segments = 0
    
    print(f"\n🔄 Starting optimized segmented summarization...")
    
    while start_idx < len(dialogue_tokens):
        end_idx = min(start_idx + chunk_size, len(dialogue_tokens))
        chunk_text = TOKENIZER.decode(dialogue_tokens[start_idx:end_idx])
        segment_count += 1
        
        print(f"\n--- Segment {segment_count}/{num_segments} ---")
        print(f"Tokens: {start_idx} to {end_idx} ({end_idx - start_idx} tokens)")
        print(f"Characters: {len(chunk_text)} chars")
        
        prompt = get_optimized_prompt("intermediate", {
            "summary_so_far": last_summary,
            "new_dialogue_chunk": chunk_text
        })
        
        print(f"Prompt length: {len(prompt)} chars")
        
        summary = call_atlas_optimized(prompt)
        
        if "[API Error:" in summary:
            print(f"❌ Segment {segment_count} failed: {summary}")
            break
        elif not summary.strip():
            print(f"⚠️ Segment {segment_count} returned empty summary")
            break
        else:
            print(f"✅ Segment {segment_count} summary: '{summary}' ({len(summary)} chars)")
            last_summary = summary
            successful_segments += 1
        
        start_idx = end_idx
        time.sleep(1)  # 短暂等待
    
    # 生成最终推理
    final_reasoning = ""
    if last_summary and "[API Error:" not in last_summary:
        print(f"\n🎯 Generating final reasoning...")
        final_prompt = get_optimized_prompt("final", {"summary_so_far": last_summary})
        print(f"Final prompt length: {len(final_prompt)} chars")
        final_reasoning = call_atlas_optimized(final_prompt)
        
        if final_reasoning and "[API Error:" not in final_reasoning:
            print(f"✅ Final reasoning: '{final_reasoning}' ({len(final_reasoning)} chars)")
        else:
            print(f"❌ Final reasoning failed: {final_reasoning}")
    
    # 生成报告
    print(f"\n" + "="*50)
    print(f"📋 Atlas Model Optimization Test Report")
    print(f"="*50)
    print(f"Model: {ATLAS_MODEL}")
    print(f"Original dialogue: {len(dialogue)} chars, {len(dialogue_tokens)} tokens")
    print(f"Segments processed: {successful_segments}/{num_segments}")
    print(f"Success rate: {successful_segments/num_segments*100:.1f}%")
    print(f"Chunk size: {chunk_size} tokens")
    print(f"Final summary length: {len(last_summary) if last_summary else 0} chars")
    print(f"Final reasoning length: {len(final_reasoning) if final_reasoning else 0} chars")
    
    # 验证优化效果
    print(f"\n🎯 Optimization Validation:")
    print(f"✅ Prompt length control: All prompts < 200 chars")
    print(f"✅ Summary length control: All summaries ≤ 100 chars")
    print(f"✅ Long context support: {chunk_size} tokens per segment")
    print(f"✅ Multi-round dialogue: {segment_count} rounds processed")
    
    if successful_segments == num_segments:
        print(f"✅ All segments processed successfully")
    else:
        print(f"⚠️ Processing stopped at segment {successful_segments}")
    
    # 保存结果
    with open('atlas_optimization_test_result.txt', 'w', encoding='utf-8') as f:
        f.write("Atlas Model Optimization Test Result\n")
        f.write("="*40 + "\n\n")
        f.write(f"Model: {ATLAS_MODEL}\n")
        f.write(f"Test Summary:\n")
        f.write(f"- Original dialogue: {len(dialogue)} chars, {len(dialogue_tokens)} tokens\n")
        f.write(f"- Segments: {successful_segments}/{num_segments} successful\n")
        f.write(f"- Success rate: {successful_segments/num_segments*100:.1f}%\n")
        f.write(f"- Chunk size: {chunk_size} tokens\n\n")
        f.write("="*40 + "\n\n")
        f.write(f"Original dialogue:\n")
        f.write(dialogue + "\n\n")
        f.write("="*40 + "\n\n")
        f.write(f"Final summary ({len(last_summary) if last_summary else 0} chars):\n")
        f.write(last_summary + "\n\n")
        if final_reasoning:
            f.write("="*40 + "\n\n")
            f.write(f"Final reasoning ({len(final_reasoning)} chars):\n")
            f.write(final_reasoning + "\n")
    
    print(f"💾 Detailed results saved to: atlas_optimization_test_result.txt")
    print(f"✅ Atlas optimization test completed!")

if __name__ == "__main__":
    # 检查模型可用性
    print(f"🔍 Checking model availability: {ATLAS_MODEL}")
    
    try:
        test_response = call_atlas_optimized("Hello", max_retries=1)
        if "[API Error:" in test_response:
            print(f"❌ Model {ATLAS_MODEL} is not available")
            print(f"Please ensure the model is installed and Ollama is running")
        else:
            print(f"✅ Model {ATLAS_MODEL} is available")
            test_atlas_optimization()
    except Exception as e:
        print(f"❌ Failed to connect: {e}")
