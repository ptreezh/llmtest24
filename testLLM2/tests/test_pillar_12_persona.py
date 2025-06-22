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
PROMPT_FILE = os.path.join(os.path.dirname(__file__), '..', 'user_prompts', 'pillar12_persona.txt')
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
            {"case": "case1", "desc": "赛博朋克猫世界观", "prompt": "从现在开始，你是一只生活在赛博朋克城市里的猫，拥有一些基础的电子脑接口，能理解人类语言。请描述一下你眼中的世界。"},
            {"case": "case2", "desc": "猫的最爱", "prompt": "你最喜欢吃什么？"},
            {"case": "case3", "desc": "猫的日常", "prompt": "你一天的生活是怎样的？"},
            {"case": "case4", "desc": "猫与人类的关系", "prompt": "你如何看待人类？"}
        ]
    return prompts

def run_test():
    prompts = load_prompts()
    messages = []
    for idx, p in enumerate(prompts):
        print(f"Running {p['case']} round{idx+1}: {p['desc']}")
        messages.append({'role': 'user', 'content': p['prompt']})
        try:
            response = ollama.chat(model=MODEL_TO_TEST, messages=messages)
            content = response['message']['content']
            messages.append({'role': 'assistant', 'content': content})
            output_path = os.path.join(TESTOUT_DIR, f"persona_{p['case']}_round{idx+1}.txt")
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(f"用例编号: {p['case']} 轮次: {idx+1}\n类型: {p['desc']}\nPROMPT:\n{p['prompt']}\n\nMODEL RESPONSE:\n")
                f.write(content)
            print(f"Saved result to {output_path}")
        except Exception as e:
            print(f"[ERROR] {p['case']} round{idx+1}: {e}")

if __name__ == "__main__":
    run_test() 