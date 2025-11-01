#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Complete Web Automation Test
完整的web自动化测试脚本
"""

import subprocess
import sys
import time
import json
import requests
import threading
from pathlib import Path

def run_web_automation_test():
    """运行完整的web自动化测试"""
    print("Complete Web Automation Test")
    print("=" * 50)
    
    test_results = []
    
    # Phase 1: Pre-flight checks
    print("\nPhase 1: Pre-flight Checks")
    print("-" * 30)
    
    # Check files exist
    required_files = [
        "visual_test_interface.py",
        "tests/config.py",
        "config/test_config.yaml",
        "launch_web_interface.py"
    ]
    
    for file_path in required_files:
        if Path(file_path).exists():
            print(f"OK: {file_path} exists")
            test_results.append({"phase": "preflight", "test": f"file_{file_path}", "status": "PASS"})
        else:
            print(f"FAIL: {file_path} missing")
            test_results.append({"phase": "preflight", "test": f"file_{file_path}", "status": "FAIL"})
    
    # Check dependencies
    try:
        import streamlit
        print("OK: Streamlit available")
        test_results.append({"phase": "preflight", "test": "streamlit", "status": "PASS"})
    except ImportError:
        print("FAIL: Streamlit not available")
        test_results.append({"phase": "preflight", "test": "streamlit", "status": "FAIL"})
    
    # Phase 2: Web Interface Launch
    print("\nPhase 2: Web Interface Launch")
    print("-" * 30)
    
    web_process = None
    try:
        print("Starting web interface...")
        web_process = subprocess.Popen([
            sys.executable, "-m", "streamlit", "run", 
            "visual_test_interface.py",
            "--server.port", "8502",
            "--server.address", "localhost",
            "--server.headless", "true",
            "--server.fileWatcherType", "none"
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        print(f"Web process started (PID: {web_process.pid})")
        
        # Wait for startup
        print("Waiting for web interface to start...")
        time.sleep(15)
        
        # Check if process is still running
        if web_process.poll() is None:
            print("OK: Web interface process running")
            test_results.append({"phase": "launch", "test": "process_running", "status": "PASS"})
        else:
            print("FAIL: Web interface process stopped")
            test_results.append({"phase": "launch", "test": "process_running", "status": "FAIL"})
            
    except Exception as e:
        print(f"FAIL: Failed to start web interface: {e}")
        test_results.append({"phase": "launch", "test": "process_start", "status": "FAIL", "error": str(e)})
    
    # Phase 3: Web Interface Testing
    print("\nPhase 3: Web Interface Testing")
    print("-" * 30)
    
    if web_process and web_process.poll() is None:
        # Test web interface accessibility
        try:
            response = requests.get("http://localhost:8502", timeout=10)
            if response.status_code == 200:
                print("OK: Web interface accessible")
                test_results.append({"phase": "testing", "test": "accessibility", "status": "PASS"})
            else:
                print(f"FAIL: Web interface returned {response.status_code}")
                test_results.append({"phase": "testing", "test": "accessibility", "status": "FAIL"})
        except Exception as e:
            print(f"FAIL: Could not access web interface: {e}")
            test_results.append({"phase": "testing", "test": "accessibility", "status": "FAIL", "error": str(e)})
        
        # Test content
        try:
            response = requests.get("http://localhost:8502", timeout=10)
            if "LLM" in response.text or "测试" in response.text:
                print("OK: Web interface contains expected content")
                test_results.append({"phase": "testing", "test": "content", "status": "PASS"})
            else:
                print("FAIL: Web interface content check failed")
                test_results.append({"phase": "testing", "test": "content", "status": "FAIL"})
        except Exception as e:
            print(f"FAIL: Content check failed: {e}")
            test_results.append({"phase": "testing", "test": "content", "status": "FAIL", "error": str(e)})
    else:
        print("SKIP: Web interface not running, skipping accessibility tests")
        test_results.append({"phase": "testing", "test": "accessibility", "status": "SKIP"})
        test_results.append({"phase": "testing", "test": "content", "status": "SKIP"})
    
    # Phase 4: Test Framework Integration
    print("\nPhase 4: Test Framework Integration")
    print("-" * 30)
    
    # Test basic test execution
    try:
        result = subprocess.run([
            sys.executable, "run_basic_web_tests.py"
        ], capture_output=True, text=True, timeout=60)
        
        if result.returncode == 0 and "ALL TESTS PASSED" in result.stdout:
            print("OK: Basic web tests passed")
            test_results.append({"phase": "integration", "test": "basic_tests", "status": "PASS"})
        else:
            print("FAIL: Basic web tests failed")
            test_results.append({"phase": "integration", "test": "basic_tests", "status": "FAIL"})
    except Exception as e:
        print(f"FAIL: Basic tests execution failed: {e}")
        test_results.append({"phase": "integration", "test": "basic_tests", "status": "FAIL", "error": str(e)})
    
    # Phase 5: Cleanup
    print("\nPhase 5: Cleanup")
    print("-" * 30)
    
    if web_process and web_process.poll() is None:
        try:
            web_process.terminate()
            web_process.wait(timeout=10)
            print("OK: Web interface stopped cleanly")
            test_results.append({"phase": "cleanup", "test": "process_stop", "status": "PASS"})
        except Exception as e:
            print(f"FAIL: Failed to stop web interface: {e}")
            test_results.append({"phase": "cleanup", "test": "process_stop", "status": "FAIL", "error": str(e)})
    else:
        print("OK: No process to stop")
        test_results.append({"phase": "cleanup", "test": "process_stop", "status": "PASS"})
    
    # Generate final report
    print("\n" + "=" * 50)
    print("FINAL TEST RESULTS")
    print("=" * 50)
    
    passed = sum(1 for r in test_results if r["status"] == "PASS")
    failed = sum(1 for r in test_results if r["status"] == "FAIL")
    skipped = sum(1 for r in test_results if r["status"] == "SKIP")
    total = len(test_results)
    success_rate = (passed / total) * 100 if total > 0 else 0
    
    print(f"Total Tests: {total}")
    print(f"Passed: {passed}")
    print(f"Failed: {failed}")
    print(f"Skipped: {skipped}")
    print(f"Success Rate: {success_rate:.1f}%")
    
    # Detailed results by phase
    phases = ["preflight", "launch", "testing", "integration", "cleanup"]
    for phase in phases:
        phase_results = [r for r in test_results if r["phase"] == phase]
        phase_passed = sum(1 for r in phase_results if r["status"] == "PASS")
        phase_total = len(phase_results)
        print(f"\n{phase.title()}: {phase_passed}/{phase_total} passed")
    
    # Save detailed report
    report = {
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "summary": {
            "total": total,
            "passed": passed,
            "failed": failed,
            "skipped": skipped,
            "success_rate": success_rate
        },
        "results": test_results
    }
    
    reports_dir = Path("test_reports")
    reports_dir.mkdir(exist_ok=True)
    
    report_file = reports_dir / f"complete_web_test_{time.strftime('%Y%m%d_%H%M%S')}.json"
    with open(report_file, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    
    print(f"\nDetailed report saved to: {report_file}")
    
    # Final status
    if success_rate >= 80:
        print("\nSUCCESS: Web automation test completed successfully!")
        print("The web interface is ready for use.")
        return True
    else:
        print("\nFAILURE: Web automation test failed.")
        print("Please check the detailed report for issues.")
        return False

if __name__ == "__main__":
    success = run_web_automation_test()
    sys.exit(0 if success else 1)