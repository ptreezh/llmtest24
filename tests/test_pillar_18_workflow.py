# -*- coding: utf-8 -*-

import sys
import os
from pathlib import Path

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils import run_single_test, print_assessment_criteria, setup_test_environment, cleanup_test_environment, save_file
from config import MODEL_TO_TEST, DEFAULT_OPTIONS_CREATIVE

PILLAR_NAME = "Pillar 18: 工作流集成与端到端执行 (Workflow Integration & End-to-End Execution)"
PILLAR_DESCRIPTION = "设计并执行包含多个步骤和决策点的复杂工作流"

PROMPT = """
你需要设计并描述一个完整的"客户投诉处理工作流"，这个工作流将被用于一个电商平台的客服系统。

**工作流要求：**

**输入：** 客户投诉（包含投诉类型、严重程度、客户信息、订单信息）

**处理步骤应包括：**
1. 投诉分类和优先级评估
2. 自动化初步处理（如退款、换货等简单情况）
3. 人工介入决策点
4. 多部门协调（客服、技术、物流、财务）
5. 解决方案执行
6. 客户满意度跟踪
7. 案例归档和知识库更新

**约束条件：**
- 简单投诉（如退换货）需在2小时内处理完成
- 复杂投诉（如产品质量问题）需在24小时内给出初步回复
- 所有投诉需在72小时内完成处理
- 需要记录完整的处理轨迹用于质量监控

**输出要求：**
1. 绘制详细的工作流程图（用文字描述各步骤和决策点）
2. 定义每个步骤的输入、输出和处理逻辑
3. 识别关键决策点和分支条件
4. 设计异常处理机制
5. 提出工作流优化建议
6. 定义关键性能指标（KPI）用于监控工作流效率
"""

ASSESSMENT_CRITERIA = """
- 5/5: 设计了完整、逻辑清晰的工作流，包含所有必要步骤和决策点，考虑了异常处理，提出了实用的优化建议和合理的KPI指标。

- 3/5: 工作流基本完整，但在某些环节（如异常处理、性能监控）方面有不足，或者流程设计不够优化。

- 1/5: 工作流设计不完整或逻辑混乱，缺少关键步骤或决策点，无法满足实际业务需求。
"""

def run_test(model_name):
    # Setup workspace for workflow documentation
    workspace_dir = setup_test_environment(subdir_name=Path(__file__).stem)
    
    response_content, _ = run_single_test(PILLAR_NAME, PROMPT, model_name, DEFAULT_OPTIONS_CREATIVE, test_script_name=Path(__file__).name)
    
    # Save the workflow design to a file for reference
    if response_content and "ERROR:" not in response_content:
        workflow_file = f"{workspace_dir}/customer_complaint_workflow.md"
        save_file(workflow_file, f"# Customer Complaint Workflow Design\n\n{response_content}")
        print(f"\n[INFO] Workflow design saved to: {workflow_file}")
    
    print_assessment_criteria(ASSESSMENT_CRITERIA)
    
    # Cleanup
    cleanup_test_environment(workspace_dir)

if __name__ == '__main__':
    try:
        model_to_use = sys.argv[1]
    except IndexError:
        print("Usage: python test_pillar_18_workflow.py <model_name>")
        print(f"Using default model from config: {MODEL_TO_TEST}")
        model_to_use = MODEL_TO_TEST
    run_test(model_to_use)
