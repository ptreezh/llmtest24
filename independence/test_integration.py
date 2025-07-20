#!/usr/bin/env python3
"""
角色独立性测试系统集成验证脚本

验证所有组件是否能正常协同工作
"""

import sys
import os
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

def test_module_imports():
    """测试模块导入"""
    print("🔍 测试模块导入...")
    
    try:
        from independence.base import IndependenceTestBase
        print("✅ independence.base 导入成功")
        
        from independence.experiments.breaking_stress import BreakingStressTest
        print("✅ independence.experiments.breaking_stress 导入成功")
        
        from independence.experiments.implicit_cognition import ImplicitCognitionTest
        print("✅ independence.experiments.implicit_cognition 导入成功")
        
        from independence.experiments.longitudinal_consistency import LongitudinalConsistencyTest
        print("✅ independence.experiments.longitudinal_consistency 导入成功")
        
        from independence.utils import call_llm_api, calculate_text_similarity
        print("✅ independence.utils 导入成功")
        
        return True
        
    except ImportError as e:
        print(f"❌ 模块导入失败: {e}")
        return False

def test_class_instantiation():
    """测试类实例化"""
    print("\n🔍 测试类实例化...")
    
    test_config = {
        'model_name': 'test_model',
        'output_dir': 'testout',
        'test_roles': ['software_engineer'],
        'stress_levels': ['low'],
        'conversation_length': 5,
        'memory_test_intervals': [3]
    }
    
    try:
        from independence.experiments.breaking_stress import BreakingStressTest
        from independence.experiments.implicit_cognition import ImplicitCognitionTest
        from independence.experiments.longitudinal_consistency import LongitudinalConsistencyTest
        
        # 创建测试实例
        breaking_test = BreakingStressTest(test_config)
        print("✅ BreakingStressTest 实例化成功")
        
        cognition_test = ImplicitCognitionTest(test_config)
        print("✅ ImplicitCognitionTest 实例化成功")
        
        consistency_test = LongitudinalConsistencyTest(test_config)
        print("✅ LongitudinalConsistencyTest 实例化成功")
        
        return True, [breaking_test, cognition_test, consistency_test]
        
    except Exception as e:
        print(f"❌ 类实例化失败: {e}")
        return False, []

def test_config_validation(test_instances):
    """测试配置验证"""
    print("\n🔍 测试配置验证...")
    
    try:
        for i, instance in enumerate(test_instances):
            class_name = instance.__class__.__name__
            if instance.validate_config():
                print(f"✅ {class_name} 配置验证通过")
            else:
                print(f"❌ {class_name} 配置验证失败")
                return False
        
        return True
        
    except Exception as e:
        print(f"❌ 配置验证异常: {e}")
        return False

def test_utility_functions():
    """测试工具函数"""
    print("\n🔍 测试工具函数...")
    
    try:
        from independence.utils import (
            calculate_text_similarity, 
            get_role_keywords,
            extract_professional_terms,
            analyze_response_style,
            detect_role_leakage
        )
        
        # 测试文本相似度计算
        similarity = calculate_text_similarity("这是一个测试", "这是另一个测试")
        print(f"✅ 文本相似度计算: {similarity:.3f}")
        
        # 测试角色关键词获取
        keywords = get_role_keywords('software_engineer')
        print(f"✅ 角色关键词获取: {len(keywords)} 个关键词")
        
        # 测试专业术语提取
        terms = extract_professional_terms("这是关于架构设计的讨论", keywords)
        print(f"✅ 专业术语提取: {len(terms)} 个术语")
        
        # 测试响应风格分析
        style = analyze_response_style(["这是第一个响应", "这是第二个响应"])
        print(f"✅ 响应风格分析: 一致性分数 {style['consistency_score']:.3f}")
        
        # 测试角色泄露检测
        leakage = detect_role_leakage("这是关于数据分析的讨论", 'software_engineer', ['data_scientist'])
        print(f"✅ 角色泄露检测: 泄露分数 {leakage['leakage_score']:.3f}")
        
        return True
        
    except Exception as e:
        print(f"❌ 工具函数测试失败: {e}")
        return False

def test_main_test_file():
    """测试主测试文件"""
    print("\n🔍 测试主测试文件...")
    
    try:
        from tests.test_pillar_25_independence import validate_test_integration
        
        if validate_test_integration():
            print("✅ 主测试文件集成验证通过")
            return True
        else:
            print("❌ 主测试文件集成验证失败")
            return False
            
    except Exception as e:
        print(f"❌ 主测试文件测试失败: {e}")
        return False

def main():
    """主验证函数"""
    print("🚀 角色独立性测试系统集成验证")
    print("=" * 50)
    
    # 测试步骤
    tests = [
        ("模块导入", test_module_imports),
        ("类实例化", test_class_instantiation),
        ("工具函数", test_utility_functions),
        ("主测试文件", test_main_test_file)
    ]
    
    test_instances = []
    all_passed = True
    
    for test_name, test_func in tests:
        print(f"\n📋 执行测试: {test_name}")
        
        if test_name == "类实例化":
            success, instances = test_func()
            if success:
                test_instances = instances
                # 继续配置验证测试
                print(f"\n📋 执行测试: 配置验证")
                if not test_config_validation(test_instances):
                    all_passed = False
            else:
                all_passed = False
        else:
            if not test_func():
                all_passed = False
    
    # 输出最终结果
    print(f"\n{'='*50}")
    if all_passed:
        print("🎉 所有集成测试通过！系统可以正常运行。")
        print("✅ 角色独立性测试系统已准备就绪")
        return 0
    else:
        print("❌ 部分测试失败，请检查错误信息并修复问题")
        return 1

if __name__ == "__main__":
    sys.exit(main())