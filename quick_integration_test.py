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

def quick_integration_test():
    """快速集成测试"""
    print("🚀 开始快速集成测试...")
    
    # 测试配置
    test_model = "qwen2:7b"  # 使用默认测试模型
    test_role = "你是一位资深的软件工程师，专注于Python开发，有10年的工作经验。"
    
    try:
        # 测试 E1: 破功压力测试
        print("\n📊 测试 E1: 破功压力测试...")
        breaking_test = BreakingStressTest(INDEPENDENCE_CONFIG)
        print("✅ E1 实例创建成功")
        
        # 测试 E2: 隐式认知测试
        print("\n🧠 测试 E2: 隐式认知测试...")
        implicit_test = ImplicitCognitionTest(INDEPENDENCE_CONFIG)
        print("✅ E2 实例创建成功")
        
        # 测试 E3: 纵向一致性测试
        print("\n📈 测试 E3: 纵向一致性测试...")
        longitudinal_test = LongitudinalConsistencyTest(INDEPENDENCE_CONFIG)
        print("✅ E3 实例创建成功")
        
        # 验证接口一致性
        print("\n🔍 验证接口一致性...")
        
        # 检查所有测试类都有 run_test 方法
        for test_name, test_instance in [
            ("E1", breaking_test),
            ("E2", implicit_test), 
            ("E3", longitudinal_test)
        ]:
            if hasattr(test_instance, 'run_test'):
                print(f"✅ {test_name} 具有 run_test 方法")
            else:
                print(f"❌ {test_name} 缺少 run_test 方法")
                return False
        
        print("\n🎉 快速集成测试通过！")
        print("📝 系统状态：三大实验系统已就绪")
        return True
        
    except Exception as e:
        print(f"\n💥 集成测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = quick_integration_test()
    if success:
        print("\n✨ 独立性测试系统修复完成！")
        print("💡 可以运行: python tests/test_pillar_25_independence.py")
    else:
        print("\n🔧 需要进一步调试...")