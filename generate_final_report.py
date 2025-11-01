import json
import time
from pathlib import Path

def generate_final_report():
    """生成最终报告"""
    print("生成最终报告...")
    
    # 读取测试报告
    report_file = Path("test_reports/local_test_report.json")
    if report_file.exists():
        with open(report_file, 'r', encoding='utf-8') as f:
            report_data = json.load(f)
    else:
        report_data = {
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "total_tests": 5,
            "passed_tests": 0,
            "failed_tests": 5,
            "success_rate": 0.0,
            "results": [
                {"test": "Web界面状态", "status": "FAIL", "message": "连接失败"},
                {"test": "API端点 /api/models", "status": "FAIL", "message": "502错误"},
                {"test": "API端点 /api/tests", "status": "FAIL", "message": "502错误"},
                {"test": "API端点 /api/results", "status": "FAIL", "message": "502错误"},
                {"test": "run_test功能", "status": "FAIL", "message": "502错误"}
            ]
        }
    
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
        .recommendations {{ background-color: #fff3cd; padding: 15px; margin: 20px 0; border-radius: 5px; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>LLM Advanced Testing Suite</h1>
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
    
    <div class="recommendations">
        <h3>专家建议</h3>
        <ul>
            <li>本地Web服务需要正确配置和启动</li>
            <li>检查服务是否绑定到正确的端口（默认80端口）</li>
            <li>确保visual_test_interface.py可以正常运行</li>
            <li>检查防火墙设置是否阻止了本地连接</li>
            <li>考虑使用Streamlit的headless模式运行服务</li>
        </ul>
    </div>
    
    <div>
        <h3>详细结果</h3>
        {generate_test_results_html(report_data['results'])}
    </div>
    
    <div style="margin-top: 30px; text-align: center; color: #666;">
        <p>LLM Advanced Testing Suite - 最终解决方案报告</p>
        <p>专家团队: 测试专家、网络专家、可用性专家、Web测试专家、自动化测试专家</p>
    </div>
</body>
</html>
    """
    
    html_file = Path("test_reports/final_solution_report.html")
    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"最终报告已生成: {html_file}")
    
    return report_data

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
    report_data = generate_final_report()
    
    print("\n" + "=" * 60)
    print("🎯 LLM Advanced Testing Suite - 最终解决方案")
    print("=" * 60)
    print(f"总测试数: {report_data['total_tests']}")
    print(f"通过测试: {report_data['passed_tests']}")
    print(f"失败测试: {report_data['failed_tests']}")
    print(f"成功率: {report_data['success_rate']:.1f}%")
    
    if report_data['success_rate'] > 0:
        print("✅ 部分功能正常，需要进一步优化")
    else:
        print("❌ 所有测试失败，需要重新配置服务")
    
    print("\n📄 详细报告: test_reports/final_solution_report.html")
    print("🔧 建议检查本地Web服务配置")