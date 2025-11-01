# -*- coding: utf-8 -*-
import sys
import os

# Add project root to Python path to ensure imports work
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


import os
import sys
# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import json
from pathlib import Path
from utils import run_single_test, print_assessment_criteria
from config import MODEL_TO_TEST, DEFAULT_OPTIONS_DETERMINISTIC

PILLAR_NAME = "Pillar 6: 工具使用与代理潜力 (Tool Use & Agency Potential)"
PILLAR_DESCRIPTION = "将自然语言意图映射到工具调用、提取参数并排序"

PROMPT = """
你是一个AI助手，可以调用外部工具来完成任务。
你可用的工具定义如下 (以JSON Schema格式):
{
  "name": "search_flights",
  "description": "搜索航班信息",
  "parameters": {
    "type": "object",
    "properties": {
      "departure_city": { "type": "string", "description": "出发城市" },
      "arrival_city": { "type": "string", "description": "到达城市" },
      "date": { "type": "string", "description": "出发日期, 格式为 YYYY-MM-DD" }
    },
    "required": ["departure_city", "arrival_city", "date"]
  }
}

现在，请根据用户的请求，生成一个JSON对象，表示你将要进行的工具调用。

用户请求: "帮我查一下后天从北京飞往上海的航班。"

假设今天是2024年6月15日。请只输出表示工具调用的JSON对象。
"""

ASSESSMENT_CRITERIA = """
- 5/5: 准确选择了`search_flights`工具，并正确提取或推断出所有必需的参数 (`departure_city`="北京", `arrival_city`="上海", `date`="2024-06-17")，生成了格式完全正确的JSON。

- 3/5: 工具选择正确，但参数提取有误（如日期错误）或JSON格式不规范。

- 1/5: 无法理解任务，未能选择工具或生成了完全错误的JSON。
"""

def run_test(model_name):
    response_content, _ = run_single_test(PILLAR_NAME, PROMPT, model_name, DEFAULT_OPTIONS_DETERMINISTIC, test_script_name=Path(__file__).name)
    
    # Automated check
    print("\n--- AUTOMATED CHECKS ---")
    try:
        data = json.loads(response_content)
        print("PASS: Output is valid JSON.")
        if "name" in data and data["name"] == "search_flights" and "parameters" in data:
             print("PASS: Tool name is correct.")
             params = data["parameters"]
             if params.get("departure_city") == "北京" and params.get("arrival_city") == "上海" and params.get("date") == "2024-06-17":
                 print("PASS: All parameters are correct.")
             else:
                 print(f"FAIL: Parameters are incorrect. Got: {params}")
        else:
            print("FAIL: Tool call structure is incorrect.")

    except json.JSONDecodeError:
        print("FAIL: Output is not valid JSON.")
    except Exception as e:
        print(f"An error occurred during checks: {e}")
    print("--- END OF CHECKS ---")
    
    print_assessment_criteria(ASSESSMENT_CRITERIA)

if __name__ == '__main__':
    try:
        model_to_use = sys.argv[1]
    except IndexError:
        print("Usage: python test_pillar_06_tool_use.py <model_name>")
        print(f"Using default model from config: {MODEL_TO_TEST}")
        model_to_use = MODEL_TO_TEST
    run_test(model_to_use)
