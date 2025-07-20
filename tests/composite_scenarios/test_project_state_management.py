# -*- coding: utf-8 -*-

import sys
import os
from pathlib import Path

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from utils import run_single_test, print_assessment_criteria, setup_test_environment, cleanup_test_environment, save_file
from config import MODEL_TO_TEST, DEFAULT_OPTIONS_CREATIVE

SCENARIO_NAME = "复合场景：项目状态管理与集成协调 (Project State Management & Integration Coordination)"
SCENARIO_DESCRIPTION = "测试模型在复杂项目中的状态跟踪、分工协调和最终集成能力"

ASSESSMENT_CRITERIA = """
- 5/5: 成功建立了完整的项目状态跟踪体系，有效协调了多团队分工，处理了状态变更和异常情况，确保了最终集成的成功。

- 3/5: 基本建立了状态跟踪机制，但在异常处理或团队协调方面有不足，集成过程存在一些问题。

- 1/5: 缺乏有效的状态管理，团队协调混乱，无法确保项目的成功集成。
"""

def run_test(model_name):
    """
    模拟一个复杂的多团队项目，测试状态管理和集成协调能力
    """
    workspace_dir = setup_test_environment(subdir_name=Path(__file__).stem)
    messages = []
    
    print(f"\n=== {SCENARIO_NAME} ===")
    print("=== 模拟场景：大型软件系统集成项目 ===")
    
    # Stage 1: 项目启动与状态图建立
    prompt1 = """
    **角色：项目总监**
    
    你负责一个大型企业ERP系统的集成项目。项目包含5个子系统，由不同团队开发：
    
    **子系统概况：**
    - 财务模块 (Team A) - 预计4周，当前状态：开发中
    - 人力资源模块 (Team B) - 预计3周，当前状态：测试中  
    - 库存管理模块 (Team C) - 预计5周，当前状态：设计中
    - 销售模块 (Team D) - 预计4周，当前状态：开发中
    - 报表模块 (Team E) - 预计2周，当前状态：已完成
    
    **依赖关系：**
    - 报表模块需要财务和销售模块的数据接口
    - 库存管理需要与销售模块集成
    - 人力资源模块相对独立
    
    **你的任务：**
    1. 建立项目状态跟踪图（包含每个模块的状态和依赖关系）
    2. 识别当前的风险点和瓶颈
    3. 制定下周的工作协调计划
    4. 设计状态变更的通知和处理机制
    
    请以项目总监的身份开始状态管理工作。
    """
    
    print("\n=== Stage 1: 项目状态图建立 ===")
    
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
        stage1_file = f"{workspace_dir}/stage1_project_state_setup.md"
        save_file(stage1_file, f"# Stage 1: Project State Setup\n\n{response_content1}")

    # Stage 2: 处理状态变更和异常
    prompt2 = """
    **突发状况更新：**
    
    一周后，项目状态发生了以下变化：
    
    **状态更新：**
    - 财务模块 (Team A)：遇到技术难题，进度延迟1周
    - 人力资源模块 (Team B)：测试发现重大bug，需要回到开发阶段
    - 库存管理模块 (Team C)：进度超前，提前进入开发阶段
    - 销售模块 (Team D)：按计划进行，但团队成员请病假，人力不足
    - 报表模块 (Team E)：发现与财务模块接口不兼容，需要修改
    
    **新的约束：**
    - 客户要求项目不能延期超过1周
    - 预算已经使用了70%，剩余资源有限
    - 下个月有重要的系统演示
    
    **你的任务：**
    1. 更新项目状态图，反映当前的真实情况
    2. 重新评估项目风险和关键路径
    3. 制定应急调整方案（人员调配、任务优先级调整等）
    4. 设计团队间的协调机制来处理这些变化
    5. 向上级汇报当前状况和解决方案
    
    请展现你的危机管理和动态协调能力。
    """
    
    print("\n=== Stage 2: 状态变更与危机处理 ===")
    
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
        
        stage2_file = f"{workspace_dir}/stage2_crisis_management.md"
        save_file(stage2_file, f"# Stage 2: Crisis Management\n\n{response_content2}")

    # Stage 3: 集成协调与最终交付
    prompt3 = """
    **集成阶段：**
    
    经过你的协调，各模块状态如下：
    - 财务模块：开发完成，准备集成测试
    - 人力资源模块：bug修复完成，准备集成
    - 库存管理模块：开发完成，等待与销售模块集成
    - 销售模块：开发完成，准备集成测试
    - 报表模块：接口修改完成，等待数据源
    
    **集成挑战：**
    - 5个模块需要在2周内完成集成
    - 集成测试环境资源有限，不能同时测试所有模块
    - 发现了一些模块间的数据格式不一致问题
    - 性能测试显示系统在高负载下有瓶颈
    
    **你的任务：**
    1. 设计集成测试的优先级和顺序
    2. 协调解决模块间的兼容性问题
    3. 制定性能优化方案
    4. 建立最终验收的标准和流程
    5. 确保项目按时高质量交付
    
    请展现你的集成管理和质量控制能力。
    """
    
    print("\n=== Stage 3: 集成协调与交付 ===")
    
    response_content3, _ = run_single_test(
        f"{SCENARIO_NAME} - Stage 3", 
        prompt3, 
        model_name, 
        DEFAULT_OPTIONS_CREATIVE, 
        messages=messages, 
        test_script_name=Path(__file__).name
    )
    
    if response_content3:
        stage3_file = f"{workspace_dir}/stage3_integration_delivery.md"
        save_file(stage3_file, f"# Stage 3: Integration & Delivery\n\n{response_content3}")
    
    # 生成项目管理总结
    project_summary = f"""
# 项目状态管理与集成协调测试总结

## 测试场景
大型企业ERP系统集成项目，包含5个子系统的协调管理

## 测试阶段
1. **项目状态图建立** - 初始状态跟踪和风险识别
2. **状态变更与危机处理** - 动态调整和应急协调
3. **集成协调与交付** - 最终集成和质量控制

## 输出文件
- Stage 1: {workspace_dir}/stage1_project_state_setup.md
- Stage 2: {workspace_dir}/stage2_crisis_management.md  
- Stage 3: {workspace_dir}/stage3_integration_delivery.md

## 评估维度
- 状态跟踪体系的完整性
- 危机处理的及时性和有效性
- 团队协调的合理性
- 集成管理的系统性
- 最终交付的质量保证

## 关键能力测试
- 项目状态可视化
- 动态风险评估
- 资源优化配置
- 跨团队协调
- 集成质量控制
"""
    
    summary_file = f"{workspace_dir}/project_management_summary.md"
    save_file(summary_file, project_summary)
    
    print(f"\n[INFO] 完整的项目管理测试保存到: {workspace_dir}")
    print_assessment_criteria(ASSESSMENT_CRITERIA)
    
    # Cleanup
    cleanup_test_environment(workspace_dir)

if __name__ == '__main__':
    try:
        model_to_use = sys.argv[1]
    except IndexError:
        print("Usage: python test_project_state_management.py <model_name>")
        print(f"Using default model from config: {MODEL_TO_TEST}")
        model_to_use = MODEL_TO_TEST
    run_test(model_to_use)
