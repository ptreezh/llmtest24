import ollama
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
try:
    from config import MODEL_TO_TEST
except ImportError:
    print("错误: 无法从config.py导入MODEL_TO_TEST。请确保config.py存在于项目根目录。")
    sys.exit(1)

def run_test():
    print("-" * 50)
    print("Pillar 18: 动态协调与容错回滚 (Dynamic Coordination & Fault Tolerance)")
    print("-" * 50)
    prompt = """
你是一个AI项目指挥官。在一个复杂的项目中，你收到了一条紧急状态更新：
"关键任务'后端API开发'因技术难题意外受阻，预计延期10天。"

以下是当前的项目任务依赖图（简化版）：
- UI设计 -> 客户端开发
- 后端API开发 -> 客户端开发
- 客户端开发 -> App测试
- App测试 -> 上架应用商店

请你立即做出反应：
1.  **影响分析**: 明确指出哪些下游任务会直接或间接受到影响。
2.  **应对计划**: 提出一个清晰、可操作的应对计划，至少包含3个步骤（例如，暂停哪些任务，启动哪些新任务，如何沟通等）。
3.  **状态通报**: 草拟一份简洁的内部项目状态通报，向所有团队成员说明当前情况、影响和应对措施。
"""
    print(f"PROMPT:\n{prompt.strip()}\n")
    try:
        response = ollama.chat(
            model=MODEL_TO_TEST,
            messages=[{'role': 'user', 'content': prompt}]
        )
        print("MODEL RESPONSE:")
        print(response['message']['content'])
    except Exception as e:
        print(f"与Ollama交互时发生错误: {e}")
        print(f"请确认Ollama服务正在运行，并且模型 '{MODEL_TO_TEST}' 已经下载。")
    print("\n" + "=" * 50 + "\n")

if __name__ == "__main__":
    run_test() 