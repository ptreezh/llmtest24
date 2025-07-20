"""
Model Manager for handling different LLM providers
"""

import requests
import json
import logging
from typing import Dict, List, Any, Optional
from datetime import datetime

logger = logging.getLogger(__name__)

class ModelManager:
    """Manages LLM model interactions across different providers"""
    
    def __init__(self, config):
        """Initialize model manager with configuration"""
        self.config = config
        self.ollama_config = config.get_ollama_config()
        self.session_stats = {}
        
    def test_model_availability(self, model: str) -> bool:
        """Test if a model is available and responsive"""
        try:
            response = self.generate_response(
                model=model,
                prompt="Hello, please respond with 'OK' to confirm you're working.",
                max_tokens=10
            )
            return response is not None and 'OK' in response.get('content', '')
        except Exception as e:
            logger.error(f"Model {model} availability test failed: {e}")
            return False
    
    def generate_response(self, model: str, prompt: str, 
                         system_prompt: Optional[str] = None,
                         max_tokens: int = 1000,
                         temperature: float = 0.7) -> Optional[Dict[str, Any]]:
        """Generate response from specified model"""
        
        # Record request
        if model not in self.session_stats:
            self.session_stats[model] = {
                'requests': 0,
                'successful': 0,
                'failed': 0,
                'total_tokens': 0
            }
        
        self.session_stats[model]['requests'] += 1
        
        try:
            # Prepare request for Ollama
            messages = []
            if system_prompt:
                messages.append({"role": "system", "content": system_prompt})
            messages.append({"role": "user", "content": prompt})
            
            payload = {
                "model": model,
                "messages": messages,
                "options": {
                    "temperature": temperature,
                    "num_predict": max_tokens
                },
                "stream": False
            }
            
            response = requests.post(
                f"{self.ollama_config['host']}/api/chat",
                json=payload,
                timeout=self.ollama_config.get('timeout', 180)  # 增加到3分钟
            )
            
            if response.status_code == 200:
                result = response.json()
                
                # Extract response content
                content = result.get('message', {}).get('content', '')
                
                # Update stats
                self.session_stats[model]['successful'] += 1
                self.session_stats[model]['total_tokens'] += len(content.split())
                
                return {
                    'content': content,
                    'model': model,
                    'timestamp': datetime.now().isoformat(),
                    'tokens_used': len(content.split()),
                    'temperature': temperature
                }
            else:
                logger.error(f"Model {model} returned status {response.status_code}")
                self.session_stats[model]['failed'] += 1
                return None
                
        except Exception as e:
            logger.error(f"Error generating response from {model}: {e}")
            self.session_stats[model]['failed'] += 1
            return None
    
    def get_model_stats(self, model: str) -> Dict[str, Any]:
        """Get statistics for a specific model"""
        return self.session_stats.get(model, {})
    
    def get_all_stats(self) -> Dict[str, Any]:
        """Get statistics for all models"""
        return self.session_stats.copy()
    
    def reset_stats(self):
        """Reset all model statistics"""
        self.session_stats.clear()


