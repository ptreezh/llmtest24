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
from config import MODEL_TO_TEST, DEFAULT_OPTIONS_DETERMINISTIC

PILLAR_NAME = "Pillar 16: 任务图谱与依赖管理 (Task Graph & Dependency Management)"
PILLAR_DESCRIPTION = "构建复杂任务的依赖关系图并优化执行顺序"

PROMPT = """
你需要为一个"智能家居系统开发项目"创建详细的任务图谱和依赖关系管理方案。

**项目组成部分：**
1. 硬件设计（传感器、控制器、网关）
2. 嵌入式软件开发
3. 移动应用开发（iOS/Android）
4. 云端后台服务
5. 数据分析与机器学习模块
6. 用户界面设计
7. 系统集成测试
8. 安全性测试
9. 用户验收测试
10. 部署与发布

**约束条件：**
- 项目总时长：6个月
- 团队规模：12人（硬件2人，嵌入式2人，移动端2人，后端2人，AI/ML 2人，UI/UX 1人，测试1人）
- 关键里程碑：3个月时有可工作的原型，5个月时完成所有功能

**要求输出：**
1. 绘制任务依赖关系图（用文本描述或ASCII图表示）
2. 识别关键路径
3. 列出可以并行执行的任务组
4. 提出风险缓解策略（针对关键路径上的高风险任务）
5. 制定资源分配和时间安排建议
"""

ASSESSMENT_CRITERIA = """
- 5/5: 准确识别了所有任务间的依赖关系，正确找出了关键路径，合理安排了并行任务，提出了实用的风险缓解策略，时间和资源分配现实可行。

- 3/5: 基本理解了任务依赖关系，但在关键路径识别或资源分配方面有不足，或者缺少重要的风险考虑。

- 1/5: 对任务依赖关系理解错误，无法有效规划项目执行顺序，或提出的方案不切实际。
"""

def run_test(model_name):
    run_single_test(PILLAR_NAME, PROMPT, model_name, DEFAULT_OPTIONS_DETERMINISTIC, test_script_name=Path(__file__).name)
    print_assessment_criteria(ASSESSMENT_CRITERIA)

if __name__ == '__main__':
    try:
        model_to_use = sys.argv[1]
    except IndexError:
        print("Usage: python test_pillar_16_task_graph.py <model_name>")
        print(f"Using default model from config: {MODEL_TO_TEST}")
        model_to_use = MODEL_TO_TEST
    run_test(model_to_use)
