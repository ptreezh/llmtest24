#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
专家级Web界面测试和修复脚本
"""

import os
import sys
import time
import json
import requests
import subprocess
from pathlib import Path

class ExpertWebTester:
    """专家级Web界面测试器"""
    
    def __init__(self):
        self.base_url = "http://localhost:8501"
        self.test_results = []
        self.max_retries = 3
        
    def test_web_interface(self):
        """测试Web界面"""
        print("🧪 LLM Advanced Testing Suite - 专家级Web界面测试")
        print("=" * 70)
        
        # 测试1: 基础连接
        print("\n测试1: 基础连接测试")
        self.test_basic_connection()
        
        # 测试2: API端点
        print("\n测试2: API端点测试")
        self.test_api_endpoints()
        
        # 测试3: 性能测试
        print("\n测试3: 性能测试")
        self.test_performance()
        
        # 测试4: 功能测试
        print("\n测试4: 功能测试")
        self.test_functionality()
        
        # 生成报告
        self.generate_report()
        
        return len([r for r in self.test_results if r["status"] == "PASS"]) == len(self.test_results)
    
    def test_basic_connection(self):
        """测试基础连接"""
        for i in range(self.max_retries):
            try:
                response = requests.get(f"{self.base_url}/", timeout=10)
                if response.status_code == 200:
                    self.test_results.append({
                        "test": "基础连接",
                        "status": "PASS",
                        "message": f"连接成功 (尝试 {i+1})",
                        "response_time": response.elapsed.total_seconds()
                    })
                    print(f"✅ 基础连接测试通过 (尝试 {i+1})")
                    return
                else:
                    print(f"⚠️ 基础连接测试失败: {response.status_code} (尝试 {i+1})")
            except Exception as e:
                print(f"⚠️ 基础连接测试错误: {e} (尝试 {i+1})")
            
            if i < self.max_retries - 1:
                time.sleep(5)
        
        self.test_results.append({
            "test": "基础连接",
            "status": "FAIL",
            "message": "连接失败",
            "response_time": 0
        })
        print("❌ 基础连接测试失败")
    
    def test_api_endpoints(self):
        """测试API端点"""
        endpoints = [
            ("/api/models", "GET"),
            ("/api/tests", "GET"),
            ("/api/results", "GET"),
            ("/api/health", "GET")
        ]
        
        for endpoint, method in endpoints:
            try:
                if method == "GET":
                    response = requests.get(f"{self.base_url}{endpoint}", timeout=10)
                else:
                    response = requests.post(f"{self.base_url}{endpoint}", timeout=10)
                
                if response.status_code == 200:
                    self.test_results.append({
                        "test": f"API端点 {endpoint}",
                        "status": "PASS",
                        "message": f"{method} {endpoint} - {response.status_code}",
                        "response_time": response.elapsed.total_seconds()
                    })
                    print(f"✅ API端点测试通过: {method} {endpoint}")
                else:
                    self.test_results.append({
                        "test": f"API端点 {endpoint}",
                        "status": "FAIL",
                        "message": f"{method} {endpoint} - {response.status_code}",
                        "response_time": response.elapsed.total_seconds()
                    })
                    print(f"❌ API端点测试失败: {method} {endpoint} - {response.status_code}")
                    
            except Exception as e:
                self.test_results.append({
                    "test": f"API端点 {endpoint}",
                    "status": "FAIL",
                    "message": f"连接错误: {e}",
                    "response_time": 0
                })
                print(f"❌ API端点测试错误: {method} {endpoint} - {e}")
    
    def test_performance(self):
        """测试性能"""
        pages = ["/", "/api/models", "/api/tests", "/api/results"]
        
        for page in pages:
            start_time = time.time()
            try:
                response = requests.get(f"{self.base_url}{page}", timeout=15)
                end_time = time.time()
                load_time = end_time - start_time
                
                if load_time < 3.0:
                    self.test_results.append({
                        "test": f"性能测试 {page}",
                        "status": "PASS",
                        "message": f"加载时间: {load_time:.2f}s",
                        "response_time": load_time
                    })
                    print(f"✅ 性能测试通过: {page} - {load_time:.2f}s")
                else:
                    self.test_results.append({
                        "test": f"性能测试 {page}",
                        "status": "WARN",
                        "message": f"加载时间过长: {load_time:.2f}s",
                        "response_time": load_time
                    })
                    print(f"⚠️ 性能测试警告: {page} - {load_time:.2f}s")
                    
            except Exception as e:
                self.test_results.append({
                    "test": f"性能测试 {page}",
                    "status": "FAIL",
                    "message": f"测试失败: {e}",
                    "response_time": 0
                })
                print(f"❌ 性能测试失败: {page} - {e}")
    
    def test_functionality(self):
        """测试功能"""
        # 测试run_test端点
        test_data = {
            "pillar_name": "pillar_01_logic",
            "prompt": "If all roses are flowers and some flowers fade quickly, can we conclude that some roses fade quickly?",
            "model_name": "test_model"
        }
        
        try:
            response = requests.post(
                f"{self.base_url}/api/run_test",
                json=test_data,
                headers={"Content-Type": "application/json"},
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                if "success" in result and "score" in result:
                    self.test_results.append({
                        "test": "功能测试 - run_test",
                        "status": "PASS",
                        "message": "run_test端点测试通过",
                        "response_time": response.elapsed.total_seconds()
                    })
                    print("✅ 功能测试通过: run_test端点")
                else:
                    self.test_results.append({
                        "test": "功能测试 - run_test",
                        "status": "FAIL",
                        "message": "run_test端点返回格式错误",
                        "response_time": response.elapsed.total_seconds()
                    })
                    print("❌ 功能测试失败: run_test端点返回格式错误")
            else:
                self.test_results.append({
                    "test": "功能测试 - run_test",
                    "status": "FAIL",
                    "message": f"run_test端点返回错误: {response.status_code}",
                    "response_time": response.elapsed.total_seconds()
                })
                print(f"❌ 功能测试失败: run_test端点返回错误: {response.status_code}")
                
        except Exception as e:
            self.test_results.append({
                "test": "功能测试 - run_test",
                "status": "FAIL",
                "message": f"run_test端点测试失败: {e}",
                "response_time": 0
            })
            print(f"❌ 功能测试失败: run_test端点测试失败: {e}")
    
    def generate_report(self):
        """生成测试报告"""
        print("\n📊 测试报告")
        print("=" * 50)
        
        # 统计结果
        total_tests = len(self.test_results)
        passed_tests = len([r for r in self.test_results if r["status"] == "PASS"])
        failed_tests = len([r for r in self.test_results if r["status"] == "FAIL"])
        warning_tests = len([r for r in self.test_results if r["status"] == "WARN"])
        
        print(f"总测试数: {total_tests}")
        print(f"通过测试: {passed_tests}")
        print(f"失败测试: {failed_tests}")
        print(f"警告测试: {warning_tests}")
        
        if total_tests > 0:
            success_rate = (passed_tests/total_tests)*100
            print(f"成功率: {success_rate:.1f}%")
        
        # 计算平均响应时间
        response_times = [r.get("response_time", 0) for r in self.test_results if "response_time" in r]
        if response_times:
            avg_response_time = sum(response_times) / len(response_times)
            print(f"平均响应时间: {avg_response_time:.2f}s")
        
        # 保存详细报告
        report_file = Path("test_reports/web_interface_test_report.json")
        report_file.parent.mkdir(parents=True, exist_ok=True)
        
        report_data = {
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "total_tests": total_tests,
            "passed_tests": passed_tests,
            "failed_tests": failed_tests,
            "warning_tests": warning_tests,
            "success_rate": (passed_tests/total_tests)*100 if total_tests > 0 else 0,
            "average_response_time": avg_response_time if response_times else 0,
            "results": self.test_results
        }
        
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(report_data, f, indent=2, ensure_ascii=False)
        
        print(f"\n📄 详细报告已保存: {report_file}")
        
        # 生成HTML报告
        self.generate_html_report(report_data)
    
    def generate_html_report(self, report_data):
        """生成HTML报告"""
        html_content = f"""
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>LLM Advanced Testing Suite - Web界面测试报告</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; }}
        .header {{ background-color: #1f77b4; color: white; padding: 20px; text-align: center; }}
        .summary {{ background-color: #f0f2f6; padding: 15px; margin: 20px 0; border-radius: 5px; }}
        .test-result {{ margin: 10px 0; padding: 10px; border-radius: 5px; }}
        .pass {{ background-color: #d4edda; color: #155724; }}
        .fail {{ background-color: #f8d7da; color: #721c24; }}
        .warn {{ background-color: #fff3cd; color: #856404; }}
        .metrics {{ display: flex; justify-content: space-around; margin: 20px 0; }}
        .metric {{ text-align: center; padding: 15px; background-color: #e9ecef; border-radius: 5px; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>🧪 LLM Advanced Testing Suite</h1>
        <h2>Web界面测试报告</h2>
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
                <h4>警告测试</h4>
                <p>{report_data['warning_tests']}</p>
            </div>
            <div class="metric">
                <h4>成功率</h4>
                <p>{report_data['success_rate']:.1f}%</p>
            </div>
        </div>
    </div>
    
    <div>
        <h3>详细结果</h3>
        {self.generate_test_results_html(report_data['results'])}
    </div>
    
    <div style="margin-top: 30px; text-align: center; color: #666;">
        <p>LLM Advanced Testing Suite - Web界面测试报告</p>
    </div>
</body>
</html>
        """
        
        html_file = Path("test_reports/web_interface_test_report.html")
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"📄 HTML报告已生成: {html_file}")
    
    def generate_test_results_html(self, results):
        """生成测试结果HTML"""
        html = ""
        for result in results:
            status_class = result["status"].lower()
            html += f"""
            <div class="test-result {status_class}">
                <h4>{result['test']}</h4>
                <p><strong>状态:</strong> {result['status']}</p>
                <p><strong>消息:</strong> {result['message']}</p>
                <p><strong>响应时间:</strong> {result.get('response_time', 0):.2f}s</p>
            </div>
            """
        return html
    
    def run(self):
        """运行测试"""
        success = self.test_web_interface()
        
        if success:
            print("\n🎉 所有测试通过！Web界面运行正常！")
            print(f"🌐 访问地址: {self.base_url}")
            return True
        else:
            print("\n❌ 部分测试失败！需要修复！")
            return False

def main():
    """主函数"""
    tester = ExpertWebTester()
    success = tester.run()
    
    if success:
        print("\n✅ Web界面测试完成 - 所有功能正常！")
        sys.exit(0)
    else:
        print("\n❌ Web界面测试失败 - 需要修复！")
        sys.exit(1)

if __name__ == "__main__":
    main()