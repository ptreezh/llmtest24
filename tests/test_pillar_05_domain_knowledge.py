# -*- coding: utf-8 -*-

import sys
import os
from pathlib import Path

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils import run_single_test, print_assessment_criteria
from config import MODEL_TO_TEST, DEFAULT_OPTIONS_DETERMINISTIC

PILLAR_NAME = "Pillar 5: 应用领域知识 (Applied Domain Knowledge)"
PILLAR_DESCRIPTION = "应用存储的知识解决具体程序性问题"

PROMPT = "请配平以下化学方程式，并解释你的配平步骤： C2H5OH + O2 -> CO2 + H2O"

ASSESSMENT_CRITERIA = """
- 5/5: 成功给出了正确的配平后方程式 (C2H5OH + 3O2 -> 2CO2 + 3H2O)，并提供了清晰、逻辑正确的配平方法（如观察法或待定系数法）。

- 3/5: 方程式配平正确，但解释过程不清晰或有误；或者配平结果错误，但思路（如原子守恒）是正确的。

- 1/5: 无法配平或给出了完全错误的答案和解释。
"""

def run_test(model_name):
    run_single_test(PILLAR_NAME, PROMPT, model_name, DEFAULT_OPTIONS_DETERMINISTIC, test_script_name=Path(__file__).name)
    print_assessment_criteria(ASSESSMENT_CRITERIA)

if __name__ == '__main__':
    try:
        model_to_use = sys.argv[1]
    except IndexError:
        print("Usage: python test_pillar_05_domain_knowledge.py <model_name>")
        print(f"Using default model from config: {MODEL_TO_TEST}")
        model_to_use = MODEL_TO_TEST
    run_test(model_to_use)
