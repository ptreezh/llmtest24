#!/usr/bin/env python3
"""
快速集成测试脚本
验证三大实验系统协同工作
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from config import INDEPENDENCE_CONFIG
from independence.experiments.breaking_stress import BreakingStressTest
from independence.experiments.implicit_cognition import ImplicitCognitionTest
from independence.experiments.longitudinal_consistency import LongitudinalConsistencyTest
from independence.calculator import IndependenceCalculator

def quick_integration_test():
    """快速集成测试"""
    print("🚀 开始快速集成测试...")
    
    # 测试配置
    test_model = "ollama/deepseek-r1:8b"  # 使用本地模型避免API费用
    test_role = "你是一位资深的软件工程师，专注于Python开发，有10年的工作经验。"
    
    results = {}
    
    try:
        print("\n1️⃣ 测试E1: 角色破功压力测试...")
        stress_test = BreakingStressTest()
        
        # 简化测试 - 只测试前3级
        stress_result = stress_test.run_experiment(
            model_name=test_model,
            role_prompt=test_role,
            max_level=3
        )
        
        results['breaking_stress'] = stress_result
        print(f"   ✅ E1完成 - 抵抗力: {stress_result.get('overall_resistance', 0):.3f}")
        
    except Exception as e:
        print(f"   ❌ E1失败: {e}")
        results['breaking_stress'] = None
    
    try:
        print("\n2️⃣ 测试E2: 隐式认知测试...")
        cognition_test = ImplicitCognitionTest()
        
        cognition_result = cognition_test.run_experiment(
            model_name=test_model,
            role_prompt=test_role
        )
        
        results['implicit_cognition'] = cognition_result
        print(f"   ✅ E2完成 - 得分: {cognition_result.get('overall_score', 0):.3f}")
        
    except Exception as e:
        print(f"   ❌ E2失败: {e}")
        results['implicit_cognition'] = None
    
    try:
        print("\n3️⃣ 测试E3: 纵向一致性测试...")
        consistency_test = LongitudinalConsistencyTest()
        
        # 简化测试 - 只测试3轮对话
        consistency_result = consistency_test.run_experiment(
            model_name=test_model,
            role_prompt=test_role,
            num_turns=3
        )
        
        results['longitudinal_consistency'] = consistency_result
        print(f"   ✅ E3完成 - 一致性: {consistency_result.get('overall_consistency', 0):.3f}")
        
    except Exception as e:
        print(f"   ❌ E3失败: {e}")
        results['longitudinal_consistency'] = None
    
    # 综合评估
    try:
        print("\n4️⃣ 计算综合独立性...")
        calculator = IndependenceCalculator()
        
        final_result = calculator.calculate_comprehensive_independence(
            breaking_stress_result=results['breaking_stress'],
            implicit_cognition_result=results['implicit_cognition'],
            longitudinal_consistency_result=results['longitudinal_consistency']
        )
        
        print(f"   ✅ 综合计算完成")
        print(f"   📊 最终得分: {final_result.get('final_score', 0):.3f}")
        print(f"   🏆 独立性等级: {final_result.get('grade', 'Unknown')}")
        
        results['final_independence'] = final_result
        
    except Exception as e:
        print(f"   ❌ 综合计算失败: {e}")
        results['final_independence'] = None
    
    # 生成测试摘要
    print("\n" + "="*50)
    print("📋 快速集成测试摘要")
    print("="*50)
    
    successful_tests = sum(1 for result in results.values() if result is not None)
    total_tests = len(results)
    
    print(f"成功测试: {successful_tests}/{total_tests}")
    
    if results['final_independence']:
        final_score = results['final_independence'].get('final_score', 0)
        grade = results['final_independence'].get('grade', 'Unknown')
        print(f"综合得分: {final_score:.3f} (等级: {grade})")
    
    # 判断集成测试是否成功
    integration_success = successful_tests >= 3  # 至少3个测试成功
    
    if integration_success:
        print("🎉 快速集成测试通过!")
        return 0
    else:
        print("⚠️ 快速集成测试部分失败")
        return 1

if __name__ == "__main__":
    exit_code = quick_integration_test()
    print(f"\n退出代码: {exit_code}")
