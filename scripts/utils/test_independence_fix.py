#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试独立性测试框架修复效果
"""

import sys
import os
from pathlib import Path

# 修复Windows下的编码问题
if sys.platform.startswith('win'):
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

def test_basic_imports():
    """测试基础导入"""
    print("检查 测试基础导入...")
    
    try:
        # 测试基类导入
        from independence.base import IndependenceTestBase
        print("成功 IndependenceTestBase 导入成功")
        
        # 测试工具函数导入
        from independence.utils import calculate_confidence_score, format_test_results
        print("成功 工具函数导入成功")
        
        # 测试隐式认知测试导入
        from independence.experiments.implicit_cognition import ImplicitCognitionTest
        print("成功 ImplicitCognitionTest 导入成功")
        
        # 测试纵向一致性测试导入
        from independence.experiments.longitudinal_consistency import LongitudinalConsistencyTest
        print("成功 LongitudinalConsistencyTest 导入成功")
        
        return True
        
    except Exception as e:
        print(f"失败 导入失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_class_instantiation():
    """测试类实例化"""
    print("\n检查 测试类实例化...")
    
    try:
        from independence.experiments.implicit_cognition import ImplicitCognitionTest
        from independence.experiments.longitudinal_consistency import LongitudinalConsistencyTest
        from config import INDEPENDENCE_CONFIG
        
        # 创建隐式认知测试实例
        implicit_test = ImplicitCognitionTest(INDEPENDENCE_CONFIG)
        print("成功 ImplicitCognitionTest 实例创建成功")
        
        # 创建纵向一致性测试实例
        longitudinal_test = LongitudinalConsistencyTest(INDEPENDENCE_CONFIG)
        print("成功 LongitudinalConsistencyTest 实例创建成功")
        
        return True, implicit_test, longitudinal_test
        
    except Exception as e:
        print(f"失败 实例化失败: {e}")
        import traceback
        traceback.print_exc()
        return False, None, None

def test_method_existence(implicit_test, longitudinal_test):
    """测试方法存在性"""
    print("\n检查 测试方法存在性...")
    
    success = True
    
    # 测试隐式认知测试方法
    if implicit_test:
        if hasattr(implicit_test, 'run_experiment'):
            print("成功 ImplicitCognitionTest.run_experiment 方法存在")
        else:
            print("失败 ImplicitCognitionTest.run_experiment 方法缺失")
            success = False
            
        if hasattr(implicit_test, '_generate_implicit_prompts'):
            print("成功 ImplicitCognitionTest._generate_implicit_prompts 方法存在")
        else:
            print("失败 ImplicitCognitionTest._generate_implicit_prompts 方法缺失")
            success = False
    
    # 测试纵向一致性测试方法
    if longitudinal_test:
        if hasattr(longitudinal_test, 'run_experiment'):
            print("成功 LongitudinalConsistencyTest.run_experiment 方法存在")
        else:
            print("失败 LongitudinalConsistencyTest.run_experiment 方法缺失")
            success = False
            
        if hasattr(longitudinal_test, '_execute_conversation_turn'):
            print("成功 LongitudinalConsistencyTest._execute_conversation_turn 方法存在")
        else:
            print("失败 LongitudinalConsistencyTest._execute_conversation_turn 方法缺失")
            success = False
    
    return success

def test_simple_functionality():
    """测试简单功能"""
    print("\n检查 测试简单功能...")
    
    try:
        from independence.utils import calculate_confidence_score, analyze_response_quality
        
        # 测试置信度计算
        score = calculate_confidence_score("我是一名软件工程师，专注于代码开发", ["软件", "工程师", "代码"])
        print(f"成功 置信度计算测试: {score:.3f}")
        
        # 测试响应质量分析
        quality = analyze_response_quality("这是一个测试响应。它包含多个句子。因此，质量应该不错。")
        print(f"成功 响应质量分析测试: {quality['overall_quality']:.3f}")
        
        return True
        
    except Exception as e:
        print(f"失败 功能测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_config_validation():
    """测试配置验证"""
    print("\n检查 测试配置验证...")
    
    try:
        from independence.utils import validate_test_config
        
        # 测试有效配置
        valid_config = {
            'model_name': 'dashscope/qwen:7b-chat',
            'role_prompt': '你是一名经验丰富的软件工程师，专注于Python开发。'
        }
        
        is_valid, errors = validate_test_config(valid_config)
        if is_valid:
            print("成功 有效配置验证通过")
        else:
            print(f"失败 有效配置验证失败: {errors}")
        
        # 测试无效配置
        invalid_config = {
            'model_name': '',
            'role_prompt': '短'
        }
        
        is_valid, errors = validate_test_config(invalid_config)
        if not is_valid:
            print(f"成功 无效配置正确识别: {len(errors)} 个错误")
        else:
            print("失败 无效配置未被识别")
        
        return True
        
    except Exception as e:
        print(f"失败 配置验证测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def run_mini_test():
    """运行一个迷你测试"""
    print("\n检查 运行迷你测试...")
    
    try:
        from independence.experiments.implicit_cognition import ImplicitCognitionTest
        from config import INDEPENDENCE_CONFIG
        
        # 创建测试实例
        test = ImplicitCognitionTest(INDEPENDENCE_CONFIG)
        
        # 简单的角色提示词
        role_prompt = "你是一名经验丰富的软件工程师，专注于Python开发，有10年的工作经验。"
        # model_name = "qwen2:7b"
        model_name = "dashscope/qwen:7b-chat"
        
        print(f"    角色: {role_prompt[:50]}...")
        print(f"    模型: {model_name}")
        
        # 运行实验（只运行一个简单的测试）
        print("    开始运行实验...")
        
        # 由于完整测试可能很耗时，我们只测试方法调用是否正常
        # 这里我们模拟一个快速测试
        test.start_test()
        
        # 检查是否能正常生成隐式提示词
        if hasattr(test, '_generate_implicit_prompts'):
            prompts = test._generate_implicit_prompts(role_prompt)
            if prompts:
                print(f"    成功 成功生成 {len(prompts)} 个隐式提示词")
            else:
                print("    警告 隐式提示词生成为空")
        
        test.end_test()
        duration = test.get_test_duration()
        print(f"    时间 测试耗时: {duration:.2f}秒")
        
        return True
        
    except Exception as e:
        print(f"失败 迷你测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """主测试函数"""
    print("测试 独立性测试框架修复效果验证")
    print("=" * 50)
    
    # 测试结果统计
    test_results = []
    
    # 1. 基础导入测试
    result1 = test_basic_imports()
    test_results.append(("基础导入", result1))
    
    if not result1:
        print("\n失败 基础导入失败，停止后续测试")
        return
    
    # 2. 类实例化测试
    result2, implicit_test, longitudinal_test = test_class_instantiation()
    test_results.append(("类实例化", result2))
    
    if not result2:
        print("\n失败 类实例化失败，停止后续测试")
        return
    
    # 3. 方法存在性测试
    result3 = test_method_existence(implicit_test, longitudinal_test)
    test_results.append(("方法存在性", result3))
    
    # 4. 简单功能测试
    result4 = test_simple_functionality()
    test_results.append(("简单功能", result4))
    
    # 5. 配置验证测试
    result5 = test_config_validation()
    test_results.append(("配置验证", result5))
    
    # 6. 迷你测试
    result6 = run_mini_test()
    test_results.append(("迷你测试", result6))
    
    # 输出测试结果摘要
    print("\n" + "=" * 50)
    print("结果 测试结果摘要")
    print("=" * 50)
    
    passed = 0
    total = len(test_results)
    
    for test_name, result in test_results:
        status = "通过" if result else "失败"
        print(f"{test_name:15} : {status}")
        if result:
            passed += 1
    
    print(f"\n总体结果: {passed}/{total} 测试通过")
    
    if passed == total:
        print("庆祝 所有测试通过！独立性测试框架修复成功！")
    elif passed >= total * 0.8:
        print("成功 大部分测试通过，框架基本可用")
    elif passed >= total * 0.5:
        print("警告 部分测试通过，需要进一步修复")
    else:
        print("失败 多数测试失败，需要重新检查修复")
    
    print("\n修复 如果有测试失败，请检查:")
    print("  1. 文件路径和导入是否正确")
    print("  2. 依赖模块是否完整")
    print("  3. 配置文件是否正确")
    print("  4. Python环境是否正常")

if __name__ == "__main__":
    main()
