#!/usr/bin/env python3
"""
LLM角色独立性测试框架 - 高级使用示例

这个示例展示了框架的高级功能，包括:
- 自定义测试配置
- 批量测试
- 结果分析和可视化
- 性能监控
"""

import os
import sys
import time
from pathlib import Path
from typing import Dict, List, Any

# 添加项目根目录到Python路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from testLLM.core.test_runner import TestRunner
from testLLM.core.config_manager import ConfigManager
from testLLM.results.report_generator import ReportGenerator
from testLLM.results.data_exporter import DataExporter

def run_performance_benchmark():
    """运行性能基准测试"""
    
    print("🚀 性能基准测试")
    print("=" * 40)
    
    config_path = project_root / "config" / "test_config.yaml"
    config = ConfigManager(str(config_path))
    runner = TestRunner(config)
    
    # 测试不同模型的性能
    models = ["gpt-3.5-turbo"]  # 可以添加更多模型
    roles = ["software_engineer", "data_scientist", "product_manager"]
    
    performance_results = {}
    
    for model in models:
        print(f"\n🔍 测试模型: {model}")
        model_performance = {}
        
        for role in roles:
            print(f"  📋 测试角色: {role}")
            
            start_time = time.time()
            
            # 运行快速测试
            result = runner.run_character_breaking_test(
                model_name=model,
                role_name=role,
                max_attempts=2
            )
            
            end_time = time.time()
            duration = end_time - start_time
            
            model_performance[role] = {
                'duration': duration,
                'score': result.get('overall_score', 0) if result else 0,
                'success': result is not None
            }
            
            print(f"    ⏱️  耗时: {duration:.2f}秒")
            print(f"    📊 评分: {model_performance[role]['score']:.2f}")
        
        performance_results[model] = model_performance
    
    return performance_results

def run_comparative_analysis():
    """运行比较分析"""
    
    print("\n🔬 比较分析测试")
    print("=" * 40)
    
    config_path = project_root / "config" / "test_config.yaml"
    config = ConfigManager(str(config_path))
    runner = TestRunner(config)
    
    # 定义测试矩阵
    test_matrix = {
        "models": ["gpt-3.5-turbo"],
        "roles": ["software_engineer", "data_scientist"],
        "test_types": ["character_breaking", "implicit_cognition"]
    }
    
    print(f"📊 测试矩阵:")
    print(f"   模型: {', '.join(test_matrix['models'])}")
    print(f"   角色: {', '.join(test_matrix['roles'])}")
    print(f"   测试类型: {', '.join(test_matrix['test_types'])}")
    
    # 运行比较测试
    comparative_results = []
    
    for model in test_matrix["models"]:
        for role in test_matrix["roles"]:
            print(f"\n🧪 测试组合: {model} + {role}")
            
            session_results = {
                'model': model,
                'role': role,
                'timestamp': time.time(),
                'results': {}
            }
            
            for test_type in test_matrix["test_types"]:
                print(f"  🔍 运行 {test_type} 测试...")
                
                if test_type == "character_breaking":
                    result = runner.run_character_breaking_test(model, role, max_attempts=2)
                elif test_type == "implicit_cognition":
                    result = runner.run_implicit_cognition_test(model, role)
                else:
                    result = None
                
                session_results['results'][test_type] = result
                
                if result:
                    score = result.get('overall_score', 0)
                    print(f"    📈 {test_type}: {score:.2f}")
                else:
                    print(f"    ❌ {test_type}: 失败")
            
            comparative_results.append(session_results)
    
    return comparative_results

