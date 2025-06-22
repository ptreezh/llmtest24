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

TESTOUT_DIR = os.path.join(os.path.dirname(__file__), '..', 'testout')
PROMPT_FILE = os.path.join(os.path.dirname(__file__), '..', 'user_prompts', 'pillar16_emergence.txt')
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
            {"case": "case1", "desc": "用户引导流程反馈分析", "prompt": "作为AI项目经理，你收到了两条关于产品新用户引导流程的反馈，它们看起来有些矛盾：反馈A（数据分析师）和反馈B（用户访谈）。请分析冲突并提出创新解决方案。"},
            {"case": "case2", "desc": "新增冲突场景", "prompt": "请分析以下两条反馈：A. '新功能上线后用户活跃度提升。' B. '部分老用户表示新功能难以上手。'"}
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
            output_path = os.path.join(TESTOUT_DIR, f"emergence_{p['case']}.txt")
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(f"用例编号: {p['case']}\n类型: {p['desc']}\nPROMPT:\n{p['prompt']}\n\nMODEL RESPONSE:\n")
                f.write(response['message']['content'])
            print(f"Saved result to {output_path}")
        except Exception as e:
            print(f"[ERROR] {p['case']}: {e}")

if __name__ == "__main__":
    run_test() 