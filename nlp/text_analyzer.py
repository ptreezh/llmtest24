"""
Text Analyzer for NLP processing of responses
"""

import logging
import re
from typing import Dict, List, Any, Optional, Tuple
from collections import Counter

logger = logging.getLogger(__name__)

class TextAnalyzer:
    """Analyzes text responses for various linguistic features"""
    
    def __init__(self, config):
        """Initialize text analyzer"""
        self.config = config
        
    def analyze_response(self, text: str) -> Dict[str, Any]:
        """Comprehensive analysis of a text response"""
        
        analysis = {
            'basic_stats': self._get_basic_stats(text),
            'linguistic_features': self._extract_linguistic_features(text),
            'sentiment_indicators': self._analyze_sentiment_indicators(text),
            'role_markers': self._extract_role_markers(text),
            'consistency_markers': self._extract_consistency_markers(text)
        }
        
        return analysis
    
    def compare_responses(self, response1: str, response2: str) -> Dict[str, Any]:
        """Compare two responses for similarity and consistency"""
        
        analysis1 = self.analyze_response(response1)
        analysis2 = self.analyze_response(response2)
        
        comparison = {
            'similarity_score': self._calculate_similarity(response1, response2),
            'style_consistency': self._compare_styles(analysis1, analysis2),
            'content_overlap': self._calculate_content_overlap(response1, response2),
            'linguistic_drift': self._detect_linguistic_drift(analysis1, analysis2)
        }
        
        return comparison
    
    def _get_basic_stats(self, text: str) -> Dict[str, Any]:
        """Get basic text statistics"""
        
        words = text.split()
        sentences = re.split(r'[.!?]+', text)
        sentences = [s.strip() for s in sentences if s.strip()]
        
        return {
            'char_count': len(text),
            'word_count': len(words),
            'sentence_count': len(sentences),
            'avg_word_length': sum(len(word) for word in words) / len(words) if words else 0,
            'avg_sentence_length': len(words) / len(sentences) if sentences else 0
        }
    
    def _extract_linguistic_features(self, text: str) -> Dict[str, Any]:
        """Extract linguistic features from text"""
        
        features = {
            'first_person_pronouns': len(re.findall(r'\b(我|我的|我们|我会|我认为)\b', text)),
            'professional_terms': len(re.findall(r'\b(专业|经验|技能|能力|职责|工作|项目)\b', text)),
            'certainty_markers': len(re.findall(r'\b(确定|肯定|一定|必须|绝对|明确)\b', text)),
            'uncertainty_markers': len(re.findall(r'\b(可能|也许|大概|或许|似乎|应该|大约)\b', text)),
            'question_count': len(re.findall(r'\?', text)),
            'exclamation_count': len(re.findall(r'!', text))
        }
        
        return features
    
    def _analyze_sentiment_indicators(self, text: str) -> Dict[str, Any]:
        """Analyze sentiment indicators in text"""
        
        positive_words = ['好', '优秀', '成功', '满意', '高兴', '自豪', '积极', '正面']
        negative_words = ['坏', '失败', '困难', '问题', '挑战', '担心', '焦虑', '消极']
        neutral_words = ['正常', '一般', '平常', '普通', '标准', '常规']
        
        sentiment = {
            'positive_count': sum(1 for word in positive_words if word in text),
            'negative_count': sum(1 for word in negative_words if word in text),
            'neutral_count': sum(1 for word in neutral_words if word in text)
        }
        
        total = sum(sentiment.values())
        if total > 0:
            sentiment['positive_ratio'] = sentiment['positive_count'] / total
            sentiment['negative_ratio'] = sentiment['negative_count'] / total
            sentiment['neutral_ratio'] = sentiment['neutral_count'] / total
        else:
            sentiment.update({'positive_ratio': 0, 'negative_ratio': 0, 'neutral_ratio': 0})
        
        return sentiment
    
    def _extract_role_markers(self, text: str) -> List[str]:
        """Extract markers that indicate role adherence"""
        
        markers = []
        
        role_patterns = {
            'identity_assertion': r'\b(我是|作为|身份|角色)\b',
            'professional_reference': r'\b(职业|专业|工作|职责|经验)\b',
            'expertise_claim': r'\b(专长|擅长|精通|熟悉|了解)\b',
            'responsibility_mention': r'\b(负责|承担|处理|管理|执行)\b'
        }
        
        for marker_type, pattern in role_patterns.items():
            matches = re.findall(pattern, text)
            if matches:
                markers.append(f"{marker_type}: {len(matches)} occurrences")
        
        return markers
    
    def _extract_consistency_markers(self, text: str) -> Dict[str, Any]:
        """Extract markers that indicate response consistency"""
        
        consistency_markers = {
            'temporal_consistency': len(re.findall(r'\b(一直|始终|总是|从来|向来)\b', text)),
            'behavioral_consistency': len(re.findall(r'\b(习惯|通常|一般|往往|经常)\b', text)),
            'value_consistency': len(re.findall(r'\b(坚持|相信|认为|原则|价值观)\b', text)),
            'style_consistency': len(re.findall(r'\b(风格|方式|方法|特点|特色)\b', text))
        }
        
        return consistency_markers
    
    def _calculate_similarity(self, text1: str, text2: str) -> float:
        """Calculate similarity between two texts"""
        
        # Simple word overlap similarity
        words1 = set(text1.lower().split())
        words2 = set(text2.lower().split())
        
        if not words1 and not words2:
            return 1.0
        
        intersection = words1.intersection(words2)
        union = words1.union(words2)
        
        return len(intersection) / len(union) if union else 0.0
    
    def _compare_styles(self, analysis1: Dict[str, Any], analysis2: Dict[str, Any]) -> Dict[str, Any]:
        """Compare linguistic styles between two analyses"""
        
        style_comparison = {}
        
        # Compare basic stats
        stats1 = analysis1['basic_stats']
        stats2 = analysis2['basic_stats']
        
        for key in ['avg_word_length', 'avg_sentence_length']:
            if key in stats1 and key in stats2:
                val1, val2 = stats1[key], stats2[key]
                if val1 > 0:
                    similarity = 1.0 - abs(val1 - val2) / val1
                    style_comparison[f'{key}_similarity'] = max(0.0, similarity)
        
        # Compare linguistic features
        features1 = analysis1['linguistic_features']
        features2 = analysis2['linguistic_features']
        
        feature_similarities = []
        for key in features1:
            if key in features2:
                val1, val2 = features1[key], features2[key]
                max_val = max(val1, val2, 1)  # Avoid division by zero
                similarity = 1.0 - abs(val1 - val2) / max_val
                feature_similarities.append(similarity)
        
        if feature_similarities:
            style_comparison['overall_feature_similarity'] = sum(feature_similarities) / len(feature_similarities)
        
        return style_comparison
    
    def _calculate_content_overlap(self, text1: str, text2: str) -> Dict[str, Any]:
        """Calculate content overlap between texts"""
        
        # Extract key phrases (2-grams and 3-grams)
        def get_ngrams(text: str, n: int) -> List[str]:
            words = text.lower().split()
            return [' '.join(words[i:i+n]) for i in range(len(words)-n+1)]
        
        bigrams1 = set(get_ngrams(text1, 2))
        bigrams2 = set(get_ngrams(text2, 2))
        
        trigrams1 = set(get_ngrams(text1, 3))
        trigrams2 = set(get_ngrams(text2, 3))
        
        bigram_overlap = len(bigrams1.intersection(bigrams2)) / len(bigrams1.union(bigrams2)) if bigrams1.union(bigrams2) else 0
        trigram_overlap = len(trigrams1.intersection(trigrams2)) / len(trigrams1.union(trigrams2)) if trigrams1.union(trigrams2) else 0
        
        return {
            'bigram_overlap': bigram_overlap,
            'trigram_overlap': trigram_overlap,
            'combined_overlap': (bigram_overlap + trigram_overlap) / 2
        }
    
    def _detect_linguistic_drift(self, analysis1: Dict[str, Any], analysis2: Dict[str, Any]) -> Dict[str, Any]:
        """Detect linguistic drift between two analyses"""
        
        drift_indicators = {}
        
        # Check for significant changes in linguistic features
        features1 = analysis1['linguistic_features']
        features2 = analysis2['linguistic_features']
        
        for feature in features1:
            if feature in features2:
                val1, val2 = features1[feature], features2[feature]
                if val1 > 0:
                    change_ratio = abs(val1 - val2) / val1
                    if change_ratio > 0.5:  # 50% change threshold
                        drift_indicators[feature] = {
                            'change_ratio': change_ratio,
                            'direction': 'increase' if val2 > val1 else 'decrease'
                        }
        
        return drift_indicators
