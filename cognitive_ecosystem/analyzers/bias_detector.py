"""
偏见检测器

识别和分析智能体在决策和推理过程中可能存在的各种认知偏见，
包括确认偏见、锚定偏见、可得性偏见等多种类型。
"""

import json
import numpy as np
import logging
import re
from typing import Dict, List, Any, Optional, Tuple, Set
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from collections import defaultdict, Counter
import hashlib
from enum import Enum
import statistics
import math


class BiasType(Enum):
    """偏见类型"""
    CONFIRMATION = "confirmation"  # 确认偏见
    ANCHORING = "anchoring"  # 锚定偏见
    AVAILABILITY = "availability"  # 可得性偏见
    REPRESENTATIVENESS = "representativeness"  # 代表性偏见
    OVERCONFIDENCE = "overconfidence"  # 过度自信偏见
    FRAMING = "framing"  # 框架偏见
    SUNK_COST = "sunk_cost"  # 沉没成本偏见
    SURVIVORSHIP = "survivorship"  # 幸存者偏见
    ATTRIBUTION = "attribution"  # 归因偏见
    HALO_EFFECT = "halo_effect"  # 光环效应
    BANDWAGON = "bandwagon"  # 从众偏见
    LOSS_AVERSION = "loss_aversion"  # 损失厌恶
    RECENCY = "recency"  # 近因偏见
    PRIMACY = "primacy"  # 首因偏见
    HINDSIGHT = "hindsight"  # 后见之明偏见


class BiasSeverity(Enum):
    """偏见严重程度"""
    LOW = "low"
    MODERATE = "moderate"
    HIGH = "high"
    CRITICAL = "critical"


@dataclass
class BiasEvidence:
    """偏见证据"""
    evidence_id: str
    bias_type: BiasType
    description: str
    text_snippet: str
    confidence: float  # 0-1
    severity: BiasSeverity
    context: str
    reasoning: str
    timestamp: datetime
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'evidence_id': self.evidence_id,
            'bias_type': self.bias_type.value,
            'description': self.description,
            'text_snippet': self.text_snippet,
            'confidence': self.confidence,
            'severity': self.severity.value,
            'context': self.context,
            'reasoning': self.reasoning,
            'timestamp': self.timestamp.isoformat()
        }


@dataclass
class BiasDetectionResult:
    """偏见检测结果"""
    detection_id: str
    agent_id: str
    text_analyzed: str
    biases_detected: List[BiasEvidence]
    overall_bias_score: float  # 0-1
    bias_distribution: Dict[BiasType, float]
    risk_assessment: str
    recommendations: List[str]
    timestamp: datetime
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'detection_id': self.detection_id,
            'agent_id': self.agent_id,
            'text_analyzed': self.text_analyzed,
            'biases_detected': [bias.to_dict() for bias in self.biases_detected],
            'overall_bias_score': self.overall_bias_score,
            'bias_distribution': {bias.value: score for bias, score in self.bias_distribution.items()},
            'risk_assessment': self.risk_assessment,
            'recommendations': self.recommendations,
            'timestamp': self.timestamp.isoformat()
        }


@dataclass
class BiasProfile:
    """偏见档案"""
    agent_id: str
    bias_tendencies: Dict[BiasType, float]  # 各类偏见倾向
    historical_detections: List[str]  # 历史检测ID
    bias_evolution: Dict[str, List[float]]  # 偏见随时间的变化
    risk_level: str
    improvement_trend: float  # 改进趋势 (-1到1)
    last_updated: datetime
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'agent_id': self.agent_id,
            'bias_tendencies': {bias.value: tendency for bias, tendency in self.bias_tendencies.items()},
            'historical_detections': self.historical_detections,
            'bias_evolution': self.bias_evolution,
            'risk_level': self.risk_level,
            'improvement_trend': self.improvement_trend,
            'last_updated': self.last_updated.isoformat()
        }


@dataclass
class BiasComparison:
    """偏见比较结果"""
    comparison_id: str
    agents: List[str]
    bias_similarities: Dict[str, float]
    complementary_biases: Dict[str, List[BiasType]]
    collective_risk: float
    mitigation_strategies: List[str]
    timestamp: datetime
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'comparison_id': self.comparison_id,
            'agents': self.agents,
            'bias_similarities': self.bias_similarities,
            'complementary_biases': {
                agent: [bias.value for bias in biases] 
                for agent, biases in self.complementary_biases.items()
            },
            'collective_risk': self.collective_risk,
            'mitigation_strategies': self.mitigation_strategies,
            'timestamp': self.timestamp.isoformat()
        }


