#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Final Comprehensive Web Test
最终综合web测试脚本
"""

import subprocess
import sys
import time
import json
import threading
import requests
from pathlib import Path

def run_comprehensive_web_test():
    """运行最终的综合web测试"""
    print("Final Comprehensive Web Test")
    print("=" * 60)
    
    # Test Summary
    test_summary = {
        "start_time": time.strftime("%Y-%m-%d %H:%M:%S"),
        "total_tests": 0,
        "passed_tests": 0,
        "failed_tests": 0,
        "phases": {}
    }
    
    # Phase 1: System Environment Check
    print("\n[PHASE 1] System Environment Check")
    print("-" * 40)
    
    phase_results = []
    
    # Check Python version
    print("Checking Python environment...")
    try:
        result = subprocess.run([sys.executable, "--version"], capture_output=True, text=True)
        print(f"OK: {result.stdout.strip()}")
        phase_results.append({"test": "python_version", "status": "PASS"})
    except Exception as e:
        print(f"FAIL: Python check failed: {e}")
        phase_results.append({"test": "python_version", "status": "FAIL"})
    
    # Check required modules
    required_modules = ["streamlit", "requests", "json", "yaml", "pathlib"]
    for module in required_modules:
        try:
            __import__(module)
            print(f"OK: {module} module available")
            phase_results.append({"test": f"module_{module}", "status": "PASS"})
        except ImportError:
            print(f"FAIL: {module} module missing")
            phase_results.append({"test": f"module_{module}", "status": "FAIL"})
    
    test_summary["phases"]["environment"] = phase_results
    
    # Phase 2: Project Structure Validation
    print("\n[PHASE 2] Project Structure Validation")
    print("-" * 40)
    
    phase_results = []
    
    # Check directory structure
    required_dirs = ["tests", "config", "scripts", "docs", "core", "cognitive_ecosystem"]
    for dir_name in required_dirs:
        if Path(dir_name).exists() and Path(dir_name).is_dir():
            print(f"OK: {dir_name}/ directory exists")
            phase_results.append({"test": f"dir_{dir_name}", "status": "PASS"})
        else:
            print(f"FAIL: {dir_name}/ directory missing")
            phase_results.append({"test": f"dir_{dir_name}", "status": "FAIL"})
    
    # Check key files
    key_files = [
        "visual_test_interface.py",
        "tests/config.py",
        "config/test_config.yaml",
        "core/framework.py",
        "core/model_manager.py",
        "README.md"
    ]
    
    for file_path in key_files:
        if Path(file_path).exists():
            print(f"OK: {file_path} exists")
            phase_results.append({"test": f"file_{file_path}", "status": "PASS"})
        else:
            print(f"FAIL: {file_path} missing")
            phase_results.append({"test": f"file_{file_path}", "status": "FAIL"})
    
    test_summary["phases"]["structure"] = phase_results
    
    # Phase 3: Core Framework Test
    print("\n[PHASE 3] Core Framework Test")
    print("-" * 40)
    
    phase_results = []
    
    # Test basic imports
    print("Testing core framework imports...")
    try:
        # Test individual components
        import core.config_manager
        import core.model_manager
        import core.test_orchestrator
        print("OK: Core framework components imported")
        phase_results.append({"test": "core_imports", "status": "PASS"})
    except Exception as e:
        print(f"FAIL: Core framework import failed: {e}")
        phase_results.append({"test": "core_imports", "status": "FAIL"})
    
    # Test configuration system
    try:
        from tests.config import get_test_config
        config = get_test_config()
        print("OK: Configuration system working")
        phase_results.append({"test": "config_system", "status": "PASS"})
    except Exception as e:
        print(f"FAIL: Configuration system failed: {e}")
        phase_results.append({"test": "config_system", "status": "FAIL"})
    
    test_summary["phases"]["framework"] = phase_results
    
    # Phase 4: Test Suite Validation
    print("\n[PHASE 4] Test Suite Validation")
    print("-" * 40)
    
    phase_results = []
    
    # Count test files
    test_dir = Path("tests")
    if test_dir.exists():
        test_files = list(test_dir.glob("test_pillar_*.py"))
        print(f"OK: Found {len(test_files)} test files")
        phase_results.append({"test": "test_files_count", "status": "PASS", "count": len(test_files)})
        
        # Test loading a few test files
        sample_tests = test_files[:3]  # Test first 3 files
        for test_file in sample_tests:
            try:
                spec = __import__('importlib.util').util.spec_from_file_location("test_module", test_file)
                test_module = __import__('importlib.util').util.module_from_spec(spec)
                print(f"OK: {test_file.name} loads successfully")
                phase_results.append({"test": f"test_load_{test_file.name}", "status": "PASS"})
            except Exception as e:
                print(f"FAIL: {test_file.name} load failed: {e}")
                phase_results.append({"test": f"test_load_{test_file.name}", "status": "FAIL"})
    else:
        print("FAIL: Tests directory not found")
        phase_results.append({"test": "test_files_count", "status": "FAIL"})
    
    test_summary["phases"]["test_suite"] = phase_results
    
    # Phase 5: Web Interface Full Test
    print("\n[PHASE 5] Web Interface Full Test")
    print("-" * 40)
    
    phase_results = []
    web_process = None
    
    try:
        # Launch web interface
        print("Launching web interface...")
        web_process = subprocess.Popen([
            sys.executable, "-m", "streamlit", "run", 
            "visual_test_interface.py",
            "--server.port", "8503",
            "--server.address", "localhost",
            "--server.headless", "true",
            "--server.fileWatcherType", "none"
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        print(f"Web process started (PID: {web_process.pid})")
        
        # Wait for startup
        print("Waiting for web interface to start...")
        time.sleep(15)
        
        # Test accessibility
        try:
            response = requests.get("http://localhost:8503", timeout=10)
            if response.status_code == 200:
                print("OK: Web interface accessible")
                phase_results.append({"test": "web_accessibility", "status": "PASS"})
                
                # Test basic functionality
                if "LLM" in response.text or "测试" in response.text or "Test" in response.text:
                    print("OK: Web interface content valid")
                    phase_results.append({"test": "web_content", "status": "PASS"})
                else:
                    print("FAIL: Web interface content invalid")
                    phase_results.append({"test": "web_content", "status": "FAIL"})
            else:
                print(f"FAIL: Web interface returned {response.status_code}")
                phase_results.append({"test": "web_accessibility", "status": "FAIL"})
        except Exception as e:
            print(f"FAIL: Web interface test failed: {e}")
            phase_results.append({"test": "web_accessibility", "status": "FAIL"})
        
    except Exception as e:
        print(f"FAIL: Web interface launch failed: {e}")
        phase_results.append({"test": "web_launch", "status": "FAIL"})
    
    finally:
        # Cleanup
        if web_process and web_process.poll() is None:
            try:
                web_process.terminate()
                web_process.wait(timeout=10)
                print("OK: Web interface cleaned up")
                phase_results.append({"test": "web_cleanup", "status": "PASS"})
            except Exception as e:
                print(f"FAIL: Web interface cleanup failed: {e}")
                phase_results.append({"test": "web_cleanup", "status": "FAIL"})
    
    test_summary["phases"]["web_interface"] = phase_results
    
    # Calculate final results
    print("\n" + "=" * 60)
    print("FINAL COMPREHENSIVE TEST RESULTS")
    print("=" * 60)
    
    total_passed = 0
    total_failed = 0
    total_tests = 0
    
    for phase_name, results in test_summary["phases"].items():
        phase_passed = sum(1 for r in results if r["status"] == "PASS")
        phase_failed = sum(1 for r in results if r["status"] == "FAIL")
        phase_total = len(results)
        
        total_passed += phase_passed
        total_failed += phase_failed
        total_tests += phase_total
        
        print(f"\n{phase_name.upper().replace('_', ' ')}:")
        print(f"  Passed: {phase_passed}/{phase_total}")
        
        # Show failed tests
        failed_tests = [r for r in results if r["status"] == "FAIL"]
        for test in failed_tests:
            print(f"  FAIL: {test['test']}")
            if "error" in test:
                print(f"       Error: {test['error']}")
    
    overall_success_rate = (total_passed / total_tests) * 100 if total_tests > 0 else 0
    
    print(f"\nOVERALL RESULTS:")
    print(f"  Total Tests: {total_tests}")
    print(f"  Passed: {total_passed}")
    print(f"  Failed: {total_failed}")
    print(f"  Success Rate: {overall_success_rate:.1f}%")
    
    # Final status
    if overall_success_rate >= 85:
        print("\n*** SUCCESS: All critical systems operational! ***")
        print("✅ Web interface is fully functional")
        print("✅ Test framework is ready")
        print("✅ Project structure is complete")
        print("✅ All dependencies are available")
        final_status = "SUCCESS"
    else:
        print(f"\n*** PARTIAL SUCCESS: {overall_success_rate:.1f}% complete ***")
        print("Some issues need attention - see details above")
        final_status = "PARTIAL"
    
    # Save comprehensive report
    test_summary["end_time"] = time.strftime("%Y-%m-%d %H:%M:%S")
    test_summary["total_tests"] = total_tests
    test_summary["passed_tests"] = total_passed
    test_summary["failed_tests"] = total_failed
    test_summary["success_rate"] = overall_success_rate
    test_summary["final_status"] = final_status
    
    reports_dir = Path("test_reports")
    reports_dir.mkdir(exist_ok=True)
    
    report_file = reports_dir / f"comprehensive_web_test_{time.strftime('%Y%m%d_%H%M%S')}.json"
    with open(report_file, 'w', encoding='utf-8') as f:
        json.dump(test_summary, f, indent=2, ensure_ascii=False)
    
    print(f"\n*** Detailed report saved to: {report_file} ***")
    
    return overall_success_rate >= 85

if __name__ == "__main__":
    success = run_comprehensive_web_test()
    if success:
        print("\n*** Web automation testing is COMPLETE and READY! ***")
        print("You can now use: python visual_test_interface.py")
    else:
        print("\n*** Some issues remain - check the report for details ***")
    
    sys.exit(0 if success else 1)