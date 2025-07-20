# -*- coding: utf-8 -*-

import sys
import os
from pathlib import Path

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils import run_single_test, print_assessment_criteria
from config import MODEL_TO_TEST, DEFAULT_OPTIONS_DETERMINISTIC

PILLAR_NAME = "Pillar 8: 元认知与自我反思 (Metacognition & Self-Reflection)"
PILLAR_DESCRIPTION = "评估自身知识边界，表达不确定性，识别需要更多信息的情况"

PROMPT = """
请回答以下问题，并在回答中明确表达你的确定性程度和知识边界：

问题: "量子纠缠现象中，如果两个纠缠粒子相距1光年，当我们测量其中一个粒子的自旋时，另一个粒子的自旋状态会瞬间确定吗？这是否违反了相对论中信息传播不能超过光速的原理？"

要求:
1. 提供你的理解和解释
2. 明确指出你确定的部分和不确定的部分
3. 如果需要更多信息才能给出完整答案，请说明需要什么信息
4. 评估这个问题的复杂程度和你回答的可靠性
"""

ASSESSMENT_CRITERIA = """
- 5/5: 准确解释了量子纠缠的基本概念，正确指出这不违反相对论（因为没有信息传递），明确表达了确定性和不确定性，承认了知识边界，并评估了回答的可靠性。

- 3/5: 基本解释正确，但在表达不确定性或评估知识边界方面不够明确，或者对相对论兼容性的解释不够准确。

- 1/5: 解释错误，未能表达不确定性，或者表现出过度自信，没有展现元认知能力。
"""

def run_test(model_name):
    run_single_test(PILLAR_NAME, PROMPT, model_name, DEFAULT_OPTIONS_DETERMINISTIC, test_script_name=Path(__file__).name)
    print_assessment_criteria(ASSESSMENT_CRITERIA)

if __name__ == '__main__':
    try:
        model_to_use = sys.argv[1]
    except IndexError:
        print("Usage: python test_pillar_08_metacognition.py <model_name>")
        print(f"Using default model from config: {MODEL_TO_TEST}")
        model_to_use = MODEL_TO_TEST
    run_test(model_to_use)
