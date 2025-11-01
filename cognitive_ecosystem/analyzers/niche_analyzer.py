import logging
import numpy as np
from typing import List, Dict
from cognitive_ecosystem.core.cognitive_niche import CognitiveNiche

# Configure basic logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class CognitiveNicheAnalyzer:
    """
    Analyzes the cognitive niches of agents within the ecosystem to understand
    diversity, overlap, and functional roles.
    """
    def __init__(self):
        """
        Initializes the CognitiveNicheAnalyzer.
        """
        self.niche_metrics = [
            'knowledge_specialization',
            'reasoning_uniqueness', 
            'functional_contribution',
            'interaction_patterns'
        ]
        logging.info("CognitiveNicheAnalyzer initialized.")

    def calculate_niche_differentiation(self, agent_niches: List[CognitiveNiche]) -> float:
        """
        Calculates the overall niche differentiation in the ecosystem.
        This is measured as the average distance between all pairs of agent niches.

        Args:
            agent_niches (List[CognitiveNiche]): A list of CognitiveNiche objects.

        Returns:
            A score from 0.0 to 1.0 representing the average differentiation.
        """
        if len(agent_niches) < 2:
            return 0.0

        distances = []
        for i in range(len(agent_niches)):
            for j in range(i + 1, len(agent_niches)):
                niche1 = agent_niches[i]
                niche2 = agent_niches[j]
                distance = niche1.cognitive_vector.distance_to(niche2.cognitive_vector)
                distances.append(distance)
        
        avg_distance = np.mean(distances) if distances else 0.0
        
        # Normalize by the maximum possible distance
        max_distance = np.sqrt(len(agent_niches[0].cognitive_vector.to_array()))
        return avg_distance / max_distance if max_distance > 0 else 0.0

    def identify_niche_overlap(self, agent_niches: List[CognitiveNiche]) -> Dict[str, float]:
        """
        Identifies pairs of agents with significant niche overlap.

        Args:
            agent_niches (List[CognitiveNiche]): A list of CognitiveNiche objects.

        Returns:
            A dictionary of agent pairs (as a tuple string) and their overlap score.
        """
        overlaps = {}
        for i in range(len(agent_niches)):
            for j in range(i + 1, len(agent_niches)):
                niche1 = agent_niches[i]
                niche2 = agent_niches[j]
                
                overlap_score = niche1.calculate_niche_overlap(niche2)
                
                pair_key = tuple(sorted((niche1.agent_id, niche2.agent_id)))
                overlaps[str(pair_key)] = overlap_score
        
        return overlaps

    def measure_ecosystem_diversity(self, agent_niches: List[CognitiveNiche]) -> float:
        """
        Measures the overall cognitive diversity of the ecosystem based on niche analysis.
        This uses a combination of differentiation and niche breadth.

        Args:
            agent_niches (List[CognitiveNiche]): A list of CognitiveNiche objects.

        Returns:
            A composite diversity score from 0.0 to 1.0.
        """
        if not agent_niches:
            return 0.0

        differentiation = self.calculate_niche_differentiation(agent_niches)
        
        breadths = [niche.calculate_niche_breadth() for niche in agent_niches]
        avg_breadth = np.mean(breadths) if breadths else 0.0

        # Combine metrics (example weighting)
        diversity_score = (differentiation * 0.6) + (avg_breadth * 0.4)
        return min(1.0, max(0.0, diversity_score))

    def detect_functional_redundancy(self, agent_niches: List[CognitiveNiche], threshold: float = 0.85) -> List[tuple]:
        """
        Detects functional redundancy by finding pairs of agents with very high niche overlap.

        Args:
            agent_niches (List[CognitiveNiche]): A list of CognitiveNiche objects.
            threshold (float): The overlap threshold to be considered redundant.

        Returns:
            A list of tuples, where each tuple contains the agent IDs of a redundant pair.
        """
        redundant_pairs = []
        overlap_map = self.identify_niche_overlap(agent_niches)

        for pair_str, score in overlap_map.items():
            if score > threshold:
                # Convert string representation of tuple back to tuple
                redundant_pairs.append(eval(pair_str))
                
        return redundant_pairs
