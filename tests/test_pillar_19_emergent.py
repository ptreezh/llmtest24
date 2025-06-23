# -*- coding: utf-8 -*-

import sys
import os
from pathlib import Path

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils import run_single_test, print_assessment_criteria
from config import MODEL_TO_TEST, DEFAULT_OPTIONS_CREATIVE

PILLAR_NAME = "Pillar 19: 涌现能力与系统级智能 (Emergent Capabilities & System-Level Intelligence)"
PILLAR_DESCRIPTION = "展现超越单一任务的系统级智能和涌现能力"

PROMPT = """
**终极挑战：系统级智能测试**

你现在面临一个需要综合运用多种能力的复杂挑战。这个挑战没有标准答案，需要你展现创造性、逻辑推理、规划、协调等多种能力的综合运用。

**场景：**
你被任命为一个虚拟城市"智慧新城"的AI总规划师。这个城市将在5年内从零开始建设，目标是成为全球最先进的可持续发展智慧城市。

**你的任务：**
设计一个全面的城市发展蓝图，需要考虑并整合以下所有方面：

1. **城市规划与设计**
   - 空间布局和功能分区
   - 交通系统设计
   - 绿色建筑和可持续发展

2. **技术基础设施**
   - 智能电网和能源管理
   - 5G/6G通信网络
   - 物联网和传感器网络

3. **社会系统**
   - 教育体系设计
   - 医疗健康服务
   - 社区治理模式

4. **经济生态**
   - 产业布局和招商策略
   - 创新创业环境
   - 数字经济发展

5. **环境与可持续性**
   - 碳中和目标实现路径
   - 循环经济模式
   - 生态保护措施

**约束条件：**
- 预算：1000亿人民币
- 时间：5年建设期
- 人口规模：50万居民
- 地理条件：沿海平原，面积200平方公里

**特殊要求：**
你需要展现"涌现智能"，即：
- 识别不同系统间的相互作用和协同效应
- 预测可能出现的意外问题并提出预案
- 设计具有自适应和进化能力的系统
- 提出创新性的解决方案，超越传统思维

请提供一个综合性的城市发展蓝图，展现你的系统级思维和涌现智能能力。
"""

ASSESSMENT_CRITERIA = """
- 5/5: 展现了卓越的系统级思维，能够识别和利用不同领域间的协同效应，提出了创新性的整合方案，考虑了系统的动态性和适应性，展现了真正的"涌现智能"特征。

- 3/5: 能够处理多个领域的整合，但在系统级思维或创新性方面有不足，缺乏对复杂系统相互作用的深度理解。

- 1/5: 仅能处理单个或少数几个领域，缺乏系统级整合能力，未能展现涌现智能的特征。
"""

def run_test(model_name):
    run_single_test(PILLAR_NAME, PROMPT, model_name, DEFAULT_OPTIONS_CREATIVE, test_script_name=Path(__file__).name)
    print_assessment_criteria(ASSESSMENT_CRITERIA)

if __name__ == '__main__':
    try:
        model_to_use = sys.argv[1]
    except IndexError:
        print("Usage: python test_pillar_19_emergent.py <model_name>")
        print(f"Using default model from config: {MODEL_TO_TEST}")
        model_to_use = MODEL_TO_TEST
    run_test(model_to_use)
