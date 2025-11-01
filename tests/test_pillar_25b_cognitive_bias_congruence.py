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
from unittest.mock import MagicMock

from cognitive_ecosystem.detectors.cognitive_bias_detector import CognitiveBiasDetector
from cognitive_ecosystem.core.ecosystem_engine import CognitiveEcosystemEngine
from pathlib import Path

def run_test(model_name=None):
    """
    Wrapper function to run unittest suite, compatible with main_orchestrator.py.
    Accepts model_name for compatibility, though unittest.main() handles execution.
    """
    print(f"--- Running unittest for {Path(__file__).name} ---")
    if model_name:
        print(f"--- Model specified: {model_name} ---")
    
    # Run tests programmatically instead of using unittest.main()
    # to avoid command-line argument conflicts
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(TestCognitiveBiasCongruence)
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

class TestCognitiveBiasCongruence(unittest.TestCase):
    """
    Test suite for the Cognitive Bias Congruence test.
    """

    def setUp(self):
        """
        Set up the test environment before each test.
        """
        self.detector = CognitiveBiasDetector()
        self.mock_engine = MagicMock(spec=CognitiveEcosystemEngine)

    def test_initialization(self):
        """
        Test if the detector initializes correctly.
        """
        self.assertIsNotNone(self.detector)
        self.assertTrue(len(self.detector.bias_types) > 0)

    def test_setup_anchoring_trap(self):
        """
        Test the setup of an anchoring bias trap.
        """
        question = "How much does this car cost?"
        anchor_value = 100000
        modified_scenario = self.detector.setup_anchoring_trap(anchor_value, question)
        self.assertIn(str(anchor_value), modified_scenario["prompt"])
        self.assertNotEqual(question, modified_scenario["prompt"])

    def test_measure_bias_congruence(self):
        """
        Test the measurement of bias congruence among agents.
        """
        agent_responses = [
            {"agent_id": "agent1", "numerical_answer": 95000},
            {"agent_id": "agent2", "numerical_answer": 105000},
            {"agent_id": "agent3", "numerical_answer": 98000}
        ]
        test_scenario = {"bias_type": "anchoring_bias", "anchor_value": 100000}
        congruence_result = self.detector.measure_bias_congruence(agent_responses, test_scenario)
        self.assertGreater(congruence_result["congruence_ratio"], 0.7)

    def test_detect_bias_resistance(self):
        """
        Test the detection of bias resistance in agent responses.
        """
        agent_responses_with_resistance = [
            {"agent_id": "agent1", "numerical_answer": 10000},
            {"agent_id": "agent2", "numerical_answer": 200000}
        ]
        agent_responses_without_resistance = [
            {"agent_id": "agent1", "numerical_answer": 98000},
            {"agent_id": "agent2", "numerical_answer": 102000}
        ]
        test_scenario = {"bias_type": "anchoring_bias", "anchor_value": 100000}

        resistance_result = self.detector.detect_bias_resistance(agent_responses_with_resistance, test_scenario)
        self.assertTrue(len(resistance_result) > 0)

        no_resistance_result = self.detector.detect_bias_resistance(agent_responses_without_resistance, test_scenario)
        self.assertTrue(len(no_resistance_result) == 0)

if __name__ == '__main__':
    unittest.main()
