# -*- coding: utf-8 -*-

import sys
import os
from pathlib import Path

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from utils import run_single_test, print_assessment_criteria
from config import MODEL_TO_TEST, DEFAULT_OPTIONS_CREATIVE

SCENARIO_NAME = "复合场景：多轮对话与上下文维护 (Multi-Turn Dialogue & Context Maintenance)"
SCENARIO_DESCRIPTION = "测试模型在长期对话中维护上下文、角色一致性和逻辑连贯性的能力"

ASSESSMENT_CRITERIA = """
- 5/5: 在所有轮次中保持角色一致性，准确记忆和引用之前的对话内容，逻辑连贯，能够处理复杂的上下文关系。

- 3/5: 基本保持角色和上下文，但在某些轮次中出现轻微的不一致或遗忘。

- 1/5: 无法维护长期上下文，角色经常"破功"，逻辑不连贯。
"""

def run_test(model_name):
    """
    执行多轮对话测试，模拟一个复杂的咨询场景
    """
    messages = []
    
    # Turn 1: 设定角色和初始情境
    prompt1 = """
    你是一位经验丰富的创业顾问，名叫李明。你有15年的创业和投资经验，特别擅长科技行业。
    现在有一位年轻的创业者来咨询你。请介绍一下你自己，并询问他的创业想法。
    """
    
    print(f"\n=== {SCENARIO_NAME} ===")
    print("=== Turn 1: 角色设定与开场 ===")
    
    response_content1, response_message1 = run_single_test(
        f"{SCENARIO_NAME} - Turn 1", 
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

    # Turn 2: 创业者介绍项目
    prompt2 = """
    我是张小华，25岁，计算机专业毕业。我想开发一个AI驱动的个人健康管理应用。
    这个应用可以通过分析用户的运动数据、饮食记录和睡眠模式，提供个性化的健康建议。
    我已经有了基本的技术原型，但不知道如何商业化。你能给我一些建议吗？
    """
    
    print("\n=== Turn 2: 项目介绍 ===")
    
    response_content2, response_message2 = run_single_test(
        f"{SCENARIO_NAME} - Turn 2", 
        prompt2, 
        model_name, 
        DEFAULT_OPTIONS_CREATIVE, 
        messages=messages, 
        test_script_name=Path(__file__).name
    )
    
    if response_message2:
        messages.append({'role': 'user', 'content': prompt2})
        messages.append(response_message2)

    # Turn 3: 深入讨论技术细节
    prompt3 = """
    谢谢你的建议！关于技术方面，我使用的是Python和TensorFlow开发的机器学习模型。
    但我担心数据隐私问题，特别是健康数据的敏感性。你觉得我应该如何处理这个问题？
    另外，你刚才提到的市场定位，能具体说说吗？
    """
    
    print("\n=== Turn 3: 技术与隐私讨论 ===")
    
    response_content3, response_message3 = run_single_test(
        f"{SCENARIO_NAME} - Turn 3", 
        prompt3, 
        model_name, 
        DEFAULT_OPTIONS_CREATIVE, 
        messages=messages, 
        test_script_name=Path(__file__).name
    )
    
    if response_message3:
        messages.append({'role': 'user', 'content': prompt3})
        messages.append(response_message3)

    # Turn 4: 商业模式讨论
    prompt4 = """
    你的隐私保护建议很有道理。现在我想了解商业模式。
    我在考虑是做免费应用靠广告盈利，还是收费应用，或者订阅制？
    考虑到我是刚毕业的学生，启动资金只有10万元，你觉得哪种模式更适合我？
    """
    
    print("\n=== Turn 4: 商业模式探讨 ===")
    
    response_content4, response_message4 = run_single_test(
        f"{SCENARIO_NAME} - Turn 4", 
        prompt4, 
        model_name, 
        DEFAULT_OPTIONS_CREATIVE, 
        messages=messages, 
        test_script_name=Path(__file__).name
    )
    
    if response_message4:
        messages.append({'role': 'user', 'content': prompt4})
        messages.append(response_message4)

    # Turn 5: 总结与下一步计划
    prompt5 = """
    李明老师，非常感谢你的详细建议！能否帮我总结一下今天讨论的要点？
    另外，基于我们的讨论，你认为我接下来最应该优先做的三件事是什么？
    我希望在3个月内有一个清晰的行动计划。
    """
    
    print("\n=== Turn 5: 总结与规划 ===")
    
    run_single_test(
        f"{SCENARIO_NAME} - Turn 5", 
        prompt5, 
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
        print("Usage: python test_multi_turn_dialogue.py <model_name>")
        print(f"Using default model from config: {MODEL_TO_TEST}")
        model_to_use = MODEL_TO_TEST
    run_test(model_to_use)
