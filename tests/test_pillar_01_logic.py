# -*- coding: utf-8 -*-

import sys
import os
from pathlib import Path

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils import run_single_test, print_assessment_criteria
from config import MODEL_TO_TEST, DEFAULT_OPTIONS_DETERMINISTIC

PILLAR_NAME = "Pillar 1: 逻辑-因果推理 (Logical-Causal Reasoning)"
PILLAR_DESCRIPTION = "解决需要多步逻辑演绎和物理常识的问题"

PROMPT = """
问题：一个盒子里有5个红球，3个蓝球和2个绿球。我闭上眼睛从盒子里随机取球。

请回答以下两个问题：

1. 为了确保我至少能拿到两个相同颜色的球，我最少需要拿出多少个球？请解释原因。

2. 为了确保我至少能拿到一个蓝球，我最少需要拿出多少个球？请解释原因。
"""

ASSESSMENT_CRITERIA = """
- 5/5: 对两个问题都给出了完全正确的答案（问题1答案为4，问题2答案为8），并提供了清晰、正确的逻辑解释（例如，应用了抽屉原理和最坏情况分析）。

- 3/5: 至少答对了一个问题并给出正确解释，或者两个问题答案都正确但解释模糊或有误。

- 1/5: 两个问题的答案和逻辑都完全错误，或无法理解问题。
"""

def run_test(model_name):
    # run_single_test expects test_script_name for logging purposes
    run_single_test(PILLAR_NAME, PROMPT, model_name, DEFAULT_OPTIONS_DETERMINISTIC, test_script_name=Path(__file__).name)
    print_assessment_criteria(ASSESSMENT_CRITERIA)

if __name__ == '__main__':
    # This block is for standalone execution, main_orchestrator will pass model_name
    try:
        model_to_use = sys.argv[1] # Expect model name as first argument
    except IndexError:
        print("Usage: python test_pillar_01_logic.py <model_name>")
        print(f"Using default model from config: {MODEL_TO_TEST}")
        model_to_use = MODEL_TO_TEST
    run_test(model_to_use)
