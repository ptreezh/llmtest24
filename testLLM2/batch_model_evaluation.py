#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
批量模型测评脚本
对models.txt中的所有模型运行今天开发的测评系统
包括零响应诊断、增强测试框架和简化最佳能力测试
"""

import os
import sys
import time
import json
import traceback
from datetime import datetime
from typing import Dict, List, Tuple
import ollama

# 导入测试模块
sys.path.append(os.path.abspath('.'))

class BatchModelEvaluator:
    def __init__(self):
        self.models = self.load_models()
        self.results = {}
        self.failed_models = []
        self.max_retries = 3
        
    def load_models(self) -> List[str]:
        """加载模型列表"""
        models = []
        try:
            with open('models.txt', 'r', encoding='utf-8') as f:
                for line in f:
                    model = line.strip()
                    if model and not model.startswith('#'):
                        models.append(model)
        except FileNotFoundError:
            print("错误: 未找到models.txt文件")
            sys.exit(1)
        
        print(f"📋 加载了 {len(models)} 个模型:")
        for i, model in enumerate(models, 1):
            print(f"  {i}. {model}")
        
        return models
    
    def test_model_connectivity(self, model: str) -> bool:
        """测试模型连接性"""
        try:
            response = ollama.chat(
                model=model,
                messages=[{'role': 'user', 'content': '你好'}],
                options={'timeout': 10}
            )
            return len(response.get('message', {}).get('content', '')) > 0
        except Exception as e:
            print(f"    连接测试失败: {str(e)[:100]}...")
            return False
    
    def run_pillars_9_19_tests(self, model: str) -> Dict:
        """运行Pillar 9-19测试"""
        print(f"  📋 运行Pillar 9-19测试...")

        try:
            # 临时修改config.py中的模型
            self.update_config_model(model)

            # 运行各个Pillar测试
            pillar_results = {}

            # Pillar测试列表
            pillar_tests = [
                ('pillar_9_reasoning', '逻辑推理'),
                ('pillar_10_math', '数学推理'),
                ('pillar_11_creativity', '创意生成'),
                ('pillar_12_persona', '角色扮演'),
                ('pillar_13_init', '环境初始化'),
                ('pillar_14_persona_depth', '深度角色扮演'),
                ('pillar_15_collaboration', '多角色协作'),
                ('pillar_16_emergence', '涌现分析'),
                ('pillar_17_task_graph', '任务图谱'),
                ('pillar_18_adaptive_exec', '自适应执行'),
                ('pillar_19_network_analysis', '网络分析')
            ]

            for pillar_name, pillar_desc in pillar_tests:
                print(f"    🔍 测试 {pillar_name} ({pillar_desc})...")

                try:
                    # 动态导入并运行测试
                    test_module = __import__(f'tests.test_{pillar_name}', fromlist=['run_test'])

                    if hasattr(test_module, 'run_test'):
                        # 捕获测试输出
                        import io
                        import contextlib

                        output_buffer = io.StringIO()
                        with contextlib.redirect_stdout(output_buffer):
                            test_module.run_test()

                        output = output_buffer.getvalue()
                        pillar_results[pillar_name] = {
                            'status': 'completed',
                            'output': output,
                            'description': pillar_desc
                        }
                        print(f"      ✅ {pillar_desc} 完成")

                    else:
                        pillar_results[pillar_name] = {
                            'status': 'no_run_test_function',
                            'description': pillar_desc
                        }
                        print(f"      ⚠️ {pillar_desc} 无run_test函数")

                except ImportError as e:
                    pillar_results[pillar_name] = {
                        'status': 'import_error',
                        'error': str(e),
                        'description': pillar_desc
                    }
                    print(f"      ❌ {pillar_desc} 导入失败")

                except Exception as e:
                    pillar_results[pillar_name] = {
                        'status': 'execution_error',
                        'error': str(e),
                        'description': pillar_desc
                    }
                    print(f"      ❌ {pillar_desc} 执行失败")

            return {
                'timestamp': datetime.now().isoformat(),
                'model': model,
                'pillar_results': pillar_results,
                'completed_tests': sum(1 for r in pillar_results.values() if r['status'] == 'completed'),
                'total_tests': len(pillar_tests)
            }

        except Exception as e:
            print(f"    Pillar测试失败: {str(e)[:100]}...")
            return {'error': str(e), 'model': model}

    def run_zero_response_diagnosis(self, model: str) -> Dict:
        """运行零响应诊断"""
        print(f"  🔬 运行零响应诊断...")

        try:
            # 临时修改config.py中的模型
            self.update_config_model(model)

            # 导入并运行诊断
            from zero_response_diagnosis import ZeroResponseDiagnostic

            diagnostic = ZeroResponseDiagnostic()

            # 运行简化版诊断以节省时间
            results = {
                'timestamp': datetime.now().isoformat(),
                'model': model,
                'tests': {}
            }

            # 基本连接性测试
            basic_success = diagnostic.test_basic_connectivity()
            results['basic_connectivity'] = basic_success

            if not basic_success:
                return results

            # 长度阈值测试（简化版）
            length_threshold = self.simplified_length_test(model)
            results['length_threshold'] = length_threshold

            # 复杂度阈值测试（简化版）
            complexity_threshold = self.simplified_complexity_test(model)
            results['complexity_threshold'] = complexity_threshold

            return results

        except Exception as e:
            print(f"    诊断失败: {str(e)[:100]}...")
            return {'error': str(e), 'model': model}
    
    def simplified_length_test(self, model: str) -> int:
        """简化的长度阈值测试"""
        test_lengths = [50, 100, 200, 400]
        base_prompt = "请分析以下问题："
        
        for length in test_lengths:
            filler = "这是一个商业分析问题。" * (length // 12)
            prompt = base_prompt + filler[:length-len(base_prompt)]
            
            try:
                response = ollama.chat(
                    model=model,
                    messages=[{'role': 'user', 'content': prompt}],
                    options={'timeout': 15}
                )
                content = response.get('message', {}).get('content', '')
                
                if len(content) == 0:
                    return len(prompt)
                    
            except Exception:
                return len(prompt)
        
        return None  # 未发现阈值
    
    def simplified_complexity_test(self, model: str) -> int:
        """简化的复杂度阈值测试"""
        complexity_tests = [
            "请分析：公司应该提高价格还是降低成本？",
            "请分析：公司面临价格竞争和成本上升，应该如何应对？",
            "请分析多方冲突：股东要求提高利润，客户要求降价，员工要求加薪。"
        ]
        
        for i, test_prompt in enumerate(complexity_tests, 1):
            try:
                response = ollama.chat(
                    model=model,
                    messages=[{'role': 'user', 'content': test_prompt}],
                    options={'timeout': 20}
                )
                content = response.get('message', {}).get('content', '')
                
                if len(content) == 0:
                    return i
                    
            except Exception:
                return i
        
        return None  # 未发现阈值
    
    def run_simplified_capabilities_test(self, model: str) -> Dict:
        """运行简化能力测试"""
        print(f"  🌟 运行简化能力测试...")
        
        try:
            # 临时修改config.py中的模型
            self.update_config_model(model)
            
            # 导入并运行简化测试
            from simplified_best_capabilities_test import SimplifiedBestCapabilitiesTest
            
            test_suite = SimplifiedBestCapabilitiesTest()
            
            # 运行各项能力测试
            emergence_results = test_suite.test_simplified_emergence()
            math_results = test_suite.test_simplified_math()
            persona_results = test_suite.test_simplified_persona()
            
            # 计算总体统计
            total_tests = len(emergence_results) + len(math_results)
            successful_tests = sum(1 for r in emergence_results if r['success']) + \
                             sum(1 for r in math_results if r['success'])
            
            # 角色扮演统计
            persona_total = sum(r['questions_completed'] for r in persona_results)
            persona_success = sum(1 for r in persona_results 
                                for score in r['consistency_scores'] if score >= 0.3)
            
            total_tests += persona_total
            successful_tests += persona_success
            
            overall_success_rate = (successful_tests / max(total_tests, 1)) * 100
            
            return {
                'timestamp': datetime.now().isoformat(),
                'model': model,
                'overall_success_rate': overall_success_rate,
                'emergence_success_rate': (sum(1 for r in emergence_results if r['success']) / 
                                         max(len(emergence_results), 1)) * 100,
                'math_success_rate': (sum(1 for r in math_results if r['success']) / 
                                    max(len(math_results), 1)) * 100,
                'persona_success_rate': (persona_success / max(persona_total, 1)) * 100,
                'detailed_results': {
                    'emergence': emergence_results,
                    'math': math_results,
                    'persona': persona_results
                }
            }
            
        except Exception as e:
            print(f"    能力测试失败: {str(e)[:100]}...")
            return {'error': str(e), 'model': model}
    
    def update_config_model(self, model: str):
        """临时更新config.py中的模型"""
        config_content = f"""# 临时配置文件 - 批量测试
