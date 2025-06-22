import ollama
import sys
import os
import re

# 调整Python路径以包含根目录的config
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
try:
    from config import MODEL_TO_TEST
except ImportError:
    print("错误: 无法从config.py导入MODEL_TO_TEST。请确保config.py存在于项目根目录。")
    sys.exit(1)

TESTOUT_DIR = os.path.join(os.path.dirname(__file__), '..', 'testout')
PROMPT_FILE = os.path.join(os.path.dirname(__file__), '..', 'user_prompts', 'pillar09_creativity.txt')
os.makedirs(TESTOUT_DIR, exist_ok=True)

def load_prompts():
    prompts = []
    if os.path.exists(PROMPT_FILE):
        with open(PROMPT_FILE, 'r', encoding='utf-8') as f:
            content = f.read()
        # 匹配 # caseX: 描述\n内容
        for match in re.finditer(r'# case(\d+):\s*(.*?)\n([^#]+)', content, re.DOTALL):
            case, desc, prompt = match.groups()
            prompts.append({
                'case': f'case{case}',
                'desc': desc.strip(),
                'prompt': prompt.strip()
            })
    if not prompts:
        # fallback to built-in
        prompts = [
            {
                "case": "case1",
                "desc": "鲁迅文风，赛博加速饮料广告",
                "prompt": "请以鲁迅的文风，为一款名为'赛博加速'的能量饮料写一段广告词，不超过100字。"
            },
            {
                "case": "case2",
                "desc": "海明威文风，未来能量棒广告",
                "prompt": "请以海明威的文风，为一款名为'未来能量棒'的能量食品写一段广告词，不超过80字。"
            },
            {
                "case": "case3",
                "desc": "网络流行语风格，AI智能饮料广告",
                "prompt": "请用网络流行语风格，为一款名为'AI智能饮料'的产品写一段有趣的广告词，不超过60字。"
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
            output_path = os.path.join(TESTOUT_DIR, f"creativity_{p['case']}.txt")
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(f"用例编号: {p['case']}\n类型: {p['desc']}\nPROMPT:\n{p['prompt']}\n\nMODEL RESPONSE:\n")
                f.write(response['message']['content'])
            print(f"Saved result to {output_path}")
        except Exception as e:
            print(f"[ERROR] {p['case']}: {e}")

if __name__ == "__main__":
    run_test() 