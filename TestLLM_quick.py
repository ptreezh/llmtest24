#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
快速测试版本 - 验证修改后的TestLLM.py功能
只测试一个案例，一个模型，用于快速验证
"""

import requests
import random
import time
import os
import string
import csv
import tiktoken
from typing import Dict, Any

# --- CONFIGURATION ---
OLLAMA_API_URL = 'http://localhost:11434/api/chat'
# 只测试一个模型进行快速验证
MODELS_TO_TEST = ['atlas/intersync-gemma-7b-instruct-function-calling:latest']
MAX_CONTEXT_TOKENS = 8192
NUM_TEST_CASES = 1  # 只测试一个案例
TOTAL_TURNS_PER_CASE = 500  # 减少对话轮数以加快测试
API_TIMEOUT = 300  # 减少超时时间

def call_ollama(model: str, prompt: str, temperature: float = 0.7) -> str:
    """调用Ollama API"""
    payload = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "stream": False,
        "options": {"temperature": temperature}
    }
    
    try:
        print(f"    - Calling model: {model}...")
        response = requests.post(OLLAMA_API_URL, json=payload, timeout=API_TIMEOUT)
        response.raise_for_status()
        
        response_data = response.json()
        content = response_data.get('message', {}).get('content', '')
        
        if not content:
            print(f"    ⚠️ 零响应警告: 模型 {model} 返回空内容")
            return ""
        
        print(f"    ✅ 响应成功: {len(content)}字符")
        return content
        
    except requests.exceptions.Timeout:
        error_msg = f"[API Error: Timeout after {API_TIMEOUT}s for model {model}]"
        print(f"    ❌ 超时错误: {model}")
        return error_msg
    except Exception as e:
        error_msg = f"[API Error: {str(e)} for model {model}]"
        print(f"    ❌ API错误: {str(e)}")
        return error_msg

def generate_case_script(case_num: int) -> Dict[str, Any]:
    """生成案例脚本"""
    killers = ["A", "B", "C"]
    killer = random.choice(killers)
    
    motives = {
        "A": {
            "motive_desc": "因商业竞争而下毒",
            "strong_clues": [
                "案发现场发现了A独有的特殊毒药残留",
                "A在案发前购买了大量相关化学品",
                "有目击者看到A在受害者饮品中投放物质"
            ],
            "red_herrings": [
                "当晚有人听到了奇怪的音乐声",
                "受害者最近收到了匿名威胁信",
                "现场发现了不明指纹"
            ]
        },
        "B": {
            "motive_desc": "因木材利润纠纷而行凶",
            "strong_clues": [
                "案发现场发现了稀有的松木碎屑，只有伐木工 B 会接触这种木材",
                "B 的斧头最近被异常仔细地打磨和清洗过",
                "有村民听到 B 在案发前晚对受害者咆哮说'这是你最后一次交货'"
            ],
            "red_herrings": [
                "当晚有人听到了奇怪的野兽嚎叫声",
                "一个常在河边散步的村民看到一个模糊的黑影跳入水中",
                "受害者最近似乎中了一笔小彩票，但很快就花光了"
            ]
        },
        "C": {
            "motive_desc": "因感情纠纷而报复",
            "strong_clues": [
                "C的日记中详细记录了对受害者的怨恨",
                "案发现场发现了C的个人物品",
                "C在案发时间没有不在场证明"
            ],
            "red_herrings": [
                "现场发现了陌生的脚印",
                "受害者最近行为异常",
                "邻居听到了争吵声但不确定是谁"
            ]
        }
    }
    
    script = motives[killer]
    return {
        "true_killer": killer,
        "motive": script["motive_desc"],
        "strong_clues": script["strong_clues"],
        "weak_clues": script["red_herrings"],
        "all_clues": script["strong_clues"] + script["red_herrings"]
    }

def get_prompt(prompt_type: str, context: Dict[str, Any]) -> str:
    """生成提示词"""
    if prompt_type == "summary":
        return f"""
Please provide a concise summary of the following dialogue segment. Focus on key facts, clues, and important details that might be relevant to solving a mystery.

Dialogue segment:
---
{context['dialogue_segment']}
---

Previous summary (if any):
{context.get('previous_summary', 'None')}

Please provide an updated summary that incorporates both the previous summary and the new dialogue segment:
"""
    
    elif prompt_type == "final":
        return f"""
You are a detective analyzing a mystery case. Based on all the evidence and information gathered, please provide your final analysis and conclusion.

Summary of all evidence and information:
---
{context['summary_so_far']}
---

Please provide your final reasoning and identify who you believe is the perpetrator and why. Be specific about the evidence that supports your conclusion.
"""

def save_case_analysis(case_num: int, model: str, script: Dict[str, Any], final_reasoning: str):
    """保存案例分析报告"""
    # 检查模型响应质量
    if not final_reasoning or final_reasoning.strip() == "":
        reasoning_status = "❌ 模型未提供分析 (零响应问题)"
        reasoning_content = "无响应内容"
    elif "[API Error:" in final_reasoning:
        reasoning_status = "❌ API调用错误"
        reasoning_content = final_reasoning
    else:
        reasoning_status = "✅ 模型提供了分析"
        reasoning_content = final_reasoning
    
    analysis_report = f"""
=== 案例 {case_num} 分析报告 ===
模型: {model}
时间: {time.strftime('%Y-%m-%d %H:%M:%S')}
状态: {reasoning_status}

--- 模型原始分析 ---
{reasoning_content}

