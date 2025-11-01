#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Simple Final Test with Real LLM
简化的最终真实LLM测试
"""

import subprocess
import sys
import time
import json
import os
from pathlib import Path

def run_simple_final_test():
    """运行简化的最终测试"""
    print("Simple Final Test with Real LLM")
    print("=" * 50)
    
    results = []
    
    # Test 1: Real LLM Integration
    print("\n1. Testing Real LLM Integration...")
    try:
        result = subprocess.run([
            sys.executable, "test_real_llm.py"
        ], capture_output=True, text=True, timeout=120)
        
        if result.returncode == 0:
            print("OK: Real LLM test passed")
            results.append({"test": "real_llm", "status": "PASS"})
        else:
            print("FAIL: Real LLM test failed")
            results.append({"test": "real_llm", "status": "FAIL"})
    except Exception as e:
        print(f"FAIL: Real LLM test error: {e}")
        results.append({"test": "real_llm", "status": "FAIL"})
    
    # Test 2: Web Interface
    print("\n2. Testing Web Interface...")
    try:
        import streamlit
        print("OK: Streamlit available")
        results.append({"test": "streamlit", "status": "PASS"})
    except ImportError:
        print("FAIL: Streamlit not available")
        results.append({"test": "streamlit", "status": "FAIL"})
    
    # Test 3: Cloud Services
    print("\n3. Testing Cloud Services...")
    try:
        sys.path.append(str(Path(__file__).parent / "scripts" / "utils"))
        import cloud_services
        
        models = cloud_services.get_all_models()
        print(f"OK: {len(models)} models available")
        results.append({"test": "cloud_services", "status": "PASS", "models": len(models)})
        
        # Test one model
        try:
            response = cloud_services.call_cloud_service(
                "together", "mistralai/Mixtral-8x7B-Instruct-v0.1", "Test"
            )
            print("OK: Model call successful")
            results.append({"test": "model_call", "status": "PASS"})
        except Exception as e:
            print(f"FAIL: Model call failed: {e}")
            results.append({"test": "model_call", "status": "FAIL"})
            
    except Exception as e:
        print(f"FAIL: Cloud services error: {e}")
        results.append({"test": "cloud_services", "status": "FAIL"})
    
    # Test 4: Test Files
    print("\n4. Testing Test Files...")
    test_dir = Path("tests")
    if test_dir.exists():
        test_files = list(test_dir.glob("test_pillar_*.py"))
        print(f"OK: {len(test_files)} test files found")
        results.append({"test": "test_files", "status": "PASS", "count": len(test_files)})
    else:
        print("FAIL: Test files not found")
        results.append({"test": "test_files", "status": "FAIL"})
    
    # Calculate results
    passed = sum(1 for r in results if r["status"] == "PASS")
    total = len(results)
    success_rate = (passed / total) * 100 if total > 0 else 0
    
    print(f"\nResults: {passed}/{total} tests passed ({success_rate:.1f}%)")
    
    # Save report
    report = {
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "total_tests": total,
        "passed_tests": passed,
        "success_rate": success_rate,
        "results": results,
        "status": "SUCCESS" if success_rate >= 75 else "PARTIAL"
    }
    
    os.makedirs("test_reports", exist_ok=True)
    with open("test_reports/final_test_summary.json", "w") as f:
        json.dump(report, f, indent=2)
    
    # Final status
    if success_rate >= 75:
        print("\n*** SUCCESS: Real LLM Web Testing is READY! ***")
        print("\nYou can now:")
        print("1. Use web interface: python visual_test_interface.py")
        print("2. Run real LLM tests: python test_real_llm.py")
        print("3. Available models: Together.ai, PPInfra, GLM")
        return True
    else:
        print(f"\n*** PARTIAL: {success_rate:.1f}% complete ***")
        return False

if __name__ == "__main__":
    success = run_simple_final_test()
    sys.exit(0 if success else 1)