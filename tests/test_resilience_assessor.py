import unittest
import os
import sys

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from cognitive_ecosystem.analyzers.resilience_assessor import SystemResilienceAssessor
from cognitive_ecosystem.core.ecosystem_engine import CognitiveEcosystemEngine

class TestSystemResilienceAssessor(unittest.TestCase):
    """
    Unit tests for the SystemResilienceAssessor.
    """

    def setUp(self):
        """
        Set up the test case.
        """
        self.assessor = SystemResilienceAssessor()
        self.engine = CognitiveEcosystemEngine(config={})
        self.engine.register_agent("agent_1", None, {})
        self.engine.register_agent("agent_2", None, {})
        self.engine.register_agent("agent_3", None, {})

    def test_simulate_agent_removal(self):
        """
        Test the simulation of agent removal.
        """
        result = self.assessor.simulate_agent_removal(self.engine, "agent_1")
        self.assertIsInstance(result, dict)
        self.assertEqual(result["removed_agent"], "agent_1")
        self.assertAlmostEqual(result["performance_drop_percentage"], 33.333, 3)

    def test_apply_information_shock(self):
        """
        Test the application of an information shock.
        """
        result = self.assessor.apply_information_shock(self.engine, "contradictory_fact", "new data", ["agent_1", "agent_2"])
        self.assertIsInstance(result, dict)
        self.assertEqual(result["shock_type"], "contradictory_fact")
        self.assertAlmostEqual(result["adaptation_ratio"], 2/3)

    def test_measure_recovery_capacity(self):
        """
        Test the measurement of recovery capacity.
        """
        recovery = self.assessor.measure_recovery_capacity(100, 80)
        self.assertEqual(recovery, 0.8)

    def test_calculate_resilience_score(self):
        """
        Test the calculation of the resilience score.
        """
        test_results = [
            {"test_type": "agent_removal", "performance_drop_percentage": 25},
            {"test_type": "information_shock", "adaptation_ratio": 0.75}
        ]
        score = self.assessor.calculate_resilience_score(test_results)
        self.assertEqual(score, 0.75)

if __name__ == '__main__':
    unittest.main()
