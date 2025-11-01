import sys
import os

# Add project root to Python path to ensure imports work
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import unittest
import os
import sys
# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import time

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from cognitive_ecosystem.detectors.personality_tracker import PersonalityTracker

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
    suite = loader.loadTestsFromTestCase(TestPersonalityTracker)
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

class TestPersonalityTracker(unittest.TestCase):
    """
    Unit tests for the PersonalityTracker.
    """

    def setUp(self):
        """
        Set up the test case.
        """
        self.tracker = PersonalityTracker()
        self.agent_id = "test_agent"

    def test_track_stance_evolution(self):
        """
        Test the tracking of stance evolution.
        """
        self.tracker.track_stance_evolution(self.agent_id, "AI_safety", 0.8, time.time())
        self.tracker.track_stance_evolution(self.agent_id, "AI_safety", 0.7, time.time())
        
        history = self.tracker.agent_history[self.agent_id]
        self.assertEqual(len(history['stances']), 2)
        self.assertEqual(history['stances'][0]['topic'], "AI_safety")

    def test_measure_memory_integration(self):
        """
        Test the measurement of memory integration.
        """
        historical_context = ["The cat sat on the mat.", "It was a fluffy cat."]
        new_response = "The fluffy cat is now sleeping on the mat."
        
        integration_score = self.tracker.measure_memory_integration(self.agent_id, new_response, historical_context)
        self.assertIsInstance(integration_score, float)
        self.assertGreater(integration_score, 0)

    def test_detect_personality_drift(self):
        """
        Test the detection of personality drift.
        """
        self.tracker.track_stance_evolution(self.agent_id, "climate_change", 0.9, time.time())
        self.tracker.track_stance_evolution(self.agent_id, "climate_change", 0.2, time.time())
        self.tracker.track_stance_evolution(self.agent_id, "climate_change", 0.8, time.time())

        drift_analysis = self.tracker.detect_personality_drift(self.agent_id)
        self.assertIsInstance(drift_analysis, dict)
        self.assertIn("stance_drift_scores", drift_analysis)
        self.assertIn("climate_change", drift_analysis["stance_drift_scores"])
        self.assertGreater(drift_analysis["stance_drift_scores"]["climate_change"], 0)

if __name__ == '__main__':
    unittest.main()
