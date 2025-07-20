#!/usr/bin/env python3
"""
云模型角色独立性测试 - 优先测试云API模型
"""

import sys
import os
import time
import json
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from tests.test_pillar_25_independence import run_independence_test

# 云模型列表 - 按优先级排序
CLOUD_MODELS_TO_TEST = [
    # SiliconFlow API 模型
    'siliconflow/deepseek-ai/DeepSeek-R1-0528-Qwen3-8B',
    'siliconflow/THUDM/GLM-Z1-9B-0414', 
    'siliconflow/Qwen/Qwen2.5-7B-Instruct',
    'siliconflow/THUDM/GLM-4-9B-0414',
    'siliconflow/Qwen/Qwen3-8B',
    'siliconflow/internlm/internlm2_5-7b-chat',
    'siliconflow/THUDM/glm-4-9b-chat',
    
    # 多平台模型 - 使用auto前缀自动轮询
    'auto/llama-3-8b-instruct',  # llama3:instruct 对应
    'auto/phi-3-mini-instruct',   # phi3:mini 对应
    'auto/yi-1.5-6b-chat',       # yi:6b 对应
    'auto/gemma-7b-it',          # gemma 对应
    'auto/granite-3b-code-instruct', # granite-code:3b 对应
    'auto/Mistral-Nemo-12B-instruct', # mistral-nemo:latest 对应
    
    # 备用：直接指定平台
    'groq/llama-3-8b-instruct',
    'together/phi-3-mini-instruct',
    'openrouter/yi-1.5-6b-chat',
]

def test_cloud_model(model_name: str) -> dict:
    """测试单个云模型"""
    print(f"\n{'='*80}")
    print(f"☁️  开始测试云模型: {model_name}")
    print(f"{'='*80}")
    
    start_time = time.time()
    
    try:
        # 运行角色独立性测试
        results = run_independence_test(model_name=model_name)
        
        end_time = time.time()
        test_duration = end_time - start_time
        
        # 添加测试时长信息
        results['test_duration_seconds'] = test_duration
        results['test_duration_formatted'] = f"{test_duration/60:.1f}分钟"
        
        # 获取综合评分
        overall_score = results.get('overall_scores', {}).get('overall_independence', 0.0)
        grade = results.get('summary', {}).get('grade', 'Unknown')
        
        print(f"\n✅ 云模型 {model_name} 测试完成!")
        print(f"📊 综合得分: {overall_score:.3f}")
        print(f"🏆 评级: {grade}")
        print(f"⏱️  测试时长: {test_duration/60:.1f}分钟")
        
        return {
            'model_name': model_name,
            'status': 'success',
            'overall_score': overall_score,
            'grade': grade,
            'test_duration': test_duration,
            'results': results
        }
        
    except Exception as e:
        end_time = time.time()
        test_duration = end_time - start_time
        
        error_msg = str(e)
        print(f"\n❌ 云模型 {model_name} 测试失败!")
        print(f"🔥 错误信息: {error_msg}")
        print(f"⏱️  失败时长: {test_duration/60:.1f}分钟")
        
        return {
            'model_name': model_name,
            'status': 'failed',
            'error': error_msg,
            'test_duration': test_duration,
            'results': None
        }

