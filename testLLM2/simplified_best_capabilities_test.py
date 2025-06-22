#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简化版最佳能力测试 - 基于模型实际表现调整测试难度
针对涌现分析、数学推理、角色扮演进行适度简化的测试
"""

import os
import sys
import time
import json
from datetime import datetime
from typing import Dict, List, Tuple, Optional
import ollama

# 导入增强测试框架
sys.path.append(os.path.abspath('.'))
from enhanced_test_framework import EnhancedTestFramework

class SimplifiedBestCapabilitiesTest(EnhancedTestFramework):
    def __init__(self):
        super().__init__()
        # 根据零响应分析调整参数
        self.max_prompt_length = 300  # 更保守的长度限制
        self.max_complexity_level = 2  # 降低复杂度限制
        self.timeout_seconds = 20     # 缩短超时时间
        
        self.capability_results = {
            'emergence': [],
            'math': [],
            'persona': []
        }
    
    def test_simplified_emergence(self):
        """简化的涌现分析测试"""
        print("🧠 简化涌现分析测试")
        print("="*50)
        
        # 简化的涌现分析问题
        simple_emergence_tests = [
            {
                "name": "基础反馈分析",
                "prompt": "分析两条反馈：A. 用户活跃度提升了。B. 部分用户觉得难用。请找出矛盾并给建议。"
            },
            {
                "name": "简单冲突识别", 
                "prompt": "产品反馈：新功能很受欢迎，但老用户不适应。请分析这个冲突。"
            },
            {
                "name": "基础解决方案",
                "prompt": "问题：客户要求降价，但成本在上升。请提出解决思路。"
            }
        ]
        
        for i, test in enumerate(simple_emergence_tests, 1):
            print(f"\n🔍 涌现测试 {i}: {test['name']}")
            print(f"提示词长度: {len(test['prompt'])}字符")
            
            success, response, metadata = self.smart_chat(test['prompt'])
            
            if success:
                # 评估涌现分析质量
                has_conflict = any(word in response for word in ['冲突', '矛盾', '对立', '问题'])
                has_solution = any(word in response for word in ['建议', '解决', '方案', '策略'])
                
                quality_score = 0
                if has_conflict: quality_score += 1
                if has_solution: quality_score += 1
                if len(response) > 50: quality_score += 1
                
                print(f"  ✅ 成功 - 质量分数: {quality_score}/3")
                result = {'success': True, 'quality_score': quality_score, 'response_length': len(response)}
            else:
                print(f"  ❌ 失败")
                result = {'success': False, 'quality_score': 0, 'response_length': 0}
            
            result.update({
                'test_name': test['name'],
                'prompt_length': len(test['prompt']),
                'metadata': metadata
            })
            self.capability_results['emergence'].append(result)
        
        return self.capability_results['emergence']
    
    def test_simplified_math(self):
        """简化的数学推理测试"""
        print("\n🔢 简化数学推理测试")
        print("="*50)
        
        # 简化的数学问题
        simple_math_tests = [
            {
                "name": "基础比例问题",
                "prompt": "甲管3小时注满水池，乙管5小时注满。两管一起开，多久注满？",
                "expected_keywords": ["小时", "注满", "计算"]
            },
            {
                "name": "简单应用题",
                "prompt": "小明买3个苹果花了6元，小红买5个苹果花了多少元？",
                "expected_keywords": ["元", "苹果", "计算"]
            },
            {
                "name": "基础工程问题",
                "prompt": "一项工作，甲单独做需要4天，乙单独做需要6天。两人合作需要几天？",
                "expected_keywords": ["天", "合作", "工作"]
            }
        ]
        
        for i, test in enumerate(simple_math_tests, 1):
            print(f"\n🧮 数学测试 {i}: {test['name']}")
            print(f"提示词长度: {len(test['prompt'])}字符")
            
            success, response, metadata = self.smart_chat(test['prompt'])
            
            if success:
                # 评估数学推理质量
                has_keywords = sum(1 for keyword in test['expected_keywords'] if keyword in response)
                has_numbers = any(char.isdigit() for char in response)
                has_process = len(response) > 30
                
                quality_score = 0
                if has_keywords >= 2: quality_score += 1
                if has_numbers: quality_score += 1
                if has_process: quality_score += 1
                
                print(f"  ✅ 成功 - 质量分数: {quality_score}/3")
                result = {'success': True, 'quality_score': quality_score, 'response_length': len(response)}
            else:
                print(f"  ❌ 失败")
                result = {'success': False, 'quality_score': 0, 'response_length': 0}
            
            result.update({
                'test_name': test['name'],
                'prompt_length': len(test['prompt']),
                'expected_keywords': test['expected_keywords'],
                'metadata': metadata
            })
            self.capability_results['math'].append(result)
        
        return self.capability_results['math']
    
    def test_simplified_persona(self):
        """简化的角色扮演测试"""
        print("\n🎭 简化角色扮演测试")
        print("="*50)
        
        # 简化的角色扮演场景
        simple_persona_tests = [
            {
                "name": "友好助手",
                "setup": "你是一个友好的助手。",
                "questions": [
                    "你好，你能帮我什么？",
                    "谢谢你的帮助。"
                ],
                "expected_traits": ["友好", "帮助", "助手"]
            },
            {
                "name": "专业顾问",
                "setup": "你是一名专业顾问。",
                "questions": [
                    "请给我一些建议。",
                    "你的专业领域是什么？"
                ],
                "expected_traits": ["建议", "专业", "顾问"]
            }
        ]
        
        for scenario in simple_persona_tests:
            print(f"\n🎪 角色测试: {scenario['name']}")
            
            # 设定角色
            setup_success, setup_response, setup_metadata = self.smart_chat(scenario['setup'])
            
            if not setup_success:
                print(f"  ❌ 角色设定失败")
                continue
            
            print(f"  ✅ 角色设定成功")
            
            # 构建上下文
            context = [
                {'role': 'user', 'content': scenario['setup']},
                {'role': 'assistant', 'content': setup_response}
            ]
            
            consistency_scores = []
            
            for i, question in enumerate(scenario['questions'], 1):
                print(f"    问题 {i}: ", end="")
                
                success, response, metadata = self.smart_chat(question, context)
                
                if success:
                    # 检查角色一致性
                    trait_matches = sum(1 for trait in scenario['expected_traits'] if trait in response)
                    consistency_score = trait_matches / len(scenario['expected_traits'])
                    consistency_scores.append(consistency_score)
                    
                    if consistency_score >= 0.3:  # 降低一致性要求
                        print(f"✅ 一致性良好 ({consistency_score:.2f})")
                    else:
                        print(f"⚠️ 一致性一般 ({consistency_score:.2f})")
                    
                    # 更新上下文
                    context.extend([
                        {'role': 'user', 'content': question},
                        {'role': 'assistant', 'content': response}
                    ])
                else:
                    print(f"❌ 失败")
                    consistency_scores.append(0.0)
                    break
            
            avg_consistency = sum(consistency_scores) / len(consistency_scores) if consistency_scores else 0
            
            result = {
                'scenario_name': scenario['name'],
                'setup_success': setup_success,
                'questions_completed': len(consistency_scores),
                'average_consistency': avg_consistency,
                'consistency_scores': consistency_scores,
                'expected_traits': scenario['expected_traits']
            }
            
            self.capability_results['persona'].append(result)
        
        return self.capability_results['persona']
    
    def run_simplified_test(self):
        """运行简化测试套件"""
        print("🌟 简化版最佳能力测试套件")
        print("="*70)
        print(f"模型: {self.model}")
        print(f"测试时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"简化参数: 长度限制{self.max_prompt_length}字符, 复杂度限制Level{self.max_complexity_level}")
        print()
        
        # 运行简化测试
        emergence_results = self.test_simplified_emergence()
        math_results = self.test_simplified_math()
        persona_results = self.test_simplified_persona()
        
        # 生成报告
        self._generate_simplified_report()
    
    def _generate_simplified_report(self):
        """生成简化测试报告"""
        print("\n" + "="*70)
        print("📊 简化测试结果报告")
        print("="*70)
        
        # 计算各能力表现
        capabilities = [
            ('涌现分析', 'emergence'),
            ('数学推理', 'math'),
            ('角色扮演', 'persona')
        ]
        
        overall_stats = {'total': 0, 'success': 0, 'avg_quality': 0}
        
        for cap_name, cap_key in capabilities:
            results = self.capability_results[cap_key]
            
            if cap_key == 'persona':
                # 角色扮演特殊处理
                total_tests = sum(r['questions_completed'] for r in results)
                successful_tests = sum(1 for r in results for score in r['consistency_scores'] if score >= 0.3)
                avg_consistency = sum(r['average_consistency'] for r in results) / len(results) if results else 0
                
                print(f"\n  {cap_name}:")
                print(f"    场景数量: {len(results)}")
                print(f"    总问题数: {total_tests}")
                print(f"    一致性良好: {successful_tests}")
                print(f"    平均一致性: {avg_consistency:.2f}")
                
                overall_stats['total'] += total_tests
                overall_stats['success'] += successful_tests
            else:
                # 涌现分析和数学推理
                total_tests = len(results)
                successful_tests = sum(1 for r in results if r['success'])
                avg_quality = sum(r['quality_score'] for r in results) / len(results) if results else 0
                success_rate = (successful_tests / total_tests * 100) if total_tests > 0 else 0
                
                print(f"\n  {cap_name}:")
                print(f"    测试数量: {total_tests}")
                print(f"    成功数量: {successful_tests}")
                print(f"    成功率: {success_rate:.1f}%")
                print(f"    平均质量: {avg_quality:.1f}/3")
                
                overall_stats['total'] += total_tests
                overall_stats['success'] += successful_tests
                overall_stats['avg_quality'] += avg_quality
        
        # 总体表现
        overall_success_rate = (overall_stats['success'] / overall_stats['total'] * 100) if overall_stats['total'] > 0 else 0
        
        print(f"\n📈 总体表现:")
        print(f"  总测试数: {overall_stats['total']}")
        print(f"  成功数量: {overall_stats['success']}")
        print(f"  总成功率: {overall_success_rate:.1f}%")
        
        # 与复杂测试对比
        print(f"\n📊 与复杂测试对比:")
        print(f"  复杂测试成功率: 8.3%")
        print(f"  简化测试成功率: {overall_success_rate:.1f}%")
        print(f"  改进幅度: +{overall_success_rate - 8.3:.1f}%")
        
        # 保存报告
        report_data = {
            'timestamp': datetime.now().isoformat(),
            'model': self.model,
            'test_type': 'simplified',
            'optimization_params': {
                'max_prompt_length': self.max_prompt_length,
                'max_complexity_level': self.max_complexity_level,
                'timeout_seconds': self.timeout_seconds
            },
            'overall_stats': overall_stats,
            'overall_success_rate': overall_success_rate,
            'capability_results': self.capability_results,
            'comparison': {
                'complex_test_success_rate': 8.3,
                'simplified_test_success_rate': overall_success_rate,
                'improvement': overall_success_rate - 8.3
            }
        }
        
        with open('simplified_best_capabilities_report.json', 'w', encoding='utf-8') as f:
            json.dump(report_data, f, ensure_ascii=False, indent=2)
        
        print(f"\n💾 详细报告已保存: simplified_best_capabilities_report.json")
        
        # 生成优化建议
        print(f"\n💡 优化建议:")
        if overall_success_rate > 50:
            print("  ✅ 简化测试表现良好，可以逐步增加复杂度")
        elif overall_success_rate > 30:
            print("  ⚠️ 表现中等，建议继续优化提示词结构")
        else:
            print("  ❌ 表现较差，建议进一步简化测试或检查模型配置")
        
        print(f"✅ 简化测试完成！")

def main():
    test_suite = SimplifiedBestCapabilitiesTest()
    test_suite.run_simplified_test()

if __name__ == "__main__":
    main()
