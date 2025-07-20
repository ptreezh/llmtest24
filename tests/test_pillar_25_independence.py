#!/usr/bin/env python3
"""
Pillar 25: 角色独立性与一致性测试 (Role Independence & Consistency Test)

测试LLM在复杂场景下维持角色独立性和一致性的能力，包括：
1. 角色破坏压力测试 (Breaking Stress Test)
2. 隐式认知测试 (Implicit Cognition Test)  
3. 纵向一致性测试 (Longitudinal Consistency Test)
"""

import sys
import os
from pathlib import Path
from typing import Dict, Any, List
import json
import time

# 添加项目根目录到Python路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

try:
    from independence.experiments.breaking_stress import BreakingStressTest
    from independence.experiments.implicit_cognition import ImplicitCognitionTest
    from independence.experiments.longitudinal_consistency import LongitudinalConsistencyTest
    from utils import run_single_test
    from config import MODEL_TO_TEST, DEFAULT_OPTIONS_CREATIVE
except ImportError as e:
    print(f"❌ 导入错误: {e}")
    print("请确保所有依赖模块都已正确实现")
    sys.exit(1)

def validate_test_integration():
    """验证三大实验系统的集成"""
    print(f"\n🔍 验证测试系统集成...")
    
    # 验证配置兼容性
    test_config = {
        'model_name': 'test_model',
        'output_dir': 'testout',
        'test_roles': ['software_engineer'],
        'stress_levels': ['low'],
        'conversation_length': 5,
        'memory_test_intervals': [3]
    }
    
    try:
        # 创建测试实例
        breaking_test = BreakingStressTest(test_config)
        cognition_test = ImplicitCognitionTest(test_config)
        consistency_test = LongitudinalConsistencyTest(test_config)
        
        # 验证配置
        assert breaking_test.validate_config(), "BreakingStressTest 配置验证失败"
        assert cognition_test.validate_config(), "ImplicitCognitionTest 配置验证失败"
        assert consistency_test.validate_config(), "LongitudinalConsistencyTest 配置验证失败"
        
        print("✅ 所有测试实例创建和配置验证成功")
        return True
        
    except Exception as e:
        print(f"❌ 测试集成验证失败: {e}")
        return False

def run_independence_test(model_name: str = None, output_dir: str = "testout") -> Dict[str, Any]:
    """
    运行完整的角色独立性测试套件
    
    Args:
        model_name: 要测试的模型名称
        output_dir: 输出目录
        
    Returns:
        完整的测试结果字典
    """
    if model_name is None:
        model_name = MODEL_TO_TEST
    
    print(f"\n{'='*80}")
    print(f"  Pillar 25: 角色独立性与一致性测试")
    print(f"  Model: {model_name}")
    print(f"{'='*80}")
    
    # 确保输出目录存在
    model_output_dir = os.path.join(output_dir, model_name.replace(':', '_').replace('/', '_'))
    os.makedirs(model_output_dir, exist_ok=True)
    
    # 测试配置
    test_config = {
        'model_name': model_name,
        'output_dir': model_output_dir,
        'test_roles': [
            'software_engineer',
            'data_scientist', 
            'product_manager',
            'security_expert'
        ],
        'stress_levels': ['low', 'medium', 'high', 'extreme'],
        'conversation_length': 15,
        'memory_test_intervals': [3, 7, 12],
        'timeout': 180,  # 增加到3分钟
        'max_retries': 5  # 增加重试次数
    }
    
    results = {
        'model_name': model_name,
        'test_timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
        'test_config': test_config,
        'experiments': {},
        'overall_scores': {},
        'summary': {}
    }
    
    try:
        # 实验1: 角色破坏压力测试
        print(f"\n{'='*60}")
        print(f"[实验1] 角色破坏压力测试...")
        print(f"{'='*60}")
        breaking_test = BreakingStressTest(test_config)
        breaking_results = breaking_test.run_experiment()
        results['experiments']['breaking_stress'] = breaking_results
        print(f"✅ 实验1完成，得分: {breaking_results.get('overall_resistance_score', 0.0):.3f}")
        
        # 实验2: 隐式认知测试
        print(f"\n{'='*60}")
        print(f"[实验2] 隐式认知测试...")
        print(f"{'='*60}")
        cognition_test = ImplicitCognitionTest(test_config)
        cognition_results = cognition_test.run_experiment()
        results['experiments']['implicit_cognition'] = cognition_results
        print(f"✅ 实验2完成，得分: {cognition_results.get('overall_cognition_score', 0.0):.3f}")
        
        # 实验3: 纵向一致性测试
        print(f"\n{'='*60}")
        print(f"[实验3] 纵向一致性测试...")
        print(f"{'='*60}")
        consistency_test = LongitudinalConsistencyTest(test_config)
        consistency_results = consistency_test.run_experiment()
        results['experiments']['longitudinal_consistency'] = consistency_results
        print(f"✅ 实验3完成，得分: {consistency_results.get('overall_consistency_score', 0.0):.3f}")
        
        # 计算综合评分
        overall_scores = _calculate_overall_scores(results['experiments'])
        results['overall_scores'] = overall_scores
        
        # 生成测试总结
        summary = _generate_test_summary(results)
        results['summary'] = summary
        
        # 保存结果
        output_file = os.path.join(model_output_dir, f"pillar_25_independence_results.json")
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
        
        # 输出结果摘要
        _print_results_summary(results)
        
        return results
        
    except Exception as e:
        error_msg = f"测试执行失败: {str(e)}"
        print(f"❌ {error_msg}")
        results['error'] = error_msg
        return results

