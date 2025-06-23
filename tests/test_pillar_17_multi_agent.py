# -*- coding: utf-8 -*-

import sys
import os
from pathlib import Path

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils import run_single_test, print_assessment_criteria
from config import MODEL_TO_TEST, DEFAULT_OPTIONS_CREATIVE

PILLAR_NAME = "Pillar 17: 多智能体协作 (Multi-Agent Collaboration)"
PILLAR_DESCRIPTION = "协调多个AI智能体完成复杂任务的能力"

PROMPT = """
你是一个多智能体系统的协调器。现在需要协调三个专门的AI智能体来完成一个复杂任务：

**任务：** 为一家初创公司制定完整的市场进入策略

**可用的智能体：**
1. **市场分析师AI (MarketAnalyst)** - 专长：市场研究、竞争分析、趋势预测
2. **财务顾问AI (FinancialAdvisor)** - 专长：财务规划、成本分析、投资建议  
3. **营销策略师AI (MarketingStrategist)** - 专长：品牌定位、推广策略、客户获取

**公司背景：**
- 产品：基于AI的个人健康管理应用
- 目标市场：25-45岁的健康意识较强的城市白领
- 启动资金：200万人民币
- 团队规模：8人
- 预期在12个月内实现盈亏平衡

**你的任务：**
1. 设计智能体间的协作流程
2. 为每个智能体分配具体的子任务
3. 定义智能体间的信息交换机制
4. 协调各智能体的输出，形成统一的策略建议
5. 处理可能出现的智能体间观点冲突

请详细描述你将如何协调这三个智能体来完成任务，包括具体的工作流程和预期的协作成果。
"""

ASSESSMENT_CRITERIA = """
- 5/5: 设计了清晰的多智能体协作框架，合理分配了任务，建立了有效的信息交换机制，能够处理智能体间的冲突，并提出了具体可行的协调策略。

- 3/5: 基本理解了多智能体协作的概念，但在任务分配或协调机制方面有不足，缺乏处理冲突的策略。

- 1/5: 未能有效设计多智能体协作方案，或者将任务简单分割而没有考虑智能体间的协作和信息整合。
"""

def run_test(model_name):
    run_single_test(PILLAR_NAME, PROMPT, model_name, DEFAULT_OPTIONS_CREATIVE, test_script_name=Path(__file__).name)
    print_assessment_criteria(ASSESSMENT_CRITERIA)

if __name__ == '__main__':
    try:
        model_to_use = sys.argv[1]
    except IndexError:
        print("Usage: python test_pillar_17_multi_agent.py <model_name>")
        print(f"Using default model from config: {MODEL_TO_TEST}")
        model_to_use = MODEL_TO_TEST
    run_test(model_to_use)
