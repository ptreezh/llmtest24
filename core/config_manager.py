"""
Configuration Manager for Unified LLM Test Framework
"""

import os
import yaml
import json
from typing import Dict, List, Any, Optional
from pathlib import Path

class ConfigManager:
    """Manages configuration for the unified testing framework"""
    
    def __init__(self, config_path: Optional[str] = None):
        """Initialize configuration manager"""
        self.config_path = config_path or "config.py"
        self.config = self._load_config()
        
    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from file"""
        # Default configuration
        default_config = {
            'ollama': {
                'host': 'http://localhost:11434',
                'timeout': 180  # 增加到3分钟
            },
            'models': {
                'default': 'gemini/gemini-2.0-flash-exp',
                'available': ['gemini/gemini-2.0-flash-exp', 'together/mistral:instruct', 'glm/glm-4-plus']
            },
            'testing': {
                'output_dir': 'testout',
                'log_level': 'INFO',
                'max_retries': 5,  # 增加重试次数
                'timeout': 240     # 增加到4分钟
            },
            'independence': {
                'embedding_model': 'sentence-transformers/all-MiniLM-L6-v2',
                'similarity_threshold': 0.7,
                'memory_retention_days': 30,
                'breaking_threshold': 0.7,
                'max_stress_rounds': 10
            }
        }
        
        # Try to load from existing config.py
        if os.path.exists(self.config_path):
            try:
                # Import existing config
                import importlib.util
                spec = importlib.util.spec_from_file_location("config", self.config_path)
                config_module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(config_module)
                
                # Merge with default config
                if hasattr(config_module, 'MODEL_TO_TEST'):
                    default_config['models']['default'] = config_module.MODEL_TO_TEST
                if hasattr(config_module, 'OLLAMA_HOST'):
                    default_config['ollama']['host'] = config_module.OLLAMA_HOST
                    
            except Exception as e:
                print(f"Warning: Could not load config from {self.config_path}: {e}")
        
        return default_config
    
    def get_available_models(self) -> List[str]:
        """Get list of available models"""
        return self.config['models']['available']
    
    def get_default_model(self) -> str:
        """Get default model"""
        return self.config['models']['default']
    
    def get_ollama_config(self) -> Dict[str, Any]:
        """Get Ollama configuration"""
        return self.config['ollama']
    
    def get_testing_config(self) -> Dict[str, Any]:
        """Get testing configuration"""
        return self.config['testing']
    
    def get_independence_config(self) -> Dict[str, Any]:
        """Get independence testing configuration"""
        return self.config['independence']
    
    def get_model_config(self, model_name: str) -> Optional[Dict[str, Any]]:
        """Get configuration for a specific model"""
        # For now, return basic model config
        available_models = self.get_available_models()
        if model_name in available_models:
            return {
                'name': model_name,
                'api_key': 'dummy_key_for_testing',
                'base_url': 'http://localhost:8000/v1',
                'max_tokens': 2048,
                'temperature': 0.7,
                'timeout': 30
            }
        return None
    
    def update_config(self, key: str, value: Any):
        """Update configuration value"""
        keys = key.split('.')
        config_ref = self.config
        
        for k in keys[:-1]:
            if k not in config_ref:
                config_ref[k] = {}
            config_ref = config_ref[k]
        
        config_ref[keys[-1]] = value
