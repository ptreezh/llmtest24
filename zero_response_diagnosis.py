#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
零响应现象深度诊断脚本
用第一性原理分析为什么高难度测试会导致完全无响应
"""

import os
import sys
import time
import json
from datetime import datetime
from typing import Tuple
import ollama

# Windows兼容的超时处理 - 移除信号处理，依赖ollama客户端的超时机制

class ZeroResponseDiagnostic:
    def __init__(self):
        # 加载配置
        try:
            sys.path.append(os.path.abspath('.'))
            from config import MODEL_TO_TEST
            self.model = MODEL_TO_TEST
        except ImportError:
            print("错误: 无法导入配置文件")
            sys.exit(1)

        # 诊断统计
        self.stats = {
            'total_requests': 0,
            'successful_requests': 0,
            'zero_responses': 0,
            'timeout_errors': 0,
            'other_errors': 0
        }

    def safe_chat_with_retry(self, prompt: str, timeout_seconds: int = 30, max_retries: int = 3) -> Tuple[bool, str, str]:
        """
        安全的聊天请求，带重试机制
        返回: (成功标志, 响应内容, 错误信息)
        """
        self.stats['total_requests'] += 1

        for attempt in range(max_retries):
            try:
                # 使用较短的超时时间避免长时间挂起
                response = ollama.chat(
                    model=self.model,
                    messages=[{'role': 'user', 'content': prompt}],
                    options={
                        'timeout': timeout_seconds,
                        'temperature': 0.7,
                        'top_p': 0.9
                    }
                )

                content = response.get('message', {}).get('content', '')

                if len(content) == 0:
                    self.stats['zero_responses'] += 1
                    return True, '', '零响应'
                else:
                    self.stats['successful_requests'] += 1
                    return True, content, ''

            except TimeoutError as e:
                self.stats['timeout_errors'] += 1
                error_msg = f"超时错误 (尝试 {attempt + 1}/{max_retries}): {str(e)}"
                print(f"    ⏰ {error_msg}")

                if attempt < max_retries - 1:
                    print(f"    🔄 等待2秒后重试...")
                    time.sleep(2)
                else:
                    return False, '', error_msg

            except Exception as e:
                self.stats['other_errors'] += 1
                error_msg = f"其他错误 (尝试 {attempt + 1}/{max_retries}): {str(e)}"
                print(f"    ❌ {error_msg}")

                if attempt < max_retries - 1:
                    print(f"    🔄 等待2秒后重试...")
                    time.sleep(2)
                else:
                    return False, '', error_msg

        return False, '', '所有重试均失败'
    
    def test_basic_connectivity(self):
        """测试基本连接性"""
        print("🔍 测试1: 基本连接性")

        success, content, error = self.safe_chat_with_retry('你好', timeout_seconds=15)

        if success:
            if content:
                print(f"  ✅ 基本连接正常: {len(content)}字符")
                print(f"  响应内容: {content[:100]}...")
                return True
            else:
                print(f"  ⚠️ 连接正常但出现零响应")
                return True  # 连接本身是正常的
        else:
            print(f"  ❌ 基本连接失败: {error}")
            return False
    
    def test_prompt_length_threshold(self):
        """测试提示词长度阈值"""
        print("\n🔍 测试2: 提示词长度阈值")

        # 渐进式增加提示词长度，使用更保守的长度
        base_prompt = "请分析以下问题："
        test_lengths = [40, 80, 150, 300, 600, 1000, 1500]

        zero_response_threshold = None
        error_threshold = None

        for length in test_lengths:
            # 生成指定长度的提示词
            filler = "这是一个复杂的商业场景分析问题。" * (length // 20)
            prompt = base_prompt + filler[:length-len(base_prompt)]
            actual_length = len(prompt)

            print(f"  测试长度: {actual_length}字符")

            success, content, error = self.safe_chat_with_retry(prompt, timeout_seconds=20)

            if not success:
                print(f"    ❌ 请求失败: {error}")
                error_threshold = actual_length
                break
            elif len(content) == 0:
                print(f"    ⚠️ 零响应出现在长度: {actual_length}")
                zero_response_threshold = actual_length
                break
            else:
                print(f"    ✅ 成功: {len(content)}字符响应")

        if zero_response_threshold:
            return zero_response_threshold
        elif error_threshold:
            return error_threshold
        else:
            print("  ✅ 所有长度测试通过")
            return None
    
    def test_complexity_threshold(self):
        """测试复杂度阈值"""
        print("\n🔍 测试3: 复杂度阈值")
        
        # 渐进式增加问题复杂度
        complexity_tests = [
            {
                "level": 1,
                "prompt": "请分析：公司应该提高产品价格还是降低成本？"
            },
            {
                "level": 2, 
                "prompt": "请分析：公司面临价格竞争和成本上升的双重压力，应该如何应对？"
            },
            {
                "level": 3,
                "prompt": "请分析：公司面临以下三重冲突：1)股东要求提高利润 2)客户要求降低价格 3)员工要求提高薪资。如何平衡？"
            },
            {
                "level": 4,
                "prompt": """请分析以下复杂商业场景：