MODEL_TO_TEST = '{model}'
"""
        with open('config.py', 'w', encoding='utf-8') as f:
            f.write(config_content)
    
    def evaluate_single_model(self, model: str) -> Dict:
        """评估单个模型"""
        print(f"\n🤖 开始评估模型: {model}")
        print("="*60)

        model_results = {
            'model': model,
            'start_time': datetime.now().isoformat(),
            'status': 'unknown',
            'connectivity': False,
            'pillars_results': {},
            'diagnosis_results': {},
            'capabilities_results': {},
            'error_count': 0,
            'retry_count': 0
        }

        # 连接性测试
        print(f"  🔌 测试连接性...")
        if not self.test_model_connectivity(model):
            model_results['status'] = 'connection_failed'
            print(f"  ❌ 模型连接失败，跳过")
            return model_results

        model_results['connectivity'] = True
        print(f"  ✅ 连接成功")

        # 第一步：运行Pillar 9-19测试（带重试）
        for attempt in range(self.max_retries):
            try:
                pillars_results = self.run_pillars_9_19_tests(model)
                if 'error' not in pillars_results:
                    model_results['pillars_results'] = pillars_results
                    print(f"  ✅ Pillar 9-19测试完成")
                    break
                else:
                    raise Exception(pillars_results['error'])
            except Exception as e:
                model_results['retry_count'] += 1
                model_results['error_count'] += 1
                print(f"  ⚠️ Pillar测试失败 (尝试 {attempt + 1}/{self.max_retries}): {str(e)[:50]}...")
                if attempt < self.max_retries - 1:
                    time.sleep(2)
                else:
                    print(f"  ❌ Pillar测试最终失败，继续后续测试")
                    model_results['pillars_results'] = {'error': str(e)}

        # 第二步：零响应诊断（带重试）
        for attempt in range(self.max_retries):
            try:
                diagnosis_results = self.run_zero_response_diagnosis(model)
                if 'error' not in diagnosis_results:
                    model_results['diagnosis_results'] = diagnosis_results
                    print(f"  ✅ 零响应诊断完成")
                    break
                else:
                    raise Exception(diagnosis_results['error'])
            except Exception as e:
                model_results['retry_count'] += 1
                model_results['error_count'] += 1
                print(f"  ⚠️ 诊断失败 (尝试 {attempt + 1}/{self.max_retries}): {str(e)[:50]}...")
                if attempt < self.max_retries - 1:
                    time.sleep(2)
                else:
                    print(f"  ❌ 诊断最终失败，继续能力测试")
                    model_results['diagnosis_results'] = {'error': str(e)}

        # 第三步：增强能力测试（带重试）
        for attempt in range(self.max_retries):
            try:
                capabilities_results = self.run_simplified_capabilities_test(model)
                if 'error' not in capabilities_results:
                    model_results['capabilities_results'] = capabilities_results
                    model_results['status'] = 'completed'
                    print(f"  ✅ 增强能力测试完成")
                    break
                else:
                    raise Exception(capabilities_results['error'])
            except Exception as e:
                model_results['retry_count'] += 1
                model_results['error_count'] += 1
                print(f"  ⚠️ 能力测试失败 (尝试 {attempt + 1}/{self.max_retries}): {str(e)[:50]}...")
                if attempt < self.max_retries - 1:
                    time.sleep(2)
                else:
                    print(f"  ❌ 能力测试最终失败")
                    model_results['capabilities_results'] = {'error': str(e)}
                    model_results['status'] = 'partial_completed'

        model_results['end_time'] = datetime.now().isoformat()
        return model_results
    
    def run_batch_evaluation(self):
        """运行批量评估"""
        print("🚀 批量模型评估开始")
        print("="*80)
        print(f"评估时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"模型数量: {len(self.models)}")
        print(f"最大重试次数: {self.max_retries}")
        print()
        
        start_time = datetime.now()
        
        for i, model in enumerate(self.models, 1):
            print(f"\n📊 进度: {i}/{len(self.models)}")
            
            try:
                model_results = self.evaluate_single_model(model)
                self.results[model] = model_results
                
                if model_results['status'] != 'completed':
                    self.failed_models.append(model)
                
            except Exception as e:
                print(f"❌ 模型 {model} 评估出现严重错误: {str(e)}")
                self.failed_models.append(model)
                self.results[model] = {
                    'model': model,
                    'status': 'critical_error',
                    'error': str(e),
                    'traceback': traceback.format_exc()
                }
        
        end_time = datetime.now()
        duration = end_time - start_time
        
        # 生成总结报告
        self.generate_batch_report(start_time, end_time, duration)
    
    def generate_batch_report(self, start_time, end_time, duration):
        """生成批量评估报告"""
        print("\n" + "="*80)
        print("📊 批量评估总结报告")
        print("="*80)
        
        successful_models = [m for m in self.models if m not in self.failed_models]
        
        print(f"⏱️ 评估时间: {duration}")
        print(f"📈 总体统计:")
        print(f"  总模型数: {len(self.models)}")
        print(f"  成功评估: {len(successful_models)}")
        print(f"  失败模型: {len(self.failed_models)}")
        print(f"  成功率: {len(successful_models)/len(self.models)*100:.1f}%")
        
        if successful_models:
            print(f"\n✅ 成功评估的模型:")
            for model in successful_models:
                result = self.results[model]

                # Pillar测试结果
                pillar_info = ""
                if 'pillars_results' in result and 'error' not in result['pillars_results']:
                    completed = result['pillars_results'].get('completed_tests', 0)
                    total = result['pillars_results'].get('total_tests', 11)
                    pillar_info = f"Pillar:{completed}/{total}"

                # 能力测试结果
                capability_info = ""
                if 'capabilities_results' in result and 'error' not in result['capabilities_results']:
                    success_rate = result['capabilities_results'].get('overall_success_rate', 0)
                    capability_info = f"能力:{success_rate:.1f}%"

                # 诊断结果
                diagnosis_info = ""
                if 'diagnosis_results' in result and 'error' not in result['diagnosis_results']:
                    diagnosis_info = "诊断:✓"

                status_parts = [info for info in [pillar_info, diagnosis_info, capability_info] if info]
                status = " | ".join(status_parts) if status_parts else "部分完成"

                print(f"  • {model}: {status}")
        
        if self.failed_models:
            print(f"\n❌ 失败的模型:")
            for model in self.failed_models:
                result = self.results[model]
                print(f"  • {model}: {result.get('status', 'unknown')}")
        
        # 保存详细报告
        report_data = {
            'batch_evaluation_summary': {
                'start_time': start_time.isoformat(),
                'end_time': end_time.isoformat(),
                'duration_seconds': duration.total_seconds(),
                'total_models': len(self.models),
                'successful_models': len(successful_models),
                'failed_models': len(self.failed_models),
                'success_rate': len(successful_models)/len(self.models)*100
            },
            'model_results': self.results,
            'successful_models': successful_models,
            'failed_models': self.failed_models
        }
        
        with open('batch_evaluation_report.json', 'w', encoding='utf-8') as f:
            json.dump(report_data, f, ensure_ascii=False, indent=2)
        
        print(f"\n💾 详细报告已保存: batch_evaluation_report.json")
        print(f"✅ 批量评估完成！")

def main():
    evaluator = BatchModelEvaluator()
    evaluator.run_batch_evaluation()

if __name__ == "__main__":
    main()
