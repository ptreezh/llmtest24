import sys
import os
from pathlib import Path

# Add project root to Python path to ensure imports work
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils import run_single_test, print_assessment_criteria
from config import MODEL_TO_TEST, DEFAULT_OPTIONS_DETERMINISTIC

PILLAR_NAME = "Pillar 14: Refactored Test"
PILLAR_DESCRIPTION = "This test was automatically refactored to use the standard test framework."

PROMPT = """
# PROMPT NOT FOUND
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
