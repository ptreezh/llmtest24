#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
高级能力测试运行脚本
专门运行三个新增的高级能力测试：项目管理、并行任务优化、多学科分解
"""

import os
import sys
import subprocess
import time
from datetime import datetime

# 定义新增的高级能力测试脚本
ADVANCED_TEST_SCRIPTS = [
    "test_pillar_22_project_management.py",           # 强项目管理、分工协调、状态跟踪、最终集成能力
    "test_pillar_23_parallel_task_optimization.py",   # 复合任务分解为并行任务的能力
    "test_pillar_24_multidisciplinary_decomposition.py" # 复杂综合多学科任务分解能力
]

# 定义测试工作区的路径
TESTS_DIR = "tests"
TESTOUT_DIR = "testout"

def ensure_directories():
    """确保必要的目录存在"""
    os.makedirs(TESTOUT_DIR, exist_ok=True)
    print(f"✅ 确保输出目录存在: {TESTOUT_DIR}")

def run_single_test(script_name):
    """运行单个测试脚本"""
    script_path = os.path.join(TESTS_DIR, script_name)
    
    if not os.path.exists(script_path):
        print(f"❌ 测试脚本不存在: {script_path}")
        return False
    
    print(f"\n{'='*60}")
    print(f"🚀 运行测试: {script_name}")
    print(f"{'='*60}")
    
    try:
        start_time = time.time()
        
        # 运行测试脚本
        result = subprocess.run(
            [sys.executable, script_path],
            cwd=os.getcwd(),
            capture_output=True,
            text=True,
            encoding='utf-8'
        )
        
        end_time = time.time()
        duration = end_time - start_time
        
        if result.returncode == 0:
            print(f"✅ 测试成功完成 (耗时: {duration:.1f}秒)")
            print("📋 测试输出:")
            print(result.stdout)
            
            if result.stderr:
                print("⚠️ 警告信息:")
                print(result.stderr)
            
            return True
        else:
            print(f"❌ 测试失败 (返回码: {result.returncode})")
            print("错误输出:")
            print(result.stderr)
            if result.stdout:
                print("标准输出:")
                print(result.stdout)
            return False
            
    except Exception as e:
        print(f"❌ 运行测试时发生异常: {e}")
        return False

def display_test_info():
    """显示测试信息"""
    print("🎯 高级能力测试套件")
    print("="*60)
    print("本测试套件专门评估LLM在复杂项目管理和任务分解方面的高级能力")
    print()
    print("📋 测试内容:")
    print("1. Pillar 22 - 强项目管理、分工协调、状态跟踪、最终集成能力")
    print("   • ERP系统集成项目管理")
    print("   • 多地点建设项目协调")
    print("   • 产品发布全流程集成")
    print()
    print("2. Pillar 23 - 复合任务分解为并行任务的能力")
    print("   • 数据中心迁移并行任务分解")
    print("   • 软件平台开发并行优化")
    print("   • 制造业生产线并行建设")
    print()
    print("3. Pillar 24 - 复杂综合多学科任务分解能力")
    print("   • 智慧城市转型多学科分解")
    print("   • 气候变化应对多学科方案")
    print("   • 太空探索计划多学科设计")
    print()
    print("🎯 评估重点:")
    print("• 复杂项目的系统性分解能力")
    print("• 跨学科知识的整合应用能力")
    print("• 并行任务的优化调度能力")
    print("• 多团队协调的管理能力")
    print("• 状态跟踪和风险控制能力")
    print()

def display_results_summary():
    """显示结果摘要"""
    print("\n" + "="*60)
    print("📊 测试结果摘要")
    print("="*60)
    
    # 检查输出文件
    result_files = []
    for script in ADVANCED_TEST_SCRIPTS:
        test_name = script.replace("test_pillar_", "").replace(".py", "")
        result_file = f"{test_name}_test.json"
        result_path = os.path.join(TESTOUT_DIR, result_file)
        
        if os.path.exists(result_path):
            file_size = os.path.getsize(result_path)
            result_files.append((result_file, file_size))
            print(f"✅ {result_file} ({file_size} bytes)")
        else:
            print(f"❌ {result_file} (未生成)")
    
    print(f"\n📁 结果文件位置: {os.path.abspath(TESTOUT_DIR)}")
    print(f"📈 生成文件数量: {len(result_files)}/{len(ADVANCED_TEST_SCRIPTS)}")
    
    if len(result_files) == len(ADVANCED_TEST_SCRIPTS):
        print("🎉 所有测试均成功完成并生成结果文件！")
    else:
        print("⚠️ 部分测试未能成功完成，请检查错误信息")

def main():
    """主函数"""
    print("🤖 LLM高级能力测试系统")
    print(f"开始时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # 显示测试信息
    display_test_info()
    
    # 确保目录存在
    ensure_directories()
    
    # 询问是否继续
    try:
        response = input("是否开始运行高级能力测试? (y/N): ").strip().lower()
        if response not in ['y', 'yes', '是']:
            print("测试已取消")
            return
    except KeyboardInterrupt:
        print("\n测试已取消")
        return
    
    print(f"\n🚀 开始运行 {len(ADVANCED_TEST_SCRIPTS)} 个高级能力测试...")
    
    # 运行所有测试
    start_time = time.time()
    success_count = 0
    
    for i, script_name in enumerate(ADVANCED_TEST_SCRIPTS, 1):
        print(f"\n📍 进度: {i}/{len(ADVANCED_TEST_SCRIPTS)}")
        
        if run_single_test(script_name):
            success_count += 1
        
        # 测试间短暂延迟
        if i < len(ADVANCED_TEST_SCRIPTS):
            time.sleep(2)
    
    end_time = time.time()
    total_duration = end_time - start_time
    
    # 显示最终结果
    print(f"\n{'='*60}")
    print("🏁 测试完成")
    print(f"{'='*60}")
    print(f"⏱️  总耗时: {total_duration:.1f} 秒")
    print(f"✅ 成功: {success_count}/{len(ADVANCED_TEST_SCRIPTS)} 个测试")
    print(f"❌ 失败: {len(ADVANCED_TEST_SCRIPTS) - success_count}/{len(ADVANCED_TEST_SCRIPTS)} 个测试")
    
    # 显示结果摘要
    display_results_summary()
    
    # 给出建议
    print(f"\n💡 建议:")
    if success_count == len(ADVANCED_TEST_SCRIPTS):
        print("• 所有测试成功完成，可以查看详细结果进行分析")
        print("• 建议运行分析脚本对结果进行深入评估")
    else:
        print("• 检查失败的测试，确认模型配置和网络连接")
        print("• 可以单独重新运行失败的测试")
    
    print("• 查看testout目录中的JSON文件了解详细测试结果")
    print("• 可以修改config.py测试不同的模型")

if __name__ == "__main__":
    main()
