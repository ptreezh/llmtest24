#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
增强测试框架 - 专门测试表现最佳的三项能力
涌现分析、数学推理、角色扮演
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

class BestCapabilitiesTestSuite(EnhancedTestFramework):
    def __init__(self):
        super().__init__()
        self.capability_stats = {
            'emergence': {'total': 0, 'success': 0, 'zero_responses': 0},
            'math': {'total': 0, 'success': 0, 'zero_responses': 0},
            'persona': {'total': 0, 'success': 0, 'zero_responses': 0}
        }
    
    def test_emergence_analysis(self):
        """测试涌现分析能力"""
        print("🧠 测试能力1: 涌现分析 (Emergence Analysis)")
        print("="*60)
        
        emergence_tests = [
            {
                "name": "用户引导流程反馈分析",
                "prompt": """作为AI项目经理，你收到了两条关于产品新用户引导流程的反馈：
                
反馈A（数据分析师）："新用户引导流程的完成率达到85%，用户平均停留时间增加了30%。"
反馈B（用户访谈）："多位新用户反映引导流程过于复杂，步骤太多，希望能够简化。"

请分析这两条反馈之间的冲突，并提出创新的解决方案。""",
                "complexity_level": 3
            },
            {
                "name": "产品功能冲突分析",
                "prompt": """请分析以下两条产品反馈中的深层矛盾：

反馈A："新功能上线后，用户活跃度提升了25%，日均使用时长增加。"
反馈B："部分老用户表示新功能难以上手，考虑转向竞争对手产品。"

请从用户体验、产品策略、商业价值三个维度进行涌现分析，找出潜在的创新机会。""",
                "complexity_level": 4
            },
            {
                "name": "多维度冲突整合",
                "prompt": """作为战略顾问，请分析以下三个维度的冲突并提出整合方案：

技术维度："AI算法准确率达到95%，但计算资源消耗增加40%。"
商业维度："客户愿意为高准确率付费，但成本上升影响利润率。"
用户维度："用户期望快速响应，但高准确率需要更多处理时间。"

请进行涌现分析，找出三者平衡的创新解决方案。""",
                "complexity_level": 5
            }
        ]
        
        emergence_results = []
        
        for i, test in enumerate(emergence_tests, 1):
            print(f"\n🔍 涌现测试 {i}: {test['name']}")
            print(f"复杂度级别: {test['complexity_level']}")
            
            self.capability_stats['emergence']['total'] += 1
            
            # 根据复杂度调整策略
            if test['complexity_level'] >= 4:
                # 使用渐进式方法
                progressive_prompts = self._decompose_emergence_prompt(test['prompt'])
                result = self.progressive_complexity_test(test['name'], progressive_prompts)
                success = result['successful_levels'] == len(progressive_prompts)
            else:
                # 直接测试
                success, response, metadata = self.smart_chat(test['prompt'])
            
            if success:
                self.capability_stats['emergence']['success'] += 1
                print(f"  ✅ 成功")
            else:
                print(f"  ❌ 失败")
                if 'zero_responses' in str(metadata):
                    self.capability_stats['emergence']['zero_responses'] += 1
            
            emergence_results.append({
                'test_name': test['name'],
                'complexity_level': test['complexity_level'],
                'success': success,
                'strategy_used': 'progressive' if test['complexity_level'] >= 4 else 'direct'
            })
        
        return emergence_results
    
    def test_math_reasoning(self):
        """测试数学推理能力"""
        print("\n🔢 测试能力2: 数学推理 (Mathematical Reasoning)")
        print("="*60)
        
        math_tests = [
            {
                "name": "基础工程问题",
                "prompt": """一个水池有甲、乙两个进水管。单开甲管，3小时可以注满水池；单开乙管，5小时可以注满水池。
现在，两个水管同时开启，请问需要多久才能将水池注满？

请给出详细的计算过程，包括：
1. 问题分析
2. 设定变量
3. 建立方程
4. 求解过程
5. 验证答案""",
                "expected_answer": "1.875小时或15/8小时"
            },
            {
                "name": "复杂工程问题",
                "prompt": """一个水池有甲、乙、丙三个进水管，分别单独注满水池需2、3、6小时。
同时还有一个排水管，单独开启可以在4小时内排空满池的水。

如果四个管道同时开启，问多久可以注满水池？请给出完整的解题过程。""",
                "expected_answer": "12/7小时"
            },
            {
                "name": "应用数学问题",
                "prompt": """某公司生产效率分析：
- 生产线A：每小时生产100个产品，运行成本50元/小时
- 生产线B：每小时生产80个产品，运行成本30元/小时
- 生产线C：每小时生产120个产品，运行成本70元/小时

现在需要在8小时内生产2000个产品，且总成本不超过400元。
请设计最优的生产方案，并计算具体的运行时间分配。""",
                "expected_answer": "需要优化计算"
            }
        ]
        
        math_results = []
        
        for i, test in enumerate(math_tests, 1):
            print(f"\n🧮 数学测试 {i}: {test['name']}")
            
            self.capability_stats['math']['total'] += 1
            
            success, response, metadata = self.smart_chat(test['prompt'])
            
            if success:
                # 检查答案质量
                has_process = any(keyword in response for keyword in ['计算', '过程', '步骤', '分析', '设定'])
                has_answer = len(response) > 100  # 基本长度检查
                
                if has_process and has_answer:
                    self.capability_stats['math']['success'] += 1
                    print(f"  ✅ 成功 - 包含详细过程")
                    quality = "high"
                else:
                    print(f"  ⚠️ 部分成功 - 缺少详细过程")
                    quality = "medium"
            else:
                print(f"  ❌ 失败")
                if not response:
                    self.capability_stats['math']['zero_responses'] += 1
                quality = "low"
            
            math_results.append({
                'test_name': test['name'],
                'success': success,
                'quality': quality,
                'response_length': len(response) if response else 0,
                'metadata': metadata
            })
        
        return math_results
    
    def test_persona_consistency(self):
        """测试角色扮演一致性"""
        print("\n🎭 测试能力3: 角色扮演 (Persona Consistency)")
        print("="*60)
        
        # 多轮角色扮演测试
        persona_scenarios = [
            {
                "name": "赛博朋克猫咪",
                "setup_prompt": "从现在开始，你是一只生活在赛博朋克城市里的猫，拥有基础的电子脑接口，能理解人类语言。请描述一下你眼中的世界。",
                "test_prompts": [
                    "你最喜欢吃什么？",
                    "你一天的生活是怎样的？",
                    "你如何看待人类？"
                ]
            },
            {
                "name": "数据分析师专家",
                "setup_prompt": "你现在是一名资深数据分析师，有10年的行业经验，专精于用户行为分析和商业智能。请介绍一下你的专业背景。",
                "test_prompts": [
                    "请为一个电商平台设计用户留存率分析方案。",
                    "如何评估A/B测试的效果？",
                    "面对数据质量问题，你通常如何处理？"
                ]
            }
        ]
        
        persona_results = []
        
        for scenario in persona_scenarios:
            print(f"\n🎪 角色测试: {scenario['name']}")
            
            # 初始化角色
            context = []
            setup_success, setup_response, setup_metadata = self.smart_chat(scenario['setup_prompt'])
            
            if not setup_success:
                print(f"  ❌ 角色设定失败")
                continue
            
            print(f"  ✅ 角色设定成功")
            context.append({'role': 'user', 'content': scenario['setup_prompt']})
            context.append({'role': 'assistant', 'content': setup_response})
            
            # 测试角色一致性
            consistency_scores = []
            
            for i, test_prompt in enumerate(scenario['test_prompts'], 1):
                print(f"    轮次 {i}: ", end="")
                
                self.capability_stats['persona']['total'] += 1
                
                success, response, metadata = self.smart_chat(test_prompt, context)
                
                if success:
                    # 检查角色一致性
                    consistency_score = self._evaluate_persona_consistency(
                        scenario['name'], response, setup_response
                    )
                    consistency_scores.append(consistency_score)
                    
                    if consistency_score >= 0.7:
                        self.capability_stats['persona']['success'] += 1
                        print(f"✅ 一致性良好 ({consistency_score:.2f})")
                    else:
                        print(f"⚠️ 一致性一般 ({consistency_score:.2f})")
                    
                    # 更新上下文
                    context.append({'role': 'user', 'content': test_prompt})
                    context.append({'role': 'assistant', 'content': response})
                else:
                    print(f"❌ 失败")
                    if not response:
                        self.capability_stats['persona']['zero_responses'] += 1
                    consistency_scores.append(0.0)
                    break
            
            avg_consistency = sum(consistency_scores) / len(consistency_scores) if consistency_scores else 0
            
            persona_results.append({
                'scenario_name': scenario['name'],
                'setup_success': setup_success,
                'rounds_completed': len(consistency_scores),
                'average_consistency': avg_consistency,
                'consistency_scores': consistency_scores
            })
        
        return persona_results
    
    def _decompose_emergence_prompt(self, complex_prompt: str) -> List[str]:
        """将复杂的涌现分析问题分解为渐进式提示"""
        return [
            "请先识别和总结给定反馈中的关键信息点。",
            "基于上述信息，请分析其中存在的冲突或矛盾。",
            "结合前面的分析，请提出创新的解决方案。"
        ]
    
    def _evaluate_persona_consistency(self, persona_type: str, current_response: str, setup_response: str) -> float:
        """评估角色一致性得分"""
        # 简化的一致性评估
        if "赛博朋克猫咪" in persona_type:
            cat_keywords = ['猫', '喵', '爪子', '尾巴', '电子', '赛博', '城市']
            score = sum(1 for keyword in cat_keywords if keyword in current_response) / len(cat_keywords)
        elif "数据分析师" in persona_type:
            analyst_keywords = ['数据', '分析', '指标', '用户', '业务', '统计', '模型']
            score = sum(1 for keyword in analyst_keywords if keyword in current_response) / len(analyst_keywords)
        else:
            score = 0.5  # 默认分数
        
        return min(score, 1.0)
    
    def run_best_capabilities_test(self):
        """运行最佳能力测试套件"""
        print("🌟 最佳能力增强测试套件")
        print("="*80)
        print(f"模型: {self.model}")
        print(f"测试时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"优化参数: 长度限制{self.max_prompt_length}字符, 复杂度限制Level{self.max_complexity_level}")
        print()
        
        # 运行三项能力测试
        emergence_results = self.test_emergence_analysis()
        math_results = self.test_math_reasoning()
        persona_results = self.test_persona_consistency()
        
        # 生成综合报告
        self._generate_capabilities_report(emergence_results, math_results, persona_results)
    
    def _generate_capabilities_report(self, emergence_results, math_results, persona_results):
        """生成能力测试报告"""
        print("\n" + "="*80)
        print("📊 最佳能力测试报告")
        print("="*80)
        
        # 总体统计
        total_tests = sum(stats['total'] for stats in self.capability_stats.values())
        total_success = sum(stats['success'] for stats in self.capability_stats.values())
        total_zero = sum(stats['zero_responses'] for stats in self.capability_stats.values())
        
        overall_success_rate = (total_success / max(total_tests, 1)) * 100
        overall_zero_rate = (total_zero / max(total_tests, 1)) * 100
        
        print(f"📈 总体表现:")
        print(f"  总测试数: {total_tests}")
        print(f"  成功测试: {total_success}")
        print(f"  零响应数: {total_zero}")
        print(f"  总成功率: {overall_success_rate:.1f}%")
        print(f"  零响应率: {overall_zero_rate:.1f}%")
        
        # 各能力详细表现
        print(f"\n🎯 各能力详细表现:")
        
        capabilities = [
            ('涌现分析', 'emergence', emergence_results),
            ('数学推理', 'math', math_results),
            ('角色扮演', 'persona', persona_results)
        ]
        
        for cap_name, cap_key, results in capabilities:
            stats = self.capability_stats[cap_key]
            success_rate = (stats['success'] / max(stats['total'], 1)) * 100
            zero_rate = (stats['zero_responses'] / max(stats['total'], 1)) * 100
            
            print(f"\n  {cap_name}:")
            print(f"    测试数量: {stats['total']}")
            print(f"    成功率: {success_rate:.1f}%")
            print(f"    零响应率: {zero_rate:.1f}%")
            
            # 特殊指标
            if cap_key == 'persona' and persona_results:
                avg_consistency = sum(r['average_consistency'] for r in persona_results) / len(persona_results)
                print(f"    平均一致性: {avg_consistency:.2f}")
        
        # 保存详细报告
        report_data = {
            'timestamp': datetime.now().isoformat(),
            'model': self.model,
            'optimization_params': {
                'max_prompt_length': self.max_prompt_length,
                'max_complexity_level': self.max_complexity_level,
                'retry_attempts': self.retry_attempts
            },
            'overall_stats': {
                'total_tests': total_tests,
                'total_success': total_success,
                'total_zero_responses': total_zero,
                'overall_success_rate': overall_success_rate,
                'overall_zero_rate': overall_zero_rate
            },
            'capability_stats': self.capability_stats,
            'detailed_results': {
                'emergence': emergence_results,
                'math': math_results,
                'persona': persona_results
            }
        }
        
        with open('best_capabilities_test_report.json', 'w', encoding='utf-8') as f:
            json.dump(report_data, f, ensure_ascii=False, indent=2)
        
        print(f"\n💾 详细测试报告已保存: best_capabilities_test_report.json")
        print(f"✅ 最佳能力测试完成！")

def main():
    test_suite = BestCapabilitiesTestSuite()
    test_suite.run_best_capabilities_test()

if __name__ == "__main__":
    main()
