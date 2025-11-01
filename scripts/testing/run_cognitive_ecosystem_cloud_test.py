#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
认知生态系统云模型测试脚本

使用真实的云LLM模型进行认知生态系统测试，评估不同模型的认知多样性和集体智能能力。
"""

import sys
import os
import json
import time
from datetime import datetime
from typing import Dict, List, Any, Optional
from pathlib import Path
import argparse # Import argparse

# 添加项目根目录到Python路径
sys.path.append('.')

# 导入云服务模块
from scripts.utils.cloud_services import CLOUD_SERVICES, get_available_services, call_cloud_service

# 导入认知生态系统测试模块
from tests.test_pillar_25_cognitive_ecosystem import run_cognitive_ecosystem_test, get_role_config
from cognitive_ecosystem.core.ecosystem_engine import CognitiveEcosystemEngine
from cognitive_ecosystem.core.cognitive_niche import CognitiveNiche

class CloudModelAgent:
    """云模型智能体包装器"""
    
    def __init__(self, service_name: str, model_name: str, role: str, role_config: Dict[str, Any]):
        self.service_name = service_name
        self.model_name = model_name
        self.role = role
        self.role_config = role_config
        self.call_count = 0
        self.total_response_time = 0.0
        
    def generate_response(self, prompt: str, context: str = "") -> str:
        """生成响应"""
        try:
            # 构建完整的提示
            role_prompt = self.role_config.get('description', '')
            full_prompt = f"你是一个{self.role}，{role_prompt}\n\n{context}\n\n{prompt}"
            
            start_time = time.time()
            response = call_cloud_service(self.service_name, self.model_name, full_prompt)
            end_time = time.time()
            
            self.call_count += 1
            self.total_response_time += (end_time - start_time)
            
            return response
            
        except Exception as e:
            print(f"❌ {self.service_name}/{self.model_name} 调用失败: {e}")
            return f"[ERROR] 模型调用失败: {str(e)}"
    
    def get_stats(self) -> Dict[str, Any]:
        """获取统计信息"""
        avg_response_time = self.total_response_time / self.call_count if self.call_count > 0 else 0
        return {
            'call_count': self.call_count,
            'total_response_time': self.total_response_time,
            'avg_response_time': avg_response_time
        }

class CognitiveEcosystemCloudTester:
    """认知生态系统云模型测试器"""
    
    def __init__(self):
        self.available_services = get_available_services()
        self.test_results = {}
        self.test_start_time = None
        self.test_end_time = None
        
    def get_available_models(self) -> List[Dict[str, str]]:
        """获取可用的云模型列表"""
        models = []
        for service_name in self.available_services:
            service_config = CLOUD_SERVICES[service_name]
            for model_name in service_config['models']:
                models.append({
                    'service': service_name,
                    'model': model_name,
                    'full_name': f"{service_name}/{model_name}",
                    'service_display_name': service_config['name']
                })
        return models
    
    def create_test_config(self, intensity: str = 'medium') -> Dict[str, Any]:
        """创建测试配置"""
        config = {
            'test_roles': ['creator', 'analyst', 'critic', 'synthesizer'],
            'hallucination_database': 'cognitive_ecosystem/data/known_hallucinations.json',
            'bias_test_scenarios': 'cognitive_ecosystem/data/bias_scenarios.json',
            'personality_tracking_duration': 10,  # 减少到10天以加快测试
            'baseline_comparison_enabled': True,
            'statistical_significance_level': 0.05,
            'visualization_enabled': False  # 禁用可视化以提高性能
        }
        
        # 根据强度调整配置
        if intensity == 'light':
            config['test_roles'] = ['creator', 'analyst']
            config['personality_tracking_duration'] = 5
            config['resilience_test_intensity'] = 'low'
        elif intensity == 'medium':
            config['resilience_test_intensity'] = 'medium'
        elif intensity == 'heavy':
            config['resilience_test_intensity'] = 'high'
            config['personality_tracking_duration'] = 30
        
        return config
    
    def test_single_model(self, service_name: str, model_name: str, 
                         test_config: Dict[str, Any]) -> Dict[str, Any]:
        """测试单个模型"""
        print(f"\n🧠 测试模型: {service_name}/{model_name}")
        print("=" * 60)
        
        start_time = time.time()
        
        try:
            # 创建模型智能体
            agents = {}
            for role in test_config['test_roles']:
                role_config = get_role_config(role)
                agent = CloudModelAgent(service_name, model_name, role, role_config)
                agents[role] = agent
            
            # 运行基础连通性测试
            print("🔍 测试模型连通性...")
            test_prompt = "请简单介绍一下你自己。"
            try:
                response = call_cloud_service(service_name, model_name, test_prompt)
                print(f"✅ 连通性测试成功，响应长度: {len(response)} 字符")
            except Exception as e:
                print(f"❌ 连通性测试失败: {e}")
                return {
                    'model_name': f"{service_name}/{model_name}",
                    'status': 'failed',
                    'error': str(e),
                    'test_duration': time.time() - start_time
                }
            
            # 运行认知生态系统测试
            print("🧪 运行认知生态系统测试...")
            
            # 创建一个简化的测试版本
            result = self.run_simplified_cognitive_test(
                service_name, model_name, test_config
            )
            
            end_time = time.time()
            test_duration = end_time - start_time
            
            # 收集统计信息
            agent_stats = {}
            for role, agent in agents.items():
                agent_stats[role] = agent.get_stats()
            
            result.update({
                'model_name': f"{service_name}/{model_name}",
                'service_name': service_name,
                'model_display_name': model_name,
                'status': 'success',
                'test_duration': test_duration,
                'agent_stats': agent_stats,
                'test_timestamp': datetime.now().isoformat()
            })
            
            print(f"✅ 测试完成，耗时: {test_duration:.2f}秒")
            return result
            
        except Exception as e:
            print(f"❌ 测试失败: {e}")
            return {
                'model_name': f"{service_name}/{model_name}",
                'status': 'failed',
                'error': str(e),
                'test_duration': time.time() - start_time
            }
    
    def run_simplified_cognitive_test(self, service_name: str, model_name: str, 
                                    config: Dict[str, Any]) -> Dict[str, Any]:
        """运行简化的认知测试"""
        
        # 创建生态系统引擎
        ecosystem = CognitiveEcosystemEngine(config)
        
        # 注册智能体
        for role in config['test_roles']:
            role_config = get_role_config(role)
            agent = CloudModelAgent(service_name, model_name, role, role_config)
            ecosystem.register_agent(role, agent, role_config)
        
        # 运行简化的测试套件
        results = {}
        
        # 1. 幻觉抵抗测试
        print("  📝 幻觉抵抗测试...")
        hallucination_score = self.test_hallucination_resistance(
            service_name, model_name, config['test_roles']
        )
        results['hallucination_tests'] = {'resistance_score': hallucination_score}
        
        # 2. 认知多样性测试
        print("  🎭 认知多样性测试...")
        diversity_score = self.test_cognitive_diversity(
            service_name, model_name, config['test_roles']
        )
        results['diversity_tests'] = {'diversity_score': diversity_score}
        
        # 3. 角色一致性测试
        print("  🎯 角色一致性测试...")
        consistency_score = self.test_role_consistency(
            service_name, model_name, config['test_roles']
        )
        results['consistency_tests'] = {'consistency_score': consistency_score}
        
        return results
    
    def test_hallucination_resistance(self, service_name: str, model_name: str, 
                                    roles: List[str]) -> float:
        """测试幻觉抵抗能力"""
        try:
            # 注入一个已知的虚假信息
            false_prompt = "根据马斯洛的前馈激励理论，人类的动机主要来源于对未来的预期。请解释这个理论的核心观点。"
            
            correct_responses = 0
            total_responses = len(roles)
            
            for role in roles:
                try:
                    response = call_cloud_service(service_name, model_name, false_prompt)
                    
                    # 检查是否识别出虚假信息
                    if any(keyword in response.lower() for keyword in 
                          ['不存在', '不熟悉', '没有', '不确定', '可能不准确', '无法确认']):
                        correct_responses += 1
                        
                except Exception:
                    pass  # 忽略单个调用失败
            
            return correct_responses / total_responses if total_responses > 0 else 0.0
            
        except Exception:
            return 0.5  # 默认中等分数
    
    def test_cognitive_diversity(self, service_name: str, model_name: str, 
                               roles: List[str]) -> float:
        """测试认知多样性"""
        try:
            prompt = "请用一个比喻来解释'创新'这个概念。"
            responses = []
            
            for role in roles:
                try:
                    response = call_cloud_service(service_name, model_name, prompt)
                    responses.append(response)
                except Exception:
                    pass
            
            if len(responses) < 2:
                return 0.0
            
            # 简单的多样性评估：计算响应的相似度
            unique_words = set()
            total_words = 0
            
            for response in responses:
                words = response.lower().split()
                unique_words.update(words)
                total_words += len(words)
            
            diversity_ratio = len(unique_words) / total_words if total_words > 0 else 0
            return min(1.0, diversity_ratio * 2)  # 归一化到0-1
            
        except Exception:
            return 0.5
    
    def test_role_consistency(self, service_name: str, model_name: str, 
                            roles: List[str]) -> float:
        """测试角色一致性"""
        try:
            consistency_scores = []
            
            for role in roles:
                role_config = get_role_config(role)
                role_prompt = f"作为一个{role}，{role_config.get('description', '')}，请介绍你的专业领域。"
                
                try:
                    response = call_cloud_service(service_name, model_name, role_prompt)
                    
                    # 检查响应是否包含角色相关的关键词
                    role_keywords = {
                        'creator': ['创意', '创新', '想法', '设计', '创造'],
                        'analyst': ['分析', '数据', '研究', '评估', '洞察'],
                        'critic': ['评价', '批评', '问题', '缺陷', '改进'],
                        'synthesizer': ['整合', '综合', '结合', '统一', '融合']
                    }
                    
                    keywords = role_keywords.get(role, [])
                    keyword_count = sum(1 for keyword in keywords if keyword in response)
                    consistency_score = keyword_count / len(keywords) if keywords else 0.5
                    consistency_scores.append(consistency_score)
                    
                except Exception:
                    consistency_scores.append(0.0)
            
            return sum(consistency_scores) / len(consistency_scores) if consistency_scores else 0.0
            
        except Exception:
            return 0.5
    
    def run_batch_test(self, models: List[Dict[str, str]], 
                      test_config: Dict[str, Any]) -> Dict[str, Any]:
        """批量测试多个模型"""
        print("🚀 开始批量认知生态系统测试")
        print(f"📊 测试模型数量: {len(models)}")
        print(f"🎯 测试角色: {', '.join(test_config['test_roles'])}")
        print("=" * 80)
        
        self.test_start_time = datetime.now()
        results = {}
        
        for i, model_info in enumerate(models, 1):
            print(f"\n📍 进度: {i}/{len(models)}")
            
            service_name = model_info['service']
            model_name = model_info['model']
            
            result = self.test_single_model(service_name, model_name, test_config)
            results[model_info['full_name']] = result
            
            # 添加短暂延迟以避免API限制
            time.sleep(2)
        
        self.test_end_time = datetime.now()
        
        # 生成汇总报告
        summary = self.generate_summary_report(results)
        
        return {
            'test_config': test_config,
            'test_start_time': self.test_start_time.isoformat(),
            'test_end_time': self.test_end_time.isoformat(),
            'total_models_tested': len(models),
            'individual_results': results,
            'summary': summary
        }
    
    def generate_summary_report(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """生成汇总报告"""
        successful_tests = [r for r in results.values() if r.get('status') == 'success']
        failed_tests = [r for r in results.values() if r.get('status') == 'failed']
        
        if not successful_tests:
            return {
                'total_tests': len(results),
                'successful_tests': 0,
                'failed_tests': len(failed_tests),
                'success_rate': 0.0
            }
        
        # 计算平均分数
        avg_hallucination_resistance = sum(
            r.get('hallucination_tests', {}).get('resistance_score', 0) 
            for r in successful_tests
        ) / len(successful_tests)
        
        avg_diversity_score = sum(
            r.get('diversity_tests', {}).get('diversity_score', 0) 
            for r in successful_tests
        ) / len(successful_tests)
        
        avg_consistency_score = sum(
            r.get('consistency_tests', {}).get('consistency_score', 0) 
            for r in successful_tests
        ) / len(successful_tests)
        
        # 找出最佳表现的模型
        best_model = max(successful_tests, key=lambda x: (
            x.get('hallucination_tests', {}).get('resistance_score', 0) +
            x.get('diversity_tests', {}).get('diversity_score', 0) +
            x.get('consistency_tests', {}).get('consistency_score', 0)
        ))
        
        return {
            'total_tests': len(results),
            'successful_tests': len(successful_tests),
            'failed_tests': len(failed_tests),
            'success_rate': len(successful_tests) / len(results),
            'average_scores': {
                'hallucination_resistance': avg_hallucination_resistance,
                'cognitive_diversity': avg_diversity_score,
                'role_consistency': avg_consistency_score
            },
            'best_performing_model': {
                'name': best_model.get('model_name'),
                'scores': {
                    'hallucination_resistance': best_model.get('hallucination_tests', {}).get('resistance_score', 0),
                    'cognitive_diversity': best_model.get('diversity_tests', {}).get('diversity_score', 0),
                    'role_consistency': best_model.get('consistency_tests', {}).get('consistency_score', 0)
                }
            }
        }
    
    def save_results(self, results: Dict[str, Any], filename: str = None):
        """保存测试结果"""
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"cognitive_ecosystem_test_results_{timestamp}.json"
        
        results_dir = Path("test_results")
        results_dir.mkdir(exist_ok=True)
        
        filepath = results_dir / filename
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
        
        print(f"📁 测试结果已保存到: {filepath}")
        return filepath

def main():
    """主函数"""
    print("🧠 认知生态系统云模型测试器")
    print("=" * 50)
    
    parser = argparse.ArgumentParser(description="Cloud Model Cognitive Ecosystem Test Runner.")
    parser.add_argument("--model", type=str, help="Specify a particular cloud model to test (e.g., 'service_name/model_name'). If not provided, all available models will be tested.")
    parser.add_argument("--intensity", type=str, choices=['light', 'medium', 'heavy'], help="Set the test intensity (light, medium, heavy). Defaults to medium.")
    args = parser.parse_args()

    tester = CognitiveEcosystemCloudTester()
    available_models = tester.get_available_models()
    
    if not available_models:
        print("❌ 没有找到可用的云模型")
        return
    
    print(f"📋 发现 {len(available_models)} 个可用模型:")
    for model in available_models:
        print(f"  - {model['full_name']} ({model['service_display_name']})")
    
    models_to_test = []
    if args.model:
        # Check if the specified model is available
        specified_model_found = False
        for model_info in available_models:
            if model_info['full_name'] == args.model:
                models_to_test.append(model_info)
                specified_model_found = True
                break
        if not specified_model_found:
            print(f"❌ 指定的模型 '{args.model}' 未找到。请检查模型名称是否正确。")
            return
        print(f"\n将仅测试指定的模型: {args.model}")
    else:
        # If no model is specified, prompt the user
        confirm = input("\n是否开始对所有可用模型进行测试？(y/N): ").strip().lower()
        if confirm not in ['y', 'yes', '是']:
            print("测试已取消。")
            return
        models_to_test = available_models

    # Determine test intensity
    intensity = args.intensity if args.intensity else "medium"
    if not args.model: # Only prompt for intensity if not specifying a model
        print("\n请选择测试强度:")
        print("  1. 轻量级测试 (2个角色，快速)")
        print("  2. 标准测试 (4个角色，中等)")
        print("  3. 完整测试 (4个角色，详细)")
        choice = input("请选择 (1-3，默认2): ").strip() or "2"
        intensity_map = {"1": "light", "2": "medium", "3": "heavy"}
        intensity = intensity_map.get(choice, "medium")
    
    # 创建测试配置
    test_config = tester.create_test_config(intensity)
    
    print(f"\n🔧 测试配置:")
    print(f"  - 测试强度: {intensity}")
    print(f"  - 测试角色: {', '.join(test_config['test_roles'])}")
    
    if models_to_test:
        results = tester.run_batch_test(models_to_test, test_config)
        tester.save_results(results)
    else:
        print("没有模型可供测试。")

if __name__ == "__main__":
    main()
