#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
动态角色切换与记忆管理测试运行脚本
专门用于测试模型的角色轮流切换、外部记忆文件管理和状态连续性能力
"""

import sys
import os
import subprocess
import time
from datetime import datetime

# 添加测试目录到路径
sys.path.append(os.path.join(os.path.dirname(__file__), 'tests'))

def run_dynamic_role_switching_test():
    """运行动态角色切换测试"""
    print("=" * 60)
    print("🎭 动态角色切换与外部记忆管理测试")
    print("=" * 60)
    print(f"开始时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # 检查测试文件是否存在
    test_file = os.path.join(os.path.dirname(__file__), 'tests', 'test_pillar_21_dynamic_role_switching.py')
    if not os.path.exists(test_file):
        print(f"❌ 测试文件不存在: {test_file}")
        return False
    
    try:
        # 运行测试
        print("🔄 正在执行动态角色切换测试...")
        print("   这个测试将模拟角色轮流切换和记忆管理...")
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
    
    analysis_file = os.path.join(os.path.dirname(__file__), 'analyze_dynamic_role_switching.py')
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
    
    # 检查并创建必要目录
    dirs_to_check = ['testout', 'role_memories', 'role_prompts']
    for dir_name in dirs_to_check:
        dir_path = os.path.join(os.path.dirname(__file__), dir_name)
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
            print(f"✅ 创建目录: {dir_path}")
        else:
            print(f"✅ 目录已存在: {dir_name}")
    
    return True

def display_test_info():
    """显示测试信息"""
    print("📋 测试信息:")
    print("   测试名称: 动态角色切换与外部记忆管理")
    print("   测试目标: 评估模型在角色轮流切换和状态连续性维护方面的能力")
    print()
    print("🎭 测试角色:")
    print("   - 侦探李明: 经验丰富，善于观察，专注案件调查")
    print("   - 王医生: 温和耐心，专业严谨，关注患者健康")
    print("   - 张老师: 热爱教育，善于启发，专注教学质量")
    print()
    print("🔄 测试流程:")
    print("   1. 角色切换序列测试 (6次切换)")
    print("   2. 记忆持续性测试 (跨角色记忆保持)")
    print("   3. 注意力焦点维护测试 (专业领域专注)")
    print()
    print("🎯 评估维度:")
    print("   - 角色切换的准确性和及时性")
    print("   - 外部记忆文件的读取和更新")
    print("   - 角色状态的连续性维护")
    print("   - 多源信息的整合能力")
    print("   - 注意力焦点的专业性保持")
    print()

def display_results_info():
    """显示结果文件信息"""
    print("📁 测试结果文件:")
    
    testout_dir = os.path.join(os.path.dirname(__file__), 'testout')
    role_memories_dir = os.path.join(os.path.dirname(__file__), 'role_memories')
    role_prompts_dir = os.path.join(os.path.dirname(__file__), 'role_prompts')
    
    print(f"   测试输出目录: {testout_dir}")
    print("   - dynamic_role_switching_test.json (详细测试结果)")
    print("   - dynamic_role_switching_analysis.json (分析报告)")
    print()
    print(f"   角色记忆目录: {role_memories_dir}")
    print("   - detective_memory.json (侦探记忆文件)")
    print("   - doctor_memory.json (医生记忆文件)")
    print("   - teacher_memory.json (老师记忆文件)")
    print()
    print(f"   角色提示词目录: {role_prompts_dir}")
    print("   - detective_prompt.txt (侦探角色设定)")
    print("   - doctor_prompt.txt (医生角色设定)")
    print("   - teacher_prompt.txt (老师角色设定)")

def main():
    """主函数"""
    print("🤖 动态角色切换与记忆管理测试系统")
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
    test_success = run_dynamic_role_switching_test()
    
    if test_success:
        # 运行分析
        analysis_success = run_analysis()
        
        if analysis_success:
            print("\n" + "=" * 60)
            print("🎉 动态角色切换测试完成!")
            print("=" * 60)
            
            # 显示结果文件位置
            display_results_info()
            
        else:
            print("\n⚠️  测试完成但分析失败")
    else:
        print("\n❌ 测试失败")
    
    end_time = time.time()
    duration = end_time - start_time
    print(f"\n⏱️  总耗时: {duration:.1f} 秒")
    
    print("\n💡 提示:")
    print("   - 查看JSON文件了解详细的测试结果和分析")
    print("   - 检查role_memories目录中的记忆文件更新情况")
    print("   - 可以修改config.py中的MODEL_TO_TEST测试不同模型")
    print("   - 可以编辑role_prompts中的角色设定进行自定义测试")

if __name__ == "__main__":
    main()
