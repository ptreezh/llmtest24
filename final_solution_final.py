import sys
import time
import json
import requests
from pathlib import Path

def test_web_interface():
    """Test web interface"""
    print("LLM Advanced Testing Suite - Web Interface Test")
    print("=" * 50)
    
    base_url = "http://localhost"
    test_results = []
    
    # Test 1: Check web interface status
    print("\nTest 1: Check web interface status")
    try:
        response = requests.get(f"{base_url}/", timeout=5)
        if response.status_code == 200:
            print("PASS: Web interface is running")
            test_results.append({"test": "Web interface status", "status": "PASS", "message": "Web interface is running"})
        else:
            print(f"FAIL: Web interface returned error status: {response.status_code}")
            test_results.append({"test": "Web interface status", "status": "FAIL", "message": f"Status code: {response.status_code}"})
    except Exception as e:
        print(f"FAIL: Web interface is not running: {e}")
        test_results.append({"test": "Web interface status", "status": "FAIL", "message": f"Connection failed: {e}"})
    
    # Test 2: Check API endpoints
    print("\nTest 2: Check API endpoints")
    api_endpoints = ["/api/models", "/api/tests", "/api/results"]
    
    for endpoint in api_endpoints:
        try:
            response = requests.get(f"{base_url}{endpoint}", timeout=5)
            if response.status_code == 200:
                print(f"PASS: {endpoint} is normal")
                test_results.append({"test": f"API endpoint {endpoint}", "status": "PASS", "message": "Normal"})
            else:
                print(f"FAIL: {endpoint} returned error: {response.status_code}")
                test_results.append({"test": f"API endpoint {endpoint}", "status": "FAIL", "message": f"Status code: {response.status_code}"})
        except Exception as e:
            print(f"FAIL: {endpoint} connection failed: {e}")
            test_results.append({"test": f"API endpoint {endpoint}", "status": "FAIL", "message": f"Connection failed: {e}"})
    
    # Test 3: Check functionality
    print("\nTest 3: Check functionality")
    try:
        test_data = {
            "pillar_name": "pillar_01_logic",
            "prompt": "Test prompt",
            "model_name": "test_model"
        }
        
        response = requests.post(
            f"{base_url}/api/run_test",
            json=test_data,
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        
        if response.status_code == 200:
            print("PASS: run_test functionality is normal")
            test_results.append({"test": "run_test functionality", "status": "PASS", "message": "Functionality is normal"})
        else:
            print(f"FAIL: run_test functionality error: {response.status_code}")
            test_results.append({"test": "run_test functionality", "status": "FAIL", "message": f"Status code: {response.status_code}"})
    except Exception as e:
        print(f"FAIL: run_test functionality failed: {e}")
        test_results.append({"test": "run_test functionality", "status": "FAIL", "message": f"Connection failed: {e}"})
    
    # Generate report
    print("\nGenerate test report")
    
    # Count results
    total_tests = len(test_results)
    passed_tests = len([r for r in test_results if r["status"] == "PASS"])
    failed_tests = len([r for r in test_results if r["status"] == "FAIL"])
    
    print(f"Total tests: {total_tests}")
    print(f"Passed tests: {passed_tests}")
    print(f"Failed tests: {failed_tests}")
    
    if total_tests > 0:
        success_rate = (passed_tests/total_tests)*100
        print(f"Success rate: {success_rate:.1f}%")
    
    # Save report
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
    
    print(f"Report saved: {report_file}")
    
    # Output final result
    print("\n" + "=" * 50)
    if passed_tests == total_tests:
        print("SUCCESS: All tests passed! Local web interface is running normally!")
        print(f"Access URL: {base_url}")
        print("Final solution successful!")
    else:
        print("FAIL: Some tests failed! Need to fix!")
        print("Please check if local web interface is running normally")
    
    return passed_tests == total_tests

if __name__ == "__main__":
    success = test_web_interface()
    sys.exit(0 if success else 1)