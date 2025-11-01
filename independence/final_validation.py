#!/usr/bin/env python3
"""
角色独立性测试系统最终验证脚本

执行全面的系统验证，确保所有组件正常工作
"""

import sys
import os
from pathlib import Path
import json
import time

# 添加项目根目录到Python路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

def final_system_validation():
    """执行最终系统验证"""
    print("🚀 角色独立性测试系统 - 最终验证")
    print("=" * 60)
    
    validation_results = {
        'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
        'tests': {},
        'overall_status': 'UNKNOWN'
    }
    
    # 验证步骤列表
    validation_steps = [
        ("模块导入验证", test_imports),
        ("配置系统验证", test_configurations),
        ("核心组件验证", test_core_components),
        ("实验系统验证", test_experiment_systems),
        ("工具函数验证", test_utility_functions),
        ("集成测试验证", test_integration),
        ("运行脚本验证", test_run_scripts)
    ]
    
    passed_tests = 0
    total_tests = len(validation_steps)
    
    for step_name, test_func in validation_steps:
        print(f"\n📋 {step_name}...")
        try:
            result = test_func()
            validation_results['tests'][step_name] = {
                'status': 'PASS' if result else 'FAIL',
                'details': 'Test completed successfully' if result else 'Test failed'
            }
            
            if result:
                print(f"✅ {step_name} - 通过")
                passed_tests += 1
            else:
                print(f"❌ {step_name} - 失败")
                
        except Exception as e:
            print(f"💥 {step_name} - 异常: {e}")
            validation_results['tests'][step_name] = {
                'status': 'ERROR',
                'details': str(e)
            }
    
    # 计算总体状态
    success_rate = passed_tests / total_tests
    if success_rate >= 0.9:
        validation_results['overall_status'] = 'EXCELLENT'
        status_emoji = "🎉"
        status_desc = "优秀 - 系统完全就绪"
    elif success_rate >= 0.7:
        validation_results['overall_status'] = 'GOOD'
        status_emoji = "✅"
        status_desc = "良好 - 系统基本就绪"
    elif success_rate >= 0.5:
        validation_results['overall_status'] = 'FAIR'
        status_emoji = "⚠️"
        status_desc = "一般 - 系统部分就绪"
    else:
        validation_results['overall_status'] = 'POOR'
        status_emoji = "❌"
        status_desc = "较差 - 系统未就绪"
    
    # 输出最终结果
    print(f"\n{'='*60}")
    print(f"📊 最终验证结果")
    print(f"{'='*60}")
    print(f"通过测试: {passed_tests}/{total_tests}")
    print(f"成功率: {success_rate:.1%}")
    print(f"系统状态: {status_emoji} {status_desc}")
    
    # 保存验证结果
    try:
        output_file = project_root / 'testout' / 'final_validation_results.json'
        output_file.parent.mkdir(exist_ok=True)
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(validation_results, f, ensure_ascii=False, indent=2)
        
        print(f"📄 验证结果已保存到: {output_file}")
    except Exception as e:
        print(f"⚠️  保存验证结果失败: {e}")
    
    return success_rate >= 0.7

def test_imports():
    """测试模块导入"""
    try:
        from independence.base import IndependenceTestBase
        from independence.experiments import BreakingStressTest, ImplicitCognitionTest, LongitudinalConsistencyTest
        from independence.utils import call_llm_api, calculate_text_similarity
        from independence.config import get_test_config, ROLE_DEFINITIONS
        from independence.metrics import IndependenceCalculator
        from tests.test_pillar_25_independence import run_independence_test
        return True
    except ImportError:
        return False

def test_configurations():
    """测试配置系统"""
    try:
        from independence.config import get_test_config, validate_config, ROLE_DEFINITIONS
        from config.config import INDEPENDENCE_CONFIG
        
        # 测试默认配置
        default_config = get_test_config('default')
        if not validate_config(default_config):
            return False
        
        # 测试快速配置
        quick_config = get_test_config('quick')
        if not validate_config(quick_config):
            return False
        
        # 测试角色定义
        if len(ROLE_DEFINITIONS) < 4:
            return False
        
        return True
    except Exception:
        return False

