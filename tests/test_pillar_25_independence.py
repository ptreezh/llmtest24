#!/usr/bin/env python3
import sys
import os
import unittest
import json
from pathlib import Path
from typing import Dict, List, Any, Optional
import yaml  # Import the PyYAML library

# Add project root to Python path to ensure imports work
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# -*- coding: utf-8 -*-
"""
Pillar 25: 角色独立性测试主文件
集成三大实验系统的综合测试
"""

import sys
# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import os
import unittest
import json
from pathlib import Path
from typing import Dict, List, Any, Optional

# 添加项目根目录到路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from independence.base import IndependenceTestBase
from independence.character_breaking import BreakingStressTest
from independence.implicit_cognition import ImplicitCognitionTest
from independence.longitudinal_consistency import LongitudinalConsistencyTest
from independence.metrics import IndependenceCalculator
from config.config import INDEPENDENCE_CONFIG, MODEL_TO_TEST, DEFAULT_OPTIONS_CREATIVE

# Load roles from YAML file
def load_roles(roles_file: str = "config/roles.yaml") -> Dict[str, str]:
    """从YAML文件加载角色提示词"""
    roles_path = project_root / roles_file
    if not roles_path.exists():
        print(f"⚠️ 警告: 角色配置文件不存在: {roles_path}，将使用默认提示词。")
        return {"software_engineer": f"你是一位资深的软件工程师。"}
    try:
        with open(roles_path, 'r', encoding='utf-8') as f:
            roles = yaml.safe_load(f)
            return roles
    except yaml.YAMLError as e:
        print(f"⚠️ 警告: 角色配置文件解析错误: {e}，将使用默认提示词。")
        return {"software_engineer": f"你是一位资深的软件工程师。"}

def validate_test_integration():
    """验证测试集成的函数，供外部脚本调用"""
    try:
        # 简单地尝试导入必要的模块
        from independence.base import IndependenceTestBase
        from independence.character_breaking import BreakingStressTest
        from independence.implicit_cognition import ImplicitCognitionTest
        from independence.longitudinal_consistency import LongitudinalConsistencyTest
        from independence.metrics import IndependenceCalculator
        print("✅ 所有必要模块导入成功")
        return True
    except ImportError as e:
        print(f"❌ 模块导入失败: {e}")
        return False


def run_independence_test(quick_mode: bool = False, validate_only: bool = False):
    """
    运行角色独立性测试的函数，供外部脚本调用
    
    Args:
        quick_mode: 是否使用快速测试模式
        validate_only: 是否只进行验证而不运行完整测试
        
    Returns:
        bool: 测试是否成功
    """
    try:
        from unittest import TestLoader, TextTestRunner
        from tests.test_pillar_25_independence import TestPillar25Independence
        
        # 创建测试套件
        loader = TestLoader()
        suite = loader.loadTestsFromTestCase(TestPillar25Independence)
        
        # 运行测试
        runner = TextTestRunner(verbosity=2)
        result = runner.run(suite)
        
        return result.wasSuccessful()
        
    except Exception as e:
        print(f"❌ 运行独立性测试失败: {e}")
        return False


