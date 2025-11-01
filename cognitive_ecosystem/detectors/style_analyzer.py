import logging
import numpy as np
from typing import List, Dict, Any
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import nltk
from nltk.corpus import wordnet as wn
from pathlib import Path
import os

# Configure basic logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Define NLTK data directory within the project
PROJECT_ROOT = Path(__file__).parent.parent.parent # Adjust if necessary to point to your project root
NLTK_DATA_DIR = PROJECT_ROOT / "data" / "nltk_data"
NLTK_DATA_DIR.mkdir(parents=True, exist_ok=True) # Ensure directory exists

# Add the custom data path to NLTK
nltk.data.path.append(str(NLTK_DATA_DIR))

# Ensure NLTK data is available
def download_nltk_data():
    """Downloads NLTK data if not already present."""
    datasets = ['wordnet', 'punkt', 'averaged_perceptron_tagger']
    for dataset in datasets:
        try:
            nltk.data.find(f'tokenizers/{dataset}' if dataset == 'punkt' else f'taggers/{dataset}' if dataset == 'averaged_perceptron_tagger' else f'corpora/{dataset}')
            logging.info(f"NLTK data '{dataset}' already present.")
        except LookupError:
            logging.info(f"Downloading NLTK data '{dataset}' to {NLTK_DATA_DIR}...")
            nltk.download(dataset, download_dir=str(NLTK_DATA_DIR))
            logging.info(f"NLTK data '{dataset}' downloaded.")
        except Exception as e:
            logging.error(f"Error checking/downloading NLTK data '{dataset}': {e}")

# Call the download function once when the module is imported
download_nltk_data()

class ProblemSolvingStyleAnalyzer:
    """
    Analyzes the diversity of problem-solving styles within the cognitive ecosystem.
    """
    def __init__(self):
        """
        Initializes the ProblemSolvingStyleAnalyzer.
        """
        self.style_dimensions = [
            'metaphor_generation',
            'knowledge_domain_preference',
            'reasoning_approach',  # e.g., deductive, inductive, abductive
            'abstraction_level'    # e.g., concrete vs. abstract
        ]
        self.vectorizer = TfidfVectorizer(stop_words='english')
        logging.info("ProblemSolvingStyleAnalyzer initialized.")

    def analyze_metaphor_diversity(self, responses: List[str]) -> float:
        """
        Analyzes the diversity of metaphors used in responses.
        A simple heuristic: counts the number of unique nouns used as potential metaphors.
        
        Args:
            responses (List[str]): A list of text responses from agents.

        Returns:
            A score representing metaphor diversity.
        """
        if not responses:
            return 0.0

        all_nouns = set()
        for text in responses:
            tokens = nltk.word_tokenize(text)
            tagged = nltk.pos_tag(tokens)
            nouns = {word for word, pos in tagged if pos.startswith('NN')}
            all_nouns.update(nouns)
        
        # Diversity score is based on the ratio of unique nouns to the total number of responses
        diversity_score = len(all_nouns) / len(responses) if responses else 0.0
        return min(1.0, diversity_score / 10) # Normalize

    def measure_knowledge_domain_spread(self, responses: List[str]) -> float:
        """
        Measures the spread of knowledge domains covered in the responses using TF-IDF.

        Args:
            responses (List[str]): A list of text responses from agents.

        Returns:
            A score representing the diversity of knowledge domains.
        """
        if len(responses) < 2:
            return 0.0
        
        try:
            tfidf_matrix = self.vectorizer.fit_transform(responses)
            # Diversity is inversely related to the average similarity between documents
            similarity_matrix = cosine_similarity(tfidf_matrix)
            # We only need the upper triangle of the matrix (excluding the diagonal)
            upper_triangle_indices = np.triu_indices_from(similarity_matrix, k=1)
            average_similarity = np.mean(similarity_matrix[upper_triangle_indices])
            
            diversity_score = 1.0 - average_similarity
            return diversity_score
        except ValueError:
            # Can happen if vocabulary is empty
            return 0.0

    def calculate_style_distance_matrix(self, agent_responses: Dict[str, str]) -> Dict[str, Dict[str, float]]:
        """
        Calculates a distance matrix based on the textual similarity of agent responses.

        Args:
            agent_responses (Dict[str, str]): A dictionary mapping agent IDs to their text responses.

        Returns:
            A nested dictionary representing the style distance matrix.
        """
        if len(agent_responses) < 2:
            return {}

        agent_ids = list(agent_responses.keys())
        responses = list(agent_responses.values())
        
        try:
            tfidf_matrix = self.vectorizer.fit_transform(responses)
            similarity_matrix = cosine_similarity(tfidf_matrix)
            distance_matrix = 1 - similarity_matrix
        except ValueError:
            # Handle case with empty vocabulary
            num_agents = len(agent_ids)
            distance_matrix = np.ones((num_agents, num_agents))

        style_distance = {}
        for i, agent_id_1 in enumerate(agent_ids):
            style_distance[agent_id_1] = {}
            for j, agent_id_2 in enumerate(agent_ids):
                style_distance[agent_id_1][agent_id_2] = float(distance_matrix[i, j])
                
        return style_distance
