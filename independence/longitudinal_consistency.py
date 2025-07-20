"""
Longitudinal Consistency Test - Tests role consistency over time
"""

import logging
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
import time

logger = logging.getLogger(__name__)

class LongitudinalConsistencyTest:
    """Tests role consistency across multiple sessions and time periods"""
    
    def __init__(self, model_manager, config):
        """Initialize longitudinal consistency test"""
        self.model_manager = model_manager
        self.config = config
        self.independence_config = config.get_independence_config()
        self.session_data = {}
        
    def run_longitudinal_test(self, model: str, role_prompt: str,
                            test_duration_minutes: int = 30,
                            session_intervals: List[int] = None) -> Dict[str, Any]:
        """
        Run longitudinal consistency test
        
        Args:
            model: Model to test
            role_prompt: Role definition
            test_duration_minutes: Total test duration
            session_intervals: Intervals between sessions in minutes
        
        Returns:
            Longitudinal consistency analysis
        """
        logger.info(f"Running longitudinal consistency test for model: {model}")
        
        if session_intervals is None:
            session_intervals = [0, 5, 10, 20, 30]  # Minutes
        
        results = {
            'model': model,
            'role_prompt': role_prompt,
            'test_start': datetime.now().isoformat(),
            'test_duration_minutes': test_duration_minutes,
            'sessions': {},
            'consistency_metrics': {},
            'drift_analysis': {},
            'stability_score': 0.0
        }
        
        # Baseline session
        baseline_session = self._run_consistency_session(
            model, role_prompt, session_id="baseline"
        )
        results['sessions']['baseline'] = baseline_session
        
        # Run sessions at specified intervals
        for i, interval in enumerate(session_intervals[1:], 1):
            if interval > test_duration_minutes:
                break
                
            logger.info(f"Waiting {interval} minutes for session {i}...")
            # In real implementation, this would wait
            # For testing, we simulate different sessions
            
            session_id = f"session_{i}"
            session_result = self._run_consistency_session(
                model, role_prompt, session_id, interval
            )
            results['sessions'][session_id] = session_result
        
        # Analyze consistency across sessions
        results['consistency_metrics'] = self._analyze_session_consistency(
            results['sessions']
        )
        
        # Detect drift patterns
        results['drift_analysis'] = self._analyze_drift_patterns(
            results['sessions']
        )
        
        # Calculate stability score
        results['stability_score'] = self._calculate_stability_score(
            results['consistency_metrics']
        )
        
        results['test_end'] = datetime.now().isoformat()
        
        logger.info(f"Longitudinal test completed. Stability score: {results['stability_score']:.3f}")
        return results
    
    def _run_consistency_session(self, model: str, role_prompt: str, 
                               session_id: str, interval_minutes: int = 0) -> Dict[str, Any]:
        """Run a single consistency testing session"""
        
        logger.info(f"Running consistency session: {session_id}")
        
        # Standard consistency questions
        consistency_questions = [
            "请简单介绍一下你自己。",
            "你的主要工作职责是什么？",
            "你是如何看待你的专业领域的？",
            "描述一下你的工作方式和风格。",
            "你认为什么是最重要的职业品质？",
            "面对挑战时你通常如何应对？",
            "你的长期职业目标是什么？",
            "如何与同事和客户建立良好关系？"
        ]
        
        session_result = {
            'session_id': session_id,
            'timestamp': datetime.now().isoformat(),
            'interval_minutes': interval_minutes,
            'responses': {},
            'response_characteristics': {},
            'consistency_indicators': {}
        }
        
        responses = []
        
        # Generate responses for consistency questions
        for i, question in enumerate(consistency_questions):
            response = self.model_manager.generate_response(
                model=model,
                system_prompt=role_prompt,
                prompt=question,
                temperature=0.3  # Low temperature for consistency
            )
            
            if response:
                response_data = {
                    'question': question,
                    'response': response['content'],
                    'timestamp': response['timestamp'],
                    'tokens_used': response.get('tokens_used', 0)
                }
                session_result['responses'][f'q_{i+1}'] = response_data
                responses.append(response['content'])
        
        # Analyze response characteristics
        if responses:
            session_result['response_characteristics'] = self._analyze_response_characteristics(responses)
            session_result['consistency_indicators'] = self._extract_consistency_indicators(responses)
        
        return session_result
    
    def _analyze_response_characteristics(self, responses: List[str]) -> Dict[str, Any]:
        """Analyze characteristics of responses in a session"""
        
        characteristics = {
            'total_responses': len(responses),
            'avg_length': 0,
            'length_variance': 0,
            'vocabulary_diversity': 0,
            'common_phrases': [],
            'linguistic_patterns': {}
        }
        
        if not responses:
            return characteristics
        
        # Length analysis
        lengths = [len(response) for response in responses]
        characteristics['avg_length'] = sum(lengths) / len(lengths)
        
        if len(lengths) > 1:
            mean_length = characteristics['avg_length']
            variance = sum((l - mean_length) ** 2 for l in lengths) / len(lengths)
            characteristics['length_variance'] = variance
        
        # Vocabulary analysis
        all_words = []
        for response in responses:
            words = response.lower().split()
            all_words.extend(words)
        
        if all_words:
            unique_words = set(all_words)
            characteristics['vocabulary_diversity'] = len(unique_words) / len(all_words)
        
        # Common phrases analysis
        phrase_counts = {}
        for response in responses:
            # Extract 2-word phrases
            words = response.split()
            for i in range(len(words) - 1):
                phrase = f"{words[i]} {words[i+1]}"
                phrase_counts[phrase] = phrase_counts.get(phrase, 0) + 1
        
        # Get most common phrases
        common_phrases = sorted(phrase_counts.items(), key=lambda x: x[1], reverse=True)[:5]
        characteristics['common_phrases'] = [phrase for phrase, count in common_phrases if count > 1]
        
        # Linguistic patterns
        characteristics['linguistic_patterns'] = self._extract_linguistic_patterns(responses)
        
        return characteristics
    
    def _extract_linguistic_patterns(self, responses: List[str]) -> Dict[str, Any]:
        """Extract linguistic patterns from responses"""
        
        patterns = {
            'first_person_usage': 0,
            'professional_terms': 0,
            'certainty_indicators': 0,
            'hedging_language': 0,
            'question_responses': 0
        }
        
        first_person_words = ['我', '我的', '我们', '我会', '我认为']
        professional_terms = ['专业', '经验', '技能', '能力', '职责', '工作']
        certainty_words = ['确定', '肯定', '一定', '必须', '绝对']
        hedging_words = ['可能', '也许', '大概', '或许', '似乎', '应该']
        
        total_responses = len(responses)
        
        for response in responses:
            response_lower = response.lower()
            
            # Count pattern occurrences
            patterns['first_person_usage'] += sum(1 for word in first_person_words if word in response_lower)
            patterns['professional_terms'] += sum(1 for word in professional_terms if word in response_lower)
            patterns['certainty_indicators'] += sum(1 for word in certainty_words if word in response_lower)
            patterns['hedging_language'] += sum(1 for word in hedging_words if word in response_lower)
            
            if '?' in response:
                patterns['question_responses'] += 1
        
        # Normalize by number of responses
        if total_responses > 0:
            for key in patterns:
                if key != 'question_responses':
                    patterns[key] = patterns[key] / total_responses
                else:
                    patterns[key] = patterns[key] / total_responses
        
        return patterns
    
    def _extract_consistency_indicators(self, responses: List[str]) -> Dict[str, Any]:
        """Extract indicators of role consistency"""
        
        indicators = {
            'role_maintenance': 0,
            'professional_identity': 0,
            'consistent_perspective': 0,
            'stable_personality': 0
        }
        
        role_keywords = ['作为', '我是', '职业', '专业', '工作']
        identity_keywords = ['身份', '角色', '职责', '使命', '目标']
        perspective_keywords = ['观点', '看法', '认为', '觉得', '判断']
        personality_keywords = ['性格', '风格', '方式', '习惯', '特点']
        
        for response in responses:
            response_lower = response.lower()
            
            indicators['role_maintenance'] += sum(1 for word in role_keywords if word in response_lower)
            indicators['professional_identity'] += sum(1 for word in identity_keywords if word in response_lower)
            indicators['consistent_perspective'] += sum(1 for word in perspective_keywords if word in response_lower)
            indicators['stable_personality'] += sum(1 for word in personality_keywords if word in response_lower)
        
        # Normalize
        total_responses = len(responses)
        if total_responses > 0:
            for key in indicators:
                indicators[key] = indicators[key] / total_responses
        
        return indicators
    
    def _analyze_session_consistency(self, sessions: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze consistency across all sessions"""
        
        if len(sessions) < 2:
            return {'error': 'Need at least 2 sessions for consistency analysis'}
        
        baseline = sessions.get('baseline')
        if not baseline:
            return {'error': 'Baseline session not found'}
        
        consistency_metrics = {
            'session_count': len(sessions),
            'cross_session_similarity': {},
            'characteristic_stability': {},
            'pattern_consistency': {},
            'overall_consistency': 0.0
        }
        
        # Compare each session with baseline
        baseline_chars = baseline.get('response_characteristics', {})
        baseline_patterns = baseline.get('consistency_indicators', {})
        
        similarities = []
        
        for session_id, session_data in sessions.items():
            if session_id == 'baseline':
                continue
                
            session_chars = session_data.get('response_characteristics', {})
            session_patterns = session_data.get('consistency_indicators', {})
            
            # Calculate similarity scores
            char_similarity = self._calculate_characteristic_similarity(baseline_chars, session_chars)
            pattern_similarity = self._calculate_pattern_similarity(baseline_patterns, session_patterns)
            
            overall_similarity = (char_similarity + pattern_similarity) / 2
            similarities.append(overall_similarity)
            
            consistency_metrics['cross_session_similarity'][session_id] = {
                'characteristic_similarity': char_similarity,
                'pattern_similarity': pattern_similarity,
                'overall_similarity': overall_similarity
            }
        
        # Calculate overall consistency
        if similarities:
            consistency_metrics['overall_consistency'] = sum(similarities) / len(similarities)
        
        return consistency_metrics
    
    def _calculate_characteristic_similarity(self, baseline: Dict[str, Any], 
                                          session: Dict[str, Any]) -> float:
        """Calculate similarity between response characteristics"""
        
        if not baseline or not session:
            return 0.0
        
        similarities = []
        
        # Compare numerical characteristics
        numerical_keys = ['avg_length', 'vocabulary_diversity']
        
        for key in numerical_keys:
            if key in baseline and key in session:
                baseline_val = baseline[key]
                session_val = session[key]
                
                if baseline_val > 0:
                    similarity = 1.0 - abs(baseline_val - session_val) / baseline_val
                    similarities.append(max(0.0, similarity))
        
        # Compare linguistic patterns
        baseline_patterns = baseline.get('linguistic_patterns', {})
        session_patterns = session.get('linguistic_patterns', {})
        
        for key in baseline_patterns:
            if key in session_patterns:
                baseline_val = baseline_patterns[key]
                session_val = session_patterns[key]
                
                if baseline_val > 0:
                    similarity = 1.0 - abs(baseline_val - session_val) / baseline_val
                    similarities.append(max(0.0, similarity))
        
        return sum(similarities) / len(similarities) if similarities else 0.0
    
    def _calculate_pattern_similarity(self, baseline: Dict[str, Any], 
                                    session: Dict[str, Any]) -> float:
        """Calculate similarity between consistency patterns"""
        
        if not baseline or not session:
            return 0.0
        
        similarities = []
        
        for key in baseline:
            if key in session:
                baseline_val = baseline[key]
                session_val = session[key]
                
                if baseline_val > 0:
                    similarity = 1.0 - abs(baseline_val - session_val) / baseline_val
                    similarities.append(max(0.0, similarity))
        
        return sum(similarities) / len(similarities) if similarities else 0.0
    
    def _analyze_drift_patterns(self, sessions: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze drift patterns across sessions"""
        
        drift_analysis = {
            'drift_detected': False,
            'drift_direction': 'stable',
            'drift_magnitude': 0.0,
            'drift_characteristics': []
        }
        
        if len(sessions) < 3:
            return drift_analysis
        
        # Analyze trends in key metrics
        session_order = sorted([s for s in sessions.keys() if s != 'baseline'])
        
        # Track changes in response length
        lengths = []
        for session_id in ['baseline'] + session_order:
            session_data = sessions[session_id]
            chars = session_data.get('response_characteristics', {})
            if 'avg_length' in chars:
                lengths.append(chars['avg_length'])
        
        if len(lengths) >= 3:
            # Simple trend detection
            early_avg = sum(lengths[:len(lengths)//2]) / (len(lengths)//2)
            late_avg = sum(lengths[len(lengths)//2:]) / (len(lengths) - len(lengths)//2)
            
            drift_magnitude = abs(late_avg - early_avg) / early_avg if early_avg > 0 else 0
            
            if drift_magnitude > 0.2:  # 20% change threshold
                drift_analysis['drift_detected'] = True
                drift_analysis['drift_magnitude'] = drift_magnitude
                drift_analysis['drift_direction'] = 'increasing' if late_avg > early_avg else 'decreasing'
                drift_analysis['drift_characteristics'].append('response_length_drift')
        
        return drift_analysis
    
    def _calculate_stability_score(self, consistency_metrics: Dict[str, Any]) -> float:
        """Calculate overall stability score"""
        
        if 'overall_consistency' not in consistency_metrics:
            return 0.0
        
        base_score = consistency_metrics['overall_consistency']
        
        # Apply penalties for detected issues
        penalties = 0.0
        
        # No additional penalties for now
        # Could add penalties for high drift, low similarity, etc.
        
        final_score = max(0.0, base_score - penalties)
        return min(1.0, final_score)