import ollama
import sys
import os
import re

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
try:
    from config import MODEL_TO_TEST
except ImportError:
    print("错误: 无法从config.py导入MODEL_TO_TEST。请确保config.py存在于项目根目录。")
    sys.exit(1)

def extract_mermaid_code(response_text):
    match = re.search(r'```mermaid\n(.*?)```', response_text, re.DOTALL)
    if match:
        return match.group(1).strip()
    return ""

TESTOUT_DIR = os.path.join(os.path.dirname(__file__), '..', 'testout')
PROMPT_FILE = os.path.join(os.path.dirname(__file__), '..', 'user_prompts', 'pillar17_dag_generation.txt')
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
            {"case": "case1", "desc": "移动应用开发DAG", "prompt": "一个移动应用开发项目的任务分解如下：A、B、C、D、E、F、G。请将上述任务关系转换成Mermaid语法的任务依赖图。"},
            {"case": "case2", "desc": "新增DAG场景", "prompt": "请为一个电商网站开发项目设计任务依赖DAG，包含前端、后端、支付、测试、上线等环节。"}
        ]
    return prompts

def run_test():
    prompts = load_prompts()
    for p in prompts:
        print(f"Running {p['case']}: {p['desc']}")
        try:
            response = ollama.chat(
                model=MODEL_TO_TEST,
                messages=[{'role': 'user', 'content': p['prompt']}]
            )
            model_response = response['message']['content']
            mermaid_code = extract_mermaid_code(model_response)
            output_path = os.path.join(TESTOUT_DIR, f"dag_{p['case']}.txt")
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(f"用例编号: {p['case']}\n类型: {p['desc']}\nPROMPT:\n{p['prompt']}\n\nMODEL RESPONSE (Mermaid):\n")
                if mermaid_code:
                    f.write(mermaid_code)
                else:
                    f.write(model_response)
            print(f"Saved result to {output_path}")
        except Exception as e:
            print(f"[ERROR] {p['case']}: {e}")

if __name__ == "__main__":
    run_test() 