#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import subprocess
import argparse
import sys
import importlib
from pathlib import Path
import json
import time
import re

from config import MODEL_TO_TEST as CONFIG_MODEL, LOG_DIR, REPORT_DIR, MODELS_LIST_FILE
from utils import run_single_test, print_assessment_criteria, setup_test_environment, cleanup_test_environment, check_ollama_dependency, modify_test_script, save_file, read_file, execute_bash_script, ensure_log_dir, ensure_report_dir

# --- Dynamic Test Discovery ---
def get_all_pillar_tests(tests_dir="tests"):
    """动态发现tests目录下的所有Pillar测试脚本"""
    test_files = sorted(Path(tests_dir).glob("test_pillar_*.py"))
    test_modules = []
    for tf in test_files:
        module_name = f"{tests_dir}.{tf.stem}"
        try:
            module = importlib.import_module(module_name)
            if hasattr(module, 'run_test'): # Check for the expected test function
                test_modules.append({
                    'name': tf.stem,
                    'module': module,
                    'path': tf,
                    'description': getattr(module, 'PILLAR_DESCRIPTION', 'No description available')
                })
            else:
                print(f"[WARN] Module {module_name} does not have a 'run_test' function. Skipping.")
        except ImportError as e:
            print(f"[ERROR] Failed to import module {module_name}: {e}")
        except Exception as e:
            print(f"[ERROR] An unexpected error occurred while processing {tf.name}: {e}")
    return test_modules

# --- Test Execution Logic ---
def run_single_pillar_test(test_info, model_name):
    """
    为单个Pillar测试准备环境并执行。
    重构：原始的test_pillar_X.py需要被调整，使其包含一个run_test(model_name)函数，
    该函数调用run_single_test来执行具体的测试逻辑。
    """
    script_name = test_info['path'].name
    print(f"\n--- Preparing to run: {script_name} ---")

    try:
        # 直接调用模块的run_test函数
        test_info['module'].run_test(model_name)
        return True
    except Exception as e:
        print(f"[ERROR] Error executing {script_name}: {e}")
        return False

def run_all_basic_tests(model_name: str, tests_to_run=None):
    """
    运行所有基础Pillar测试。
    Args:
        model_name: 要测试的模型名称。
        tests_to_run: 可选列表，指定要运行的测试脚本文件名（例如['test_pillar_01_logic.py']）。
    """
    print(f"\n{'='*30} STARTING BASIC PILLAR TESTS FOR MODEL: {model_name} {'='*30}")
    check_ollama_dependency() # Ensure ollama is installed and reachable
    
    all_tests = get_all_pillar_tests()
    
    if tests_to_run:
        print(f"[INFO] Filtering tests to run: {tests_to_run}")
        tests_to_run_set = {t.split('/')[-1] for t in tests_to_run} # Normalize to just filename
        tests_to_execute = [t for t in all_tests if t['path'].name in tests_to_run_set]
    else:
        tests_to_execute = all_tests
    
    results = {}
    
    for test_info in tests_to_execute:
        script_name = test_info['path'].name
        
        # Save test output to a log file
        ensure_log_dir()
        log_file_path = os.path.join(LOG_DIR, f"{script_name.replace('.py', '')}_{model_name.replace(':', '_').replace('/', '_')}.log")
        
        # Redirect stdout and stderr for the subprocess
        with open(log_file_path, 'w', encoding='utf-8') as log_file:
            original_stdout = sys.stdout
            original_stderr = sys.stderr
            try:
                sys.stdout = log_file
                sys.stderr = log_file # Also redirect stderr to the log file

                success = run_single_pillar_test(test_info, model_name)
                results[script_name] = {'success': success, 'log': log_file_path}
            except Exception as e:
                print(f"[CRITICAL ERROR] Unhandled exception during test execution for {script_name}: {e}", file=sys.stderr)
                results[script_name] = {'success': False, 'log': log_file_path, 'error': str(e)}
            finally:
                sys.stdout = original_stdout # Restore stdout
                sys.stderr = original_stderr # Restore stderr

        # 检查日志内容是否为所有云API均失败
        with open(log_file_path, 'r', encoding='utf-8') as f:
            log_content = f.read()
        if re.search(r'所有云API均失败', log_content) or '[API Error: All cloud APIs failed]' in log_content:
            fail_log_name = f"{model_name.replace(':', '_').replace('/', '_')}_Allfail.log"
            fail_log_path = os.path.join(LOG_DIR, fail_log_name)
            os.replace(log_file_path, fail_log_path)
            print(f"[LOG] All cloud APIs failed for {model_name}, log saved to {fail_log_path}")
        else:
            print(f"[LOG] Test results for {script_name} saved to {log_file_path}")

    print(f"\n{'='*30} BASIC PILLAR TESTS COMPLETED FOR MODEL: {model_name} {'='*30}")

    return results

