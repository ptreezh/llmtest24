#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
零响应现象分析和解决方案脚本
基于诊断结果提供具体的优化建议和测试方案
"""

import json
import os
import sys
from datetime import datetime
from typing import Dict, List, Tuple
import ollama

class ZeroResponseAnalyzer:
    def __init__(self):
        # 加载配置
        try:
            sys.path.append(os.path.abspath('.'))
            from config import MODEL_TO_TEST
            self.model = MODEL_TO_TEST
        except ImportError:
            print("错误: 无法导入配置文件")
            sys.exit(1)
        
        # 加载诊断结果
        self.diagnosis_data = self.load_diagnosis_results()
        
    def load_diagnosis_results(self) -> Dict:
        """加载诊断结果"""
        try:
            with open('zero_response_diagnosis.json', 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            print("警告: 未找到诊断结果文件，请先运行 zero_response_diagnosis.py")
            return {}
    
    def analyze_patterns(self):
        """分析零响应模式"""
        print("🔍 零响应模式分析")
        print("="*50)
        
        if not self.diagnosis_data:
            print("❌ 无诊断数据可分析")
            return
        
        stats = self.diagnosis_data.get('statistics', {})
        thresholds = self.diagnosis_data.get('thresholds', {})
        
        print(f"📊 关键发现:")
        print(f"  • 零响应率: {stats.get('zero_response_rate', 0):.1f}%")
        print(f"  • 长度阈值: ~{thresholds.get('length_threshold', 'N/A')}字符")
        print(f"  • 复杂度阈值: Level {thresholds.get('complexity_threshold', 'N/A')}")
        
        # 分析模式
        length_threshold = thresholds.get('length_threshold', 0)
        complexity_threshold = thresholds.get('complexity_threshold', 0)
        
        print(f"\n🎯 问题模式识别:")
        
        if length_threshold and length_threshold < 500:
            print(f"  ⚠️ 长度敏感: 提示词超过{length_threshold}字符时容易出现零响应")
            print(f"    建议: 将复杂提示词分解为多个较短的子问题")
        
        if complexity_threshold and complexity_threshold <= 4:
            print(f"  ⚠️ 复杂度敏感: Level {complexity_threshold}以上的复杂问题容易失败")
            print(f"    建议: 采用渐进式问题分解策略")
        
        zero_rate = stats.get('zero_response_rate', 0)
        if zero_rate > 15:
            print(f"  ⚠️ 高零响应率: {zero_rate:.1f}%的请求无响应")
            print(f"    建议: 优化提示词结构和参数设置")
    
    def generate_optimized_prompts(self):
        """生成优化的提示词策略"""
        print(f"\n💡 优化提示词策略")
        print("="*50)
        
        # 基于阈值生成建议
        length_threshold = self.diagnosis_data.get('thresholds', {}).get('length_threshold', 400)
        
        strategies = [
            {
                "name": "分段式提示",
                "description": "将长提示词分解为多个短段",
                "example": f"原始: 长提示词({length_threshold + 100}字符)\n分解: 3个短提示词(各{length_threshold//3}字符)"
            },
            {
                "name": "渐进式复杂度",
                "description": "从简单问题开始，逐步增加复杂度",
                "example": "Level 1 → Level 2 → Level 3 (而非直接Level 4)"
            },
            {
                "name": "结构化提示",
                "description": "使用清晰的结构和标记",
                "example": "使用编号、分点、明确的问题陈述"
            },
            {
                "name": "上下文管理",
                "description": "控制上下文长度，避免累积过多信息",
                "example": "定期清理对话历史，保持焦点"
            }
        ]
        
        for i, strategy in enumerate(strategies, 1):
            print(f"{i}. {strategy['name']}")
            print(f"   描述: {strategy['description']}")
            print(f"   示例: {strategy['example']}")
            print()
    
    def test_optimized_strategies(self):
        """测试优化策略的效果"""
        print(f"🧪 优化策略效果测试")
        print("="*50)
        
        # 获取已知的问题提示词
        length_threshold = self.diagnosis_data.get('thresholds', {}).get('length_threshold', 400)
        
        # 测试分段策略
        print("测试1: 分段策略")
        long_prompt = "请分析以下复杂商业场景：" + "这是一个包含多方利益冲突的复杂问题。" * 20
        
        if len(long_prompt) > length_threshold:
            # 分解为多个短提示
            segments = [
                "请简要分析商业场景中的主要利益相关者。",
                "请分析这些利益相关者之间的主要冲突点。",
                "请提出初步的平衡方案建议。"
            ]
            
            print(f"  原始提示词长度: {len(long_prompt)}字符")
            print(f"  分解为{len(segments)}个段落:")
            
            success_count = 0
            for i, segment in enumerate(segments, 1):
                print(f"    段落{i} ({len(segment)}字符): ", end="")
                
                try:
                    response = ollama.chat(
                        model=self.model,
                        messages=[{'role': 'user', 'content': segment}],
                        options={'timeout': 20}
                    )
                    content = response.get('message', {}).get('content', '')
                    
                    if content:
                        print(f"✅ 成功 ({len(content)}字符)")
                        success_count += 1
                    else:
                        print("❌ 零响应")
                        
                except Exception as e:
                    print(f"❌ 错误: {str(e)[:50]}...")
            
            success_rate = (success_count / len(segments)) * 100
            print(f"  分段策略成功率: {success_rate:.1f}%")
        
        # 测试渐进式复杂度
        print(f"\n测试2: 渐进式复杂度")
        progressive_prompts = [
            "请分析：公司应该提高价格还是降低成本？",
            "基于上述分析，如果同时面临客户价格压力，应该如何调整策略？",
            "进一步考虑员工薪资需求，请完善整体平衡方案。"
        ]
        
        context = []
        success_count = 0
        
        for i, prompt in enumerate(progressive_prompts, 1):
            print(f"  阶段{i}: ", end="")
            
            # 构建上下文
            messages = []
            for j, (prev_prompt, prev_response) in enumerate(context):
                messages.extend([
                    {'role': 'user', 'content': prev_prompt},
                    {'role': 'assistant', 'content': prev_response}
                ])
            messages.append({'role': 'user', 'content': prompt})
            
            try:
                response = ollama.chat(
                    model=self.model,
                    messages=messages,
                    options={'timeout': 25}
                )
                content = response.get('message', {}).get('content', '')
                
                if content:
                    print(f"✅ 成功 ({len(content)}字符)")
                    context.append((prompt, content))
                    success_count += 1
                else:
                    print("❌ 零响应")
                    break
                    
            except Exception as e:
                print(f"❌ 错误: {str(e)[:50]}...")
                break
        
        progressive_success_rate = (success_count / len(progressive_prompts)) * 100
        print(f"  渐进式策略成功率: {progressive_success_rate:.1f}%")
    
    def generate_recommendations(self):
        """生成具体的优化建议"""
        print(f"\n📋 具体优化建议")
        print("="*50)
        
        stats = self.diagnosis_data.get('statistics', {})
        thresholds = self.diagnosis_data.get('thresholds', {})
        
        recommendations = []
        
        # 基于零响应率的建议
        zero_rate = stats.get('zero_response_rate', 0)
        if zero_rate > 20:
            recommendations.append({
                "priority": "高",
                "category": "提示词优化",
                "action": "立即实施提示词长度控制",
                "details": f"将提示词限制在{thresholds.get('length_threshold', 400)}字符以内"
            })
        
        # 基于复杂度阈值的建议
        complexity_threshold = thresholds.get('complexity_threshold', 0)
        if complexity_threshold <= 4:
            recommendations.append({
                "priority": "高",
                "category": "复杂度管理",
                "action": "采用分步骤问题解决",
                "details": "将Level 4+的复杂问题分解为多个Level 2-3的子问题"
            })
        
        # 通用优化建议
        recommendations.extend([
            {
                "priority": "中",
                "category": "参数调优",
                "action": "优化模型参数",
                "details": "调整temperature、top_p等参数以提高响应稳定性"
            },
            {
                "priority": "中",
                "category": "重试机制",
                "action": "实施智能重试",
                "details": "对零响应情况自动重试，使用不同的提示词变体"
            },
            {
                "priority": "低",
                "category": "监控优化",
                "action": "建立响应质量监控",
                "details": "持续监控零响应率和响应质量指标"
            }
        ])
        
        # 输出建议
        for i, rec in enumerate(recommendations, 1):
            priority_emoji = {"高": "🔴", "中": "🟡", "低": "🟢"}
            print(f"{i}. {priority_emoji[rec['priority']]} {rec['category']}: {rec['action']}")
            print(f"   详情: {rec['details']}")
            print()
    
    def run_analysis(self):
        """运行完整分析"""
        print("🔬 零响应现象深度分析")
        print("="*60)
        print(f"模型: {self.model}")
        print(f"分析时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print()
        
        self.analyze_patterns()
        self.generate_optimized_prompts()
        self.test_optimized_strategies()
        self.generate_recommendations()
        
        print("\n" + "="*60)
        print("✅ 分析完成！请根据建议优化您的测试策略。")

def main():
    analyzer = ZeroResponseAnalyzer()
    analyzer.run_analysis()

if __name__ == "__main__":
    main()
