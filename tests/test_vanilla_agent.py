import unittest
import os
import sys

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from cognitive_ecosystem.baselines.vanilla_agent import VanillaAgent

class MockModel:
    def generate(self, prompt):
        return f"Response to: {prompt}"

class TestVanillaAgent(unittest.TestCase):
    """
    Unit tests for the VanillaAgent.
    """

    def setUp(self):
        """
        Set up the test case.
        """
        self.model = MockModel()
        self.agent = VanillaAgent(self.model)

    def test_generate_response(self):
        """
        Test the generation of a baseline response.
        """
        prompt = "What is the capital of France?"
        response = self.agent.generate_response(prompt)
        self.assertEqual(response, "Response to: What is the capital of France?")

    def test_run_baseline_tests(self):
        """
        Test running a series of baseline tests.
        """
        scenarios = [
            {"prompt": "Scenario 1"},
            {"prompt": "Scenario 2"}
        ]
        results = self.agent.run_baseline_tests(scenarios)
        self.assertEqual(len(results), 2)
        self.assertEqual(results[0]["baseline_response"], "Response to: Scenario 1")

if __name__ == '__main__':
    unittest.main()
