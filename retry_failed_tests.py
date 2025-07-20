#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
失败测试重跑脚本
自动检测无响应或失败的测试，并进行重新测试
"""

import os
import sys
import time
import json
from datetime import datetime
from typing import List, Dict, Tuple
import ollama

class FailedTestRetrier:
    def __init__(self):
        self.testout_dir = "testout"
        self.retry_results = {}
        
        # 加载配置
        try:
            sys.path.append(os.path.abspath('.'))
            from config import MODEL_TO_TEST
            self.model = MODEL_TO_TEST
        except ImportError:
            print("错误: 无法导入配置文件")
            sys.exit(1)
    
    def detect_failed_tests(self) -> List[Dict]:
        """检测失败的测试"""
        failed_tests = []
        
        if not os.path.exists(self.testout_dir):
            print("testout目录不存在")
            return failed_tests
        
        for filename in os.listdir(self.testout_dir):
            if not filename.endswith('.txt'):
                continue
                
            filepath = os.path.join(self.testout_dir, filename)
            
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # 检查是否有有效响应
                lines = content.split('\n')
                response_started = False
                response_content = ""
                
                for line in lines:
                    if line.startswith("MODEL RESPONSE:"):
                        response_started = True
                        continue
                    if response_started:
                        response_content += line + "\n"
                
                response_content = response_content.strip()
                
                # 判断是否失败
                is_failed = False
                failure_reason = ""
                
                if not response_content:
                    is_failed = True
                    failure_reason = "无响应内容"
                elif len(response_content) < 10:
                    is_failed = True
                    failure_reason = f"响应过短 ({len(response_content)}字符)"
                elif "error" in response_content.lower() or "错误" in response_content:
                    is_failed = True
                    failure_reason = "响应包含错误信息"
                
                if is_failed:
                    # 提取测试信息
                    case_id = ""
                    test_type = ""
                    prompt = ""
                    
                    for line in lines:
                        if line.startswith("用例编号:"):
                            case_id = line.split(":", 1)[1].strip()
                        elif line.startswith("类型:"):
                            test_type = line.split(":", 1)[1].strip()
                        elif line.startswith("PROMPT:"):
                            # 提取prompt内容
                            prompt_started = False
                            for l in lines:
                                if l.startswith("PROMPT:"):
                                    prompt_started = True
                                    continue
                                elif l.startswith("MODEL RESPONSE:"):
                                    break
                                elif prompt_started:
                                    prompt += l + "\n"
                            prompt = prompt.strip()
                            break
                    
                    failed_tests.append({
                        'filename': filename,
                        'filepath': filepath,
                        'case_id': case_id,
                        'test_type': test_type,
                        'prompt': prompt,
                        'failure_reason': failure_reason,
                        'original_response': response_content
                    })
                    
            except Exception as e:
                print(f"检查文件 {filename} 时出错: {e}")
        
        return failed_tests
    
    def retry_single_test(self, test_info: Dict, max_retries: int = 3) -> Tuple[bool, str]:
        """重试单个测试"""
        print(f"\n🔄 重试测试: {test_info['test_type']} ({test_info['case_id']})")
        print(f"   原因: {test_info['failure_reason']}")
        
        for attempt in range(max_retries):
            try:
                print(f"   尝试 {attempt + 1}/{max_retries}...")
                
                # 调用模型
                response = ollama.chat(
                    model=self.model,
                    messages=[{'role': 'user', 'content': test_info['prompt']}],
                    options={
                        'timeout': 90,  # 增加超时时间
                        'temperature': 0.8,  # 稍微增加随机性
                        'top_p': 0.9
                    }
                )
                
                content = response['message']['content']
                
                # 检查响应质量
                if content and len(content.strip()) > 20:
                    print(f"   ✅ 重试成功! ({len(content)}字符)")
                    return True, content
                else:
                    print(f"   ⚠️ 响应仍然过短: {len(content) if content else 0}字符")
                    if attempt < max_retries - 1:
                        time.sleep(3)  # 短暂等待
                        
            except Exception as e:
                print(f"   ❌ 尝试 {attempt + 1} 失败: {e}")
                if attempt < max_retries - 1:
                    time.sleep(5)  # 等待更长时间
        
        print(f"   ❌ 所有重试都失败了")
        return False, ""
    
    def save_retry_result(self, test_info: Dict, new_response: str):
        """保存重试结果"""
        # 创建备份
        backup_path = test_info['filepath'] + '.backup'
        if not os.path.exists(backup_path):
            with open(test_info['filepath'], 'r', encoding='utf-8') as f:
                backup_content = f.read()
            with open(backup_path, 'w', encoding='utf-8') as f:
                f.write(backup_content)
        
        # 保存新结果
        with open(test_info['filepath'], 'w', encoding='utf-8') as f:
            f.write(f"用例编号: {test_info['case_id']}\n")
            f.write(f"类型: {test_info['test_type']}\n")
            f.write(f"PROMPT:\n{test_info['prompt']}\n\n")
            f.write(f"MODEL RESPONSE:\n{new_response}\n\n")
            f.write(f"# 重试信息\n")
            f.write(f"# 重试时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"# 原失败原因: {test_info['failure_reason']}\n")
        
        print(f"   💾 结果已更新: {test_info['filepath']}")
    
    def run_retry_process(self):
        """运行重试流程"""
        print("🔍 检测失败的测试...")
        
        failed_tests = self.detect_failed_tests()
        
        if not failed_tests:
            print("✅ 没有发现失败的测试!")
            return
        
        print(f"📋 发现 {len(failed_tests)} 个失败的测试:")
        for i, test in enumerate(failed_tests, 1):
            print(f"  {i}. {test['test_type']} - {test['failure_reason']}")
        
        # 询问用户是否继续
        user_input = input(f"\n是否重试这些失败的测试? (y/N): ").strip().lower()
        if user_input != 'y':
            print("用户取消重试")
            return
        
        print(f"\n🚀 开始重试 {len(failed_tests)} 个失败的测试...")
        
        success_count = 0
        
        for test_info in failed_tests:
            success, new_response = self.retry_single_test(test_info)
            
            if success:
                self.save_retry_result(test_info, new_response)
                success_count += 1
                
                self.retry_results[test_info['filename']] = {
                    'status': 'success',
                    'original_failure': test_info['failure_reason'],
                    'new_response_length': len(new_response),
                    'retry_time': datetime.now().isoformat()
                }
            else:
                self.retry_results[test_info['filename']] = {
                    'status': 'failed',
                    'original_failure': test_info['failure_reason'],
                    'retry_time': datetime.now().isoformat()
                }
        
        # 生成重试报告
        print(f"\n{'='*60}")
        print(f"📊 重试完成报告")
        print(f"{'='*60}")
        print(f"重试测试数: {len(failed_tests)}")
        print(f"重试成功数: {success_count}")
        print(f"仍然失败数: {len(failed_tests) - success_count}")
        print(f"重试成功率: {success_count/len(failed_tests)*100:.1f}%")
        
        # 保存重试结果
        with open('retry_results.json', 'w', encoding='utf-8') as f:
            json.dump({
                'summary': {
                    'total_retries': len(failed_tests),
                    'successful_retries': success_count,
                    'failed_retries': len(failed_tests) - success_count,
                    'retry_success_rate': success_count/len(failed_tests)*100,
                    'timestamp': datetime.now().isoformat()
                },
                'detailed_results': self.retry_results
            }, f, ensure_ascii=False, indent=2)
        
        print(f"\n💾 重试结果已保存: retry_results.json")
        
        if success_count > 0:
            print(f"\n🎯 建议: 重新运行评价脚本以更新分析结果")
            print(f"   python evaluate_results.py")

def main():
    retrier = FailedTestRetrier()
    retrier.run_retry_process()

if __name__ == "__main__":
    main()
