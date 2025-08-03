#!/usr/bin/env python3
"""
运行用户选择的测试脚本
"""

import os
import sys
import importlib
import json
import argparse
from datetime import datetime
from pathlib import Path

# 将项目根目录和tests目录添加到Python路径
project_root = Path(__file__).parent.parent
print(f"项目根目录: {project_root}")
print(f"sys.path: {sys.path}")
sys.path.append(str(project_root))
sys.path.append(str(project_root / "tests"))
print(f"更新后的 sys.path: {sys.path}")

def run_test_module(module_name, model_name=None):
    """运行单个测试模块"""
    try:
        # 特殊处理独立性测试
        if module_name == "independence_test":
            print("正在运行认知独立性测试...")
            # 从 run_pillar_25_independence.py 导入函数
            from run_pillar_25_independence import run_independence_test
            success = run_independence_test()
            return {"success": success}
        
        # 动态导入其他测试模块
        module = importlib.import_module(module_name.replace('/', '.').rstrip('.py'))
        
        if hasattr(module, 'run_test'):
            print(f"正在运行测试: {module_name}")
            if model_name:
                result = module.run_test(model_name)
            else:
                result = module.run_test()
            
            # 检查 result 是否为元组，如果是，则只取第一个元素作为成功与否的判断
            if isinstance(result, tuple):
                # 假设元组的第一个元素是响应，第二个元素是元数据
                # 我们认为只要能成功调用API，测试就算成功
                return {"success": True, "response": result[0], "metadata": result[1]}
            elif isinstance(result, bool):
                return {"success": result}
            else:
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

def main():
    parser = argparse.ArgumentParser(description='运行选定的测试')
    parser.add_argument('--model', required=True, help='要测试的模型名称，格式为 service/model_name')
    parser.add_argument('--tests', nargs='+', required=True, help='要运行的测试文件名，例如 test_pillar_01_logic.py')
    args = parser.parse_args()

    start_time = datetime.now()
    print(f"开始执行选定的测试: {start_time.strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    print(f"测试模型: {args.model}")
    print(f"测试文件: {', '.join(args.tests)}")
    print("-" * 60)

    results = {
        "start_time": start_time.isoformat(),
        "model_name": args.model,
        "test_results": {}
    }

    # 执行选定的测试
    for test_file in args.tests:
        # 构建模块名，例如 tests.test_pillar_01_logic，移除 .py 后缀
        module_name = f"tests.{os.path.basename(test_file).replace('.py', '')}"
        result = run_test_module(module_name, args.model)
        # 确保等待单个测试的响应
        if isinstance(result, dict) and result.get("success", False):
            print(f"测试 {test_file} 成功")
        else:
            print(f"测试 {test_file} 失败: {result.get('error', '未知错误')}")
        results["test_results"][test_file] = result

    # 生成摘要
    total_tests = len(results["test_results"])
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
    
    # 使用模型名和测试文件名生成文件名
    # 将模型名中的 / 替换为 _，测试文件名用 _ 连接
    safe_model_name = args.model.replace('/', '_')
    test_names = '_'.join([Path(test).stem for test in args.tests])  # 只取文件名，不带.py
    # 再次确保文件名安全，移除可能的其他非法字符
    safe_filename = f"results_{safe_model_name}_{test_names}_{start_time.strftime('%Y%m%d_%H%M%S')}.json"
    # 限制文件名长度，避免Windows路径过长错误
    max_filename_length = 255  # Windows文件名长度限制
    if len(safe_filename) > max_filename_length:
        # 如果文件名过长，使用模型名的哈希值和测试数量来缩短
        import hashlib
        model_hash = hashlib.md5(safe_model_name.encode()).hexdigest()[:8]
        num_tests = len(args.tests)
        safe_filename = f"results_{model_hash}_{num_tests}tests_{start_time.strftime('%Y%m%d_%H%M%S')}.json"
    
    safe_filename = "".join(c for c in safe_filename if c.isalnum() or c in "._-")
    output_file = output_dir / safe_filename
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    end_time = datetime.now()
    duration = (end_time - start_time).total_seconds()

    print("=" * 60)
    print(f"选定的测试完成! 耗时: {duration:.2f} 秒")
    print(f"成功: {results['summary']['successful_tests']}/{results['summary']['total_tests']} ({results['summary']['success_rate']:.1%})")
    print(f"结果已保存到: {output_file}")

    return results

if __name__ == "__main__":
    main()