class BiasDetector:
    """偏见检测器"""
    
    def __init__(self, data_dir: str = "cognitive_ecosystem/data"):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)
        
        # 存储数据
        self.detection_results: List[BiasDetectionResult] = []
        self.bias_profiles: Dict[str, BiasProfile] = {}
        self.comparison_history: List[BiasComparison] = []
        
        # 偏见检测规则
        self.bias_patterns = self._initialize_bias_patterns()
        self.bias_keywords = self._initialize_bias_keywords()
        self.bias_indicators = self._initialize_bias_indicators()
        
        # 设置日志
        self.logger = logging.getLogger(__name__)
        
        self.logger.info("偏见检测器初始化完成")
    
    def _initialize_bias_patterns(self) -> Dict[BiasType, List[str]]:
        """初始化偏见模式"""
        return {
            BiasType.CONFIRMATION: [
                r"这证实了我的观点",
                r"正如我所预期的",
                r"这支持了我的假设",
                r"果然如此",
                r"我早就知道"
            ],
            BiasType.ANCHORING: [
                r"基于最初的.*",
                r"从.*开始考虑",
                r"第一印象.*",
                r"初始.*影响",
                r"起始点.*"
            ],
            BiasType.AVAILABILITY: [
                r"我记得.*",
                r"最近.*",
                r"经常听到.*",
                r"容易想到.*",
                r"印象深刻的.*"
            ],
            BiasType.OVERCONFIDENCE: [
                r"我确信.*",
                r"毫无疑问.*",
                r"绝对.*",
                r"100%确定",
                r"肯定.*"
            ],
            BiasType.FRAMING: [
                r"从.*角度看",
                r"换个说法.*",
                r"如果这样表述.*",
                r"重新定义.*",
                r"框架.*"
            ],
            BiasType.SUNK_COST: [
                r"已经投入.*",
                r"不能白费.*",
                r"既然开始了.*",
                r"投资.*不能浪费",
                r"沉没成本.*"
            ],
            BiasType.ATTRIBUTION: [
                r"他们.*是因为",
                r"我.*是由于",
                r"归因于.*",
                r"原因在于.*",
                r"责任.*"
            ],
            BiasType.HALO_EFFECT: [
                r"因为.*所以其他方面也.*",
                r"整体.*都很好",
                r"一好百好",
                r"光环.*",
                r"连带.*"
            ],
            BiasType.BANDWAGON: [
                r"大家都.*",
                r"众人.*",
                r"流行.*",
                r"主流.*",
                r"跟风.*"
            ],
            BiasType.LOSS_AVERSION: [
                r"损失.*",
                r"失去.*",
                r"风险.*",
                r"保守.*",
                r"避免.*"
            ]
        }
    
    def _initialize_bias_keywords(self) -> Dict[BiasType, List[str]]:
        """初始化偏见关键词"""
        return {
            BiasType.CONFIRMATION: [
                "证实", "验证", "支持", "符合", "预期", "假设", "观点", "理论"
            ],
            BiasType.ANCHORING: [
                "锚定", "起始", "初始", "第一", "基准", "参考点", "出发点"
            ],
            BiasType.AVAILABILITY: [
                "记得", "想起", "回忆", "印象", "最近", "经常", "容易", "明显"
            ],
            BiasType.REPRESENTATIVENESS: [
                "典型", "代表", "相似", "像", "符合", "模式", "刻板", "原型"
            ],
            BiasType.OVERCONFIDENCE: [
                "确信", "肯定", "绝对", "毫无疑问", "100%", "必然", "一定"
            ],
            BiasType.FRAMING: [
                "框架", "角度", "视角", "表述", "描述", "定义", "包装", "呈现"
            ],
            BiasType.SUNK_COST: [
                "沉没", "投入", "成本", "浪费", "白费", "既然", "已经"
            ],
            BiasType.SURVIVORSHIP: [
                "幸存", "成功", "存活", "剩下", "留下", "看到", "注意到"
            ],
            BiasType.ATTRIBUTION: [
                "归因", "原因", "责任", "怪罪", "功劳", "因为", "由于"
            ],
            BiasType.HALO_EFFECT: [
                "光环", "整体", "全面", "连带", "影响", "印象", "形象"
            ],
            BiasType.BANDWAGON: [
                "从众", "跟风", "流行", "大家", "众人", "主流", "趋势"
            ],
            BiasType.LOSS_AVERSION: [
                "损失", "失去", "风险", "保守", "避免", "害怕", "担心"
            ],
            BiasType.RECENCY: [
                "最近", "刚刚", "新近", "近期", "最新", "当前", "现在"
            ],
            BiasType.PRIMACY: [
                "首先", "最初", "开始", "第一", "起初", "首次", "最早"
            ],
            BiasType.HINDSIGHT: [
                "早知道", "后见之明", "事后", "回头看", "现在想来", "其实"
            ]
        }
    
    def _initialize_bias_indicators(self) -> Dict[BiasType, Dict[str, Any]]:
        """初始化偏见指标"""
        return {
            BiasType.CONFIRMATION: {
                'weight_threshold': 0.6,
                'context_importance': 0.8,
                'linguistic_markers': ['证实', '支持', '验证', '符合预期'],
                'severity_factors': ['绝对化表述', '忽略反证', '选择性引用']
            },
            BiasType.ANCHORING: {
                'weight_threshold': 0.5,
                'context_importance': 0.7,
                'linguistic_markers': ['基于', '从...开始', '初始'],
                'severity_factors': ['过度依赖初始信息', '调整不足']
            },
            BiasType.AVAILABILITY: {
                'weight_threshold': 0.5,
                'context_importance': 0.6,
                'linguistic_markers': ['记得', '想起', '最近', '经常'],
                'severity_factors': ['忽略基础概率', '过度依赖记忆']
            },
            BiasType.OVERCONFIDENCE: {
                'weight_threshold': 0.7,
                'context_importance': 0.9,
                'linguistic_markers': ['确信', '绝对', '毫无疑问', '100%'],
                'severity_factors': ['极端确定性', '忽略不确定性', '缺乏谦逊']
            },
            BiasType.FRAMING: {
                'weight_threshold': 0.4,
                'context_importance': 0.6,
                'linguistic_markers': ['角度', '框架', '表述', '描述'],
                'severity_factors': ['单一视角', '忽略其他框架']
            }
        }
    
    def detect_biases(self, agent_id: str, text: str, context: str = "") -> BiasDetectionResult:
        """检测偏见"""
        biases_detected = []
        
        # 对每种偏见类型进行检测
        for bias_type in BiasType:
            evidence_list = self._detect_specific_bias(bias_type, text, context)
            biases_detected.extend(evidence_list)
        
        # 计算整体偏见得分
        overall_bias_score = self._calculate_overall_bias_score(biases_detected)
        
        # 计算偏见分布
        bias_distribution = self._calculate_bias_distribution(biases_detected)
        
        # 风险评估
        risk_assessment = self._assess_bias_risk(overall_bias_score, biases_detected)
        
        # 生成建议
        recommendations = self._generate_bias_recommendations(biases_detected, overall_bias_score)
        
        # 创建检测结果
        result = BiasDetectionResult(
            detection_id=self._generate_detection_id(),
            agent_id=agent_id,
            text_analyzed=text,
            biases_detected=biases_detected,
            overall_bias_score=overall_bias_score,
            bias_distribution=bias_distribution,
            risk_assessment=risk_assessment,
            recommendations=recommendations,
            timestamp=datetime.now()
        )
        
        self.detection_results.append(result)
        
        # 更新偏见档案
        self._update_bias_profile(result)
        
        return result
    
    def _detect_specific_bias(self, bias_type: BiasType, text: str, context: str) -> List[BiasEvidence]:
        """检测特定类型的偏见"""
        evidence_list = []
        
        # 获取该偏见类型的检测规则
        patterns = self.bias_patterns.get(bias_type, [])
        keywords = self.bias_keywords.get(bias_type, [])
        indicators = self.bias_indicators.get(bias_type, {})
        
        # 模式匹配检测
        for pattern in patterns:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                evidence = self._create_bias_evidence(
                    bias_type, match.group(), text, context, 
                    confidence=0.7, reasoning=f"匹配模式: {pattern}"
                )
                evidence_list.append(evidence)
        
        # 关键词检测
        keyword_count = sum(1 for keyword in keywords if keyword in text.lower())
        if keyword_count > 0:
            keyword_density = keyword_count / len(text.split())
            if keyword_density > 0.02:  # 关键词密度阈值
                evidence = self._create_bias_evidence(
                    bias_type, f"关键词密度: {keyword_density:.3f}", text, context,
                    confidence=min(0.9, keyword_density * 10),
                    reasoning=f"检测到{keyword_count}个相关关键词"
                )
                evidence_list.append(evidence)
        
        # 特定偏见的专门检测
        specific_evidence = self._detect_bias_specific_logic(bias_type, text, context)
        evidence_list.extend(specific_evidence)
        
        return evidence_list
    
    def _detect_bias_specific_logic(self, bias_type: BiasType, text: str, context: str) -> List[BiasEvidence]:
        """特定偏见的专门检测逻辑"""
        evidence_list = []
        
        if bias_type == BiasType.CONFIRMATION:
            evidence_list.extend(self._detect_confirmation_bias(text, context))
        elif bias_type == BiasType.ANCHORING:
            evidence_list.extend(self._detect_anchoring_bias(text, context))
        elif bias_type == BiasType.AVAILABILITY:
            evidence_list.extend(self._detect_availability_bias(text, context))
        elif bias_type == BiasType.OVERCONFIDENCE:
            evidence_list.extend(self._detect_overconfidence_bias(text, context))
        elif bias_type == BiasType.FRAMING:
            evidence_list.extend(self._detect_framing_bias(text, context))
        elif bias_type == BiasType.ATTRIBUTION:
            evidence_list.extend(self._detect_attribution_bias(text, context))
        elif bias_type == BiasType.HALO_EFFECT:
            evidence_list.extend(self._detect_halo_effect(text, context))
        elif bias_type == BiasType.BANDWAGON:
            evidence_list.extend(self._detect_bandwagon_bias(text, context))
        elif bias_type == BiasType.LOSS_AVERSION:
            evidence_list.extend(self._detect_loss_aversion(text, context))
        
        return evidence_list
    
    def _detect_confirmation_bias(self, text: str, context: str) -> List[BiasEvidence]:
        """检测确认偏见"""
        evidence_list = []
        
        # 检测选择性引用
        if "支持" in text and "反对" not in text:
            evidence = self._create_bias_evidence(
                BiasType.CONFIRMATION, "只提及支持证据，忽略反对证据", 
                text, context, confidence=0.6,
                reasoning="可能存在选择性信息处理"
            )
            evidence_list.append(evidence)
        
        # 检测过度确定性表述
        certainty_words = ["肯定", "确实", "毫无疑问", "显然", "当然"]
        certainty_count = sum(1 for word in certainty_words if word in text)
        if certainty_count > 2:
            evidence = self._create_bias_evidence(
                BiasType.CONFIRMATION, f"过度确定性表述({certainty_count}次)", 
                text, context, confidence=0.7,
                reasoning="高频使用确定性词汇可能表明确认偏见"
            )
            evidence_list.append(evidence)
        
        return evidence_list
    
    def _detect_anchoring_bias(self, text: str, context: str) -> List[BiasEvidence]:
        """检测锚定偏见"""
        evidence_list = []
        
        # 检测对初始信息的过度依赖
        anchor_phrases = ["基于最初", "从...开始", "第一印象", "起始"]
        for phrase in anchor_phrases:
            if phrase in text:
                evidence = self._create_bias_evidence(
                    BiasType.ANCHORING, f"依赖初始信息: {phrase}", 
                    text, context, confidence=0.6,
                    reasoning="可能过度依赖初始锚点信息"
                )
                evidence_list.append(evidence)
        
        return evidence_list
    
    def _detect_availability_bias(self, text: str, context: str) -> List[BiasEvidence]:
        """检测可得性偏见"""
        evidence_list = []
        
        # 检测对近期或易记忆事件的过度依赖
        availability_indicators = ["最近", "记得", "印象深刻", "经常听到"]
        for indicator in availability_indicators:
            if indicator in text:
                evidence = self._create_bias_evidence(
                    BiasType.AVAILABILITY, f"依赖易得信息: {indicator}", 
                    text, context, confidence=0.5,
                    reasoning="可能过度依赖容易回忆的信息"
                )
                evidence_list.append(evidence)
        
        return evidence_list
    
    def _detect_overconfidence_bias(self, text: str, context: str) -> List[BiasEvidence]:
        """检测过度自信偏见"""
        evidence_list = []
        
        # 检测极端确定性表述
        extreme_confidence = ["100%", "绝对", "毫无疑问", "必然", "一定会"]
        confidence_score = 0
        
        for phrase in extreme_confidence:
            if phrase in text:
                confidence_score += 0.2
        
        if confidence_score > 0.4:
            evidence = self._create_bias_evidence(
                BiasType.OVERCONFIDENCE, "极端确定性表述", 
                text, context, confidence=confidence_score,
                reasoning="使用过多极端确定性词汇"
            )
            evidence_list.append(evidence)
        
        # 检测缺乏不确定性表达
        uncertainty_words = ["可能", "也许", "大概", "或许", "不确定"]
        if not any(word in text for word in uncertainty_words) and len(text) > 100:
            evidence = self._create_bias_evidence(
                BiasType.OVERCONFIDENCE, "缺乏不确定性表达", 
                text, context, confidence=0.6,
                reasoning="长文本中缺乏不确定性表达可能表明过度自信"
            )
            evidence_list.append(evidence)
        
        return evidence_list
    
    def _detect_framing_bias(self, text: str, context: str) -> List[BiasEvidence]:
        """检测框架偏见"""
        evidence_list = []
        
        # 检测单一视角表述
        framing_indicators = ["从...角度", "换个说法", "如果这样看", "重新定义"]
        single_perspective_count = 0
        
        for indicator in framing_indicators:
            if indicator in text:
                single_perspective_count += 1
        
        if single_perspective_count == 1:  # 只有一种框架
            evidence = self._create_bias_evidence(
                BiasType.FRAMING, "单一视角框架", 
                text, context, confidence=0.5,
                reasoning="可能受到特定框架影响，缺乏多角度思考"
            )
            evidence_list.append(evidence)
        
        return evidence_list
    
    def _detect_attribution_bias(self, text: str, context: str) -> List[BiasEvidence]:
        """检测归因偏见"""
        evidence_list = []
        
        # 检测基本归因错误
        self_attribution = re.findall(r'我.*是因为.*环境|情况|条件', text)
        other_attribution = re.findall(r'他们?.*是因为.*性格|能力|态度', text)
        
        if len(other_attribution) > len(self_attribution) and len(other_attribution) > 0:
            evidence = self._create_bias_evidence(
                BiasType.ATTRIBUTION, "基本归因错误", 
                text, context, confidence=0.7,
                reasoning="倾向于将他人行为归因于内在因素，自己行为归因于外在因素"
            )
            evidence_list.append(evidence)
        
        return evidence_list
    
    def _detect_halo_effect(self, text: str, context: str) -> List[BiasEvidence]:
        """检测光环效应"""
        evidence_list = []
        
        # 检测整体性评价
        halo_patterns = [
            r'因为.*好，所以.*也.*好',
            r'整体.*都很.*',
            r'一.*百.*',
            r'全面.*优秀'
        ]
        
        for pattern in halo_patterns:
            if re.search(pattern, text):
                evidence = self._create_bias_evidence(
                    BiasType.HALO_EFFECT, "整体性评价倾向", 
                    text, context, confidence=0.6,
                    reasoning="可能受到光环效应影响，基于单一特征进行整体评价"
                )
                evidence_list.append(evidence)
                break
        
        return evidence_list
    
    def _detect_bandwagon_bias(self, text: str, context: str) -> List[BiasEvidence]:
        """检测从众偏见"""
        evidence_list = []
        
        # 检测从众表述
        bandwagon_phrases = ["大家都", "众人", "流行", "主流", "大多数人"]
        bandwagon_count = sum(1 for phrase in bandwagon_phrases if phrase in text)
        
        if bandwagon_count > 1:
            evidence = self._create_bias_evidence(
                BiasType.BANDWAGON, f"从众表述({bandwagon_count}次)", 
                text, context, confidence=0.6,
                reasoning="频繁引用群体行为作为决策依据"
            )
            evidence_list.append(evidence)
        
        return evidence_list
    
    def _detect_loss_aversion(self, text: str, context: str) -> List[BiasEvidence]:
        """检测损失厌恶"""
        evidence_list = []
        
        # 检测损失相关表述
        loss_words = ["损失", "失去", "风险", "避免", "保守", "安全"]
        gain_words = ["获得", "收益", "机会", "积极", "进取", "冒险"]
        
        loss_count = sum(1 for word in loss_words if word in text)
        gain_count = sum(1 for word in gain_words if word in text)
        
        if loss_count > gain_count * 2 and loss_count > 2:
            evidence = self._create_bias_evidence(
                BiasType.LOSS_AVERSION, f"过度关注损失(损失词{loss_count}次 vs 收益词{gain_count}次)", 
                text, context, confidence=0.7,
                reasoning="对损失的关注明显超过对收益的关注"
            )
            evidence_list.append(evidence)
        
        return evidence_list
    
    def _create_bias_evidence(self, bias_type: BiasType, description: str, 
                            text: str, context: str, confidence: float, 
                            reasoning: str) -> BiasEvidence:
        """创建偏见证据"""
        # 确定严重程度
        severity = self._determine_severity(bias_type, confidence, description)
        
        # 提取相关文本片段
        snippet = self._extract_relevant_snippet(text, description, bias_type)
        
        return BiasEvidence(
            evidence_id=self._generate_evidence_id(),
            bias_type=bias_type,
            description=description,
            text_snippet=snippet,
            confidence=confidence,
            severity=severity,
            context=context,
            reasoning=reasoning,
            timestamp=datetime.now()
        )
    
    def _determine_severity(self, bias_type: BiasType, confidence: float, description: str) -> BiasSeverity:
        """确定偏见严重程度"""
        # 基础严重程度基于置信度
        if confidence >= 0.8:
            base_severity = BiasSeverity.HIGH
        elif confidence >= 0.6:
            base_severity = BiasSeverity.MODERATE
        else:
            base_severity = BiasSeverity.LOW
        
        # 根据偏见类型调整
        high_risk_biases = [BiasType.OVERCONFIDENCE, BiasType.CONFIRMATION, BiasType.ATTRIBUTION]
        if bias_type in high_risk_biases and confidence > 0.7:
            return BiasSeverity.CRITICAL
        
        # 根据描述内容调整
        critical_keywords = ["极端", "绝对", "100%", "毫无疑问", "必然"]
        if any(keyword in description for keyword in critical_keywords):
            if base_severity == BiasSeverity.HIGH:
                return BiasSeverity.CRITICAL
            elif base_severity == BiasSeverity.MODERATE:
                return BiasSeverity.HIGH
        
        return base_severity
    
    def _extract_relevant_snippet(self, text: str, description: str, bias_type: BiasType) -> str:
        """提取相关文本片段"""
        # 简单实现：返回包含关键信息的句子
        sentences = text.split('。')
        keywords = self.bias_keywords.get(bias_type, [])
        
        for sentence in sentences:
            if any(keyword in sentence for keyword in keywords):
                return sentence.strip() + '。'
        
        # 如果没找到相关句子，返回前100个字符
        return text[:100] + "..." if len(text) > 100 else text
    
    def _calculate_overall_bias_score(self, biases: List[BiasEvidence]) -> float:
        """计算整体偏见得分"""
        if not biases:
            return 0.0
        
        # 加权平均，考虑置信度和严重程度
        total_weight = 0
        weighted_sum = 0
        
        severity_weights = {
            BiasSeverity.LOW: 1.0,
            BiasSeverity.MODERATE: 2.0,
            BiasSeverity.HIGH: 3.0,
            BiasSeverity.CRITICAL: 4.0
        }
        
        for bias in biases:
            weight = severity_weights[bias.severity]
            weighted_sum += bias.confidence * weight
            total_weight += weight
        
        return min(1.0, weighted_sum / total_weight) if total_weight > 0 else 0.0
    
    def _calculate_bias_distribution(self, biases: List[BiasEvidence]) -> Dict[BiasType, float]:
        """计算偏见分布"""
        distribution = {bias_type: 0.0 for bias_type in BiasType}
        
        if not biases:
            return distribution
        
        # 按类型统计偏见
        type_counts = Counter(bias.bias_type for bias in biases)
        type_confidences = defaultdict(list)
        
        for bias in biases:
            type_confidences[bias.bias_type].append(bias.confidence)
        
        # 计算每种类型的得分
        for bias_type, count in type_counts.items():
            avg_confidence = np.mean(type_confidences[bias_type])
            distribution[bias_type] = avg_confidence * (count / len(biases))
        
        return distribution
    
    def _assess_bias_risk(self, overall_score: float, biases: List[BiasEvidence]) -> str:
        """评估偏见风险"""
        critical_count = sum(1 for bias in biases if bias.severity == BiasSeverity.CRITICAL)
        high_count = sum(1 for bias in biases if bias.severity == BiasSeverity.HIGH)
        
        if critical_count > 0 or overall_score > 0.8:
            return "高风险：检测到严重偏见，可能显著影响决策质量"
        elif high_count > 2 or overall_score > 0.6:
            return "中等风险：存在多个偏见，需要注意和改进"
        elif overall_score > 0.3:
            return "低风险：存在轻微偏见，建议保持警觉"
        else:
            return "风险较低：未检测到明显偏见"
    
    def _generate_bias_recommendations(self, biases: List[BiasEvidence], overall_score: float) -> List[str]:
        """生成偏见改进建议"""
        recommendations = []
        
        # 基于检测到的偏见类型生成建议
        bias_types = set(bias.bias_type for bias in biases)
        
        bias_recommendations = {
            BiasType.CONFIRMATION: "主动寻找反对证据，考虑不同观点",
            BiasType.ANCHORING: "在做决策前考虑多个起始点和参考框架",
            BiasType.AVAILABILITY: "收集更全面的数据，不仅依赖容易回忆的信息",
            BiasType.OVERCONFIDENCE: "表达适当的不确定性，承认知识的局限性",
            BiasType.FRAMING: "从多个角度重新审视问题，考虑不同的表述方式",
            BiasType.ATTRIBUTION: "考虑情境因素对行为的影响，避免过度归因于个人特质",
            BiasType.HALO_EFFECT: "独立评估不同维度，避免让单一印象影响整体判断",
            BiasType.BANDWAGON: "独立思考，不盲从群体意见",
            BiasType.LOSS_AVERSION: "平衡考虑潜在收益和损失，避免过度保守"
        }
        
        for bias_type in bias_types:
            if bias_type in bias_recommendations:
                recommendations.append(bias_recommendations[bias_type])
        
        # 基于整体得分的通用建议
        if overall_score > 0.7:
            recommendations.append("建议进行系统性的偏见意识训练")
            recommendations.append("在重要决策前进行偏见检查清单审核")
        elif overall_score > 0.4:
            recommendations.append("定期反思决策过程，识别可能的偏见")
            recommendations.append("寻求他人意见，获得不同视角")
        
        # 去重并限制数量
        recommendations = list(set(recommendations))[:8]
        
        return recommendations
    
    def _update_bias_profile(self, result: BiasDetectionResult):
        """更新偏见档案"""
        agent_id = result.agent_id
        
        if agent_id not in self.bias_profiles:
            # 创建新的偏见档案
            self.bias_profiles[agent_id] = BiasProfile(
                agent_id=agent_id,
                bias_tendencies={bias_type: 0.0 for bias_type in BiasType},
                historical_detections=[],
                bias_evolution={bias_type.value: [] for bias_type in BiasType},
                risk_level="unknown",
                improvement_trend=0.0,
                last_updated=datetime.now()
            )
        
        profile = self.bias_profiles[agent_id]
        
        # 更新偏见倾向
        for bias_type, score in result.bias_distribution.items():
            # 使用指数移动平均更新
            alpha = 0.3  # 学习率
            current_tendency = profile.bias_tendencies.get(bias_type, 0.0)
            profile.bias_tendencies[bias_type] = alpha * score + (1 - alpha) * current_tendency
        
        # 添加历史记录
        profile.historical_detections.append(result.detection_id)
        
        # 更新偏见演化
        for bias_type in BiasType:
            profile.bias_evolution[bias_type.value].append(
                profile.bias_tendencies[bias_type]
            )
            # 保持最近20次记录
            if len(profile.bias_evolution[bias_type.value]) > 20:
                profile.bias_evolution[bias_type.value] = profile.bias_evolution[bias_type.value][-20:]
        
        # 更新风险等级
        profile.risk_level = self._calculate_risk_level(profile.bias_tendencies)
        
        # 计算改进趋势
        profile.improvement_trend = self._calculate_improvement_trend(profile.bias_evolution)
        
        profile.last_updated = datetime.now()
    
    def _calculate_risk_level(self, bias_tendencies: Dict[BiasType, float]) -> str:
        """计算风险等级"""
        avg_bias = np.mean(list(bias_tendencies.values()))
        max_bias = max(bias_tendencies.values()) if bias_tendencies else 0
        
        if max_bias > 0.8 or avg_bias > 0.6:
            return "高风险"
        elif max_bias > 0.6 or avg_bias > 0.4:
            return "中等风险"
        elif max_bias > 0.3 or avg_bias > 0.2:
            return "低风险"
        else:
            return "风险很低"
    
    def _calculate_improvement_trend(self, bias_evolution: Dict[str, List[float]]) -> float:
        """计算改进趋势"""
        trends = []
        
        for bias_type, history in bias_evolution.items():
            if len(history) >= 3:
                # 计算线性趋势
                x = np.arange(len(history))
                y = np.array(history)
                
                # 简单线性回归
                if len(x) > 1:
                    slope = np.corrcoef(x, y)[0, 1] * (np.std(y) / np.std(x))
                    trends.append(-slope)  # 负斜率表示改进
        
        return np.mean(trends) if trends else 0.0
    
    def compare_bias_profiles(self, agent_ids: List[str]) -> BiasComparison:
        """比较偏见档案"""
        if len(agent_ids) < 2:
            raise ValueError("至少需要两个智能体进行比较")
        
        # 获取偏见档案
        profiles = []
        for agent_id in agent_ids:
            if agent_id in self.bias_profiles:
                profiles.append(self.bias_profiles[agent_id])
            else:
                self.logger.warning(f"智能体 {agent_id} 没有偏见档案")
        
        if len(profiles) < 2:
            raise ValueError("没有足够的偏见档案进行比较")
        
        # 计算偏见相似性
        bias_similarities = {}
        for i in range(len(profiles)):
            for j in range(i + 1, len(profiles)):
                agent1, agent2 = profiles[i].agent_id, profiles[j].agent_id
                similarity = self._calculate_bias_similarity(profiles[i], profiles[j])
                bias_similarities[f"{agent1}-{agent2}"] = similarity
        
        # 识别互补偏见
        complementary_biases = self._identify_complementary_biases(profiles)
        
        # 计算集体风险
        collective_risk = self._calculate_collective_risk(profiles)
        
        # 生成缓解策略
        mitigation_strategies = self._generate_mitigation_strategies(profiles, collective_risk)
        
        comparison = BiasComparison(
            comparison_id=self._generate_comparison_id(),
            agents=agent_ids,
            bias_similarities=bias_similarities,
            complementary_biases=complementary_biases,
            collective_risk=collective_risk,
            mitigation_strategies=mitigation_strategies,
            timestamp=datetime.now()
        )
        
        self.comparison_history.append(comparison)
        
        return comparison
    
    def _calculate_bias_similarity(self, profile1: BiasProfile, profile2: BiasProfile) -> float:
        """计算偏见相似性"""
        similarities = []
        
        for bias_type in BiasType:
            tendency1 = profile1.bias_tendencies.get(bias_type, 0.0)
            tendency2 = profile2.bias_tendencies.get(bias_type, 0.0)
            
            # 计算相似性（1 - 绝对差值）
            similarity = 1.0 - abs(tendency1 - tendency2)
            similarities.append(similarity)
        
        return np.mean(similarities)
    
    def _identify_complementary_biases(self, profiles: List[BiasProfile]) -> Dict[str, List[BiasType]]:
        """识别互补偏见"""
        complementary = {}
        
        for profile in profiles:
            agent_id = profile.agent_id
            # 找出该智能体的主要偏见（倾向值 > 0.5）
            major_biases = [
                bias_type for bias_type, tendency in profile.bias_tendencies.items()
                if tendency > 0.5
            ]
            complementary[agent_id] = major_biases
        
        return complementary
    
    def _calculate_collective_risk(self, profiles: List[BiasProfile]) -> float:
        """计算集体风险"""
        # 计算平均偏见倾向
        all_tendencies = []
        for profile in profiles:
            all_tendencies.extend(profile.bias_tendencies.values())
        
        avg_bias = np.mean(all_tendencies) if all_tendencies else 0.0
        
        # 计算偏见重叠度
        bias_overlaps = []
        for bias_type in BiasType:
            agents_with_bias = sum(
                1 for profile in profiles 
                if profile.bias_tendencies.get(bias_type, 0) > 0.5
            )
            overlap_ratio = agents_with_bias / len(profiles)
            bias_overlaps.append(overlap_ratio)
        
        max_overlap = max(bias_overlaps) if bias_overlaps else 0.0
        
        # 综合风险评分
        collective_risk = (avg_bias * 0.6 + max_overlap * 0.4)
        
        return collective_risk
    
    def _generate_mitigation_strategies(self, profiles: List[BiasProfile], collective_risk: float) -> List[str]:
        """生成缓解策略"""
        strategies = []
        
        # 基于集体风险等级的策略
        if collective_risk > 0.7:
            strategies.append("实施强制性偏见检查流程")
            strategies.append("引入外部审核机制")
            strategies.append("建立多元化决策团队")
        elif collective_risk > 0.4:
            strategies.append("定期进行偏见意识培训")
            strategies.append("建立同伴审查制度")
            strategies.append("使用结构化决策工具")
        
        # 基于共同偏见的策略
        common_biases = self._find_common_biases(profiles)
        
        if BiasType.CONFIRMATION in common_biases:
            strategies.append("建立红队/蓝队辩论机制")
        if BiasType.OVERCONFIDENCE in common_biases:
            strategies.append("要求提供置信区间而非点估计")
        if BiasType.ANCHORING in common_biases:
            strategies.append("使用多个独立的起始点进行分析")
        
        # 通用策略
        strategies.append("建立偏见监控仪表板")
        strategies.append("定期进行偏见评估和反馈")
        
        return list(set(strategies))[:10]  # 去重并限制数量
    
    def _find_common_biases(self, profiles: List[BiasProfile]) -> List[BiasType]:
        """找出共同偏见"""
        common_biases = []
        
        for bias_type in BiasType:
            agents_with_bias = sum(
                1 for profile in profiles 
                if profile.bias_tendencies.get(bias_type, 0) > 0.5
            )
            
            # 如果超过一半的智能体都有这种偏见
            if agents_with_bias > len(profiles) / 2:
                common_biases.append(bias_type)
        
        return common_biases
    
    def get_bias_summary(self, agent_id: str) -> Optional[Dict[str, Any]]:
        """获取偏见摘要"""
        if agent_id not in self.bias_profiles:
            return None
        
        profile = self.bias_profiles[agent_id]
        agent_detections = [r for r in self.detection_results if r.agent_id == agent_id]
        
        # 计算统计信息
        total_detections = len(agent_detections)
        avg_bias_score = np.mean([r.overall_bias_score for r in agent_detections]) if agent_detections else 0
        
        # 找出主要偏见
        major_biases = [
            bias_type for bias_type, tendency in profile.bias_tendencies.items()
            if tendency > 0.4
        ]
        
        return {
            'agent_id': agent_id,
            'bias_profile': profile.to_dict(),
            'detection_history': {
                'total_detections': total_detections,
                'avg_bias_score': avg_bias_score,
                'recent_detections': len([r for r in agent_detections[-10:]]),
                'improvement_trend': profile.improvement_trend
            },
            'major_biases': [bias.value for bias in major_biases],
            'risk_assessment': profile.risk_level,
            'recommendations': self._get_personalized_recommendations(profile)
        }
    
    def _get_personalized_recommendations(self, profile: BiasProfile) -> List[str]:
        """获取个性化建议"""
        recommendations = []
        
        # 基于主要偏见的建议
        for bias_type, tendency in profile.bias_tendencies.items():
            if tendency > 0.6:
                if bias_type == BiasType.CONFIRMATION:
                    recommendations.append("建立反驳自己观点的习惯")
                elif bias_type == BiasType.OVERCONFIDENCE:
                    recommendations.append("在表达观点时加入不确定性表述")
                elif bias_type == BiasType.ANCHORING:
                    recommendations.append("在分析前考虑多个不同的起始假设")
        
        # 基于改进趋势的建议
        if profile.improvement_trend < -0.1:
            recommendations.append("当前偏见有恶化趋势，需要加强自我监控")
        elif profile.improvement_trend > 0.1:
            recommendations.append("偏见控制有所改善，继续保持当前做法")
        
        return recommendations[:5]
    
    def _generate_detection_id(self) -> str:
        """生成检测ID"""
        timestamp = datetime.now().isoformat()
        content = f"detection_{timestamp}_{len(self.detection_results)}"
        return hashlib.md5(content.encode()).hexdigest()[:12]
    
    def _generate_evidence_id(self) -> str:
        """生成证据ID"""
        timestamp = datetime.now().isoformat()
        content = f"evidence_{timestamp}_{np.random.randint(1000, 9999)}"
        return hashlib.md5(content.encode()).hexdigest()[:8]
    
    def _generate_comparison_id(self) -> str:
        """生成比较ID"""
        timestamp = datetime.now().isoformat()
        content = f"comparison_{timestamp}_{len(self.comparison_history)}"
        return hashlib.md5(content.encode()).hexdigest()[:12]
    
    def export_bias_analysis(self, output_file: str, agent_id: Optional[str] = None):
        """导出偏见分析结果"""
        if agent_id:
            # 导出特定智能体的分析
            if agent_id not in self.bias_profiles:
                raise ValueError(f"智能体 {agent_id} 没有偏见档案")
            
            export_data = {
                'bias_summary': self.get_bias_summary(agent_id),
                'detection_results': [r.to_dict() for r in self.detection_results if r.agent_id == agent_id],
                'export_timestamp': datetime.now().isoformat()
            }
        else:
            # 导出所有分析
            export_data = {
                'bias_profiles': {agent_id: profile.to_dict() for agent_id, profile in self.bias_profiles.items()},
                'detection_results': [r.to_dict() for r in self.detection_results],
                'bias_comparisons': [c.to_dict() for c in self.comparison_history],
                'statistics': self._get_bias_statistics(),
                'export_timestamp': datetime.now().isoformat()
            }
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(export_data, f, ensure_ascii=False, indent=2)
        
        self.logger.info(f"偏见分析结果已导出到: {output_file}")
    
    def _get_bias_statistics(self) -> Dict[str, Any]:
        """获取偏见统计信息"""
        return {
            'total_agents_analyzed': len(self.bias_profiles),
            'total_detections': len(self.detection_results),
            'total_comparisons': len(self.comparison_history),
            'bias_type_distribution': {
                bias_type.value: sum(
                    1 for result in self.detection_results
                    for bias in result.biases_detected
                    if bias.bias_type == bias_type
                )
                for bias_type in BiasType
            },
            'avg_bias_score': np.mean([r.overall_bias_score for r in self.detection_results]) if self.detection_results else 0,
            'high_risk_agents': len([p for p in self.bias_profiles.values() if p.risk_level == "高风险"]),
            'most_common_bias': self._get_most_common_bias(),
            'improvement_rate': len([p for p in self.bias_profiles.values() if p.improvement_trend > 0]) / len(self.bias_profiles) if self.bias_profiles else 0
        }
    
    def _get_most_common_bias(self) -> str:
        """获取最常见的偏见"""
        all_biases = []
        for result in self.detection_results:
            for bias in result.biases_detected:
                all_biases.append(bias.bias_type)
        
        if all_biases:
            most_common = Counter(all_biases).most_common(1)[0][0]
            return most_common.value
        
        return "unknown"