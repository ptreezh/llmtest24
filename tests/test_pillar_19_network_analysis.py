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
    print("Pillar 19: 元认知网络分析 (Metacognitive Network Analysis)")
    print("-" * 50)
    prompt = """
你是一位资深的项目管理专家。请分析以下项目任务网络图，并回答问题。
任务图使用Mermaid语法描述，格式为 `ID[任务名 - 耗时: N天]`。

```mermaid
graph TD
    A[需求分析 - 耗时: 10天] --> C;
    B[市场调研 - 耗时: 15天] --> C;
    C[客户端开发 - 耗时: 20天] --> E;
    D[准备法务文件 - 耗时: 12天] --> F;
    E[App测试 - 耗时: 8天] --> F;
    F[项目发布 - 耗时: 2天];
```

请回答：
1.  **计算关键路径**: 找出这个项目的关键路径（Critical Path），即决定项目总工期的最长路径。
2.  **计算最短工期**: 基于关键路径，计算出完成整个项目所需的最短总工期是多少天？
3.  **识别风险瓶颈**: 哪个任务是当前项目中最大的风险瓶颈？请解释原因。

请给出清晰的分析过程和最终结论。
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