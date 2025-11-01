"""
认知生态位分析模块

定义和分析每个智能体在认知空间中的独特位置，
包括认知风格、专业领域、思维模式等多维度特征。
"""

import numpy as np
from typing import Dict, List, Any, Optional, Tuple, Set
from dataclasses import dataclass, field
from datetime import datetime
import json
from enum import Enum


class CognitiveStyle(Enum):
    """认知风格枚举"""
    ANALYTICAL = "analytical"          # 分析型
    CREATIVE = "creative"             # 创造型
    PRACTICAL = "practical"           # 实用型
    SYSTEMATIC = "systematic"         # 系统型
    INTUITIVE = "intuitive"           # 直觉型
    COLLABORATIVE = "collaborative"   # 协作型
    CRITICAL = "critical"             # 批判型
    BALANCED = "balanced"             # 平衡型


class KnowledgeDomain(Enum):
    """知识领域枚举"""
    TECHNOLOGY = "technology"
    BUSINESS = "business"
    SCIENCE = "science"
    ARTS = "arts"
    SOCIAL = "social"
    MATHEMATICS = "mathematics"
    LANGUAGE = "language"
    PHILOSOPHY = "philosophy"


@dataclass
class CognitiveVector:
    """认知向量 - 表示智能体在多维认知空间中的位置"""
    analytical_thinking: float = 0.5      # 分析思维能力
    creative_thinking: float = 0.5        # 创造思维能力
    logical_reasoning: float = 0.5        # 逻辑推理能力
    emotional_intelligence: float = 0.5   # 情感智能
    pattern_recognition: float = 0.5      # 模式识别能力
    abstract_thinking: float = 0.5        # 抽象思维能力
    practical_application: float = 0.5    # 实践应用能力
    collaborative_tendency: float = 0.5   # 协作倾向
    risk_tolerance: float = 0.5           # 风险容忍度
    innovation_drive: float = 0.5         # 创新驱动力
    
    def to_array(self) -> np.ndarray:
        """转换为numpy数组"""
        return np.array([
            self.analytical_thinking, self.creative_thinking,
            self.logical_reasoning, self.emotional_intelligence,
            self.pattern_recognition, self.abstract_thinking,
            self.practical_application, self.collaborative_tendency,
            self.risk_tolerance, self.innovation_drive
        ])
    
    def distance_to(self, other: 'CognitiveVector') -> float:
        """计算与另一个认知向量的欧几里得距离"""
        return np.linalg.norm(self.to_array() - other.to_array())
    
    def similarity_to(self, other: 'CognitiveVector') -> float:
        """计算与另一个认知向量的相似度 (0-1)"""
        distance = self.distance_to(other)
        max_distance = np.sqrt(10)  # 10维空间的最大距离
        return 1.0 - (distance / max_distance)


@dataclass
class NicheMetrics:
    """生态位指标"""
    specialization_index: float = 0.0     # 专业化指数
    adaptability_score: float = 0.0       # 适应性得分
    uniqueness_factor: float = 0.0        # 独特性因子
    collaboration_potential: float = 0.0   # 协作潜力
    niche_breadth: float = 0.0            # 生态位宽度
    niche_overlap: Dict[str, float] = field(default_factory=dict)  # 与其他智能体的重叠度


