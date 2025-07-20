#!/usr/bin/env python3
"""
单独测试破功模块导入
"""

def test_breaking_stress_only():
    """只测试破功模块导入"""
    try:
        print("测试破功测试模块导入...")
        from independence.experiments.breaking_stress import BreakingStressTest
        print("✅ 破功测试模块导入成功")
        
        print("测试配置导入...")
        from config import INDEPENDENCE_CONFIG
        print("✅ 配置导入成功")
        
        print("创建破功测试实例...")
        breaking_test = BreakingStressTest(INDEPENDENCE_CONFIG)
        print("✅ 破功测试实例创建成功")
        
        print("测试方法存在性...")
        if hasattr(breaking_test, 'run_test'):
            print("✅ run_test 方法存在")
        if hasattr(breaking_test, 'run_experiment'):
            print("✅ run_experiment 方法存在")
        
        return True
        
    except Exception as e:
        print(f"❌ 错误: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_breaking_stress_only()
    if success:
        print("\n🎉 破功模块测试通过！")
    else:
        print("\n💥 破功模块测试失败！")