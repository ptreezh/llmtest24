import argparse
import subprocess
import json
import os
import time

def run_selected_tests(model_name, test_files):
    """
    Runs the selected tests for a given model and collects the results.
    Args:
        model_name (str): The name of the model to test.
        test_files (list): A list of test file paths to execute.
    Returns:
        dict: A dictionary containing the test results summary.
    """
    # Fix: Add project root to python path to solve import errors
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    env = os.environ.copy()
    env['PYTHONPATH'] = project_root + os.pathsep + env.get('PYTHONPATH', '')

    start_time = time.time()
    results_dir = "testout"
    os.makedirs(results_dir, exist_ok=True)

    successful_tests = 0
    total_tests = len(test_files)
    all_test_details = []

    for test_file in test_files:
        test_name = os.path.basename(test_file).replace(".py", "")
        print(f"Running test: {test_name} for model: {model_name}")
        # Fix: Add -u for unbuffered output
        command = [
            "python",
            "-u", 
            "scripts/run_selected_tests.py",
            "--model", model_name,
            "--tests", test_file
        ]
        
        try:
            # Fix: Pass the modified environment to the subprocess
            process = subprocess.run(
                command,
                capture_output=True,
                text=True,
                check=True,
                env=env
            )
            print(f"Test {test_name} output:\n{process.stdout}")
            # Assuming run_selected_tests.py outputs a path to a JSON file or similar
            # For now, we'll just assume success/failure based on return code
            if process.returncode == 0:
                successful_tests += 1
                status = "SUCCESS"
            else:
                status = "FAILURE"
            
            all_test_details.append({
                "test_file": test_file,
                "test_name": test_name,
                "status": status,
                "output": process.stdout,
                "error": process.stderr
            })

        except subprocess.CalledProcessError as e:
            print(f"Test {test_name} failed with error:\n{e.stdout}\n{e.stderr}")
            all_test_details.append({
                "test_file": test_file,
                "test_name": test_name,
                "status": "ERROR",
                "output": e.stdout,
                "error": e.stderr
            })
        except Exception as e:
            print(f"An unexpected error occurred for test {test_name}: {e}")
            all_test_details.append({
                "test_file": test_file,
                "test_name": test_name,
                "status": "ERROR",
                "output": "",
                "error": str(e)
            })

    end_time = time.time()
    duration = end_time - start_time
    success_rate = (successful_tests / total_tests) * 100 if total_tests > 0 else 0

    summary = {
        "model_name": model_name,
        "total_tests": total_tests,
        "successful_tests": successful_tests,
        "success_rate": success_rate,
        "start_time": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(start_time)),
        "end_time": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(end_time)),
        "duration_seconds": duration,
        "test_details": all_test_details
    }

    # Save results to a unique JSON file
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    output_filename = os.path.join(results_dir, f"web_test_results_{timestamp}.json")
    with open(output_filename, 'w', encoding='utf-8') as f:
        json.dump(summary, f, ensure_ascii=False, indent=4)
    
    print(f"Test results saved to {output_filename}")
    return summary

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run selected LLM tests via web interface.")
    parser.add_argument("--model", required=True, help="The LLM model to test (e.g., 'together/mistralai/Mixtral-8x7B-Instruct-v0.1').")
    parser.add_argument("--tests", nargs='+', required=True, help="List of test files to run (e.g., 'tests/test_pillar_01_logic.py').")
    
    args = parser.parse_args()
    
    results = run_selected_tests(args.model, args.tests)
    # The script should print the path to the output file or the JSON directly
    # for the Streamlit app to pick it up.
    print(json.dumps(results))
