# -*- coding: utf-8 -*-

import sys
import json
from pathlib import Path
from utils import run_single_test, print_assessment_criteria, setup_test_environment, cleanup_test_environment, save_file
from config import MODEL_TO_TEST, DEFAULT_OPTIONS_CREATIVE

SCENARIO_NAME = "复合场景：跨能力整合测试 (Cross-Capability Integration)"
SCENARIO_DESCRIPTION = "测试模型同时运用多种核心能力解决复杂问题的能力"

ASSESSMENT_CRITERIA = """
- 5/5: 成功整合了逻辑推理、创意生成、结构化输出、工具使用等多种能力，解决方案完整且实用，展现了优秀的综合能力。

- 3/5: 能够运用多种能力，但整合程度不够深入，或某些能力的运用不够熟练。

- 1/5: 只能运用单一或少数几种能力，缺乏有效的能力整合。
"""

def run_test(model_name):
    """
    执行跨能力整合测试，要求模型同时运用多种核心能力
    """
    workspace_dir = setup_test_environment(subdir_name=Path(__file__).stem)
    
    prompt = """
    **综合能力挑战：智能客服系统设计**
    
    你需要为一家在线教育公司设计一个智能客服系统。这个任务需要你综合运用多种能力：
    
    **任务要求：**
    
    1. **逻辑推理能力**：分析客服场景中的问题分类和处理逻辑
    2. **创意生成能力**：设计创新的客服交互方式和用户体验
    3. **结构化输出能力**：生成规范的系统配置文件和API接口定义
    4. **工具使用能力**：设计客服机器人需要调用的外部工具和服务
    5. **规划能力**：制定系统开发和部署的详细计划
    
    **具体输出要求：**
    
    1. **问题分类树**（JSON格式）：
       - 至少包含5个主要问题类别
       - 每个类别下至少3个子问题
       - 为每个问题定义处理优先级（1-5级）
    
    2. **智能回复模板**：
       - 设计至少3种不同风格的回复模板（正式、友好、专业）
       - 每种模板包含开场白、问题确认、解决方案、结束语
    
    3. **工具调用配置**（JSON Schema格式）：
       - 定义查询课程信息的工具
       - 定义查询订单状态的工具
       - 定义转人工客服的工具
    
    4. **创新功能设计**：
       - 提出至少2个创新的客服功能
       - 解释这些功能如何提升用户体验
    
    5. **实施计划**：
       - 分阶段的开发计划（至少3个阶段）
       - 每个阶段的时间安排和关键里程碑
    
    请确保你的输出结构清晰，JSON格式正确，并且展现出对不同能力的熟练运用。
    """
    
    print(f"\n=== {SCENARIO_NAME} ===")
    
    response_content, _ = run_single_test(
        SCENARIO_NAME, 
        prompt, 
        model_name, 
        DEFAULT_OPTIONS_CREATIVE, 
        test_script_name=Path(__file__).name
    )
    
    # 自动化检查
    print("\n--- AUTOMATED CAPABILITY CHECKS ---")
    
    if response_content and "ERROR:" not in response_content:
        # 保存完整响应
        full_response_file = f"{workspace_dir}/intelligent_customer_service_design.md"
        save_file(full_response_file, f"# Intelligent Customer Service System Design\n\n{response_content}")
        
        # 检查是否包含JSON结构
        json_found = False
        if "```json" in response_content or "{" in response_content:
            json_found = True
            print("PASS: JSON structures detected in response.")
        else:
            print("FAIL: No JSON structures found.")
        
        # 检查是否包含创新元素
        innovation_keywords = ["创新", "新颖", "独特", "智能", "自动", "个性化", "AI", "机器学习"]
        innovation_found = any(keyword in response_content for keyword in innovation_keywords)
        if innovation_found:
            print("PASS: Innovation elements detected.")
        else:
            print("FAIL: Limited innovation elements found.")
        
        # 检查是否包含规划元素
        planning_keywords = ["阶段", "计划", "时间", "里程碑", "步骤", "实施", "部署"]
        planning_found = any(keyword in response_content for keyword in planning_keywords)
        if planning_found:
            print("PASS: Planning elements detected.")
        else:
            print("FAIL: Limited planning elements found.")
        
        # 检查逻辑结构
        if "分类" in response_content and "优先级" in response_content:
            print("PASS: Logical categorization detected.")
        else:
            print("FAIL: Limited logical structure found.")
        
        print(f"\n[INFO] Full design saved to: {full_response_file}")
    else:
        print("FAIL: No valid response generated.")
    
    print("--- END OF CHECKS ---")
    
    print_assessment_criteria(ASSESSMENT_CRITERIA)
    
    # Cleanup
    cleanup_test_environment(workspace_dir)

if __name__ == '__main__':
    try:
        model_to_use = sys.argv[1]
    except IndexError:
        print("Usage: python test_cross_capability_integration.py <model_name>")
        print(f"Using default model from config: {MODEL_TO_TEST}")
        model_to_use = MODEL_TO_TEST
    run_test(model_to_use)
