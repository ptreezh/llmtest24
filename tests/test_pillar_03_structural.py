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

PILLAR_NAME = "Pillar 3: 结构化与抽象操作 (Structural & Abstract Manipulation)"
PILLAR_DESCRIPTION = "将非结构化文本映射到预定义的抽象模式（如JSON）"

PROMPT = """
请从以下非结构化文本中提取信息，并严格按照指定的JSON Schema格式输出。

源文本:
"张三，手机号13812345678，订购了我们的'高级会员'套餐，订单号是 ORD-2024-001。他有两个收货地址，首选地址是北京市海淀区中关村大街1号，备用地址是上海市浦东新区世纪大道100号。他希望我们周一到周五的上午9点到下午5点之间配送。"

目标JSON Schema:
{
  "type": "object",
  "properties": {
    "customerName": { "type": "string" },
    "contact": {
      "type": "object",
      "properties": {
        "phone": { "type": "string" }
      },
      "required": ["phone"]
    },
    "order": {
      "type": "object",
      "properties": {
        "orderId": { "type": "string" },
        "plan": { "type": "string" }
      },
      "required": ["orderId", "plan"]
    },
    "shippingInfo": {
      "type": "object",
      "properties": {
        "addresses": {
          "type": "array",
          "items": {
            "type": "object",
            "properties": {
              "type": { "type": "string", "enum": ["primary", "secondary"] },
              "address": { "type": "string" }
            },
            "required": ["type", "address"]
          }
        },
        "deliveryWindow": { "type": "string" }
      },
      "required": ["addresses"]
    }
  },
  "required": ["customerName", "contact", "order", "shippingInfo"]
}

请只输出符合该Schema的JSON对象，不要有任何其他文字。
"""

ASSESSMENT_CRITERIA = """
- 5/5: 成功生成了完全符合Schema的、格式正确的JSON。所有信息都被准确无误地提取和映射到了正确的字段中，包括嵌套结构和数组。

- 3/5: 生成了JSON，但存在一些问题，如：部分字段缺失、信息提取错误、数据类型不匹配，或JSON结构与Schema不完全一致。

- 1/5: 无法生成有效的JSON，或者提取的信息完全错误，或者输出与要求无关。
"""

def run_test(model_name):
    response_content, _ = run_single_test(PILLAR_NAME, PROMPT, model_name, DEFAULT_OPTIONS_DETERMINISTIC, test_script_name=Path(__file__).name)
    
    # Automated check
    print("\n--- AUTOMATED CHECKS ---")
    try:
        data = json.loads(response_content)
        print("PASS: Output is valid JSON.")
        if "shippingInfo" in data and "addresses" in data["shippingInfo"] and len(data["shippingInfo"]["addresses"]) == 2:
            print("PASS: Shipping addresses array seems correctly populated.")
        else:
            print("FAIL: Shipping addresses structure appears incorrect.")
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
        print("Usage: python test_pillar_03_structural.py <model_name>")
        print(f"Using default model from config: {MODEL_TO_TEST}")
        model_to_use = MODEL_TO_TEST
    run_test(model_to_use)
