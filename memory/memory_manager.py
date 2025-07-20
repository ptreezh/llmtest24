"""
Memory Manager for role consistency tracking
"""

import logging
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
import json

logger = logging.getLogger(__name__)

class MemoryManager:
    """Manages memory and context for role consistency testing"""
    
    def __init__(self, config):
        """Initialize memory manager"""
        self.config = config
        self.independence_config = config.get_independence_config()
        self.memory_store = {}
        self.context_history = {}
        
    def store_interaction(self, session_id: str, role_id: str, 
                         interaction_data: Dict[str, Any]):
        """Store interaction data for future reference"""
        
        if session_id not in self.memory_store:
            self.memory_store[session_id] = {}
        
        if role_id not in self.memory_store[session_id]:
            self.memory_store[session_id][role_id] = []
        
        interaction_entry = {
            'timestamp': datetime.now().isoformat(),
            'data': interaction_data
        }
        
        self.memory_store[session_id][role_id].append(interaction_entry)
        
    def retrieve_role_history(self, session_id: str, role_id: str) -> List[Dict[str, Any]]:
        """Retrieve interaction history for a specific role"""
        
        if session_id in self.memory_store and role_id in self.memory_store[session_id]:
            return self.memory_store[session_id][role_id]
        
        return []
    
    def analyze_memory_consistency(self, session_id: str, role_id: str) -> Dict[str, Any]:
        """Analyze consistency in stored memories"""
        
        history = self.retrieve_role_history(session_id, role_id)
        
        if not history:
            return {'error': 'No history found'}
        
        return {
            'total_interactions': len(history),
            'time_span': self._calculate_time_span(history),
            'consistency_score': self._calculate_memory_consistency(history)
        }
    
    def _calculate_time_span(self, history: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Calculate time span of interactions"""
        
        if len(history) < 2:
            return {'span_minutes': 0}
        
        timestamps = [datetime.fromisoformat(entry['timestamp']) for entry in history]
        earliest = min(timestamps)
        latest = max(timestamps)
        
        span = latest - earliest
        
        return {
            'earliest': earliest.isoformat(),
            'latest': latest.isoformat(),
            'span_minutes': span.total_seconds() / 60
        }
    
    def _calculate_memory_consistency(self, history: List[Dict[str, Any]]) -> float:
        """Calculate consistency score from memory history"""
        
        # Simple consistency calculation based on response patterns
        # In full implementation, this would use semantic similarity
        
        if len(history) < 2:
            return 1.0
        
        consistency_scores = []
        
        for i in range(1, len(history)):
            current = history[i]['data']
            previous = history[i-1]['data']
            
            # Compare response characteristics
            score = self._compare_interactions(previous, current)
            consistency_scores.append(score)
        
        return sum(consistency_scores) / len(consistency_scores) if consistency_scores else 0.0
    
    def _compare_interactions(self, interaction1: Dict[str, Any], 
                            interaction2: Dict[str, Any]) -> float:
        """Compare two interactions for consistency"""
        
        # Placeholder comparison logic
        # Real implementation would use semantic similarity
        
        return 0.8  # Default consistency score