class TestPillar25Independence(unittest.TestCase):
    """Pillar 25: 角色独立性综合测试"""

    @classmethod
    def setUpClass(cls):
        """测试类初始化"""
        cls.model_name = INDEPENDENCE_CONFIG.get('model_name', MODEL_TO_TEST)
        cls.config = INDEPENDENCE_CONFIG
        cls.roles = load_roles()  # Load all roles
        cls.results = {}

    def test_01_breaking_stress_experiment(self):
        """测试E1: 角色破功压力测试"""
        print("\n" + "="*60)
        print("🧪 执行测试: E1 角色破功压力测试")
        print("="*60)
        
        for role_name, role_prompt in self.roles.items():
            print(f"  - 正在测试角色: {role_name}")
            try:
                # 初始化测试器
                stress_test = BreakingStressTest(self.config)
                
                # 简化测试配置
                test_config = {
                    'test_roles': {role_name: role_prompt},
                    'stress_levels': ['low', 'medium', 'high']
                }
                stress_test.role_prompts = test_config['test_roles']

                # 执行测试
                result = stress_test.run_experiment(
                    model_name=self.model_name,
                    test_config=test_config
                )
                
                # 验证结果
                self.assertIsInstance(result, dict)
                self.assertIn('summary', result)
                self.assertIn('overall_resistance', result['summary'])
                self.assertIn('test_results', result)
                
                # 保存结果
                if role_name not in self.results:
                    self.results[role_name] = {}
                self.results[role_name]['breaking_stress'] = result
                
                print(f"✅ E1测试完成 - 总体抵抗力: {result.get('summary', {}).get('overall_resistance', 0):.3f}")
                
            except Exception as e:
                print(f"❌ E1测试失败: {e}")
                if role_name not in self.results:
                    self.results[role_name] = {}
                self.results[role_name]['breaking_stress'] = {'error': str(e)}
                self.fail(f"Breaking stress test failed for role {role_name}: {e}")
    
    def test_02_implicit_cognition_experiment(self):
        """测试E2: 隐式认知测试"""
        print("\n" + "="*60)
        print("🧪 执行测试: E2 隐式认知测试")
        print("="*60)
        
        for role_name, role_prompt in self.roles.items():
            print(f"  - 正在测试角色: {role_name}")
            try:
                # 初始化测试器
                cognition_test = ImplicitCognitionTest(self.config)
                
                # 测试配置
                test_config = {
                    'role_prompt': role_prompt,
                    'test_categories': ["世界观测试", "专业知识测试"] # 减少测试类别以节省时间
                }

                # 执行测试
                result = cognition_test.run_experiment(
                    model_name=self.model_name,
                    test_config=test_config
                )
                
                # 验证结果
                self.assertIsInstance(result, dict)
                self.assertIn('summary', result)
                self.assertIn('overall_implicit_score', result['summary'])
                self.assertIn('test_results', result)
                
                # 保存结果
                if role_name not in self.results:
                    self.results[role_name] = {}
                self.results[role_name]['implicit_cognition'] = result
                
                print(f"✅ E2测试完成 - 总体得分: {result.get('summary', {}).get('overall_implicit_score', 0):.3f}")
                
            except Exception as e:
                print(f"❌ E2测试失败: {e}")
                if role_name not in self.results:
                    self.results[role_name] = {}
                self.results[role_name]['implicit_cognition'] = {'error': str(e)}
                self.fail(f"Implicit cognition test failed for role {role_name}: {e}")
    
    def test_03_longitudinal_consistency_experiment(self):
        """测试E3: 纵向一致性测试"""
        print("\n" + "="*60)
        print("🧪 执行测试: E3 纵向一致性测试")
        print("="*60)
        
        for role_name, role_prompt in self.roles.items():
            print(f"  - 正在测试角色: {role_name}")
            try:
                # 初始化测试器
                consistency_test = LongitudinalConsistencyTest(self.config)
                
                # 测试配置
                test_config = {
                    'role_prompt': role_prompt,
                    'conversation_turns': 3, # 减少轮次
                    'consistency_checks': 2  # 减少检查
                }

                # 执行测试
                result = consistency_test.run_experiment(
                    model_name=self.model_name,
                    test_config=test_config
                )
                
                # 验证结果
                self.assertIsInstance(result, dict)
                self.assertIn('summary', result)
                self.assertIn('overall_consistency', result['summary'])
                self.assertIn('conversation_history', result)
                
                # 保存结果
                if role_name not in self.results:
                    self.results[role_name] = {}
                self.results[role_name]['longitudinal_consistency'] = result
                
                print(f"✅ E3测试完成 - 总体一致性: {result.get('summary', {}).get('overall_consistency', 0):.3f}")
                
            except Exception as e:
                print(f"❌ E3测试失败: {e}")
                if role_name not in self.results:
                    self.results[role_name] = {}
                self.results[role_name]['longitudinal_consistency'] = {'error': str(e)}
                self.fail(f"Longitudinal consistency test failed for role {role_name}: {e}")
    
    def test_04_comprehensive_independence_calculation(self):
        """测试综合独立性计算"""
        print("\n" + "="*60)
        print("🧪 执行测试: 综合独立性计算")
        print("="*60)
        
        for role_name in self.roles.keys():
            print(f"  - 正在计算角色: {role_name}")
            try:
                # 确保前面的测试已完成
                if not self.results or role_name not in self.results or 'breaking_stress' not in self.results[role_name] or 'implicit_cognition' not in self.results[role_name] or 'longitudinal_consistency' not in self.results[role_name]:
                    print(f"⚠️ 警告: 角色 {role_name} 的实验结果不完整，跳过综合计算。")
                    continue
                
                # 初始化计算器
                calculator = IndependenceCalculator()
                
                # 计算综合独立性
                independence_score = calculator.calculate_comprehensive_independence(
                    breaking_stress_result=self.results[role_name].get('breaking_stress'),
                    implicit_cognition_result=self.results[role_name].get('implicit_cognition'),
                    longitudinal_consistency_result=self.results[role_name].get('longitudinal_consistency')
                )
                
                # 验证结果
                self.assertIsInstance(independence_score, dict)
                self.assertIn('final_score', independence_score)
                self.assertIn('grade', independence_score)
                
                # 保存最终结果
                if role_name not in self.results:
                    self.results[role_name] = {}
                self.results[role_name]['final_independence'] = independence_score
                
                print(f"✅ 综合计算完成 - 最终得分: {independence_score.get('final_score', 0):.3f}")
                print(f"📊 独立性等级: {independence_score.get('grade', 'Unknown')}")
                
            except Exception as e:
                print(f"❌ 综合计算失败: {e}")
                if role_name not in self.results:
                    self.results[role_name] = {}
                self.results[role_name]['final_independence'] = {'error': str(e)}
                self.fail(f"Comprehensive calculation failed for role {role_name}: {e}")
    
    def test_05_generate_final_report(self):
        """生成最终测试报告"""
        print("\n" + "="*60)
        print("📊 生成最终测试报告")
        print("="*60)
        
        try:
            # 生成报告
            report = self._generate_test_report()
            
            # 保存报告到文件
            output_dir = Path("testout")
            output_dir.mkdir(exist_ok=True)
            
            report_file = output_dir / "pillar_25_independence_report.json"
            with open(report_file, 'w', encoding='utf-8') as f:
                json.dump(report, f, ensure_ascii=False, indent=2)
            
            print(f"✅ 报告已保存: {report_file}")
            
            # 打印摘要
            self._print_test_summary(report)
            
            return {"success": True} # Add this line
        except Exception as e:
            print(f"❌ 报告生成失败: {e}")
            self.fail(f"Report generation failed: {e}")
            return {"success": False, "error": str(e)} # Add this line
    
    def _generate_test_report(self) -> Dict[str, Any]:
        """生成测试报告"""
        report = {
            'test_info': {
                'pillar': 'Pillar 25: Role Independence',
                'model': self.model_name,
                'timestamp': str(Path(__file__).stat().st_mtime)
            },
            'experiment_results': self.results,
            'summary': {
                'total_experiments': 0,
                'final_score': 0,
                'grade': 'Unknown'
            }
        }
        
        # 计算总实验数和最终得分
        total_experiments = 0
        final_score_sum = 0
        valid_roles = 0
        for role_name, role_results in self.results.items():
            if 'final_independence' in role_results and isinstance(role_results['final_independence'], dict) and 'final_score' in role_results['final_independence']:
                total_experiments += 1
                final_score_sum += role_results['final_independence']['final_score']
                valid_roles += 1
        
        if valid_roles > 0:
            report['summary']['total_experiments'] = total_experiments
            report['summary']['final_score'] = final_score_sum / valid_roles
            # 简化等级计算
            if report['summary']['final_score'] >= 0.8:
                report['summary']['grade'] = 'A'
            elif report['summary']['final_score'] >= 0.6:
                report['summary']['grade'] = 'B'
            elif report['summary']['final_score'] >= 0.4:
                report['summary']['grade'] = 'C'
            elif report['summary']['final_score'] >= 0.2:
                report['summary']['grade'] = 'D'
            else:
                report['summary']['grade'] = 'F'
        
        return report
    
    def _print_test_summary(self, report: Dict[str, Any]):
        """打印测试摘要"""
        print("\n" + "="*60)
        print("📋 测试摘要")
        print("="*60)
        
        summary = report.get('summary', {})
        print(f"模型: {self.model_name}")
        print(f"实验数量: {summary.get('total_experiments', 0)}")
        print(f"最终得分: {summary.get('final_score', 0):.3f}")
        print(f"独立性等级: {summary.get('grade', 'Unknown')}")
