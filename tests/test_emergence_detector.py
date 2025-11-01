import unittest
import os
import sys

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from cognitive_ecosystem.analyzers.emergence_detector import EmergenceDetector

class TestEmergenceDetector(unittest.TestCase):
    """
    Unit tests for the EmergenceDetector.
    """

    def setUp(self):
        """
        Set up the test case.
        """
        self.detector = EmergenceDetector()

    def test_detect_collective_intelligence(self):
        """
        Test the detection of collective intelligence.
        """
        synergy = self.detector.detect_collective_intelligence(120, 100)
        self.assertAlmostEqual(synergy, 0.2)

    def test_measure_synergy_effects(self):
        """
        Test the measurement of synergy effects.
        """
        effects = self.detector.measure_synergy_effects([0.8, 0.9, 0.7])
        self.assertAlmostEqual(effects, 0.8)

    def test_identify_emergent_properties(self):
        """
        Test the identification of emergent properties.
        """
        properties = self.detector.identify_emergent_properties({})
        self.assertIn("synergy", properties)
        self.assertIn("specialization", properties)

if __name__ == '__main__':
    unittest.main()
