#!/usr/bin/env python3
"""
测试所有独立性模块导入
"""

def test_all_modules():
    """测试所有独立性模块导入"""
    try:
        print("🔍 测试基础类导入...")
        from independence.base import IndependenceTestBase
        print("✅ 基础类导入成功")
        
        print("🔍 测试破功测试模块导入...")
        from independence.experiments.breaking_stress import BreakingStressTest
        print("✅ 破功测试模块导入成功")
        
        print("🔍 测试隐式认知模块导入...")
        from independence.experiments.implicit_cognition import ImplicitCognitionTest
        print("✅ 隐式认知模块导入成功")
        
        print("🔍 测试纵向一致性模块导入...")
        from independence.experiments.longitudinal_consistency import LongitudinalConsistencyTest
        print("✅ 纵向一致性模块导入成功")
        
        print("🔍 测试配置导入...")
        from config import INDEPENDENCE_CONFIG
        print("✅ 配置导入成功")
        
        print("🔍 创建所有测试实例...")
        breaking_test = BreakingStressTest(INDEPENDENCE_CONFIG)
        implicit_test = ImplicitCognitionTest(INDEPENDENCE_CONFIG)
        longitudinal_test = LongitudinalConsistencyTest(INDEPENDENCE_CONFIG)
        print("✅ 所有测试实例创建成功")
        
        print("🔍 验证方法存在性...")
        for test_name, test_instance in [
            ("破功测试", breaking_test),
            ("隐式认知测试", implicit_test),
            ("纵向一致性测试", longitudinal_test)
        ]:
            if hasattr(test_instance, 'run_experiment'):
                print(f"✅ {test_name} 具有 run_experiment 方法")
            else:
                print(f"❌ {test_name} 缺少 run_experiment 方法")
                
            if hasattr(test_instance, 'run_test'):
                print(f"✅ {test_name} 具有 run_test 方法")
            else:
                print(f"⚠️  {test_name} 缺少 run_test 方法")
        
        return True
        
    except Exception as e:
        print(f"❌ 错误: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_all_modules()
    if success:
        print("\n🎉 所有模块测试通过！")
        print("📝 三大实验系统已就绪：")
        print("   - E1: 破功压力测试 ✅")
        print("   - E2: 隐式认知测试 ✅") 
        print("   - E3: 纵向一致性测试 ✅")
    else:
        print("\n💥 模块测试失败！")