def test_core_components():
    """测试核心组件"""
    try:
        from independence.base import IndependenceTestBase
        from independence.config import get_test_config
        
        # 创建基础测试实例
        config = get_test_config('quick')
        config['model_name'] = 'test_model'
        config['output_dir'] = 'testout'
        
        base_test = IndependenceTestBase(config)
        
        # 验证配置
        if not base_test.validate_config():
            return False
        
        # 验证基础方法存在
        required_methods = ['setup_test', 'run_experiment', 'analyze_results', 'generate_report']
        for method in required_methods:
            if not hasattr(base_test, method):
                return False
        
        return True
    except Exception:
        return False

def test_experiment_systems():
    """测试实验系统"""
    try:
        from independence.experiments import BreakingStressTest, ImplicitCognitionTest, LongitudinalConsistencyTest
        from independence.config import get_test_config
        
        config = get_test_config('quick')
        config['model_name'] = 'test_model'
        config['output_dir'] = 'testout'
        
        # 创建实验实例
        experiments = [
            BreakingStressTest(config),
            ImplicitCognitionTest(config),
            LongitudinalConsistencyTest(config)
        ]
        
        # 验证所有实验都能正确初始化和配置验证
        for exp in experiments:
            if not exp.validate_config():
                return False
        
        return True
    except Exception:
        return False

def test_utility_functions():
    """测试工具函数"""
    try:
        from independence.utils import (
            calculate_text_similarity,
            get_role_keywords,
            extract_professional_terms,
            analyze_response_style,
            detect_role_leakage,
            evaluate_role_consistency
        )
        
        # 测试文本相似度
        sim = calculate_text_similarity("测试文本1", "测试文本2")
        if not (0 <= sim <= 1):
            return False
        
        # 测试角色关键词
        keywords = get_role_keywords('software_engineer')
        if not keywords or len(keywords) < 5:
            return False
        
        # 测试专业术语提取
        terms = extract_professional_terms("这是关于架构设计的讨论", keywords)
        if terms is None:
            return False
        
        # 测试响应风格分析
        style = analyze_response_style(["响应1", "响应2"])
        if 'consistency_score' not in style:
            return False
        
        # 测试角色泄露检测
        leakage = detect_role_leakage("测试响应", 'software_engineer', ['data_scientist'])
        if 'leakage_score' not in leakage:
            return False
        
        # 测试角色一致性评估
        consistency = evaluate_role_consistency(["响应1", "响应2"], 'software_engineer')
        if 'consistency_score' not in consistency:
            return False
        
        return True
    except Exception:
        return False

def test_integration():
    """测试集成功能"""
    try:
        from tests.test_pillar_25_independence import validate_test_integration
        return validate_test_integration()
    except Exception:
        return False

def test_run_scripts():
    """测试运行脚本"""
    try:
        # 检查运行脚本文件是否存在
        run_script = project_root / 'run_pillar_25_independence.py'
        if not run_script.exists():
            return False
        
        # 尝试导入运行脚本的主要函数
        sys.path.insert(0, str(project_root))
        from run_pillar_25_independence import main
        
        return True
    except Exception:
        return False

if __name__ == "__main__":
    success = final_system_validation()
    
    if success:
        print(f"\n🎉 角色独立性测试系统验证完成！")
        print(f"✅ 系统已准备就绪，可以开始测试")
        print(f"\n🚀 使用方法:")
        print(f"  python run_pillar_25_independence.py")
        print(f"  python run_pillar_25_independence.py --quick")
        print(f"  python run_pillar_25_independence.py --validate-only")
        sys.exit(0)
    else:
        print(f"\n❌ 系统验证未完全通过")
        print(f"🔧 请检查错误信息并修复问题后重新验证")
        sys.exit(1)
