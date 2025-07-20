#!/usr/bin/env python3
"""
LLM角色独立性测试框架 - 主运行脚本

使用方法:
    python run_tests.py --help                    # 查看帮助
    python run_tests.py --basic                   # 运行基础测试
    python run_tests.py --comprehensive           # 运行综合测试
    python run_tests.py --model gpt-4 --role software_engineer  # 指定模型和角色
"""

import argparse
import sys
import os
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from testLLM.core.test_runner import TestRunner
from testLLM.core.config_manager import ConfigManager

def setup_argument_parser():
    """设置命令行参数解析器"""
    
    parser = argparse.ArgumentParser(
        description="LLM角色独立性测试框架",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例用法:
  %(prog)s --basic                                    # 运行基础测试
  %(prog)s --comprehensive                            # 运行综合测试
  %(prog)s --model gpt-4 --role software_engineer    # 测试特定模型和角色
  %(prog)s --batch --models gpt-4,gpt-3.5-turbo      # 批量测试多个模型
  %(prog)s --config custom_config.yaml               # 使用自定义配置
        """
    )
    
    # 测试模式选择
    mode_group = parser.add_mutually_exclusive_group()
    mode_group.add_argument(
        '--basic', 
        action='store_true',
        help='运行基础测试（快速验证）'
    )
    mode_group.add_argument(
        '--comprehensive', 
        action='store_true',
        help='运行综合测试（完整测试套件）'
    )
    mode_group.add_argument(
        '--batch', 
        action='store_true',
        help='批量测试模式'
    )
    
    # 模型和角色选择
    parser.add_argument(
        '--model', 
        type=str,
        help='指定要测试的模型名称'
    )
    parser.add_argument(
        '--models', 
        type=str,
        help='指定多个模型（逗号分隔）'
    )
    parser.add_argument(
        '--role', 
        type=str,
        help='指定要测试的角色名称'
    )
    parser.add_argument(
        '--roles', 
        type=str,
        help='指定多个角色（逗号分隔）'
    )
    
    # 测试类型选择
    parser.add_argument(
        '--test-types', 
        type=str,
        default='character_breaking,implicit_cognition,longitudinal_consistency',
        help='指定测试类型（逗号分隔），默认: character_breaking,implicit_cognition,longitudinal_consistency'
    )
    
    # 配置选项
    parser.add_argument(
        '--config', 
        type=str,
        default='config/test_config.yaml',
        help='配置文件路径，默认: config/test_config.yaml'
    )
    parser.add_argument(
        '--output', 
        type=str,
        default='results',
        help='输出目录，默认: results'
    )
    
    # 报告选项
    parser.add_argument(
        '--formats', 
        type=str,
        default='json,html',
        help='报告格式（逗号分隔），默认: json,html'
    )
    parser.add_argument(
        '--no-report', 
        action='store_true',
        help='不生成报告，仅显示结果'
    )
    
    # 其他选项
    parser.add_argument(
        '--verbose', '-v', 
        action='store_true',
        help='详细输出'
    )
    parser.add_argument(
        '--dry-run', 
        action='store_true',
        help='试运行，不实际执行测试'
    )
    parser.add_argument(
        '--max-attempts', 
        type=int,
        default=5,
        help='每个测试的最大尝试次数，默认: 5'
    )
    
    return parser

def validate_arguments(args):
    """验证命令行参数"""
    
    errors = []
    
    # 检查配置文件是否存在
    config_path = Path(args.config)
    if not config_path.exists():
        errors.append(f"配置文件不存在: {args.config}")
    
    # 检查输出目录
    output_path = Path(args.output)
    try:
        output_path.mkdir(parents=True, exist_ok=True)
    except Exception as e:
        errors.append(f"无法创建输出目录 {args.output}: {str(e)}")
    
    # 检查测试参数
    if not any([args.basic, args.comprehensive, args.batch, args.model, args.models]):
        errors.append("必须指定测试模式或具体的模型")
    
    if errors:
        print("❌ 参数验证失败:")
        for error in errors:
            print(f"   {error}")
        return False
    
    return True

def run_basic_test(runner, args):
    """运行基础测试"""
    
    print("🧪 运行基础测试")
    print("=" * 40)
    
    # 使用默认的测试配置
    models = ["gpt-3.5-turbo"]
    roles = ["software_engineer"]
    
    if args.model:
        models = [args.model]
    if args.role:
        roles = [args.role]
    
    results = {}
    
    for model in models:
        for role in roles:
            print(f"\n🔍 测试: {model} + {role}")
            
            # 运行角色破坏测试
            result = runner.run_character_breaking_test(
                model_name=model,
                role_name=role,
                max_attempts=min(args.max_attempts, 3)  # 基础测试限制尝试次数
            )
            
            if result:
                score = result.get('overall_score', 0)
                status = "✅ 通过" if score >= 0.7 else "❌ 失败"
                print(f"   结果: {score:.3f} {status}")
                
                if model not in results:
                    results[model] = {}
                results[model][role] = {'character_breaking': result}
            else:
                print("   ❌ 测试失败")
    
    return results

def run_comprehensive_test(runner, args):
    """运行综合测试"""
    
    print("🔬 运行综合测试")
    print("=" * 40)
    
    # 确定测试模型和角色
    models = ["gpt-3.5-turbo"]
    roles = ["software_engineer", "data_scientist"]
    
    if args.models:
        models = [m.strip() for m in args.models.split(',')]
    elif args.model:
        models = [args.model]
    
    if args.roles:
        roles = [r.strip() for r in args.roles.split(',')]
    elif args.role:
        roles = [args.role]
    
    # 确定测试类型
    test_types = [t.strip() for t in args.test_types.split(',')]
    
    print(f"📊 测试配置:")
    print(f"   模型: {', '.join(models)}")
    print(f"   角色: {', '.join(roles)}")
    print(f"   测试类型: {', '.join(test_types)}")
    
    # 运行综合测试
    results = runner.run_comprehensive_test(
        models=models,
        roles=roles,
        test_types=test_types
    )
    
    return results

def run_batch_test(runner, args):
    """运行批量测试"""
    
    print("📦 运行批量测试")
    print("=" * 40)
    
    # 获取所有可用的模型和角色
    available_models = ["gpt-3.5-turbo", "gpt-4"]  # 可以从配置中读取
    available_roles = ["software_engineer", "data_scientist", "product_manager"]
    
    if args.models:
        models = [m.strip() for m in args.models.split(',')]
    else:
        models = available_models
    
    if args.roles:
        roles = [r.strip() for r in args.roles.split(',')]
    else:
        roles = available_roles
    
    print(f"📊 批量测试配置:")
    print(f"   模型数量: {len(models)}")
    print(f"   角色数量: {len(roles)}")
    print(f"   总测试组合: {len(models) * len(roles)}")
    
    # 运行批量测试
    batch_results = []
    
    for i, model in enumerate(models, 1):
        for j, role in enumerate(roles, 1):
            print(f"\n🔍 [{i}/{len(models)}][{j}/{len(roles)}] 测试: {model} + {role}")
            
            try:
                result = runner.run_character_breaking_test(
                    model_name=model,
                    role_name=role,
                    max_attempts=args.max_attempts
                )
                
                if result:
                    score = result.get('overall_score', 0)
                    status = "✅" if score >= 0.7 else "❌"
                    print(f"   结果: {score:.3f} {status}")
                    
                    batch_results.append({
                        'model': model,
                        'role': role,
                        'score': score,
                        'result': result
                    })
                else:
                    print("   ❌ 测试失败")
                    
            except Exception as e:
                print(f"   ❌ 测试异常: {str(e)}")
    
    return batch_results

def display_results_summary(results):
    """显示结果摘要"""
    
    print("\n📊 测试结果摘要")
    print("=" * 40)
    
    if isinstance(results, dict) and 'test_results' in results:
        # 综合测试结果格式
        total_tests = 0
        passed_tests = 0
        
        for model_name, model_results in results['test_results'].items():
            print(f"\n🤖 模型: {model_name}")
            
            for role_name, role_results in model_results.items():
                print(f"   👤 角色: {role_name}")
                
                for test_type, test_result in role_results.items():
                    if isinstance(test_result, dict) and 'overall_score' in test_result:
                        score = test_result['overall_score']
                        status = "✅ 通过" if score >= 0.7 else "❌ 失败"
                        print(f"      🧪 {test_type}: {score:.3f} {status}")
                        
                        total_tests += 1
                        if score >= 0.7:
                            passed_tests += 1
        
        if total_tests > 0:
            pass_rate = (passed_tests / total_tests) * 100
            print(f"\n📈 总体统计:")
            print(f"   总测试数: {total_tests}")
            print(f"   通过数: {passed_tests}")
            print(f"   通过率: {pass_rate:.1f}%")
    
    elif isinstance(results, list):
        # 批量测试结果格式
        total_tests = len(results)
        passed_tests = sum(1 for r in results if r.get('score', 0) >= 0.7)
        
        if total_tests > 0:
            pass_rate = (passed_tests / total_tests) * 100
            avg_score = sum(r.get('score', 0) for r in results) / total_tests
            
            print(f"📈 批量测试统计:")
            print(f"   总测试数: {total_tests}")
            print(f"   通过数: {passed_tests}")
            print(f"   通过率: {pass_rate:.1f}%")
            print(f"   平均分数: {avg_score:.3f}")

def main():
    """主函数"""
    
    # 解析命令行参数
    parser = setup_argument_parser()
    args = parser.parse_args()
    
    # 显示标题
    print("🚀 LLM角色独立性测试框架")
    print("=" * 50)
    
    # 验证参数
    if not validate_arguments(args):
        return 1
    
    # 试运行模式
    if args.dry_run:
        print("🔍 试运行模式 - 不会实际执行测试")
        print(f"   配置文件: {args.config}")
        print(f"   输出目录: {args.output}")
        print(f"   报告格式: {args.formats}")
        return 0
    
    try:
        # 初始化配置和测试运行器
        print("📋 正在加载配置...")
        config = ConfigManager(args.config)
        
        print("🔧 正在初始化测试运行器...")
        runner = TestRunner(config)
        
        # 根据模式运行测试
        results = None
        
        if args.basic:
            results = run_basic_test(runner, args)
        elif args.comprehensive:
            results = run_comprehensive_test(runner, args)
        elif args.batch:
            results = run_batch_test(runner, args)
        elif args.model or args.models:
            # 单独指定模型的情况，运行综合测试
            results = run_comprehensive_test(runner, args)
        
        # 显示结果摘要
        if results:
            display_results_summary(results)
            
            # 生成报告
            if not args.no_report:
                print("\n📄 正在生成报告...")
                
                formats = [f.strip() for f in args.formats.split(',')]
                
                if isinstance(results, dict):
                    report_files = runner.generate_report(results, args.output, formats)
                else:
                    # 批量测试结果需要转换格式
                    formatted_results = {
                        'session_id': f"batch_test_{int(__import__('time').time())}",
                        'timestamp': __import__('time').strftime("%Y-%m-%d %H:%M:%S"),
                        'test_results': {},
                        'batch_results': results
                    }
                    report_files = runner.generate_report(formatted_results, args.output, formats)
                
                print("✅ 报告生成完成:")
                for format_type, file_path in report_files.items():
                    print(f"   📁 {format_type.upper()}: {file_path}")
        
        print("\n🎉 测试完成!")
        
    except KeyboardInterrupt:
        print("\n⚠️ 用户中断测试")
        return 1
    except Exception as e:
        print(f"\n❌ 测试过程中发生错误: {str(e)}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())