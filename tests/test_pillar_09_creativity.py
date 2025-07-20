# -*- coding: utf-8 -*-

import sys
import os
from pathlib import Path

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils import run_single_test, print_assessment_criteria
from config import MODEL_TO_TEST, DEFAULT_OPTIONS_CREATIVE

PILLAR_NAME = "Pillar 9: 创意生成与发散思维 (Creative Generation & Divergent Thinking)"
PILLAR_DESCRIPTION = "在给定约束条件下产生新颖、有用的创意内容"

PROMPT = """
请为一个名为"时间胶囊咖啡馆"的概念设计一个完整的商业计划。

约束条件：
1. 咖啡馆的核心概念是"时间"——顾客可以体验不同时代的氛围
2. 预算限制：启动资金不超过50万元人民币
3. 地点：位于一个大学城附近
4. 目标客户：学生、年轻专业人士、怀旧爱好者
5. 必须包含可持续发展元素

请提供：
- 独特的价值主张
- 室内设计概念（至少3个不同时代的区域）
- 特色菜单项目（结合时间主题）
- 营销策略
- 盈利模式
"""

ASSESSMENT_CRITERIA = """
- 5/5: 提供了高度原创且实用的商业计划，所有约束条件都被巧妙整合，展现出强烈的创新思维和商业洞察力。设计概念新颖且可执行。

- 3/5: 商业计划基本完整，有一定创意，但某些方面缺乏原创性或未充分考虑约束条件。

- 1/5: 缺乏创意，提供的是通用的咖啡馆计划，未能体现"时间胶囊"概念或忽略了大部分约束条件。
"""

def run_test(model_name):
    run_single_test(PILLAR_NAME, PROMPT, model_name, DEFAULT_OPTIONS_CREATIVE, test_script_name=Path(__file__).name)
    print_assessment_criteria(ASSESSMENT_CRITERIA)

if __name__ == '__main__':
    try:
        model_to_use = sys.argv[1]
    except IndexError:
        print("Usage: python test_pillar_09_creativity.py <model_name>")
        print(f"Using default model from config: {MODEL_TO_TEST}")
        model_to_use = MODEL_TO_TEST
    run_test(model_to_use)
