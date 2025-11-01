#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
LLM Advanced Testing Suite - Web Interface Test
This script tests the web interface functionality.
"""

import os
import sys
import time
import json
import requests
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

def test_web_interface():
    """Test the web interface"""
    print("LLM Advanced Testing Suite - Web Interface Test")
    print("=" * 60)
    
    base_url = "http://localhost:8501"
    test_results = []
    
    # Test 1: Check if web interface is accessible
    print("Test 1: Checking web interface accessibility...")
    try:
        response = requests.get(f"{base_url}/", timeout=10)
        if response.status_code == 200:
            print("PASS: Web interface is accessible")
            test_results.append({"test": "Web Interface Accessibility", "status": "PASS", "response_time": response.elapsed.total_seconds()})
        else:
            print(f"FAIL: Web interface returned status code {response.status_code}")
            test_results.append({"test": "Web Interface Accessibility", "status": "FAIL", "response_time": response.elapsed.total_seconds()})
    except Exception as e:
        print(f"FAIL: Could not connect to web interface - {e}")
        test_results.append({"test": "Web Interface Accessibility", "status": "FAIL", "message": str(e)})
    
    # Test 2: Check API endpoints
    print("\nTest 2: Checking API endpoints...")
    endpoints = [
        ("/api/models", "GET"),
        ("/api/tests", "GET"),
        ("/api/results", "GET")
    ]
    
    for endpoint, method in endpoints:
        try:
            if method == "GET":
                response = requests.get(f"{base_url}{endpoint}", timeout=10)
            else:
                response = requests.post(f"{base_url}{endpoint}", timeout=10)
            
            if response.status_code in [200, 201]:
                print(f"PASS: {endpoint} - {method}")
                test_results.append({"test": f"API {endpoint}", "status": "PASS", "response_time": response.elapsed.total_seconds()})
            else:
                print(f"FAIL: {endpoint} - Status {response.status_code}")
                test_results.append({"test": f"API {endpoint}", "status": "FAIL", "response_time": response.elapsed.total_seconds()})
        except Exception as e:
            print(f"FAIL: {endpoint} - {e}")
            test_results.append({"test": f"API {endpoint}", "status": "FAIL", "message": str(e)})
    
    # Test 3: Test run_test endpoint
    print("\nTest 3: Testing run_test endpoint...")
    test_data = {
        "pillar_name": "pillar_01_logic",
        "prompt": "If all roses are flowers and some flowers fade quickly, can we conclude that some roses fade quickly?",
        "model_name": "test_model"
    }
    
    try:
        response = requests.post(
            f"{base_url}/api/run_test",
            json=test_data,
            headers={"Content-Type": "application/json"},
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            if "success" in result and "score" in result:
                print("PASS: run_test endpoint works correctly")
                test_results.append({"test": "run_test endpoint", "status": "PASS", "response_time": response.elapsed.total_seconds()})
            else:
                print("FAIL: run_test endpoint returned invalid response")
                test_results.append({"test": "run_test endpoint", "status": "FAIL", "response_time": response.elapsed.total_seconds()})
        else:
            print(f"FAIL: run_test endpoint returned status {response.status_code}")
            test_results.append({"test": "run_test endpoint", "status": "FAIL", "response_time": response.elapsed.total_seconds()})
    except Exception as e:
        print(f"FAIL: run_test endpoint error - {e}")
        test_results.append({"test": "run_test endpoint", "status": "FAIL", "message": str(e)})
    
    # Test 4: Test performance
    print("\nTest 4: Testing performance...")
    pages = ["/", "/api/models", "/api/tests", "/api/results"]
    
    for page in pages:
        start_time = time.time()
        try:
            response = requests.get(f"{base_url}{page}", timeout=10)
            end_time = time.time()
            load_time = end_time - start_time
            
            if load_time < 3.0:
                print(f"PASS: {page} - {load_time:.2f}s")
                test_results.append({"test": f"Performance - {page}", "status": "PASS", "response_time": load_time})
            else:
                print(f"WARN: {page} - {load_time:.2f}s (slow)")
                test_results.append({"test": f"Performance - {page}", "status": "WARN", "response_time": load_time})
        except Exception as e:
            print(f"FAIL: {page} - {e}")
            test_results.append({"test": f"Performance - {page}", "status": "FAIL", "message": str(e)})
    
    # Generate report
    generate_report(test_results)
    
    # Return success status
    passed_tests = len([r for r in test_results if r["status"] == "PASS"])
    total_tests = len(test_results)
    
    print(f"\nSummary: {passed_tests}/{total_tests} tests passed")
    
    return passed_tests == total_tests

def generate_report(test_results):
    """Generate test report"""
    print("\nTest Report")
    print("=" * 60)
    
    # Count results
    total_tests = len(test_results)
    passed_tests = len([r for r in test_results if r["status"] == "PASS"])
    failed_tests = len([r for r in test_results if r["status"] == "FAIL"])
    warning_tests = len([r for r in test_results if r["status"] == "WARN"])
    
    print(f"Total Tests: {total_tests}")
    print(f"Passed: {passed_tests}")
    print(f"Failed: {failed_tests}")
    print(f"Warnings: {warning_tests}")
    
    if total_tests > 0:
        success_rate = (passed_tests/total_tests)*100
        print(f"Success Rate: {success_rate:.1f}%")
    
    # Calculate average response time
    response_times = [r.get("response_time", 0) for r in test_results if "response_time" in r]
    if response_times:
        avg_response_time = sum(response_times) / len(response_times)
        print(f"Average Response Time: {avg_response_time:.2f}s")
    
    # Print detailed results
    print("\nDetailed Results:")
    for result in test_results:
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
        "results": test_results
    }
    
    with open(report_file, 'w', encoding='utf-8') as f:
        json.dump(report_data, f, indent=2, ensure_ascii=False)
    
    print(f"\nDetailed report saved to: {report_file}")

def main():
    """Main test function"""
    success = test_web_interface()
    
    if success:
        print("\nAll tests passed!")
        sys.exit(0)
    else:
        print("\nSome tests failed!")
        sys.exit(1)

if __name__ == "__main__":
    main()