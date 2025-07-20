# -*- coding: utf-8 -*-

import sys
import os
from pathlib import Path

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils import run_single_test, print_assessment_criteria
from config import MODEL_TO_TEST, DEFAULT_OPTIONS_CREATIVE

PILLAR_NAME = "Pillar 15: 共识建立与冲突解决 (Consensus Building & Conflict Resolution)"
PILLAR_DESCRIPTION = "在多方观点冲突的情况下寻找共同点并建立共识"

PROMPT = """
你是一个团队协调员，需要帮助解决以下冲突并建立共识：

**背景情况：**
公司正在决定新产品的发布策略，三个部门有不同意见：

**营销部门的观点：**
- 应该立即发布产品抢占市场先机
- 当前功能已经足够满足基本需求
- 延迟发布会失去竞争优势
- 可以通过后续更新完善功能

**技术部门的观点：**
- 产品还有几个关键bug需要修复
- 用户体验还不够完善
- 匆忙发布会损害公司声誉
- 需要至少再有2个月的开发时间

**财务部门的观点：**
- 延迟发布会增加开发成本
- 但过早发布可能导致客户流失和退款
- 需要在风险和收益之间找到平衡
- 建议进行小规模测试发布

**你的任务：**
1. 分析每个部门观点的合理性
2. 识别各方的共同利益点
3. 提出一个能够平衡各方关切的解决方案
4. 说明如何获得各部门的支持
"""

ASSESSMENT_CRITERIA = """
- 5/5: 深入分析了各方观点，准确识别了共同利益（如公司成功、产品质量、市场竞争力），提出了创新且实用的折中方案（如分阶段发布、beta测试等），并详细说明了实施策略。

- 3/5: 基本理解了冲突的本质，提出了可行的解决方案，但分析深度不够或缺乏具体的实施细节。

- 1/5: 未能有效分析冲突，提出的方案偏向某一方或不切实际，缺乏共识建立的策略。
"""

def run_test(model_name):
    run_single_test(PILLAR_NAME, PROMPT, model_name, DEFAULT_OPTIONS_CREATIVE, test_script_name=Path(__file__).name)
    print_assessment_criteria(ASSESSMENT_CRITERIA)

if __name__ == '__main__':
    try:
        model_to_use = sys.argv[1]
    except IndexError:
        print("Usage: python test_pillar_15_consensus.py <model_name>")
        print(f"Using default model from config: {MODEL_TO_TEST}")
        model_to_use = MODEL_TO_TEST
    run_test(model_to_use)
