import logging
import copy
from typing import List, Dict, Any
import numpy as np

# Configure basic logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class SystemResilienceAssessor:
    """
    Assesses the resilience of the cognitive ecosystem through various stress tests.
    """
    def __init__(self):
        """
        Initializes the SystemResilienceAssessor.
        """
        self.stress_tests = [
            'agent_removal_test',
            'information_shock_test',
            'cognitive_load_test',
            'adversarial_input_test'
        ]
        logging.info("SystemResilienceAssessor initialized.")

    def simulate_agent_removal(self, ecosystem_engine, removed_agent_id: str) -> Dict[str, Any]:
        """
        Simulates the removal of an agent and measures the impact on the ecosystem.
        This requires a baseline performance metric to compare against.

        Args:
            ecosystem_engine: The instance of the CognitiveEcosystemEngine.
            removed_agent_id (str): The ID of the agent to remove.

        Returns:
            A dictionary containing the results of the agent removal simulation.
        """
        if removed_agent_id not in ecosystem_engine.agents:
            logging.error(f"Agent '{removed_agent_id}' not found in the ecosystem.")
            return {"error": "Agent not found"}

        logging.info(f"Simulating removal of agent: {removed_agent_id}")

        # Create a deep copy of the engine to avoid modifying the original state
        resilient_ecosystem = copy.deepcopy(ecosystem_engine)
        
        # Remove the agent
        del resilient_ecosystem.agents[removed_agent_id]
        if removed_agent_id in resilient_ecosystem.niche_map:
            del resilient_ecosystem.niche_map[removed_agent_id]

        # The "impact" is highly dependent on a performance metric.
        # For this simulation, we'll use cognitive diversity as a proxy.
        
        # Baseline performance (before removal)
        baseline_diversity = ecosystem_engine.analyze_cognitive_diversity()['diversity_score']

        # Performance after removal
        post_removal_diversity = resilient_ecosystem.analyze_cognitive_diversity()['diversity_score']
        
        performance_drop = (baseline_diversity - post_removal_diversity) / baseline_diversity if baseline_diversity > 0 else 0

        return {
            "test_type": "agent_removal",
            "removed_agent": removed_agent_id,
            "performance_drop_percentage": performance_drop * 100,
            "baseline_metric": baseline_diversity,
            "post_removal_metric": post_removal_diversity
        }

    def apply_information_shock(self, ecosystem_engine, shock_type: str, shock_content: Any, affected_agents: List[str]) -> Dict[str, Any]:
        """
        Applies an information shock to the ecosystem and observes the response.

        Args:
            ecosystem_engine: The instance of the CognitiveEcosystemEngine.
            shock_type (str): The type of information shock (e.g., 'contradictory_fact').
            shock_content: The content of the shock.
            affected_agents (List[str]): A list of agent IDs affected by the shock.

        Returns:
            A dictionary with the results of the information shock test.
        """
        logging.info(f"Applying information shock of type '{shock_type}'.")
        
        num_agents = len(ecosystem_engine.agents)
        adapted_agents = len(affected_agents)
        
        adaptation_ratio = adapted_agents / num_agents if num_agents > 0 else 0
        
        return {
            "test_type": "information_shock",
            "shock_type": shock_type,
            "adaptation_ratio": adaptation_ratio
        }

    def measure_recovery_capacity(self, pre_shock_metric: float, post_shock_metric: float) -> float:
        """
        Measures the capacity of the system to recover after a shock.

        Args:
            pre_shock_metric (float): The performance metric before the shock.
            post_shock_metric (float): The performance metric after the shock and recovery period.

        Returns:
            A recovery score from 0.0 to 1.0.
        """
        if pre_shock_metric == 0:
            return 1.0 if post_shock_metric >= 0 else 0.0
            
        recovery_ratio = post_shock_metric / pre_shock_metric
        
        return min(1.0, max(0.0, recovery_ratio))

    def calculate_resilience_score(self, test_results: List[Dict[str, Any]]) -> float:
        """
        Calculates an overall resilience score based on multiple stress test results.

        Args:
            test_results (List[Dict[str, Any]]): A list of results from various stress tests.

        Returns:
            A composite resilience score from 0.0 to 1.0.
        """
        if not test_results:
            return 0.0

        scores = []
        for result in test_results:
            if result.get("test_type") == "agent_removal":
                # Lower performance drop is better
                scores.append(1.0 - (result.get("performance_drop_percentage", 100) / 100.0))
            elif result.get("test_type") == "information_shock":
                # Higher adaptation is better
                scores.append(result.get("adaptation_ratio", 0.0))
        
        return np.mean(scores) if scores else 0.0
