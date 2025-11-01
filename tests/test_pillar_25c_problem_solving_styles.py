import sys
import os

# Add project root to Python path to ensure imports work
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import unittest
import os
import sys
# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from cognitive_ecosystem.detectors.style_analyzer import ProblemSolvingStyleAnalyzer
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
    suite = loader.loadTestsFromTestCase(TestProblemSolvingStyleAnalyzer)
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

class TestProblemSolvingStyleAnalyzer(unittest.TestCase):
    """
    Unit tests for the ProblemSolvingStyleAnalyzer.
    """

    def setUp(self):
        """
        Set up the test case.
        """
        self.analyzer = ProblemSolvingStyleAnalyzer()
        self.responses = [
            "The project is a journey, we need a map to navigate the challenges.",
            "Let's architect a solution. The foundation must be solid, with scalable pillars.",
            "This problem is a tangled web. We need to find the critical thread to unravel it.",
            "We should plant the seeds of innovation and nurture them into a flourishing outcome."
        ]
        self.agent_responses = {
            "agent_1": "The project is a journey, we need a map to navigate the challenges.",
            "agent_2": "Let's architect a solution. The foundation must be solid, with scalable pillars.",
            "agent_3": "This problem is a tangled web. We need to find the critical thread to unravel it.",
            "agent_4": "We should plant the seeds of innovation and nurture them into a flourishing outcome."
        }

    def test_analyze_metaphor_diversity(self):
        """
        Test the analysis of metaphor diversity.
        """
        diversity_score = self.analyzer.analyze_metaphor_diversity(self.responses)
        self.assertIsInstance(diversity_score, float)
        self.assertGreater(diversity_score, 0)

    def test_measure_knowledge_domain_spread(self):
        """
        Test the measurement of knowledge domain spread.
        """
        spread_score = self.analyzer.measure_knowledge_domain_spread(self.responses)
        self.assertIsInstance(spread_score, float)
        self.assertGreater(spread_score, 0)

    def test_calculate_style_distance_matrix(self):
        """
        Test the calculation of the style distance matrix.
        """
        distance_matrix = self.analyzer.calculate_style_distance_matrix(self.agent_responses)
        self.assertIsInstance(distance_matrix, dict)
        self.assertIn("agent_1", distance_matrix)
        self.assertIn("agent_2", distance_matrix["agent_1"])
        self.assertAlmostEqual(distance_matrix["agent_1"]["agent_1"], 0.0, places=10)

if __name__ == '__main__':
    unittest.main()
