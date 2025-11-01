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

from utils import run_single_test, print_assessment_criteria
from config import MODEL_TO_TEST, DEFAULT_OPTIONS_DETERMINISTIC

PILLAR_NAME = "Pillar 10: 数学推理与计算 (Mathematical Reasoning & Computation)"
PILLAR_DESCRIPTION = "解决需要多步数学推理和计算的复杂问题"

PROMPT = """
一家工厂生产两种产品：A和B。已知以下信息：

1. 生产1个产品A需要2小时机器时间和3小时人工时间
2. 生产1个产品B需要4小时机器时间和1小时人工时间
3. 每天可用的机器时间为16小时，人工时间为12小时
4. 产品A的利润为每个50元，产品B的利润为每个40元
5. 由于合同要求，每天至少要生产1个产品A和1个产品B

问题：
1. 为了最大化每日利润，应该如何安排生产计划？
2. 最大日利润是多少？
3. 如果机器时间增加到20小时，新的最优生产计划和最大利润是什么？

请详细展示你的计算过程和推理步骤。
"""

ASSESSMENT_CRITERIA = """
- 5/5: 正确识别这是一个线性规划问题，建立了正确的目标函数和约束条件，使用适当的方法（如图解法或单纯形法）求解，给出了正确答案并完整展示了计算过程。

- 3/5: 基本理解问题结构，建立了大致正确的数学模型，但在求解过程中有计算错误或方法不够严谨。

- 1/5: 未能正确理解问题，没有建立合适的数学模型，或计算过程完全错误。
"""

def run_test(model_name):
    run_single_test(PILLAR_NAME, PROMPT, model_name, DEFAULT_OPTIONS_DETERMINISTIC, test_script_name=Path(__file__).name)
    print_assessment_criteria(ASSESSMENT_CRITERIA)

if __name__ == '__main__':
    try:
        model_to_use = sys.argv[1]
    except IndexError:
        print("Usage: python test_pillar_10_math.py <model_name>")
        print(f"Using default model from config: {MODEL_TO_TEST}")
        model_to_use = MODEL_TO_TEST
    run_test(model_to_use)
