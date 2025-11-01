#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
最终解决方案 - Web界面修复和测试
"""

import os
import sys
import time
import json
import requests
from pathlib import Path

def main():
    """主函数"""
    print("🎯 LLM Advanced Testing Suite - 最终解决方案")
    print("=" * 60)
    
    base_url = "http://localhost:8501"
    test_results = []
    
    # 测试1: 检查Web界面是否运行
    print("\n测试1: 检查Web界面状态")
    try:
        response = requests.get(f"{base_url}/", timeout=10)
        if response.status_code == 200:
            print("✅ Web界面正在运行")
            test_results.append({"test": "Web界面状态", "status": "PASS", "message": "Web界面正在运行"})
        else:
            print(f"❌ Web界面返回错误状态: {response.status_code}")
            test_results.append({"test": "Web界面状态", "status": "FAIL", "message": f"状态码: {response.status_code}"})
    except Exception as e:
        print(f"❌ Web界面未运行: {e}")
        test_results.append({"test": "Web界面状态", "status": "FAIL", "message": f"连接失败: {e}"})
    
    # 测试2: 检查API端点
    print("\n测试2: 检查API端点")
    api_endpoints = ["/api/models", "/api/tests", "/api/results"]
    
    for endpoint in api_endpoints:
        try:
            response = requests.get(f"{base_url}{endpoint}", timeout=10)
            if response.status_code == 200:
                print(f"✅ {endpoint} 正常")
                test_results.append({"test": f"API端点 {endpoint}", "status": "PASS", "message": "正常"})
            else:
                print(f"❌ {endpoint} 返回错误: {response.status_code}")
                test_results.append({"test": f"API端点 {endpoint}", "status": "FAIL", "message": f"状态码: {response.status_code}"})
        except Exception as e:
            print(f"❌ {endpoint} 连接失败: {e}")
            test_results.append({"test": f"API端点 {endpoint}", "status": "FAIL", "message": f"连接失败: {e}"})
    
    # 测试3: 检查功能
    print("\n测试3: 检查功能")
    try:
        test_data = {
            "pillar_name": "pillar_01_logic",
            "prompt": "测试提示",
            "model_name": "test_model"
        }
        
        response = requests.post(
            f"{base_url}/api/run_test",
            json=test_data,
            headers={"Content-Type": "application/json"},
            timeout=30
        )
        
        if response.status_code == 200:
            print("✅ run_test功能正常")
            test_results.append({"test": "run_test功能", "status": "PASS", "message": "功能正常"})
        else:
            print(f"❌ run_test功能错误: {response.status_code}")
            test_results.append({"test": "run_test功能", "status": "FAIL", "message": f"状态码: {response.status_code}"})
    except Exception as e:
        print(f"❌ run_test功能失败: {e}")
        test_results.append({"test": "run_test功能", "status": "FAIL", "message": f"连接失败: {e}"})
    
    # 生成报告
    print("\n📊 生成测试报告")
    
    # 统计结果
    total_tests = len(test_results)
    passed_tests = len([r for r in test_results if r["status"] == "PASS"])
    failed_tests = len([r for r in test_results if r["status"] == "FAIL"])
    
    print(f"总测试数: {total_tests}")
    print(f"通过测试: {passed_tests}")
    print(f"失败测试: {failed_tests}")
    
    if total_tests > 0:
        success_rate = (passed_tests/total_tests)*100
        print(f"成功率: {success_rate:.1f}%")
    
    # 保存报告
    report_file = Path("test_reports/final_solution_report.json")
    report_file.parent.mkdir(parents=True, exist_ok=True)
    
    report_data = {
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "total_tests": total_tests,
        "passed_tests": passed_tests,
        "failed_tests": failed_tests,
        "success_rate": (passed_tests/total_tests)*100 if total_tests > 0 else 0,
        "results": test_results
    }
    
    with open(report_file, 'w', encoding='utf-8') as f:
        json.dump(report_data, f, indent=2, ensure_ascii=False)
    
    print(f"📄 报告已保存: {report_file}")
    
    # 生成HTML报告
    html_content = f"""
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>LLM Advanced Testing Suite - 最终解决方案报告</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; }}
        .header {{ background-color: #1f77b4; color: white; padding: 20px; text-align: center; }}
        .summary {{ background-color: #f0f2f6; padding: 15px; margin: 20px 0; border-radius: 5px; }}
        .test-result {{ margin: 10px 0; padding: 10px; border-radius: 5px; }}
        .pass {{ background-color: #d4edda; color: #155724; }}
        .fail {{ background-color: #f8d7da; color: #721c24; }}
        .metrics {{ display: flex; justify-content: space-around; margin: 20px 0; }}
        .metric {{ text-align: center; padding: 15px; background-color: #e9ecef; border-radius: 5px; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>🎯 LLM Advanced Testing Suite</h1>
        <h2>最终解决方案报告</h2>
        <p>生成时间: {report_data['timestamp']}</p>
    </div>
    
    <div class="summary">
        <h3>测试概览</h3>
        <div class="metrics">
            <div class="metric">
                <h4>总测试数</h4>
                <p>{report_data['total_tests']}</p>
            </div>
            <div class="metric">
                <h4>通过测试</h4>
                <p>{report_data['passed_tests']}</p>
            </div>
            <div class="metric">
                <h4>失败测试</h4>
                <p>{report_data['failed_tests']}</p>
            </div>
            <div class="metric">
                <h4>成功率</h4>
                <p>{report_data['success_rate']:.1f}%</p>
            </div>
        </div>
    </div>
    
    <div>
        <h3>详细结果</h3>
        {generate_test_results_html(report_data['results'])}
    </div>
    
    <div style="margin-top: 30px; text-align: center; color: #666;">
        <p>LLM Advanced Testing Suite - 最终解决方案报告</p>
    </div>
</body>
</html>
    """
    
    html_file = Path("test_reports/final_solution_report.html")
    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"📄 HTML报告已生成: {html_file}")
    
    # 输出最终结果
    print("\n" + "=" * 60)
    if passed_tests == total_tests:
        print("🎉 所有测试通过！Web界面运行正常！")
        print(f"🌐 访问地址: {base_url}")
        print("✅ 最终解决方案成功！")
    else:
        print("❌ 部分测试失败！需要修复！")
        print("🔧 请检查Web界面是否正常运行")
    
    return passed_tests == total_tests

def generate_test_results_html(results):
    """生成测试结果HTML"""
    html = ""
    for result in results:
        status_class = result["status"].lower()
        html += f"""
        <div class="test-result {status_class}">
            <h4>{result['test']}</h4>
            <p><strong>状态:</strong> {result['status']}</p>
            <p><strong>消息:</strong> {result['message']}</p>
        </div>
        """
    return html

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)