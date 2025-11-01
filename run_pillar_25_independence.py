#!/usr/bin/env python3
"""
Pillar 25: 角色独立性测试运行脚本

用于启动角色独立性综合测试的主入口脚本。
"""

import sys
import os
import argparse
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def run_independence_test(quick_mode: bool = False, validate_only: bool = False):
    """
    运行角色独立性测试
    
    Args:
        quick_mode: 是否使用快速测试模式
        validate_only: 是否只进行验证而不运行完整测试
    """
    try:
        from tests.test_pillar_25_independence import TestPillar25Independence
        import unittest
        
        # 创建测试套件
        loader = unittest.TestLoader()
        if quick_mode:
            # 快速测试只运行前两个测试
            suite = loader.loadTestsFromTestCase(TestPillar25Independence)
            # 这里可以添加逻辑来过滤测试，但为了简单起见，我们假设TestPillar25Independence类已经处理了快速模式
        else:
            suite = loader.loadTestsFromTestCase(TestPillar25Independence)
        
        # 运行测试
        runner = unittest.TextTestRunner(verbosity=2)
        result = runner.run(suite)
        
        # 返回测试结果
        return result.wasSuccessful()
        
    except ImportError as e:
        print(f"❌ 无法导入测试模块: {e}")
        return False
    except Exception as e:
        print(f"❌ 运行测试时发生错误: {e}")
        return False

def main():
    """主函数"""
    parser = argparse.ArgumentParser(description='Pillar 25: 角色独立性测试')
    parser.add_argument('--quick', action='store_true', help='使用快速测试模式')
    parser.add_argument('--validate-only', action='store_true', help='只进行验证，不运行完整测试')
    
    args = parser.parse_args()
    
    print("🚀 开始执行角色独立性测试...")
    print(f"模式: {'快速' if args.quick else '完整'}")
    
    success = run_independence_test(quick_mode=args.quick, validate_only=args.validate_only)
    
    if success:
        print("\n🎉 角色独立性测试执行完成！")
        print("✅ 所有测试通过")
        sys.exit(0)
    else:
        print("\n❌ 角色独立性测试未完全通过")
        print("🔧 请检查错误信息并修复问题")
        sys.exit(1)

if __name__ == "__main__":
    main()
