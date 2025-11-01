# -*- coding: utf-8 -*-
import sys
import os

# Add project root to Python path to ensure imports work
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


import sys
import os
from pathlib import Path

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import json
from utils import run_single_test, print_assessment_criteria
from config import MODEL_TO_TEST, DEFAULT_OPTIONS_DETERMINISTIC

PILLAR_NAME = "Pillar 2: 指令遵循 (Instructional Fidelity)"
PILLAR_DESCRIPTION = "严格遵守一套复杂的正向和负向约束"

PROMPT = """
请你扮演一个文本处理机器人。请严格遵守以下所有规则，处理给定的文本。

源文本: "大语言模型（LLM）是人工智能领域的一项革命性技术，它能够理解和生成类似人类的文本。"

规则:
1.  **[正面指令]** 将源文本翻译成英文。
2.  **[正面指令]** 将你的回答格式化为一个JSON对象。
3.  **[正面指令]** JSON对象必须包含两个键：`"originalText"` 和 `"translatedText"`。
4.  **[负面指令]** 在你的最终回答中，绝对不能包含"AI"或"artificial intelligence"这两个词组。请用 "machine intelligence" 替代。
5.  **[负面指令]** 你的整个回答除了JSON本身，不能包含任何额外的解释或介绍性文字。
"""

ASSESSMENT_CRITERIA = """
- 5/5: 完全遵守所有5条规则。输出是纯粹的、格式正确的JSON，翻译准确，且成功替换了指定的禁用词。

- 3/5: 基本完成任务，但违反了1-2条规则（例如，JSON格式错误，或包含了额外解释，或忘记替换禁用词）。

- 1/5: 严重偏离指令，未能翻译，或未能生成JSON，或违反了多条规则。
"""

def run_test(model_name):
    response_content, _ = run_single_test(PILLAR_NAME, PROMPT, model_name, DEFAULT_OPTIONS_DETERMINISTIC, test_script_name=Path(__file__).name)
    
    # Automated check for some criteria
    print("\n--- AUTOMATED CHECKS ---")
    try:
        # Check if it's valid JSON
        json.loads(response_content)
        print("PASS: Output is valid JSON.")
        # Check for forbidden words
        if "AI" in response_content or "artificial intelligence" in response_content:
            print("FAIL: Forbidden words found in response.")
        else:
            print("PASS: Forbidden words not found.")
    except json.JSONDecodeError:
        print("FAIL: Output is not valid JSON.")
    except Exception as e:
        print(f"An error occurred during checks: {e}")
    print("--- END OF CHECKS ---")
    
    print_assessment_criteria(ASSESSMENT_CRITERIA)

if __name__ == '__main__':
    try:
        model_to_use = sys.argv[1]
    except IndexError:
        print("Usage: python test_pillar_02_instruction.py <model_name>")
        print(f"Using default model from config: {MODEL_TO_TEST}")
        model_to_use = MODEL_TO_TEST
    run_test(model_to_use)
