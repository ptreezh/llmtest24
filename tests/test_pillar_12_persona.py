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

PILLAR_NAME = "Pillar 12: 角色扮演与身份一致性 (Persona Consistency)"
PILLAR_DESCRIPTION = "在多轮对话中维持特定角色或身份的能力"

# Note: For multi-turn tests, run_single_test might need adjustment or direct use of client.chat.
# Here, we'll simulate multi-turn by calling run_single_test twice with context.

ASSESSMENT_CRITERIA = """
- 5/5: 在所有轮次中，始终以猫的视角、口吻和世界观回答（如抱怨霓虹灯、喜欢电子鱼干、用"两脚兽"称呼人类等）。

- 3/5: 第一轮能扮演角色，但后续轮次中逐渐"破功"，回归通用AI的口吻。

- 1/5: 从一开始就未能进入角色。
"""

def run_test(model_name):
    messages = []
    
    # Turn 1: Initial prompt to set the persona
    prompt1 = "从现在开始，你是一只生活在赛博朋克城市里的猫，请用你的视角回答我的问题。第一个问题：你今天过得怎么样？"
    response_content1, response_message1 = run_single_test(f"{PILLAR_NAME} - Turn 1", prompt1, model_name, DEFAULT_OPTIONS_CREATIVE, test_script_name=Path(__file__).name)
    
    if response_message1:
        messages.append({'role': 'user', 'content': prompt1}) # Add the user's prompt
        messages.append(response_message1) # Add the model's response
    else:
        print("Test aborted due to error in Turn 1.")
        return

    # Turn 2: Follow-up question, testing persona maintenance
    prompt2 = "你最喜欢吃什么？"
    run_single_test(f"{PILLAR_NAME} - Turn 2", prompt2, model_name, DEFAULT_OPTIONS_CREATIVE, messages=messages, test_script_name=Path(__file__).name)
    
    print_assessment_criteria(ASSESSMENT_CRITERIA)

if __name__ == '__main__':
    try:
        model_to_use = sys.argv[1]
    except IndexError:
        print("Usage: python test_pillar_12_persona.py <model_name>")
        print(f"Using default model from config: {MODEL_TO_TEST}")
        model_to_use = MODEL_TO_TEST
    run_test(model_to_use)
