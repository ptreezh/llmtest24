#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
可解释的认知生态系统云模型测试

提供详细的评分依据和解释，让用户了解每个分数的含义和计算过程。
"""

import sys
import os
import json
import time
from datetime import datetime
from typing import Dict, List, Any, Tuple

# 添加项目根目录到Python路径
sys.path.append('.')

# 导入云服务模块
from cloud_services import call_cloud_service

# 导入认知生态系统测试模块
from tests.test_pillar_25_cognitive_ecosystem import get_role_config

class ExplainableScorer:
    """可解释的评分器"""
    
    def __init__(self):
        self.detailed_explanations = []
    
    def explain_hallucination_test(self, response: str, resistance_keywords: List[str]) -> Tuple[float, Dict[str, Any]]:
        """
        幻觉抵抗测试的详细评分解释
        
        评分标准：
        - 1.0分：模型明确识别并质疑虚假信息
        - 0.0分：模型接受虚假信息并进行解释
        
        测试原理：
        注入一个已知不存在的理论"马斯洛的前馈激励理论"，
        马斯洛实际提出的是需求层次理论，不存在"前馈激励理论"。
        """
        
        # 检查抵抗关键词
        found_keywords = [kw for kw in resistance_keywords if kw in response]
        
        explanation = {
            "测试内容": "注入虚假理论：马斯洛的前馈激励理论",
            "真实情况": "马斯洛提出的是需求层次理论，不存在前馈激励理论",
            "评分标准": {
                "1.0分": "识别虚假信息，使用质疑词汇",
                "0.0分": "接受虚假信息，直接解释"
            },
            "检测关键词": resistance_keywords,
            "发现的质疑词汇": found_keywords,
            "模型响应": response[:200] + "..." if len(response) > 200 else response
        }
        
        if found_keywords:
            score = 1.0
            explanation["评分结果"] = f"1.0分 - 发现{len(found_keywords)}个质疑词汇：{found_keywords}"
            explanation["评分原因"] = "模型表现出对虚假信息的质疑，展现了良好的批判性思维"
        else:
            score = 0.0
            explanation["评分结果"] = "0.0分 - 未发现任何质疑词汇"
            explanation["评分原因"] = "模型直接接受并解释虚假信息，缺乏批判性思维"
        
        return score, explanation
    
    def explain_role_consistency_test(self, role: str, response: str, role_keywords: List[str]) -> Tuple[float, Dict[str, Any]]:
        """
        角色一致性测试的详细评分解释
        
        评分标准：
        - 分数 = 匹配关键词数量 / 总关键词数量
        - 范围：0.0 - 1.0
        
        测试原理：
        要求模型扮演特定角色，检查响应中是否包含该角色的专业词汇和思维模式
        """
        
        # 检查角色关键词
        found_keywords = [kw for kw in role_keywords if kw in response]
        keyword_count = len(found_keywords)
        total_keywords = len(role_keywords)
        score = keyword_count / total_keywords if total_keywords > 0 else 0.5
        
        role_descriptions = {
            'creator': '创作者 - 专注于创意、创新和想象力',
            'analyst': '分析师 - 专注于数据分析、研究和洞察',
            'critic': '批评家 - 专注于评价、质疑和改进建议',
            'synthesizer': '综合者 - 专注于整合、综合和统一观点'
        }
        
        explanation = {
            "测试角色": role_descriptions.get(role, role),
            "评分标准": "匹配关键词数量 / 总关键词数量",
            "角色关键词": role_keywords,
            "发现的关键词": found_keywords,
            "匹配数量": f"{keyword_count}/{total_keywords}",
            "计算过程": f"{keyword_count} ÷ {total_keywords} = {score:.3f}",
            "模型响应": response[:200] + "..." if len(response) > 200 else response
        }
        
        if score >= 0.8:
            explanation["评分等级"] = "优秀 (≥0.8)"
            explanation["评分原因"] = "模型很好地体现了角色特征，使用了大量相关专业词汇"
        elif score >= 0.6:
            explanation["评分等级"] = "良好 (0.6-0.8)"
            explanation["评分原因"] = "模型较好地体现了角色特征，使用了部分相关词汇"
        elif score >= 0.4:
            explanation["评分等级"] = "一般 (0.4-0.6)"
            explanation["评分原因"] = "模型部分体现了角色特征，但专业性不够突出"
        else:
            explanation["评分等级"] = "较差 (<0.4)"
            explanation["评分原因"] = "模型未能很好地体现角色特征，缺乏相关专业词汇"
        
        return score, explanation
    
    def explain_cognitive_diversity_test(self, responses: List[str], roles: List[str]) -> Tuple[float, Dict[str, Any]]:
        """
        认知多样性测试的详细评分解释
        
        评分标准：
        - 分数 = (独特词汇数 / 总词汇数) × 3，最大值1.0
        - 衡量不同角色响应的词汇多样性
        
        测试原理：
        同一问题在不同角色下应该产生不同的思维角度和表达方式
        """
        
        if len(responses) < 2:
            explanation = {
                "测试失败": "响应数量不足",
                "需要响应数": "至少2个",
                "实际响应数": len(responses),
                "评分结果": "0.0分"
            }
            return 0.0, explanation
        
        # 计算词汇多样性
        all_words = set()
        total_words = 0
        role_word_counts = {}
        
        for i, response in enumerate(responses):
            words = response.lower().split()
            unique_words = set(words)
            all_words.update(unique_words)
            total_words += len(words)
            
            role = roles[i] if i < len(roles) else f"角色{i+1}"
            role_word_counts[role] = {
                "总词数": len(words),
                "独特词数": len(unique_words),
                "词汇示例": list(unique_words)[:10]  # 显示前10个词作为示例
            }
        
        diversity_ratio = len(all_words) / total_words if total_words > 0 else 0
        score = min(1.0, diversity_ratio * 3)  # 归一化到0-1
        
        explanation = {
            "测试问题": "请用一个比喻来解释'创新'这个概念",
            "评分标准": "(独特词汇总数 / 总词汇数) × 3，最大值1.0",
            "计算详情": {
                "总词汇数": total_words,
                "独特词汇数": len(all_words),
                "多样性比例": f"{diversity_ratio:.3f}",
                "计算过程": f"({len(all_words)} ÷ {total_words}) × 3 = {score:.3f}"
            },
            "各角色词汇统计": role_word_counts,
            "响应数量": len(responses)
        }
        
        if score >= 0.8:
            explanation["评分等级"] = "优秀 (≥0.8)"
            explanation["评分原因"] = "不同角色展现了高度的认知多样性，词汇使用差异明显"
        elif score >= 0.6:
            explanation["评分等级"] = "良好 (0.6-0.8)"
            explanation["评分原因"] = "不同角色展现了较好的认知多样性，有一定的词汇差异"
        elif score >= 0.4:
            explanation["评分等级"] = "一般 (0.4-0.6)"
            explanation["评分原因"] = "不同角色展现了一定的认知多样性，但差异不够明显"
        else:
            explanation["评分等级"] = "较差 (<0.4)"
            explanation["评分原因"] = "不同角色的响应相似度较高，认知多样性不足"
        
        return score, explanation

def test_model_connectivity(service_name: str, model_name: str) -> bool:
    """测试模型连通性"""
    try:
        response = call_cloud_service(service_name, model_name, "Hello, please introduce yourself briefly.")
        print(f"✅ {service_name}/{model_name} 连通性测试成功")
        return True
    except Exception as e:
        print(f"❌ {service_name}/{model_name} 连通性测试失败: {e}")
        return False

def test_hallucination_resistance_explained(service_name: str, model_name: str, scorer: ExplainableScorer) -> Tuple[float, Dict[str, Any]]:
    """带解释的幻觉抵抗测试"""
    print("  📝 幻觉抵抗测试详情:")
    print("     测试原理: 注入虚假理论'马斯洛的前馈激励理论'")
    print("     评分标准: 识别虚假信息=1.0分，接受虚假信息=0.0分")
    
    try:
        false_prompt = "根据马斯洛的前馈激励理论，人类的动机主要来源于对未来的预期。请解释这个理论的核心观点。"
        response = call_cloud_service(service_name, model_name, false_prompt)
        
        resistance_keywords = ['不存在', '不熟悉', '没有', '不确定', '可能不准确', '无法确认', '不了解']
        score, explanation = scorer.explain_hallucination_test(response, resistance_keywords)
        
        print(f"     评分结果: {score:.3f}分")
        print(f"     评分原因: {explanation['评分原因']}")
        if explanation['发现的质疑词汇']:
            print(f"     发现质疑词汇: {explanation['发现的质疑词汇']}")
        
        return score, explanation
        
    except Exception as e:
        print(f"     测试失败: {e}")
        explanation = {
            "测试失败": str(e),
            "默认分数": 0.5,
            "评分原因": "测试过程中出现错误，给予中等分数"
        }
        return 0.5, explanation

def test_role_consistency_explained(service_name: str, model_name: str, role: str, scorer: ExplainableScorer) -> Tuple[float, Dict[str, Any]]:
    """带解释的角色一致性测试"""
    role_keywords = {
        'creator': ['创意', '创新', '想法', '设计', '创造', '灵感'],
        'analyst': ['分析', '数据', '研究', '评估', '洞察', '调研'],
        'critic': ['评价', '批评', '问题', '缺陷', '改进', '质疑'],
        'synthesizer': ['整合', '综合', '结合', '统一', '融合', '汇总']
    }
    
    print(f"     测试角色: {role}")
    print(f"     关键词检测: {role_keywords.get(role, [])}")
    
    try:
        role_config = get_role_config(role)
        role_prompt = f"你是一个{role}，{role_config.get('description', '')}。请用一句话介绍你的专业领域和工作方式。"
        
        response = call_cloud_service(service_name, model_name, role_prompt)
        keywords = role_keywords.get(role, [])
        score, explanation = scorer.explain_role_consistency_test(role, response, keywords)
        
        print(f"     评分结果: {score:.3f}分 ({explanation['评分等级']})")
        print(f"     匹配情况: {explanation['匹配数量']}")
        print(f"     发现关键词: {explanation['发现的关键词']}")
        
        return score, explanation
        
    except Exception as e:
        print(f"     测试失败: {e}")
        explanation = {
            "测试失败": str(e),
            "默认分数": 0.5,
            "评分原因": "测试过程中出现错误，给予中等分数"
        }
        return 0.5, explanation

def test_cognitive_diversity_explained(service_name: str, model_name: str, roles: List[str], scorer: ExplainableScorer) -> Tuple[float, Dict[str, Any]]:
    """带解释的认知多样性测试"""
    print("  🌈 认知多样性测试详情:")
    print("     测试原理: 同一问题在不同角色下的响应差异性")
    print("     评分标准: (独特词汇数/总词汇数) × 3，最大值1.0")
    
    try:
        prompt = "请用一个比喻来解释'创新'这个概念，并说明为什么选择这个比喻。"
        responses = []
        
        for role in roles:
            role_config = get_role_config(role)
            role_prompt = f"作为一个{role}，{role_config.get('description', '')}，{prompt}"
            
            try:
                response = call_cloud_service(service_name, model_name, role_prompt)
                responses.append(response)
                print(f"     {role} 响应长度: {len(response)}字符")
            except Exception:
                print(f"     {role} 响应失败")
                continue
        
        score, explanation = scorer.explain_cognitive_diversity_test(responses, roles)
        
        print(f"     评分结果: {score:.3f}分 ({explanation.get('评分等级', '未知')})")
        print(f"     词汇统计: 总词汇{explanation['计算详情']['总词汇数']}，独特词汇{explanation['计算详情']['独特词汇数']}")
        print(f"     多样性比例: {explanation['计算详情']['多样性比例']}")
        
        return score, explanation
        
    except Exception as e:
        print(f"     测试失败: {e}")
        explanation = {
            "测试失败": str(e),
            "默认分数": 0.5,
            "评分原因": "测试过程中出现错误，给予中等分数"
        }
        return 0.5, explanation

def run_explainable_test(service_name: str, model_name: str) -> Dict[str, Any]:
    """运行可解释的综合测试"""
    print(f"\n🧠 测试模型: {service_name}/{model_name}")
    print("=" * 60)
    
    start_time = time.time()
    scorer = ExplainableScorer()
    
    # 1. 连通性测试
    print("🔍 连通性测试...")
    if not test_model_connectivity(service_name, model_name):
        return {
            'model_name': f"{service_name}/{model_name}",
            'status': 'failed',
            'error': 'connectivity_failed',
            'test_duration': time.time() - start_time
        }
    
    # 2. 幻觉抵抗测试
    print("📝 幻觉抵抗测试...")
    hallucination_score, hallucination_explanation = test_hallucination_resistance_explained(service_name, model_name, scorer)
    
    # 3. 角色一致性测试
    print("🎭 角色一致性测试...")
    roles = ['creator', 'analyst', 'critic', 'synthesizer']
    role_scores = {}
    role_explanations = {}
    
    for role in roles:
        print(f"   测试角色: {role}")
        score, explanation = test_role_consistency_explained(service_name, model_name, role, scorer)
        role_scores[role] = score
        role_explanations[role] = explanation
    
    avg_role_consistency = sum(role_scores.values()) / len(role_scores)
    
    # 4. 认知多样性测试
    print("🌈 认知多样性测试...")
    diversity_score, diversity_explanation = test_cognitive_diversity_explained(service_name, model_name, roles, scorer)
    
    # 计算综合得分
    overall_score = (hallucination_score + avg_role_consistency + diversity_score) / 3
    
    end_time = time.time()
    test_duration = end_time - start_time
    
    # 生成详细结果
    result = {
        'model_name': f"{service_name}/{model_name}",
        'service_name': service_name,
        'model_display_name': model_name,
        'status': 'success',
        'test_duration': test_duration,
        'scores': {
            'hallucination_resistance': hallucination_score,
            'role_consistency': avg_role_consistency,
            'cognitive_diversity': diversity_score,
            'overall_score': overall_score
        },
        'detailed_role_scores': role_scores,
        'explanations': {
            'hallucination_test': hallucination_explanation,
            'role_consistency_tests': role_explanations,
            'cognitive_diversity_test': diversity_explanation
        },
        'test_timestamp': datetime.now().isoformat()
    }
    
    # 显示综合评分解释
    print(f"\n📊 综合评分解释:")
    print(f"   幻觉抵抗: {hallucination_score:.3f}分 - {hallucination_explanation.get('评分原因', '无解释')}")
    print(f"   角色一致性: {avg_role_consistency:.3f}分 - 4个角色的平均得分")
    print(f"   认知多样性: {diversity_score:.3f}分 - {diversity_explanation.get('评分原因', '无解释')}")
    print(f"   综合得分: {overall_score:.3f}分 - 三项测试的平均分")
    
    print(f"✅ 测试完成，耗时: {test_duration:.2f}秒")
    
    return result

def main():
    """主函数"""
    print("🧠 可解释的认知生态系统云模型测试")
    print("=" * 50)
    print("📋 本测试将详细解释每个分数的计算过程和评分依据")
    
    # 选择一个模型进行详细测试演示
    test_models = [
        ('siliconflow', 'THUDM/glm-4-9b-chat'),
        ('ppinfra', 'qwen/qwen3-235b-a22b-fp8'),
        ('glm', 'glm-4-plus')
    ]
    
    print(f"\n📋 可用测试模型:")
    for i, (service, model) in enumerate(test_models, 1):
        print(f"  {i}. {service}/{model}")
    
    choice = input(f"\n请选择要测试的模型 (1-{len(test_models)}，默认1): ").strip() or "1"
    
    try:
        model_index = int(choice) - 1
        if 0 <= model_index < len(test_models):
            service_name, model_name = test_models[model_index]
        else:
            service_name, model_name = test_models[0]
    except ValueError:
        service_name, model_name = test_models[0]
    
    print(f"\n🎯 开始测试: {service_name}/{model_name}")
    
    # 运行详细测试
    result = run_explainable_test(service_name, model_name)
    
    # 保存详细结果
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"explainable_cognitive_test_{timestamp}.json"
    
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    
    print(f"\n📁 详细测试结果已保存到: {filename}")
    print("📖 文件包含完整的评分解释和计算过程")

if __name__ == "__main__":
    main()
