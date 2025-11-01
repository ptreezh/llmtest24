#!/usr/bin/env python3
"""
主测试编排脚本
执行完整的1-24测试体系
"""

import os
import sys
import importlib
import json
from datetime import datetime
from pathlib import Path

# 将项目根目录和tests目录添加到Python路径
project_root = Path(__file__).parent
sys.path.append(str(project_root))
sys.path.append(str(project_root / "tests"))

def discover_tests(test_dir="tests"):
    """发现所有测试文件"""
    test_files = []
    test_path = Path(test_dir)
    
    if test_path.exists():
        for file_path in test_path.glob("test_pillar_*.py"):
            if file_path.name != "test_pillar_25_independence.py":  # 排除独立性测试，将单独处理
                test_files.append(file_path)
    
    # 按文件名排序，确保测试按顺序执行
    test_files.sort(key=lambda x: x.name)
    return test_files

def run_test_module(module_name, model_name=None):
    """运行单个测试模块"""
    try:
        # 动态导入测试模块
        module = importlib.import_module(module_name.replace('/', '.').rstrip('.py'))
        
        if hasattr(module, 'run_test'):
            print(f"正在运行测试: {module_name}")
            if model_name:
                result = module.run_test(model_name)
            else:
                result = module.run_test()
            
            if isinstance(result, bool):
                return {"success": result}
            return result
        else:
            return {
                "success": False,
                "error": f"模块 {module_name} 缺少 run_test 函数"
            }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "traceback": str(e.__traceback__)
        }

def run_independence_tests(model_name=None):
    """运行独立性测试"""
    try:
        # 修正导入路径，从 tests.test_pillar_25_independence 导入 run_independence_test
        from tests.test_pillar_25_independence import run_independence_test as run_pillar_25_independence_test
        print("正在运行独立性测试 (Pillar 25)...")
        result = run_pillar_25_independence_test(model_name)
        return result
    except ImportError as e:
        return {
            "success": False,
            "error": f"无法导入独立性测试 (Pillar 25): {str(e)}"
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "traceback": str(e.__traceback__)
        }

def main():
    """主函数"""
    start_time = datetime.now()
    print(f"开始执行完整测试套件: {start_time.strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)

    # 定义要测试的模型
    model_name = "glm/glm-4-plus"
    print(f"测试模型: {model_name}")
    
    # 发现所有测试
    test_files = discover_tests()
    print(f"发现 {len(test_files)} 个测试文件")
    print("-" * 60)
    
    # 执行测试
    results = {
        "start_time": start_time.isoformat(),
        "model_name": model_name,
        "test_results": {},
        "summary": {}
    }
    
    # 执行基础和高级测试
    for test_file in test_files:
        module_name = str(test_file).replace(os.sep, '.')
        result = run_test_module(module_name, model_name)
        results["test_results"][module_name] = result
    
    # 执行独立性测试
    independence_result = run_independence_tests(model_name)
    results["test_results"]["independence_test"] = independence_result
    
    # 生成摘要
    total_tests = len(results["test_results"])
    # 修正：处理返回列表的测试结果
    successful_tests = sum(1 for r in results["test_results"].values() if isinstance(r, dict) and r.get("success", False))
    results["summary"] = {
        "total_tests": total_tests,
        "successful_tests": successful_tests,
        "success_rate": successful_tests / total_tests if total_tests > 0 else 0,
        "end_time": datetime.now().isoformat()
    }
    
    # 保存结果
    output_dir = Path("testout")
    output_dir.mkdir(exist_ok=True)
    
    timestamp = start_time.strftime("%Y%m%d_%H%M%S")
    output_file = output_dir / f"comprehensive_test_results_{timestamp}.json"
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    
    end_time = datetime.now()
    duration = (end_time - start_time).total_seconds()
    
    print("=" * 60)
    print(f"测试完成! 耗时: {duration:.2f} 秒")
    # 计算总测试数和成功测试数
    total_tests = 0
    successful_tests = 0
    for model_name, model_results in results["test_results"].items():
        total_tests += len(model_results)
        successful_tests += sum(1 for r in model_results.values() if r.get("success", False))
    
    # 计算总成功率
    success_rate = successful_tests / total_tests if total_tests > 0 else 0
    
    results["summary"] = {
        "total_tests": total_tests,
        "successful_tests": successful_tests,
        "success_rate": success_rate,
        "end_time": datetime.now().isoformat()
    }
    
    print("=" * 60)
    print(f"测试完成! 耗时: {duration:.2f} 秒")
    print(f"成功: {successful_tests}/{total_tests} ({results['summary']['success_rate']:.1%})")
    print(f"结果已保存到: {output_file}")
    
    return results

if __name__ == "__main__":
    main()
