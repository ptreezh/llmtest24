#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
海量角色共识测试运行脚本
专门用于测试大规模角色协作、投票机制和区块链共识能力
"""

import sys
import os
import subprocess
import time
from datetime import datetime

# 添加测试目录到路径
sys.path.append(os.path.join(os.path.dirname(__file__), 'tests'))

def run_massive_consensus_test():
    """运行海量角色共识测试"""
    print("=" * 60)
    print("🚀 海量角色协同编辑与区块链共识测试")
    print("=" * 60)
    print(f"开始时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # 检查测试文件是否存在
    test_file = os.path.join(os.path.dirname(__file__), 'tests', 'test_pillar_20_massive_consensus.py')
    if not os.path.exists(test_file):
        print(f"❌ 测试文件不存在: {test_file}")
        return False
    
    try:
        # 运行测试
        print("🔄 正在执行海量角色共识测试...")
        print("   这可能需要几分钟时间，请耐心等待...")
        print()
        
        # 执行测试脚本
        result = subprocess.run(
            [sys.executable, test_file],
            cwd=os.path.dirname(__file__),
            capture_output=True,
            text=True,
            encoding='utf-8'
        )
        
        if result.returncode == 0:
            print("✅ 测试执行成功!")
            print("\n📋 测试输出:")
            print("-" * 40)
            print(result.stdout)
            if result.stderr:
                print("\n⚠️  警告信息:")
                print(result.stderr)
        else:
            print("❌ 测试执行失败!")
            print(f"返回码: {result.returncode}")
            print("\n错误输出:")
            print(result.stderr)
            if result.stdout:
                print("\n标准输出:")
                print(result.stdout)
            return False
            
    except Exception as e:
        print(f"❌ 执行测试时发生异常: {e}")
        return False
    
    return True

def run_analysis():
    """运行结果分析"""
    print("\n" + "=" * 60)
    print("📊 开始分析测试结果")
    print("=" * 60)
    
    analysis_file = os.path.join(os.path.dirname(__file__), 'analyze_massive_consensus.py')
    if not os.path.exists(analysis_file):
        print(f"❌ 分析脚本不存在: {analysis_file}")
        return False
    
    try:
        print("🔄 正在分析测试结果...")
        
        result = subprocess.run(
            [sys.executable, analysis_file],
            cwd=os.path.dirname(__file__),
            capture_output=True,
            text=True,
            encoding='utf-8'
        )
        
        if result.returncode == 0:
            print("✅ 分析完成!")
            print("\n📈 分析结果:")
            print("-" * 40)
            print(result.stdout)
            if result.stderr:
                print("\n⚠️  警告信息:")
                print(result.stderr)
        else:
            print("❌ 分析失败!")
            print(f"返回码: {result.returncode}")
            print("\n错误输出:")
            print(result.stderr)
            return False
            
    except Exception as e:
        print(f"❌ 分析时发生异常: {e}")
        return False
    
    return True

def check_prerequisites():
    """检查运行前提条件"""
    print("🔍 检查运行环境...")
    
    # 检查config.py
    config_file = os.path.join(os.path.dirname(__file__), 'config.py')
    if not os.path.exists(config_file):
        print("❌ 缺少config.py文件")
        return False
    
    # 检查ollama模块
    try:
        import ollama
        print("✅ ollama模块已安装")
    except ImportError:
        print("❌ 缺少ollama模块，请运行: pip install ollama")
        return False
    
    # 检查testout目录
    testout_dir = os.path.join(os.path.dirname(__file__), 'testout')
    if not os.path.exists(testout_dir):
        os.makedirs(testout_dir)
        print(f"✅ 创建输出目录: {testout_dir}")
    else:
        print("✅ 输出目录已存在")
    
    return True

def display_test_info():
    """显示测试信息"""
    print("📋 测试信息:")
    print("   测试名称: 海量角色协同编辑与区块链共识")
    print("   测试目标: 评估大规模角色协作、投票机制和共识算法能力")
    print("   测试用例:")
    print("     - 用例1: 20个角色 + 多数决投票 (人工智能伦理)")
    print("     - 用例2: 50个角色 + 权威加权投票 (量子计算)")
    print("     - 用例3: 100个角色 + 拜占庭容错共识 (元宇宙技术)")
    print()
    print("🎯 评估维度:")
    print("   - 角色生成与管理能力")
    print("   - 协同编辑协调能力")
    print("   - 投票机制理解与实现")
    print("   - 区块链共识算法应用")
    print("   - 大规模状态管理能力")
    print()

def main():
    """主函数"""
    print("🤖 海量角色共识测试系统")
    print("=" * 60)
    
    # 显示测试信息
    display_test_info()
    
    # 检查前提条件
    if not check_prerequisites():
        print("\n❌ 环境检查失败，请解决上述问题后重试")
        return
    
    print("✅ 环境检查通过")
    print()
    
    # 询问是否继续
    try:
        response = input("是否开始测试? (y/N): ").strip().lower()
        if response not in ['y', 'yes', '是']:
            print("测试已取消")
            return
    except KeyboardInterrupt:
        print("\n测试已取消")
        return
    
    start_time = time.time()
    
    # 运行测试
    test_success = run_massive_consensus_test()
    
    if test_success:
        # 运行分析
        analysis_success = run_analysis()
        
        if analysis_success:
            print("\n" + "=" * 60)
            print("🎉 海量角色共识测试完成!")
            print("=" * 60)
            
            # 显示结果文件位置
            testout_dir = os.path.join(os.path.dirname(__file__), 'testout')
            print(f"📁 测试结果保存在: {testout_dir}")
            print("   - massive_consensus_case1.json (20角色测试)")
            print("   - massive_consensus_case2.json (50角色测试)")
            print("   - massive_consensus_case3.json (100角色测试)")
            print("   - massive_consensus_analysis.json (分析报告)")
            
        else:
            print("\n⚠️  测试完成但分析失败")
    else:
        print("\n❌ 测试失败")
    
    end_time = time.time()
    duration = end_time - start_time
    print(f"\n⏱️  总耗时: {duration:.1f} 秒")
    
    print("\n💡 提示:")
    print("   - 可以查看JSON文件了解详细结果")
    print("   - 可以修改config.py中的MODEL_TO_TEST测试不同模型")
    print("   - 可以调整测试参数进行更深入的评估")

if __name__ == "__main__":
    main()
