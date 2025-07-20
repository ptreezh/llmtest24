#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
增强版LLM测试运行脚本
确保所有测试结果都被保存到文件，便于后续分析
"""

import os
import sys
import subprocess
import shutil
from datetime import datetime
import ollama

# 定义测试脚本的顺序
TEST_SCRIPTS = [
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

# 定义测试工作区的路径
TESTS_DIR = "tests"
WORKSPACE_DIR = os.path.join(TESTS_DIR, "test_workspace")
TESTOUT_DIR = "testout"

def ensure_output_saved():
    """确保所有测试脚本都保存输出到文件"""
    
    # 检查并修改测试脚本，确保它们保存输出
    scripts_to_modify = [
        "test_pillar_18_fault_tolerance.py",
        "test_pillar_19_network_analysis.py"
    ]
    
    for script_name in scripts_to_modify:
        script_path = os.path.join(TESTS_DIR, script_name)
        if not os.path.exists(script_path):
            continue
            
        # 读取脚本内容
        with open(script_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 检查是否已经有输出保存逻辑
        if 'testout' in content and 'with open' in content:
            continue  # 已经有保存逻辑
            
        # 添加输出保存逻辑
        if script_name == "test_pillar_18_fault_tolerance.py":
            pillar_name = "fault_tolerance"
        elif script_name == "test_pillar_19_network_analysis.py":
            pillar_name = "network_analysis"
        else:
            continue
            
        # 在脚本中添加保存逻辑
        new_content = content.replace(
            'import ollama\nimport sys\nimport os',
            f'''import ollama
import sys
import os

TESTOUT_DIR = os.path.join(os.path.dirname(__file__), '..', 'testout')
os.makedirs(TESTOUT_DIR, exist_ok=True)'''
        )
        
        # 修改run_test函数以保存输出
        new_content = new_content.replace(
            'print("MODEL RESPONSE:")\n        print(response[\'message\'][\'content\'])',
            f'''print("MODEL RESPONSE:")
        model_response = response['message']['content']
        print(model_response)
        
        # 保存结果到文件
        output_path = os.path.join(TESTOUT_DIR, "{pillar_name}_case1.txt")
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(f"用例编号: case1\\n类型: {pillar_name}\\nPROMPT:\\n{{prompt.strip()}}\\n\\nMODEL RESPONSE:\\n")
            f.write(model_response)
        print(f"Saved result to {{output_path}}")'''
        )
        
        # 写回文件
        with open(script_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        print(f"已更新 {script_name} 以保存输出")

def run_single_test_with_output_capture(script_name):
    """运行单个测试并捕获输出"""
    script_path = os.path.join(TESTS_DIR, script_name)
    
    if not os.path.exists(script_path):
        print(f"\n警告: 找不到测试脚本 {script_path}，已跳过。")
        return
    
    print(f"\n{'='*60}")
    print(f"运行测试: {script_name}")
    print(f"{'='*60}")
    
    try:
        # 运行测试脚本
        result = subprocess.run(
            [sys.executable, script_path], 
            capture_output=True,
            text=True, 
            encoding='utf-8',
            errors='replace',
            cwd=os.getcwd()
        )
        
        # 打印输出
        if result.stdout:
            print(result.stdout)
        if result.stderr:
            print("STDERR:", result.stderr)
            
        if result.returncode != 0:
            print(f"警告: {script_name} 返回非零退出码: {result.returncode}")
            
    except Exception as e:
        print(f"运行 {script_name} 时发生错误: {e}")

def main():
    print("=" * 80)
    print(f"启动LLM高级能力测评套件 (Pillars 9-19) - 增强版")
    print(f"开始时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 80)
    
    # 检查配置
    try:
        from config import MODEL_TO_TEST
        print(f"配置加载成功。待测模型: {MODEL_TO_TEST}\n")
    except ImportError:
        print("错误: 找不到 config.py 文件。请确保该文件在项目根目录。")
        sys.exit(1)
    except AttributeError:
        print("错误: config.py 文件中未定义 'MODEL_TO_TEST'。")
        sys.exit(1)
    
    # 检查Ollama连接
    try:
        ollama.list()
        print("✓ Ollama服务连接正常")
    except Exception as e:
        print(f"✗ Ollama服务连接失败: {e}")
        print("请确保Ollama服务正在运行")
        sys.exit(1)
    
    # 准备输出目录
    os.makedirs(TESTOUT_DIR, exist_ok=True)
    print(f"✓ 输出目录已准备: {TESTOUT_DIR}")
    
    # 准备工作区
    print(f"\n--- 准备测试环境 ---")
    if os.path.exists(WORKSPACE_DIR):
        print(f"发现旧的工作区 '{WORKSPACE_DIR}', 正在清理...")
        shutil.rmtree(WORKSPACE_DIR)
    print(f"创建新的工作区 '{WORKSPACE_DIR}'...")
    os.makedirs(WORKSPACE_DIR)
    print("环境准备完毕。\n")
    
    # 确保测试脚本保存输出
    ensure_output_saved()
    
    # 运行所有测试
    for script_name in TEST_SCRIPTS:
        run_single_test_with_output_capture(script_name)
    
    print("\n" + "=" * 80)
    print(f"所有测试已完成！")
    print(f"结束时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"测试结果保存在: {TESTOUT_DIR}")
    print(f"测试工作区: {WORKSPACE_DIR}")
    print("=" * 80)
    
    # 自动运行评价脚本
    print("\n正在生成评价报告...")
    try:
        subprocess.run([sys.executable, "evaluate_results.py"], check=True)
        print("✓ 评价报告已生成")
    except Exception as e:
        print(f"✗ 生成评价报告时出错: {e}")

if __name__ == "__main__":
    main()
