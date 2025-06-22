#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
安全的测试运行器
处理编码问题和异常情况
"""

import os
import sys
import subprocess
import traceback
from datetime import datetime

def run_test_safely(script_path):
    """安全地运行单个测试脚本"""
    print(f"\n{'='*60}")
    print(f"运行测试: {os.path.basename(script_path)}")
    print(f"{'='*60}")
    
    try:
        # 使用subprocess运行测试，处理编码问题
        result = subprocess.run(
            [sys.executable, script_path],
            capture_output=True,
            text=True,
            encoding='utf-8',
            errors='replace',  # 关键：处理编码错误
            timeout=300  # 5分钟超时
        )
        
        # 打印输出
        if result.stdout:
            print("STDOUT:")
            print(result.stdout)
        
        if result.stderr:
            print("STDERR:")
            print(result.stderr)
        
        if result.returncode != 0:
            print(f"⚠️ 测试返回非零退出码: {result.returncode}")
        else:
            print("✅ 测试完成")
            
        return result.returncode == 0
        
    except subprocess.TimeoutExpired:
        print("❌ 测试超时")
        return False
    except Exception as e:
        print(f"❌ 运行测试时出错: {e}")
        traceback.print_exc()
        return False

def main():
    tests_dir = "tests"
    test_scripts = [
        "test_pillar_09_creativity.py",
        "test_pillar_10_math.py",
        "test_pillar_11_safety.py",
        "test_pillar_12_persona.py",
        "test_pillar_13_init.py",
        "test_pillar_14_persona_depth.py",
        "test_pillar_15_collaboration.py",
        "test_pillar_16_emergence.py",
        "test_pillar_17_dag_generation.py",
        "test_pillar_18_fault_tolerance.py",
        "test_pillar_19_network_analysis.py",
    ]
    
    print(f"开始安全测试运行 - {datetime.now()}")
    
    success_count = 0
    total_count = len(test_scripts)
    
    for script_name in test_scripts:
        script_path = os.path.join(tests_dir, script_name)
        if os.path.exists(script_path):
            if run_test_safely(script_path):
                success_count += 1
        else:
            print(f"⚠️ 测试脚本不存在: {script_path}")
    
    print(f"\n{'='*60}")
    print(f"测试完成: {success_count}/{total_count} 成功")
    print(f"结束时间: {datetime.now()}")
    print(f"{'='*60}")

if __name__ == "__main__":
    main()
