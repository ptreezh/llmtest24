"""
Model Manager for LLM Test Framework - Enhanced for Real LLM Testing
Handles real model loading, configuration, and inference
"""

import logging
from typing import Dict, Any, Optional, List
import requests
import json
import time
from .config_manager import ConfigManager

logger = logging.getLogger(__name__)

class ModelManager:
    """Manages LLM models for real testing"""
    
    def __init__(self, config: ConfigManager):
        """Initialize model manager with configuration"""
        self.config = config
        self.models = {}
        self.current_model = None
        self.cloud_services = self._load_cloud_services()
        
    def _load_cloud_services(self):
        """Load cloud services module"""
        try:
            sys.path.append(str(Path(__file__).parent.parent / "scripts" / "utils"))
            import cloud_services
            return cloud_services
        except Exception as e:
            logger.error(f"Failed to load cloud services: {e}")
            return None
    
    def load_model(self, model_name: str, **kwargs) -> bool:
        """Load a specific model"""
        try:
            # Get model configuration
            model_config = self.config.get_model_config(model_name)
            if not model_config:
                logger.error(f"Model configuration not found: {model_name}")
                return False
            
            # For real models, check if we can access them
            if self.cloud_services:
                try:
                    # Try to call the model with a simple test
                    test_response = self._test_model_call(model_name)
                    if test_response:
                        self.models[model_name] = {
                            'name': model_name,
                            'config': model_config,
                            'loaded': True,
                            'status': 'ready',
                            'test_response': test_response
                        }
                        self.current_model = model_name
                        logger.info(f"Model loaded successfully: {model_name}")
                        return True
                    else:
                        logger.error(f"Model test call failed: {model_name}")
                        return False
                except Exception as e:
                    logger.error(f"Error testing model {model_name}: {e}")
                    return False
            else:
                # Fallback to simulation
                self.models[model_name] = {
                    'name': model_name,
                    'config': model_config,
                    'loaded': True,
                    'status': 'ready',
                    'test_response': 'Simulation mode - cloud services not available'
                }
                self.current_model = model_name
                logger.info(f"Model loaded in simulation mode: {model_name}")
                return True
            
        except Exception as e:
            logger.error(f"Failed to load model {model_name}: {e}")
            return False
    
    def _test_model_call(self, model_name: str) -> Optional[str]:
        """Test if we can call the model"""
        try:
            # Extract service and model name
            if '/' in model_name:
                service_name, actual_model = model_name.split('/', 1)
            else:
                service_name = 'ollama'  # Default to ollama
                actual_model = model_name
            
            # Test with a simple prompt
            test_prompt = "Hello, please respond with 'Test successful'"
            
            if service_name == 'ollama':
                # Test ollama
                try:
                    import ollama
                    response = ollama.chat(
                        model=actual_model,
                        messages=[{"role": "user", "content": test_prompt}]
                    )
                    return response['message']['content']
                except:
                    return None
            else:
                # Test cloud service
                try:
                    response = self.cloud_services.call_cloud_service(
                        service_name, actual_model, test_prompt
                    )
                    return response
                except:
                    return None
                    
        except Exception as e:
            logger.error(f"Model test call failed: {e}")
            return None
    
    def generate_response(self, prompt: str, model_name: Optional[str] = None, **kwargs) -> Optional[str]:
        """Generate response from real model"""
        target_model = model_name or self.current_model
        
        if not target_model or target_model not in self.models:
            logger.error(f"Model not available: {target_model}")
            return None
        
        try:
            # Extract service and model name
            if '/' in target_model:
                service_name, actual_model = target_model.split('/', 1)
            else:
                service_name = 'ollama'
                actual_model = target_model
            
            # Generate response
            if service_name == 'ollama':
                try:
                    import ollama
                    messages = [{"role": "user", "content": prompt}]
                    response = ollama.chat(
                        model=actual_model,
                        messages=messages
                    )
                    return response['message']['content']
                except Exception as e:
                    logger.error(f"Ollama call failed: {e}")
                    return None
            else:
                try:
                    response = self.cloud_services.call_cloud_service(
                        service_name, actual_model, prompt
                    )
                    return response
                except Exception as e:
                    logger.error(f"Cloud service call failed: {e}")
                    return None
                    
        except Exception as e:
            logger.error(f"Response generation failed: {e}")
            return None
    
    def get_available_models(self) -> List[str]:
        """Get list of available models from cloud services"""
        if self.cloud_services:
            try:
                models_info = self.cloud_services.get_all_models()
                return [model['key'] for model in models_info]
            except:
                pass
        
        # Fallback models
        return [
            'together/mistralai/Mixtral-8x7B-Instruct-v0.1',
            'openrouter/openai/gpt-3.5-turbo',
            'ollama/llama2'
        ]
    
    def is_model_ready(self, model_name: str) -> bool:
        """Check if model is ready for inference"""
        model = self.models.get(model_name)
        return model and model.get('loaded', False)
    
    def get_model_info(self, model_name: str) -> Optional[Dict[str, Any]]:
        """Get model information"""
        return self.models.get(model_name)
