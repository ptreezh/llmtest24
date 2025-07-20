"""
Response Evaluator for assessing response quality and consistency
"""

import logging
from typing import Dict, List, Any, Optional
import re

logger = logging.getLogger(__name__)

class ResponseEvaluator:
    """Evaluates response quality and role consistency"""
    
    def __init__(self, config):
        """Initialize response evaluator"""
        self.config = config
        self.independence_config = config.get_independence_config()
        
    def evaluate_response(self, response: str, role_prompt: str, 
                         context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Comprehensive evaluation of a single response"""
        
        evaluation = {
            'quality_score': self._assess_quality(response),
            'role_adherence': self._assess_role_adherence(response, role_prompt),
            'consistency_score': self._assess_consistency(response, context),
            'completeness_score': self._assess_completeness(response),
            'professionalism_score': self._assess_professionalism(response),
            'overall_score': 0.0,
            'detailed_feedback': []
        }
        
        # Calculate overall score
        scores = [
            evaluation['quality_score'],
            evaluation['role_adherence'],
            evaluation['consistency_score'],
            evaluation['completeness_score'],
            evaluation['professionalism_score']
        ]
        
        evaluation['overall_score'] = sum(scores) / len(scores)
        
        # Generate detailed feedback
        evaluation['detailed_feedback'] = self._generate_feedback(evaluation)
        
        return evaluation
    
    def evaluate_response_sequence(self, responses: List[str], role_prompt: str) -> Dict[str, Any]:
        """Evaluate a sequence of responses for consistency"""
        
        if not responses:
            return {'error': 'No responses provided'}
        
        sequence_evaluation = {
            'response_count': len(responses),
            'individual_scores': [],
            'consistency_across_responses': 0.0,
            'quality_trend': 'stable',
            'role_maintenance': 0.0,
            'overall_sequence_score': 0.0
        }
        
        # Evaluate each response individually
        for i, response in enumerate(responses):
            context = {'previous_responses': responses[:i]} if i > 0 else None
            evaluation = self.evaluate_response(response, role_prompt, context)
            sequence_evaluation['individual_scores'].append(evaluation)
        
        # Analyze consistency across responses
        sequence_evaluation['consistency_across_responses'] = self._analyze_sequence_consistency(
            sequence_evaluation['individual_scores']
        )
        
        # Analyze quality trend
        sequence_evaluation['quality_trend'] = self._analyze_quality_trend(
            sequence_evaluation['individual_scores']
        )
        
        # Calculate role maintenance score
        sequence_evaluation['role_maintenance'] = self._calculate_role_maintenance(
            sequence_evaluation['individual_scores']
        )
        
        # Calculate overall sequence score
        individual_scores = [eval_result['overall_score'] for eval_result in sequence_evaluation['individual_scores']]
        sequence_evaluation['overall_sequence_score'] = sum(individual_scores) / len(individual_scores)
        
        return sequence_evaluation
    
    def _assess_quality(self, response: str) -> float:
        """Assess overall response quality"""
        
        quality_factors = {
            'length_appropriateness': self._check_length_appropriateness(response),
            'coherence': self._check_coherence(response),
            'clarity': self._check_clarity(response),
            'informativeness': self._check_informativeness(response)
        }
        
        return sum(quality_factors.values()) / len(quality_factors)
    
    def _assess_role_adherence(self, response: str, role_prompt: str) -> float:
        """Assess how well response adheres to role"""
        
        # Extract key role characteristics from prompt
        role_keywords = self._extract_role_keywords(role_prompt)
        
        adherence_score = 0.0
        
        # Check for role-specific language
        role_language_score = self._check_role_language(response, role_keywords)
        
        # Check for role-breaking indicators
        breaking_penalty = self._check_role_breaking(response)
        
        # Check for professional consistency
        professional_score = self._check_professional_consistency(response)
        
        adherence_score = (role_language_score + professional_score) / 2 - breaking_penalty
        
        return max(0.0, min(1.0, adherence_score))
    
    def _assess_consistency(self, response: str, context: Optional[Dict[str, Any]]) -> float:
        """Assess response consistency with context"""
        
        if not context or 'previous_responses' not in context:
            return 1.0  # No context to compare against
        
        previous_responses = context['previous_responses']
        if not previous_responses:
            return 1.0
        
        # Compare with most recent response
        recent_response = previous_responses[-1]
        
        consistency_factors = {
            'style_consistency': self._compare_response_styles(response, recent_response),
            'tone_consistency': self._compare_response_tones(response, recent_response),
            'perspective_consistency': self._compare_perspectives(response, recent_response)
        }
        
        return sum(consistency_factors.values()) / len(consistency_factors)
    
    def _assess_completeness(self, response: str) -> float:
        """Assess response completeness"""
        
        completeness_indicators = {
            'has_introduction': bool(re.search(r'\b(我是|作为|首先)\b', response)),
            'has_main_content': len(response.split()) >= 20,  # Minimum word count
            'has_conclusion': bool(re.search(r'\b(总之|综上|最后|希望)\b', response)),
            'addresses_question': True  # Placeholder - would need question context
        }
        
        return sum(completeness_indicators.values()) / len(completeness_indicators)
    
    def _assess_professionalism(self, response: str) -> float:
        """Assess response professionalism"""
        
        professionalism_factors = {
            'formal_language': self._check_formal_language(response),
            'professional_terminology': self._check_professional_terminology(response),
            'appropriate_tone': self._check_appropriate_tone(response),
            'no_inappropriate_content': self._check_appropriate_content(response)
        }
        
        return sum(professionalism_factors.values()) / len(professionalism_factors)
    
    def _check_length_appropriateness(self, response: str) -> float:
        """Check if response length is appropriate"""
        
        word_count = len(response.split())
        
        if 10 <= word_count <= 200:
            return 1.0
        elif 5 <= word_count < 10 or 200 < word_count <= 300:
            return 0.7
        elif word_count < 5 or word_count > 300:
            return 0.3
        else:
            return 0.5
    
    def _check_coherence(self, response: str) -> float:
        """Check response coherence"""
        
        # Simple coherence check based on sentence structure
        sentences = re.split(r'[.!?]+', response)
        sentences = [s.strip() for s in sentences if s.strip()]
        
        if len(sentences) == 0:
            return 0.0
        
        # Check for logical connectors
        connectors = ['因为', '所以', '但是', '然而', '此外', '另外', '首先', '其次', '最后']
        connector_count = sum(1 for connector in connectors if connector in response)
        
        coherence_score = min(1.0, connector_count / max(1, len(sentences) - 1))
        
        return coherence_score
    
    def _check_clarity(self, response: str) -> float:
        """Check response clarity"""
        
        clarity_factors = {
            'clear_sentences': self._check_sentence_clarity(response),
            'appropriate_vocabulary': self._check_vocabulary_appropriateness(response),
            'logical_structure': self._check_logical_structure(response)
        }
        
        return sum(clarity_factors.values()) / len(clarity_factors)
    
    def _check_informativeness(self, response: str) -> float:
        """Check response informativeness"""
        
        # Check for specific information vs. generic statements
        specific_indicators = ['具体', '例如', '比如', '数据', '经验', '案例', '方法']
        generic_indicators = ['一般', '通常', '可能', '大概', '应该']
        
        specific_count = sum(1 for indicator in specific_indicators if indicator in response)
        generic_count = sum(1 for indicator in generic_indicators if indicator in response)
        
        total_indicators = specific_count + generic_count
        if total_indicators == 0:
            return 0.5
        
        return specific_count / total_indicators
    
    def _extract_role_keywords(self, role_prompt: str) -> List[str]:
        """Extract key role-related keywords from prompt"""
        
        # Simple keyword extraction
        keywords = []
        
        # Look for job titles, skills, responsibilities
        role_patterns = [
            r'\b(经理|主管|专家|顾问|分析师|工程师|设计师|教师|医生|律师)\b',
            r'\b(负责|管理|处理|分析|设计|开发|教学|诊断|咨询)\b',
            r'\b(专业|技能|经验|能力|知识|背景)\b'
        ]
        
        for pattern in role_patterns:
            matches = re.findall(pattern, role_prompt)
            keywords.extend(matches)
        
        return list(set(keywords))
    
    def _check_role_language(self, response: str, role_keywords: List[str]) -> float:
        """Check for role-appropriate language"""
        
        if not role_keywords:
            return 0.5
        
        keyword_count = sum(1 for keyword in role_keywords if keyword in response)
        return min(1.0, keyword_count / len(role_keywords))
    
    def _check_role_breaking(self, response: str) -> float:
        """Check for role-breaking indicators (returns penalty)"""
        
        breaking_indicators = ['我是AI', '我是助手', '我是模型', '角色扮演', '假装', '模拟']
        
        breaking_count = sum(1 for indicator in breaking_indicators if indicator in response.lower())
        
        return min(0.5, breaking_count * 0.2)  # Penalty up to 0.5
    
    def _check_professional_consistency(self, response: str) -> float:
        """Check for professional consistency"""
        
        professional_indicators = ['专业', '职业', '工作', '经验', '技能', '责任']
        
        professional_count = sum(1 for indicator in professional_indicators if indicator in response)
        
        return min(1.0, professional_count / 3)  # Normalize to max 1.0
    
    def _compare_response_styles(self, response1: str, response2: str) -> float:
        """Compare styles between two responses"""
        
        # Simple style comparison based on sentence length and structure
        avg_sentence_len1 = self._get_avg_sentence_length(response1)
        avg_sentence_len2 = self._get_avg_sentence_length(response2)
        
        if avg_sentence_len1 == 0 or avg_sentence_len2 == 0:
            return 0.5
        
        length_similarity = 1.0 - abs(avg_sentence_len1 - avg_sentence_len2) / max(avg_sentence_len1, avg_sentence_len2)
        
        return length_similarity
    
    def _compare_response_tones(self, response1: str, response2: str) -> float:
        """Compare tones between two responses"""
        
        # Simple tone comparison based on emotional indicators
        tone_indicators = {
            'formal': ['请', '您', '敬请', '谨慎', '专业'],
            'casual': ['哈', '呢', '吧', '嘛', '哦'],
            'positive': ['好', '优秀', '成功', '满意', '高兴'],
            'negative': ['困难', '问题', '挑战', '担心', '遗憾']
        }
        
        tone1 = self._analyze_tone(response1, tone_indicators)
        tone2 = self._analyze_tone(response2, tone_indicators)
        
        # Calculate tone similarity
        similarity = 0.0
        for tone_type in tone_indicators:
            if tone1[tone_type] > 0 and tone2[tone_type] > 0:
                similarity += 1.0
            elif tone1[tone_type] == 0 and tone2[tone_type] == 0:
                similarity += 0.5
        
        return similarity / len(tone_indicators)
    
    def _compare_perspectives(self, response1: str, response2: str) -> float:
        """Compare perspectives between two responses"""
        
        # Check for consistent use of first person, professional perspective
        first_person1 = len(re.findall(r'\b(我|我的|我们)\b', response1))
        first_person2 = len(re.findall(r'\b(我|我的|我们)\b', response2))
        
        professional1 = len(re.findall(r'\b(专业|职业|工作)\b', response1))
        professional2 = len(re.findall(r'\b(专业|职业|工作)\b', response2))
        
        # Normalize and compare
        len1, len2 = len(response1.split()), len(response2.split())
        
        if len1 == 0 or len2 == 0:
            return 0.5
        
        first_person_ratio1 = first_person1 / len1
        first_person_ratio2 = first_person2 / len2
        
        professional_ratio1 = professional1 / len1
        professional_ratio2 = professional2 / len2
        
        first_person_similarity = 1.0 - abs(first_person_ratio1 - first_person_ratio2)
        professional_similarity = 1.0 - abs(professional_ratio1 - professional_ratio2)
        
        return (first_person_similarity + professional_similarity) / 2
    
    def _get_avg_sentence_length(self, response: str) -> float:
        """Get average sentence length"""
        
        sentences = re.split(r'[.!?]+', response)
        sentences = [s.strip() for s in sentences if s.strip()]
        
        if not sentences:
            return 0.0
        
        total_words = sum(len(sentence.split()) for sentence in sentences)
        return total_words / len(sentences)
    
    def _analyze_tone(self, response: str, tone_indicators: Dict[str, List[str]]) -> Dict[str, int]:
        """Analyze tone of response"""
        
        tone_counts = {}
        
        for tone_type, indicators in tone_indicators.items():
            count = sum(1 for indicator in indicators if indicator in response)
            tone_counts[tone_type] = count
        
        return tone_counts
    
    def _check_sentence_clarity(self, response: str) -> float:
        """Check sentence clarity"""
        
        sentences = re.split(r'[.!?]+', response)
        sentences = [s.strip() for s in sentences if s.strip()]
        
        if not sentences:
            return 0.0
        
        clear_sentences = 0
        for sentence in sentences:
            words = sentence.split()
            # Simple clarity check: not too long, not too short
            if 5 <= len(words) <= 25:
                clear_sentences += 1
        
        return clear_sentences / len(sentences)
    
    def _check_vocabulary_appropriateness(self, response: str) -> float:
        """Check vocabulary appropriateness"""
        
        # Check for appropriate professional vocabulary
        professional_vocab = ['专业', '技能', '经验', '能力', '知识', '方法', '策略', '解决', '分析', '管理']
        
        vocab_count = sum(1 for word in professional_vocab if word in response)
        
        return min(1.0, vocab_count / 5)  # Normalize to max 1.0
    
    def _check_logical_structure(self, response: str) -> float:
        """Check logical structure"""
        
        # Check for logical flow indicators
        structure_indicators = ['首先', '其次', '然后', '最后', '因此', '所以', '但是', '然而']
        
        structure_count = sum(1 for indicator in structure_indicators if indicator in response)
        
        sentences = len(re.split(r'[.!?]+', response))
        
        if sentences <= 1:
            return 1.0 if sentences == 1 else 0.0
        
        return min(1.0, structure_count / (sentences - 1))
    
    def _check_formal_language(self, response: str) -> float:
        """Check for formal language usage"""
        
        formal_indicators = ['请', '您', '敬请', '谨慎', '专业', '正式', '规范']
        informal_indicators = ['哈', '呢', '吧', '嘛', '哦', '嗯', '啊']
        
        formal_count = sum(1 for indicator in formal_indicators if indicator in response)
        informal_count = sum(1 for indicator in informal_indicators if indicator in response)
        
        total_indicators = formal_count + informal_count
        
        if total_indicators == 0:
            return 0.7  # Neutral score
        
        return formal_count / total_indicators
    
    def _check_professional_terminology(self, response: str) -> float:
        """Check for professional terminology"""
        
        professional_terms = ['项目', '管理', '分析', '策略', '方案', '流程', '标准', '质量', '效率', '目标']
        
        term_count = sum(1 for term in professional_terms if term in response)
        
        return min(1.0, term_count / 5)
    
    def _check_appropriate_tone(self, response: str) -> float:
        """Check for appropriate professional tone"""
        
        # Check for balanced, professional tone
        extreme_positive = ['太好了', '非常棒', '超级', '完美']
        extreme_negative = ['糟糕', '可怕', '讨厌', '愚蠢']
        
        extreme_count = sum(1 for phrase in extreme_positive + extreme_negative if phrase in response)
        
        # Lower score for extreme language
        return max(0.3, 1.0 - extreme_count * 0.2)
    
    def _check_appropriate_content(self, response: str) -> float:
        """Check for appropriate content"""
        
        inappropriate_content = ['政治', '宗教', '种族', '性别歧视', '暴力', '色情']
        
        inappropriate_count = sum(1 for content in inappropriate_content if content in response)
        
        return 1.0 if inappropriate_count == 0 else 0.0
    
    def _analyze_sequence_consistency(self, individual_scores: List[Dict[str, Any]]) -> float:
        """Analyze consistency across response sequence"""
        
        if len(individual_scores) < 2:
            return 1.0
        
        consistency_scores = []
        
        for i in range(1, len(individual_scores)):
            current_score = individual_scores[i]['role_adherence']
            previous_score = individual_scores[i-1]['role_adherence']
            
            consistency = 1.0 - abs(current_score - previous_score)
            consistency_scores.append(consistency)
        
        return sum(consistency_scores) / len(consistency_scores)
    
    def _analyze_quality_trend(self, individual_scores: List[Dict[str, Any]]) -> str:
        """Analyze quality trend across responses"""
        
        if len(individual_scores) < 3:
            return 'insufficient_data'
        
        scores = [score['overall_score'] for score in individual_scores]
        
        # Simple trend analysis
        early_avg = sum(scores[:len(scores)//2]) / (len(scores)//2)
        late_avg = sum(scores[len(scores)//2:]) / (len(scores) - len(scores)//2)
        
        if late_avg > early_avg + 0.1:
            return 'improving'
        elif late_avg < early_avg - 0.1:
            return 'declining'
        else:
            return 'stable'
    
    def _calculate_role_maintenance(self, individual_scores: List[Dict[str, Any]]) -> float:
        """Calculate role maintenance score across sequence"""
        
        role_adherence_scores = [score['role_adherence'] for score in individual_scores]
        
        if not role_adherence_scores:
            return 0.0
        
        # Average role adherence with penalty for high variance
        avg_adherence = sum(role_adherence_scores) / len(role_adherence_scores)
        
        if len(role_adherence_scores) > 1:
            variance = sum((score - avg_adherence) ** 2 for score in role_adherence_scores) / len(role_adherence_scores)
            variance_penalty = min(0.3, variance)  # Max penalty of 0.3
            return max(0.0, avg_adherence - variance_penalty)
        
        return avg_adherence
    
    def _generate_feedback(self, evaluation: Dict[str, Any]) -> List[str]:
        """Generate detailed feedback based on evaluation"""
        
        feedback = []
        
        if evaluation['quality_score'] < 0.6:
            feedback.append("响应质量需要改进，建议增加内容的深度和清晰度。")
        
        if evaluation['role_adherence'] < 0.7:
            feedback.append("角色一致性不足，建议更好地保持专业身份和角色特征。")
        
        if evaluation['consistency_score'] < 0.7:
            feedback.append("响应一致性有待提高，建议保持与之前回答的风格和观点一致。")
        
        if evaluation['completeness_score'] < 0.6:
            feedback.append("响应完整性不够，建议提供更全面的回答。")
        
        if evaluation['professionalism_score'] < 0.7:
            feedback.append("专业性需要加强，建议使用更正式和专业的语言。")
        
        if evaluation['overall_score'] >= 0.8:
            feedback.append("整体表现优秀，保持当前的回答质量和风格。")
        
        return feedback