def main():
    """主函数 - 批量测试云模型"""
    print(f"☁️  云模型角色独立性测试")
    print(f"📋 待测试云模型数量: {len(CLOUD_MODELS_TO_TEST)}")
    print(f"⏰ 预计总时长: {len(CLOUD_MODELS_TO_TEST) * 8}分钟")
    
    # 创建结果目录
    results_dir = Path("testout/cloud_results")
    results_dir.mkdir(parents=True, exist_ok=True)
    
    # 批量测试结果
    batch_results = {
        'test_type': 'cloud_models_independence',
        'start_time': time.strftime('%Y-%m-%d %H:%M:%S'),
        'total_models': len(CLOUD_MODELS_TO_TEST),
        'model_results': [],
        'summary': {}
    }
    
    successful_tests = 0
    failed_tests = 0
    total_start_time = time.time()
    
    # 逐个测试云模型
    for i, model_name in enumerate(CLOUD_MODELS_TO_TEST, 1):
        print(f"\n{'☁️ ' * 15}")
        print(f"进度: {i}/{len(CLOUD_MODELS_TO_TEST)} - {model_name}")
        print(f"{'☁️ ' * 15}")
        
        # 测试单个云模型
        model_result = test_cloud_model(model_name)
        batch_results['model_results'].append(model_result)
        
        # 统计结果
        if model_result['status'] == 'success':
            successful_tests += 1
        else:
            failed_tests += 1
        
        # 保存中间结果
        intermediate_file = results_dir / f"cloud_results_progress_{i}.json"
        with open(intermediate_file, 'w', encoding='utf-8') as f:
            json.dump(batch_results, f, ensure_ascii=False, indent=2)
        
        print(f"\n📈 当前进度统计:")
        print(f"   ✅ 成功: {successful_tests}")
        print(f"   ❌ 失败: {failed_tests}")
        print(f"   📊 成功率: {successful_tests/(successful_tests+failed_tests)*100:.1f}%")
        
        # 短暂休息，避免API限流
        if i < len(CLOUD_MODELS_TO_TEST):
            print(f"   ⏸️  休息10秒，避免API限流...")
            time.sleep(10)
    
    # 计算总体统计
    total_end_time = time.time()
    total_duration = total_end_time - total_start_time
    
    batch_results['end_time'] = time.strftime('%Y-%m-%d %H:%M:%S')
    batch_results['total_duration_seconds'] = total_duration
    batch_results['total_duration_formatted'] = f"{total_duration/3600:.1f}小时"
    batch_results['summary'] = {
        'successful_tests': successful_tests,
        'failed_tests': failed_tests,
        'success_rate': successful_tests / len(CLOUD_MODELS_TO_TEST) * 100,
        'average_test_time': total_duration / len(CLOUD_MODELS_TO_TEST)
    }
    
    # 保存最终结果
    final_results_file = results_dir / "cloud_results_final.json"
    with open(final_results_file, 'w', encoding='utf-8') as f:
        json.dump(batch_results, f, ensure_ascii=False, indent=2)
    
    # 输出最终统计
    print(f"\n{'🎉' * 30}")
    print(f"🏁 云模型测试完成!")
    print(f"{'🎉' * 30}")
    print(f"📊 最终统计:")
    print(f"   总云模型数: {len(CLOUD_MODELS_TO_TEST)}")
    print(f"   ✅ 成功: {successful_tests}")
    print(f"   ❌ 失败: {failed_tests}")
    print(f"   📈 成功率: {successful_tests/len(CLOUD_MODELS_TO_TEST)*100:.1f}%")
    print(f"   ⏱️  总时长: {total_duration/3600:.1f}小时")
    print(f"   📁 结果文件: {final_results_file}")
    
    # 显示最佳云模型
    successful_models = [r for r in batch_results['model_results'] if r['status'] == 'success']
    if successful_models:
        # 按得分排序
        successful_models.sort(key=lambda x: x.get('overall_score', 0), reverse=True)
        
        print(f"\n🏆 云模型排行榜 (Top 5):")
        for i, model in enumerate(successful_models[:5], 1):
            print(f"   {i}. {model['model_name']}")
            print(f"      📊 得分: {model.get('overall_score', 0):.3f}")
            print(f"      🏅 评级: {model.get('grade', 'Unknown')}")
            print(f"      ⏱️  时长: {model.get('test_duration', 0)/60:.1f}分钟")
    
    # 按API提供商分组统计
    api_stats = {}
    for result in batch_results['model_results']:
        if result['status'] == 'success':
            model_name = result['model_name']
            if model_name.startswith('siliconflow/'):
                api_provider = 'SiliconFlow'
            elif model_name.startswith('auto/'):
                api_provider = 'Auto-Multi-Cloud'
            elif model_name.startswith('groq/'):
                api_provider = 'Groq'
            elif model_name.startswith('together/'):
                api_provider = 'Together'
            elif model_name.startswith('openrouter/'):
                api_provider = 'OpenRouter'
            else:
                api_provider = 'Other'
            
            if api_provider not in api_stats:
                api_stats[api_provider] = {'count': 0, 'avg_score': 0, 'scores': []}
            
            api_stats[api_provider]['count'] += 1
            api_stats[api_provider]['scores'].append(result.get('overall_score', 0))
    
    # 计算平均分
    for provider in api_stats:
        scores = api_stats[provider]['scores']
        api_stats[provider]['avg_score'] = sum(scores) / len(scores) if scores else 0
    
    print(f"\n📊 API提供商表现:")
    for provider, stats in api_stats.items():
        print(f"   {provider}: {stats['count']}个模型, 平均分: {stats['avg_score']:.3f}")

if __name__ == "__main__":
    main()
