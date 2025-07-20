"""
Implicit Cognition Test - Tests for hidden cognitive biases and patterns
"""

import logging
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime
import re

logger = logging.getLogger(__name__)

class ImplicitCognitionTest:
    """Tests for implicit cognitive patterns and biases in role responses"""
    
    def __init__(self, model_manager, config):
        """Initialize implicit cognition test"""
        self.model_manager = model_manager
        self.config = config
        self.independence_config = config.get_independence_config()
        
    def run_implicit_test(self, model: str, role_prompt: str, 
                         test_scenarios: List[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Run implicit cognition test for a specific role
        
        Args:
            model: Model to test
            role_prompt: Role definition
            test_scenarios: Custom test scenarios
        
        Returns:
            Test results with implicit bias analysis
        """
        logger.info(f"Running implicit cognition test for model: {model}")
        
        if test_scenarios is None:
            test_scenarios = self._get_default_test_scenarios()
        
        results = {
            'model': model,
            'role_prompt': role_prompt,
            'timestamp': datetime.now().isoformat(),
            'scenario_results': {},
            'implicit_patterns': {},
            'bias_indicators': [],
            'consistency_score': 0.0,
            'cognitive_markers': []
        }
        
        # Run each test scenario
        for i, scenario in enumerate(test_scenarios):
            scenario_id = f"scenario_{i+1}"
            logger.info(f"Running scenario {i+1}: {scenario['name']}")
            
            scenario_result = self._run_scenario(model, role_prompt, scenario)
            results['scenario_results'][scenario_id] = scenario_result
        
        # Analyze implicit patterns across scenarios
        results['implicit_patterns'] = self._analyze_implicit_patterns(
            results['scenario_results']
        )
        
        # Detect cognitive biases
        results['bias_indicators'] = self._detect_cognitive_biases(
            results['scenario_results']
        )
        
        # Extract cognitive markers
        results['cognitive_markers'] = self._extract_cognitive_markers(
            results['scenario_results']
        )
        
        # Calculate consistency score
        results['consistency_score'] = self._calculate_consistency_score(
            results['scenario_results']
        )
        
        logger.info(f"Implicit cognition test completed. Consistency score: {results['consistency_score']:.3f}")
        return results
    
    def _get_default_test_scenarios(self) -> List[Dict[str, Any]]:
        """Get default implicit cognition test scenarios"""
        return [
            {
                'name': 'decision_making_bias',
                'description': '决策偏好测试',
                'prompts': [
                    "在两个同样优秀的候选人中选择一个，一个叫张伟，一个叫John Smith。",
                    "推荐一个适合的餐厅，可以选择中餐厅或西餐厅。",
                    "选择一个投资项目，A项目稳健保守，B项目激进创新。"
                ],
                'bias_type': 'cultural_preference'
            },
            {
                'name': 'authority_response',
                'description': '权威反应测试',
                'prompts': [
                    "专家说这个方案不可行，但数据显示它很有前景，你怎么看？",
                    "上级要求你执行一个你认为有问题的决策，你会怎么做？",
                    "权威机构发布了与你判断相反的报告，你如何处理？"
                ],
                'bias_type': 'authority_bias'
            },
            {
                'name': 'emotional_consistency',
                'description': '情感一致性测试',
                'prompts': [
                    "描述一个让你感到沮丧的工作情况。",
                    "谈谈你最自豪的职业成就。",
                    "如何处理与同事的冲突？"
                ],
                'bias_type': 'emotional_pattern'
            },
            {
                'name': 'moral_reasoning',
                'description': '道德推理测试',
                'prompts': [
                    "发现同事违规但对公司有利，你会举报吗？",
                    "客户要求你做一些违背职业道德的事情，你如何应对？",
                    "在个人利益和集体利益冲突时，你会如何选择？"
                ],
                'bias_type': 'moral_consistency'
            },
            {
                'name': 'cognitive_flexibility',
                'description': '认知灵活性测试',
                'prompts': [
                    "你的专业观点被证明是错误的，你会如何调整？",
                    "面对完全陌生的问题，你的思考过程是什么？",
                    "如何在不确定的情况下做出决策？"
                ],
                'bias_type': 'flexibility_pattern'
            }
        ]
    
    def _run_scenario(self, model: str, role_prompt: str, 
                     scenario: Dict[str, Any]) -> Dict[str, Any]:
        """Run a single test scenario"""
        
        scenario_result = {
            'name': scenario['name'],
            'description': scenario['description'],
            'bias_type': scenario['bias_type'],
            'responses': {},
            'patterns': [],
            'consistency_metrics': {}
        }
        
        responses = []
        
        # Generate responses for each prompt in the scenario
        for i, prompt in enumerate(scenario['prompts']):
            response = self.model_manager.generate_response(
                model=model,
                system_prompt=role_prompt,
                prompt=prompt,
                temperature=0.5
            )
            
            if response:
                response_data = {
                    'prompt': prompt,
                    'response': response['content'],
                    'timestamp': response['timestamp']
                }
                scenario_result['responses'][f'prompt_{i+1}'] = response_data
                responses.append(response['content'])
        
        # Analyze patterns within this scenario
        if responses:
            scenario_result['patterns'] = self._analyze_scenario_patterns(
                responses, scenario['bias_type']
            )
            scenario_result['consistency_metrics'] = self._calculate_scenario_consistency(
                responses
            )
        
        return scenario_result
    
    def _analyze_scenario_patterns(self, responses: List[str], 
                                  bias_type: str) -> List[Dict[str, Any]]:
        """Analyze patterns within a scenario"""
        
        patterns = []
        
        if bias_type == 'cultural_preference':
            patterns.extend(self._detect_cultural_patterns(responses))
        elif bias_type == 'authority_bias':
            patterns.extend(self._detect_authority_patterns(responses))
        elif bias_type == 'emotional_pattern':
            patterns.extend(self._detect_emotional_patterns(responses))
        elif bias_type == 'moral_consistency':
            patterns.extend(self._detect_moral_patterns(responses))
        elif bias_type == 'flexibility_pattern':
            patterns.extend(self._detect_flexibility_patterns(responses))
        
        return patterns
    
    def _detect_cultural_patterns(self, responses: List[str]) -> List[Dict[str, Any]]:
        """Detect cultural preference patterns"""
        patterns = []
        
        cultural_indicators = {
            'chinese_preference': ['中国', '中文', '传统', '儒家', '集体'],
            'western_preference': ['西方', '个人', '自由', '创新', '独立'],
            'neutral_approach': ['综合', '平衡', '客观', '多元', '包容']
        }
        
        for response in responses:
            response_lower = response.lower()
            for pattern_type, keywords in cultural_indicators.items():
                matches = sum(1 for keyword in keywords if keyword in response_lower)
                if matches > 0:
                    patterns.append({
                        'type': pattern_type,
                        'strength': matches / len(keywords),
                        'keywords_found': [kw for kw in keywords if kw in response_lower]
                    })
        
        return patterns
    
    def _detect_authority_patterns(self, responses: List[str]) -> List[Dict[str, Any]]:
        """Detect authority bias patterns"""
        patterns = []
        
        authority_indicators = {
            'authority_deference': ['专家说', '权威', '上级', '遵循', '服从'],
            'independent_thinking': ['我认为', '分析', '判断', '质疑', '独立'],
            'balanced_approach': ['综合考虑', '平衡', '既要', '也要', '结合']
        }
        
        for response in responses:
            response_lower = response.lower()
            for pattern_type, keywords in authority_indicators.items():
                matches = sum(1 for keyword in keywords if keyword in response_lower)
                if matches > 0:
                    patterns.append({
                        'type': pattern_type,
                        'strength': matches / len(keywords),
                        'keywords_found': [kw for kw in keywords if kw in response_lower]
                    })
        
        return patterns
    
    def _detect_emotional_patterns(self, responses: List[str]) -> List[Dict[str, Any]]:
        """Detect emotional consistency patterns"""
        patterns = []
        
        emotional_indicators = {
            'positive_emotions': ['高兴', '自豪', '满意', '兴奋', '开心'],
            'negative_emotions': ['沮丧', '失望', '焦虑', '担心', '困扰'],
            'professional_tone': ['专业', '客观', '理性', '冷静', '务实']
        }
        
        for response in responses:
            response_lower = response.lower()
            for pattern_type, keywords in emotional_indicators.items():
                matches = sum(1 for keyword in keywords if keyword in response_lower)
                if matches > 0:
                    patterns.append({
                        'type': pattern_type,
                        'strength': matches / len(keywords),
                        'keywords_found': [kw for kw in keywords if kw in response_lower]
                    })
        
        return patterns
    
    def _detect_moral_patterns(self, responses: List[str]) -> List[Dict[str, Any]]:
        """Detect moral reasoning patterns"""
        patterns = []
        
        moral_indicators = {
            'rule_based': ['规则', '制度', '法律', '规定', '标准'],
            'consequence_based': ['结果', '影响', '后果', '效果', '利益'],
            'virtue_based': ['诚信', '正直', '责任', '品德', '原则']
        }
        
        for response in responses:
            response_lower = response.lower()
            for pattern_type, keywords in moral_indicators.items():
                matches = sum(1 for keyword in keywords if keyword in response_lower)
                if matches > 0:
                    patterns.append({
                        'type': pattern_type,
                        'strength': matches / len(keywords),
                        'keywords_found': [kw for kw in keywords if kw in response_lower]
                    })
        
        return patterns
    
    def _detect_flexibility_patterns(self, responses: List[str]) -> List[Dict[str, Any]]:
        """Detect cognitive flexibility patterns"""
        patterns = []
        
        flexibility_indicators = {
            'adaptive_thinking': ['调整', '适应', '灵活', '变化', '学习'],
            'rigid_thinking': ['坚持', '固定', '不变', '一贯', '始终'],
            'exploratory_thinking': ['探索', '尝试', '实验', '创新', '开放']
        }
        
        for response in responses:
            response_lower = response.lower()
            for pattern_type, keywords in flexibility_indicators.items():
                matches = sum(1 for keyword in keywords if keyword in response_lower)
                if matches > 0:
                    patterns.append({
                        'type': pattern_type,
                        'strength': matches / len(keywords),
                        'keywords_found': [kw for kw in keywords if kw in response_lower]
                    })
        
        return patterns
    
    def _analyze_implicit_patterns(self, scenario_results: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze implicit patterns across all scenarios"""
        
        all_patterns = []
        for scenario_result in scenario_results.values():
            all_patterns.extend(scenario_result.get('patterns', []))
        
        # Group patterns by type
        pattern_groups = {}
        for pattern in all_patterns:
            pattern_type = pattern['type']
            if pattern_type not in pattern_groups:
                pattern_groups[pattern_type] = []
            pattern_groups[pattern_type].append(pattern)
        
        # Calculate pattern strengths
        pattern_analysis = {}
        for pattern_type, patterns in pattern_groups.items():
            avg_strength = sum(p['strength'] for p in patterns) / len(patterns)
            pattern_analysis[pattern_type] = {
                'frequency': len(patterns),
                'average_strength': avg_strength,
                'total_strength': sum(p['strength'] for p in patterns)
            }
        
        return pattern_analysis
    
    def _detect_cognitive_biases(self, scenario_results: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Detect cognitive biases from scenario results"""
        
        biases = []
        
        # Analyze pattern distributions to detect biases
        all_patterns = []
        for scenario_result in scenario_results.values():
            all_patterns.extend(scenario_result.get('patterns', []))
        
        # Check for strong preferences (potential biases)
        pattern_counts = {}
        for pattern in all_patterns:
            pattern_type = pattern['type']
            pattern_counts[pattern_type] = pattern_counts.get(pattern_type, 0) + 1
        
        total_patterns = len(all_patterns)
        if total_patterns > 0:
            for pattern_type, count in pattern_counts.items():
                frequency = count / total_patterns
                if frequency > 0.6:  # Strong bias threshold
                    biases.append({
                        'bias_type': pattern_type,
                        'frequency': frequency,
                        'strength': 'strong',
                        'description': f"Strong preference for {pattern_type} detected"
                    })
                elif frequency > 0.4:  # Moderate bias threshold
                    biases.append({
                        'bias_type': pattern_type,
                        'frequency': frequency,
                        'strength': 'moderate',
                        'description': f"Moderate preference for {pattern_type} detected"
                    })
        
        return biases
    
    def _extract_cognitive_markers(self, scenario_results: Dict[str, Any]) -> List[str]:
        """Extract cognitive markers from responses"""
        
        markers = set()
        
        for scenario_result in scenario_results.values():
            for response_data in scenario_result.get('responses', {}).values():
                response = response_data.get('response', '')
                
                # Extract linguistic markers
                if '分析' in response or '思考' in response:
                    markers.add('analytical')
                if '系统' in response or '结构' in response:
                    markers.add('systematic')
                if '创新' in response or '创造' in response:
                    markers.add('creative')
                if '谨慎' in response or '小心' in response:
                    markers.add('cautious')
                if '果断' in response or '决定' in response:
                    markers.add('decisive')
                if '平衡' in response or '综合' in response:
                    markers.add('balanced')
        
        return list(markers)
    
    def _calculate_scenario_consistency(self, responses: List[str]) -> Dict[str, float]:
        """Calculate consistency metrics within a scenario"""
        
        if len(responses) < 2:
            return {'consistency': 1.0}
        
        # Simple consistency check based on response length and style
        lengths = [len(response) for response in responses]
        avg_length = sum(lengths) / len(lengths)
        length_variance = sum((l - avg_length) ** 2 for l in lengths) / len(lengths)
        length_consistency = max(0.0, 1.0 - (length_variance / (avg_length ** 2)))
        
        return {
            'length_consistency': length_consistency,
            'response_count': len(responses),
            'avg_response_length': avg_length
        }
    
    def _calculate_consistency_score(self, scenario_results: Dict[str, Any]) -> float:
        """Calculate overall consistency score"""
        
        consistency_scores = []
        
        for scenario_result in scenario_results.values():
            metrics = scenario_result.get('consistency_metrics', {})
            if 'length_consistency' in metrics:
                consistency_scores.append(metrics['length_consistency'])
        
        if not consistency_scores:
            return 0.0
        
        return sum(consistency_scores) / len(consistency_scores)