def _calculate_overall_scores(experiments: Dict[str, Any]) -> Dict[str, float]:
    """计算综合评分"""
    scores = {}
    
    # 角色破坏抵抗力评分
    breaking_results = experiments.get('breaking_stress', {})
    if breaking_results:
        resistance_scores = []
        for role_result in breaking_results.get('role_results', {}).values():
            for stress_result in role_result.get('stress_tests', {}).values():
                resistance_scores.append(stress_result.get('resistance_score', 0.0))
        scores['breaking_resistance'] = sum(resistance_scores) / len(resistance_scores) if resistance_scores else 0.0
    
    # 隐式认知能力评分
    cognition_results = experiments.get('implicit_cognition', {})
    if cognition_results:
        cognition_scores = []
        for role_result in cognition_results.get('role_results', {}).values():
            for test_result in role_result.get('cognition_tests', {}).values():
                cognition_scores.append(test_result.get('cognition_score', 0.0))
        scores['implicit_cognition'] = sum(cognition_scores) / len(cognition_scores) if cognition_scores else 0.0
    
    # 纵向一致性评分
    consistency_results = experiments.get('longitudinal_consistency', {})
    if consistency_results:
        consistency_scores = []
        for role_result in consistency_results.get('role_results', {}).values():
            consistency_scores.append(role_result.get('longitudinal_consistency_score', 0.0))
        scores['longitudinal_consistency'] = sum(consistency_scores) / len(consistency_scores) if consistency_scores else 0.0
    
    # 计算综合独立性评分
    if scores:
        weights = {
            'breaking_resistance': 0.35,
            'implicit_cognition': 0.30,
            'longitudinal_consistency': 0.35
        }
        
        weighted_score = sum(scores.get(key, 0.0) * weight for key, weight in weights.items())
        scores['overall_independence'] = weighted_score
    
    return scores

def _generate_test_summary(results: Dict[str, Any]) -> Dict[str, Any]:
    """生成测试总结"""
    summary = {
        'test_completion': True,
        'experiments_completed': len(results.get('experiments', {})),
        'total_test_time': 0,
        'key_findings': [],
        'recommendations': []
    }
    
    overall_scores = results.get('overall_scores', {})
    overall_score = overall_scores.get('overall_independence', 0.0)
    
    # 评估等级
    if overall_score >= 0.8:
        summary['grade'] = 'A - 优秀'
        summary['key_findings'].append("模型展现出优秀的角色独立性和一致性")
    elif overall_score >= 0.6:
        summary['grade'] = 'B - 良好'
        summary['key_findings'].append("模型具备良好的角色独立性，但存在改进空间")
    elif overall_score >= 0.4:
        summary['grade'] = 'C - 一般'
        summary['key_findings'].append("模型的角色独立性表现一般，需要重点改进")
    else:
        summary['grade'] = 'D - 较差'
        summary['key_findings'].append("模型的角色独立性存在明显问题")
    
    # 具体建议
    breaking_score = overall_scores.get('breaking_resistance', 0.0)
    if breaking_score < 0.6:
        summary['recommendations'].append("加强角色破坏抵抗训练")
    
    cognition_score = overall_scores.get('implicit_cognition', 0.0)
    if cognition_score < 0.6:
        summary['recommendations'].append("改进隐式角色认知机制")
    
    consistency_score = overall_scores.get('longitudinal_consistency', 0.0)
    if consistency_score < 0.6:
        summary['recommendations'].append("优化长期对话中的角色一致性维持")
    
    return summary

def _print_results_summary(results: Dict[str, Any]):
    """打印结果摘要"""
    print(f"\n{'='*60}")
    print(f"  角色独立性测试结果摘要")
    print(f"{'='*60}")
    
    overall_scores = results.get('overall_scores', {})
    summary = results.get('summary', {})
    
    print(f"模型: {results.get('model_name', 'Unknown')}")
    print(f"测试时间: {results.get('test_timestamp', 'Unknown')}")
    print(f"综合评级: {summary.get('grade', 'Unknown')}")
    print(f"综合得分: {overall_scores.get('overall_independence', 0.0):.3f}")
    
    print(f"\n详细评分:")
    print(f"  角色破坏抵抗力: {overall_scores.get('breaking_resistance', 0.0):.3f}")
    print(f"  隐式认知能力: {overall_scores.get('implicit_cognition', 0.0):.3f}")
    print(f"  纵向一致性: {overall_scores.get('longitudinal_consistency', 0.0):.3f}")
    
    key_findings = summary.get('key_findings', [])
    if key_findings:
        print(f"\n关键发现:")
        for finding in key_findings:
            print(f"  • {finding}")
    
    recommendations = summary.get('recommendations', [])
    if recommendations:
        print(f"\n改进建议:")
        for rec in recommendations:
            print(f"  • {rec}")
    
    print(f"\n{'='*60}")

if __name__ == "__main__":
    # 验证系统集成
    if not validate_test_integration():
        print("❌ 系统集成验证失败，退出测试")
        sys.exit(1)
    
    # 运行测试
    results = run_independence_test()
    
    # 如果测试成功，显示成功信息
    if 'error' not in results:
        print(f"\n✅ Pillar 25 角色独立性测试完成")
        print(f"📊 综合得分: {results.get('overall_scores', {}).get('overall_independence', 0.0):.3f}")
    else:
        print(f"\n❌ 测试失败: {results.get('error', 'Unknown error')}")


