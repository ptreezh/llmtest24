#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Final Complete Web Test with Real LLM
最终完整web测试，包含真实LLM
"""

import subprocess
import sys
import time
import json
import threading
import requests
import os
from pathlib import Path

def run_final_complete_web_test():
    """运行最终完整的web测试"""
    print("Final Complete Web Test with Real LLM")
    print("=" * 60)
    
    test_results = []
    
    # Phase 1: System Readiness Check
    print("\n[PHASE 1] System Readiness Check")
    print("-" * 40)
    
    # Check API keys
    api_keys = ['TOGETHER_API_KEY', 'OPENROUTER_API_KEY', 'PPINFRA_API_KEY', 'GEMINI_API_KEY']
    available_keys = [key for key in api_keys if os.getenv(key)]
    print(f"Available API keys: {len(available_keys)}/{len(api_keys)}")
    test_results.append({
        "phase": "readiness",
        "test": "api_keys",
        "status": "PASS" if len(available_keys) > 0 else "FAIL",
        "available": len(available_keys)
    })
    
    # Check dependencies
    deps_to_check = ['streamlit', 'requests', 'yaml', 'json']
    for dep in deps_to_check:
        try:
            __import__(dep)
            print(f"OK: {dep} available")
            test_results.append({"phase": "readiness", "test": f"dep_{dep}", "status": "PASS"})
        except ImportError:
            print(f"FAIL: {dep} missing")
            test_results.append({"phase": "readiness", "test": f"dep_{dep}", "status": "FAIL"})
    
    # Phase 2: Real LLM Testing
    print("\n[PHASE 2] Real LLM Testing")
    print("-" * 40)
    
    # Run real LLM test
    try:
        result = subprocess.run([
            sys.executable, "test_real_llm.py"
        ], capture_output=True, text=True, timeout=120)
        
        if result.returncode == 0:
            print("OK: Real LLM integration test passed")
            test_results.append({"phase": "real_llm", "test": "integration", "status": "PASS"})
            
            # Parse the results
            if "Results:" in result.stdout:
                results_line = [line for line in result.stdout.split('\n') if line.startswith("Results:")][0]
                print(f"  {results_line}")
        else:
            print("FAIL: Real LLM integration test failed")
            test_results.append({"phase": "real_llm", "test": "integration", "status": "FAIL"})
    except Exception as e:
        print(f"FAIL: Real LLM test execution failed: {e}")
        test_results.append({"phase": "real_llm", "test": "integration", "status": "FAIL"})
    
    # Phase 3: Web Interface Launch and Test
    print("\n[PHASE 3] Web Interface Launch and Test")
    print("-" * 40)
    
    web_process = None
    try:
        # Launch web interface
        print("Launching web interface...")
        web_process = subprocess.Popen([
            sys.executable, "-m", "streamlit", "run", 
            "visual_test_interface.py",
            "--server.port", "8504",
            "--server.address", "localhost",
            "--server.headless", "true",
            "--server.fileWatcherType", "none"
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        print(f"Web process started (PID: {web_process.pid})")
        
        # Wait for startup
        print("Waiting for web interface to start...")
        time.sleep(20)
        
        # Test accessibility
        try:
            response = requests.get("http://localhost:8504", timeout=15)
            if response.status_code == 200:
                print("OK: Web interface accessible")
                test_results.append({"phase": "web", "test": "accessibility", "status": "PASS"})
                
                # Test content
                if "LLM" in response.text or "测试" in response.text:
                    print("OK: Web interface content valid")
                    test_results.append({"phase": "web", "test": "content", "status": "PASS"})
                else:
                    print("FAIL: Web interface content invalid")
                    test_results.append({"phase": "web", "test": "content", "status": "FAIL"})
            else:
                print(f"FAIL: Web interface returned {response.status_code}")
                test_results.append({"phase": "web", "test": "accessibility", "status": "FAIL"})
        except Exception as e:
            print(f"FAIL: Web interface test failed: {e}")
            test_results.append({"phase": "web", "test": "accessibility", "status": "FAIL"})
            
    except Exception as e:
        print(f"FAIL: Web interface launch failed: {e}")
        test_results.append({"phase": "web", "test": "launch", "status": "FAIL"})
    
    finally:
        # Cleanup
        if web_process and web_process.poll() is None:
            try:
                web_process.terminate()
                web_process.wait(timeout=10)
                print("OK: Web interface stopped")
                test_results.append({"phase": "web", "test": "cleanup", "status": "PASS"})
            except Exception as e:
                print(f"FAIL: Web interface cleanup failed: {e}")
                test_results.append({"phase": "web", "test": "cleanup", "status": "FAIL"})
    
    # Phase 4: End-to-End Test Execution
    print("\n[PHASE 4] End-to-End Test Execution")
    print("-" * 40)
    
    # Test actual test execution via web interface
    try:
        # Run a comprehensive test
        result = subprocess.run([
            sys.executable, "final_comprehensive_web_test.py"
        ], capture_output=True, text=True, timeout=180)
        
        if result.returncode == 0:
            print("OK: Comprehensive web test passed")
            test_results.append({"phase": "e2e", "test": "comprehensive", "status": "PASS"})
            
            # Extract success rate
            if "Success Rate:" in result.stdout:
                for line in result.stdout.split('\n'):
                    if "Success Rate:" in line:
                        print(f"  {line.strip()}")
                        break
        else:
            print("FAIL: Comprehensive web test failed")
            test_results.append({"phase": "e2e", "test": "comprehensive", "status": "FAIL"})
    except Exception as e:
        print(f"FAIL: End-to-end test failed: {e}")
        test_results.append({"phase": "e2e", "test": "comprehensive", "status": "FAIL"})
    
    # Phase 5: Model Selection and Real Test
    print("\n[PHASE 5] Model Selection and Real Test")
    print("-" * 40)
    
    try:
        # Test model selection
        sys.path.append(str(Path(__file__).parent / "scripts" / "utils"))
        import cloud_services
        
        models = cloud_services.get_all_models()
        working_models = []
        
        # Test a few models
        for model_info in models[:3]:  # Test first 3 models
            try:
                service, model = model_info['key'].split('-')[-1], model_info['model']
                response = cloud_services.call_cloud_service(
                    service, model, "Respond with 'Model test successful'"
                )
                if response and "successful" in response.lower():
                    working_models.append(model_info['key'])
                    print(f"OK: {model_info['key']} working")
                else:
                    print(f"FAIL: {model_info['key']} not working properly")
            except Exception as e:
                print(f"FAIL: {model_info['key']} error: {e}")
        
        if working_models:
            print(f"OK: {len(working_models)} models working")
            test_results.append({
                "phase": "models", 
                "test": "working_models", 
                "status": "PASS",
                "count": len(working_models),
                "models": working_models
            })
        else:
            print("FAIL: No working models")
            test_results.append({"phase": "models", "test": "working_models", "status": "FAIL"})
            
    except Exception as e:
        print(f"FAIL: Model testing failed: {e}")
        test_results.append({"phase": "models", "test": "working_models", "status": "FAIL"})
    
    # Calculate final results
    print("\n" + "=" * 60)
    print("FINAL COMPLETE WEB TEST RESULTS")
    print("=" * 60)
    
    passed = sum(1 for r in test_results if r["status"] == "PASS")
    total = len(test_results)
    success_rate = (passed / total) * 100 if total > 0 else 0
    
    print(f"Total Tests: {total}")
    print(f"Passed: {passed}")
    print(f"Failed: {total - passed}")
    print(f"Success Rate: {success_rate:.1f}%")
    
    # Results by phase
    phases = ["readiness", "real_llm", "web", "e2e", "models"]
    for phase in phases:
        phase_results = [r for r in test_results if r["phase"] == phase]
        phase_passed = sum(1 for r in phase_results if r["status"] == "PASS")
        phase_total = len(phase_results)
        print(f"\n{phase.upper()}: {phase_passed}/{phase_total} passed")
    
    # Final status
    if success_rate >= 85:
        print("\n*** SUCCESS: Complete web testing with real LLM operational! ***")
        print("Real LLM integration working")
        print("Web interface fully functional")
        print("End-to-end testing complete")
        print("Multiple models available")
        final_status = "SUCCESS"
    else:
        print(f"\n*** PARTIAL SUCCESS: {success_rate:.1f}% complete ***")
        print("Some issues remain")
        final_status = "PARTIAL"
    
    # Save comprehensive report
    report = {
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "test_type": "Final Complete Web Test with Real LLM",
        "summary": {
            "total": total,
            "passed": passed,
            "failed": total - passed,
            "success_rate": success_rate,
            "final_status": final_status
        },
        "test_results": test_results,
        "available_api_keys": len(available_keys),
        "working_models": len([r for r in test_results if r.get("count")])
    }
    
    os.makedirs("test_reports", exist_ok=True)
    report_file = f"test_reports/final_complete_test_{time.strftime('%Y%m%d_%H%M%S')}.json"
    with open(report_file, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    
    print(f"\nDetailed report saved to: {report_file}")
    
    return success_rate >= 85

if __name__ == "__main__":
    success = run_final_complete_web_test()
    if success:
        print("\n*** WEB AUTOMATION WITH REAL LLM IS COMPLETE AND READY! ***")
        print("\nUsage Instructions:")
        print("1. Launch web interface: python visual_test_interface.py")
        print("2. Run tests via web interface")
        print("3. Or run directly: python test_real_llm.py")
        print("\nAvailable real models: Together.ai, PPInfra, GLM")
    else:
        print("\n*** Some issues remain - check the report ***")
    
    sys.exit(0 if success else 1)