公司面临多方压力：
- 股东：要求Q4利润增长30%，否则更换管理层
- 客户：产品质量下降，要求降价15%，否则转向竞争对手  
- 员工：工作强度极限，要求加薪20%，否则大量离职
- 监管：新法规要求增加合规成本500万
- 供应商：原材料涨价25%，要求调整合同

请提出一个能平衡所有利益相关者的创新解决方案。"""
            },
            {
                "level": 5,
                "prompt": """作为CEO，请分析这个极其复杂的全球化战略悖论：

**全球化压力**：
- 标准化产品降低成本40%
- 统一品牌提升认知度
- 规模经济效应显著
- 跨国人才流动优势

**本土化压力**：
- 各国法规差异巨大，合规成本高
- 文化偏好完全不同，产品适应性差
- 本地竞争对手更灵活，价格更低
- 政治风险和贸易保护主义抬头

**现实困境**：
- 全球化导致某些市场水土不服，销量下降30%
- 本土化导致成本激增60%，失去价格优势
- 中间路线导致两边不讨好，市场份额持续下滑

这是经典的"全球化悖论"。请提出一个突破性的第三条道路战略框架。"""
            }
        ]
        
        failure_level = None
        
        for test in complexity_tests:
            print(f"  复杂度Level {test['level']}: {len(test['prompt'])}字符")

            success, content, error = self.safe_chat_with_retry(
                test['prompt'],
                timeout_seconds=45,  # 复杂问题给更多时间
                max_retries=2  # 减少重试次数以节省时间
            )

            if not success:
                print(f"    ❌ 请求失败: {error}")
                failure_level = test['level']
                break
            elif len(content) == 0:
                print(f"    ❌ 零响应! 复杂度阈值: Level {test['level']}")
                failure_level = test['level']
                break
            else:
                print(f"    ✅ 成功: {len(content)}字符")

        return failure_level
    
    def test_token_limit_hypothesis(self):
        """测试token限制假说"""
        print("\n🔍 测试4: Token限制假说")
        
        # 测试不同的token密度
        token_tests = [
            {
                "type": "简单中文",
                "prompt": "请分析" + "这是一个简单的问题。" * 50
            },
            {
                "type": "复杂中文", 
                "prompt": "请分析" + "这是一个包含专业术语、复杂逻辑关系、多维度思考要求的综合性商业战略问题。" * 20
            },
            {
                "type": "英文混合",
                "prompt": "Please analyze this complex business scenario with multiple stakeholders, conflicting interests, and strategic implications for global operations." * 10
            },
            {
                "type": "数学符号",
                "prompt": "请计算：∑(i=1 to n) f(x_i) = max{∫[a,b] g(x)dx | constraints: h_j(x) ≤ 0, j=1...m}" * 5
            }
        ]
        
        for test in token_tests:
            print(f"  测试类型: {test['type']}, 长度: {len(test['prompt'])}字符")

            success, content, error = self.safe_chat_with_retry(test['prompt'], timeout_seconds=25)

            if success:
                if content:
                    print(f"    ✅ 响应长度: {len(content)}字符")
                else:
                    print(f"    ⚠️ 零响应")
            else:
                print(f"    ❌ 失败: {error}")
    
    def test_safety_filter_hypothesis(self):
        """测试安全过滤假说"""
        print("\n🔍 测试5: 安全过滤假说")
        
        safety_tests = [
            {
                "type": "中性商业",
                "prompt": "请分析公司的市场策略。"
            },
            {
                "type": "竞争分析", 
                "prompt": "请分析如何在激烈竞争中获得优势。"
            },
            {
                "type": "利益冲突",
                "prompt": "请分析股东利益和员工利益的冲突。"
            },
            {
                "type": "伦理决策",
                "prompt": "请分析技术发展与隐私保护的冲突。"
            },
            {
                "type": "复杂冲突",
                "prompt": "请分析多方利益相关者之间的复杂冲突和权力斗争。"
            }
        ]
        
        for test in safety_tests:
            print(f"  测试类型: {test['type']}")

            success, content, error = self.safe_chat_with_retry(test['prompt'], timeout_seconds=25)

            if not success:
                print(f"    ❌ 请求失败: {error}")
            elif len(content) == 0:
                print(f"    ❌ 可能触发安全过滤 (零响应)")
            else:
                print(f"    ✅ 正常响应: {len(content)}字符")
    
    def test_model_state_hypothesis(self):
        """测试模型状态假说"""
        print("\n🔍 测试6: 模型状态假说")
        
        # 测试连续请求对模型状态的影响
        print("  测试连续复杂请求...")
        
        complex_prompt = """请分析以下复杂的多方利益冲突：
