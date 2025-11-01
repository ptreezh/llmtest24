import sys
import os
from pathlib import Path

# Add project root to Python path to ensure imports work
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import sys
import os
# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import unittest
import os
import json
from unittest.mock import MagicMock, patch

from cognitive_ecosystem.detectors.hallucination_detector import CollusiveHallucinationDetector
from cognitive_ecosystem.core.ecosystem_engine import CognitiveEcosystemEngine

def run_test(model_name=None):
    """
    Wrapper function to run unittest suite, compatible with main_orchestrator.py.
    Accepts model_name for compatibility, though unittest.main() handles execution.
    """
    print(f"--- Running unittest for {Path(__file__).name} ---")
    if model_name:
        print(f"--- Model specified: {model_name} ---")
    
    # unittest.main() discovers and runs tests in this file.
    # It might be necessary to configure the environment or mocks
    # if tests rely on specific model interactions that are not mocked.
    
    # Run tests programmatically instead of using unittest.main()
    # to avoid command-line argument conflicts
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(TestCollusiveHallucinationDetector)
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Convert unittest result to our expected format
    return {
        "success": result.wasSuccessful(),
        "tests_run": result.testsRun,
        "errors": len(result.errors),
        "failures": len(result.failures),
        "time": getattr(result, 'time', 'unknown')
    }

class TestCollusiveHallucinationDetector(unittest.TestCase):
    """
    Test suite for the Collusive Hallucination Detector.
    """

    def setUp(self):
        """
        Set up the test environment before each test.
        """
        self.detector = CollusiveHallucinationDetector()
        self.mock_engine = MagicMock(spec=CognitiveEcosystemEngine)

    def test_initialization(self):
        """
        Test if the detector initializes correctly.
        """
        self.assertIsNotNone(self.detector)
        self.assertTrue(len(self.detector.injection_strategies) > 0)
        # This assumes you have a data file for known hallucinations
        self.assertIsNotNone(self.detector.known_hallucinations)

    def test_select_and_inject_hallucination(self):
        """
        Test the selection and injection of a hallucination.
        """
        strategy = "fake_theory_injection"
        injection_scenario = self.detector.select_and_inject_hallucination(strategy)
        self.assertIsNotNone(injection_scenario)
        self.assertIn("prompt", injection_scenario)
        self.assertIn("Maslow's Feed-Forward Motivation Theory", injection_scenario["prompt"])

    def test_analyze_collective_response(self):
        """
        Test the analysis of collective responses for collusion patterns.
        """
        agent_responses = [
            {"agent_id": "agent1", "text": "I agree with the theory of pre-attentive motivation."},
            {"agent_id": "agent2", "text": "Yes, Dr. Vasquez's work on pre-attentive motivation is groundbreaking."}
        ]
        analysis_result = self.detector.analyze_collective_response(agent_responses)
        self.assertGreater(analysis_result["agreement_count"], 0)

    def test_calculate_resistance_score(self):
        """
        Test the calculation of the hallucination resistance score.
        """
        analysis_results = {
            "reality_check_count": 1,
            "disagreement_count": 1,
            "agreement_count": 2
        }
        total_agents = 4
        score = self.detector.calculate_resistance_score(analysis_results, total_agents)
        self.assertGreater(score, 0.3)


if __name__ == '__main__':
    unittest.main()
