"""
共识分析器

分析多个智能体之间的观点一致性、分歧程度和共识形成过程，
评估集体决策的质量和多样性价值。
"""

import json
import numpy as np
import logging
from typing import Dict, List, Any, Optional, Tuple, Set
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from collections import defaultdict, Counter
import hashlib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import re


@dataclass
class AgentOpinion:
    """智能体观点"""
    agent_id: str
    opinion_text: str
    confidence: float
    reasoning: List[str]
    key_points: List[str]
    stance: str  # 'support', 'oppose', 'neutral', 'mixed'
    timestamp: datetime
    context: str = ""
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'agent_id': self.agent_id,
            'opinion_text': self.opinion_text,
            'confidence': self.confidence,
            'reasoning': self.reasoning,
            'key_points': self.key_points,
            'stance': self.stance,
            'timestamp': self.timestamp.isoformat(),
            'context': self.context
        }


@dataclass
class ConsensusMetrics:
    """共识度量指标"""
    agreement_score: float  # 0-1, 整体一致性
    diversity_score: float  # 0-1, 观点多样性
    polarization_score: float  # 0-1, 极化程度
    convergence_trend: float  # -1到1, 收敛趋势
    quality_score: float  # 0-1, 共识质量
    participation_balance: float  # 0-1, 参与平衡度
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'agreement_score': self.agreement_score,
            'diversity_score': self.diversity_score,
            'polarization_score': self.polarization_score,
            'convergence_trend': self.convergence_trend,
            'quality_score': self.quality_score,
            'participation_balance': self.participation_balance
        }


@dataclass
class ConsensusAnalysis:
    """共识分析结果"""
    analysis_id: str
    topic: str
    agent_opinions: List[AgentOpinion]
    consensus_metrics: ConsensusMetrics
    dominant_viewpoints: List[Dict[str, Any]]
    minority_viewpoints: List[Dict[str, Any]]
    key_disagreements: List[str]
    convergence_points: List[str]
    recommendations: List[str]
    timestamp: datetime
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'analysis_id': self.analysis_id,
            'topic': self.topic,
            'agent_opinions': [op.to_dict() for op in self.agent_opinions],
            'consensus_metrics': self.consensus_metrics.to_dict(),
            'dominant_viewpoints': self.dominant_viewpoints,
            'minority_viewpoints': self.minority_viewpoints,
            'key_disagreements': self.key_disagreements,
            'convergence_points': self.convergence_points,
            'recommendations': self.recommendations,
            'timestamp': self.timestamp.isoformat()
        }


@dataclass
class ConsensusEvolution:
    """共识演化过程"""
    topic: str
    time_series: List[Tuple[datetime, ConsensusMetrics]]
    opinion_shifts: List[Dict[str, Any]]
    influence_network: Dict[str, List[str]]
    consensus_milestones: List[Dict[str, Any]]
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'topic': self.topic,
            'time_series': [(ts.isoformat(), metrics.to_dict()) for ts, metrics in self.time_series],
            'opinion_shifts': self.opinion_shifts,
            'influence_network': self.influence_network,
            'consensus_milestones': self.consensus_milestones
        }


