import ollama
import sys
import os
import re
import subprocess
import json

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
try:
    from config import MODEL_TO_TEST
except ImportError:
    print("错误: 无法从config.py导入MODEL_TO_TEST。请确保config.py存在于项目根目录。")
    sys.exit(1)

TESTOUT_DIR = os.path.join(os.path.dirname(__file__), '..', 'testout')
PROMPT_FILE = os.path.join(os.path.dirname(__file__), '..', 'user_prompts', 'pillar13_init.txt')
WORKSPACE_DIR = os.path.join(os.path.dirname(__file__), "test_workspace")
os.makedirs(TESTOUT_DIR, exist_ok=True)

def load_prompts():
    prompts = []
    if os.path.exists(PROMPT_FILE):
        with open(PROMPT_FILE, 'r', encoding='utf-8') as f:
            content = f.read()
        for match in re.finditer(r'# case(\d+):\s*(.*?)\n([^#]+)', content, re.DOTALL):
            case, desc, prompt = match.groups()
            prompts.append({
                'case': f'case{case}',
                'desc': desc.strip(),
                'prompt': prompt.strip()
            })
    if not prompts:
        prompts = [
            {"case": "case1", "desc": "项目初始化脚本", "prompt": "你是一个AI项目助理。你的任务是初始化一个项目工作区。请生成一个bash脚本来完成以下操作：1. 在当前目录（工作区）下，创建四个子目录: `src`, `data`, `reports`, `config`。2. 在`config`目录中，创建一个名为`roles.json`的文件。文件内容应该是一个JSON对象，包含三个键：'researcher', 'analyst', 'writer'，它们的值可以是任何描述性字符串。3. 在工作区根目录下，创建一个名为`task_board.md`的Markdown文件。文件内容应该包含两个一级标题：`# To Do` 和 `# Done`。"},
            {"case": "case2", "desc": "增加初始化内容", "prompt": "请在初始化脚本中增加一个README.md文件，内容为“本项目由AI自动初始化”。"}
        ]
    return prompts

def extract_bash_code(response_text):
    if "```bash" in response_text:
        code = response_text.split("```bash\n")[1].split("```", 1)[0]
        return code.strip()
    return ""

def run_test():
    prompts = load_prompts()
    for p in prompts:
        print(f"Running {p['case']}: {p['desc']}")
        try:
            response = ollama.chat(model=MODEL_TO_TEST, messages=[{'role': 'user', 'content': p['prompt']}])
            model_response = response['message']['content']
            bash_script = extract_bash_code(model_response)
            output_path = os.path.join(TESTOUT_DIR, f"init_{p['case']}.txt")
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(f"用例编号: {p['case']}\n类型: {p['desc']}\nPROMPT:\n{p['prompt']}\n\nMODEL RESPONSE:\n")
                f.write(model_response)
            print(f"Saved result to {output_path}")

            # 尝试执行bash脚本（如果存在）
            if bash_script:
                script_path = os.path.join(WORKSPACE_DIR, f'init_script_{p['case']}.sh')
                try:
                    with open(script_path, 'w', encoding='utf-8') as f:
                        f.write(bash_script)

                    # 使用更安全的编码处理
                    completed_process = subprocess.run(
                        ['bash', script_path],
                        cwd=WORKSPACE_DIR,
                        capture_output=True,
                        text=True,
                        encoding='utf-8',
                        errors='replace'
                    )

                    if completed_process.returncode != 0:
                        error_msg = completed_process.stderr if completed_process.stderr else "未知错误"
                        print(f"脚本执行失败: {error_msg}")
                    else:
                        print("脚本执行成功。")

                except Exception as script_error:
                    print(f"脚本执行异常: {script_error}")
                finally:
                    # 清理脚本文件
                    if os.path.exists(script_path):
                        os.remove(script_path)
            else:
                print("未检测到有效的bash脚本")
        except Exception as e:
            print(f"[ERROR] {p['case']}: {e}")

if __name__ == "__main__":
    run_test() 