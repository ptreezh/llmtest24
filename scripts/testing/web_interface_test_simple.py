#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
LLM Advanced Testing Suite - Web Interface Automated Tests (Simplified)
This script runs automated tests for the web interface using only requests.
"""

import os
import sys
import time
import json
import requests
import subprocess
from pathlib import Path
from urllib.parse import urljoin

# Add project root to Python path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

class SimpleWebInterfaceTester:
    """Simple web interface automated tester"""
    
    def __init__(self):
        self.base_url = "http://localhost:8501"
        self.test_results = []
        self.session = requests.Session()
        self.session.timeout = 10
    
    def start_web_interface(self):
        """Start the web interface"""
        print("Starting web interface...")
        
        # Check if web interface is already running
        try:
            response = self.session.get(f"{self.base_url}/")
            if response.status_code == 200:
                print("Web interface is already running")
                return True
        except requests.exceptions.ConnectionError:
            pass
        
        # Start the web interface
        try:
            # Use the visual_test_interface.py script
            script_path = project_root / "visual_test_interface.py"
            if not script_path.exists():
                print(f"Web interface script not found: {script_path}")
                return False
            
            # Start the web interface in background
            self.web_process = subprocess.Popen(
                [sys.executable, str(script_path)],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                cwd=project_root
            )
            
            # Wait for web interface to start
            print("Waiting for web interface to start...")
            for i in range(30):  # Wait up to 30 seconds
                try:
                    response = self.session.get(f"{self.base_url}/")
                    if response.status_code == 200:
                        print("Web interface started successfully")
                        return True
                except requests.exceptions.ConnectionError:
                    pass
                time.sleep(1)
            
            print("Web interface failed to start")
            return False
            
        except Exception as e:
            print(f"Error starting web interface: {e}")
            return False
    
    def test_home_page(self):
        """Test the home page"""
        print("Testing home page...")
        
        try:
            response = self.session.get(f"{self.base_url}/")
            if response.status_code == 200:
                content = response.text
                if "LLM Advanced Testing Suite" in content:
                    print("Home page loaded successfully")
                    self.test_results.append({
                        "test": "Home Page",
                        "status": "PASS",
                        "message": "Home page loaded successfully",
                        "response_time": response.elapsed.total_seconds()
                    })
                    return True
                else:
                    print("Home page content is incorrect")
                    self.test_results.append({
                        "test": "Home Page",
                        "status": "FAIL",
                        "message": "Home page content is incorrect",
                        "response_time": response.elapsed.total_seconds()
                    })
                    return False
            else:
                print(f"Home page returned status code: {response.status_code}")
                self.test_results.append({
                    "test": "Home Page",
                    "status": "FAIL",
                    "message": f"Status code: {response.status_code}",
                    "response_time": response.elapsed.total_seconds()
                })
                return False
        except Exception as e:
            print(f"Error accessing home page: {e}")
            self.test_results.append({
                "test": "Home Page",
                "status": "FAIL",
                "message": str(e)
            })
            return False
    
    def test_api_endpoints(self):
        """Test API endpoints"""
        print("Testing API endpoints...")
        
        endpoints = [
            ("/api/models", "GET", "Get available models"),
            ("/api/tests", "GET", "Get available tests"),
            ("/api/results", "GET", "Get test results"),
        ]
        
        for endpoint, method, description in endpoints:
            try:
                if method == "GET":
                    response = self.session.get(f"{self.base_url}{endpoint}")
                elif method == "POST":
                    response = self.session.post(f"{self.base_url}{endpoint}")
                
                response_time = response.elapsed.total_seconds()
                
                if response.status_code in [200, 201]:
                    print(f"{endpoint} - {method} - SUCCESS ({response_time:.2f}s)")
                    self.test_results.append({
                        "test": f"API {endpoint}",
                        "status": "PASS",
                        "message": f"{description} - {method} request successful",
                        "response_time": response_time
                    })
                else:
                    print(f"{endpoint} - {method} - Status: {response.status_code} ({response_time:.2f}s)")
                    self.test_results.append({
                        "test": f"API {endpoint}",
                        "status": "FAIL",
                        "message": f"Status code: {response.status_code}",
                        "response_time": response_time
                    })
            except Exception as e:
                print(f"{endpoint} - {method} - ERROR: {e}")
                self.test_results.append({
                    "test": f"API {endpoint}",
                    "status": "FAIL",
                    "message": str(e)
                })
    
    def test_run_test_endpoint(self):
        """Test the run_test endpoint"""
        print("Testing run_test endpoint...")
        
        # Test data
        test_data = {
            "pillar_name": "pillar_01_logic",
            "prompt": "If all roses are flowers and some flowers fade quickly, can we conclude that some roses fade quickly? Explain your reasoning step by step.",
            "model_name": "test_model"
        }
        
        try:
            response = self.session.post(
                f"{self.base_url}/api/run_test",
                json=test_data,
                headers={"Content-Type": "application/json"}
            )
            
            response_time = response.elapsed.total_seconds()
            
            if response.status_code == 200:
                result = response.json()
                if "success" in result and "score" in result:
                    print(f"/api/run_test - SUCCESS ({response_time:.2f}s)")
                    self.test_results.append({
                        "test": "API /api/run_test",
                        "status": "PASS",
                        "message": "Test execution successful",
                        "response_time": response_time,
                        "result": result
                    })
                    return True
                else:
                    print(f"/api/run_test - Invalid response format ({response_time:.2f}s)")
                    self.test_results.append({
                        "test": "API /api/run_test",
                        "status": "FAIL",
                        "message": "Invalid response format",
                        "response_time": response_time
                    })
                    return False
            else:
                print(f"/api/run_test - Status: {response.status_code} ({response_time:.2f}s)")
                self.test_results.append({
                    "test": "API /api/run_test",
                    "status": "FAIL",
                    "message": f"Status code: {response.status_code}",
                    "response_time": response_time
                })
                return False
                
        except Exception as e:
            print(f"/api/run_test - ERROR: {e}")
            self.test_results.append({
                "test": "API /api/run_test",
                "status": "FAIL",
                "message": str(e)
            })
            return False
    
    def test_performance(self):
        """Test page load performance"""
        print("Testing performance...")
        
        try:
            # Test page load times
            pages = ["/", "/api/models", "/api/tests", "/api/results"]
            
            for page in pages:
                start_time = time.time()
                try:
                    response = self.session.get(f"{self.base_url}{page}")
                    end_time = time.time()
                    load_time = end_time - start_time
                    
                    if load_time < 3.0:  # Less than 3 seconds
                        print(f"Performance - {page} - {load_time:.2f}s - GOOD")
                        self.test_results.append({
                            "test": f"Performance - {page}",
                            "status": "PASS",
                            "message": f"Load time: {load_time:.2f}s",
                            "response_time": load_time
                        })
                    else:
                        print(f"Performance - {page} - {load_time:.2f}s - SLOW")
                        self.test_results.append({
                            "test": f"Performance - {page}",
                            "status": "WARNING",
                            "message": f"Load time: {load_time:.2f}s (slow)",
                            "response_time": load_time
                        })
                        
                except Exception as e:
                    print(f"Performance - {page} - ERROR: {e}")
                    self.test_results.append({
                        "test": f"Performance - {page}",
                        "status": "FAIL",
                        "message": str(e)
                    })
            
        except Exception as e:
            print(f"Error testing performance: {e}")
            self.test_results.append({
                "test": "Performance",
                "status": "FAIL",
                "message": str(e)
            })
    
    def test_error_handling(self):
        """Test error handling"""
        print("Testing error handling...")
        
        # Test invalid endpoints
        invalid_endpoints = [
            ("/api/invalid", "GET"),
            ("/api/invalid", "POST"),
            ("/", "POST"),  # Invalid method for home
        ]
        
        for endpoint, method in invalid_endpoints:
            try:
                if method == "GET":
                    response = self.session.get(f"{self.base_url}{endpoint}")
                elif method == "POST":
                    response = self.session.post(f"{self.base_url}{endpoint}")
                
                # Should return 404 or 405 for invalid endpoints
                if response.status_code in [404, 405]:
                    print(f"Error handling - {endpoint} - {method} - Status: {response.status_code}")
                    self.test_results.append({
                        "test": f"Error Handling - {endpoint}",
                        "status": "PASS",
                        "message": f"Properly handled invalid endpoint",
                        "response_time": response.elapsed.total_seconds()
                    })
                else:
                    print(f"Error handling - {endpoint} - {method} - Status: {response.status_code}")
                    self.test_results.append({
                        "test": f"Error Handling - {endpoint}",
                        "status": "WARNING",
                        "message": f"Unexpected status code: {response.status_code}",
                        "response_time": response.elapsed.total_seconds()
                    })
                    
            except Exception as e:
                print(f"Error handling - {endpoint} - {method} - ERROR: {e}")
                self.test_results.append({
                    "test": f"Error Handling - {endpoint}",
                    "status": "FAIL",
                    "message": str(e)
                })
    
    def run_all_tests(self):
        """Run all tests"""
        print("Starting web interface automated tests...")
        print("=" * 60)
        
        # Start web interface
        if not self.start_web_interface():
            print("Failed to start web interface")
            return False
        
        # Give web interface more time to fully load
        print("Waiting for web interface to fully load...")
        time.sleep(5)
        
        # Run tests
        self.test_home_page()
        self.test_api_endpoints()
        self.test_run_test_endpoint()
        self.test_performance()
        self.test_error_handling()
        
        # Generate report
        self.generate_report()
        
        return True
    
    def generate_report(self):
        """Generate test report"""
        print("\nTest Report")
        print("=" * 60)
        
        # Count results
        total_tests = len(self.test_results)
        passed_tests = len([r for r in self.test_results if r["status"] == "PASS"])
        failed_tests = len([r for r in self.test_results if r["status"] == "FAIL"])
        warning_tests = len([r for r in self.test_results if r["status"] == "WARNING"])
        
        print(f"Total Tests: {total_tests}")
        print(f"Passed: {passed_tests}")
        print(f"Failed: {failed_tests}")
        print(f"Warnings: {warning_tests}")
        
        if total_tests > 0:
            success_rate = (passed_tests/total_tests)*100
            print(f"Success Rate: {success_rate:.1f}%")
        else:
            success_rate = 0
            print("Success Rate: 0%")
        
        # Calculate average response time
        response_times = [r.get("response_time", 0) for r in self.test_results if "response_time" in r]
        if response_times:
            avg_response_time = sum(response_times) / len(response_times)
            print(f"Average Response Time: {avg_response_time:.2f}s")
        
        # Print detailed results
        print("\nDetailed Results:")
        for result in self.test_results:
            status_icon = "PASS" if result["status"] == "PASS" else "FAIL" if result["status"] == "FAIL" else "WARN"
            print(f"{status_icon} {result['test']}: {result['message']}")
        
        # Save report to file
        report_file = project_root / "test_reports" / "web_interface_test_report.json"
        report_file.parent.mkdir(parents=True, exist_ok=True)
        
        report_data = {
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "total_tests": total_tests,
            "passed_tests": passed_tests,
            "failed_tests": failed_tests,
            "warning_tests": warning_tests,
            "success_rate": success_rate,
            "average_response_time": avg_response_time if response_times else 0,
            "results": self.test_results
        }
        
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(report_data, f, indent=2, ensure_ascii=False)
        
        # Save summary report
        summary_file = project_root / "test_reports" / "web_interface_test_summary.txt"
        with open(summary_file, 'w', encoding='utf-8') as f:
            f.write("LLM Advanced Testing Suite - Web Interface Test Report\n")
            f.write("=" * 60 + "\n")
            f.write(f"Timestamp: {report_data['timestamp']}\n")
            f.write(f"Total Tests: {total_tests}\n")
            f.write(f"Passed: {passed_tests}\n")
            f.write(f"Failed: {failed_tests}\n")
            f.write(f"Warnings: {warning_tests}\n")
            f.write(f"Success Rate: {success_rate:.1f}%\n")
            f.write(f"Average Response Time: {avg_response_time:.2f}s\n")
            f.write("\nDetailed Results:\n")
            f.write("-" * 40 + "\n")
            for result in self.test_results:
                status_icon = "PASS" if result["status"] == "PASS" else "FAIL" if result["status"] == "FAIL" else "WARN"
                f.write(f"{status_icon} {result['test']}: {result['message']}\n")
        
        print(f"\nDetailed report saved to: {report_file}")
        print(f"Summary report saved to: {summary_file}")
        
        # Close web interface
        self.cleanup()
        
        return passed_tests == total_tests
    
    def cleanup(self):
        """Clean up resources"""
        print("\nCleaning up...")
        
        if hasattr(self, 'web_process'):
            try:
                self.web_process.terminate()
                self.web_process.wait(timeout=5)
                print("Web interface stopped")
            except:
                print("Could not stop web interface gracefully")
        
        self.session.close()
        print("Session closed")

def main():
    """Main test function"""
    print("LLM Advanced Testing Suite - Web Interface Automated Tests")
    print("=" * 70)
    print()
    
    tester = SimpleWebInterfaceTester()
    success = tester.run_all_tests()
    
    if success:
        print("\nAll tests passed!")
        sys.exit(0)
    else:
        print("\nSome tests failed!")
        sys.exit(1)

if __name__ == "__main__":
    main()