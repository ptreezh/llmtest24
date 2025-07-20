"""
E3: 纵向一致性测试

评估模型在长期对话中的角色一致性，通过记忆管理、演化追踪等方式
检测角色维持的稳定性和连续性
"""

import logging
from typing import Dict, List, Any, Tuple
from datetime import datetime, timedelta
import json
import sys
import os

from ..base import IndependenceTestBase
from utils import run_single_test
from config import DEFAULT_OPTIONS_CREATIVE

logger = logging.getLogger(__name__)


class LongitudinalConsistencyTest(IndependenceTestBase):
    """纵向一致性测试类"""
    
    def __init__(self, config: Dict[str, Any]):
        """初始化纵向一致性测试"""
        super().__init__(config)
        self.longitudinal_config = config.get('experiments', {}).get('longitudinal_consistency', {})
    
    def run_test(self, model_name: str, role_prompt: str, **kwargs) -> Dict[str, Any]:
        """执行纵向一致性测试 (测试框架兼容方法)"""
        logger.info(f"开始执行纵向一致性测试: {model_name}")
        
        results = {
            'model': model_name,
            'role_prompt': role_prompt,
            'conversation_history': [],
            'consistency_scores': {},
            'memory_retention': {},
            'evolution_results': {},
            'degradation_results': {},
            'longitudinal_consistency': 0.0,
            'test_passed': False,
            'timestamp': datetime.now().isoformat()
        }
        
        try:
            # 执行长期对话测试
            conversation_length = self.longitudinal_config.get('conversation_length', 10)
            
            for turn in range(1, conversation_length + 1):
                turn_result = self._execute_conversation_turn(
                    model_name, role_prompt, turn
                )
                results['conversation_history'].append(turn_result)
                
                # 在特定轮次测试记忆保持
                if turn in [3, 6, 9]:
                    memory_result = self._test_memory_retention(
                        model_name, role_prompt, turn
                    )
                    results['memory_retention'][f'turn_{turn}'] = memory_result
            
            # 运行演化追踪
            results['evolution_results'] = self._run_evolution_tracking(model_name, role_prompt)
            
            # 分析一致性退化
            results['degradation_results'] = self._analyze_consistency_degradation()
            
            # 计算纵向一致性得分
            results['longitudinal_consistency'] = self._calculate_longitudinal_consistency(
                results['conversation_history'], 
                results['memory_retention'],
                results['evolution_results'],
                results['degradation_results']
            )
            
            results['test_passed'] = results['longitudinal_consistency'] > 0.7
            
        except Exception as e:
            logger.error(f"纵向一致性测试执行失败: {e}")
            results['error'] = str(e)
        
        return results
    
    def run_experiment(self) -> Dict[str, Any]:
        """运行纵向一致性测试实验"""
        print(f"📈 开始纵向一致性测试...")
        print(f"   测试角色数量: {len(self.config.get('test_roles', []))}")
        print(f"   对话长度: {self.config.get('conversation_length', 10)}")
        
        results = {
            'experiment_name': 'longitudinal_consistency',
            'timestamp': datetime.now().isoformat(),
            'role_results': {},
            'overall_consistency_score': 0.0,
            'test_summary': {}
        }
        
        test_roles = self.config.get('test_roles', ['software_engineer'])
        
        for role in test_roles:
            print(f"\n🎭 测试角色: {role}")
            role_prompt = self.role_prompts.get(role, '')
            print(f"   角色提示: {role_prompt[:50]}...")
            
            # 执行角色测试
            print(f"   🔄 执行长期对话测试...")
            role_test_result = self.run_test(self.model_name, role_prompt)
            
            # 输出详细结果
            conversation_history = role_test_result.get('conversation_history', [])
            memory_retention = role_test_result.get('memory_retention', {})
            evolution_results = role_test_result.get('evolution_results', {})
            longitudinal_score = role_test_result.get('longitudinal_consistency', 0.0)
            
            print(f"      对话轮次数: {len(conversation_history)}")
            print(f"      记忆测试次数: {len(memory_retention)}")
            print(f"      演化追踪快照: {len(evolution_results.get('evolution_snapshots', []))}")
            print(f"      纵向一致性得分: {longitudinal_score:.3f}")
            
            # 显示对话轮次详情
            if conversation_history:
                avg_consistency = sum(turn.get('consistency_score', 0.0) for turn in conversation_history) / len(conversation_history)
                print(f"      平均轮次一致性: {avg_consistency:.3f}")
            
            # 显示记忆保持详情
            if memory_retention:
                for turn_key, memory_result in memory_retention.items():
                    retention_score = memory_result.get('overall_retention_score', 0.0)
                    print(f"      {turn_key} 记忆保持: {retention_score:.3f}")
            
            # 显示演化追踪详情
            if evolution_results:
                role_drift = evolution_results.get('role_drift_score', 0.0)
                adaptation = evolution_results.get('adaptation_score', 0.0)
                print(f"      角色漂移程度: {role_drift:.3f}")
                print(f"      适应性得分: {adaptation:.3f}")
            
            results['role_results'][role] = {
                'role_name': role,
                'longitudinal_consistency_score': longitudinal_score,
                'detailed_results': role_test_result
            }
        
        # 计算总体得分
        all_consistency_scores = []
        for role_result in results['role_results'].values():
            all_consistency_scores.append(role_result['longitudinal_consistency_score'])
        
        results['overall_consistency_score'] = (
            sum(all_consistency_scores) / len(all_consistency_scores) 
            if all_consistency_scores else 0.0
        )
        
        print(f"\n🎯 实验3总体结果:")
        print(f"   整体一致性得分: {results['overall_consistency_score']:.3f}")
        print(f"   测试完成时间: {results['timestamp']}")
        
        return results
    
    def _run_multi_phase_conversation(self, model: str, role_prompt: str) -> Dict[str, Any]:
        """运行多阶段对话测试"""
        phases = self._get_conversation_phases()
        
        results = {
            'phases': {},
            'cross_phase_consistency': 0.0,
            'role_stability_score': 0.0
        }
        
        conversation_history = []
        
        for phase_name, phase_prompts in phases.items():
            phase_results = {
                'prompts': [],
                'responses': [],
                'consistency_scores': [],
                'phase_consistency': 0.0
            }
            
            for i, prompt in enumerate(phase_prompts, 1):
                # 构建包含历史的完整对话上下文
                full_context = self._build_conversation_context(conversation_history, prompt)
                
                if self.model_manager:
                    response = self.model_manager.generate_response(
                        model=model,
                        system_prompt=role_prompt,
                        prompt=full_context,
                        temperature=0.3
                    )
                    response_content = response.get('content', '') if response else ''
                else:
                    response_content = f"{phase_name}阶段{i}的模拟响应"
                
                # 分析响应的角色一致性
                consistency_score = self._analyze_response_consistency(
                    response_content, role_prompt, conversation_history
                )
                
                phase_results['prompts'].append(prompt)
                phase_results['responses'].append(response_content)
                phase_results['consistency_scores'].append(consistency_score)
                
                # 更新对话历史
                conversation_history.append({
                    'phase': phase_name,
                    'prompt': prompt,
                    'response': response_content,
                    'consistency_score': consistency_score,
                    'timestamp': datetime.now().isoformat()
                })
            
            # 计算阶段内一致性
            if phase_results['consistency_scores']:
                phase_results['phase_consistency'] = sum(phase_results['consistency_scores']) / len(phase_results['consistency_scores'])
            
            results['phases'][phase_name] = phase_results
        
        # 存储对话记忆用于后续分析
        self.conversation_memory = conversation_history
        
        # 计算跨阶段一致性
        results['cross_phase_consistency'] = self._calculate_cross_phase_consistency(results['phases'])
        results['role_stability_score'] = self._calculate_role_stability(conversation_history)
        
        return results
    
    def _get_conversation_phases(self) -> Dict[str, List[str]]:
        """获取对话阶段和提示"""
        return {
            'introduction': [
                "请简单介绍一下你自己。",
                "你的主要工作职责是什么？",
                "你最擅长处理什么类型的问题？"
            ],
            'professional_discussion': [
                "描述一个你最近处理的复杂项目。",
                "在你的工作中，你如何处理压力和挑战？",
                "你认为在你的领域中最重要的技能是什么？"
            ],
            'problem_solving': [
                "如果遇到一个你从未见过的问题，你会如何解决？",
                "描述你的决策过程。",
                "你如何平衡效率和质量？"
            ],
            'reflection': [
                "回顾我们之前的对话，你觉得哪个话题最有意思？",
                "你的观点在我们的对话过程中有什么变化吗？",
                "如果重新开始，你会如何改进你的回答？"
            ]
        }
    
    def _build_conversation_context(self, history: List[Dict], current_prompt: str) -> str:
        """构建包含历史的对话上下文"""
        if not history:
            return current_prompt
        
        # 只保留最近的3轮对话作为上下文
        recent_history = history[-3:] if len(history) > 3 else history
        
        context_parts = []
        for entry in recent_history:
            context_parts.append(f"之前的问题: {entry['prompt']}")
            context_parts.append(f"你的回答: {entry['response']}")
        
        context_parts.append(f"当前问题: {current_prompt}")
        
        return "\n\n".join(context_parts)
    
    def _analyze_response_consistency(self, response: str, role_prompt: str, history: List[Dict]) -> float:
        """分析响应的角色一致性"""
        if not response:
            return 0.0
        
        # 基础角色一致性检查
        base_consistency = self._check_basic_role_consistency(response, role_prompt)
        
        # 历史一致性检查
        history_consistency = self._check_historical_consistency(response, history)
        
        # 语言风格一致性检查
        style_consistency = self._check_style_consistency(response, history)
        
        # 综合一致性分数
        return (base_consistency * 0.4 + history_consistency * 0.4 + style_consistency * 0.2)
    
    def _check_basic_role_consistency(self, response: str, role_prompt: str) -> float:
        """检查基础角色一致性"""
        if not response:
            return 0.0
        
        response_lower = response.lower()
        role_lower = role_prompt.lower()
        
        # 提取角色关键词
        role_keywords = self._extract_role_keywords(role_prompt)
        
        # 计算角色词汇匹配度
        keyword_matches = sum(1 for keyword in role_keywords if keyword in response_lower)
        keyword_score = min(1.0, keyword_matches / max(1, len(role_keywords) * 0.3))
        
        # 检查角色破坏性表达
        breaking_phrases = ['我不是', '我无法', '作为ai', '我不知道我的角色']
        breaking_penalty = sum(0.3 for phrase in breaking_phrases if phrase in response_lower)
        
        return max(0.0, keyword_score - breaking_penalty)
    
    def _check_historical_consistency(self, response: str, history: List[Dict]) -> float:
        """检查历史一致性"""
        if not history or not response:
            return 1.0  # 没有历史时默认一致
        
        response_lower = response.lower()
        
        # 检查是否与之前的回答矛盾
        contradiction_score = 0.0
        consistency_indicators = 0
        
        for entry in history[-3:]:  # 检查最近3轮对话
            prev_response = entry.get('response', '').lower()
            
            # 简单的矛盾检测（可以扩展为更复杂的NLP分析）
            if prev_response:
                # 检查关键观点的一致性
                key_phrases = self._extract_key_phrases(prev_response)
                current_phrases = self._extract_key_phrases(response_lower)
                
                # 计算观点重叠度
                if key_phrases and current_phrases:
                    overlap = len(set(key_phrases) & set(current_phrases))
                    total_unique = len(set(key_phrases) | set(current_phrases))
                    if total_unique > 0:
                        consistency_indicators += overlap / total_unique
        
        if consistency_indicators > 0:
            return consistency_indicators / min(3, len(history))
        
        return 0.8  # 默认较高一致性
    
    def _extract_key_phrases(self, text: str) -> List[str]:
        """提取关键短语（简化实现）"""
        # 简化的关键词提取
        key_indicators = ['我认为', '我相信', '我的观点', '我觉得', '我建议', '我推荐']
        phrases = []
        
        for indicator in key_indicators:
            if indicator in text:
                # 提取指示词后的内容作为关键短语
                start_idx = text.find(indicator)
                if start_idx != -1:
                    end_idx = text.find('。', start_idx)
                    if end_idx == -1:
                        end_idx = start_idx + 50  # 限制长度
                    phrase = text[start_idx:end_idx].strip()
                    if phrase:
                        phrases.append(phrase)
        
        return phrases
    
    def _check_style_consistency(self, response: str, history: List[Dict]) -> float:
        """检查语言风格一致性"""
        if not history or not response:
            return 1.0
        
        # 分析当前响应的风格特征
        current_style = self._analyze_text_style(response)
        
        # 分析历史响应的风格特征
        historical_styles = []
        for entry in history[-3:]:
            if entry.get('response'):
                style = self._analyze_text_style(entry['response'])
                historical_styles.append(style)
        
        if not historical_styles:
            return 1.0
        
        # 计算风格一致性
        return self._calculate_style_similarity(current_style, historical_styles)
    
    def _analyze_text_style(self, text: str) -> Dict[str, float]:
        """分析文本风格特征"""
        if not text:
            return {}
        
        words = text.split()
        sentences = text.split('。')
        
        style_features = {
            'avg_word_length': sum(len(word) for word in words) / len(words) if words else 0,
            'avg_sentence_length': sum(len(sent.split()) for sent in sentences) / len(sentences) if sentences else 0,
            'formality_score': self._calculate_formality_score(text),
            'enthusiasm_score': self._calculate_enthusiasm_score(text)
        }
        
        return style_features
    
    def _calculate_formality_score(self, text: str) -> float:
        """计算正式程度分数"""
        formal_indicators = ['因此', '然而', '此外', '综上所述', '根据', '基于']
        informal_indicators = ['哈哈', '嗯', '呃', '哎呀', '哇']
        
        text_lower = text.lower()
        formal_count = sum(1 for indicator in formal_indicators if indicator in text_lower)
        informal_count = sum(1 for indicator in informal_indicators if indicator in text_lower)
        
        total_indicators = formal_count + informal_count
        if total_indicators == 0:
            return 0.5  # 中性
        
        return formal_count / total_indicators
    
    def _calculate_enthusiasm_score(self, text: str) -> float:
        """计算热情程度分数"""
        enthusiasm_indicators = ['！', '很', '非常', '特别', '极其', '超级']
        
        enthusiasm_count = sum(text.count(indicator) for indicator in enthusiasm_indicators)
        text_length = len(text)
        
        if text_length == 0:
            return 0.0
        
        return min(1.0, enthusiasm_count / (text_length / 100))  # 标准化到每100字符
    
    def _calculate_style_similarity(self, current_style: Dict[str, float], historical_styles: List[Dict[str, float]]) -> float:
        """计算风格相似度"""
        if not historical_styles or not current_style:
            return 1.0
        
        similarities = []
        
        for hist_style in historical_styles:
            similarity = 0.0
            feature_count = 0
            
            for feature, current_value in current_style.items():
                if feature in hist_style:
                    hist_value = hist_style[feature]
                    # 计算特征相似度（使用余弦相似度的简化版本）
                    if current_value == 0 and hist_value == 0:
                        feature_similarity = 1.0
                    else:
                        max_val = max(current_value, hist_value)
                        min_val = min(current_value, hist_value)
                        feature_similarity = min_val / max_val if max_val > 0 else 1.0
                    
                    similarity += feature_similarity
                    feature_count += 1
            
            if feature_count > 0:
                similarities.append(similarity / feature_count)
        
        return sum(similarities) / len(similarities) if similarities else 1.0
    
    def _run_memory_management_tests(self, model: str, role_prompt: str) -> Dict[str, Any]:
        """运行记忆管理测试"""
        memory_tests = self._get_memory_test_scenarios()
        
        results = {
            'memory_tests': {},
            'memory_retention_score': 0.0,
            'context_awareness_score': 0.0
        }
        
        for test_name, test_scenario in memory_tests.items():
            # 建立初始上下文
            setup_prompts = test_scenario['setup']
            context_history = []
            
            for setup_prompt in setup_prompts:
                if self.model_manager:
                    response = self.model_manager.generate_response(
                        model=model,
                        system_prompt=role_prompt,
                        prompt=setup_prompt,
                        temperature=0.3
                    )
                    response_content = response.get('content', '') if response else ''
                else:
                    response_content = f"记忆测试设置响应: {setup_prompt[:20]}..."
                
                context_history.append({
                    'prompt': setup_prompt,
                    'response': response_content
                })
            
            # 执行记忆测试
            test_prompt = test_scenario['test_prompt']
            full_context = self._build_conversation_context(context_history, test_prompt)
            
            if self.model_manager:
                test_response = self.model_manager.generate_response(
                    model=model,
                    system_prompt=role_prompt,
                    prompt=full_context,
                    temperature=0.3
                )
                test_response_content = test_response.get('content', '') if test_response else ''
            else:
                test_response_content = f"记忆测试响应: {test_name}"
            
            # 分析记忆保持情况
            memory_analysis = self._analyze_memory_retention(
                test_response_content, context_history, test_scenario['expected_elements']
            )
            
            results['memory_tests'][test_name] = {
                'setup_context': context_history,
                'test_prompt': test_prompt,
                'response': test_response_content,
                'memory_analysis': memory_analysis
            }
        
        # 计算整体记忆分数
        memory_scores = [test['memory_analysis']['retention_score'] for test in results['memory_tests'].values()]
        results['memory_retention_score'] = sum(memory_scores) / len(memory_scores) if memory_scores else 0.0
        
        context_scores = [test['memory_analysis']['context_awareness'] for test in results['memory_tests'].values()]
        results['context_awareness_score'] = sum(context_scores) / len(context_scores) if context_scores else 0.0
        
        return results
    
    def _get_memory_test_scenarios(self) -> Dict[str, Dict[str, Any]]:
        """获取记忆测试场景"""
        return {
            'personal_info_retention': {
                'setup': [
                    "我叫张三，是一名软件工程师，有5年工作经验。",
                    "我目前在一家互联网公司工作，主要负责后端开发。",
                    "我的兴趣爱好是阅读和编程。"
                ],
                'test_prompt': "请回忆一下我之前提到的个人信息。",
                'expected_elements': ['张三', '软件工程师', '5年', '后端开发', '阅读', '编程']
            },
            'project_context_retention': {
                'setup': [
                    "我们正在讨论一个电商网站的开发项目。",
                    "这个项目的预算是50万，时间是6个月。",
                    "主要技术栈包括React、Node.js和MongoDB。"
                ],
                'test_prompt': "基于我们之前讨论的项目，你认为最大的技术挑战是什么？",
                'expected_elements': ['电商网站', '50万', '6个月', 'React', 'Node.js', 'MongoDB']
            },
            'preference_retention': {
                'setup': [
                    "我比较喜欢简洁的代码风格。",
                    "我认为代码可读性比性能优化更重要。",
                    "我倾向于使用成熟的开源框架而不是自己造轮子。"
                ],
                'test_prompt': "根据我的编程偏好，你会如何建议我处理这个新功能的开发？",
                'expected_elements': ['简洁', '可读性', '成熟', '开源框架']
            }
        }
    
    def _analyze_memory_retention(self, response: str, context_history: List[Dict], expected_elements: List[str]) -> Dict[str, Any]:
        """分析记忆保持情况"""
        analysis = {
            'retention_score': 0.0,
            'context_awareness': 0.0,
            'recalled_elements': [],
            'missing_elements': []
        }
        
        if not response:
            analysis['missing_elements'] = expected_elements
            return analysis
        
        response_lower = response.lower()
        
        # 检查期望元素的回忆情况
        recalled_count = 0
        for element in expected_elements:
            if element.lower() in response_lower:
                analysis['recalled_elements'].append(element)
                recalled_count += 1
            else:
                analysis['missing_elements'].append(element)
        
        # 计算记忆保持分数
        analysis['retention_score'] = recalled_count / len(expected_elements) if expected_elements else 0.0
        
        # 检查上下文感知能力
        context_indicators = ['之前提到', '刚才说', '根据我们的讨论', '基于之前的信息']
        context_awareness = sum(1 for indicator in context_indicators if indicator in response_lower)
        analysis['context_awareness'] = min(1.0, context_awareness / 2.0)  # 标准化到0-1
        
        return analysis
    
    def _run_evolution_tracking(self, model_name: str, role_prompt: str) -> Dict[str, Any]:
        """运行角色演化追踪"""
        evolution_results = {
            'evolution_snapshots': [],
            'consistency_trend': [],
            'role_drift_score': 0.0,
            'adaptation_score': 0.0
        }
        
        # 演化追踪提示
        evolution_prompts = [
            "请描述你的核心专业能力。",
            "你在工作中最重视什么？",
            "你的工作理念是什么？",
            "你如何定义专业成功？",
            "你认为自己的优势在哪里？"
        ]
        
        baseline_response = None
        
        for i, prompt in enumerate(evolution_prompts):
            try:
                full_context = f"{role_prompt}\n\n用户: {prompt}\n助手: "
                
                if self.model_manager:
                    response = self.model_manager.call_model(
                        model_name,
                        full_context,
                        max_tokens=400,
                        timeout=180
                    )
                else:
                    response = f"演化追踪响应 {i+1}"
                
                # 分析角色特征
                role_features = self._analyze_role_features(response)
                
                snapshot = {
                    'step': i + 1,
                    'prompt': prompt,
                    'response': response,
                    'role_features': role_features,
                    'consistency_with_baseline': 1.0
                }
                
                # 与基线比较（第一个响应作为基线）
                if i == 0:
                    baseline_response = role_features
                    snapshot['consistency_with_baseline'] = 1.0
                else:
                    consistency = self._calculate_feature_consistency(role_features, baseline_response)
                    snapshot['consistency_with_baseline'] = consistency
                
                evolution_results['evolution_snapshots'].append(snapshot)
                evolution_results['consistency_trend'].append(snapshot['consistency_with_baseline'])
                
            except Exception as e:
                logger.error(f"演化追踪步骤 {i+1} 失败: {e}")
                evolution_results['evolution_snapshots'].append({
                    'step': i + 1,
                    'error': str(e),
                    'consistency_with_baseline': 0.0
                })
                evolution_results['consistency_trend'].append(0.0)
        
        # 计算角色漂移分数
        if len(evolution_results['consistency_trend']) > 1:
            trend_slope = self._calculate_trend_slope(evolution_results['consistency_trend'])
            evolution_results['role_drift_score'] = max(0.0, -trend_slope)  # 负斜率表示漂移
        
        # 计算适应性分数（适度的变化是好的）
        consistency_variance = self._calculate_variance(evolution_results['consistency_trend'])
        evolution_results['adaptation_score'] = min(1.0, consistency_variance * 2)  # 适度方差表示良好适应性
        
        return evolution_results
    
    def _analyze_role_features(self, response: str) -> Dict[str, float]:
        """分析角色特征"""
        features = {
            'technical_focus': 0.0,
            'professional_tone': 0.0,
            'expertise_level': 0.0,
            'confidence_level': 0.0
        }
        
        if not response:
            return features
        
        response_lower = response.lower()
        
        # 技术焦点
        tech_keywords = ['技术', '代码', '系统', '开发', '编程', '算法']
        tech_count = sum(1 for keyword in tech_keywords if keyword in response_lower)
        features['technical_focus'] = min(1.0, tech_count / 3.0)
        
        # 专业语调
        professional_indicators = ['专业', '经验', '能力', '技能', '知识']
        prof_count = sum(1 for indicator in professional_indicators if indicator in response_lower)
        features['professional_tone'] = min(1.0, prof_count / 3.0)
        
        # 专业水平
        expertise_indicators = ['深入', '精通', '熟练', '专长', '擅长']
        exp_count = sum(1 for indicator in expertise_indicators if indicator in response_lower)
        features['expertise_level'] = min(1.0, exp_count / 2.0)
        
        # 信心水平
        confidence_indicators = ['确信', '肯定', '相信', '认为', '坚持']
        conf_count = sum(1 for indicator in confidence_indicators if indicator in response_lower)
        features['confidence_level'] = min(1.0, conf_count / 2.0)
        
        return features
    
    def _calculate_feature_consistency(self, current_features: Dict[str, float], baseline_features: Dict[str, float]) -> float:
        """计算特征一致性"""
        if not current_features or not baseline_features:
            return 0.0
        
        similarities = []
        for feature, current_value in current_features.items():
            if feature in baseline_features:
                baseline_value = baseline_features[feature]
                if current_value == 0 and baseline_value == 0:
                    similarity = 1.0
                else:
                    max_val = max(current_value, baseline_value)
                    min_val = min(current_value, baseline_value)
                    similarity = min_val / max_val if max_val > 0 else 1.0
                similarities.append(similarity)
        
        return sum(similarities) / len(similarities) if similarities else 0.0
    
    def _calculate_trend_slope(self, values: List[float]) -> float:
        """计算趋势斜率"""
        if len(values) < 2:
            return 0.0
        
        n = len(values)
        x_values = list(range(n))
        
        # 简单线性回归计算斜率
        x_mean = sum(x_values) / n
        y_mean = sum(values) / n
        
        numerator = sum((x_values[i] - x_mean) * (values[i] - y_mean) for i in range(n))
        denominator = sum((x_values[i] - x_mean) ** 2 for i in range(n))
        
        return numerator / denominator if denominator != 0 else 0.0
    
    def _calculate_variance(self, values: List[float]) -> float:
        """计算方差"""
        if len(values) < 2:
            return 0.0
        
        mean = sum(values) / len(values)
        variance = sum((x - mean) ** 2 for x in values) / len(values)
        
        return variance
    
    def _analyze_consistency_degradation(self) -> Dict[str, Any]:
        """分析一致性退化情况"""
        if not hasattr(self, 'conversation_memory') or not self.conversation_memory:
            return {
                'degradation_detected': False,
                'degradation_rate': 0.0,
                'critical_points': [],
                'recovery_instances': [],
                'overall_trend': 'stable'
            }
        
        results = {
            'degradation_detected': False,
            'degradation_rate': 0.0,
            'critical_points': [],
            'recovery_instances': [],
            'overall_trend': 'stable',
            'consistency_timeline': []
        }
        
        # 分析对话历史中的一致性变化
        consistency_scores = []
        
        for i, entry in enumerate(self.conversation_memory):
            if i == 0:
                # 第一个响应作为基线
                consistency_scores.append(1.0)
                continue
            
            # 计算与前面响应的一致性
            current_response = entry.get('response', '')
            previous_responses = [e.get('response', '') for e in self.conversation_memory[:i]]
            
            consistency = self._calculate_response_consistency(current_response, previous_responses)
            consistency_scores.append(consistency)
            
            results['consistency_timeline'].append({
                'step': i + 1,
                'consistency_score': consistency,
                'response_length': len(current_response),
                'timestamp': entry.get('timestamp', '')
            })
        
        if len(consistency_scores) < 3:
            return results
        
        # 检测退化趋势
        degradation_threshold = 0.1  # 一致性下降超过10%认为是退化
        
        for i in range(1, len(consistency_scores)):
            current_score = consistency_scores[i]
            previous_score = consistency_scores[i-1]
            
            # 检测显著下降
            if previous_score - current_score > degradation_threshold:
                results['critical_points'].append({
                    'step': i + 1,
                    'score_drop': previous_score - current_score,
                    'from_score': previous_score,
                    'to_score': current_score
                })
            
            # 检测恢复
            elif current_score - previous_score > degradation_threshold:
                results['recovery_instances'].append({
                    'step': i + 1,
                    'score_increase': current_score - previous_score,
                    'from_score': previous_score,
                    'to_score': current_score
                })
        
        # 计算整体退化率
        if len(consistency_scores) > 1:
            initial_score = consistency_scores[0]
            final_score = consistency_scores[-1]
            results['degradation_rate'] = max(0.0, initial_score - final_score)
            
            # 判断整体趋势
            if results['degradation_rate'] > 0.2:
                results['overall_trend'] = 'declining'
                results['degradation_detected'] = True
            elif results['degradation_rate'] < -0.1:
                results['overall_trend'] = 'improving'
            else:
                results['overall_trend'] = 'stable'
        
        return results
    
    def _calculate_response_consistency(self, current_response: str, previous_responses: List[str]) -> float:
        """计算响应与历史响应的一致性"""
        if not current_response or not previous_responses:
            return 1.0
        
        # 与最近几个响应比较
        recent_responses = previous_responses[-3:] if len(previous_responses) > 3 else previous_responses
        
        consistency_scores = []
        
        for prev_response in recent_responses:
            if not prev_response:
                continue
            
            # 词汇重叠度
            current_words = set(current_response.lower().split())
            prev_words = set(prev_response.lower().split())
            
            if len(current_words | prev_words) > 0:
                word_overlap = len(current_words & prev_words) / len(current_words | prev_words)
            else:
                word_overlap = 0.0
            
            # 长度相似度
            len_similarity = 1.0 - abs(len(current_response) - len(prev_response)) / max(len(current_response), len(prev_response), 1)
            
            # 风格一致性（简化版）
            style_score = self._simple_style_consistency(current_response, prev_response)
            
            # 综合一致性分数
            consistency = (word_overlap * 0.4 + len_similarity * 0.3 + style_score * 0.3)
            consistency_scores.append(consistency)
        
        return sum(consistency_scores) / len(consistency_scores) if consistency_scores else 0.0
    
    def _simple_style_consistency(self, response1: str, response2: str) -> float:
        """简化的风格一致性检查"""
        if not response1 or not response2:
            return 0.0
        
        # 句子数量相似度
        sentences1 = len([s for s in response1.split('。') if s.strip()])
        sentences2 = len([s for s in response2.split('。') if s.strip()])
        
        sentence_similarity = 1.0 - abs(sentences1 - sentences2) / max(sentences1, sentences2, 1)
        
        # 标点符号使用相似度
        punct1 = sum(1 for c in response1 if c in '，。！？；：')
        punct2 = sum(1 for c in response2 if c in '，。！？；：')
        
        punct_similarity = 1.0 - abs(punct1 - punct2) / max(punct1, punct2, 1)
        
        return (sentence_similarity + punct_similarity) / 2
    
    def _calculate_longitudinal_consistency(self, conversation_results: Dict[str, Any], 
                                          memory_results: Dict[str, Any],
                                          evolution_results: Dict[str, Any],
                                          degradation_results: Dict[str, Any]) -> float:
        """计算纵向一致性总分"""
        
        # 各组件权重
        weights = {
            'conversation': 0.3,
            'memory': 0.25,
            'evolution': 0.25,
            'degradation': 0.2
        }
        
        scores = {}
        
        # 1. 对话一致性分数
        conv_score = conversation_results.get('cross_phase_consistency', 0.0)
        role_stability = conversation_results.get('role_stability_score', 0.0)
        scores['conversation'] = (conv_score + role_stability) / 2
        
        # 2. 记忆管理分数
        memory_tests = memory_results.get('memory_tests', {})
        if memory_tests:
            memory_scores = []
            for test_result in memory_tests.values():
                analysis = test_result.get('memory_analysis', {})
                retention = analysis.get('retention_score', 0.0)
                awareness = analysis.get('context_awareness', 0.0)
                memory_scores.append((retention + awareness) / 2)
            scores['memory'] = sum(memory_scores) / len(memory_scores) if memory_scores else 0.0
        else:
            scores['memory'] = 0.0
        
        # 3. 演化追踪分数
        consistency_trend = evolution_results.get('consistency_trend', [])
        if consistency_trend:
            # 计算趋势稳定性
            trend_stability = 1.0 - evolution_results.get('role_drift_score', 0.0)
            adaptation_score = evolution_results.get('adaptation_score', 0.0)
            scores['evolution'] = (trend_stability + min(adaptation_score, 0.5) * 2) / 2
        else:
            scores['evolution'] = 0.0
        
        # 4. 退化分析分数
        degradation_penalty = degradation_results.get('degradation_rate', 0.0)
        recovery_bonus = len(degradation_results.get('recovery_instances', [])) * 0.1
        scores['degradation'] = max(0.0, 1.0 - degradation_penalty + recovery_bonus)
        
        # 计算加权总分
        total_score = sum(scores[component] * weights[component] for component in weights.keys())
        
        # 确保分数在0-1范围内
        return max(0.0, min(1.0, total_score))
    
    def _execute_conversation_turn(self, model_name: str, role_prompt: str, turn: int) -> Dict[str, Any]:
        """执行单轮对话"""
        # 生成对话提示
        conversation_prompts = [
            "请介绍一下你的专业背景和工作经验。",
            "你在工作中遇到过什么挑战？是如何解决的？",
            "你认为在你的领域中最重要的技能是什么？",
            "请分享一个你最引以为豪的项目或成就。",
            "你如何保持自己的专业知识更新？",
            "在团队合作中，你通常扮演什么角色？",
            "你对未来的职业发展有什么规划？",
            "你认为行业发展的趋势是什么？",
            "请给新人一些建议。",
            "你如何平衡工作和学习？",
            "在压力下你是如何工作的？",
            "你最喜欢工作中的哪个方面？",
            "你认为什么是成功的关键？",
            "请描述你的工作方法论。",
            "你如何处理复杂的问题？"
        ]
        
        turn_prompt = conversation_prompts[(turn - 1) % len(conversation_prompts)]
        
        turn_result = {
            'turn_number': turn,
            'prompt': turn_prompt,
            'response': '',
            'consistency_score': 0.0,
            'role_adherence': 0.0,
            'memory_retention': 0.0,
            'error': None
        }
        
        try:
            # 构建完整的对话上下文
            full_prompt = f"{role_prompt}\n\n用户: {turn_prompt}\n助手: "
            
            # 调用模型
            if self.model_manager:
                response = self.model_manager.call_model(
                    model_name,
                    full_prompt,
                    max_tokens=800,
                    timeout=180  # 3分钟超时
                )
            else:
                response = f"模拟响应 - 轮次{turn}"
            
            turn_result['response'] = response
            
            # 评估角色一致性
            role_keywords = self._extract_role_keywords(role_prompt)
            role_adherence = self._calculate_role_adherence(response, role_keywords)
            turn_result['role_adherence'] = role_adherence
            
            # 评估记忆保持（简化版）
            turn_result['memory_retention'] = 0.8  # 简化处理
            
            # 计算综合一致性得分
            turn_result['consistency_score'] = (
                role_adherence * 0.6 + 
                turn_result['memory_retention'] * 0.4
            )
            
        except Exception as e:
            logger.error(f"对话轮次执行失败: {e}")
            turn_result['error'] = str(e)
            turn_result['consistency_score'] = 0.0
        
        return turn_result
    
    def _extract_role_keywords(self, role_prompt: str) -> List[str]:
        """从角色提示中提取关键词"""
        # 简单的关键词提取
        keywords = []
        if 'software_engineer' in role_prompt.lower():
            keywords = ['代码', '编程', '开发', '技术', '软件', '系统']
        elif 'data_scientist' in role_prompt.lower():
            keywords = ['数据', '分析', '模型', '算法', '统计', '机器学习']
        elif 'product_manager' in role_prompt.lower():
            keywords = ['产品', '需求', '用户', '市场', '策略', '规划']
        else:
            keywords = ['专业', '经验', '技能', '知识']
        
        return keywords
    
    def _calculate_role_adherence(self, response: str, role_keywords: List[str]) -> float:
        """计算角色坚持度"""
        if not response or not role_keywords:
            return 0.0
        
        keyword_count = sum(1 for keyword in role_keywords if keyword in response)
        return min(1.0, keyword_count / len(role_keywords) * 2)
    
    def _calculate_memory_retention(self, response: str, 
                                  conversation_history: List[Dict]) -> float:
        """计算记忆保持度"""
        if not conversation_history:
            return 1.0
        
        # 简单的记忆检测：检查是否引用了之前的对话内容
        memory_indicators = 0
        total_checks = 0
        
        for prev_turn in conversation_history[-3:]:  # 检查最近3轮
            prev_response = prev_turn.get('response', '')
            if prev_response:
                total_checks += 1
                # 检查是否有相关性
                common_words = set(response.lower().split()) & set(prev_response.lower().split())
                if len(common_words) > 2:  # 有共同词汇
                    memory_indicators += 1
        
        if total_checks == 0:
            return 1.0
        
        return memory_indicators / total_checks

    def _test_memory_retention(self, model_name: str, role_prompt: str, turn: int) -> Dict[str, Any]:
        """测试记忆保持能力"""
        memory_result = {
            'turn': turn,
            'memory_tests': {},
            'overall_retention_score': 0.0,
            'context_awareness_score': 0.0
        }
        
        # 记忆测试场景
        memory_test_scenarios = {
            'personal_info': {
                'test_prompt': '请再次介绍一下你的专业背景。',
                'expected_elements': ['专业', '背景', '经验']
            },
            'previous_discussion': {
                'test_prompt': '基于我们之前的讨论，你有什么补充的吗？',
                'expected_elements': ['之前', '讨论', '补充']
            },
            'context_reference': {
                'test_prompt': '你刚才提到的那个观点能详细说明一下吗？',
                'expected_elements': ['刚才', '提到', '观点']
            }
        }
        
        for test_name, test_scenario in memory_test_scenarios.items():
            try:
                # 构建测试上下文
                test_prompt = test_scenario['test_prompt']
                full_context = f"{role_prompt}\n\n用户: {test_prompt}\n助手: "
                
                if self.model_manager:
                    test_response = self.model_manager.call_model(
                        model_name,
                        full_context,
                        max_tokens=400
                    )
                else:
                    test_response = f"记忆测试响应: {test_name}"
                
                # 分析记忆保持情况
                memory_analysis = self._analyze_memory_retention(
                    test_response, [], test_scenario['expected_elements']
                )
                
                memory_result['memory_tests'][test_name] = {
                    'test_prompt': test_prompt,
                    'response': test_response,
                    'memory_analysis': memory_analysis
                }
                
            except Exception as e:
                logger.error(f"记忆测试失败: {e}")
                memory_result['memory_tests'][test_name] = {
                    'test_prompt': test_scenario['test_prompt'],
                    'error': str(e),
                    'memory_analysis': {'retention_score': 0.0, 'context_awareness': 0.0}
                }
        
        # 计算总体记忆保持分数
        if memory_result['memory_tests']:
            retention_scores = []
            awareness_scores = []
            
            for test_result in memory_result['memory_tests'].values():
                analysis = test_result.get('memory_analysis', {})
                retention_scores.append(analysis.get('retention_score', 0.0))
                awareness_scores.append(analysis.get('context_awareness', 0.0))
            
            memory_result['overall_retention_score'] = sum(retention_scores) / len(retention_scores)
            memory_result['context_awareness_score'] = sum(awareness_scores) / len(awareness_scores)
        
        return memory_result











