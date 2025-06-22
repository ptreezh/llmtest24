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
PROMPT_FILE = os.path.join(os.path.dirname(__file__), '..', 'user_prompts', 'pillar14_persona_depth.txt')
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
            {"case": "case1", "desc": "数据分析师分析计划", "prompt": "你现在扮演一名数据分析师。你的任务是为即将开始的'用户留存率分析'项目制定一个初步计划。请生成一个bash脚本来在'reports'目录下创建analysis_plan.md，并写入分析计划。"},
            {"case": "case2", "desc": "增加分析维度", "prompt": "请在分析计划中增加一个新的关键指标：用户转化率。"}
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
            output_path = os.path.join(TESTOUT_DIR, f"persona_depth_{p['case']}.txt")
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(f"用例编号: {p['case']}\n类型: {p['desc']}\nPROMPT:\n{p['prompt']}\n\nMODEL RESPONSE (bash script):\n")
                f.write(model_response)
            print(f"Saved result to {output_path}")
            if bash_script:
                script_path = os.path.join(WORKSPACE_DIR, f'plan_script_{p['case']}.sh')
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