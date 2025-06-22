#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
增强测试框架 - 基于零响应分析的优化策略
实现智能重试、分段提示、渐进式复杂度等优化技术
"""

import os
import sys
import time
import json
from datetime import datetime
from typing import Dict, List, Tuple, Optional
import ollama

class EnhancedTestFramework:
    def __init__(self):
        # 加载配置
        try:
            sys.path.append(os.path.abspath('.'))
            from config import MODEL_TO_TEST
            self.model = MODEL_TO_TEST
        except ImportError:
            print("错误: 无法导入配置文件")
            sys.exit(1)
        
        # 基于诊断结果的优化参数
        self.max_prompt_length = 400  # 基于488字符阈值，保守设置
        self.max_complexity_level = 3  # 基于Level 4失败，限制为Level 3
        self.retry_attempts = 3
        self.timeout_seconds = 25
        
        # 测试统计
        self.stats = {
            'total_tests': 0,
            'successful_tests': 0,
            'zero_responses': 0,
            'retries_used': 0,
            'segmentation_used': 0,
            'progressive_used': 0
        }
    
    def smart_chat(self, prompt: str, context: List[Dict] = None, use_retry: bool = True) -> Tuple[bool, str, Dict]:
        """
        智能聊天方法，集成所有优化策略
        返回: (成功标志, 响应内容, 元数据)
        """
        self.stats['total_tests'] += 1
        metadata = {'strategy_used': 'direct', 'attempts': 0, 'original_length': len(prompt)}
        
        # 检查是否需要分段
        if len(prompt) > self.max_prompt_length:
            return self._segmented_chat(prompt, context, metadata)
        
        # 直接请求
        messages = context or []
        messages.append({'role': 'user', 'content': prompt})
        
        for attempt in range(self.retry_attempts if use_retry else 1):
            metadata['attempts'] = attempt + 1
            
            try:
                response = ollama.chat(
                    model=self.model,
                    messages=messages,
                    options={
                        'timeout': self.timeout_seconds,
                        'temperature': 0.7,
                        'top_p': 0.9
                    }
                )
                
                content = response.get('message', {}).get('content', '')
                
                if content:
                    self.stats['successful_tests'] += 1
                    if attempt > 0:
                        self.stats['retries_used'] += 1
                    return True, content, metadata
                else:
                    self.stats['zero_responses'] += 1
                    if attempt < self.retry_attempts - 1:
                        print(f"    🔄 零响应，重试 {attempt + 1}/{self.retry_attempts}")
                        time.sleep(1)
                        continue
                    else:
                        return False, '', metadata
                        
            except Exception as e:
                if attempt < self.retry_attempts - 1:
                    print(f"    🔄 错误重试 {attempt + 1}/{self.retry_attempts}: {str(e)[:50]}...")
                    time.sleep(2)
                    continue
                else:
                    metadata['error'] = str(e)
                    return False, '', metadata
        
        return False, '', metadata
    
    def _segmented_chat(self, long_prompt: str, context: List[Dict], metadata: Dict) -> Tuple[bool, str, Dict]:
        """分段处理长提示词"""
        self.stats['segmentation_used'] += 1
        metadata['strategy_used'] = 'segmented'
        
        # 智能分段策略
        segments = self._intelligent_segmentation(long_prompt)
        metadata['segments_count'] = len(segments)
        
        print(f"    📝 长提示词分段: {len(long_prompt)}字符 → {len(segments)}段")
        
        combined_response = ""
        current_context = context or []
        
        for i, segment in enumerate(segments):
            print(f"      段落{i+1}/{len(segments)}: ", end="")
            
            success, response, seg_meta = self.smart_chat(segment, current_context, use_retry=False)
            
            if success:
                print(f"✅ ({len(response)}字符)")
                combined_response += f"\n\n=== 段落{i+1}回答 ===\n{response}"
                
                # 更新上下文
                current_context.append({'role': 'user', 'content': segment})
                current_context.append({'role': 'assistant', 'content': response})
            else:
                print(f"❌ 段落{i+1}失败")
                metadata['failed_segment'] = i + 1
                return False, combined_response, metadata
        
        return True, combined_response, metadata
    
    def _intelligent_segmentation(self, prompt: str) -> List[str]:
        """智能分段算法"""
        # 简单的基于句号和问号的分段
        sentences = []
        current = ""
        
        for char in prompt:
            current += char
            if char in '。？！.?!' and len(current.strip()) > 20:
                sentences.append(current.strip())
                current = ""
        
        if current.strip():
            sentences.append(current.strip())
        
        # 合并短句，确保每段不超过最大长度
        segments = []
        current_segment = ""
        
        for sentence in sentences:
            if len(current_segment + sentence) <= self.max_prompt_length:
                current_segment += sentence
            else:
                if current_segment:
                    segments.append(current_segment)
                current_segment = sentence
        
        if current_segment:
            segments.append(current_segment)
        
        return segments
    
    def progressive_complexity_test(self, base_topic: str, levels: List[str]) -> Dict:
        """渐进式复杂度测试"""
        self.stats['progressive_used'] += 1
        
        print(f"🔄 渐进式复杂度测试: {base_topic}")
        
        results = {
            'topic': base_topic,
            'levels_tested': 0,
            'successful_levels': 0,
            'responses': [],
            'failure_level': None
        }
        
        context = []
        
        for i, level_prompt in enumerate(levels[:self.max_complexity_level], 1):
            print(f"  Level {i}: ", end="")
            
            success, response, metadata = self.smart_chat(level_prompt, context)
            
            results['levels_tested'] = i
            results['responses'].append({
                'level': i,
                'prompt': level_prompt,
                'success': success,
                'response': response,
                'metadata': metadata
            })
            
            if success:
                print(f"✅ 成功 ({len(response)}字符)")
                results['successful_levels'] = i
                
                # 更新上下文
                context.append({'role': 'user', 'content': level_prompt})
                context.append({'role': 'assistant', 'content': response})
            else:
                print(f"❌ 失败在Level {i}")
                results['failure_level'] = i
                break
        
        return results
    
    def run_enhanced_tests(self):
        """运行增强测试套件"""
        print("🚀 增强测试框架")
        print("="*60)
        print(f"模型: {self.model}")
        print(f"优化参数: 最大长度{self.max_prompt_length}字符, 最大复杂度Level{self.max_complexity_level}")
        print()
        
        test_results = []
        
        # 测试1: 基础功能验证
        print("🔍 测试1: 基础功能验证")
        basic_tests = [
            "请简要介绍人工智能的发展历程。",
            "请分析云计算的主要优势。",
            "请解释区块链技术的核心原理。"
        ]
        
        for i, test in enumerate(basic_tests, 1):
            print(f"  基础测试{i}: ", end="")
            success, response, metadata = self.smart_chat(test)
            
            if success:
                print(f"✅ 成功 ({len(response)}字符)")
            else:
                print(f"❌ 失败")
            
            test_results.append({
                'category': 'basic',
                'test_id': i,
                'success': success,
                'metadata': metadata
            })
        
        # 测试2: 长文本处理
        print(f"\n🔍 测试2: 长文本处理 (分段策略)")
        long_prompt = """请详细分析以下复杂的商业场景：
        一家跨国科技公司面临多重挑战：市场竞争加剧导致利润下降，新兴技术要求大量研发投入，
        监管环境变化增加合规成本，全球供应链不稳定影响生产，员工对远程工作的需求改变了组织结构，
        客户对数据隐私和环境责任的要求不断提高。请从战略规划、运营优化、风险管理、
        人力资源、技术创新五个维度提出综合解决方案。"""
        
        print(f"  长文本测试 ({len(long_prompt)}字符): ", end="")
        success, response, metadata = self.smart_chat(long_prompt)
        
        if success:
            print(f"✅ 成功 (策略: {metadata.get('strategy_used', 'unknown')})")
        else:
            print(f"❌ 失败")
        
        test_results.append({
            'category': 'long_text',
            'success': success,
            'metadata': metadata
        })
        
        # 测试3: 渐进式复杂度
        print(f"\n🔍 测试3: 渐进式复杂度测试")
        complexity_levels = [
            "请分析企业数字化转型的基本概念。",
            "基于上述分析，请探讨数字化转型过程中的主要挑战。",
            "结合前面的讨论，请提出一个完整的数字化转型实施方案。"
        ]
        
        progressive_result = self.progressive_complexity_test("企业数字化转型", complexity_levels)
        test_results.append({
            'category': 'progressive',
            'result': progressive_result
        })
        
        # 生成测试报告
        self._generate_test_report(test_results)
    
    def _generate_test_report(self, test_results: List[Dict]):
        """生成测试报告"""
        print(f"\n" + "="*60)
        print("📊 测试结果报告")
        print("="*60)
        
        # 统计信息
        print(f"📈 执行统计:")
        print(f"  总测试数: {self.stats['total_tests']}")
        print(f"  成功测试: {self.stats['successful_tests']}")
        print(f"  零响应数: {self.stats['zero_responses']}")
        print(f"  使用重试: {self.stats['retries_used']}")
        print(f"  使用分段: {self.stats['segmentation_used']}")
        print(f"  使用渐进: {self.stats['progressive_used']}")
        
        success_rate = (self.stats['successful_tests'] / max(self.stats['total_tests'], 1)) * 100
        print(f"  总成功率: {success_rate:.1f}%")
        
        # 策略效果分析
        print(f"\n🎯 策略效果分析:")
        
        segmented_tests = [r for r in test_results if r.get('metadata', {}).get('strategy_used') == 'segmented']
        if segmented_tests:
            seg_success = sum(1 for r in segmented_tests if r.get('success', False))
            seg_rate = (seg_success / len(segmented_tests)) * 100
            print(f"  分段策略成功率: {seg_rate:.1f}% ({seg_success}/{len(segmented_tests)})")
        
        progressive_tests = [r for r in test_results if r.get('category') == 'progressive']
        if progressive_tests:
            prog_result = progressive_tests[0]['result']
            prog_rate = (prog_result['successful_levels'] / prog_result['levels_tested']) * 100
            print(f"  渐进策略成功率: {prog_rate:.1f}% ({prog_result['successful_levels']}/{prog_result['levels_tested']})")
        
        # 保存详细结果
        report_data = {
            'timestamp': datetime.now().isoformat(),
            'model': self.model,
            'optimization_params': {
                'max_prompt_length': self.max_prompt_length,
                'max_complexity_level': self.max_complexity_level,
                'retry_attempts': self.retry_attempts
            },
            'statistics': self.stats,
            'test_results': test_results,
            'success_rate': success_rate
        }
        
        with open('enhanced_test_report.json', 'w', encoding='utf-8') as f:
            json.dump(report_data, f, ensure_ascii=False, indent=2)
        
        print(f"\n💾 详细测试报告已保存: enhanced_test_report.json")
        print(f"✅ 增强测试框架执行完成！")

def main():
    framework = EnhancedTestFramework()
    framework.run_enhanced_tests()

if __name__ == "__main__":
    main()
