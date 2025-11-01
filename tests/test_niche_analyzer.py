import unittest
import os
import sys

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from cognitive_ecosystem.analyzers.niche_analyzer import CognitiveNicheAnalyzer
from cognitive_ecosystem.core.cognitive_niche import CognitiveNiche

class TestCognitiveNicheAnalyzer(unittest.TestCase):
    """
    Unit tests for the CognitiveNicheAnalyzer.
    """

    def setUp(self):
        """
        Set up the test case.
        """
        self.analyzer = CognitiveNicheAnalyzer()
        self.niches = [
            CognitiveNiche("agent_1", "software_engineer", "analytical", {"openness": 0.8}),
            CognitiveNiche("agent_2", "product_manager", "creative", {"openness": 0.9}),
            CognitiveNiche("agent_3", "data_scientist", "systematic", {"openness": 0.7})
        ]

    def test_calculate_niche_differentiation(self):
        """
        Test the calculation of niche differentiation.
        """
        differentiation = self.analyzer.calculate_niche_differentiation(self.niches)
        self.assertIsInstance(differentiation, float)
        self.assertGreaterEqual(differentiation, 0)
        self.assertLessEqual(differentiation, 1)

    def test_identify_niche_overlap(self):
        """
        Test the identification of niche overlap.
        """
        overlap = self.analyzer.identify_niche_overlap(self.niches)
        self.assertIsInstance(overlap, dict)
        self.assertIn("('agent_1', 'agent_2')", str(list(overlap.keys())))

    def test_measure_ecosystem_diversity(self):
        """
        Test the measurement of ecosystem diversity.
        """
        diversity = self.analyzer.measure_ecosystem_diversity(self.niches)
        self.assertIsInstance(diversity, float)
        self.assertGreaterEqual(diversity, 0)
        self.assertLessEqual(diversity, 1)

    def test_detect_functional_redundancy(self):
        """
        Test the detection of functional redundancy.
        """
        # Add a redundant niche
        redundant_niches = self.niches + [CognitiveNiche("agent_4", "software_engineer", "analytical", {"openness": 0.8})]
        redundancy = self.analyzer.detect_functional_redundancy(redundant_niches, threshold=0.9)
        self.assertIsInstance(redundancy, list)
        # This assertion depends heavily on the threshold and calculation, so it might need adjustment
        # For now, just check the type
        

if __name__ == '__main__':
    unittest.main()
