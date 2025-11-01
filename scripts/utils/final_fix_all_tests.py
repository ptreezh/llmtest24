import os
import glob
import re

def fix_test_file(filepath):
    """
    Systematically fixes a test pillar script by restructuring its imports
    and model call methods.
    """
    print(f"Processing: {filepath}...")
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Standardize imports
    # 1. Remove old, incorrect sys.path manipulations and ollama imports
    content = re.sub(r"import ollama\n", "", content)
    content = re.sub(r"sys\.path\.append\(os\.path\.abspath\(os\.path\.join\(os\.path\.dirname\(__file__\), '\.\.'\)\)\)\n", "", content)
    content = re.sub(r"from utils import call_qiniu_deepseek, run_single_test", "from utils import run_single_test", content)

    # 2. Define the correct, standardized header
    correct_header = """import sys
import os

# Add project root to Python path to ensure imports work
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

"""
    # 3. Remove any existing header and add the correct one
    # This regex finds the start of the file, optional shebang, optional encoding, and then adds our header.
    content = re.sub(r"(?:^#!\/usr\/bin\/env python3\n)?(?:^# -\*- coding: utf-8 -\*-\n)?", 
                     f"\\g<0>{correct_header}", content, count=1)

    # Standardize the `call_model` method if it exists
    call_model_pattern = re.compile(
        r"(def call_model\(self, prompt, options=None\):\n)"
        r"(\s+return run_single_test\([^)]+\)\[0\])",
        re.MULTILINE
    )
    
    correct_call_model = r"""def call_model(self, prompt, options=None):
        content, _ = run_single_test(
            pillar_name="Pillar XX: Auto-Detected", # Placeholder
            prompt=prompt,
            model=self.model_name,
            options=options or {},
            test_script_name=os.path.basename(__file__)
        )
        return content"""

    # Replace if a simple version exists
    if call_model_pattern.search(content):
        content = call_model_pattern.sub(correct_call_model, content)

    # Remove duplicate imports that might have been added
    lines = content.split('\\n')
    unique_lines = []
    seen_imports = set()
    for line in lines:
        stripped_line = line.strip()
        if stripped_line.startswith("import ") or stripped_line.startswith("from "):
            if stripped_line not in seen_imports:
                unique_lines.append(line)
                seen_imports.add(stripped_line)
        else:
            unique_lines.append(line)
    content = '\\n'.join(unique_lines)


    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"  -> Fixed: {filepath}")

def main():
    """Main function to run the fix on all pillar tests."""
    print("--- Starting Final Batch Fix for All Test Scripts ---")
    test_files = glob.glob("tests/test_pillar_*.py")
    for filepath in test_files:
        try:
            fix_test_file(filepath)
        except Exception as e:
            print(f"  -> FAILED to fix {filepath}: {e}")
    print("--- Batch Fix Complete ---")

if __name__ == "__main__":
    main()
