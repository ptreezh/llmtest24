import logging
from typing import List, Dict, Any

# Configure basic logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class CognitiveBiasDetector:
    """
    Designs and executes tests to measure cognitive bias congruence within the ecosystem.
    """
    def __init__(self):
        """
        Initializes the CognitiveBiasDetector.
        """
        self.bias_types = [
            'anchoring_bias',
            'confirmation_bias', 
            'availability_heuristic',
            'representativeness_heuristic'
        ]
        logging.info("CognitiveBiasDetector initialized.")

    def setup_anchoring_trap(self, anchor_value: float, question: str) -> Dict[str, Any]:
        """
        Creates a scenario to test for anchoring bias.

        Args:
            anchor_value (float): The numerical anchor to present to the agents.
            question (str): The question to ask that might be influenced by the anchor.

        Returns:
            A dictionary representing the anchoring bias test scenario.
        """
        logging.info(f"Setting up anchoring trap with anchor: {anchor_value}")
        return {
            "bias_type": "anchoring_bias",
            "anchor_value": anchor_value,
            "prompt": f"Considering the initial estimate of {anchor_value}, {question}"
        }

    def measure_bias_congruence(self, agent_responses: List[Dict[str, Any]], test_scenario: Dict[str, Any]) -> Dict[str, Any]:
        """
        Measures the degree to which agents' responses exhibit the targeted cognitive bias.

        Args:
            agent_responses (List[Dict[str, Any]]): A list of agent responses.
            test_scenario (Dict[str, Any]): The bias test scenario that was run.

        Returns:
            A dictionary containing the analysis of bias congruence.
        """
        bias_type = test_scenario.get("bias_type")
        logging.info(f"Measuring bias congruence for '{bias_type}'.")

        if bias_type == "anchoring_bias":
            return self._measure_anchoring_congruence(agent_responses, test_scenario)
        
        # Placeholder for other bias types
        logging.warning(f"Measurement for bias type '{bias_type}' is not yet implemented.")
        return {"status": "not_implemented"}

    def _measure_anchoring_congruence(self, agent_responses: List[Dict[str, Any]], test_scenario: Dict[str, Any]) -> Dict[str, Any]:
        """
        Specifically measures congruence for anchoring bias.
        """
        anchor_value = test_scenario.get("anchor_value")
        influenced_responses = 0
        total_responses = len(agent_responses)
        deviations = []

        for response in agent_responses:
            # This assumes the response contains a numerical answer that can be extracted.
            # A more robust implementation would use NLP to extract numbers.
            try:
                # A simple heuristic: check if the number is "close" to the anchor.
                # This needs to be adapted to the specific question's scale.
                numerical_response = float(response.get("numerical_answer", 0))
                deviation = abs(numerical_response - anchor_value) / anchor_value if anchor_value != 0 else 0
                deviations.append(deviation)
                if deviation < 0.5: # Arbitrary threshold for "influenced"
                    influenced_responses += 1
            except (ValueError, TypeError):
                continue

        congruence_ratio = influenced_responses / total_responses if total_responses > 0 else 0.0
        
        return {
            "bias_type": "anchoring_bias",
            "congruence_ratio": congruence_ratio,
            "influenced_count": influenced_responses,
            "total_responses": total_responses,
            "average_deviation": sum(deviations) / len(deviations) if deviations else 0.0
        }

    def detect_bias_resistance(self, agent_responses: List[Dict[str, Any]], test_scenario: Dict[str, Any]) -> List[str]:
        """
        Identifies agents that show resistance to the induced bias.

        Args:
            agent_responses (List[Dict[str, Any]]): The list of agent responses.
            test_scenario (Dict[str, Any]): The bias test scenario.

        Returns:
            A list of agent IDs that demonstrated resistance.
        """
        resistant_agents = []
        if test_scenario.get("bias_type") == "anchoring_bias":
            anchor_value = test_scenario.get("anchor_value")
            for response in agent_responses:
                try:
                    numerical_response = float(response.get("numerical_answer", 0))
                    deviation = abs(numerical_response - anchor_value) / anchor_value if anchor_value != 0 else 0
                    # Agents whose answers are far from the anchor are considered resistant
                    if deviation > 0.8: # Arbitrary threshold
                        resistant_agents.append(response.get("agent_id"))
                except (ValueError, TypeError):
                    # Agents that didn't provide a numerical answer might also be resistant
                    # by challenging the premise, but this is harder to detect automatically.
                    pass
        
        return resistant_agents
