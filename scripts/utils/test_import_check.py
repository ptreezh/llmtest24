#!/usr/bin/env python3
"""
快速导入测试脚本
"""

def test_imports():
    """测试独立性模块导入"""
    try:
        print("测试基础模块导入...")
        from independence import BreakingStressTest, ImplicitCognitionTest, LongitudinalConsistencyTest
        print("✅ 基础模块导入成功")
        
        print("测试破功测试模块直接导入...")
        from independence.experiments.breaking_stress import BreakingStressTest
        print("✅ 破功测试模块导入成功")
        
        print("测试配置导入...")
        from config import INDEPENDENCE_CONFIG
        print("✅ 配置导入成功")
        
        print("创建测试实例...")
        breaking_test = BreakingStressTest(INDEPENDENCE_CONFIG)
        print("✅ 破功测试实例创建成功")
        
        print("测试方法存在性...")
        if hasattr(breaking_test, 'run_test'):
            print("✅ run_test 方法存在")
        else:
            print("❌ run_test 方法缺失")
            
        if hasattr(breaking_test, 'run_experiment'):
            print("✅ run_experiment 方法存在")
        else:
            print("❌ run_experiment 方法缺失")
        
        return True
        
    except ImportError as e:
        print(f"❌ 导入错误: {e}")
        import traceback
        traceback.print_exc()
        return False
    except Exception as e:
        print(f"❌ 其他错误: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_imports()
    if success:
        print("\n🎉 所有导入测试通过！")
    else:
        print("\n💥 导入测试失败！")
