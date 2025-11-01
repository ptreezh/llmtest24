import logging
from typing import List, Dict, Any
from collections import defaultdict
import numpy as np

# Configure basic logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class PersonalityTracker:
    """
    Tracks the longitudinal stability of agent personalities within the ecosystem.
    """
    def __init__(self):
        """
        Initializes the PersonalityTracker.
        """
        self.personality_dimensions = [
            'stance_consistency',    # Consistency of opinions on a topic over time
            'argument_evolution',    # How arguments change or deepen
            'memory_integration',    # Integration of new information with past interactions
            'learning_adaptation'    # Adaptation based on feedback or new data
        ]
        # In-memory storage for agent history. A database would be used in a larger system.
        self.agent_history = defaultdict(lambda: {'stances': [], 'responses': []})
        logging.info("PersonalityTracker initialized.")

    def track_stance_evolution(self, agent_id: str, topic: str, stance: float, timestamp: Any):
        """
        Records an agent's stance on a specific topic at a given time.

        Args:
            agent_id (str): The ID of the agent.
            topic (str): The topic being discussed.
            stance (float): A numerical representation of the stance (e.g., -1 for against, 1 for for).
            timestamp: The time of the stance measurement.
        """
        self.agent_history[agent_id]['stances'].append({
            'topic': topic,
            'stance': stance,
            'timestamp': timestamp
        })
        logging.info(f"Tracked stance for agent '{agent_id}' on topic '{topic}'.")

    def measure_memory_integration(self, agent_id: str, new_response: str, historical_context: List[str]) -> float:
        """
        Measures how well an agent integrates historical context into a new response.
        This is a heuristic and would ideally use more advanced NLP.

        Args:
            agent_id (str): The ID of the agent.
            new_response (str): The agent's latest response.
            historical_context (List[str]): A list of previous relevant interactions.

        Returns:
            A score from 0.0 to 1.0 representing memory integration.
        """
        if not historical_context:
            return 0.0
        
        # Simple keyword-based check for integration
        historical_keywords = set(" ".join(historical_context).lower().split())
        response_keywords = set(new_response.lower().split())
        
        common_keywords = historical_keywords.intersection(response_keywords)
        
        # Normalize by the number of historical keywords (or response keywords, depending on desired metric)
        integration_score = len(common_keywords) / len(historical_keywords) if historical_keywords else 0.0
        
        return min(1.0, integration_score)

    def detect_personality_drift(self, agent_id: str, time_window_days: int = 7) -> Dict[str, Any]:
        """
        Detects significant changes in an agent's personality over a time window.

        Args:
            agent_id (str): The ID of the agent.
            time_window_days (int): The number of days to look back for analysis.

        Returns:
            A dictionary containing drift analysis results.
        """
        if agent_id not in self.agent_history:
            return {"status": "no_history", "message": "No history found for this agent."}

        # Analyze stance consistency
        stances = self.agent_history[agent_id].get('stances', [])
        topic_stances = defaultdict(list)
        for s in stances:
            topic_stances[s['topic']].append(s['stance'])

        stance_drift = {}
        for topic, topic_stance_values in topic_stances.items():
            if len(topic_stance_values) > 1:
                # Calculate standard deviation as a measure of drift
                drift_score = np.std(topic_stance_values)
                stance_drift[topic] = drift_score
        
        # A more complex implementation would analyze response style, vocabulary, etc.
        
        return {
            "agent_id": agent_id,
            "stance_drift_scores": stance_drift,
            "overall_consistency": 1.0 - np.mean(list(stance_drift.values())) if stance_drift else 1.0
        }

    def record_response(self, agent_id: str, response: str, timestamp: Any):
        """
        Records a generic response from an agent for future analysis.
        """
        self.agent_history[agent_id]['responses'].append({
            'response': response,
            'timestamp': timestamp
        })
