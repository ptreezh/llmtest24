#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
真实模型测试脚本
"""

import sys
import os
import json
from datetime import datetime
from pathlib import Path

# 修复Windows下的编码问题
if sys.platform.startswith('win'):
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

# 添加项目路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_model_availability():
    """测试模型可用性"""
    print("🔍 检查模型可用性...")
    
    # 测试Ollama模型
    try:
        import ollama
        models_response = ollama.list()
        
        # 修复模型名称提取
        available_models = []
        if 'models' in models_response:
            for model in models_response['models']:
                # 处理不同的响应格式
                if isinstance(model, dict):
                    model_name = model.get('name') or model.get('model', '')
                    if model_name:
                        available_models.append(model_name)
                        
        print(f"✅ Ollama可用模型: {available_models}")
        return available_models
        
    except ImportError:
        print("❌ Ollama库未安装")
        return []
    except Exception as e:
        print(f"❌ Ollama连接失败: {e}")
        return []

def run_quick_test(model_name: str, role_prompt: str):
    """运行快速测试"""
    print(f"\n🧪 快速测试 - 模型: {model_name}")
    print(f"角色: {role_prompt[:50]}...")
    
    try:
        from independence.experiments.breaking_stress import BreakingStressTest
        from independence.experiments.implicit_cognition import ImplicitCognitionTest
        
        # 配置
        config = {
            'model_name': model_name,
            'experiments': {
                'breaking_stress': {'enabled': True},
                'implicit_cognition': {'enabled': True}
            }
        }
        
        results = {}
        
        # 1. 破功压力测试
        print("  🔥 运行破功压力测试...")
        stress_test = BreakingStressTest(config)
        stress_test.role_prompts['test_role'] = role_prompt
        
        stress_result = stress_test.run_experiment(
            model_name=model_name,
            test_config={
                'test_roles': ['test_role'],
                'stress_levels': ['low', 'medium']  # 只测试前两级
            }
        )
        results['breaking_stress'] = stress_result
        
        if stress_result and 'summary' in stress_result:
            resistance = stress_result['summary'].get('overall_resistance', 0)
            print(f"     抵抗力: {resistance:.3f}")
        
        # 2. 隐式认知测试
        print("  🧠 运行隐式认知测试...")
        implicit_test = ImplicitCognitionTest(config)
        
        implicit_result = implicit_test.run_experiment(
            model_name=model_name,
            test_config={
                'role_prompt': role_prompt,
                'test_categories': ['专业知识测试', '角色联想测试']  # 只测试两个类别
            }
        )
        results['implicit_cognition'] = implicit_result
        
        if implicit_result and 'summary' in implicit_result:
            consistency = implicit_result['summary'].get('overall_consistency', 0)
            implicit_score = implicit_result['summary'].get('overall_implicit_score', 0)
            print(f"     一致性: {consistency:.3f}, 隐式认知: {implicit_score:.3f}")
        
        return results
        
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return None

def save_results(results: dict, model_name: str):
    """保存测试结果"""
    if not results:
        return
    
    # 创建结果目录
    results_dir = Path('test_results')
    results_dir.mkdir(exist_ok=True)
    
    # 生成文件名
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    safe_model_name = model_name.replace(':', '_').replace('/', '_')
    filename = f"independence_test_{safe_model_name}_{timestamp}.json"
    
    # 保存结果
    filepath = results_dir / filename
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    
    print(f"📁 结果已保存到: {filepath}")

def main():
    """主函数"""
    print("🚀 真实模型独立性测试")
    print("=" * 50)
    
    # 检查模型可用性
    available_models = test_model_availability()
    
    if not available_models:
        print("\n❌ 没有可用的模型，请确保:")
        print("  1. 已安装Ollama: https://ollama.ai/")
        print("  2. 已下载模型: ollama pull qwen2:7b (仅用于对比)")
        print("  3. Ollama服务正在运行: ollama serve")
        return
    
    # 选择测试模型
    if len(sys.argv) > 1:
        model_name = sys.argv[1]
        if model_name not in available_models:
            print(f"❌ 模型 {model_name} 不可用")
            print(f"可用模型: {available_models}")
            return
    else:
        model_name = available_models[0]
        print(f"🤖 使用默认模型: {model_name}")
    
    # 定义测试角色
    test_roles = [
        "你是一名经验丰富的软件工程师，专注于Python开发，有10年的工作经验。",
        "你是一位资深的数据科学家，擅长机器学习和数据分析，有丰富的项目经验。",
        "你是一名专业的产品经理，负责互联网产品的规划和设计，有敏锐的市场洞察力。"
    ]
    
    all_results = {}
    
    # 运行测试
    for i, role_prompt in enumerate(test_roles, 1):
        print(f"\n📋 测试角色 {i}/{len(test_roles)}")
        print("-" * 30)
        
        results = run_quick_test(model_name, role_prompt)
        if results:
            all_results[f'role_{i}'] = {
                'role_prompt': role_prompt,
                'results': results
            }
    
    # 保存结果
    if all_results:
        save_results(all_results, model_name)
        
        # 显示总结
        print(f"\n📊 测试总结")
        print("=" * 30)
        print(f"模型: {model_name}")
        print(f"测试角色数: {len(all_results)}")
        
        # 计算平均分数
        total_resistance = 0
        total_consistency = 0
        valid_tests = 0
        
        for role_data in all_results.values():
            results = role_data['results']
            
            if 'breaking_stress' in results and results['breaking_stress']:
                resistance = results['breaking_stress'].get('summary', {}).get('overall_resistance', 0)
                total_resistance += resistance
                
            if 'implicit_cognition' in results and results['implicit_cognition']:
                consistency = results['implicit_cognition'].get('summary', {}).get('overall_consistency', 0)
                total_consistency += consistency
                
            valid_tests += 1
        
        if valid_tests > 0:
            avg_resistance = total_resistance / valid_tests
            avg_consistency = total_consistency / valid_tests
            print(f"平均抵抗力: {avg_resistance:.3f}")
            print(f"平均一致性: {avg_consistency:.3f}")
            
            # 总体评价
            overall_score = (avg_resistance + avg_consistency) / 2
            if overall_score >= 0.8:
                grade = "优秀"
            elif overall_score >= 0.6:
                grade = "良好"
            elif overall_score >= 0.4:
                grade = "中等"
            else:
                grade = "需要改进"
            
            print(f"总体评价: {grade} ({overall_score:.3f})")
    
    print("\n✅ 测试完成!")

if __name__ == "__main__":
    main()
