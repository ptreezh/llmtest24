#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
云模型角色独立性批量测试脚本

使用真实的云LLM模型进行角色独立性测试，评估不同模型的表现。
"""

import sys
import os
import json
import time
from datetime import datetime
from typing import Dict, List, Any
from pathlib import Path
import argparse # Import argparse

# 添加项目根目录到Python路径
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))
print(f"Current sys.path: {sys.path}")
print(f"Project root: {project_root}")

# 导入云服务和独立性测试模块
import importlib.util
import os

# 构建cloud_services.py的绝对路径
cloud_services_path = os.path.join(project_root, "scripts", "utils", "cloud_services.py")
spec = importlib.util.spec_from_file_location("cloud_services", cloud_services_path)
cloud_services = importlib.util.module_from_spec(spec)
spec.loader.exec_module(cloud_services)

# 从模块中导入需要的变量
CLOUD_SERVICES = cloud_services.CLOUD_SERVICES
get_available_services = cloud_services.get_available_services
from independence.character_breaking import BreakingStressTest
from independence.implicit_cognition import ImplicitCognitionTest
from independence.longitudinal_consistency import LongitudinalConsistencyTest
from independence.metrics.independence_calculator import IndependenceCalculator
from config.config import INDEPENDENCE_CONFIG

def load_role_prompt(role_name: str) -> str:
    """从文件加载角色提示词"""
    prompt_path = project_root / "role_prompts" / f"{role_name}_prompt.txt"
    if not prompt_path.exists():
        print(f"⚠️ 警告: 角色提示词文件不存在: {prompt_path}，将使用默认提示词。")
        return f"你是一位资深的{role_name}。"
    
    with open(prompt_path, 'r', encoding='utf-8') as f:
        return f.read()

class CloudIndependenceTester:
    """云模型角色独立性测试器"""

    def __init__(self):
        self.available_services = get_available_services()

    def get_available_models(self) -> List[Dict[str, str]]:
        """获取可用的云模型列表"""
        models = []
        for service_name in self.available_services:
            service_config = CLOUD_SERVICES.get(service_name, {})
            for model_name in service_config.get('models', []):
                models.append({
                    'service': service_name,
                    'model': model_name,
                    'full_name': f"{service_name}/{model_name}",
                    'service_display_name': service_config.get('name', service_name)
                })
        return models

    def run_single_model_test(self, model_full_name: str) -> Dict[str, Any]:
        """对单个模型运行完整的独立性测试"""
        print(f"\n🧠 测试模型: {model_full_name}")
        print("=" * 60)
        
        start_time = time.time()
        
        # 加载防御加强的角色提示词
        test_role_prompt = load_role_prompt("software_engineer")
        
        test_config = INDEPENDENCE_CONFIG.copy()
        test_config['model_name'] = model_full_name
        
        stress_test = BreakingStressTest(test_config)
        cognition_test = ImplicitCognitionTest(test_config)
        consistency_test = LongitudinalConsistencyTest(test_config)
        calculator = IndependenceCalculator()
        
        individual_results = {}
        
        try:
            # 1. 角色破功压力测试
            print("  🧪 运行 E1: 角色破功压力测试...")
            stress_config = {'test_roles': {'software_engineer': test_role_prompt}, 'stress_levels': ['low', 'medium', 'high']}
            stress_result = stress_test.run_experiment(model_full_name, stress_config)
            individual_results['breaking_stress'] = stress_result
            print(f"    ✅ E1 完成 - 抵抗力: {stress_result.get('summary', {}).get('overall_resistance', 0):.3f}")

            # 2. 隐式认知测试
            print("  🧪 运行 E2: 隐式认知测试...")
            cognition_config = {'role_prompt': test_role_prompt}
            cognition_result = cognition_test.run_experiment(model_full_name, cognition_config)
            individual_results['implicit_cognition'] = cognition_result
            print(f"    ✅ E2 完成 - 得分: {cognition_result.get('summary', {}).get('overall_implicit_score', 0):.3f}")

            # 3. 纵向一致性测试
            print("  🧪 运行 E3: 纵向一致性测试...")
            consistency_config = {'role_prompt': test_role_prompt}
            consistency_result = consistency_test.run_experiment(model_full_name, consistency_config)
            individual_results['longitudinal_consistency'] = consistency_result
            print(f"    ✅ E3 完成 - 一致性: {consistency_result.get('summary', {}).get('overall_consistency', 0):.3f}")

            # 4. 计算综合得分
            print("  📊 计算综合独立性得分...")
            final_score = calculator.calculate_comprehensive_independence(
                breaking_stress_result=stress_result,
                implicit_cognition_result=cognition_result,
                longitudinal_consistency_result=consistency_result
            )
            individual_results['final_independence'] = final_score
            print(f"    ✅ 综合得分: {final_score.get('final_score', 0):.3f}, 等级: {final_score.get('grade', 'N/A')}")

            end_time = time.time()
            return {
                'model_name': model_full_name, 'status': 'success',
                'test_duration': end_time - start_time, 'scores': final_score,
                'details': individual_results
            }

        except Exception as e:
            print(f"❌ 测试失败: {e}")
            import traceback
            traceback.print_exc()
            return {
                'model_name': model_full_name, 'status': 'failed',
                'error': str(e), 'test_duration': time.time() - start_time
            }

    def run_batch_test(self, models_to_run: List[Dict[str, str]]):
        """批量测试多个模型"""
        print("🚀 开始批量角色独立性测试 (云模型)")
        print(f"📊 测试模型数量: {len(models_to_run)}")
        print("=" * 80)

        results = {}
        for i, model_info in enumerate(models_to_run, 1):
            print(f"\n📍 进度: {i}/{len(models_to_run)}")
            result = self.run_single_model_test(model_info['full_name'])
            results[model_info['full_name']] = result
            time.sleep(2)

        return results

    def save_results(self, results: Dict[str, Any], filename: str = None):
        """保存测试结果"""
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"cloud_independence_test_results_{timestamp}.json"
        
        results_dir = Path("testout")
        results_dir.mkdir(exist_ok=True)
        filepath = results_dir / filename
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
        
        print(f"📁 测试结果已保存到: {filepath}")

def main():
    """主函数"""
    print("🧠 云模型角色独立性测试器")
    print("=" * 50)
    
    parser = argparse.ArgumentParser(description="Cloud Model Independence Test Runner.")
    parser.add_argument("--model", type=str, help="Specify a particular cloud model to test (e.g., 'service_name/model_name'). If not provided, all available models will be tested.")
    args = parser.parse_args()

    tester = CloudIndependenceTester()
    available_models = tester.get_available_models()

    if not available_models:
        print("❌ 没有找到可用的云模型。请检查 cloud_services.py 和 .env 文件。")
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
        confirm = input("\n是否开始对所有可用模型进行测试？(y/N): ").strip().lower()
        if confirm not in ['y', 'yes', '是']:
            print("测试已取消。")
            return
        models_to_test = available_models

    if models_to_test:
        results = tester.run_batch_test(models_to_test)
        tester.save_results(results)
    else:
        print("没有模型可供测试。")

if __name__ == "__main__":
    main()
