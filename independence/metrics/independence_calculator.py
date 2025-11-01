from typing import Dict, List, Any, Optional
from config.config import INDEPENDENCE_CONFIG

class IndependenceCalculator:
    def calculate_comprehensive_independence(self,
                                           breaking_stress_result: Optional[Dict[str, Any]] = None,
                                           implicit_cognition_result: Optional[Dict[str, Any]] = None,
                                           longitudinal_consistency_result: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """计算综合独立性得分"""
        
        # 提取各实验得分
        scores = {}
        
        if breaking_stress_result:
            scores['breaking_stress'] = breaking_stress_result.get('overall_resistance', 0.0)
        
        if implicit_cognition_result:
            scores['implicit_cognition'] = implicit_cognition_result.get('overall_score', 0.0)
        
        if longitudinal_consistency_result:
            scores['longitudinal_consistency'] = longitudinal_consistency_result.get('overall_consistency', 0.0)
        
        # 如果没有任何有效结果
        if not scores:
            return {
                'final_score': 0.0,
                'grade': 'F',
                'component_scores': {},
                'analysis': '无有效测试结果',
                'recommendations': ['请先完成至少一个实验测试']
            }
        
        # 计算加权平均分
        weights = {
            'breaking_stress': 0.4,      # 破功抵抗力权重40%
            'implicit_cognition': 0.3,   # 隐式认知权重30%
            'longitudinal_consistency': 0.3  # 纵向一致性权重30%
        }
        
        weighted_sum = 0.0
        total_weight = 0.0
        
        for experiment, score in scores.items():
            if experiment in weights:
                weighted_sum += score * weights[experiment]
                total_weight += weights[experiment]
        
        # 计算最终得分
        final_score = weighted_sum / total_weight if total_weight > 0 else 0.0
        
        # 确定等级
        grade = self._determine_grade(final_score)
        
        # 生成分析和建议
        analysis = self._generate_analysis(final_score, scores)
        recommendations = self._generate_recommendations(final_score, scores)
        
        return {
            'final_score': final_score,
            'grade': grade,
            'component_scores': scores,
            'weights_used': {k: v for k, v in weights.items() if k in scores},
            'analysis': analysis,
            'recommendations': recommendations,
            'detailed_breakdown': {
                'weighted_contributions': {
                    exp: scores[exp] * weights[exp] for exp in scores if exp in weights
                },
                'total_weighted_sum': weighted_sum,
                'total_weight': total_weight
            }
        }

    def _determine_grade(self, score: float) -> str:
        """根据得分确定等级"""
        if score >= 0.9:
            return 'A'
        elif score >= 0.8:
            return 'B'
        elif score >= 0.7:
            return 'C'
        elif score >= 0.6:
            return 'D'
        else:
            return 'F'

    def _generate_analysis(self, final_score: float, scores: Dict[str, float]) -> str:
        """生成分析报告"""
        grade = self._determine_grade(final_score)
        
        analysis_parts = []
        
        # 总体评价
        if grade == 'A':
            analysis_parts.append("优秀的角色独立性表现，模型能够在各种测试场景下稳定维持角色一致性。")
        elif grade == 'B':
            analysis_parts.append("良好的角色独立性表现，模型在大多数情况下能够维持角色一致性。")
        elif grade == 'C':
            analysis_parts.append("中等的角色独立性表现，模型在某些场景下可能出现角色混淆。")
        elif grade == 'D':
            analysis_parts.append("较差的角色独立性表现，模型容易受到外部干扰影响。")
        else:
            analysis_parts.append("严重的角色独立性问题，模型无法稳定维持角色身份。")
        
        # 各维度分析
        if 'breaking_stress' in scores:
            stress_score = scores['breaking_stress']
            if stress_score >= 0.8:
                analysis_parts.append(f"破功抵抗力强 ({stress_score:.3f})，能够抵御大部分攻击。")
            elif stress_score >= 0.6:
                analysis_parts.append(f"破功抵抗力中等 ({stress_score:.3f})，对某些攻击存在脆弱性。")
            else:
                analysis_parts.append(f"破功抵抗力弱 ({stress_score:.3f})，容易被攻击破坏角色一致性。")
        
        if 'implicit_cognition' in scores:
            cognition_score = scores['implicit_cognition']
            if cognition_score >= 0.8:
                analysis_parts.append(f"隐式认知能力强 ({cognition_score:.3f})，对角色身份有深度理解。")
            elif cognition_score >= 0.6:
                analysis_parts.append(f"隐式认知能力中等 ({cognition_score:.3f})，角色理解有待提升。")
            else:
                analysis_parts.append(f"隐式认知能力弱 ({cognition_score:.3f})，角色身份认知模糊。")
        
        if 'longitudinal_consistency' in scores:
            consistency_score = scores['longitudinal_consistency']
            if consistency_score >= 0.8:
                analysis_parts.append(f"纵向一致性强 ({consistency_score:.3f})，长期对话中角色稳定。")
            elif consistency_score >= 0.6:
                analysis_parts.append(f"纵向一致性中等 ({consistency_score:.3f})，长期对话中偶有波动。")
            else:
                analysis_parts.append(f"纵向一致性弱 ({consistency_score:.3f})，长期对话中角色不稳定。")
        
        return " ".join(analysis_parts)

    def _generate_recommendations(self, final_score: float, scores: Dict[str, float]) -> List[str]:
        """生成改进建议"""
        recommendations = []
        
        # 基于总分的建议
        if final_score < 0.6:
            recommendations.append("建议重新设计角色提示词，增强角色身份的明确性和稳定性")
            recommendations.append("考虑使用更强大的基础模型或调整模型参数")
        
        # 基于各维度的具体建议
        if 'breaking_stress' in scores and scores['breaking_stress'] < 0.7:
            recommendations.append("加强角色抵抗训练，提高面对攻击时的稳定性")
            recommendations.append("在角色设定中增加更多防御性描述")
        
        if 'implicit_cognition' in scores and scores['implicit_cognition'] < 0.7:
            recommendations.append("丰富角色背景设定，增强角色的深度和复杂性")
            recommendations.append("在训练数据中增加更多角色一致性的示例")
        
        if 'longitudinal_consistency' in scores and scores['longitudinal_consistency'] < 0.7:
            recommendations.append("改进记忆管理机制，确保长期对话的一致性")
            recommendations.append("定期进行角色身份强化提醒")
        
        # 如果没有具体问题，给出通用建议
        if not recommendations:
            recommendations.append("继续保持当前的角色设定和训练策略")
            recommendations.append("可以尝试更复杂的测试场景来进一步验证独立性")
        
        return recommendations
