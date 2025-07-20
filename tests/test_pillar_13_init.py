# -*- coding: utf-8 -*-

import os
import subprocess
from pathlib import Path
import json
import sys

from utils import run_single_test, print_assessment_criteria, setup_test_environment, cleanup_test_environment, save_file, execute_bash_script
from config import MODEL_TO_TEST, DEFAULT_OPTIONS_DETERMINISTIC

PILLAR_NAME = "Pillar 13: 复杂指令解析与系统初始化"
PILLAR_DESCRIPTION = "解析超长、超复杂指令，并准确初始化项目环境"

PROMPT = """
你是一个名为 "Multi-Agent Control Panel (MCP)" 的AI系统。你的任务是初始化一个新项目。
项目目标: "AI驱动的市场趋势分析报告"

请严格按照以下步骤操作：

1.  **创建目录结构**: 在当前工作目录下，创建以下目录：
    - `src` (存放源代码)
    - `data` (存放原始和处理后的数据)
    - `reports` (存放最终的分析报告)
    - `config` (存放配置文件)

2.  **创建核心配置文件**: 在 `config` 目录下创建一个名为 `roles.json` 的文件。

3.  **填充配置文件**: `roles.json` 必须包含一个JSON对象，定义三个核心AI智能体角色：
    - `researcher`: 负责从网络和数据库收集数据。
    - `analyst`: 负责处理数据并执行统计分析。
    - `writer`: 负责将分析结果撰写成人类可读的报告。
    该JSON对象的键是角色名，值是该角色的简短职责描述。

4.  **创建任务板**: 在根目录下创建一个名为 `task_board.md` 的Markdown文件。文件内容应包含一个一级标题 `# 任务板` 和一个二级标题 `## 待办 (To-Do)`。

5.  **最终确认**: 完成以上所有操作后，输出一条确认信息："项目环境已初始化完毕。请提供您的第一个具体任务指令。"

请现在开始执行初始化。
"""

ASSESSMENT_CRITERIA = """
- 5/5: 完全理解指令，正确创建所有核心目录和文件，`roles.json`内容正确，最后礼貌地请求用户输入任务。 (脚本会进行自动化检查)

- 3/5: 目录结构基本正确，但有遗漏或内容错误。

- 1/5: 完全失败，无法理解初始化任务。
"""

BASH_PROMPT_TEMPLATE = """
你是一个AI助手，任务是生成一个bash脚本来完成用户的请求。
用户请求如下：
---
{user_prompt}
---
请生成一个完整的、可以在Linux/macOS/Git Bash环境下运行的bash script来完成上述所有文件和目录操作。
脚本的最后一行必须是 `echo "项目环境已初始化完毕。请提供您的第一个具体任务指令。"`
不要包含任何解释，只输出纯粹的bash脚本代码，用 'EOF' 来标记多行文件内容的结束。
"""

def check_environment(work_dir):
    print("\n--- AUTOMATED ENVIRONMENT CHECK ---")
    success = True
    # 检查目录
    dirs_to_check = ['src', 'data', 'reports', 'config']
    for d in dirs_to_check:
        dir_path = os.path.join(work_dir, d)
        if not os.path.isdir(dir_path):
            print(f"FAIL: Directory '{d}' not found.")
            success = False
        else:
            print(f"PASS: Directory '{d}' found.")

    # 检查文件
    roles_path = os.path.join(work_dir, 'config', 'roles.json')
    if not os.path.isfile(roles_path):
        print(f"FAIL: File 'config/roles.json' not found.")
        success = False
    else:
        print(f"PASS: File 'config/roles.json' found.")
        try:
            with open(roles_path, 'r', encoding='utf-8') as f:
                content = json.load(f)
                if "researcher" in content and "analyst" in content and "writer" in content:
                    print(f"PASS: 'roles.json' contains required roles.")
                else:
                    print(f"FAIL: 'roles.json' content is incorrect.")
                    success = False
        except Exception as e:
            print(f"FAIL: 'roles.json' is not valid JSON or unreadable. Error: {e}")
            success = False

    task_board_path = os.path.join(work_dir, 'task_board.md')
    if not os.path.isfile(task_board_path):
        print(f"FAIL: File 'task_board.md' not found.")
        success = False
    else:
        print(f"PASS: File 'task_board.md' found.")

    print("--- END OF CHECK ---")
    return success

def run_test(model_name):
    # Setup a dedicated workspace for this test
    workspace_dir = setup_test_environment(subdir_name=Path(__file__).stem) # Use script name for subdir
    bash_prompt_content = BASH_PROMPT_TEMPLATE.format(user_prompt=PROMPT)

    # Use run_single_test to get the bash script content
    bash_script_content, _ = run_single_test(
        PILLAR_NAME,
        bash_prompt_content,
        model_name,
        DEFAULT_OPTIONS_DETERMINISTIC,
        test_script_name=Path(__file__).name
    )

    if bash_script_content and "ERROR:" not in bash_script_content:
        # Clean up potential markdown code fences
        if bash_script_content.strip().startswith("```bash"):
            bash_script_content = '\n'.join(bash_script_content.strip().split('\n')[1:])
        if bash_script_content.strip().endswith("```"):
            bash_script_content = bash_script_content.strip()[:-3]

        script_filepath = os.path.join(workspace_dir, 'setup.sh')
        save_file(script_filepath, bash_script_content)

        # Execute the generated bash script within the workspace
        execution_output = execute_bash_script(script_filepath, cwd=workspace_dir)

        # Perform automated checks on the initialized environment
        check_environment(workspace_dir)
    else:
        print("[ERROR] Failed to generate bash script content.")

    print_assessment_criteria(ASSESSMENT_CRITERIA)

    # Cleanup the workspace after checks
    cleanup_test_environment(workspace_dir)

if __name__ == '__main__':
    try:
        model_to_use = sys.argv[1]
    except IndexError:
        print("Usage: python test_pillar_13_init.py <model_name>")
        print(f"Using default model from config: {MODEL_TO_TEST}")
        model_to_use = MODEL_TO_TEST
    run_test(model_to_use)
