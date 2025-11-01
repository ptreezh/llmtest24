import sys
import os
from pathlib import Path

# Add project root to Python path to ensure imports work
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils import run_single_test, print_assessment_criteria
from config import MODEL_TO_TEST, DEFAULT_OPTIONS_DETERMINISTIC

PILLAR_NAME = "Pillar 18: Refactored Test"
PILLAR_DESCRIPTION = "This test was automatically refactored to use the standard test framework."

PROMPT = """
你是一个AI项目指挥官。在一个复杂的项目中，你收到了一条紧急状态更新：
"关键任务'后端API开发'因技术难题意外受阻，预计延期10天。"

以下是当前的项目任务依赖图（简化版）：
- UI设计 -> 客户端开发
- 后端API开发 -> 客户端开发
- 客户端开发 -> App测试
- App测试 -> 上架应用商店

请你立即做出反应：
1.  **影响分析**: 明确指出哪些下游任务会直接或间接受到影响。
2.  **应对计划**: 提出一个清晰、可操作的应对计划，至少包含3个步骤（例如，暂停哪些任务，启动哪些新任务，如何沟通等）。
3.  **状态通报**: 草拟一份简洁的内部项目状态通报，向所有团队成员说明当前情况、影响和应对措施。
"""

ASSESSMENT_CRITERIA = """
- 5/5: Correctly and fully answers the prompt.
- 3/5: Partially answers the prompt or contains minor errors.
- 1/5: Fails to understand the prompt or gives a completely incorrect answer.
"""

def run_test(model_name):
    """Runs the test for a given model."""
    run_single_test(
        pillar_name=PILLAR_NAME,
        prompt=PROMPT,
        model=model_name,
        options=DEFAULT_OPTIONS_DETERMINISTIC,
        test_script_name=Path(__file__).name
    )
    print_assessment_criteria(ASSESSMENT_CRITERIA)

if __name__ == '__main__':
    try:
        model_to_use = sys.argv[1]
    except IndexError:
        print(f"Usage: python {os.path.basename(__file__)} <model_name>")
        print(f"Using default model from config: {MODEL_TO_TEST}")
        model_to_use = MODEL_TO_TEST
    run_test(model_to_use)