# --- Workflow Orchestration (Placeholder) ---
def run_workflow_test(workflow_name: str, model_name: str, workflow_params: dict):
    """
    Placeholder for running complex, multi-Pillar workflow tests.
    This function would dynamically import and orchestrate tests from different pillars
    based on the workflow definition.
    """
    print(f"\n{'='*30} STARTING WORKFLOW TEST: {workflow_name} FOR MODEL: {model_name} {'='*30}")
    workspace = None
    try:
        # Example: Initialize a workspace for the workflow
        workspace = setup_test_environment(workflow_name)

        # --- Example Workflow: Wiki Collaboration ---
        if workflow_name == "wiki_collaboration":
            print("\n[Workflow] Starting Wiki Collaboration Simulation...")

            # 1. Task Decomposition & Planning (Pillar 7)
            print("\n[Step 1/4] Task Decomposition for Wiki Entry...")
            wiki_task_prompt = "Create a WBS for editing a Wikipedia page about 'Large Language Models'. Decompose into sections like 'Introduction', 'Architecture', 'Training', 'Applications', 'Limitations', 'Future'."

            # Simulate task decomposition
            from config import DEFAULT_OPTIONS_DETERMINISTIC
            task_decomposition_results, _ = run_single_test("Pillar 7: Task Decomposition", wiki_task_prompt, model_name, DEFAULT_OPTIONS_DETERMINISTIC, test_script_name="workflow_wiki_collaboration")

            if task_decomposition_results and "ERROR" not in task_decomposition_results:
                # Simulate saving the WBS to a file
                wbs_file = os.path.join(workspace, "wiki_wbs.md")
                save_file(wbs_file, task_decomposition_results)
                print(f"[Workflow] WBS generated and saved to {wbs_file}")

                # 2. Role Assignment & Project Initialization (Pillars 13, 14, 2)
                print("\n[Step 2/4] Initializing Project Environment & Roles...")
                # Simulate creating roles.json based on Pillar 13's structure and assigning roles for Wiki editing
                roles_data = {
                    "researcher": "Finds factual information and citations for Wiki entries.",
                    "writer": "Writes and formats Wiki content following style guides.",
                    "editor": "Reviews content for accuracy, style, and consistency, proposes edits."
                }
                roles_file_path = os.path.join(workspace, "config", "roles.json")
                save_file(roles_file_path, json.dumps(roles_data, indent=2))
                print(f"[Workflow] Roles defined in {roles_file_path}")

                # 3. Multi-turn Collaboration & Consensus (Pillars 12, 15)
                print("\n[Step 3/4] Simulating multi-turn editing and review...")
                # Simulate a review and revision cycle
                editor_review_prompt = "Review the following Wiki entry section on 'Limitations' and provide suggestions for improvement to ensure clarity and neutrality."
                editor_feedback = "The current text mentions 'hallucinations', but 'confabulation' might be a more precise term. Also, ensure the tone remains objective."
                print(f"[Workflow] Editor feedback received: {editor_feedback}")

                # 4. State Update & Finalization (Pillar 15 - Consensus)
                print("\n[Step 4/4] Finalizing task and updating status...")
                consensus_reached = True # Simplified
                if consensus_reached:
                    print("[Workflow] Consensus reached on 'Limitations' section. Task complete.")
                    task_status_update = f"- Task 'Limitations Section' for Wiki: Completed. Model: {model_name}. Status: Consensus Reached."
                    print(f"[Workflow] Updating task board with: {task_status_update}")
            else:
                print("[Workflow] Failed to perform task decomposition. Aborting Wiki collaboration simulation.")

        # --- Example Workflow: Project Management Simulation ---
        elif workflow_name == "project_management":
            print("\n[Workflow] Starting Project Management Simulation...")

            # Import and run composite scenario tests
            try:
                from tests.composite_scenarios.test_workflow_simulation import run_test as run_workflow_sim
                run_workflow_sim(model_name)
            except ImportError as e:
                print(f"[ERROR] Could not import workflow simulation: {e}")

        # --- Example Workflow: Cross-Capability Integration ---
        elif workflow_name == "capability_integration":
            print("\n[Workflow] Starting Cross-Capability Integration Test...")

            try:
                from tests.composite_scenarios.test_cross_capability_integration import run_test as run_capability_test
                run_capability_test(model_name)
            except ImportError as e:
                print(f"[ERROR] Could not import capability integration test: {e}")

        # --- Example Workflow: Multi-Turn Dialogue ---
        elif workflow_name == "multi_turn_dialogue":
            print("\n[Workflow] Starting Multi-Turn Dialogue Test...")

            try:
                from tests.composite_scenarios.test_multi_turn_dialogue import run_test as run_dialogue_test
                run_dialogue_test(model_name)
            except ImportError as e:
                print(f"[ERROR] Could not import multi-turn dialogue test: {e}")

        # Add other workflow simulations here...
        else:
            print(f"[INFO] No specific workflow logic defined for '{workflow_name}'. Running basic tests as fallback.")
            run_all_basic_tests(model_name)

    finally:
        if workspace:
            cleanup_test_environment(workspace)
    print(f"\n{'='*30} WORKFLOW TEST '{workflow_name}' COMPLETED {'='*30}")

