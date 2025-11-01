#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
LLM Advanced Testing Suite - Complete Web Interface Test
This script starts the web interface and runs comprehensive tests.
"""

import os
import sys
import time
import json
import requests
import subprocess
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

class WebInterfaceTester:
    def __init__(self):
        self.base_url = "http://localhost:8501"
        self.web_process = None
        self.test_results = []
    
    def start_web_interface(self):
        """Start the web interface"""
        print("Starting web interface...")
        
        # Check if web interface is already running
        try:
            response = requests.get(f"{self.base_url}/", timeout=5)
            if response.status_code == 200:
                print("Web interface is already running")
                return True
        except:
            pass
        
        # Start the web interface
        try:
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
                    response = requests.get(f"{self.base_url}/", timeout=5)
                    if response.status_code == 200:
                        print("Web interface started successfully")
                        return True
                except:
                    pass
                time.sleep(1)
            
            print("Web interface failed to start")
            return False
            
        except Exception as e:
            print(f"Error starting web interface: {e}")
            return False
    
    def test_basic_functionality(self):
        """Test basic web interface functionality"""
        print("\nTesting basic functionality...")
        
        # Test 1: Home page
        print("Test 1: Home page")
        try:
            response = requests.get(f"{self.base_url}/", timeout=10)
            if response.status_code == 200:
                print("PASS: Home page accessible")
                self.test_results.append({"test": "Home Page", "status": "PASS", "response_time": response.elapsed.total_seconds()})
            else:
                print(f"FAIL: Home page status {response.status_code}")
                self.test_results.append({"test": "Home Page", "status": "FAIL", "response_time": response.elapsed.total_seconds()})
        except Exception as e:
            print(f"FAIL: Home page error - {e}")
            self.test_results.append({"test": "Home Page", "status": "FAIL", "message": str(e)})
        
        # Test 2: API models
        print("Test 2: API models")
        try:
            response = requests.get(f"{self.base_url}/api/models", timeout=10)
            if response.status_code == 200:
                print("PASS: API models accessible")
                self.test_results.append({"test": "API Models", "status": "PASS", "response_time": response.elapsed.total_seconds()})
            else:
                print(f"FAIL: API models status {response.status_code}")
                self.test_results.append({"test": "API Models", "status": "FAIL", "response_time": response.elapsed.total_seconds()})
        except Exception as e:
            print(f"FAIL: API models error - {e}")
            self.test_results.append({"test": "API Models", "status": "FAIL", "message": str(e)})
        
        # Test 3: API tests
        print("Test 3: API tests")
        try:
            response = requests.get(f"{self.base_url}/api/tests", timeout=10)
            if response.status_code == 200:
                print("PASS: API tests accessible")
                self.test_results.append({"test": "API Tests", "status": "PASS", "response_time": response.elapsed.total_seconds()})
            else:
                print(f"FAIL: API tests status {response.status_code}")
                self.test_results.append({"test": "API Tests", "status": "FAIL", "response_time": response.elapsed.total_seconds()})
        except Exception as e:
            print(f"FAIL: API tests error - {e}")
            self.test_results.append({"test": "API Tests", "status": "FAIL", "message": str(e)})
        
        # Test 4: API results
        print("Test 4: API results")
        try:
            response = requests.get(f"{self.base_url}/api/results", timeout=10)
            if response.status_code == 200:
                print("PASS: API results accessible")
                self.test_results.append({"test": "API Results", "status": "PASS", "response_time": response.elapsed.total_seconds()})
            else:
                print(f"FAIL: API results status {response.status_code}")
                self.test_results.append({"test": "API Results", "status": "FAIL", "response_time": response.elapsed.total_seconds()})
        except Exception as e:
            print(f"FAIL: API results error - {e}")
            self.test_results.append({"test": "API Results", "status": "FAIL", "message": str(e)})
    
    def test_run_test_endpoint(self):
        """Test the run_test endpoint"""
        print("\nTesting run_test endpoint...")
        
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
                    print("PASS: run_test endpoint works correctly")
                    self.test_results.append({"test": "run_test endpoint", "status": "PASS", "response_time": response.elapsed.total_seconds()})
                else:
                    print("FAIL: run_test endpoint returned invalid response")
                    self.test_results.append({"test": "run_test endpoint", "status": "FAIL", "response_time": response.elapsed.total_seconds()})
            else:
                print(f"FAIL: run_test endpoint returned status {response.status_code}")
                self.test_results.append({"test": "run_test endpoint", "status": "FAIL", "response_time": response.elapsed.total_seconds()})
        except Exception as e:
            print(f"FAIL: run_test endpoint error - {e}")
            self.test_results.append({"test": "run_test endpoint", "status": "FAIL", "message": str(e)})
    
    def test_performance(self):
        """Test performance"""
        print("\nTesting performance...")
        
        pages = ["/", "/api/models", "/api/tests", "/api/results"]
        
        for page in pages:
            start_time = time.time()
            try:
                response = requests.get(f"{self.base_url}{page}", timeout=10)
                end_time = time.time()
                load_time = end_time - start_time
                
                if load_time < 3.0:
                    print(f"PASS: {page} - {load_time:.2f}s")
                    self.test_results.append({"test": f"Performance - {page}", "status": "PASS", "response_time": load_time})
                else:
                    print(f"WARN: {page} - {load_time:.2f}s (slow)")
                    self.test_results.append({"test": f"Performance - {page}", "status": "WARN", "response_time": load_time})
            except Exception as e:
                print(f"FAIL: {page} - {e}")
                self.test_results.append({"test": f"Performance - {page}", "status": "FAIL", "message": str(e)})
    
    def generate_report(self):
        """Generate test report"""
        print("\nTest Report")
        print("=" * 60)
        
        # Count results
        total_tests = len(self.test_results)
        passed_tests = len([r for r in self.test_results if r["status"] == "PASS"])
        failed_tests = len([r for r in self.test_results if r["status"] == "FAIL"])
        warning_tests = len([r for r in self.test_results if r["status"] == "WARN"])
        
        print(f"Total Tests: {total_tests}")
        print(f"Passed: {passed_tests}")
        print(f"Failed: {failed_tests}")
        print(f"Warnings: {warning_tests}")
        
        if total_tests > 0:
            success_rate = (passed_tests/total_tests)*100
            print(f"Success Rate: {success_rate:.1f}%")
        
        # Calculate average response time
        response_times = [r.get("response_time", 0) for r in self.test_results if "response_time" in r]
        if response_times:
            avg_response_time = sum(response_times) / len(response_times)
            print(f"Average Response Time: {avg_response_time:.2f}s")
        
        # Print detailed results
        print("\nDetailed Results:")
        for result in self.test_results:
            status = result["status"]
            test_name = result["test"]
            message = result.get("message", f"Response time: {result.get('response_time', 0):.2f}s")
            print(f"{status} - {test_name}: {message}")
        
        # Save report to file
        report_file = project_root / "test_reports" / "web_interface_test_report.json"
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
        
        print(f"\nDetailed report saved to: {report_file}")
    
    def cleanup(self):
        """Clean up resources"""
        print("\nCleaning up...")
        
        if self.web_process:
            try:
                self.web_process.terminate()
                self.web_process.wait(timeout=5)
                print("Web interface stopped")
            except:
                print("Could not stop web interface gracefully")
    
    def run_tests(self):
        """Run all tests"""
        print("LLM Advanced Testing Suite - Complete Web Interface Test")
        print("=" * 70)
        
        # Start web interface
        if not self.start_web_interface():
            print("Failed to start web interface")
            return False
        
        # Give web interface time to fully load
        print("Waiting for web interface to fully load...")
        time.sleep(5)
        
        # Run tests
        self.test_basic_functionality()
        self.test_run_test_endpoint()
        self.test_performance()
        
        # Generate report
        self.generate_report()
        
        # Cleanup
        self.cleanup()
        
        # Return success status
        passed_tests = len([r for r in self.test_results if r["status"] == "PASS"])
        total_tests = len(self.test_results)
        
        print(f"\nSummary: {passed_tests}/{total_tests} tests passed")
        
        return passed_tests == total_tests

def main():
    """Main test function"""
    tester = WebInterfaceTester()
    success = tester.run_tests()
    
    if success:
        print("\nAll tests passed!")
        sys.exit(0)
    else:
        print("\nSome tests failed!")
        sys.exit(1)

if __name__ == "__main__":
    main()