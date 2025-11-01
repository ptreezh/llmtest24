import os
import sys
import subprocess
import shutil
from datetime import datetime
import glob

# 定义测试目录
TESTS_DIR = "tests"
WORKSPACE_DIR = os.path.join(TESTS_DIR, "test_workspace")

def get_test_scripts():
    """自动发现所有 pillar 测试脚本，并按 pillar 编号排序"""
    all_pillar_tests = []
    # glob.glob 返回的顺序可能不确定，需要手动排序
    test_files = glob.glob(os.path.join(TESTS_DIR, "test_pillar_*.py"))
    
    # 提取 pillar 编号用于排序
    def get_pillar_number(filename):
        basename = os.path.basename(filename)
        try:
            # 匹配 "test_pillar_XX_" 或 "test_pillar_XXa_"
            num_str = basename.split('_')[2]
            # 处理 '25a', '25b' 等情况
            num = int(''.join(filter(str.isdigit, num_str)))
            return (num, basename)
        except (IndexError, ValueError):
            # 如果格式不匹配，则排在最后
            return (999, basename)

    sorted_files = sorted(test_files, key=get_pillar_number)
    
    for file_path in sorted_files:
        all_pillar_tests.append(os.path.basename(file_path))
        
    return all_pillar_tests

def main():
    """主执行函数"""
    # 获取所有测试脚本
    test_scripts = get_test_scripts()
    
    print("=" * 80)
    print(f"启动LLM全面能力测评套件 (Pillars 1-25+)")
    print(f"共发现 {len(test_scripts)} 个测试脚本。")
    print(f"开始时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 80)

    # 检查配置文件
    try:
        from config import MODEL_TO_TEST
        print(f"配置加载成功。待测模型: {MODEL_TO_TEST}\n")
    except ImportError:
        print("错误: 找不到 config.py 文件。请确保该文件在项目根目录。")
        sys.exit(1)
    except AttributeError:
        print("错误: config.py 文件中未定义 'MODEL_TO_TEST'。")
        sys.exit(1)

    # 准备测试环境
    print(f"--- 准备测试环境 ---")
    if os.path.exists(WORKSPACE_DIR):
        print(f"发现旧的工作区 '{WORKSPACE_DIR}', 正在清理...")
        shutil.rmtree(WORKSPACE_DIR)
    print(f"创建新的工作区 '{WORKSPACE_DIR}'...")
    os.makedirs(WORKSPACE_DIR)
    print("环境准备完毕。\n")

    # 依次执行测试脚本
    for i, script_name in enumerate(test_scripts):
        script_path = os.path.join(TESTS_DIR, script_name)
        
        print("-" * 80)
        print(f"[{i+1}/{len(test_scripts)}] ==> 开始执行: {script_name}")
        
        try:
            # 设置环境变量以强制UTF-8编码
            env = os.environ.copy()
            env['PYTHONUTF8'] = '1'
            
            # 使用 subprocess.run 执行脚本
            process = subprocess.run(
                [sys.executable, script_path],
                check=True,
                text=True,
                # encoding='utf-8', # text=True 和 env['PYTHONUTF8']='1' 已经处理了编码
                errors='replace',
                capture_output=True,  # 捕获输出
                env=env
            )
            # 打印脚本的 stdout
            if process.stdout:
                print("--- 脚本输出 ---")
                print(process.stdout)
                print("--- 输出结束 ---")

        except subprocess.CalledProcessError as e:
            print(f"\n{'!'*20} 错误 {'!'*20}")
            print(f"执行脚本 {script_name} 时发生错误。测试中断。")
            print(f"返回码: {e.returncode}")
            print(f"--- STDOUT ---")
            print(e.stdout)
            print(f"--- STDERR ---")
            print(e.stderr)
            print(f"{'!'*50}")
            sys.exit(1)
        except FileNotFoundError:
            print(f"错误: 无法找到Python解释器 '{sys.executable}'。请检查您的Python环境。")
            sys.exit(1)
        
        print(f"[{i+1}/{len(test_scripts)}] ==> 成功完成: {script_name}")

    print("=" * 80)
    print(f"所有 {len(test_scripts)} 个测试已全部成功完成！")
    print(f"结束时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"测试工作区 '{WORKSPACE_DIR}' 中的产物已保留，供您检查。")
    print("=" * 80)

if __name__ == "__main__":
    main()
