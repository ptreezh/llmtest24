#!/usr/bin/env python3
"""
LLM角色独立性测试框架 - 基础使用示例

这个示例展示了如何使用测试框架进行基本的角色独立性测试
"""

import os
import sys
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from testLLM.core.test_runner import TestRunner
from testLLM.core.config_manager import ConfigManager

def main():
    """主函数 - 演示基础测试流程"""
    
    print("🚀 LLM角色独立性测试框架 - 基础使用示例")
    print("=" * 50)
    
    try:
        # 1. 初始化配置管理器
        print("📋 正在加载配置...")
        config_path = project_root / "config" / "test_config.yaml"
        config = ConfigManager(str(config_path))
        print("✅ 配置加载成功")
        
        # 2. 创建测试运行器
        print("\n🔧 正在初始化测试运行器...")
        runner = TestRunner(config)
        print("✅ 测试运行器初始化成功")
        
        # 3. 定义测试参数
        test_models = ["gpt-3.5-turbo"]  # 可以根据需要添加更多模型
        test_roles = ["software_engineer", "data_scientist"]
        
        print(f"\n🎯 测试配置:")
        print(f"   模型: {', '.join(test_models)}")
        print(f"   角色: {', '.join(test_roles)}")
        
        # 4. 运行单个测试类型示例
        print("\n" + "="*50)
        print("🧪 运行角色破坏测试示例")
        print("="*50)
        
        for model in test_models:
            for role in test_roles:
                print(f"\n🔍 测试 {model} 模型的 {role} 角色...")
                
                # 运行角色破坏测试
                breaking_results = runner.run_character_breaking_test(
                    model_name=model,
                    role_name=role,
                    max_attempts=3  # 减少测试次数以加快演示
                )
                
                # 显示结果摘要
                if breaking_results:
                    score = breaking_results.get('overall_score', 0)
                    status = "通过" if score >= 0.7 else "失败"
                    print(f"   📊 测试结果: {score:.2f} ({status})")
                    
                    # 显示详细信息
                    if 'test_details' in breaking_results:
                        details = breaking_results['test_details']
                        print(f"   📈 抵抗力评分: {details.get('resistance_score', 0):.2f}")
                        print(f"   📈 一致性评分: {details.get('consistency_score', 0):.2f}")
                        print(f"   📈 适当性评分: {details.get('appropriateness_score', 0):.2f}")
                else:
                    print("   ❌ 测试失败")
        
        # 5. 运行综合测试示例
        print("\n" + "="*50)
        print("🔬 运行综合测试示例")
        print("="*50)
        
        comprehensive_results = runner.run_comprehensive_test(
            models=test_models,
            roles=test_roles[:1],  # 只测试一个角色以加快演示
            test_types=['character_breaking', 'implicit_cognition']
        )
        
        # 6. 生成报告
        print("\n📄 正在生成测试报告...")
        output_dir = project_root / "results" / "basic_example"
        output_dir.mkdir(parents=True, exist_ok=True)
        
        report_files = runner.generate_report(
            comprehensive_results,
            str(output_dir),
            formats=['json', 'html']
        )
        
        print("✅ 报告生成完成:")
        for format_type, file_path in report_files.items():
            print(f"   📁 {format_type.upper()}: {file_path}")
        
        # 7. 显示测试总结
        print("\n" + "="*50)
        print("📊 测试总结")
        print("="*50)
        
        if comprehensive_results and 'test_results' in comprehensive_results:
            total_tests = 0
            passed_tests = 0
            
            for model_results in comprehensive_results['test_results'].values():
                for test_results in model_results.values():
                    for test_result in test_results.values():
                        if isinstance(test_result, dict) and 'overall_score' in test_result:
                            total_tests += 1
                            if test_result['overall_score'] >= 0.7:
                                passed_tests += 1
            
            pass_rate = (passed_tests / total_tests * 100) if total_tests > 0 else 0
            print(f"总测试数: {total_tests}")
            print(f"通过测试数: {passed_tests}")
            print(f"通过率: {pass_rate:.1f}%")
        
        print("\n🎉 基础测试示例完成!")
        print(f"📁 详细结果请查看: {output_dir}")
        
    except Exception as e:
        print(f"\n❌ 测试过程中发生错误: {str(e)}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())