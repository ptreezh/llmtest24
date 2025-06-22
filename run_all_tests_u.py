#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import subprocess
import argparse
import sys
import re

# List of test scripts to be executed
TEST_SCRIPTS = [
    "test_pillar_1_logic.py",
    "test_pillar_2_fidelity.py",
    "test_pillar_3_structure.py",
    "test_pillar_4_context.py",
    "test_pillar_5_knowledge.py",
    "test_pillar_6_tool_use.py",
    "test_pillar_7_planning.py",
    "test_pillar_8_metacognition.py",
]

def check_dependencies():
    """Check if the 'ollama' python package is installed."""
    try:
        __import__('ollama')
    except ImportError:
        print("[SETUP] 'ollama' python package not found. Installing...")
        try:
            # Using sys.executable ensures we use the pip of the correct python version (python3)
            subprocess.check_call([sys.executable, "-m", "pip", "install", "ollama"])
            print("[SETUP] 'ollama' installed successfully.")
        except subprocess.CalledProcessError:
            print("[ERROR] Failed to install 'ollama'. Please install it manually.")
            print("[INFO] On Ubuntu/Debian, you may need to install pip first: 'sudo apt install python3-pip'")
            sys.exit(1)

def run_test(script_name, model_name):
    """Dynamically sets the model in a test script and runs it. Returns stdout for parsing."""
    print(f"\n{'-'*20} Running: {script_name} on model: {model_name} {'-'*20}")

    if not os.path.exists(script_name):
        print(f"[ERROR] Script not found: {script_name}. Make sure all scripts are in the same directory.")
        return ""

    # Read the original script content
    with open(script_name, 'r', encoding='utf-8') as f:
        original_content = f.read()

    # Replace the placeholder model name
    modified_content = []
    for line in original_content.splitlines():
        if line.strip().startswith('MODEL_TO_TEST'):
            modified_content.append(f"MODEL_TO_TEST = '{model_name}'")
        else:
            modified_content.append(line)
    modified_content = "\n".join(modified_content)

    # We use a temporary file to avoid complex command-line argument passing to each subprocess.
    temp_script_name = "_temp_test_runner.py"
    with open(temp_script_name, 'w', encoding='utf-8') as f:
        f.write(modified_content)

    try:
        result = subprocess.run(
            [sys.executable, temp_script_name],
            capture_output=True,
            text=True,
            check=True,
            encoding='utf-8',
            errors='replace'
        )
        if result.stdout:
            print(result.stdout)
        if result.stderr:
            print(f"[STDERR]:\n{result.stderr}")
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] An error occurred while running {script_name}:")
        print(e.stdout)
        print(e.stderr)
        return e.stdout + "\n" + e.stderr
    finally:
        # Clean up the temporary file
        if os.path.exists(temp_script_name):
            os.remove(temp_script_name)

def parse_test_output(output):
    score_match = re.search(r'\[SCORE\]\s*(\d+/10)', output)
    analysis_match = re.search(r'\[ANALYSIS\](.*?)(?=\n\[|\n$)', output, re.DOTALL)
    score = score_match.group(1) if score_match else "N/A"
    analysis = analysis_match.group(1).strip().replace('\n', ' ') if analysis_match else "No analysis found."
    return score, analysis

def main():
    parser = argparse.ArgumentParser(description="Run the SLM Foundational Capability Test Suite.")
    parser.add_argument("--model", required=True, help="The name of the ollama model to test (e.g., 'mistral', 'yi:6b').")
    args = parser.parse_args()

    print("[INFO] Starting SLM Foundational Capability Test Suite...")
    print(f"[INFO] Target Model: {args.model}")
    print("[INFO] Make sure the Ollama service is running.")

    check_dependencies()

    pillar_results = []
    for idx, script in enumerate(TEST_SCRIPTS, 1):
        output = run_test(script, args.model)
        score, analysis = parse_test_output(output)
        pillar_results.append((idx, script, score, analysis))

    # 计算总分
    total_score = 0
    valid_scores = 0
    for _, _, score, _ in pillar_results:
        try:
            s = int(score.split('/')[0])
            total_score += s
            valid_scores += 1
        except:
            pass
    overall_score = round(total_score / valid_scores, 1) if valid_scores else 0

    # 写报告 TXT
    report_filename = f"report_{args.model.replace(':','-')}.txt"
    with open(report_filename, "w", encoding="utf-8") as f:
        f.write("Test Suite Evaluation Summary\n")
        f.write("Pillar\tTest Name\tScore\tAnalysis\n")
        for idx, script, score, analysis in pillar_results:
            test_name = script.replace('test_pillar_','').replace('.py','').replace('_',' ').title()
            f.write(f"{idx}\t{test_name}\t{score}\t{analysis}\n")
        f.write("Final Score & Conclusion\n")
        f.write(f"Overall Score: {overall_score}/10\n")
        f.write(f"The {args.model} model demonstrates highly polarized capabilities. Please review individual pillar analyses for details.\n")
    print(f"\n[INFO] Test report written to {report_filename}\n")

    # 写报告 HTML
    html_filename = f"report_{args.model.replace(':','-')}.html"
    with open(html_filename, "w", encoding="utf-8") as f:
        f.write("""
<!DOCTYPE html>
<html lang='en'>
<head>
<meta charset='UTF-8'>
<title>Test Suite Evaluation Summary</title>
<style>
body { font-family: Arial, sans-serif; margin: 2em; background: #f9f9f9; }
h1 { text-align: center; }
table { border-collapse: collapse; width: 100%; background: #fff; box-shadow: 0 2px 8px #eee; }
th, td { border: 1px solid #ccc; padding: 10px; text-align: center; }
th { background: #f2f2f2; font-weight: bold; }
tr:nth-child(even) { background: #f9f9f9; }
tr:hover { background: #e6f7ff; }
tfoot td { font-weight: bold; background: #f2f2f2; }
.summary { margin-top: 2em; font-size: 1.1em; }
</style>
</head>
<body>
<h1>Test Suite Evaluation Summary</h1>
<table>
<thead>
<tr><th>Pillar</th><th>Test Name</th><th>Score</th><th>Analysis</th></tr>
</thead>
<tbody>
""")
        for idx, script, score, analysis in pillar_results:
            test_name = script.replace('test_pillar_','').replace('.py','').replace('_',' ').title()
            f.write(f"<tr><td>{idx}</td><td>{test_name}</td><td><b>{score}</b></td><td style='text-align:left'>{analysis}</td></tr>\n")
        f.write("""
</tbody>
<tfoot>
<tr><td colspan='2'>Overall Score</td><td colspan='2'><b>{overall_score}/10</b></td></tr>
</tfoot>
</table>
<div class='summary'>
<h2>Final Score & Conclusion</h2>
<p>The <b>{model}</b> model demonstrates highly polarized capabilities. Please review individual pillar analyses for details.</p>
</div>
</body>
</html>
""".replace('{model}', args.model))
    print(f"[INFO] HTML test report written to {html_filename}\n")

if __name__ == "__main__":
    main()
