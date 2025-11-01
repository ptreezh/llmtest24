import logging
from typing import List, Dict, Any

# Configure basic logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class VanillaAgent:
    """
    A baseline agent that responds to prompts without any specific role-playing.
    This serves as a control group for comparison against specialized agents.
    """
    def __init__(self, base_model):
        """
        Initializes the VanillaAgent.

        Args:
            base_model: The underlying language model instance used for generation.
                        This model should have a `generate` method.
        """
        self.model = base_model
        self.no_role_prompt = True  # Explicitly state that no role prompt is used
        logging.info(f"VanillaAgent initialized with model: {type(base_model).__name__}")

    def generate_response(self, prompt: str) -> str:
        """
        Generates a direct, non-role-played response to a given prompt.

        Args:
            prompt (str): The input prompt for the model.

        Returns:
            The generated text response.
        """
        logging.info("Generating baseline response.")
        try:
            # Assuming the base_model has a standard generation method.
            # This might need to be adapted based on the actual model's API.
            if hasattr(self.model, 'generate_response'):
                response = self.model.generate_response(prompt)
            elif hasattr(self.model, 'generate'):
                response = self.model.generate(prompt)
            elif hasattr(self.model, 'predict'):
                response = self.model.predict(prompt)
            else:
                raise NotImplementedError("The provided base model does not have a recognized generation method.")
            
            return response
        except Exception as e:
            logging.error(f"Error during baseline response generation: {e}")
            return "Error: Could not generate a response."

    def run_baseline_tests(self, test_scenarios: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Runs a series of test scenarios through the vanilla agent to generate baseline results.

        Args:
            test_scenarios (List[Dict[str, Any]]): A list of scenarios, each with a 'prompt'.

        Returns:
            A list of results, each containing the original scenario and the agent's response.
        """
        logging.info(f"Running {len(test_scenarios)} baseline tests.")
        baseline_results = []
        for scenario in test_scenarios:
            prompt = scenario.get("prompt")
            if not prompt:
                logging.warning(f"Skipping scenario with no prompt: {scenario}")
                continue
            
            response = self.generate_response(prompt)
            
            result = {
                "scenario": scenario,
                "baseline_response": response
            }
            baseline_results.append(result)
        
        logging.info("Baseline tests completed.")
        return baseline_results
