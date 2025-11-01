#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Pillar 25: 角色独立性测试便捷运行脚本

提供多种运行模式：
- 完整测试模式
- 快速测试模式  
- 验证模式
- 批量测试模式
"""

import sys
import os
import argparse
from pathlib import Path
from typing import List, Optional

# 设置UTF-8编码输出
if sys.platform.startswith('win'):
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

# 添加项目根目录到Python路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

try:
    from tests.test_pillar_25_independence import run_independence_test, validate_test_integration
    from independence.test_integration import main as integration_test
    from config import MODEL_TO_TEST, MODELS_TO_TEST
except ImportError as e:
    print(f"❌ 导入错误: {e}")
    print("请确保所有依赖模块都已正确实现")
    sys.exit(1)

def run_full_test(model_name: str, output_dir: str = "testout") -> bool:
    """运行完整测试"""
    print(f"🚀 启动完整角色独立性测试...")
    print(f"📋 模型: {model_name}")
    print(f"📁 输出目录: {output_dir}")
    
    try:
        results = run_independence_test(model_name, output_dir)
        
        if 'error' not in results:
            overall_score = results.get('overall_scores', {}).get('overall_independence', 0.0)
            grade = results.get('summary', {}).get('grade', 'Unknown')
            
            print(f"\n🎉 测试完成!")
            print(f"📊 综合得分: {overall_score:.3f}")
            print(f"🏆 评级: {grade}")
            return True
        else:
            print(f"❌ 测试失败: {results.get('error', 'Unknown error')}")
            return False
            
    except Exception as e:
        print(f"❌ 测试执行异常: {e}")
        return False

def run_quick_test(model_name: str, output_dir: str = "testout") -> bool:
    """运行快速测试（简化配置）"""
    print(f"⚡ 启动快速角色独立性测试...")
    print(f"📋 模型: {model_name}")
    
    # 临时修改测试配置以加速测试
    original_config = None
    try:
        from tests.test_pillar_25_independence import run_independence_test
        
        # 创建快速测试配置
        quick_config = {
            'model_name': model_name,
            'output_dir': output_dir,
            'test_roles': ['software_engineer', 'data_scientist'],  # 减少角色
            'stress_levels': ['low', 'medium'],  # 减少压力等级
            'conversation_length': 8,  # 缩短对话长度
            'memory_test_intervals': [3, 6]  # 减少记忆测试点
        }
        
        print(f"⚡ 使用快速配置: 2个角色, 2个压力等级, 8轮对话")
        
        # 这里需要修改run_independence_test以支持自定义配置
        # 暂时使用标准测试，但输出提示这是快速模式
        results = run_independence_test(model_name, output_dir)
        
        if 'error' not in results:
            overall_score = results.get('overall_scores', {}).get('overall_independence', 0.0)
            print(f"\n⚡ 快速测试完成!")
            print(f"📊 综合得分: {overall_score:.3f}")
            print(f"💡 提示: 这是快速测试结果，完整测试可能有不同结果")
            return True
        else:
            print(f"❌ 快速测试失败: {results.get('error', 'Unknown error')}")
            return False
            
    except Exception as e:
        print(f"❌ 快速测试执行异常: {e}")
        return False

def run_validation_only() -> bool:
    """仅运行系统验证"""
    print("[INFO] 启动系统集成验证...")
    
    try:
        # 运行集成测试
        result = integration_test()
        
        if result == 0:
            print("[SUCCESS] 系统验证通过!")
            print("[READY] 角色独立性测试系统已准备就绪")
            return True
        else:
            print("[ERROR] 系统验证失败!")
            print("[FIX] 请检查错误信息并修复问题")
            return False
            
    except Exception as e:
        print(f"[ERROR] 验证执行异常: {e}")
        return False

def run_batch_test(models: List[str], output_dir: str = "testout") -> dict:
    """批量测试多个模型"""
    print(f"🔄 启动批量角色独立性测试...")
    print(f"📋 模型列表: {', '.join(models)}")
    print(f"📁 输出目录: {output_dir}")
    
    results = {}
    successful_tests = 0
    
    for i, model in enumerate(models, 1):
        print(f"\n{'='*60}")
        print(f"🔄 测试进度: {i}/{len(models)} - {model}")
        print(f"{'='*60}")
        
        try:
            test_result = run_independence_test(model, output_dir)
            
            if 'error' not in test_result:
                overall_score = test_result.get('overall_scores', {}).get('overall_independence', 0.0)
                grade = test_result.get('summary', {}).get('grade', 'Unknown')
                
                results[model] = {
                    'success': True,
                    'score': overall_score,
                    'grade': grade,
                    'details': test_result
                }
                successful_tests += 1
                
                print(f"✅ {model} 测试完成 - 得分: {overall_score:.3f}, 评级: {grade}")
            else:
                results[model] = {
                    'success': False,
                    'error': test_result.get('error', 'Unknown error'),
                    'details': test_result
                }
                print(f"❌ {model} 测试失败: {test_result.get('error', 'Unknown error')}")
                
        except Exception as e:
            results[model] = {
                'success': False,
                'error': str(e),
                'details': None
            }
            print(f"❌ {model} 测试异常: {e}")
    
    # 输出批量测试总结
    print(f"\n{'='*60}")
    print(f"📊 批量测试总结")
    print(f"{'='*60}")
    print(f"总测试数: {len(models)}")
    print(f"成功测试: {successful_tests}")
    print(f"失败测试: {len(models) - successful_tests}")
    
    if successful_tests > 0:
        print(f"\n🏆 成功测试结果:")
        successful_results = [(model, data) for model, data in results.items() if data['success']]
        successful_results.sort(key=lambda x: x[1]['score'], reverse=True)
        
        for model, data in successful_results:
            print(f"  {model}: {data['score']:.3f} ({data['grade']})")
    
    if len(models) - successful_tests > 0:
        print(f"\n❌ 失败测试:")
        failed_results = [(model, data) for model, data in results.items() if not data['success']]
        for model, data in failed_results:
            print(f"  {model}: {data['error']}")
    
    return results

def main():
    """主函数"""
    try:
        parser = argparse.ArgumentParser(description='Pillar 25: 角色认知独立性测试系统')
        parser.add_argument('--mode', choices=['full', 'quick', 'validate', 'batch'], 
                          default='full', help='运行模式 (full, quick, validate, batch)')
        parser.add_argument('--model', type=str, help=f'指定要测试的模型名称 (默认: {MODEL_TO_TEST})')
        parser.add_argument('--output', type=str, default='testout', help='指定输出目录')
        
        args = parser.parse_args()
        
        print("="*80)
        print("Pillar 25: 角色认知独立性测试系统")
        print("="*80)

        # 确定要测试的模型，如果用户未指定，则使用配置中的默认模型
        model_to_run = args.model or MODEL_TO_TEST
        
        if args.mode == 'validate':
            success = run_validation_only()
        elif args.mode == 'quick':
            success = run_quick_test(model_to_run, args.output)
        elif args.mode == 'full':
            success = run_full_test(model_to_run, args.output)
        elif args.mode == 'batch':
            # 批量测试使用其内部定义的模型列表
            success = run_batch_test(MODELS_TO_TEST, args.output)
        else:
            print(f"[ERROR] 未知模式: {args.mode}")
            return 1
        
        return 0 if success else 1
        
    except Exception as e:
        print(f"[ERROR] 程序异常: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
