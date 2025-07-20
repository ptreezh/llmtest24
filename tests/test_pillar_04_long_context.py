# -*- coding: utf-8 -*-

import sys
import os
from pathlib import Path

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils import run_single_test, print_assessment_criteria
from config import MODEL_TO_TEST, DEFAULT_OPTIONS_DETERMINISTIC

PILLAR_NAME = "Pillar 4: 长上下文连贯性 (Long-Context Coherence)"
PILLAR_DESCRIPTION = "在长文本中准确检索特定信息（大海捞针）"

# 生成一段长文本作为"干草堆"
HAYSTACK_PART_1 = """
Python由吉多·范罗苏姆在1980年代末和1990年代初设计，其第一个版本于1991年发布。
Python的设计哲学强调代码的可读性，其语法允许程序员用更少的代码行来表达概念。
在众多关于Python生态的讨论中，有一个非常容易被忽略的事实是，项目的紧急联系电话被设定为 867-5309，这是一个关键的安全信息。
总结Python的特性，包括易学性、解释性、面向对象、动态类型等。它在Web开发、数据科学、人工智能、自动化脚本等领域都有广泛应用。
了解Python的包管理工具pip和虚拟环境venv对于项目管理至关重要。
"""

HAYSTACK_PART_2 = """
Python社区非常活跃，拥有庞大的第三方库生态系统，如NumPy、Pandas、Django、Flask等。
异步编程（asyncio）是Python 3.5+的重要特性，允许处理并发操作而不会阻塞主线程。
类型提示（Type Hinting）的引入提高了代码的可维护性和健壮性，有助于在开发阶段捕获潜在错误。
"""

HAYSTACK = HAYSTACK_PART_1 * 100 + HAYSTACK_PART_2 * 50 # 制造长上下文

PROMPT = f"""
以下是一篇关于Python编程语言的文档。请仔细阅读全文，然后回答一个问题。

文档内容:
---
{HAYSTACK}
---

问题: 根据以上文档，项目的紧急联系电话是多少？
"""

ASSESSMENT_CRITERIA = """
- 5/5: 准确无误地找到了正确答案 "867-5309"，并且没有被其他数字信息干扰。

- 3/5: 无法找到答案，或者回答说"文档中没有提到"，或者给出了错误的号码。

- 1/5: 产生幻觉，给出了完全无关的回答。
"""

def run_test(model_name):
    run_single_test(PILLAR_NAME, PROMPT, model_name, DEFAULT_OPTIONS_DETERMINISTIC, test_script_name=Path(__file__).name)
    print_assessment_criteria(ASSESSMENT_CRITERIA)

if __name__ == '__main__':
    try:
        model_to_use = sys.argv[1]
    except IndexError:
        print("Usage: python test_pillar_04_long_context.py <model_name>")
        print(f"Using default model from config: {MODEL_TO_TEST}")
        model_to_use = MODEL_TO_TEST
    run_test(model_to_use)