class ConsensusAnalyzer:
    """共识分析器"""
    
    def __init__(self, data_dir: str = "cognitive_ecosystem/data"):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)
        
        # 分析历史
        self.analysis_history: List[ConsensusAnalysis] = []
        self.evolution_history: Dict[str, ConsensusEvolution] = {}
        
        # 观点聚类器
        self.vectorizer = TfidfVectorizer(
            max_features=1000,
            stop_words=None,  # 支持中文
            ngram_range=(1, 2)
        )
        
        # 设置日志
        self.logger = logging.getLogger(__name__)
        
        self.logger.info("共识分析器初始化完成")
    
    def analyze_consensus(self, topic: str, agent_opinions: List[Dict[str, Any]]) -> ConsensusAnalysis:
        """分析共识状态"""
        # 转换为AgentOpinion对象
        opinions = []
        for op_data in agent_opinions:
            opinion = AgentOpinion(
                agent_id=op_data['agent_id'],
                opinion_text=op_data['opinion_text'],
                confidence=op_data.get('confidence', 0.5),
                reasoning=op_data.get('reasoning', []),
                key_points=op_data.get('key_points', []),
                stance=op_data.get('stance', 'neutral'),
                timestamp=datetime.fromisoformat(op_data['timestamp']) if isinstance(op_data.get('timestamp'), str) else datetime.now(),
                context=op_data.get('context', '')
            )
            opinions.append(opinion)
        
        # 计算共识指标
        consensus_metrics = self._calculate_consensus_metrics(opinions)
        
        # 识别主导观点和少数观点
        dominant_viewpoints, minority_viewpoints = self._identify_viewpoint_clusters(opinions)
        
        # 识别关键分歧点
        key_disagreements = self._identify_key_disagreements(opinions)
        
        # 识别收敛点
        convergence_points = self._identify_convergence_points(opinions)
        
        # 生成建议
        recommendations = self._generate_consensus_recommendations(
            consensus_metrics, dominant_viewpoints, minority_viewpoints, key_disagreements
        )
        
        analysis = ConsensusAnalysis(
            analysis_id=self._generate_analysis_id(topic),
            topic=topic,
            agent_opinions=opinions,
            consensus_metrics=consensus_metrics,
            dominant_viewpoints=dominant_viewpoints,
            minority_viewpoints=minority_viewpoints,
            key_disagreements=key_disagreements,
            convergence_points=convergence_points,
            recommendations=recommendations,
            timestamp=datetime.now()
        )
        
        self.analysis_history.append(analysis)
        
        # 更新演化历史
        self._update_evolution_history(topic, consensus_metrics, opinions)
        
        return analysis
    
    def _calculate_consensus_metrics(self, opinions: List[AgentOpinion]) -> ConsensusMetrics:
        """计算共识指标"""
        if not opinions:
            return ConsensusMetrics(0, 0, 0, 0, 0, 0)
        
        # 计算语义相似性矩阵
        opinion_texts = [op.opinion_text for op in opinions]
        similarity_matrix = self._calculate_semantic_similarity(opinion_texts)
        
        # 1. 一致性得分 (Agreement Score)
        agreement_score = np.mean(similarity_matrix[np.triu_indices_from(similarity_matrix, k=1)])
        
        # 2. 多样性得分 (Diversity Score)
        diversity_score = 1.0 - agreement_score
        
        # 3. 极化程度 (Polarization Score)
        polarization_score = self._calculate_polarization(opinions, similarity_matrix)
        
        # 4. 收敛趋势 (Convergence Trend)
        convergence_trend = self._calculate_convergence_trend(opinions)
        
        # 5. 质量得分 (Quality Score)
        quality_score = self._calculate_consensus_quality(opinions, agreement_score)
        
        # 6. 参与平衡度 (Participation Balance)
        participation_balance = self._calculate_participation_balance(opinions)
        
        return ConsensusMetrics(
            agreement_score=float(agreement_score),
            diversity_score=float(diversity_score),
            polarization_score=float(polarization_score),
            convergence_trend=float(convergence_trend),
            quality_score=float(quality_score),
            participation_balance=float(participation_balance)
        )
    
    def _calculate_semantic_similarity(self, texts: List[str]) -> np.ndarray:
        """计算语义相似性矩阵"""
        try:
            # 使用TF-IDF向量化
            tfidf_matrix = self.vectorizer.fit_transform(texts)
            
            # 计算余弦相似性
            similarity_matrix = cosine_similarity(tfidf_matrix)
            
            return similarity_matrix
        except Exception as e:
            self.logger.warning(f"语义相似性计算失败: {e}")
            # 返回单位矩阵作为后备
            n = len(texts)
            return np.eye(n)
    
    def _calculate_polarization(self, opinions: List[AgentOpinion], 
                              similarity_matrix: np.ndarray) -> float:
        """计算极化程度"""
        if len(opinions) < 2:
            return 0.0
        
        # 基于立场的极化分析
        stance_counts = Counter([op.stance for op in opinions])
        
        # 如果只有一种立场，极化程度为0
        if len(stance_counts) <= 1:
            return 0.0
        
        # 计算立场分布的不平衡程度
        total_opinions = len(opinions)
        stance_proportions = [count / total_opinions for count in stance_counts.values()]
        
        # 使用基尼系数衡量不平衡程度
        gini_coefficient = self._calculate_gini_coefficient(stance_proportions)
        
        # 结合语义相似性
        avg_similarity = np.mean(similarity_matrix[np.triu_indices_from(similarity_matrix, k=1)])
        semantic_polarization = 1.0 - avg_similarity
        
        # 综合极化得分
        polarization = (gini_coefficient * 0.6 + semantic_polarization * 0.4)
        
        return min(1.0, polarization)
    
    def _calculate_gini_coefficient(self, proportions: List[float]) -> float:
        """计算基尼系数"""
        if not proportions:
            return 0.0
        
        proportions = sorted(proportions)
        n = len(proportions)
        cumsum = np.cumsum(proportions)
        
        return (n + 1 - 2 * np.sum(cumsum)) / (n * np.sum(proportions))
    
    def _calculate_convergence_trend(self, opinions: List[AgentOpinion]) -> float:
        """计算收敛趋势"""
        if len(opinions) < 2:
            return 0.0
        
        # 按时间排序
        sorted_opinions = sorted(opinions, key=lambda x: x.timestamp)
        
        # 计算时间窗口内的相似性变化
        window_size = min(5, len(sorted_opinions) // 2)
        if window_size < 2:
            return 0.0
        
        early_opinions = sorted_opinions[:window_size]
        late_opinions = sorted_opinions[-window_size:]
        
        # 计算早期和晚期的内部相似性
        early_texts = [op.opinion_text for op in early_opinions]
        late_texts = [op.opinion_text for op in late_opinions]
        
        try:
            early_similarity = np.mean(self._calculate_semantic_similarity(early_texts))
            late_similarity = np.mean(self._calculate_semantic_similarity(late_texts))
            
            # 收敛趋势 = 晚期相似性 - 早期相似性
            convergence_trend = late_similarity - early_similarity
            
            return np.clip(convergence_trend, -1.0, 1.0)
        except:
            return 0.0
    
    def _calculate_consensus_quality(self, opinions: List[AgentOpinion], 
                                   agreement_score: float) -> float:
        """计算共识质量"""
        if not opinions:
            return 0.0
        
        # 质量因子
        quality_factors = []
        
        # 1. 推理深度
        avg_reasoning_depth = np.mean([len(op.reasoning) for op in opinions])
        reasoning_quality = min(1.0, avg_reasoning_depth / 5.0)  # 假设5个推理步骤为满分
        quality_factors.append(reasoning_quality * 0.3)
        
        # 2. 置信度分布
        confidences = [op.confidence for op in opinions]
        avg_confidence = np.mean(confidences)
        confidence_std = np.std(confidences)
        
        # 高平均置信度，低标准差表示高质量
        confidence_quality = avg_confidence * (1.0 - confidence_std)
        quality_factors.append(confidence_quality * 0.3)
        
        # 3. 关键点覆盖度
        all_key_points = set()
        for op in opinions:
            all_key_points.update(op.key_points)
        
        if all_key_points:
            avg_key_points = np.mean([len(op.key_points) for op in opinions])
            coverage_quality = min(1.0, avg_key_points / len(all_key_points))
            quality_factors.append(coverage_quality * 0.2)
        
        # 4. 一致性贡献
        quality_factors.append(agreement_score * 0.2)
        
        return sum(quality_factors)
    
    def _calculate_participation_balance(self, opinions: List[AgentOpinion]) -> float:
        """计算参与平衡度"""
        if not opinions:
            return 0.0
        
        # 统计每个智能体的参与度
        agent_participation = Counter([op.agent_id for op in opinions])
        participation_counts = list(agent_participation.values())
        
        if len(participation_counts) <= 1:
            return 1.0
        
        # 使用基尼系数的逆来衡量平衡度
        gini = self._calculate_gini_coefficient(participation_counts)
        balance = 1.0 - gini
        
        return balance
    
    def _identify_viewpoint_clusters(self, opinions: List[AgentOpinion]) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
        """识别观点聚类"""
        if not opinions:
            return [], []
        
        # 按立场分组
        stance_groups = defaultdict(list)
        for op in opinions:
            stance_groups[op.stance].append(op)
        
        # 计算每个立场的支持度
        total_opinions = len(opinions)
        viewpoint_stats = []
        
        for stance, stance_opinions in stance_groups.items():
            support_rate = len(stance_opinions) / total_opinions
            avg_confidence = np.mean([op.confidence for op in stance_opinions])
            
            # 提取代表性观点
            representative_opinion = max(stance_opinions, key=lambda x: x.confidence)
            
            # 提取共同关键点
            all_key_points = []
            for op in stance_opinions:
                all_key_points.extend(op.key_points)
            common_key_points = [point for point, count in Counter(all_key_points).most_common(5)]
            
            viewpoint_stats.append({
                'stance': stance,
                'support_rate': support_rate,
                'avg_confidence': avg_confidence,
                'agent_count': len(stance_opinions),
                'representative_opinion': representative_opinion.opinion_text,
                'representative_agent': representative_opinion.agent_id,
                'common_key_points': common_key_points,
                'agents': [op.agent_id for op in stance_opinions]
            })
        
        # 按支持率排序
        viewpoint_stats.sort(key=lambda x: x['support_rate'], reverse=True)
        
        # 区分主导观点和少数观点
        threshold = 0.3  # 30%以上为主导观点
        dominant_viewpoints = [vp for vp in viewpoint_stats if vp['support_rate'] >= threshold]
        minority_viewpoints = [vp for vp in viewpoint_stats if vp['support_rate'] < threshold]
        
        return dominant_viewpoints, minority_viewpoints
    
    def _identify_key_disagreements(self, opinions: List[AgentOpinion]) -> List[str]:
        """识别关键分歧点"""
        disagreements = []
        
        # 收集所有关键点
        all_key_points = []
        for op in opinions:
            all_key_points.extend(op.key_points)
        
        key_point_counter = Counter(all_key_points)
        
        # 识别有争议的关键点
        for key_point, count in key_point_counter.items():
            if count >= 2:  # 至少被2个智能体提及
                # 检查对此关键点的不同立场
                supporting_agents = []
                opposing_agents = []
                
                for op in opinions:
                    if key_point in op.key_points:
                        if op.stance in ['support']:
                            supporting_agents.append(op.agent_id)
                        elif op.stance in ['oppose']:
                            opposing_agents.append(op.agent_id)
                
                # 如果存在明显分歧
                if supporting_agents and opposing_agents:
                    disagreement = f"关于'{key_point}'存在分歧：支持方({len(supporting_agents)}个智能体) vs 反对方({len(opposing_agents)}个智能体)"
                    disagreements.append(disagreement)
        
        # 基于语义相似性识别分歧
        opinion_texts = [op.opinion_text for op in opinions]
        if len(opinion_texts) >= 2:
            similarity_matrix = self._calculate_semantic_similarity(opinion_texts)
            
            # 找出相似性最低的观点对
            n = len(opinions)
            min_similarity = float('inf')
            most_disagreed_pair = None
            
            for i in range(n):
                for j in range(i + 1, n):
                    if similarity_matrix[i][j] < min_similarity:
                        min_similarity = similarity_matrix[i][j]
                        most_disagreed_pair = (i, j)
            
            if most_disagreed_pair and min_similarity < 0.3:  # 相似性低于30%
                i, j = most_disagreed_pair
                disagreement = f"智能体{opinions[i].agent_id}和{opinions[j].agent_id}的观点存在根本性分歧 (相似性: {min_similarity:.2f})"
                disagreements.append(disagreement)
        
        return disagreements[:10]  # 返回最多10个关键分歧
    
    def _identify_convergence_points(self, opinions: List[AgentOpinion]) -> List[str]:
        """识别收敛点"""
        convergence_points = []
        
        # 收集所有关键点
        all_key_points = []
        for op in opinions:
            all_key_points.extend(op.key_points)
        
        key_point_counter = Counter(all_key_points)
        
        # 识别高度一致的关键点
        total_agents = len(set(op.agent_id for op in opinions))
        
        for key_point, count in key_point_counter.most_common():
            agreement_rate = count / total_agents
            if agreement_rate >= 0.7:  # 70%以上的智能体同意
                convergence_points.append(f"'{key_point}' (一致性: {agreement_rate:.1%})")
        
        # 识别共同推理模式
        all_reasoning = []
        for op in opinions:
            all_reasoning.extend(op.reasoning)
        
        reasoning_counter = Counter(all_reasoning)
        for reasoning, count in reasoning_counter.most_common(5):
            if count >= max(2, total_agents * 0.5):  # 至少一半智能体使用相似推理
                convergence_points.append(f"共同推理: '{reasoning}' (使用率: {count}/{total_agents})")
        
        return convergence_points[:10]  # 返回最多10个收敛点
    
    def _generate_consensus_recommendations(self, metrics: ConsensusMetrics,
                                          dominant_viewpoints: List[Dict[str, Any]],
                                          minority_viewpoints: List[Dict[str, Any]],
                                          key_disagreements: List[str]) -> List[str]:
        """生成共识建议"""
        recommendations = []
        
        # 基于一致性得分的建议
        if metrics.agreement_score < 0.3:
            recommendations.append("共识度较低，建议进行更深入的讨论和信息交换")
        elif metrics.agreement_score > 0.8:
            recommendations.append("共识度很高，可以考虑进入决策阶段")
        
        # 基于多样性得分的建议
        if metrics.diversity_score < 0.2:
            recommendations.append("观点多样性不足，建议引入更多不同视角")
        elif metrics.diversity_score > 0.8:
            recommendations.append("观点过于分散，建议寻找共同点进行整合")
        
        # 基于极化程度的建议
        if metrics.polarization_score > 0.7:
            recommendations.append("存在严重极化，建议采用调解机制缓解对立")
        
        # 基于收敛趋势的建议
        if metrics.convergence_trend < -0.3:
            recommendations.append("观点正在分化，建议重新审视讨论方向")
        elif metrics.convergence_trend > 0.3:
            recommendations.append("观点正在收敛，这是积极的趋势")
        
        # 基于参与平衡度的建议
        if metrics.participation_balance < 0.5:
            recommendations.append("参与不平衡，建议鼓励沉默的智能体表达观点")
        
        # 基于主导观点的建议
        if len(dominant_viewpoints) == 1 and dominant_viewpoints[0]['support_rate'] > 0.8:
            recommendations.append("存在压倒性主导观点，建议确保少数意见得到充分考虑")
        
        # 基于分歧的建议
        if len(key_disagreements) > 5:
            recommendations.append("分歧点较多，建议逐一解决关键争议")
        
        # 基于质量得分的建议
        if metrics.quality_score < 0.5:
            recommendations.append("共识质量有待提高，建议加强论证和证据支持")
        
        return recommendations
    
    def track_consensus_evolution(self, topic: str, time_window_days: int = 30) -> Optional[ConsensusEvolution]:
        """跟踪共识演化过程"""
        if topic not in self.evolution_history:
            return None
        
        evolution = self.evolution_history[topic]
        
        # 过滤时间窗口
        cutoff_time = datetime.now().timestamp() - (time_window_days * 24 * 3600)
        filtered_time_series = [
            (ts, metrics) for ts, metrics in evolution.time_series
            if ts.timestamp() > cutoff_time
        ]
        
        if not filtered_time_series:
            return None
        
        # 更新演化数据
        evolution.time_series = filtered_time_series
        
        return evolution
    
    def _update_evolution_history(self, topic: str, metrics: ConsensusMetrics, 
                                opinions: List[AgentOpinion]):
        """更新演化历史"""
        if topic not in self.evolution_history:
            self.evolution_history[topic] = ConsensusEvolution(
                topic=topic,
                time_series=[],
                opinion_shifts=[],
                influence_network={},
                consensus_milestones=[]
            )
        
        evolution = self.evolution_history[topic]
        current_time = datetime.now()
        
        # 添加时间序列数据
        evolution.time_series.append((current_time, metrics))
        
        # 检测观点转变
        self._detect_opinion_shifts(evolution, opinions)
        
        # 更新影响网络
        self._update_influence_network(evolution, opinions)
        
        # 检测共识里程碑
        self._detect_consensus_milestones(evolution, metrics)
        
        # 保持历史记录大小
        if len(evolution.time_series) > 100:
            evolution.time_series = evolution.time_series[-100:]
    
    def _detect_opinion_shifts(self, evolution: ConsensusEvolution, 
                             opinions: List[AgentOpinion]):
        """检测观点转变"""
        # 简化实现：检测立场变化
        current_stances = {op.agent_id: op.stance for op in opinions}
        
        # 与历史记录比较（这里简化处理）
        if len(evolution.opinion_shifts) > 0:
            last_shift = evolution.opinion_shifts[-1]
            last_stances = last_shift.get('stances', {})
            
            for agent_id, current_stance in current_stances.items():
                if agent_id in last_stances and last_stances[agent_id] != current_stance:
                    shift = {
                        'agent_id': agent_id,
                        'from_stance': last_stances[agent_id],
                        'to_stance': current_stance,
                        'timestamp': datetime.now().isoformat()
                    }
                    evolution.opinion_shifts.append(shift)
        
        # 记录当前状态
        evolution.opinion_shifts.append({
            'stances': current_stances,
            'timestamp': datetime.now().isoformat()
        })
    
    def _update_influence_network(self, evolution: ConsensusEvolution, 
                                opinions: List[AgentOpinion]):
        """更新影响网络"""
        # 简化实现：基于观点相似性构建影响网络
        agent_ids = [op.agent_id for op in opinions]
        opinion_texts = [op.opinion_text for op in opinions]
        
        if len(opinion_texts) >= 2:
            similarity_matrix = self._calculate_semantic_similarity(opinion_texts)
            
            # 构建影响关系
            for i, agent_i in enumerate(agent_ids):
                influences = []
                for j, agent_j in enumerate(agent_ids):
                    if i != j and similarity_matrix[i][j] > 0.7:  # 高相似性表示可能的影响
                        influences.append(agent_j)
                
                evolution.influence_network[agent_i] = influences
    
    def _detect_consensus_milestones(self, evolution: ConsensusEvolution, 
                                   metrics: ConsensusMetrics):
        """检测共识里程碑"""
        current_time = datetime.now()
        
        # 检测高共识里程碑
        if metrics.agreement_score > 0.8:
            milestone = {
                'type': 'high_consensus',
                'description': f'达到高共识水平 (一致性: {metrics.agreement_score:.2f})',
                'timestamp': current_time.isoformat(),
                'metrics': metrics.to_dict()
            }
            evolution.consensus_milestones.append(milestone)
        
        # 检测收敛里程碑
        if metrics.convergence_trend > 0.5:
            milestone = {
                'type': 'strong_convergence',
                'description': f'观点强烈收敛 (收敛趋势: {metrics.convergence_trend:.2f})',
                'timestamp': current_time.isoformat(),
                'metrics': metrics.to_dict()
            }
            evolution.consensus_milestones.append(milestone)
        
        # 检测极化里程碑
        if metrics.polarization_score > 0.8:
            milestone = {
                'type': 'high_polarization',
                'description': f'出现严重极化 (极化程度: {metrics.polarization_score:.2f})',
                'timestamp': current_time.isoformat(),
                'metrics': metrics.to_dict()
            }
            evolution.consensus_milestones.append(milestone)
    
    def compare_consensus_across_topics(self, topics: List[str]) -> Dict[str, Any]:
        """比较不同主题的共识状态"""
        topic_analyses = {}
        
        for topic in topics:
            # 获取该主题的最新分析
            topic_analyses_list = [a for a in self.analysis_history if a.topic == topic]
            if topic_analyses_list:
                latest_analysis = max(topic_analyses_list, key=lambda x: x.timestamp)
                topic_analyses[topic] = latest_analysis
        
        if not topic_analyses:
            return {'error': '没有找到相关主题的分析数据'}
        
        # 计算比较统计
        metrics_comparison = {}
        for metric_name in ['agreement_score', 'diversity_score', 'polarization_score', 
                          'convergence_trend', 'quality_score', 'participation_balance']:
            values = [getattr(analysis.consensus_metrics, metric_name) 
                     for analysis in topic_analyses.values()]
            metrics_comparison[metric_name] = {
                'average': np.mean(values),
                'max': max(values),
                'min': min(values),
                'std': np.std(values)
            }
        
        # 识别最佳和最差主题
        best_topic = max(topic_analyses.keys(), 
                        key=lambda t: topic_analyses[t].consensus_metrics.quality_score)
        worst_topic = min(topic_analyses.keys(), 
                         key=lambda t: topic_analyses[t].consensus_metrics.quality_score)
        
        return {
            'topic_analyses': {topic: analysis.to_dict() for topic, analysis in topic_analyses.items()},
            'metrics_comparison': metrics_comparison,
            'best_consensus_topic': best_topic,
            'worst_consensus_topic': worst_topic,
            'total_topics': len(topic_analyses),
            'comparison_timestamp': datetime.now().isoformat()
        }
    
    def _generate_analysis_id(self, topic: str) -> str:
        """生成分析ID"""
        timestamp = datetime.now().isoformat()
        content = f"consensus_{topic}_{timestamp}"
        return hashlib.md5(content.encode()).hexdigest()[:12]
    
    def get_consensus_statistics(self, topic: Optional[str] = None) -> Dict[str, Any]:
        """获取共识统计信息"""
        if topic:
            analyses = [a for a in self.analysis_history if a.topic == topic]
        else:
            analyses = self.analysis_history
        
        if not analyses:
            return {'total_analyses': 0}
        
        # 计算统计指标
        agreement_scores = [a.consensus_metrics.agreement_score for a in analyses]
        diversity_scores = [a.consensus_metrics.diversity_score for a in analyses]
        quality_scores = [a.consensus_metrics.quality_score for a in analyses]
        
        return {
            'total_analyses': len(analyses),
            'average_agreement': np.mean(agreement_scores),
            'average_diversity': np.mean(diversity_scores),
            'average_quality': np.mean(quality_scores),
            'best_consensus_score': max(agreement_scores),
            'topics_analyzed': len(set(a.topic for a in analyses)),
            'recent_analyses': len([a for a in analyses 
                                  if (datetime.now() - a.timestamp).days <= 7])
        }
    
    def export_consensus_analysis(self, output_file: str, topic: Optional[str] = None):
        """导出共识分析结果"""
        if topic:
            analyses = [a.to_dict() for a in self.analysis_history if a.topic == topic]
            evolution = self.evolution_history.get(topic)
        else:
            analyses = [a.to_dict() for a in self.analysis_history]
            evolution = {t: e.to_dict() for t, e in self.evolution_history.items()}
        
        export_data = {
            'consensus_analyses': analyses,
            'evolution_history': evolution.to_dict() if isinstance(evolution, ConsensusEvolution) else evolution,
            'statistics': self.get_consensus_statistics(topic),
            'export_timestamp': datetime.now().isoformat()
        }
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(export_data, f, ensure_ascii=False, indent=2)
        
        self.logger.info(f"共识分析结果已导出到: {output_file}")