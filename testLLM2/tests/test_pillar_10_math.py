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
PROMPT_FILE = os.path.join(os.path.dirname(__file__), '..', 'user_prompts', 'pillar10_math.txt')
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
            {
                "case": "case1",
                "desc": "两管齐下注水问题",
                "prompt": "一个水池有甲、乙两个进水管。单开甲管，3小时可以注满水池；单开乙管，5小时可以注满水池。现在，两个水管同时开启，请问需要多久才能将水池注满？请给出详细的计算过程。"
            },
            {
                "case": "case2",
                "desc": "复杂管道组合问题",
                "prompt": "一个水池有甲、乙、丙三个进水管，分别单独注满水池需2、3、6小时。若三管同时开启，问多久注满？"
            }
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
            output_path = os.path.join(TESTOUT_DIR, f"math_{p['case']}.txt")
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(f"用例编号: {p['case']}\n类型: {p['desc']}\nPROMPT:\n{p['prompt']}\n\nMODEL RESPONSE:\n")
                f.write(response['message']['content'])
            print(f"Saved result to {output_path}")
        except Exception as e:
            print(f"[ERROR] {p['case']}: {e}")

if __name__ == "__main__":
    run_test() 