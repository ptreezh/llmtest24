#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
动态角色切换与记忆管理测试结果分析脚本
分析模型在角色轮流切换、外部记忆文件管理和状态连续性方面的表现
"""

import json
import os
import re
from typing import Dict, List, Any
from datetime import datetime

class DynamicRoleSwitchingAnalyzer:
    def __init__(self, testout_dir: str = "testout"):
        self.testout_dir = testout_dir
        self.analysis_criteria = {
            "role_switching": {
                "accuracy": "角色切换的准确性",
                "speed": "切换响应的及时性", 
                "consistency": "角色特征的一致性",
                "differentiation": "角色间的区分度"
            },
            "memory_management": {
                "persistence": "记忆持续性",
                "integration": "新信息整合能力",
                "retrieval": "记忆检索准确性",
                "update": "记忆更新的逻辑性"
            },
            "state_continuity": {
                "personality": "个性连续性",
                "task_progress": "任务状态连续性",
                "dialogue_coherence": "对话连贯性",
                "attention_focus": "注意力焦点维护"
            },
            "context_integration": {
                "multi_source": "多源信息整合",
                "priority_handling": "优先级处理",
                "conflict_resolution": "信息冲突解决",
                "coherence": "整体连贯性"
            }
        }
    
    def load_test_results(self) -> Dict[str, Any]:
        """加载测试结果文件"""
        result_file = os.path.join(self.testout_dir, "dynamic_role_switching_test.json")
        try:
            with open(result_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"测试结果文件不存在: {result_file}")
            return {}
        except Exception as e:
            print(f"加载测试结果失败: {e}")
            return {}
    
    def analyze_role_switching_performance(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """分析角色切换性能"""
        switching_results = results.get("test_results", {}).get("results", {}).get("role_switching_sequence", [])
        
        if not switching_results:
            return {"error": "没有找到角色切换测试结果"}
        
        analysis = {
            "total_switches": len(switching_results),
            "successful_switches": 0,
            "failed_switches": 0,
            "role_accuracy": {},
            "response_quality": {},
            "consistency_scores": {}
        }
        
        role_counts = {}
        role_successes = {}
        
        for result in switching_results:
            expected_role = result.get("expected_role", "")
            success = result.get("success", False)
            response = result.get("response", "")
            
            # 统计成功率
            if success:
                analysis["successful_switches"] += 1
            else:
                analysis["failed_switches"] += 1
            
            # 按角色统计
            if expected_role not in role_counts:
                role_counts[expected_role] = 0
                role_successes[expected_role] = 0
            
            role_counts[expected_role] += 1
            if success:
                role_successes[expected_role] += 1
            
            # 分析响应质量
            if success and response:
                quality_score = self._assess_response_quality(response, expected_role)
                if expected_role not in analysis["response_quality"]:
                    analysis["response_quality"][expected_role] = []
                analysis["response_quality"][expected_role].append(quality_score)
        
        # 计算各角色准确率
        for role in role_counts:
            analysis["role_accuracy"][role] = role_successes[role] / role_counts[role] if role_counts[role] > 0 else 0
        
        # 计算平均响应质量
        for role in analysis["response_quality"]:
            scores = analysis["response_quality"][role]
            analysis["response_quality"][role] = sum(scores) / len(scores) if scores else 0
        
        return analysis
    
    def analyze_memory_persistence(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """分析记忆持续性"""
        memory_results = results.get("test_results", {}).get("results", {}).get("memory_persistence", {})
        
        if not memory_results:
            return {"error": "没有找到记忆持续性测试结果"}
        
        analysis = {
            "memory_continuity_score": 0,
            "cross_role_interference": 0,
            "information_retention": {},
            "context_awareness": {}
        }
        
        # 分析侦探记忆连续性
        detective_first = memory_results.get("detective_first", {})
        detective_second = memory_results.get("detective_second", {})
        
        if detective_first.get("success") and detective_second.get("success"):
            # 检查是否记住了钥匙线索
            first_response = detective_first.get("response", "")
            second_response = detective_second.get("response", "")
            
            if "钥匙" in first_response and "钥匙" in second_response:
                analysis["memory_continuity_score"] = 1.0
            elif "钥匙" in second_response:
                analysis["memory_continuity_score"] = 0.8
            else:
                analysis["memory_continuity_score"] = 0.3
        
        # 分析跨角色干扰
        doctor_interrupt = memory_results.get("doctor_interrupt", {})
        if doctor_interrupt.get("success"):
            doctor_response = doctor_interrupt.get("response", "")
            # 检查医生回应中是否混入了侦探的内容
            if any(word in doctor_response for word in ["失踪", "案件", "线索", "钥匙"]):
                analysis["cross_role_interference"] = 1.0  # 有干扰
            else:
                analysis["cross_role_interference"] = 0.0  # 无干扰
        
        return analysis
    
    def analyze_attention_focus(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """分析注意力焦点维护"""
        focus_results = results.get("test_results", {}).get("results", {}).get("attention_focus_maintenance", {})
        
        if not focus_results:
            return {"error": "没有找到注意力焦点测试结果"}
        
        analysis = {
            "focus_accuracy": {},
            "professional_consistency": {},
            "role_specific_keywords": {}
        }
        
        expected_focus_keywords = {
            "detective": ["案件", "线索", "调查", "失踪", "嫌疑", "证据"],
            "doctor": ["患者", "症状", "诊断", "健康", "医学", "治疗"],
            "teacher": ["学生", "教学", "理解", "故事", "学习", "课程"]
        }
        
        for role, result in focus_results.items():
            if result.get("success"):
                response = result.get("response", "")
                expected_keywords = expected_focus_keywords.get(role, [])
                
                # 计算关键词匹配度
                keyword_matches = sum(1 for keyword in expected_keywords if keyword in response)
                keyword_score = keyword_matches / len(expected_keywords) if expected_keywords else 0
                
                analysis["focus_accuracy"][role] = keyword_score
                analysis["role_specific_keywords"][role] = {
                    "expected": expected_keywords,
                    "matches": keyword_matches,
                    "score": keyword_score
                }
                
                # 评估专业一致性
                analysis["professional_consistency"][role] = self._assess_professional_consistency(response, role)
        
        return analysis
    
    def _assess_response_quality(self, response: str, role: str) -> float:
        """评估响应质量"""
        if not response:
            return 0.0
        
        quality_score = 0.0
        
        # 基础质量检查
        if len(response) > 20:
            quality_score += 0.3
        
        # 角色特征检查
        role_indicators = {
            "detective": ["根据我的观察", "线索", "调查", "分析"],
            "doctor": ["从医学角度", "症状", "健康", "建议"],
            "teacher": ["让我们一起", "学习", "理解", "思考"]
        }
        
        indicators = role_indicators.get(role, [])
        for indicator in indicators:
            if indicator in response:
                quality_score += 0.7 / len(indicators)
        
        return min(quality_score, 1.0)
    
    def _assess_professional_consistency(self, response: str, role: str) -> float:
        """评估专业一致性"""
        professional_terms = {
            "detective": ["调查", "证据", "嫌疑人", "案件", "线索", "推理"],
            "doctor": ["症状", "诊断", "治疗", "健康", "医学", "患者"],
            "teacher": ["学生", "教学", "学习", "理解", "课程", "知识"]
        }
        
        terms = professional_terms.get(role, [])
        if not terms:
            return 0.5
        
        term_count = sum(1 for term in terms if term in response)
        return min(term_count / len(terms), 1.0)
    
    def generate_comprehensive_analysis(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """生成综合分析报告"""
        if not results:
            return {"error": "没有测试结果可供分析"}
        
        comprehensive_analysis = {
            "test_summary": {
                "model_tested": results.get("test_results", {}).get("model", "unknown"),
                "test_date": datetime.now().isoformat(),
                "total_roles": len(results.get("test_results", {}).get("roles_tested", [])),
                "total_switches": results.get("test_results", {}).get("total_switches", 0)
            },
            "performance_analysis": {},
            "capability_assessment": {},
            "recommendations": []
        }
        
        # 分析各个维度
        comprehensive_analysis["performance_analysis"]["role_switching"] = self.analyze_role_switching_performance(results)
        comprehensive_analysis["performance_analysis"]["memory_persistence"] = self.analyze_memory_persistence(results)
        comprehensive_analysis["performance_analysis"]["attention_focus"] = self.analyze_attention_focus(results)
        
        # 生成能力评估
        comprehensive_analysis["capability_assessment"] = self._generate_capability_assessment(
            comprehensive_analysis["performance_analysis"]
        )
        
        # 生成建议
        comprehensive_analysis["recommendations"] = self._generate_recommendations(
            comprehensive_analysis["performance_analysis"]
        )
        
        return comprehensive_analysis
    
    def _generate_capability_assessment(self, performance_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """生成能力评估"""
        assessment = {}
        
        # 角色切换能力
        role_switching = performance_analysis.get("role_switching", {})
        if "successful_switches" in role_switching and "total_switches" in role_switching:
            success_rate = role_switching["successful_switches"] / role_switching["total_switches"]
            if success_rate >= 0.9:
                assessment["role_switching"] = "优秀"
            elif success_rate >= 0.7:
                assessment["role_switching"] = "良好"
            else:
                assessment["role_switching"] = "需要改进"
        
        # 记忆管理能力
        memory_persistence = performance_analysis.get("memory_persistence", {})
        memory_score = memory_persistence.get("memory_continuity_score", 0)
        if memory_score >= 0.8:
            assessment["memory_management"] = "优秀"
        elif memory_score >= 0.6:
            assessment["memory_management"] = "良好"
        else:
            assessment["memory_management"] = "需要改进"
        
        # 注意力焦点能力
        attention_focus = performance_analysis.get("attention_focus", {})
        focus_scores = list(attention_focus.get("focus_accuracy", {}).values())
        if focus_scores:
            avg_focus_score = sum(focus_scores) / len(focus_scores)
            if avg_focus_score >= 0.7:
                assessment["attention_focus"] = "优秀"
            elif avg_focus_score >= 0.5:
                assessment["attention_focus"] = "良好"
            else:
                assessment["attention_focus"] = "需要改进"
        
        return assessment
    
    def _generate_recommendations(self, performance_analysis: Dict[str, Any]) -> List[str]:
        """生成改进建议"""
        recommendations = []
        
        # 基于角色切换性能的建议
        role_switching = performance_analysis.get("role_switching", {})
        if role_switching.get("failed_switches", 0) > 0:
            recommendations.append("建议优化角色切换机制，提高切换成功率")
        
        # 基于记忆管理的建议
        memory_persistence = performance_analysis.get("memory_persistence", {})
        if memory_persistence.get("memory_continuity_score", 0) < 0.7:
            recommendations.append("建议加强记忆持续性管理，确保角色状态的连续性")
        
        if memory_persistence.get("cross_role_interference", 0) > 0.5:
            recommendations.append("建议改进角色隔离机制，减少跨角色信息干扰")
        
        # 基于注意力焦点的建议
        attention_focus = performance_analysis.get("attention_focus", {})
        focus_scores = list(attention_focus.get("focus_accuracy", {}).values())
        if focus_scores and min(focus_scores) < 0.5:
            recommendations.append("建议加强角色专业性训练，提高注意力焦点的准确性")
        
        if not recommendations:
            recommendations.append("整体表现良好，可以尝试更复杂的角色切换场景")
        
        return recommendations

def main():
    """主函数"""
    analyzer = DynamicRoleSwitchingAnalyzer()
    
    # 加载测试结果
    results = analyzer.load_test_results()
    if not results:
        print("未找到测试结果文件")
        return
    
    # 生成分析报告
    analysis = analyzer.generate_comprehensive_analysis(results)
    
    # 保存分析报告
    output_path = os.path.join(analyzer.testout_dir, "dynamic_role_switching_analysis.json")
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(analysis, f, ensure_ascii=False, indent=2)
    
    print(f"分析报告已保存到: {output_path}")
    
    # 打印简要总结
    print("\n=== 动态角色切换测试分析总结 ===")
    
    test_summary = analysis.get("test_summary", {})
    print(f"测试模型: {test_summary.get('model_tested', 'unknown')}")
    print(f"测试角色数: {test_summary.get('total_roles', 0)}")
    print(f"总切换次数: {test_summary.get('total_switches', 0)}")
    
    capability_assessment = analysis.get("capability_assessment", {})
    print(f"\n能力评估:")
    for capability, level in capability_assessment.items():
        print(f"  {capability}: {level}")
    
    recommendations = analysis.get("recommendations", [])
    print(f"\n改进建议:")
    for i, rec in enumerate(recommendations, 1):
        print(f"  {i}. {rec}")

if __name__ == "__main__":
    main()
