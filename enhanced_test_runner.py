#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
增强版测试运行器
包含自动重测、超时处理、失败恢复等功能
"""

import os
import sys
import time
import json
import subprocess
from datetime import datetime
from typing import Dict, List, Optional
import ollama

class EnhancedTestRunner:
    def __init__(self, max_retries=3, timeout_seconds=60, retry_delay=5):
        self.max_retries = max_retries
        self.timeout_seconds = timeout_seconds
        self.retry_delay = retry_delay
        self.test_results = {}
        self.failed_tests = []
        
        # 加载配置
        try:
            sys.path.append(os.path.abspath('.'))
            from config import MODEL_TO_TEST
            self.model = MODEL_TO_TEST
        except ImportError:
            print("错误: 无法导入配置文件")
            sys.exit(1)
    
    def test_ollama_connection(self) -> bool:
        """测试Ollama连接"""
        try:
            ollama.list()
            return True
        except Exception as e:
            print(f"Ollama连接失败: {e}")
            return False
    
    def call_ollama_with_retry(self, messages: List[Dict], test_id: str) -> Optional[str]:
        """带重试的Ollama调用"""
        for attempt in range(self.max_retries):
            try:
                print(f"  尝试 {attempt + 1}/{self.max_retries}...")
                
                # 设置较短的超时时间
                response = ollama.chat(
                    model=self.model, 
                    messages=messages,
                    options={
                        'timeout': self.timeout_seconds,
                        'temperature': 0.7,
                        'top_p': 0.9
                    }
                )
                
                content = response['message']['content']
                
                # 检查响应是否有效
                if content and len(content.strip()) > 10:
                    print(f"  ✅ 成功获得响应 ({len(content)}字符)")
                    return content
                else:
                    print(f"  ⚠️ 响应过短或为空: {len(content) if content else 0}字符")
                    if attempt < self.max_retries - 1:
                        time.sleep(self.retry_delay)
                        continue
                    
            except Exception as e:
                print(f"  ❌ 尝试 {attempt + 1} 失败: {e}")
                if attempt < self.max_retries - 1:
                    print(f"  等待 {self.retry_delay} 秒后重试...")
                    time.sleep(self.retry_delay)
                else:
                    print(f"  所有重试都失败了")
                    self.failed_tests.append({
                        'test_id': test_id,
                        'error': str(e),
                        'attempts': self.max_retries
                    })
        
        return None
    
    def run_single_case_test(self, test_script: str, case_info: Dict) -> bool:
        """运行单个测试案例"""
        test_id = f"{test_script}_{case_info.get('case', 'unknown')}"
        print(f"\n🧪 运行测试: {test_id}")
        print(f"   描述: {case_info.get('desc', 'N/A')}")
        
        messages = [{'role': 'user', 'content': case_info['prompt']}]
        
        # 调用模型
        response = self.call_ollama_with_retry(messages, test_id)
        
        if response:
            # 保存结果
            output_dir = "testout"
            os.makedirs(output_dir, exist_ok=True)
            
            output_file = os.path.join(output_dir, f"{test_script}_{case_info['case']}.txt")
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(f"用例编号: {case_info['case']}\n")
                f.write(f"类型: {case_info['desc']}\n")
                f.write(f"PROMPT:\n{case_info['prompt']}\n\n")
                f.write(f"MODEL RESPONSE:\n{response}")
            
            print(f"  💾 结果已保存: {output_file}")
            
            # 记录成功
            self.test_results[test_id] = {
                'status': 'success',
                'response_length': len(response),
                'output_file': output_file
            }
            return True
        else:
            # 记录失败
            self.test_results[test_id] = {
                'status': 'failed',
                'attempts': self.max_retries
            }
            return False
    
    def run_multi_round_test(self, test_script: str, cases: List[Dict]) -> bool:
        """运行多轮对话测试（特殊处理）"""
        print(f"\n🔄 运行多轮测试: {test_script}")
        
        messages = []
        all_success = True
        
        for idx, case_info in enumerate(cases):
            round_num = idx + 1
            test_id = f"{test_script}_case{case_info['case']}_round{round_num}"
            
            print(f"\n  轮次 {round_num}: {case_info['desc']}")
            
            # 添加用户消息
            messages.append({'role': 'user', 'content': case_info['prompt']})
            
            # 获取响应
            response = self.call_ollama_with_retry(messages, test_id)
            
            if response:
                # 添加助手响应到对话历史
                messages.append({'role': 'assistant', 'content': response})
                
                # 保存结果
                output_dir = "testout"
                os.makedirs(output_dir, exist_ok=True)
                
                output_file = os.path.join(output_dir, f"persona_case{case_info['case']}_round{round_num}.txt")
                with open(output_file, 'w', encoding='utf-8') as f:
                    f.write(f"用例编号: case{case_info['case']} 轮次: {round_num}\n")
                    f.write(f"类型: {case_info['desc']}\n")
                    f.write(f"PROMPT:\n{case_info['prompt']}\n\n")
                    f.write(f"MODEL RESPONSE:\n{response}")
                
                print(f"    💾 结果已保存: {output_file}")
                
                self.test_results[test_id] = {
                    'status': 'success',
                    'response_length': len(response),
                    'output_file': output_file,
                    'round': round_num
                }
            else:
                print(f"    ❌ 轮次 {round_num} 失败")
                all_success = False
                
                # 尝试重置对话上下文继续
                if len(messages) > 2:  # 如果有历史对话
                    print(f"    🔄 重置对话上下文，继续下一轮...")
                    messages = []  # 清空历史
                
                self.test_results[test_id] = {
                    'status': 'failed',
                    'attempts': self.max_retries,
                    'round': round_num
                }
        
        return all_success
    
    def run_all_tests(self):
        """运行所有测试"""
        print("🚀 启动增强版测试运行器")
        print(f"配置: 模型={self.model}, 重试={self.max_retries}次, 超时={self.timeout_seconds}秒")
        
        # 检查连接
        if not self.test_ollama_connection():
            print("❌ Ollama连接失败，退出")
            return
        
        start_time = datetime.now()
        
        # 定义测试配置
        test_configs = [
            {
                'script': 'creativity',
                'cases': [
                    {'case': '1', 'desc': '鲁迅文风广告', 'prompt': '请以鲁迅的文风，为一款名为"赛博加速"的能量饮料写一段广告词，不超过100字。'},
                    {'case': '2', 'desc': '海明威文风广告', 'prompt': '请以海明威的文风，为一款名为"未来能量棒"的能量食品写一段广告词，不超过80字。'},
                    {'case': '3', 'desc': '网络流行语广告', 'prompt': '请用网络流行语风格，为一款名为"AI智能饮料"的产品写一段有趣的广告词，不超过60字。'}
                ],
                'multi_round': False
            },
            {
                'script': 'persona',
                'cases': [
                    {'case': '1', 'desc': '赛博朋克猫世界观', 'prompt': '从现在开始，你是一只生活在赛博朋克城市里的猫，拥有一些基础的电子脑接口，能理解人类语言。请描述一下你眼中的世界。'},
                    {'case': '2', 'desc': '猫的最爱', 'prompt': '你最喜欢吃什么？'},
                    {'case': '3', 'desc': '猫的日常', 'prompt': '你一天的生活是怎样的？'},
                    {'case': '4', 'desc': '猫与人类的关系', 'prompt': '你如何看待人类？'}
                ],
                'multi_round': True
            }
        ]
        
        # 运行测试
        total_tests = 0
        successful_tests = 0
        
        for config in test_configs:
            if config['multi_round']:
                success = self.run_multi_round_test(config['script'], config['cases'])
                total_tests += len(config['cases'])
                if success:
                    successful_tests += len(config['cases'])
                else:
                    # 计算实际成功的轮次
                    for case in config['cases']:
                        test_id = f"{config['script']}_case{case['case']}_round{config['cases'].index(case)+1}"
                        if self.test_results.get(test_id, {}).get('status') == 'success':
                            successful_tests += 1
            else:
                for case in config['cases']:
                    success = self.run_single_case_test(config['script'], case)
                    total_tests += 1
                    if success:
                        successful_tests += 1
        
        # 生成报告
        end_time = datetime.now()
        duration = end_time - start_time
        
        print(f"\n{'='*60}")
        print(f"📊 测试完成报告")
        print(f"{'='*60}")
        print(f"总测试数: {total_tests}")
        print(f"成功测试: {successful_tests}")
        print(f"失败测试: {total_tests - successful_tests}")
        print(f"成功率: {successful_tests/total_tests*100:.1f}%")
        print(f"运行时间: {duration}")
        
        if self.failed_tests:
            print(f"\n❌ 失败的测试:")
            for failed in self.failed_tests:
                print(f"  - {failed['test_id']}: {failed['error']}")
        
        # 保存详细结果
        with open('test_results_detailed.json', 'w', encoding='utf-8') as f:
            json.dump({
                'summary': {
                    'total_tests': total_tests,
                    'successful_tests': successful_tests,
                    'failed_tests': total_tests - successful_tests,
                    'success_rate': successful_tests/total_tests*100,
                    'duration': str(duration),
                    'timestamp': datetime.now().isoformat()
                },
                'detailed_results': self.test_results,
                'failed_tests': self.failed_tests
            }, ensure_ascii=False, indent=2)
        
        print(f"\n💾 详细结果已保存: test_results_detailed.json")

def main():
    runner = EnhancedTestRunner(
        max_retries=3,      # 最多重试3次
        timeout_seconds=60, # 60秒超时
        retry_delay=5       # 重试间隔5秒
    )
    runner.run_all_tests()

if __name__ == "__main__":
    main()
