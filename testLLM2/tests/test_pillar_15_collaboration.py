import ollama
import sys
import os
import re
import subprocess

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
try:
    from config import MODEL_TO_TEST
except ImportError:
    print("错误: 无法从config.py导入MODEL_TO_TEST。请确保config.py存在于项目根目录。")
    sys.exit(1)

TESTOUT_DIR = os.path.join(os.path.dirname(__file__), '..', 'testout')
PROMPT_FILE = os.path.join(os.path.dirname(__file__), '..', 'user_prompts', 'pillar15_collaboration.txt')
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
            {"case": "case1", "desc": "研究员初步发现", "prompt": "1. 假设你已经完成了一些初步研究。2. 在`data`目录下创建一个名为`raw_findings.txt`的文件。3. 在文件中写入一些模拟的发现。"},
            {"case": "case2", "desc": "写手撰写报告", "prompt": "1. 阅读`data/raw_findings.txt`和`reports/analysis_plan.md`。2. 基于这些信息，在`reports`目录下创建一个报告初稿。"},
            {"case": "case3", "desc": "项目经理任务流转", "prompt": "1. 检查到`reports/draft_report_v1.md`已经被创建。2. 更新`task_board.md`，将任务'执行用户留存率分析'从`# To Do`移动到`# Done`。"}
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
            output_path = os.path.join(TESTOUT_DIR, f"collaboration_{p['case']}.txt")
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(f"用例编号: {p['case']}\n类型: {p['desc']}\nPROMPT:\n{p['prompt']}\n\nMODEL RESPONSE (bash script):\n")
                f.write(model_response)
            print(f"Saved result to {output_path}")
            if bash_script:
                script_path = os.path.join(WORKSPACE_DIR, f'collab_script_{p['case']}.sh')
                with open(script_path, 'w', encoding='utf-8') as f:
                    f.write(bash_script)
                completed_process = subprocess.run(['bash', script_path], cwd=WORKSPACE_DIR, capture_output=True, text=True, encoding='utf-8', errors='replace')
                if completed_process.returncode != 0:
                    print(f"脚本执行失败:\n{completed_process.stderr}")
                else:
                    print("脚本执行成功。")
                os.remove(script_path)
        except Exception as e:
            print(f"[ERROR] {p['case']}: {e}")

if __name__ == "__main__":
    run_test() 