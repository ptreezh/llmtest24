import os
import sys
import subprocess
import shutil
from datetime import datetime

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

def main():
    print("=" * 80)
    print(f"启动LLM高级能力测评套件 (Pillars 9-19)")
    print(f"开始时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 80)
    try:
        from config import MODEL_TO_TEST
        print(f"配置加载成功。待测模型: {MODEL_TO_TEST}\n")
    except ImportError:
        print("错误: 找不到 config.py 文件。请确保该文件在项目根目录。")
        sys.exit(1)
    except AttributeError:
        print("错误: config.py 文件中未定义 'MODEL_TO_TEST'。")
        sys.exit(1)
    print(f"--- 准备测试环境 ---")
    if os.path.exists(WORKSPACE_DIR):
        print(f"发现旧的工作区 '{WORKSPACE_DIR}', 正在清理...")
        shutil.rmtree(WORKSPACE_DIR)
    print(f"创建新的工作区 '{WORKSPACE_DIR}'...")
    os.makedirs(WORKSPACE_DIR)
    print("环境准备完毕。\n")
    for script_name in TEST_SCRIPTS:
        script_path = os.path.join(TESTS_DIR, script_name)
        if not os.path.exists(script_path):
            print(f"\n警告: 找不到测试脚本 {script_path}，已跳过。")
            continue
        try:
            subprocess.run(
                [sys.executable, script_path], 
                check=True, 
                text=True, 
                encoding='utf-8',
                errors='replace'
            )
        except subprocess.CalledProcessError as e:
            print(f"\n{'!'*20} 错误 {'!'*20}")
            print(f"执行脚本 {script_name} 时发生错误。测试中断。")
            print(f"返回码: {e.returncode}")
            print(f"输出:\n{e.stdout}")
            print(f"错误输出:\n{e.stderr}")
            sys.exit(1)
        except FileNotFoundError:
            print(f"错误: 无法找到Python解释器 '{sys.executable}'。请检查您的Python环境。")
            sys.exit(1)
    print("=" * 80)
    print(f"所有测试已成功完成！")
    print(f"结束时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"测试工作区 '{WORKSPACE_DIR}' 中的产物已保留，供您检查。")
    print("=" * 80)

if __name__ == "__main__":
    main() 