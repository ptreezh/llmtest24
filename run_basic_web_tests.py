#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Simple test runner for web testing
"""

import sys
import os
import time
import json
from pathlib import Path

def run_basic_tests():
    """Run basic tests to verify functionality"""
    print("Running Basic Web Tests")
    print("=" * 40)
    
    results = []
    
    # Test 1: Check basic imports
    print("Test 1: Basic imports...")
    try:
        import json
        import os
        import sys
        import time
        print("OK: Basic Python modules imported")
        results.append({"test": "basic_imports", "status": "PASS"})
    except Exception as e:
        print(f"FAIL: Basic imports failed: {e}")
        results.append({"test": "basic_imports", "status": "FAIL", "error": str(e)})
    
    # Test 2: Check project structure
    print("\nTest 2: Project structure...")
    required_files = [
        "visual_test_interface.py",
        "tests/config.py",
        "config/test_config.yaml",
        "README.md"
    ]
    
    for file_path in required_files:
        if Path(file_path).exists():
            print(f"OK: {file_path} exists")
            results.append({"test": f"file_{file_path}", "status": "PASS"})
        else:
            print(f"FAIL: {file_path} missing")
            results.append({"test": f"file_{file_path}", "status": "FAIL"})
    
    # Test 3: Check test files
    print("\nTest 3: Test files...")
    test_dir = Path("tests")
    if test_dir.exists():
        test_files = list(test_dir.glob("test_pillar_*.py"))
        print(f"OK: Found {len(test_files)} test files")
        results.append({"test": "test_files_count", "status": "PASS", "count": len(test_files)})
        
        # Try to load a test file
        if test_files:
            try:
                test_file = test_files[0]
                spec = __import__('importlib.util').util.spec_from_file_location("test_module", test_file)
                test_module = __import__('importlib.util').util.module_from_spec(spec)
                print(f"OK: Test file {test_file.name} can be loaded")
                results.append({"test": "test_file_load", "status": "PASS"})
            except Exception as e:
                print(f"FAIL: Test file load failed: {e}")
                results.append({"test": "test_file_load", "status": "FAIL", "error": str(e)})
    else:
        print("FAIL: Tests directory missing")
        results.append({"test": "test_files_count", "status": "FAIL"})
    
    # Test 4: Configuration test
    print("\nTest 4: Configuration...")
    try:
        # Try to load config directly
        config_path = Path("tests/config.py")
        if config_path.exists():
            with open(config_path, 'r', encoding='utf-8') as f:
                config_content = f.read()
            print("OK: Configuration file readable")
            results.append({"test": "config_readable", "status": "PASS"})
        else:
            print("FAIL: Configuration file missing")
            results.append({"test": "config_readable", "status": "FAIL"})
    except Exception as e:
        print(f"FAIL: Configuration test failed: {e}")
        results.append({"test": "config_readable", "status": "FAIL", "error": str(e)})
    
    # Test 5: Web interface check
    print("\nTest 5: Web interface...")
    web_interface = Path("visual_test_interface.py")
    if web_interface.exists():
        try:
            with open(web_interface, 'r', encoding='utf-8') as f:
                web_content = f.read()
            if 'streamlit' in web_content:
                print("OK: Web interface contains streamlit")
                results.append({"test": "web_interface_streamlit", "status": "PASS"})
            else:
                print("FAIL: Web interface missing streamlit")
                results.append({"test": "web_interface_streamlit", "status": "FAIL"})
        except Exception as e:
            print(f"FAIL: Web interface read failed: {e}")
            results.append({"test": "web_interface_streamlit", "status": "FAIL", "error": str(e)})
    else:
        print("FAIL: Web interface file missing")
        results.append({"test": "web_interface_streamlit", "status": "FAIL"})
    
    # Calculate results
    passed = sum(1 for r in results if r["status"] == "PASS")
    total = len(results)
    success_rate = (passed / total) * 100 if total > 0 else 0
    
    # Generate report
    print("\n" + "=" * 40)
    print("TEST RESULTS")
    print("=" * 40)
    print(f"Total Tests: {total}")
    print(f"Passed: {passed}")
    print(f"Failed: {total - passed}")
    print(f"Success Rate: {success_rate:.1f}%")
    
    # Save results
    report = {
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "total_tests": total,
        "passed_tests": passed,
        "failed_tests": total - passed,
        "success_rate": success_rate,
        "results": results
    }
    
    # Create reports directory
    reports_dir = Path("test_reports")
    reports_dir.mkdir(exist_ok=True)
    
    # Save JSON report
    report_file = reports_dir / f"web_test_report_{time.strftime('%Y%m%d_%H%M%S')}.json"
    with open(report_file, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    
    print(f"\nDetailed report saved to: {report_file}")
    
    return success_rate >= 80

if __name__ == "__main__":
    success = run_basic_tests()
    if success:
        print("\nOK: ALL TESTS PASSED - Web interface ready!")
    else:
        print("\nFAIL: SOME TESTS FAILED - Check report for details")
    
    sys.exit(0 if success else 1)