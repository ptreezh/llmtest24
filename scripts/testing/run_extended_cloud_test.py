#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
扩展云模型认知生态系统测试

测试更多的云大模型，包括国内外主流的LLM服务。
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

def get_extended_test_models() -> List[Tuple[str, str]]:
    """获取扩展的测试模型列表"""
    return [
        # SiliconFlow 模型
        ('siliconflow', 'THUDM/glm-4-9b-chat'),
        ('siliconflow', 'Qwen/Qwen2.5-7B-Instruct'),
        ('siliconflow', 'deepseek-ai/DeepSeek-V2.5'),
        ('siliconflow', 'deepseek-ai/DeepSeek-V3'),
        
        # Together.ai 模型
        ('together', 'mistralai/Mixtral-8x7B-Instruct-v0.1'),
        ('together', 'meta-llama/Llama-3-8b-chat'),
        
        # OpenRouter 模型
        ('openrouter', 'openai/gpt-3.5-turbo'),
        ('openrouter', 'anthropic/claude-3-opus'),
        ('openrouter', 'google/gemma-2-9b-it'),
        
        # PPInfra 模型
        ('ppinfra', 'qwen/qwen3-235b-a22b-fp8'),
        ('ppinfra', 'minimaxai/minimax-m1-80k'),
        
        # Google Gemini 模型
        ('gemini', 'gemini-1.5-flash'),
        ('gemini', 'gemini-1.5-pro'),
        ('gemini', 'gemini-2.0-flash-exp'),
        
        # 阿里云DashScope 模型
        ('dashscope', 'qwen-plus'),
        ('dashscope', 'qwen-max'),
        ('dashscope', 'qwen-turbo'),
        
        # 智谱AI GLM 模型
        ('glm', 'glm-4-plus'),
        ('glm', 'glm-4-air'),
        ('glm', 'glm-4-airx'),
        ('glm', 'glm-4-flash'),
        
        # 百度文心 模型
        ('baidu', 'ernie-4.0-8k'),
        ('baidu', 'ernie-3.5-8k'),
        ('baidu', 'ernie-speed-8k'),
    ]