class CognitiveNiche:
    """认知生态位类"""
    
    def __init__(self, agent_id: str, role: str, cognitive_style: str, 
                 personality_traits: Dict[str, float]):
        self.agent_id = agent_id
        self.role = role
        self.cognitive_style = CognitiveStyle(cognitive_style)
        self.personality_traits = personality_traits
        
        # From plan: reasoning_patterns, value_orientations, problem_solving_styles
        self.reasoning_patterns: List[str] = []
        self.value_orientations: Dict[str, float] = {}
        self.problem_solving_styles: List[str] = []
        
        # 初始化认知向量
        self.cognitive_vector = self._initialize_cognitive_vector()
        
        # 知识领域
        self.knowledge_domains: Set[KnowledgeDomain] = self._determine_knowledge_domains()
        
        # 生态位指标
        self.metrics = NicheMetrics()
        
        # 历史记录
        self.interaction_history: List[Dict[str, Any]] = []
        self.performance_history: List[Dict[str, Any]] = []
        
        # 时间戳
        self.created_at = datetime.now()
        self.last_updated = datetime.now()
    
    def _initialize_cognitive_vector(self) -> CognitiveVector:
        """基于角色和认知风格初始化认知向量"""
        # 角色基础向量
        role_vectors = {
            'software_engineer': CognitiveVector(
                analytical_thinking=0.9, logical_reasoning=0.9,
                pattern_recognition=0.8, practical_application=0.8,
                creative_thinking=0.6, abstract_thinking=0.7
            ),
            'data_scientist': CognitiveVector(
                analytical_thinking=0.95, pattern_recognition=0.9,
                logical_reasoning=0.85, abstract_thinking=0.8,
                creative_thinking=0.7, practical_application=0.75
            ),
            'product_manager': CognitiveVector(
                collaborative_tendency=0.9, emotional_intelligence=0.8,
                practical_application=0.85, creative_thinking=0.75,
                analytical_thinking=0.7, innovation_drive=0.8
            ),
            'security_expert': CognitiveVector(
                analytical_thinking=0.9, logical_reasoning=0.9,
                risk_tolerance=0.3, pattern_recognition=0.85,
                practical_application=0.8, abstract_thinking=0.7
            ),
            'marketing_specialist': CognitiveVector(
                creative_thinking=0.9, emotional_intelligence=0.85,
                collaborative_tendency=0.8, innovation_drive=0.8,
                practical_application=0.75, analytical_thinking=0.6
            ),
            'financial_analyst': CognitiveVector(
                analytical_thinking=0.95, logical_reasoning=0.9,
                pattern_recognition=0.8, risk_tolerance=0.4,
                practical_application=0.8, abstract_thinking=0.7
            )
        }
        
        base_vector = role_vectors.get(self.role, CognitiveVector())
        
        # 根据认知风格调整
        style_adjustments = {
            CognitiveStyle.ANALYTICAL: {'analytical_thinking': 0.1, 'logical_reasoning': 0.1},
            CognitiveStyle.CREATIVE: {'creative_thinking': 0.15, 'innovation_drive': 0.1},
            CognitiveStyle.PRACTICAL: {'practical_application': 0.15, 'risk_tolerance': -0.05},
            CognitiveStyle.SYSTEMATIC: {'logical_reasoning': 0.1, 'pattern_recognition': 0.1},
            CognitiveStyle.INTUITIVE: {'emotional_intelligence': 0.1, 'abstract_thinking': 0.1},
            CognitiveStyle.COLLABORATIVE: {'collaborative_tendency': 0.15, 'emotional_intelligence': 0.1},
            CognitiveStyle.CRITICAL: {'analytical_thinking': 0.1, 'logical_reasoning': 0.1}
        }
        
        adjustments = style_adjustments.get(self.cognitive_style, {})
        for attr, adjustment in adjustments.items():
            current_value = getattr(base_vector, attr)
            setattr(base_vector, attr, min(1.0, max(0.0, current_value + adjustment)))
        
        # 根据个性特征微调
        for trait, value in self.personality_traits.items():
            if trait == 'openness' and value > 0.7:
                base_vector.creative_thinking = min(1.0, base_vector.creative_thinking + 0.1)
            elif trait == 'conscientiousness' and value > 0.7:
                base_vector.practical_application = min(1.0, base_vector.practical_application + 0.1)
            elif trait == 'extraversion' and value > 0.7:
                base_vector.collaborative_tendency = min(1.0, base_vector.collaborative_tendency + 0.1)
            elif trait == 'agreeableness' and value > 0.7:
                base_vector.emotional_intelligence = min(1.0, base_vector.emotional_intelligence + 0.1)
            elif trait == 'neuroticism' and value > 0.7:
                base_vector.risk_tolerance = max(0.0, base_vector.risk_tolerance - 0.1)
        
        return base_vector
    
    def _determine_knowledge_domains(self) -> Set[KnowledgeDomain]:
        """根据角色确定知识领域"""
        role_domains = {
            'software_engineer': {KnowledgeDomain.TECHNOLOGY, KnowledgeDomain.MATHEMATICS},
            'data_scientist': {KnowledgeDomain.TECHNOLOGY, KnowledgeDomain.MATHEMATICS, KnowledgeDomain.SCIENCE},
            'product_manager': {KnowledgeDomain.BUSINESS, KnowledgeDomain.TECHNOLOGY, KnowledgeDomain.SOCIAL},
            'security_expert': {KnowledgeDomain.TECHNOLOGY, KnowledgeDomain.BUSINESS},
            'marketing_specialist': {KnowledgeDomain.BUSINESS, KnowledgeDomain.SOCIAL, KnowledgeDomain.ARTS},
            'financial_analyst': {KnowledgeDomain.BUSINESS, KnowledgeDomain.MATHEMATICS}
        }
        
        return role_domains.get(self.role, {KnowledgeDomain.BUSINESS})
    
    def calculate_specialization_index(self) -> float:
        """计算专业化指数 - 衡量智能体在特定领域的专精程度"""
        vector_array = self.cognitive_vector.to_array()
        
        # 计算向量的标准差，标准差越大说明越专业化
        std_dev = np.std(vector_array)
        
        # 归一化到0-1范围
        max_std = np.sqrt(0.25)  # 理论最大标准差
        specialization = std_dev / max_std
        
        self.metrics.specialization_index = min(1.0, specialization)
        return self.metrics.specialization_index
    
    def calculate_adaptability_score(self) -> float:
        """计算适应性得分 - 衡量智能体适应不同任务的能力"""
        vector_array = self.cognitive_vector.to_array()
        
        # 适应性与各维度的平衡性相关
        mean_value = np.mean(vector_array)
        variance = np.var(vector_array)
        
        # 高均值、低方差表示高适应性
        adaptability = mean_value * (1 - variance)
        
        self.metrics.adaptability_score = max(0.0, min(1.0, adaptability))
        return self.metrics.adaptability_score
    
    def calculate_uniqueness_factor(self, other_niches: List['CognitiveNiche']) -> float:
        """计算独特性因子 - 衡量与其他智能体的差异程度"""
        if not other_niches:
            self.metrics.uniqueness_factor = 1.0
            return 1.0
        
        similarities = []
        for other_niche in other_niches:
            if other_niche.agent_id != self.agent_id:
                similarity = self.cognitive_vector.similarity_to(other_niche.cognitive_vector)
                similarities.append(similarity)
        
        if similarities:
            avg_similarity = np.mean(similarities)
            uniqueness = 1.0 - avg_similarity
        else:
            uniqueness = 1.0
        
        self.metrics.uniqueness_factor = max(0.0, min(1.0, uniqueness))
        return self.metrics.uniqueness_factor
    
    def calculate_collaboration_potential(self, target_niche: 'CognitiveNiche') -> float:
        """计算与目标智能体的协作潜力"""
        # 协作潜力基于互补性而非相似性
        my_vector = self.cognitive_vector.to_array()
        target_vector = target_niche.cognitive_vector.to_array()
        
        # 计算互补性：在某些维度上的差异可以带来协作优势
        complementarity = 0.0
        
        # 检查关键互补维度
        complementary_pairs = [
            ('analytical_thinking', 'creative_thinking'),
            ('logical_reasoning', 'emotional_intelligence'),
            ('practical_application', 'abstract_thinking'),
            ('risk_tolerance', 'innovation_drive')
        ]
        
        vector_dict = {
            'analytical_thinking': 0, 'creative_thinking': 1,
            'logical_reasoning': 2, 'emotional_intelligence': 3,
            'pattern_recognition': 4, 'abstract_thinking': 5,
            'practical_application': 6, 'collaborative_tendency': 7,
            'risk_tolerance': 8, 'innovation_drive': 9
        }
        
        for dim1, dim2 in complementary_pairs:
            idx1, idx2 = vector_dict[dim1], vector_dict[dim2]
            # 如果一方在dim1强而dim2弱，另一方相反，则互补性高
            complementarity += abs((my_vector[idx1] - my_vector[idx2]) - 
                                 (target_vector[idx1] - target_vector[idx2]))
        
        # 归一化
        max_complementarity = len(complementary_pairs) * 2.0
        collaboration_potential = complementarity / max_complementarity
        
        return min(1.0, collaboration_potential)
    
    def calculate_niche_breadth(self) -> float:
        """计算生态位宽度 - 衡量智能体能力的广度"""
        vector_array = self.cognitive_vector.to_array()
        
        # 生态位宽度与能力的均匀分布相关
        # 使用熵的概念：分布越均匀，熵越大，宽度越大
        
        # 将能力值转换为概率分布
        probabilities = vector_array / np.sum(vector_array)
        
        # 计算熵
        entropy = -np.sum(probabilities * np.log2(probabilities + 1e-10))
        
        # 归一化到0-1范围
        max_entropy = np.log2(len(vector_array))
        breadth = entropy / max_entropy
        
        self.metrics.niche_breadth = breadth
        return breadth
    
    def calculate_niche_overlap(self, other_niche: 'CognitiveNiche') -> float:
        """计算与另一个生态位的重叠度"""
        # 基于认知向量的相似性
        cognitive_similarity = self.cognitive_vector.similarity_to(other_niche.cognitive_vector)
        
        # 基于知识领域的重叠
        domain_overlap = len(self.knowledge_domains & other_niche.knowledge_domains) / \
                        len(self.knowledge_domains | other_niche.knowledge_domains)
        
        # 综合重叠度
        total_overlap = (cognitive_similarity * 0.7 + domain_overlap * 0.3)
        
        # 更新重叠度记录
        self.metrics.niche_overlap[other_niche.agent_id] = total_overlap
        
        return total_overlap
    
    def update_metrics(self, other_niches: List['CognitiveNiche']):
        """更新所有生态位指标"""
        self.calculate_specialization_index()
        self.calculate_adaptability_score()
        self.calculate_uniqueness_factor(other_niches)
        self.calculate_niche_breadth()
        
        # 计算与所有其他生态位的重叠度
        for other_niche in other_niches:
            if other_niche.agent_id != self.agent_id:
                self.calculate_niche_overlap(other_niche)
        
        self.last_updated = datetime.now()
    
    def record_interaction(self, interaction_data: Dict[str, Any]):
        """记录交互历史"""
        interaction_record = {
            'timestamp': datetime.now().isoformat(),
            'data': interaction_data
        }
        self.interaction_history.append(interaction_record)
        
        # 保持历史记录在合理范围内
        if len(self.interaction_history) > 100:
            self.interaction_history = self.interaction_history[-100:]
    
    def record_performance(self, performance_data: Dict[str, Any]):
        """记录性能历史"""
        performance_record = {
            'timestamp': datetime.now().isoformat(),
            'data': performance_data
        }
        self.performance_history.append(performance_record)
        
        # 保持历史记录在合理范围内
        if len(self.performance_history) > 50:
            self.performance_history = self.performance_history[-50:]
    
    def get_niche_summary(self) -> Dict[str, Any]:
        """获取生态位摘要信息"""
        return {
            'agent_id': self.agent_id,
            'role': self.role,
            'cognitive_style': self.cognitive_style.value,
            'knowledge_domains': [domain.value for domain in self.knowledge_domains],
            'cognitive_vector': {
                'analytical_thinking': self.cognitive_vector.analytical_thinking,
                'creative_thinking': self.cognitive_vector.creative_thinking,
                'logical_reasoning': self.cognitive_vector.logical_reasoning,
                'emotional_intelligence': self.cognitive_vector.emotional_intelligence,
                'practical_application': self.cognitive_vector.practical_application,
                'collaborative_tendency': self.cognitive_vector.collaborative_tendency
            },
            'metrics': {
                'specialization_index': self.metrics.specialization_index,
                'adaptability_score': self.metrics.adaptability_score,
                'uniqueness_factor': self.metrics.uniqueness_factor,
                'niche_breadth': self.metrics.niche_breadth,
                'collaboration_potential': self.metrics.collaboration_potential
            },
            'interaction_count': len(self.interaction_history),
            'performance_records': len(self.performance_history),
            'created_at': self.created_at.isoformat(),
            'last_updated': self.last_updated.isoformat()
        }
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典格式"""
        return {
            'agent_id': self.agent_id,
            'role': self.role,
            'cognitive_style': self.cognitive_style.value,
            'personality_traits': self.personality_traits,
            'knowledge_domains': [domain.value for domain in self.knowledge_domains],
            'cognitive_vector': {
                'analytical_thinking': self.cognitive_vector.analytical_thinking,
                'creative_thinking': self.cognitive_vector.creative_thinking,
                'logical_reasoning': self.cognitive_vector.logical_reasoning,
                'emotional_intelligence': self.cognitive_vector.emotional_intelligence,
                'pattern_recognition': self.cognitive_vector.pattern_recognition,
                'abstract_thinking': self.cognitive_vector.abstract_thinking,
                'practical_application': self.cognitive_vector.practical_application,
                'collaborative_tendency': self.cognitive_vector.collaborative_tendency,
                'risk_tolerance': self.cognitive_vector.risk_tolerance,
                'innovation_drive': self.cognitive_vector.innovation_drive
            },
            'metrics': {
                'specialization_index': self.metrics.specialization_index,
                'adaptability_score': self.metrics.adaptability_score,
                'uniqueness_factor': self.metrics.uniqueness_factor,
                'collaboration_potential': self.metrics.collaboration_potential,
                'niche_breadth': self.metrics.niche_breadth,
                'niche_overlap': self.metrics.niche_overlap
            },
            'created_at': self.created_at.isoformat(),
            'last_updated': self.last_updated.isoformat()
        }

    def identify_unique_contributions(self, other_niches: List['CognitiveNiche']) -> Dict[str, Any]:
        """
        Identifies the unique contributions of this niche compared to others.
        This method provides a qualitative analysis of uniqueness.
        """
        if not other_niches:
            return {
                "uniqueness_factor": 1.0,
                "strongest_traits": ["all"],
                "least_overlapped_domains": list(self.knowledge_domains)
            }

        self.calculate_uniqueness_factor(other_niches)
        
        # Find strongest traits
        my_vector_dict = self.cognitive_vector.__dict__
        strongest_traits = sorted(my_vector_dict, key=my_vector_dict.get, reverse=True)[:3]

        # Find least overlapped knowledge domains
        all_other_domains = set()
        for other in other_niches:
            if other.agent_id != self.agent_id:
                all_other_domains.update(other.knowledge_domains)
        
        unique_domains = self.knowledge_domains - all_other_domains

        return {
            "uniqueness_factor": self.metrics.uniqueness_factor,
            "strongest_traits": strongest_traits,
            "least_overlapped_domains": [domain.value for domain in unique_domains]
        }
