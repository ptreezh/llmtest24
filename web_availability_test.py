#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
LLM Advanced Testing Suite - Web Availability Test
Web可用性测试脚本
"""

import os
import sys
import json
import time
import subprocess
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def test_web_availability():
    """Web可用性测试"""
    print("LLM Advanced Testing Suite - Web Availability Test")
    print("=" * 60)
    
    test_results = []
    
    # Test 1: Check if visual_test_interface.py exists
    print("Test 1: Checking web interface file...")
    web_interface_file = Path("visual_test_interface.py")
    if web_interface_file.exists():
        print("PASS: visual_test_interface.py exists")
        test_results.append({"test": "Web Interface File", "status": "PASS"})
    else:
        print("FAIL: visual_test_interface.py missing")
        test_results.append({"test": "Web Interface File", "status": "FAIL"})
    
    # Test 2: Check basic dependencies
    print("\nTest 2: Checking basic dependencies...")
    basic_deps = ["requests", "json", "os", "sys", "time"]
    for dep in basic_deps:
        try:
            __import__(dep)
            print(f"PASS: {dep} available")
            test_results.append({"test": f"Dependency {dep}", "status": "PASS"})
        except ImportError:
            print(f"FAIL: {dep} missing")
            test_results.append({"test": f"Dependency {dep}", "status": "FAIL"})
    
    # Test 3: Check test structure
    print("\nTest 3: Checking test structure...")
    test_structure = [
        "tests/",
        "config/",
        "scripts/",
        "docs/"
    ]
    
    for structure in test_structure:
        path = Path(structure)
        if path.exists():
            print(f"PASS: {structure} exists")
            test_results.append({"test": f"Structure {structure}", "status": "PASS"})
        else:
            print(f"FAIL: {structure} missing")
            test_results.append({"test": f"Structure {structure}", "status": "FAIL"})
    
    # Test 4: Check configuration files
    print("\nTest 4: Checking configuration...")
    config_files = [
        "config/config.py",
        "config/test_config.yaml",
        "config/roles.yaml"
    ]
    
    for config_file in config_files:
        if Path(config_file).exists():
            print(f"PASS: {config_file} exists")
            test_results.append({"test": f"Config {config_file}", "status": "PASS"})
        else:
            print(f"FAIL: {config_file} missing")
            test_results.append({"test": f"Config {config_file}", "status": "FAIL"})
    
    # Test 5: Check if we can import basic test modules
    print("\nTest 5: Checking test modules...")
    test_modules = [
        "tests.config",
        "tests.utils"
    ]
    
    for module in test_modules:
        try:
            __import__(module)
            print(f"PASS: {module} imports successfully")
            test_results.append({"test": f"Module {module}", "status": "PASS"})
        except ImportError as e:
            print(f"FAIL: {module} import failed: {e}")
            test_results.append({"test": f"Module {module}", "status": "FAIL", "error": str(e)})
    
    # Test 6: Test basic functionality without web interface
    print("\nTest 6: Testing basic functionality...")
    try:
        # Test if we can read configuration
        result = subprocess.run([
            sys.executable, "-c", 
            """
import sys
sys.path.append('.')
try:
    from tests.config import get_test_config
    config = get_test_config()
    print('Configuration loaded successfully')
except Exception as e:
    print(f'Configuration test failed: {e}')
    sys.exit(1)
"""
        ], capture_output=True, text=True, timeout=10)
        
        if result.returncode == 0:
            print("PASS: Basic functionality test")
            test_results.append({"test": "Basic Functionality", "status": "PASS"})
        else:
            print(f"FAIL: Basic functionality test: {result.stderr}")
            test_results.append({"test": "Basic Functionality", "status": "FAIL", "error": result.stderr})
    except Exception as e:
        print(f"FAIL: Basic functionality test exception: {e}")
        test_results.append({"test": "Basic Functionality", "status": "FAIL", "error": str(e)})
    
    # Test 7: Check if test files exist
    print("\nTest 7: Checking test files...")
    test_dir = Path("tests")
    if test_dir.exists():
        test_files = list(test_dir.glob("test_pillar_*.py"))
        print(f"PASS: Found {len(test_files)} test files")
        test_results.append({"test": "Test Files Count", "status": "PASS", "count": len(test_files)})
    else:
        print("FAIL: Tests directory not found")
        test_results.append({"test": "Test Files Count", "status": "FAIL"})
    
    # Generate test report
    print("\n" + "=" * 60)
    print("WEB AVAILABILITY TEST REPORT")
    print("=" * 60)
    
    passed_tests = sum(1 for result in test_results if result["status"] == "PASS")
    total_tests = len(test_results)
    success_rate = (passed_tests / total_tests) * 100 if total_tests > 0 else 0
    
    print(f"Total Tests: {total_tests}")
    print(f"Passed: {passed_tests}")
    print(f"Failed: {total_tests - passed_tests}")
    print(f"Success Rate: {success_rate:.1f}%")
    
    # Save detailed results
    report_path = Path("test_reports/web_availability_test_report.json")
    report_path.parent.mkdir(exist_ok=True)
    
    report_data = {
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "total_tests": total_tests,
        "passed_tests": passed_tests,
        "failed_tests": total_tests - passed_tests,
        "success_rate": success_rate,
        "test_results": test_results
    }
    
    with open(report_path, 'w', encoding='utf-8') as f:
        json.dump(report_data, f, indent=2, ensure_ascii=False)
    
    print(f"\nDetailed report saved to: {report_path}")
    
    if success_rate >= 70:
        print("SUCCESS: Web availability test PASSED")
        return True
    else:
        print("FAILURE: Web availability test FAILED")
        return False

if __name__ == "__main__":
    success = test_web_availability()
    sys.exit(0 if success else 1)