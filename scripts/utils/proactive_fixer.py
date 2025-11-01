import os
import glob
import re

def needs_fixing(content):
    """Check if the file uses the problematic direct ollama call."""
    return "ollama.chat" in content

def get_prompt_from_content(content):
    """Extracts the main prompt string from the script content."""
    match = re.search(r'prompt = """(.*?)"""', content, re.DOTALL)
    if match:
        return match.group(1).strip()
    return "# PROMPT NOT FOUND"

def create_fixed_content(original_content, pillar_name, pillar_description, prompt):
    """Creates the full content for a standardized test script."""
    
    # Basic template for a standard test script
    template = f"""import sys
import os
from pathlib import Path

# Add project root to Python path to ensure imports work
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils import run_single_test, print_assessment_criteria
from config import MODEL_TO_TEST, DEFAULT_OPTIONS_DETERMINISTIC

PILLAR_NAME = "{pillar_name}"
PILLAR_DESCRIPTION = "{pillar_description}"

PROMPT = \"\"\"
{prompt}
\"\"\"

ASSESSMENT_CRITERIA = \"\"\"
- 5/5: Correctly and fully answers the prompt.
- 3/5: Partially answers the prompt or contains minor errors.
- 1/5: Fails to understand the prompt or gives a completely incorrect answer.
\"\"\"

def run_test(model_name):
    \"\"\"Runs the test for a given model.\"\"\"
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
        print(f"Usage: python {{os.path.basename(__file__)}} <model_name>")
        print(f"Using default model from config: {{MODEL_TO_TEST}}")
        model_to_use = MODEL_TO_TEST
    run_test(model_to_use)
"""
    return template

def main():
    """Finds and fixes all non-compliant test scripts."""
    print("--- Starting Proactive and Comprehensive Test Script Fixer ---")
    test_files = glob.glob("tests/test_pillar_*.py")
    
    for filepath in test_files:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            
        if needs_fixing(content):
            print(f"  -> Fixing required for: {filepath}")
            
            # Extract basic info to preserve it
            filename = os.path.basename(filepath)
            pillar_num = filename.split('_')[2]
            pillar_name = f"Pillar {pillar_num}: Refactored Test"
            pillar_desc = "This test was automatically refactored to use the standard test framework."
            prompt = get_prompt_from_content(content)
            
            # Re-write the entire file with the standard template
            fixed_content = create_fixed_content(content, pillar_name, pillar_desc, prompt)
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(fixed_content)
            print(f"     ... Fixed!")
        else:
            print(f"  -> OK: {filepath}")
            
    print("--- Proactive Fixer Complete ---")

if __name__ == "__main__":
    main()