def run_extended_batch_test():
    """运行扩展的批量测试"""
    print("🌐 扩展云模型认知生态系统测试")
    print("=" * 70)
    
    test_models = get_extended_test_models()
    print(f"📋 计划测试 {len(test_models)} 个模型:")
    
    # 按服务商分组显示
    services = {}
    for service, model in test_models:
        if service not in services:
            services[service] = []
        services[service].append(model)
    
    for service, models in services.items():
        print(f"\n🔹 {service.upper()}:")
        for i, model in enumerate(models, 1):
            print(f"   {i:2d}. {model}")
    
    print(f"\n🎯 测试特点:")
    print(f"  - 覆盖国内外主流LLM服务")
    print(f"  - 详细的评分解释和计算过程")
    print(f"  - 实时显示测试进度和结果")
    print(f"  - 保存完整的测试数据和解释")
    
    # 询问测试模式
    print(f"\n🎛️ 选择测试模式:")
    print(f"  1. 快速测试 (跳过失败的服务)")
    print(f"  2. 完整测试 (测试所有模型)")
    print(f"  3. 选择性测试 (选择特定服务)")
    
    mode = input(f"请选择测试模式 (1-3，默认1): ").strip() or "1"
    
    if mode == "3":
        print(f"\n📋 可用服务:")
        service_list = list(services.keys())
        for i, service in enumerate(service_list, 1):
            print(f"  {i}. {service}")
        
        selected = input(f"请选择要测试的服务 (用逗号分隔，如1,3,5): ").strip()
        if selected:
            try:
                indices = [int(x.strip()) - 1 for x in selected.split(',')]
                selected_services = [service_list[i] for i in indices if 0 <= i < len(service_list)]
                test_models = [(s, m) for s, m in test_models if s in selected_services]
                print(f"已选择 {len(selected_services)} 个服务，共 {len(test_models)} 个模型")
            except:
                print("输入格式错误，使用默认测试")
    
    # 询问是否继续
    confirm = input(f"\n是否开始测试？(y/N): ").strip().lower()
    if confirm not in ['y', 'yes', '是']:
        print("测试已取消")
        return
    
    # 开始批量测试
    start_time = datetime.now()
    all_results = {}
    successful_tests = []
    failed_tests = []
    skip_fast_mode = mode == "1"
    
    print(f"\n🚀 开始扩展测试 - {start_time.strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 80)
    
    for i, (service_name, model_name) in enumerate(test_models, 1):
        print(f"\n📍 进度: {i}/{len(test_models)} - {service_name}/{model_name}")
        print("─" * 70)
        
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
                error_msg = result.get('error', '未知错误')
                print(f"❌ 测试失败: {error_msg}")
                
                # 快速模式下跳过同一服务的其他模型
                if skip_fast_mode and 'connectivity_failed' in error_msg:
                    remaining_same_service = [
                        (s, m) for s, m in test_models[i:] if s == service_name
                    ]
                    if remaining_same_service:
                        print(f"⚡ 快速模式：跳过 {service_name} 的其余 {len(remaining_same_service)} 个模型")
                        for s, m in remaining_same_service:
                            model_key = f"{s}/{m}"
                            all_results[model_key] = {
                                'model_name': model_key,
                                'status': 'skipped',
                                'error': f'跳过：{service_name} 服务不可用',
                                'test_timestamp': datetime.now().isoformat()
                            }
                            failed_tests.append(all_results[model_key])
                        # 跳过这些模型
                        test_models = [
                            (s, m) for s, m in test_models 
                            if not (s == service_name and (s, m) in remaining_same_service)
                        ]
        
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
    
    # 生成详细汇总报告
    generate_extended_report(
        all_results, successful_tests, failed_tests, 
        start_time, end_time, total_duration, len(test_models)
    )

def generate_extended_report(all_results, successful_tests, failed_tests, 
                           start_time, end_time, total_duration, total_planned):
    """生成扩展测试报告"""
    
    print(f"\n" + "=" * 80)
    print(f"📊 扩展云模型测试完成汇总")
    print(f"=" * 80)
    
    print(f"🕐 测试时间: {start_time.strftime('%Y-%m-%d %H:%M:%S')} - {end_time.strftime('%H:%M:%S')}")
    print(f"⏱️  总耗时: {total_duration:.1f}秒 ({total_duration/60:.1f}分钟)")
    print(f"📈 测试统计:")
    print(f"   计划测试: {total_planned}")
    print(f"   实际测试: {len(all_results)}")
    print(f"   成功测试: {len(successful_tests)}")
    print(f"   失败测试: {len(failed_tests)}")
    print(f"   成功率: {len(successful_tests)/len(all_results)*100:.1f}%")
    
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
        
        # 按服务商分组分析
        service_stats = {}
        for test in successful_tests:
            service = test['service_name']
            if service not in service_stats:
                service_stats[service] = []
            service_stats[service].append(test)
        
        print(f"\n📊 按服务商分析:")
        for service, tests in service_stats.items():
            if tests:
                service_avg = sum(t['scores']['overall_score'] for t in tests) / len(tests)
                best_model = max(tests, key=lambda x: x['scores']['overall_score'])
                print(f"   {service.upper():12s}: 平均 {service_avg:.3f} | "
                      f"最佳 {best_model['model_display_name']} ({best_model['scores']['overall_score']:.3f})")
        
        # 排序并显示前10名
        successful_tests.sort(key=lambda x: x['scores']['overall_score'], reverse=True)
        
        print(f"\n🏆 模型排名 (前10名):")
        for i, test in enumerate(successful_tests[:10], 1):
            scores = test['scores']
            print(f"   {i:2d}. {test['model_name']}")
            print(f"       综合: {scores['overall_score']:.3f} | "
                  f"幻觉: {scores['hallucination_resistance']:.3f} | "
                  f"一致性: {scores['role_consistency']:.3f} | "
                  f"多样性: {scores['cognitive_diversity']:.3f}")
        
        # 分析最佳和最差表现
        if len(successful_tests) >= 2:
            best_model = successful_tests[0]
            worst_model = successful_tests[-1]
            
            print(f"\n🥇 最佳表现: {best_model['model_name']}")
            print(f"   综合得分: {best_model['scores']['overall_score']:.3f}")
            
            print(f"\n🔻 最弱表现: {worst_model['model_name']}")
            print(f"   综合得分: {worst_model['scores']['overall_score']:.3f}")
    
    # 显示失败的测试
    if failed_tests:
        print(f"\n❌ 失败的测试:")
        failure_reasons = {}
        for test in failed_tests:
            reason = test.get('error', '未知错误')
            if reason not in failure_reasons:
                failure_reasons[reason] = []
            failure_reasons[reason].append(test['model_name'])
        
        for reason, models in failure_reasons.items():
            print(f"   {reason}: {len(models)} 个模型")
            for model in models[:3]:  # 只显示前3个
                print(f"     - {model}")
            if len(models) > 3:
                print(f"     - ... 还有 {len(models)-3} 个")
    
    # 保存完整结果
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"extended_cloud_test_results_{timestamp}.json"
    
    final_results = {
        'test_metadata': {
            'test_type': 'extended_cloud_cognitive_ecosystem',
            'start_time': start_time.isoformat(),
            'end_time': end_time.isoformat(),
            'total_duration_seconds': total_duration,
            'total_models_planned': total_planned,
            'total_models_tested': len(all_results),
            'successful_tests': len(successful_tests),
            'failed_tests': len(failed_tests),
            'success_rate': len(successful_tests) / len(all_results) if all_results else 0
        },
        'summary_statistics': {
            'average_scores': {
                'hallucination_resistance': avg_hallucination if successful_tests else 0,
                'role_consistency': avg_consistency if successful_tests else 0,
                'cognitive_diversity': avg_diversity if successful_tests else 0,
                'overall_score': avg_overall if successful_tests else 0
            } if successful_tests else None,
            'service_statistics': service_stats if successful_tests else None,
            'best_model': successful_tests[0]['model_name'] if successful_tests else None,
            'worst_model': successful_tests[-1]['model_name'] if len(successful_tests) > 1 else None
        },
        'individual_results': all_results
    }
    
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(final_results, f, ensure_ascii=False, indent=2)
    
    print(f"\n📁 完整测试结果已保存到: {filename}")
    print(f"📖 文件包含所有模型的详细评分解释和计算过程")
    
    # 生成简化的CSV报告
    if successful_tests:
        csv_filename = f"extended_test_summary_{timestamp}.csv"
        try:
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
        except ImportError:
            print("📊 需要安装pandas才能生成CSV报告")
    
    print(f"\n🎉 扩展测试完成！")
    return final_results

def main():
    """主函数"""
    try:
        results = run_extended_batch_test()
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
