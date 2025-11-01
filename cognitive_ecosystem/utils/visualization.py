import logging
import matplotlib.pyplot as plt
import numpy as np
import networkx as nx
from typing import List, Dict, Any

# Configure basic logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class Visualization:
    """
    Provides methods to generate various visualizations for the cognitive ecosystem analysis.
    """
    def __init__(self, output_dir: str = "test_reports"):
        """
        Initializes the Visualization class.
        
        Args:
            output_dir (str): The directory to save generated plots.
        """
        self.output_dir = output_dir
        logging.info(f"Visualization utility initialized. Output directory: {self.output_dir}")

    def plot_cognitive_niche_map(self, niches: List[Dict[str, Any]], save_path: str):
        """
        Creates a 2D scatter plot representing the cognitive niches of agents.
        Uses PCA for dimensionality reduction.
        """
        if not niches:
            logging.warning("No niche data to plot.")
            return

        labels = [n['agent_id'] for n in niches]
        vectors = [list(n['cognitive_vector'].values()) for n in niches]
        
        if len(vectors[0]) < 2:
            logging.warning("Cannot plot niches with less than 2 dimensions.")
            return

        # Use PCA to reduce to 2 dimensions for plotting
        from sklearn.decomposition import PCA
        pca = PCA(n_components=2)
        transformed_vectors = pca.fit_transform(vectors)

        plt.figure(figsize=(10, 8))
        scatter = plt.scatter(transformed_vectors[:, 0], transformed_vectors[:, 1], s=100)
        
        for i, label in enumerate(labels):
            plt.annotate(label, (transformed_vectors[i, 0], transformed_vectors[i, 1]))

        plt.title("Cognitive Niche Map (PCA)")
        plt.xlabel("Principal Component 1")
        plt.ylabel("Principal Component 2")
        plt.grid(True)
        plt.savefig(f"{self.output_dir}/{save_path}")
        plt.close()
        logging.info(f"Cognitive niche map saved to {self.output_dir}/{save_path}")

    def plot_resilience_radar_chart(self, resilience_scores: Dict[str, float], save_path: str):
        """
        Creates a radar chart to visualize system resilience across different stress tests.
        """
        labels = list(resilience_scores.keys())
        stats = list(resilience_scores.values())
        
        angles = np.linspace(0, 2 * np.pi, len(labels), endpoint=False).tolist()
        stats = np.concatenate((stats,[stats[0]]))
        angles += angles[:1]

        fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))
        ax.fill(angles, stats, color='red', alpha=0.25)
        ax.plot(angles, stats, color='red', linewidth=2)
        
        ax.set_yticklabels([])
        ax.set_xticks(angles[:-1])
        ax.set_xticklabels(labels)
        
        plt.title("System Resilience Radar Chart")
        plt.savefig(f"{self.output_dir}/{save_path}")
        plt.close()
        logging.info(f"Resilience radar chart saved to {self.output_dir}/{save_path}")

    def plot_personality_evolution(self, personality_history: Dict[str, List[Dict]], save_path: str):
        """
        Plots the evolution of personality traits over time for multiple agents.
        """
        plt.figure(figsize=(12, 7))
        
        for agent_id, history in personality_history.items():
            timestamps = [h['timestamp'] for h in history]
            stances = [h['stance'] for h in history]
            plt.plot(timestamps, stances, marker='o', linestyle='-', label=agent_id)

        plt.title("Longitudinal Personality Evolution")
        plt.xlabel("Time")
        plt.ylabel("Stance Score")
        plt.legend()
        plt.grid(True)
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig(f"{self.output_dir}/{save_path}")
        plt.close()
        logging.info(f"Personality evolution plot saved to {self.output_dir}/{save_path}")

    def plot_emergence_trend(self, emergence_scores: List[float], timestamps: List[Any], save_path: str):
        """
        Plots the trend of collective intelligence emergence over time.
        """
        plt.figure(figsize=(10, 6))
        plt.plot(timestamps, emergence_scores, marker='.', linestyle='--')
        plt.title("Collective Intelligence Emergence Trend")
        plt.xlabel("Time")
        plt.ylabel("Emergence Score")
        plt.grid(True)
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig(f"{self.output_dir}/{save_path}")
        plt.close()
        logging.info(f"Emergence trend plot saved to {self.output_dir}/{save_path}")
