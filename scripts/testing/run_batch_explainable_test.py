#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
批量可解释认知生态系统测试

对多个云模型进行详细的认知生态系统测试，提供完整的评分解释。
"""

import sys
import os
import json
import time
from datetime import datetime
from typing import Dict, List, Any, Tuple
from pathlib import Path

# 添加项目根目录到Python路径
sys.path.append('.')

# 导入可解释测试模块
from run_explainable_cognitive_test import run_explainable_test, ExplainableScorer

def get_available_test_models() -> List[Tuple[str, str]]:
    """获取可用的测试模型列表"""
    return [
        ('siliconflow', 'THUDM/glm-4-9b-chat'),
        ('siliconflow', 'Qwen/Qwen2.5-7B-Instruct'),
        ('together', 'mistralai/Mixtral-8x7B-Instruct-v0.1'),
        ('together', 'meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo'),
        ('ppinfra', 'qwen/qwen3-235b-a22b-fp8'),
        ('ppinfra', 'meta-llama/llama-3.1-405b-instruct'),
        ('glm', 'glm-4-plus'),
        ('glm', 'glm-4-0520'),
        ('gemini', 'gemini-1.5-flash'),
        ('gemini', 'gemini-1.5-pro')
    ]

def run_batch_explainable_tests():
    """运行批量可解释测试"""
    print("🧠 批量可解释认知生态系统测试")
    print("=" * 60)
    
    test_models = get_available_test_models()
    print(f"📋 计划测试 {len(test_models)} 个模型:")
    
    for i, (service, model) in enumerate(test_models, 1):
        print(f"  {i:2d}. {service:12s} / {model}")
    
    print(f"\n🎯 测试特点:")
    print(f"  - 详细的评分解释和计算过程")
    print(f"  - 实时显示测试进度和结果")
    print(f"  - 保存完整的测试数据和解释")
    
    # 询问是否继续
    confirm = input(f"\n是否开始批量测试？(y/N): ").strip().lower()
    if confirm not in ['y', 'yes', '是']:
        print("测试已取消")
        return
    
    # 开始批量测试
    start_time = datetime.now()
    all_results = {}
    successful_tests = []
    failed_tests = []
    
    print(f"\n🚀 开始批量测试 - {start_time.strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 80)
    
    for i, (service_name, model_name) in enumerate(test_models, 1):
        print(f"\n📍 进度: {i}/{len(test_models)} - {service_name}/{model_name}")
        print("─" * 60)
        
        try:
            # 运行单个模型的详细测试
            result = run_explainable_test(service_name, model_name)
            
            # 保存结果
            model_key = f"{service_name}/{model_name}"
            all_results[model_key] = result
            
            if result.get('status') == 'success':
                successful_tests.append(result)
                scores = result['scores']
                print(f"✅ 测试成功 - 综合得分: {scores['overall_score']:.3f}")
                print(f"   幻觉抵抗: {scores['hallucination_resistance']:.3f} | "
                      f"角色一致性: {scores['role_consistency']:.3f} | "
                      f"认知多样性: {scores['cognitive_diversity']:.3f}")
            else:
                failed_tests.append(result)
                print(f"❌ 测试失败: {result.get('error', '未知错误')}")
        
        except Exception as e:
            print(f"❌ 测试过程中出现异常: {e}")
            failed_result = {
                'model_name': f"{service_name}/{model_name}",
                'status': 'failed',
                'error': str(e),
                'test_timestamp': datetime.now().isoformat()
            }
            all_results[f"{service_name}/{model_name}"] = failed_result
            failed_tests.append(failed_result)
        
        # 添加延迟以避免API限制
        if i < len(test_models):
            print("⏳ 等待3秒后继续下一个测试...")
            time.sleep(3)
    
    end_time = datetime.now()
    total_duration = (end_time - start_time).total_seconds()
    
    # 生成汇总报告
    print(f"\n" + "=" * 80)
    print(f"📊 批量测试完成汇总")
    print(f"=" * 80)
    
    print(f"🕐 测试时间: {start_time.strftime('%Y-%m-%d %H:%M:%S')} - {end_time.strftime('%H:%M:%S')}")
    print(f"⏱️  总耗时: {total_duration:.1f}秒 ({total_duration/60:.1f}分钟)")
    print(f"📈 测试统计:")
    print(f"   总测试数: {len(test_models)}")
    print(f"   成功测试: {len(successful_tests)}")
    print(f"   失败测试: {len(failed_tests)}")
    print(f"   成功率: {len(successful_tests)/len(test_models):.1%}")
    
    if successful_tests:
        # 计算平均分数
        avg_hallucination = sum(t['scores']['hallucination_resistance'] for t in successful_tests) / len(successful_tests)
        avg_consistency = sum(t['scores']['role_consistency'] for t in successful_tests) / len(successful_tests)
        avg_diversity = sum(t['scores']['cognitive_diversity'] for t in successful_tests) / len(successful_tests)
        avg_overall = sum(t['scores']['overall_score'] for t in successful_tests) / len(successful_tests)
        
        print(f"\n📈 平均分数:")
        print(f"   幻觉抵抗: {avg_hallucination:.3f}")
        print(f"   角色一致性: {avg_consistency:.3f}")
        print(f"   认知多样性: {avg_diversity:.3f}")
        print(f"   综合得分: {avg_overall:.3f}")
        
        # 排序并显示前5名
        successful_tests.sort(key=lambda x: x['scores']['overall_score'], reverse=True)
        
        print(f"\n🏆 模型排名 (前5名):")
        for i, test in enumerate(successful_tests[:5], 1):
            scores = test['scores']
            print(f"   {i}. {test['model_name']}")
            print(f"      综合: {scores['overall_score']:.3f} | "
                  f"幻觉: {scores['hallucination_resistance']:.3f} | "
                  f"一致性: {scores['role_consistency']:.3f} | "
                  f"多样性: {scores['cognitive_diversity']:.3f}")
        
        # 分析最佳和最差表现
        best_model = successful_tests[0]
        worst_model = successful_tests[-1]
        
        print(f"\n🥇 最佳表现: {best_model['model_name']}")
        print(f"   综合得分: {best_model['scores']['overall_score']:.3f}")
        print(f"   优势: ", end="")
        best_scores = best_model['scores']
        strengths = []
        if best_scores['hallucination_resistance'] >= 0.7:
            strengths.append("幻觉抵抗强")
        if best_scores['role_consistency'] >= 0.7:
            strengths.append("角色一致性好")
        if best_scores['cognitive_diversity'] >= 0.8:
            strengths.append("认知多样性高")
        print(", ".join(strengths) if strengths else "综合表现均衡")
        
        if len(successful_tests) > 1:
            print(f"\n🔻 最弱表现: {worst_model['model_name']}")
            print(f"   综合得分: {worst_model['scores']['overall_score']:.3f}")
            print(f"   待改进: ", end="")
            worst_scores = worst_model['scores']
            weaknesses = []
            if worst_scores['hallucination_resistance'] < 0.3:
                weaknesses.append("幻觉抵抗弱")
            if worst_scores['role_consistency'] < 0.3:
                weaknesses.append("角色一致性差")
            if worst_scores['cognitive_diversity'] < 0.6:
                weaknesses.append("认知多样性低")
            print(", ".join(weaknesses) if weaknesses else "各项能力均需提升")
    
    # 显示失败的测试
    if failed_tests:
        print(f"\n❌ 失败的测试:")
        for test in failed_tests:
            print(f"   {test['model_name']}: {test.get('error', '未知错误')}")
    
    # 保存完整结果
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"batch_explainable_test_results_{timestamp}.json"
    
    final_results = {
        'test_metadata': {
            'test_type': 'batch_explainable_cognitive_ecosystem',
            'start_time': start_time.isoformat(),
            'end_time': end_time.isoformat(),
            'total_duration_seconds': total_duration,
            'total_models_tested': len(test_models),
            'successful_tests': len(successful_tests),
            'failed_tests': len(failed_tests),
            'success_rate': len(successful_tests) / len(test_models)
        },
        'summary_statistics': {
            'average_scores': {
                'hallucination_resistance': avg_hallucination if successful_tests else 0,
                'role_consistency': avg_consistency if successful_tests else 0,
                'cognitive_diversity': avg_diversity if successful_tests else 0,
                'overall_score': avg_overall if successful_tests else 0
            } if successful_tests else None,
            'best_model': best_model['model_name'] if successful_tests else None,
            'worst_model': worst_model['model_name'] if successful_tests else None
        },
        'individual_results': all_results
    }
    
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(final_results, f, ensure_ascii=False, indent=2)
    
    print(f"\n📁 完整测试结果已保存到: {filename}")
    print(f"📖 文件包含所有模型的详细评分解释和计算过程")
    
    # 生成简化的CSV报告
    csv_filename = f"batch_test_summary_{timestamp}.csv"
    if successful_tests:
        import pandas as pd
        
        csv_data = []
        for test in successful_tests:
            scores = test['scores']
            csv_data.append({
                '模型名称': test['model_name'],
                '服务商': test['service_name'],
                '综合得分': f"{scores['overall_score']:.3f}",
                '幻觉抵抗': f"{scores['hallucination_resistance']:.3f}",
                '角色一致性': f"{scores['role_consistency']:.3f}",
                '认知多样性': f"{scores['cognitive_diversity']:.3f}",
                '测试时长(秒)': f"{test['test_duration']:.1f}"
            })
        
        df = pd.DataFrame(csv_data)
        df.to_csv(csv_filename, index=False, encoding='utf-8-sig')
        print(f"📊 简化报告已保存到: {csv_filename}")
    
    print(f"\n🎉 批量测试完成！")
    return final_results

def main():
    """主函数"""
    try:
        results = run_batch_explainable_tests()
        return results
    except KeyboardInterrupt:
        print(f"\n\n⚠️ 测试被用户中断")
        return None
    except Exception as e:
        print(f"\n\n❌ 测试过程中出现严重错误: {e}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == "__main__":
    main()
