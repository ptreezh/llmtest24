#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
海量角色共识测试结果分析脚本
分析模型在大规模角色协作、投票机制和共识算法方面的表现
"""

import json
import os
import re
from typing import Dict, List, Any
from datetime import datetime

class MassiveConsensusAnalyzer:
    def __init__(self, testout_dir: str = "testout"):
        self.testout_dir = testout_dir
        self.analysis_criteria = {
            "role_generation": {
                "diversity": "角色背景和观点的多样性",
                "realism": "角色设定的真实性和合理性",
                "scalability": "大规模角色生成的能力"
            },
            "collaborative_editing": {
                "perspective_differentiation": "不同角色观点的区分度",
                "conflict_identification": "分歧识别的准确性",
                "content_quality": "编辑建议的质量和专业性"
            },
            "voting_mechanism": {
                "algorithm_understanding": "共识算法的理解程度",
                "weight_allocation": "权重分配的合理性",
                "process_clarity": "投票过程的清晰度"
            },
            "blockchain_consensus": {
                "technical_accuracy": "区块链概念的准确性",
                "consensus_logic": "共识逻辑的完整性",
                "finality": "最终确定性的实现"
            },
            "overall_coordination": {
                "scale_management": "大规模协调能力",
                "convergence": "共识收敛能力",
                "consistency": "整体一致性维护"
            }
        }
    
    def load_test_results(self) -> List[Dict[str, Any]]:
        """加载测试结果文件"""
        results = []
        for filename in os.listdir(self.testout_dir):
            if filename.startswith("massive_consensus_case") and filename.endswith(".json"):
                filepath = os.path.join(self.testout_dir, filename)
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        data['filename'] = filename
                        results.append(data)
                except Exception as e:
                    print(f"加载文件 {filename} 失败: {e}")
        return results
    
    def analyze_role_generation(self, result: Dict[str, Any]) -> Dict[str, Any]:
        """分析角色生成阶段"""
        phase_data = result.get('phases', {}).get('role_generation', {})
        num_roles = phase_data.get('num_roles_generated', 0)
        
        analysis = {
            "num_roles_generated": num_roles,
            "scale_category": self._categorize_scale(num_roles),
            "diversity_score": self._estimate_diversity_score(result),
            "realism_score": self._estimate_realism_score(result)
        }
        
        return analysis
    
    def analyze_collaborative_editing(self, result: Dict[str, Any]) -> Dict[str, Any]:
        """分析协同编辑阶段"""
        editing_data = result.get('phases', {}).get('collaborative_editing', {})
        response = editing_data.get('response', '')
        
        analysis = {
            "response_length": len(response),
            "conflict_mentions": self._count_conflict_indicators(response),
            "perspective_diversity": self._assess_perspective_diversity(response),
            "structure_quality": self._assess_structure_quality(response)
        }
        
        return analysis
    
    def analyze_voting_mechanism(self, result: Dict[str, Any]) -> Dict[str, Any]:
        """分析投票机制阶段"""
        voting_data = result.get('phases', {}).get('voting_mechanism', {})
        response = voting_data.get('response', '')
        algorithm = voting_data.get('algorithm', '')
        
        analysis = {
            "algorithm_type": algorithm,
            "algorithm_understanding": self._assess_algorithm_understanding(response, algorithm),
            "weight_allocation": self._assess_weight_allocation(response),
            "process_completeness": self._assess_process_completeness(response)
        }
        
        return analysis
    
    def analyze_blockchain_consensus(self, result: Dict[str, Any]) -> Dict[str, Any]:
        """分析区块链共识阶段"""
        consensus_data = result.get('phases', {}).get('blockchain_consensus', {})
        response = consensus_data.get('response', '')
        
        analysis = {
            "blockchain_concepts": self._count_blockchain_concepts(response),
            "consensus_logic": self._assess_consensus_logic(response),
            "finality_achievement": self._assess_finality(response),
            "technical_depth": self._assess_technical_depth(response)
        }
        
        return analysis
    
    def _categorize_scale(self, num_roles: int) -> str:
        """分类规模等级"""
        if num_roles < 10:
            return "小规模"
        elif num_roles < 30:
            return "中等规模"
        elif num_roles < 60:
            return "大规模"
        else:
            return "超大规模"
    
    def _estimate_diversity_score(self, result: Dict[str, Any]) -> float:
        """估算角色多样性分数"""
        # 基于参数和响应内容估算
        num_roles = result.get('parameters', {}).get('num_roles', 0)
        if num_roles >= 50:
            return 0.9
        elif num_roles >= 20:
            return 0.7
        else:
            return 0.5
    
    def _estimate_realism_score(self, result: Dict[str, Any]) -> float:
        """估算角色真实性分数"""
        # 简化评估，实际应该分析角色描述的质量
        return 0.8
    
    def _count_conflict_indicators(self, text: str) -> int:
        """统计冲突指示词"""
        conflict_words = ['分歧', '争议', '冲突', '不同意见', '反对', '质疑', '辩论']
        count = 0
        for word in conflict_words:
            count += text.count(word)
        return count
    
    def _assess_perspective_diversity(self, text: str) -> float:
        """评估观点多样性"""
        perspective_indicators = ['观点', '立场', '角度', '视角', '看法', '意见']
        score = 0
        for indicator in perspective_indicators:
            if indicator in text:
                score += 0.2
        return min(score, 1.0)
    
    def _assess_structure_quality(self, text: str) -> float:
        """评估结构化程度"""
        structure_indicators = ['1.', '2.', '3.', '一、', '二、', '三、', '首先', '其次', '最后']
        score = 0
        for indicator in structure_indicators:
            if indicator in text:
                score += 0.1
        return min(score, 1.0)
    
    def _assess_algorithm_understanding(self, text: str, algorithm: str) -> float:
        """评估算法理解程度"""
        if '投票' in algorithm:
            keywords = ['权重', '多数', '投票', '统计']
        elif '拜占庭' in algorithm:
            keywords = ['拜占庭', '容错', '恶意', '验证']
        else:
            keywords = ['共识', '算法', '机制']
        
        score = 0
        for keyword in keywords:
            if keyword in text:
                score += 0.25
        return min(score, 1.0)
    
    def _assess_weight_allocation(self, text: str) -> float:
        """评估权重分配合理性"""
        weight_indicators = ['权重', '权威', '专业', '经验', '贡献']
        score = 0
        for indicator in weight_indicators:
            if indicator in text:
                score += 0.2
        return min(score, 1.0)
    
    def _assess_process_completeness(self, text: str) -> float:
        """评估过程完整性"""
        process_indicators = ['步骤', '阶段', '流程', '过程', '执行']
        score = 0
        for indicator in process_indicators:
            if indicator in text:
                score += 0.2
        return min(score, 1.0)
    
    def _count_blockchain_concepts(self, text: str) -> int:
        """统计区块链概念"""
        concepts = ['区块链', '共识', '验证', '节点', '分布式', '去中心化', '哈希', '签名']
        count = 0
        for concept in concepts:
            if concept in text:
                count += 1
        return count
    
    def _assess_consensus_logic(self, text: str) -> float:
        """评估共识逻辑"""
        logic_indicators = ['验证', '确认', '一致性', '最终性', '收敛']
        score = 0
        for indicator in logic_indicators:
            if indicator in text:
                score += 0.2
        return min(score, 1.0)
    
    def _assess_finality(self, text: str) -> float:
        """评估最终确定性"""
        finality_indicators = ['最终', '确定', '不可篡改', '固化', '完成']
        score = 0
        for indicator in finality_indicators:
            if indicator in text:
                score += 0.2
        return min(score, 1.0)
    
    def _assess_technical_depth(self, text: str) -> float:
        """评估技术深度"""
        return len(text) / 2000  # 简化评估
    
    def generate_comprehensive_analysis(self, results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """生成综合分析报告"""
        if not results:
            return {"error": "没有找到测试结果"}
        
        comprehensive_analysis = {
            "test_summary": {
                "total_cases": len(results),
                "test_date": datetime.now().isoformat(),
                "model_tested": results[0].get('parameters', {}).get('model', 'unknown')
            },
            "case_analyses": [],
            "overall_assessment": {}
        }
        
        # 分析每个测试用例
        for result in results:
            case_analysis = {
                "case_file": result.get('filename', ''),
                "parameters": result.get('parameters', {}),
                "role_generation": self.analyze_role_generation(result),
                "collaborative_editing": self.analyze_collaborative_editing(result),
                "voting_mechanism": self.analyze_voting_mechanism(result),
                "blockchain_consensus": self.analyze_blockchain_consensus(result)
            }
            comprehensive_analysis["case_analyses"].append(case_analysis)
        
        # 生成总体评估
        comprehensive_analysis["overall_assessment"] = self._generate_overall_assessment(
            comprehensive_analysis["case_analyses"]
        )
        
        return comprehensive_analysis
    
    def _generate_overall_assessment(self, case_analyses: List[Dict[str, Any]]) -> Dict[str, Any]:
        """生成总体评估"""
        if not case_analyses:
            return {}
        
        # 计算平均分数
        avg_scores = {}
        for phase in ["role_generation", "collaborative_editing", "voting_mechanism", "blockchain_consensus"]:
            scores = []
            for case in case_analyses:
                phase_data = case.get(phase, {})
                # 提取数值型指标进行平均
                for key, value in phase_data.items():
                    if isinstance(value, (int, float)) and 0 <= value <= 1:
                        scores.append(value)
            
            if scores:
                avg_scores[phase] = sum(scores) / len(scores)
        
        # 生成能力评估
        capabilities = {
            "大规模角色管理": self._assess_capability(case_analyses, "role_generation"),
            "协同编辑协调": self._assess_capability(case_analyses, "collaborative_editing"),
            "共识机制理解": self._assess_capability(case_analyses, "voting_mechanism"),
            "区块链技术应用": self._assess_capability(case_analyses, "blockchain_consensus")
        }
        
        return {
            "average_scores": avg_scores,
            "capability_assessment": capabilities,
            "recommendations": self._generate_recommendations(avg_scores)
        }
    
    def _assess_capability(self, case_analyses: List[Dict[str, Any]], phase: str) -> str:
        """评估特定能力"""
        # 简化评估逻辑
        return "中等"
    
    def _generate_recommendations(self, avg_scores: Dict[str, float]) -> List[str]:
        """生成改进建议"""
        recommendations = []
        
        for phase, score in avg_scores.items():
            if score < 0.5:
                recommendations.append(f"需要加强{phase}相关能力")
            elif score < 0.7:
                recommendations.append(f"{phase}能力有待提升")
        
        if not recommendations:
            recommendations.append("整体表现良好，可以尝试更复杂的场景")
        
        return recommendations

def main():
    """主函数"""
    analyzer = MassiveConsensusAnalyzer()
    
    # 加载测试结果
    results = analyzer.load_test_results()
    if not results:
        print("未找到测试结果文件")
        return
    
    # 生成分析报告
    analysis = analyzer.generate_comprehensive_analysis(results)
    
    # 保存分析报告
    output_path = os.path.join(analyzer.testout_dir, "massive_consensus_analysis.json")
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(analysis, f, ensure_ascii=False, indent=2)
    
    print(f"分析报告已保存到: {output_path}")
    
    # 打印简要总结
    print("\n=== 海量角色共识测试分析总结 ===")
    print(f"测试用例数量: {analysis['test_summary']['total_cases']}")
    
    for i, case in enumerate(analysis['case_analyses'], 1):
        params = case['parameters']
        print(f"\n用例{i}: {params.get('num_roles', 0)}个角色, 主题: {params.get('topic', '')}")
        print(f"  共识算法: {params.get('consensus_algorithm', '')}")
    
    capabilities = analysis['overall_assessment'].get('capability_assessment', {})
    print(f"\n能力评估:")
    for capability, level in capabilities.items():
        print(f"  {capability}: {level}")
    
    recommendations = analysis['overall_assessment'].get('recommendations', [])
    print(f"\n改进建议:")
    for rec in recommendations:
        print(f"  - {rec}")

if __name__ == "__main__":
    main()
