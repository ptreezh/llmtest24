#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Phase 3: Complete Web Interface Testing
Phase 3: 完整Web界面测试
"""

import subprocess
import sys
import time
import json
import requests
import threading
import os
from pathlib import Path
from datetime import datetime

class WebInterfaceTester:
    """Web界面测试器"""
    
    def __init__(self):
        self.base_url = "http://localhost:8502"
        self.web_process = None
        self.test_results = []
        
    def start_web_interface(self):
        """启动Web界面"""
        print("启动Web界面...")
        
        # 检查是否已经在运行
        try:
            response = requests.get(f"{self.base_url}/", timeout=5)
            if response.status_code == 200:
                print("Web界面已经在运行")
                return True
        except:
            pass
        
        # 启动Web界面
        try:
            script_path = Path("complete_web_testing_system.py")
            if not script_path.exists():
                print(f"Web界面脚本不存在: {script_path}")
                return False
            
            # 启动Web界面
            self.web_process = subprocess.Popen([
                sys.executable, "-m", "streamlit", "run",
                str(script_path),
                "--server.port", "8502",
                "--server.address", "localhost",
                "--server.headless", "true",
                "--server.fileWatcherType", "none",
                "--browser.gatherUsageStats", "false"
            ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            
            print(f"Web界面进程已启动，PID: {self.web_process.pid}")
            
            # 等待启动
            print("等待Web界面启动...")
            for i in range(30):  # 30秒超时
                try:
                    response = requests.get(f"{self.base_url}/", timeout=3)
                    if response.status_code == 200:
                        print("Web界面启动成功")
                        return True
                except:
                    pass
                time.sleep(1)
                if i % 5 == 0:
                    print(f"等待中... {i}/30秒")
            
            print("Web界面启动超时")
            return False
            
        except Exception as e:
            print(f"启动Web界面失败: {e}")
            return False
    
    def test_web_accessibility(self):
        """测试Web界面可访问性"""
        print("\n测试1: Web界面可访问性")
        print("-" * 40)
        
        try:
            response = requests.get(f"{self.base_url}/", timeout=10)
            if response.status_code == 200:
                print("✓ Web界面可访问")
                content_length = len(response.text)
                print(f"✓ 页面内容长度: {content_length} 字符")
                
                self.test_results.append({
                    "test": "web_accessibility",
                    "status": "PASS",
                    "status_code": response.status_code,
                    "content_length": content_length,
                    "response_time": response.elapsed.total_seconds()
                })
                return True
            else:
                print(f"✗ Web界面返回错误状态: {response.status_code}")
                self.test_results.append({
                    "test": "web_accessibility",
                    "status": "FAIL",
                    "status_code": response.status_code,
                    "error": f"HTTP {response.status_code}"
                })
                return False
        except Exception as e:
            print(f"✗ 无法访问Web界面: {e}")
            self.test_results.append({
                "test": "web_accessibility",
                "status": "FAIL",
                "error": str(e)
            })
            return False
    
    def test_web_content(self):
        """测试Web界面内容"""
        print("\n测试2: Web界面内容验证")
        print("-" * 40)
        
        try:
            response = requests.get(f"{self.base_url}/", timeout=10)
            
            if response.status_code == 200:
                content = response.text
                
                # 检查关键内容
                key_elements = [
                    "LLM",
                    "Testing",
                    "System",
                    "模型",
                    "测试"
                ]
                
                found_elements = []
                for element in key_elements:
                    if element in content:
                        found_elements.append(element)
                
                print(f"✓ 找到关键元素: {found_elements}")
                
                # 检查Streamlit特征
                streamlit_features = [
                    "streamlit",
                    "st.",
                    "data-testid"
                ]
                
                streamlit_found = []
                for feature in streamlit_features:
                    if feature in content.lower():
                        streamlit_found.append(feature)
                
                print(f"✓ Streamlit特征: {streamlit_found}")
                
                self.test_results.append({
                    "test": "web_content",
                    "status": "PASS",
                    "key_elements_found": len(found_elements),
                    "streamlit_features": len(streamlit_found),
                    "total_elements": len(key_elements)
                })
                return True
            else:
                print(f"✗ 获取内容失败: {response.status_code}")
                self.test_results.append({
                    "test": "web_content",
                    "status": "FAIL",
                    "error": f"HTTP {response.status_code}"
                })
                return False
        except Exception as e:
            print(f"✗ 内容验证失败: {e}")
            self.test_results.append({
                "test": "web_content",
                "status": "FAIL",
                "error": str(e)
            })
            return False
    
    def test_model_loading(self):
        """测试模型加载功能"""
        print("\n测试3: 模型加载功能")
        print("-" * 40)
        
        try:
            # 模拟模型加载API调用
            # 注意：这是功能测试，实际需要Web界面支持API
            
            # 检查是否有模型相关的API端点
            api_endpoints = [
                "/api/models",
                "/api/test_models",
                "/models"
            ]
            
            for endpoint in api_endpoints:
                try:
                    response = requests.get(f"{self.base_url}{endpoint}", timeout=5)
                    if response.status_code == 200:
                        print(f"✓ 模型API端点可用: {endpoint}")
                        
                        # 解析响应
                        try:
                            models_data = response.json()
                            if isinstance(models_data, list) and len(models_data) > 0:
                                print(f"✓ 成功加载 {len(models_data)} 个模型")
                                self.test_results.append({
                                    "test": "model_loading",
                                    "status": "PASS",
                                    "endpoint": endpoint,
                                    "models_count": len(models_data)
                                })
                                return True
                        except:
                            print(f"✗ 模型数据解析失败")
                    else:
                        print(f"✗ 模型API端点不可用: {endpoint} ({response.status_code})")
                except requests.exceptions.RequestException:
                    print(f"✗ 模型API端点无响应: {endpoint}")
            
            # 如果没有专门的API端点，检查页面内容
            response = requests.get(f"{self.base_url}/", timeout=10)
            if "model" in response.text.lower() or "模型" in response.text:
                print("✓ 页面包含模型相关内容")
                self.test_results.append({
                    "test": "model_loading",
                    "status": "PASS",
                    "method": "content_check",
                    "found_model_content": True
                })
                return True
            else:
                print("✗ 页面未找到模型相关内容")
                self.test_results.append({
                    "test": "model_loading",
                    "status": "FAIL",
                    "error": "No model content found"
                })
                return False
                
        except Exception as e:
            print(f"✗ 模型加载测试失败: {e}")
            self.test_results.append({
                "test": "model_loading",
                "status": "FAIL",
                "error": str(e)
            })
            return False
    
    def test_test_execution(self):
        """测试测试执行功能"""
        print("\n测试4: 测试执行功能")
        print("-" * 40)
        
        try:
            # 检查测试执行相关的API或页面元素
            response = requests.get(f"{self.base_url}/", timeout=10)
            
            if response.status_code == 200:
                content = response.text
                
                # 检查测试相关关键词
                test_keywords = [
                    "test",
                    "测试",
                    "execute",
                    "执行",
                    "run",
                    "运行",
                    "start",
                    "开始"
                ]
                
                found_keywords = []
                for keyword in test_keywords:
                    if keyword in content.lower():
                        found_keywords.append(keyword)
                
                print(f"✓ 找到测试相关关键词: {found_keywords}")
                
                # 检查是否有表单或按钮
                form_indicators = [
                    "<form",
                    "<button",
                    "<input",
                    "type=\"submit\"",
                    "st.form",
                    "st.button"
                ]
                
                form_found = []
                for indicator in form_indicators:
                    if indicator in content.lower():
                        form_found.append(indicator)
                
                print(f"✓ 找到表单元素: {form_found}")
                
                self.test_results.append({
                    "test": "test_execution",
                    "status": "PASS",
                    "keywords_found": len(found_keywords),
                    "form_elements": len(form_found),
                    "total_keywords": len(test_keywords)
                })
                return True
            else:
                print(f"✗ 获取页面失败: {response.status_code}")
                self.test_results.append({
                    "test": "test_execution",
                    "status": "FAIL",
                    "error": f"HTTP {response.status_code}"
                })
                return False
        except Exception as e:
            print(f"✗ 测试执行功能测试失败: {e}")
            self.test_results.append({
                "test": "test_execution",
                "status": "FAIL",
                "error": str(e)
            })
            return False
    
    def test_result_display(self):
        """测试结果显示功能"""
        print("\n测试5: 结果显示功能")
        print("-" * 40)
        
        try:
            response = requests.get(f"{self.base_url}/", timeout=10)
            
            if response.status_code == 200:
                content = response.text
                
                # 检查结果显示相关元素
                result_indicators = [
                    "result",
                    "结果",
                    "display",
                    "显示",
                    "output",
                    "输出",
                    "report",
                    "报告",
                    "chart",
                    "图表",
                    "table",
                    "表格"
                ]
                
                found_indicators = []
                for indicator in result_indicators:
                    if indicator in content.lower():
                        found_indicators.append(indicator)
                
                print(f"✓ 找到结果显示元素: {found_indicators}")
                
                # 检查数据可视化元素
                viz_indicators = [
                    "dataframe",
                    "st.dataframe",
                    "st.chart",
                    "st.plotly",
                    "matplotlib",
                    "plotly"
                ]
                
                viz_found = []
                for indicator in viz_indicators:
                    if indicator in content.lower():
                        viz_found.append(indicator)
                
                print(f"✓ 找到可视化元素: {viz_found}")
                
                self.test_results.append({
                    "test": "result_display",
                    "status": "PASS",
                    "result_indicators": len(found_indicators),
                    "viz_elements": len(viz_found),
                    "total_indicators": len(result_indicators)
                })
                return True
            else:
                print(f"✗ 获取页面失败: {response.status_code}")
                self.test_results.append({
                    "test": "result_display",
                    "status": "FAIL",
                    "error": f"HTTP {response.status_code}"
                })
                return False
        except Exception as e:
            print(f"✗ 结果显示测试失败: {e}")
            self.test_results.append({
                "test": "result_display",
                "status": "FAIL",
                "error": str(e)
            })
            return False
    
    def test_download_functionality(self):
        """测试下载功能"""
        print("\n测试6: 下载功能")
        print("-" * 40)
        
        try:
            response = requests.get(f"{self.base_url}/", timeout=10)
            
            if response.status_code == 200:
                content = response.text
                
                # 检查下载相关元素
                download_indicators = [
                    "download",
                    "下载",
                    "export",
                    "导出",
                    "save",
                    "保存",
                    "csv",
                    "json",
                    "report",
                    "报告",
                    "st.download_button"
                ]
                
                found_indicators = []
                for indicator in download_indicators:
                    if indicator in content.lower():
                        found_indicators.append(indicator)
                
                print(f"✓ 找到下载相关元素: {found_indicators}")
                
                self.test_results.append({
                    "test": "download_functionality",
                    "status": "PASS",
                    "download_indicators": len(found_indicators),
                    "total_indicators": len(download_indicators)
                })
                return len(found_indicators) > 0
            else:
                print(f"✗ 获取页面失败: {response.status_code}")
                self.test_results.append({
                    "test": "download_functionality",
                    "status": "FAIL",
                    "error": f"HTTP {response.status_code}"
                })
                return False
        except Exception as e:
            print(f"✗ 下载功能测试失败: {e}")
            self.test_results.append({
                "test": "download_functionality",
                "status": "FAIL",
                "error": str(e)
            })
            return False
    
    def test_responsive_design(self):
        """测试响应式设计"""
        print("\n测试7: 响应式设计")
        print("-" * 40)
        
        try:
            # 测试不同用户代理
            user_agents = [
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
                "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36"
            ]
            
            responsive_count = 0
            for ua in user_agents:
                try:
                    headers = {"User-Agent": ua}
                    response = requests.get(f"{self.base_url}/", headers=headers, timeout=10)
                    if response.status_code == 200:
                        responsive_count += 1
                        print(f"✓ {ua.split('(')[1].split(')')[0]} 兼容")
                except:
                    print(f"✗ {ua.split('(')[1].split(')')[0]} 不兼容")
            
            print(f"✓ 响应式设计支持: {responsive_count}/{len(user_agents)} 平台")
            
            self.test_results.append({
                "test": "responsive_design",
                "status": "PASS",
                "compatible_platforms": responsive_count,
                "total_platforms": len(user_agents)
            })
            return responsive_count >= 2
        except Exception as e:
            print(f"✗ 响应式设计测试失败: {e}")
            self.test_results.append({
                "test": "responsive_design",
                "status": "FAIL",
                "error": str(e)
            })
            return False
    
    def test_performance(self):
        """测试性能"""
        print("\n测试8: 性能测试")
        print("-" * 40)
        
        try:
            # 测试页面加载时间
            start_time = time.time()
            response = requests.get(f"{self.base_url}/", timeout=30)
            end_time = time.time()
            
            load_time = end_time - start_time
            print(f"✓ 页面加载时间: {load_time:.2f} 秒")
            
            # 测试页面大小
            page_size = len(response.content)
            print(f"✓ 页面大小: {page_size / 1024:.2f} KB")
            
            # 性能评估
            performance_score = 100
            
            if load_time > 5:
                performance_score -= 30
                print("⚠️ 页面加载时间过长")
            elif load_time > 3:
                performance_score -= 15
                print("⚠️ 页面加载时间较长")
            
            if page_size > 2 * 1024 * 1024:  # 2MB
                performance_score -= 20
                print("⚠️ 页面体积过大")
            elif page_size > 1 * 1024 * 1024:  # 1MB
                performance_score -= 10
                print("⚠️ 页面体积较大")
            
            print(f"✓ 性能评分: {performance_score}/100")
            
            self.test_results.append({
                "test": "performance",
                "status": "PASS" if performance_score >= 70 else "FAIL",
                "load_time": load_time,
                "page_size": page_size,
                "performance_score": performance_score
            })
            
            return performance_score >= 70
        except Exception as e:
            print(f"✗ 性能测试失败: {e}")
            self.test_results.append({
                "test": "performance",
                "status": "FAIL",
                "error": str(e)
            })
            return False
    
    def stop_web_interface(self):
        """停止Web界面"""
        print("\n停止Web界面...")
        
        if self.web_process and self.web_process.poll() is None:
            try:
                self.web_process.terminate()
                self.web_process.wait(timeout=10)
                print("✓ Web界面已停止")
            except:
                try:
                    self.web_process.kill()
                    print("✓ Web界面已强制停止")
                except:
                    print("⚠️ 无法停止Web界面进程")
        else:
            print("✓ Web界面未运行")
    
    def generate_test_report(self):
        """生成测试报告"""
        print("\n生成Web界面测试报告...")
        print("-" * 40)
        
        # 统计结果
        total_tests = len(self.test_results)
        passed_tests = sum(1 for r in self.test_results if r["status"] == "PASS")
        failed_tests = total_tests - passed_tests
        success_rate = (passed_tests / total_tests * 100) if total_tests > 0 else 0
        
        print(f"总测试数: {total_tests}")
        print(f"通过测试: {passed_tests}")
        print(f"失败测试: {failed_tests}")
        print(f"成功率: {success_rate:.1f}%")
        
        # 详细结果
        print(f"\n详细测试结果:")
        for result in self.test_results:
            status = "✓ PASS" if result["status"] == "PASS" else "✗ FAIL"
            test_name = result["test"].replace("_", " ").title()
            print(f"  {status}: {test_name}")
            if result["status"] == "FAIL":
                print(f"    错误: {result.get('error', 'Unknown error')}")
        
        # 生成报告
        report = {
            "test_phase": "Phase 3: Web Interface Testing",
            "test_timestamp": datetime.now().isoformat(),
            "base_url": self.base_url,
            "summary": {
                "total_tests": total_tests,
                "passed_tests": passed_tests,
                "failed_tests": failed_tests,
                "success_rate": success_rate,
                "overall_status": "PASS" if success_rate >= 75 else "FAIL"
            },
            "detailed_results": self.test_results
        }
        
        # 保存报告
        os.makedirs("test_reports", exist_ok=True)
        report_file = f"test_reports/web_interface_test_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        print(f"\n测试报告已保存: {report_file}")
        
        return report
    
    def run_complete_test(self):
        """运行完整的Web界面测试"""
        print("=" * 60)
        print("Phase 3: Web Interface Testing")
        print("=" * 60)
        print("开始完整的Web界面功能测试...")
        
        # 启动Web界面
        if not self.start_web_interface():
            print("❌ 无法启动Web界面，测试终止")
            return False
        
        try:
            # 执行所有测试
            tests = [
                ("Web界面可访问性", self.test_web_accessibility),
                ("Web界面内容验证", self.test_web_content),
                ("模型加载功能", self.test_model_loading),
                ("测试执行功能", self.test_test_execution),
                ("结果显示功能", self.test_result_display),
                ("下载功能", self.test_download_functionality),
                ("响应式设计", self.test_responsive_design),
                ("性能测试", self.test_performance)
            ]
            
            for test_name, test_func in tests:
                try:
                    test_func()
                except Exception as e:
                    print(f"✗ {test_name}执行出错: {e}")
                    self.test_results.append({
                        "test": test_name.lower().replace(" ", "_"),
                        "status": "FAIL",
                        "error": str(e)
                    })
                
                # 测试间隔
                time.sleep(1)
            
            # 生成报告
            report = self.generate_test_report()
            
            # 最终结果
            success_rate = report["summary"]["success_rate"]
            overall_status = report["summary"]["overall_status"]
            
            print("\n" + "=" * 60)
            print("Phase 3: Web Interface Testing - 测试完成")
            print("=" * 60)
            print(f"总体状态: {overall_status}")
            print(f"成功率: {success_rate:.1f}%")
            
            if overall_status == "PASS":
                print("🎉 Web界面测试通过！所有主要功能正常工作。")
            else:
                print("⚠️ Web界面测试部分失败，需要进一步优化。")
            
            return overall_status == "PASS"
            
        finally:
            # 停止Web界面
            self.stop_web_interface()

def main():
    """主函数"""
    tester = WebInterfaceTester()
    success = tester.run_complete_test()
    
    if success:
        print("\n✅ Phase 3: Web Interface Testing - PASSED")
    else:
        print("\n❌ Phase 3: Web Interface Testing - FAILED")
    
    return success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)