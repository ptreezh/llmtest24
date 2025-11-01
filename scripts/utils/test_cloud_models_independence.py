#!/usr/bin/env python3
"""
云模型角色独立性测试 - 只测试指定的三个模型
"""

import sys
import os
import time
import json
import requests
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from tests.test_pillar_25_independence import run_independence_test
from utils import call_ppinfra, call_gemini, call_dashscope, call_glm, call_baidu_llm

# 只测试指定的模型
CLOUD_MODELS_TO_TEST = [
    # Google Gemini模型 - 暂时注释（配额限制）
    # 'gemini/gemini-1.5-flash-latest',
    
    # PPInfra模型
    'ppinfra/qwen/qwen3-235b-a22b-fp8',
    'ppinfra/minimaxai/minimax-m1-80k',
    
    # 阿里云DashScope模型
    'dashscope/qwen-plus',
    'dashscope/qwen-max',
    
    # 智谱AI GLM模型
    'glm/glm-4-plus',
    'glm/glm-z1-airx',
    'glm/glm-z1-flash',
    
    # 百度云模型
    'baidu/ernie-4.0-8k',
    'baidu/ernie-3.5-8k',
    'baidu/ernie-speed-8k',
]

def main():
    """主函数：运行云模型角色独立性测试"""
    print("="*80)
    print("🚀 开始云模型角色独立性测试")
    print("="*80)
    
    results = {}
    
    for model in CLOUD_MODELS_TO_TEST:
        print(f"\n\n--- 测试模型: {model} ---")
        try:
            # 运行独立性测试
            test_result = run_independence_test(model)
            results[model] = test_result
            
            # 保存中间结果
            with open(f"testout/cloud_independence_{model.replace('/', '_')}.json", "w", encoding="utf-8") as f:
                json.dump(test_result, f, ensure_ascii=False, indent=2)
            
            print(f"✅ 模型 {model} 测试完成")
        except Exception as e:
            print(f"❌ 模型 {model} 测试失败: {e}")
            import traceback
            traceback.print_exc()  # 打印完整错误堆栈
            results[model] = {"error": str(e)}
    
    # 保存总结果
    with open("testout/cloud_independence_results.json", "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    
    print("\n"+"="*80)
    print("🏁 云模型角色独立性测试完成")
    print("="*80)
    
    # 打印简要结果
    print("\n简要结果:")
    for model, result in results.items():
        if "error" in result:
            print(f"❌ {model}: 测试失败 - {result['error']}")
        else:
            score = result.get("independence_score", 0)
            print(f"{'✅' if score >= 0.7 else '⚠️'} {model}: 独立性得分 = {score:.2f}")

if __name__ == "__main__":
    main()