def analyze_results(results: List[Dict[str, Any]]):
    """分析测试结果"""
    
    print("\n📊 结果分析")
    print("=" * 40)
    
    # 按模型分组分析
    model_stats = {}
    
    for session in results:
        model = session['model']
        if model not in model_stats:
            model_stats[model] = {
                'total_tests': 0,
                'passed_tests': 0,
                'scores': [],
                'test_types': {}
            }
        
        for test_type, result in session['results'].items():
            model_stats[model]['total_tests'] += 1
            
            if test_type not in model_stats[model]['test_types']:
                model_stats[model]['test_types'][test_type] = []
            
            if result and 'overall_score' in result:
                score = result['overall_score']
                model_stats[model]['scores'].append(score)
                model_stats[model]['test_types'][test_type].append(score)
                
                if score >= 0.7:
                    model_stats[model]['passed_tests'] += 1
    
    # 输出分析结果
    for model, stats in model_stats.items():
        print(f"\n🤖 模型: {model}")
        
        if stats['scores']:
            avg_score = sum(stats['scores']) / len(stats['scores'])
            pass_rate = (stats['passed_tests'] / stats['total_tests']) * 100
            
            print(f"   📈 平均分数: {avg_score:.3f}")
            print(f"   ✅ 通过率: {pass_rate:.1f}%")
            print(f"   📊 测试总数: {stats['total_tests']}")
            
            # 按测试类型分析
            for test_type, scores in stats['test_types'].items():
                if scores:
                    avg_type_score = sum(scores) / len(scores)
                    print(f"   🔍 {test_type}: {avg_type_score:.3f}")
        else:
            print("   ❌ 无有效测试结果")

def generate_advanced_reports(results: List[Dict[str, Any]]):
    """生成高级报告"""
    
    print("\n📄 生成高级报告")
    print("=" * 40)
    
    output_dir = project_root / "results" / "advanced_example"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # 初始化报告生成器和数据导出器
    config_path = project_root / "config" / "test_config.yaml"
    config = ConfigManager(str(config_path))
    
    report_generator = ReportGenerator(config)
    data_exporter = DataExporter(config)
    
    # 转换结果格式
    formatted_results = {
        'session_id': f"advanced_test_{int(time.time())}",
        'timestamp': time.strftime("%Y-%m-%d %H:%M:%S"),
        'test_results': {},
        'metadata': {
            'test_type': 'advanced_comparative',
            'total_sessions': len(results)
        }
    }
    
    for session in results:
        model = session['model']
        role = session['role']
        
        if model not in formatted_results['test_results']:
            formatted_results['test_results'][model] = {}
        
        if role not in formatted_results['test_results'][model]:
            formatted_results['test_results'][model][role] = {}
        
        formatted_results['test_results'][model][role] = session['results']
    
    # 生成多种格式的报告
    try:
        # JSON报告
        json_file = data_exporter.export_results(
            formatted_results, 
            str(output_dir), 
            ['json']
        )
        print(f"✅ JSON报告: {json_file.get('json', 'N/A')}")
        
        # CSV报告
        csv_file = data_exporter.export_results(
            formatted_results,
            str(output_dir),
            ['csv']
        )
        print(f"✅ CSV报告: {csv_file.get('csv', 'N/A')}")
        
        # HTML报告
        html_file = report_generator.generate_html_report(
            formatted_results,
            str(output_dir / "advanced_report.html")
        )
        print(f"✅ HTML报告: {html_file}")
        
        # 比较分析报告
        comparison_file = data_exporter.export_comparison_data(
            [formatted_results],
            str(output_dir)
        )
        print(f"✅ 比较分析: {comparison_file}")
        
    except Exception as e:
        print(f"❌ 报告生成失败: {str(e)}")

def main():
    """主函数"""
    
    print("🚀 LLM角色独立性测试框架 - 高级使用示例")
    print("=" * 60)
    
    try:
        # 1. 运行性能基准测试
        performance_results = run_performance_benchmark()
        
        # 2. 运行比较分析
        comparative_results = run_comparative_analysis()
        
        # 3. 分析结果
        analyze_results(comparative_results)
        
        # 4. 生成高级报告
        generate_advanced_reports(comparative_results)
        
        print("\n🎉 高级测试示例完成!")
        print(f"📁 详细结果请查看: {project_root / 'results' / 'advanced_example'}")
        
        # 5. 显示性能统计
        print("\n⚡ 性能统计:")
        for model, model_perf in performance_results.items():
            total_time = sum(role_perf['duration'] for role_perf in model_perf.values())
            avg_score = sum(role_perf['score'] for role_perf in model_perf.values()) / len(model_perf)
            print(f"   {model}: 总耗时 {total_time:.2f}秒, 平均分数 {avg_score:.3f}")
        
    except Exception as e:
        print(f"\n❌ 高级测试过程中发生错误: {str(e)}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())