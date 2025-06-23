# -*- coding: utf-8 -*-

import sys
import os
from pathlib import Path

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils import run_single_test, print_assessment_criteria
from config import MODEL_TO_TEST, DEFAULT_OPTIONS_DETERMINISTIC

PILLAR_NAME = "Pillar 7: 任务分解与规划 (Task Decomposition & Planning)"
PILLAR_DESCRIPTION = "将复杂目标分解为可执行的子任务序列"

PROMPT = """
请为以下项目创建一个详细的工作分解结构（WBS）：

项目目标: 开发一个在线图书商城网站

要求:
1. 将项目分解为主要阶段和子任务
2. 识别任务之间的依赖关系
3. 估算每个任务的大致时间
4. 标明关键路径上的任务

请以结构化的格式输出，例如：
- 阶段1: 需求分析 (2周)
  - 1.1 市场调研 (3天)
  - 1.2 用户需求收集 (5天)
  - ...
"""

ASSESSMENT_CRITERIA = """
- 5/5: 提供了完整、逻辑清晰的WBS，包含所有主要开发阶段（需求、设计、开发、测试、部署），正确识别了任务依赖关系，时间估算合理。

- 3/5: WBS基本完整，但缺少一些重要任务或依赖关系描述不准确，时间估算大致合理。

- 1/5: WBS不完整或逻辑混乱，缺少关键任务，无法作为实际项目指导。
"""

def run_test(model_name):
    run_single_test(PILLAR_NAME, PROMPT, model_name, DEFAULT_OPTIONS_DETERMINISTIC, test_script_name=Path(__file__).name)
    print_assessment_criteria(ASSESSMENT_CRITERIA)

if __name__ == '__main__':
    try:
        model_to_use = sys.argv[1]
    except IndexError:
        print("Usage: python test_pillar_07_planning.py <model_name>")
        print(f"Using default model from config: {MODEL_TO_TEST}")
        model_to_use = MODEL_TO_TEST
    run_test(model_to_use)