股东要求利润增长30%，员工要求加薪20%，客户要求降价15%。
请提出平衡方案。"""
        
        for i in range(5):
            print(f"    第{i+1}次请求:")

            success, content, error = self.safe_chat_with_retry(
                complex_prompt,
                timeout_seconds=25,
                max_retries=1  # 减少重试以观察状态变化
            )

            if not success:
                print(f"      ❌ 请求失败: {error}")
                break
            elif len(content) == 0:
                print(f"      ❌ 第{i+1}次请求出现零响应")
                break
            else:
                print(f"      ✅ 响应长度: {len(content)}字符")

            time.sleep(2)  # 短暂等待
    
    def run_comprehensive_diagnosis(self):
        """运行综合诊断"""
        print("🔬 零响应现象深度诊断")
        print("="*60)
        
        # 记录诊断结果
        diagnosis_results = {
            "timestamp": datetime.now().isoformat(),
            "model": self.model,
            "tests": {}
        }
        
        # 运行所有测试
        if not self.test_basic_connectivity():
            print("❌ 基本连接失败，停止诊断")
            return
        
        length_threshold = self.test_prompt_length_threshold()
        complexity_threshold = self.test_complexity_threshold()
        
        self.test_token_limit_hypothesis()
        self.test_safety_filter_hypothesis() 
        self.test_model_state_hypothesis()
        
        # 生成诊断报告
        print("\n" + "="*60)
        print("🎯 诊断结果总结")
        print("="*60)

        # 统计信息
        print(f"📊 请求统计:")
        print(f"  总请求数: {self.stats['total_requests']}")
        print(f"  成功请求: {self.stats['successful_requests']}")
        print(f"  零响应数: {self.stats['zero_responses']}")
        print(f"  超时错误: {self.stats['timeout_errors']}")
        print(f"  其他错误: {self.stats['other_errors']}")

        success_rate = (self.stats['successful_requests'] / max(self.stats['total_requests'], 1)) * 100
        zero_response_rate = (self.stats['zero_responses'] / max(self.stats['total_requests'], 1)) * 100

        print(f"  成功率: {success_rate:.1f}%")
        print(f"  零响应率: {zero_response_rate:.1f}%")

        print(f"\n🔍 阈值分析:")
        if length_threshold:
            print(f"📏 提示词长度阈值: ~{length_threshold}字符")
        else:
            print("📏 提示词长度: 未发现明显阈值")

        if complexity_threshold:
            print(f"🧠 复杂度阈值: Level {complexity_threshold}")
        else:
            print("🧠 复杂度: 未发现明显阈值")

        # 生成建议
        print(f"\n💡 优化建议:")
        if zero_response_rate > 20:
            print("  ⚠️ 零响应率较高，建议:")
            print("    - 简化提示词复杂度")
            print("    - 减少单次请求的长度")
            print("    - 检查模型配置参数")

        if self.stats['timeout_errors'] > 0:
            print("  ⏰ 发现超时问题，建议:")
            print("    - 增加超时时间设置")
            print("    - 检查网络连接稳定性")
            print("    - 考虑分批处理复杂请求")

        # 更新诊断结果
        diagnosis_results.update({
            "statistics": self.stats,
            "thresholds": {
                "length_threshold": length_threshold,
                "complexity_threshold": complexity_threshold
            },
            "success_rate": success_rate,
            "zero_response_rate": zero_response_rate
        })

        # 保存诊断结果
        with open('zero_response_diagnosis.json', 'w', encoding='utf-8') as f:
            json.dump(diagnosis_results, f, ensure_ascii=False, indent=2)

        print(f"\n💾 详细诊断结果已保存: zero_response_diagnosis.json")

def main():
    diagnostic = ZeroResponseDiagnostic()
    diagnostic.run_comprehensive_diagnosis()

if __name__ == "__main__":
    main()
