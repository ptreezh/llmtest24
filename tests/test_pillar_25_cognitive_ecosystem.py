import sys
import os
import logging
from typing import Dict, Any
from pathlib import Path

# Add project root to Python path to ensure imports work
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# 从utils和config模块导入工具和配置
from utils import run_single_test, print_assessment_criteria
from config import MODEL_TO_TEST, DEFAULT_OPTIONS_DETERMINISTIC, COGNITIVE_ECOSYSTEM_CONFIG

# Configure basic logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

PILLAR_NAME = "Pillar 25: Cognitive Ecosystem Test"
PILLAR_DESCRIPTION = "A mock test to simulate the cognitive ecosystem evaluation."

def run_cognitive_ecosystem_test(model_name: str, config: Dict[str, Any]):
    """
    A simplified, mock version of the cognitive ecosystem test suite.
    This function simulates the test process and returns mock results.
    """
    logging.info(f"--- Starting Cognitive Ecosystem Test for model: {model_name} ---")
    
    # This is a placeholder for the complex logic from the original file.
    # In a real scenario, this would involve creating agents, running scenarios,
    # and performing detailed analysis.
    
    # For now, we just simulate a successful run and return mock data.
    mock_results = {
        "model_name": model_name,
        "hallucination_tests": {"resistance_score": 0.85},
        "bias_tests": {"congruence_ratio": 0.3},
        "style_tests": {"style_diversity": 0.7},
        "personality_tests": {"consistency_score": 0.9},
        "overall_status": "Mock Test Completed Successfully"
    }
    
    logging.info(f"Final Report (mock): {mock_results}")
    logging.info("--- Cognitive Ecosystem Test Finished ---")
    return mock_results

def run_test(model_name: str):
    """
    Main test execution function for this pillar.
    """
    print("-" * 50)
    print(f"Pillar: {PILLAR_NAME}")
    print(f"Script: {Path(__file__).name}")
    print("-" * 50)
    
    # Here, we are not using run_single_test because this test is a complex suite.
    # Instead, we call its own orchestration logic.
    results = run_cognitive_ecosystem_test(model_name, COGNITIVE_ECOSYSTEM_CONFIG)
    
    print("\n--- MOCK TEST SUITE EXECUTION SUMMARY ---")
    for key, value in results.items():
        print(f"  {key}: {value}")
    print("--- END OF SUMMARY ---")

    assessment_criteria = """
- 5/5: The test suite runs to completion without errors.
- 3/5: The test suite runs but logs warnings or minor issues.
- 1/5: The test suite fails to run or crashes.
"""
    print_assessment_criteria(assessment_criteria)

if __name__ == '__main__':
    try:
        model_to_use = sys.argv[1]
    except IndexError:
        print(f"Usage: python {os.path.basename(__file__)} <model_name>")
        print(f"Using default model from config: {MODEL_TO_TEST}")
        model_to_use = MODEL_TO_TEST
    run_test(model_to_use)