--- 正确答案与评判标准 ---
✅ 正确凶手: {script['true_killer']}
✅ 作案动机: {script['motive']}

✅ 关键证据 (强线索):
{chr(10).join(f"  • {clue}" for clue in script['strong_clues'])}

⚠️ 干扰信息 (弱线索):
{chr(10).join(f"  • {clue}" for clue in script['weak_clues'])}

📋 评判标准:
1. 凶手识别 (是否正确指出 {script['true_killer']})
2. 证据使用 (是否有效利用关键证据)
3. 逻辑推理 (推理链是否清晰连贯)
4. 干扰排除 (是否被弱线索误导)

--- 推理要点 ---
正确的推理应该:
• 重点关注强线索，它们直接指向真凶
• 识别并排除干扰信息
• 建立清晰的因果关系链
• 得出明确的结论

--- 手动评判指南 ---
请根据以上标准对模型分析进行评分 (1-5分):
□ 凶手识别: ___/5 (是否正确识别出 {script['true_killer']})
□ 证据使用: ___/5 (是否有效使用强线索)
□ 逻辑推理: ___/5 (推理是否清晰连贯)
□ 干扰排除: ___/5 (是否避免被弱线索误导)
□ 总体评分: ___/5

===============================
"""
    
    filename = f"quick_test_case_{case_num}_{model.replace('/', '_').replace(':', '_')}_analysis.txt"
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(analysis_report)
    
    print(f"    ✅ 分析报告已保存: {filename}")
    return analysis_report

def run_quick_test():
    """运行快速测试"""
    print("🚀 快速测试开始")
    print("="*50)
    
    results = []
    
    for i in range(NUM_TEST_CASES):
        print(f"\n--- 运行测试案例 {i + 1}/{NUM_TEST_CASES} ---")
        
        # 生成案例
        script = generate_case_script(i + 1)
        print(f"  - 案例生成完成. 凶手: {script['true_killer']}")
        
        # 生成简化的对话内容
        dialogue_content = f"""
侦探调查记录 - 案例 {i + 1}

现场勘查:
{chr(10).join(f"- {clue}" for clue in script['all_clues'])}

嫌疑人信息:
- 嫌疑人A: 商人，与受害者有商业往来
- 嫌疑人B: 伐木工，与受害者有合作关系  
- 嫌疑人C: 邻居，与受害者关系复杂

调查进展:
经过详细调查，发现了多条线索。需要仔细分析哪些是关键证据，哪些可能是干扰信息。
"""
        
        # 使用tiktoken计算token数
        encoding = tiktoken.get_encoding("cl100k_base")
        dialogue_tokens = encoding.encode(dialogue_content)
        print(f"  - 对话内容生成完成. 总tokens: {len(dialogue_tokens)}")
        
        for model in MODELS_TO_TEST:
            print(f"\n  测试模型: {model}, 策略: Balanced-4k")
            
            # 平衡策略处理
            breakpoint = int(MAX_CONTEXT_TOKENS * 0.5)  # 4096
            
            if len(dialogue_tokens) <= breakpoint:
                # 直接处理
                print(f"    - 直接处理: {len(dialogue_tokens)} tokens")
                summary_prompt = get_prompt("summary", {
                    "dialogue_segment": dialogue_content,
                    "previous_summary": ""
                })
                last_summary = call_ollama(model, summary_prompt)
            else:
                # 分段处理
                print(f"    - 分段处理: 段1 (0 到 {breakpoint})")
                segment1 = encoding.decode(dialogue_tokens[:breakpoint])
                summary_prompt1 = get_prompt("summary", {
                    "dialogue_segment": segment1,
                    "previous_summary": ""
                })
                summary1 = call_ollama(model, summary_prompt1)
                
                print(f"    - 分段处理: 段2 ({breakpoint} 到 {len(dialogue_tokens)})")
                segment2 = encoding.decode(dialogue_tokens[breakpoint:])
                summary_prompt2 = get_prompt("summary", {
                    "dialogue_segment": segment2,
                    "previous_summary": summary1
                })
                last_summary = call_ollama(model, summary_prompt2)
            
            # 最终推理
            if "[API Error:" in last_summary:
                final_reasoning = last_summary
            else:
                print("    - 生成最终推理...")
                final_prompt = get_prompt("final", {"summary_so_far": last_summary})
                final_reasoning = call_ollama(model, final_prompt)
            
            # 保存分析报告
            if "[API Error:" not in final_reasoning:
                print("    - 保存分析报告...")
                save_case_analysis(i + 1, model, script, final_reasoning)
            
            # 记录结果
            if not final_reasoning or final_reasoning.strip() == "":
                response_status = "zero_response"
            elif "[API Error:" in final_reasoning:
                response_status = "api_error"
            else:
                response_status = "success"
            
            result = {
                "test_case": i + 1,
                "model": model,
                "strategy": "Balanced-4k",
                "true_killer": script['true_killer'],
                "motive": script['motive'],
                "final_reasoning": final_reasoning,
                "response_status": response_status,
                "reasoning_length": len(final_reasoning) if final_reasoning else 0,
                "timestamp": time.strftime('%Y-%m-%d %H:%M:%S')
            }
            results.append(result)
    
    # 保存CSV报告
    if results:
        with open('quick_test_report.csv', 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=results[0].keys())
            writer.writeheader()
            writer.writerows(results)
    
    print(f"\n--- 快速测试完成 ---")
    print(f"CSV报告: quick_test_report.csv")
    print(f"详细分析报告已保存到当前目录")

if __name__ == "__main__":
    run_quick_test()
