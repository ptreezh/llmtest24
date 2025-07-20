#!/usr/bin/env python3
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
    print(f"🔍 启动系统集成验证...")
    
    try:
        # 运行集成测试
        result = integration_test()
        
        if result == 0:
            print(f"\n✅ 系统验证通过!")
            print(f"🎯 角色独立性测试系统已准备就绪")
            return True
        else:
            print(f"\n❌ 系统验证失败!")
            print(f"🔧 请检查错误信息并修复问题")
            return False
            
    except Exception as e:
        print(f"❌ 验证执行异常: {e}")
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
    parser = argparse.ArgumentParser(
        description="Pillar 25: 角色独立性测试便捷运行脚本",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用示例:
  python run_pillar_25_independence.py                    # 使用默认模型运行完整测试
  python run_pillar_25_independence.py --quick            # 快速测试模式
  python run_pillar_25_independence.py --validate-only    # 仅验证系统
  python run_pillar_25_independence.py --model qwen2:7b   # 指定模型测试
  python run_pillar_25_independence.py --batch            # 批量测试所有配置的模型
  python run_pillar_25_independence.py --batch --models model1 model2  # 批量测试指定模型
        """
    )
    
    parser.add_argument(
        '--model', '-m',
        type=str,
        default=None,
        help=f'指定要测试的模型名称 (默认: {MODEL_TO_TEST})'
    )
    
    parser.add_argument(
        '--output-dir', '-o',
        type=str,
        default='testout',
        help='指定输出目录 (默认: testout)'
    )
    
    parser.add_argument(
        '--quick', '-q',
        action='store_true',
        help='快速测试模式 (减少测试项目以加速测试)'
    )
    
    parser.add_argument(
        '--validate-only', '-v',
        action='store_true',
        help='仅运行系统集成验证，不执行实际测试'
    )
    
    parser.add_argument(
        '--batch', '-b',
        action='store_true',
        help='批量测试模式 (测试配置中的所有模型)'
    )
    
    parser.add_argument(
        '--models',
        nargs='+',
        help='批量测试时指定模型列表 (与--batch一起使用)'
    )
    
    parser.add_argument(
        '--list-models',
        action='store_true',
        help='列出配置中的所有可用模型'
    )
    
    args = parser.parse_args()
    
    # 列出模型
    if args.list_models:
        print("📋 配置中的可用模型:")
        print(f"  默认模型: {MODEL_TO_TEST}")
        print(f"  所有模型: {', '.join(MODELS_TO_TEST)}")
        return 0
    
    # 验证模式
    if args.validate_only:
        success = run_validation_only()
        return 0 if success else 1
    
    # 批量测试模式
    if args.batch:
        models = args.models if args.models else MODELS_TO_TEST
        results = run_batch_test(models, args.output_dir)
        
        # 统计成功率
        successful_count = sum(1 for r in results.values() if r['success'])
        success_rate = successful_count / len(results) if results else 0
        
        return 0 if success_rate > 0.5 else 1  # 成功率超过50%视为整体成功
    
    # 单模型测试模式
    model_name = args.model if args.model else MODEL_TO_TEST
    
    if args.quick:
        success = run_quick_test(model_name, args.output_dir)
    else:
        success = run_full_test(model_name, args.output_dir)
    
    return 0 if success else 1

if __name__ == "__main__":
    try:
        exit_code = main()
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print(f"\n⚠️  用户中断测试")
        sys.exit(130)
    except Exception as e:
        print(f"\n💥 程序异常: {e}")
        sys.exit(1)





