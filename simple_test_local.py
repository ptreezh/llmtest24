import sys
import time
import json
import requests
from pathlib import Path

def test_web_interface():
    """测试本地Web界面"""
    print("LLM Advanced Testing Suite - 本地Web界面测试")
    print("=" * 50)
    
    # 假设本地服务运行在默认端口80上
    # 如果您的服务运行在其他端口，请相应修改
    base_url = "http://localhost"
    test_results = []
    
    # 测试1: 检查Web界面是否运行
    print("\n测试1: 检查Web界面状态")
    try:
        response = requests.get(f"{base_url}/", timeout=5)
        if response.status_code == 200:
            print("PASS: Web界面正在运行")
            test_results.append({"test": "Web界面状态", "status": "PASS", "message": "Web界面正在运行"})
        else:
            print(f"FAIL: Web界面返回错误状态: {response.status_code}")
            test_results.append({"test": "Web界面状态", "status": "FAIL", "message": f"状态码: {response.status_code}"})
    except Exception as e:
        print(f"FAIL: Web界面未运行: {e}")
        test_results.append({"test": "Web界面状态", "status": "FAIL", "message": f"连接失败: {e}"})
    
    # 测试2: 检查API端点
    print("\n测试2: 检查API端点")
    api_endpoints = ["/api/models", "/api/tests", "/api/results"]
    
    for endpoint in api_endpoints:
        try:
            response = requests.get(f"{base_url}{endpoint}", timeout=5)
            if response.status_code == 200:
                print(f"PASS: {endpoint} 正常")
                test_results.append({"test": f"API端点 {endpoint}", "status": "PASS", "message": "正常"})
            else:
                print(f"FAIL: {endpoint} 返回错误: {response.status_code}")
                test_results.append({"test": f"API端点 {endpoint}", "status": "FAIL", "message": f"状态码: {response.status_code}"})
        except Exception as e:
            print(f"FAIL: {endpoint} 连接失败: {e}")
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
            timeout=10
        )
        
        if response.status_code == 200:
            print("PASS: run_test功能正常")
            test_results.append({"test": "run_test功能", "status": "PASS", "message": "功能正常"})
        else:
            print(f"FAIL: run_test功能错误: {response.status_code}")
            test_results.append({"test": "run_test功能", "status": "FAIL", "message": f"状态码: {response.status_code}"})
    except Exception as e:
        print(f"FAIL: run_test功能失败: {e}")
        test_results.append({"test": "run_test功能", "status": "FAIL", "message": f"连接失败: {e}"})
    
    # 生成报告
    print("\n生成测试报告")
    
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
    report_file = Path("test_reports/local_test_report.json")
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
    
    print(f"报告已保存: {report_file}")
    
    # 输出最终结果
    print("\n" + "=" * 50)
    if passed_tests == total_tests:
        print("SUCCESS: 所有测试通过！本地Web界面运行正常！")
        print(f"访问地址: {base_url}")
        print("最终解决方案成功！")
    else:
        print("FAIL: 部分测试失败！需要修复！")
        print("请检查本地Web界面是否正常运行")
    
    return passed_tests == total_tests

if __name__ == "__main__":
    success = test_web_interface()
    sys.exit(0 if success else 1)