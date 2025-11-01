import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, Any

# Configure basic logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class StateManager:
    """
    Manages the state of the cognitive ecosystem, including saving, loading,
    and creating snapshots of the system's state.
    """
    def __init__(self, storage_dir: str = "ecosystem_states"):
        """
        Initializes the StateManager.

        Args:
            storage_dir (str): The directory where state files will be stored.
        """
        self.storage_path = Path(storage_dir)
        self.storage_path.mkdir(parents=True, exist_ok=True)
        logging.info(f"StateManager initialized. Storage directory: '{self.storage_path}'")

    def save_state(self, ecosystem_engine, file_name: str = None) -> Path:
        """
        Saves the current state of the cognitive ecosystem to a file.

        Args:
            ecosystem_engine: The instance of the CognitiveEcosystemEngine.
            file_name (str, optional): The name of the file to save the state to.
                                       If not provided, a timestamped name is generated.

        Returns:
            Path: The path to the saved state file.
        """
        if file_name is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            file_name = f"ecosystem_state_{timestamp}.json"
        
        file_path = self.storage_path / file_name
        
        state_data = self._capture_ecosystem_state(ecosystem_engine)
        
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(state_data, f, indent=4, ensure_ascii=False)
            logging.info(f"Ecosystem state successfully saved to '{file_path}'")
            return file_path
        except (IOError, TypeError) as e:
            logging.error(f"Failed to save ecosystem state to '{file_path}': {e}")
            raise

    def load_state(self, ecosystem_engine, file_path: Path):
        """
        Loads the ecosystem state from a file and restores it to the engine.
        Note: This method currently returns the state data. A full implementation
              would require the ecosystem_engine to have a method to restore state.

        Args:
            ecosystem_engine: The instance of the CognitiveEcosystemEngine to restore state to.
            file_path (Path): The path to the state file to load.

        Returns:
            dict: The loaded state data.
        """
        if not file_path.exists():
            logging.error(f"State file not found: '{file_path}'")
            raise FileNotFoundError(f"State file not found: {file_path}")
            
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                state_data = json.load(f)
            logging.info(f"Ecosystem state successfully loaded from '{file_path}'")
            
            # Here you would typically restore the state to the engine, e.g.:
            # ecosystem_engine.restore_state(state_data)
            # For now, we just return the data.
            
            return state_data
        except (IOError, json.JSONDecodeError) as e:
            logging.error(f"Failed to load ecosystem state from '{file_path}': {e}")
            raise

    def create_snapshot(self, ecosystem_engine, snapshot_name: str) -> Path:
        """
        Creates a named snapshot of the current ecosystem state.

        Args:
            ecosystem_engine: The instance of the CognitiveEcosystemEngine.
            snapshot_name (str): A descriptive name for the snapshot.

        Returns:
            Path: The path to the created snapshot file.
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_name = f"snapshot_{snapshot_name}_{timestamp}.json"
        return self.save_state(ecosystem_engine, file_name)

    def _capture_ecosystem_state(self, ecosystem_engine) -> Dict[str, Any]:
        """
        Captures the serializable state of the ecosystem engine.

        Args:
            ecosystem_engine: The instance of the CognitiveEcosystemEngine.

        Returns:
            dict: A dictionary representing the ecosystem's state.
        """
        # A more robust implementation would involve serializing agent instances
        # and other complex objects properly.
        state = {
            "config": ecosystem_engine.config,
            "interaction_history": ecosystem_engine.interaction_history,
            "cognitive_state": ecosystem_engine.cognitive_state,
            "niche_map": {agent_id: niche.to_dict() for agent_id, niche in ecosystem_engine.niche_map.items()},
            "timestamp": datetime.now().isoformat()
        }
        return state
