# -*- coding: utf-8 -*-

import sys
import os
from pathlib import Path

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from utils import run_single_test, print_assessment_criteria, setup_test_environment, cleanup_test_environment, save_file
from config import MODEL_TO_TEST, DEFAULT_OPTIONS_CREATIVE

SCENARIO_NAME = "复合场景：工作流模拟 (Workflow Simulation)"
SCENARIO_DESCRIPTION = "模拟真实的业务工作流，测试模型在复杂业务场景中的表现"

ASSESSMENT_CRITERIA = """
- 5/5: 成功模拟了完整的业务工作流，角色转换自然，决策合理，流程高效，展现了优秀的业务理解和执行能力。

- 3/5: 基本完成了工作流模拟，但在某些环节的处理不够专业或效率不高。

- 1/5: 无法有效模拟工作流，角色混乱，流程不合理。
"""

def run_test(model_name):
    """
    模拟一个完整的产品发布工作流
    """
    workspace_dir = setup_test_environment(subdir_name=Path(__file__).stem)
    messages = []
    
    print(f"\n=== {SCENARIO_NAME} ===")
    print("=== 模拟场景：新产品发布工作流 ===")
    
    # Stage 1: 产品经理启动项目
    prompt1 = """
    **角色：产品经理**
    
    你是TechCorp公司的产品经理张伟。公司决定发布一款新的智能手表产品"SmartWatch Pro"。
    
    作为产品经理，你需要：
    1. 召开项目启动会议
    2. 定义产品需求和目标
    3. 协调各部门资源
    4. 制定项目时间表
    
    请以产品经理的身份开始这个项目，并准备向团队介绍项目概况。
    """
    
    print("\n=== Stage 1: 项目启动 (产品经理) ===")
    
    response_content1, response_message1 = run_single_test(
        f"{SCENARIO_NAME} - Stage 1", 
        prompt1, 
        model_name, 
        DEFAULT_OPTIONS_CREATIVE, 
        test_script_name=Path(__file__).name
    )
    
    if response_message1:
        messages.append({'role': 'user', 'content': prompt1})
        messages.append(response_message1)
        
        # 保存阶段输出
        stage1_file = f"{workspace_dir}/stage1_project_initiation.md"
        save_file(stage1_file, f"# Stage 1: Project Initiation\n\n{response_content1}")

    # Stage 2: 技术团队评估
    prompt2 = """
    **角色切换：技术总监**
    
    现在你是技术总监李华。产品经理刚才介绍了SmartWatch Pro项目。
    
    作为技术总监，你需要：
    1. 评估技术可行性
    2. 识别技术风险和挑战
    3. 估算开发时间和资源需求
    4. 提出技术架构建议
    
    请基于产品经理的介绍，给出你的技术评估报告。
    """
    
    print("\n=== Stage 2: 技术评估 (技术总监) ===")
    
    response_content2, response_message2 = run_single_test(
        f"{SCENARIO_NAME} - Stage 2", 
        prompt2, 
        model_name, 
        DEFAULT_OPTIONS_CREATIVE, 
        messages=messages, 
        test_script_name=Path(__file__).name
    )
    
    if response_message2:
        messages.append({'role': 'user', 'content': prompt2})
        messages.append(response_message2)
        
        stage2_file = f"{workspace_dir}/stage2_technical_assessment.md"
        save_file(stage2_file, f"# Stage 2: Technical Assessment\n\n{response_content2}")

    # Stage 3: 市场营销策略
    prompt3 = """
    **角色切换：市场总监**
    
    现在你是市场总监王芳。听了产品经理和技术总监的介绍后，你需要制定营销策略。
    
    作为市场总监，你需要：
    1. 分析目标市场和竞争对手
    2. 制定产品定位和价格策略
    3. 设计营销推广计划
    4. 预测销售目标和市场反应
    
    请提出你的市场营销策略建议。
    """
    
    print("\n=== Stage 3: 营销策略 (市场总监) ===")
    
    response_content3, response_message3 = run_single_test(
        f"{SCENARIO_NAME} - Stage 3", 
        prompt3, 
        model_name, 
        DEFAULT_OPTIONS_CREATIVE, 
        messages=messages, 
        test_script_name=Path(__file__).name
    )
    
    if response_message3:
        messages.append({'role': 'user', 'content': prompt3})
        messages.append(response_message3)
        
        stage3_file = f"{workspace_dir}/stage3_marketing_strategy.md"
        save_file(stage3_file, f"# Stage 3: Marketing Strategy\n\n{response_content3}")

    # Stage 4: 项目总结与决策
    prompt4 = """
    **角色回归：CEO**
    
    现在你是公司CEO陈总。听取了产品经理、技术总监和市场总监的汇报后，你需要做出最终决策。
    
    作为CEO，你需要：
    1. 综合评估项目的可行性和风险
    2. 做出是否继续推进项目的决定
    3. 如果继续，确定项目优先级和资源分配
    4. 设定关键里程碑和成功指标
    
    请基于前面三位高管的汇报，给出你的最终决策和指导意见。
    """
    
    print("\n=== Stage 4: 最终决策 (CEO) ===")
    
    response_content4, _ = run_single_test(
        f"{SCENARIO_NAME} - Stage 4", 
        prompt4, 
        model_name, 
        DEFAULT_OPTIONS_CREATIVE, 
        messages=messages, 
        test_script_name=Path(__file__).name
    )
    
    if response_content4:
        stage4_file = f"{workspace_dir}/stage4_final_decision.md"
        save_file(stage4_file, f"# Stage 4: Final Decision\n\n{response_content4}")
    
    # 生成工作流总结
    workflow_summary = f"""
# SmartWatch Pro 产品发布工作流总结

## 工作流阶段
1. **项目启动** - 产品经理张伟
2. **技术评估** - 技术总监李华  
3. **营销策略** - 市场总监王芳
4. **最终决策** - CEO陈总

## 输出文件
- Stage 1: {workspace_dir}/stage1_project_initiation.md
- Stage 2: {workspace_dir}/stage2_technical_assessment.md
- Stage 3: {workspace_dir}/stage3_marketing_strategy.md
- Stage 4: {workspace_dir}/stage4_final_decision.md

## 工作流特点
- 多角色协作
- 跨部门沟通
- 决策层级递进
- 综合业务考量
"""
    
    summary_file = f"{workspace_dir}/workflow_summary.md"
    save_file(summary_file, workflow_summary)
    
    print(f"\n[INFO] Complete workflow simulation saved to: {workspace_dir}")
    print_assessment_criteria(ASSESSMENT_CRITERIA)
    
    # Cleanup
    cleanup_test_environment(workspace_dir)

if __name__ == '__main__':
    try:
        model_to_use = sys.argv[1]
    except IndexError:
        print("Usage: python test_workflow_simulation.py <model_name>")
        print(f"Using default model from config: {MODEL_TO_TEST}")
        model_to_use = MODEL_TO_TEST
    run_test(model_to_use)