# --- Main Orchestration Function ---
def run_tests(model_name: str, tests_to_run: list = None, workflow: str = None, workflow_params: dict = None):
    """
    主入口函数，根据参数决定是运行基础测试还是工作流测试。
    Args:
        model_name: 要测试的模型名称。
        tests_to_run: 可选列表，指定要运行的基础测试脚本 (e.g., ['test_pillar_01_logic.py'])。
        workflow: 指定要运行的工作流名称 (e.g., 'wiki_collaboration').
        workflow_params: 传递给工作流的参数。
    """
    print(f"[INFO] Starting Test Suite Orchestration...")
    print(f"[INFO] Target Model: {model_name}")

    # Ensure necessary directories exist
    ensure_log_dir()
    ensure_report_dir()

    if workflow:
        run_workflow_test(workflow, model_name, workflow_params or {})
    elif tests_to_run:
        run_all_basic_tests(model_name, tests_to_run)
    else:
        print("\n[INFO] No specific tests or workflow selected. Running all basic pillar tests.")
        run_all_basic_tests(model_name)

    print(f"\n{'='*30} TEST SUITE EXECUTION FINISHED {'='*30}")

# --- Argument Parsing and Main Execution ---
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="SLM/LLM Advanced Capability Test Suite Orchestrator.")
    parser.add_argument("--model", type=str, default=CONFIG_MODEL, help="The Ollama model name to test (e.g., 'llama3:8b'). Overrides config.py.")
    parser.add_argument("--test", type=str, nargs='+', help="Specific Pillar test scripts to run (e.g., --test test_pillar_01_logic.py test_pillar_02_instruction.py).")
    parser.add_argument("--workflow", type=str, help="Name of a complex workflow to run (e.g., 'wiki_collaboration').")
    # Add arguments for workflow parameters if needed
    # parser.add_argument("--workflow-param-key", type=str, help="Parameter for the specified workflow.")

    args = parser.parse_args()

    # Prepare workflow parameters if workflow is specified (placeholder)
    workflow_params = {}
    # if args.workflow and args.workflow_param_key:
    #     workflow_params['key'] = args.workflow_param_key

    run_tests(
        model_name=args.model,
        tests_to_run=args.test,
        workflow=args.workflow,
        workflow_params=workflow_params
    )
