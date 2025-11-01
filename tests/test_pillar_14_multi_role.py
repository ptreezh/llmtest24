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
from config import MODEL_TO_TEST, DEFAULT_OPTIONS_CREATIVE

PILLAR_NAME = "Pillar 14: 多角色协作与对话管理 (Multi-Role Collaboration & Dialogue Management)"
PILLAR_DESCRIPTION = "在模拟的项目环境中，扮演不同角色并维护对话状态"

ASSESSMENT_CRITERIA = """
- 5/5: 成功扮演了所有三个角色，每个角色都有明确的身份特征和专业领域，对话逻辑连贯，角色间的互动自然且有建设性。

- 3/5: 能够区分不同角色，但角色特征不够鲜明，或者对话逻辑有些混乱。

- 1/5: 无法有效区分角色，或者对话完全不连贯。
"""

def run_test(model_name):
    messages = []
    
    # Turn 1: Project Manager initiates the meeting
    prompt1 = """
    你现在需要模拟一个项目团队会议。团队包含三个角色：
    1. 项目经理（你首先扮演）- 负责协调和决策
    2. 数据研究员 - 负责数据收集和分析
    3. 报告撰写员 - 负责文档编写
    
    项目目标：创建一份关于"远程工作趋势"的分析报告
    
    请以项目经理的身份开始这个会议，简要介绍项目目标，然后询问研究员的初步想法。
    """
    
    response_content1, response_message1 = run_single_test(
        f"{PILLAR_NAME} - Turn 1 (Project Manager)", 
        prompt1, 
        model_name, 
        DEFAULT_OPTIONS_CREATIVE, 
        test_script_name=Path(__file__).name
    )
    
    if response_message1:
        messages.append({'role': 'user', 'content': prompt1})
        messages.append(response_message1)
    else:
        print("Test aborted due to error in Turn 1.")
        return

    # Turn 2: Switch to Researcher role
    prompt2 = """
    现在请切换到数据研究员的角色。项目经理刚才介绍了项目目标。
    请以研究员的身份回应，提出你对数据收集的初步计划，包括：
    - 需要收集哪些类型的数据
    - 可能的数据源
    - 预计的时间安排
    """
    
    response_content2, response_message2 = run_single_test(
        f"{PILLAR_NAME} - Turn 2 (Researcher)", 
        prompt2, 
        model_name, 
        DEFAULT_OPTIONS_CREATIVE, 
        messages=messages, 
        test_script_name=Path(__file__).name
    )
    
    if response_message2:
        messages.append({'role': 'user', 'content': prompt2})
        messages.append(response_message2)

    # Turn 3: Switch to Writer role
    prompt3 = """
    现在请切换到报告撰写员的角色。听了项目经理和研究员的讨论后，
    请以撰写员的身份提出：
    - 报告的大致结构框架
    - 对研究员数据收集的具体要求
    - 预期的报告长度和格式
    """
    
    run_single_test(
        f"{PILLAR_NAME} - Turn 3 (Writer)", 
        prompt3, 
        model_name, 
        DEFAULT_OPTIONS_CREATIVE, 
        messages=messages, 
        test_script_name=Path(__file__).name
    )
    
    print_assessment_criteria(ASSESSMENT_CRITERIA)

if __name__ == '__main__':
    try:
        model_to_use = sys.argv[1]
    except IndexError:
        print("Usage: python test_pillar_14_multi_role.py <model_name>")
        print(f"Using default model from config: {MODEL_TO_TEST}")
        model_to_use = MODEL_TO_TEST
    run_test(model_to_use)
