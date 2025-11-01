#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Real LLM Integration Test
真实的LLM集成测试
"""

import sys
import os
import time
import json
from pathlib import Path

# Add project root to path
sys.path.append(str(Path(__file__).parent))

def test_real_llm_integration():
    """测试真实的LLM集成"""
    print("Real LLM Integration Test")
    print("=" * 40)
    
    results = []
    
    # Test 1: Import cloud services
    print("Test 1: Testing cloud services import...")
    try:
        sys.path.append(str(Path(__file__).parent / "scripts" / "utils"))
        import cloud_services
        print("OK: Cloud services imported")
        results.append({"test": "cloud_services_import", "status": "PASS"})
    except Exception as e:
        print(f"FAIL: Cloud services import failed: {e}")
        results.append({"test": "cloud_services_import", "status": "FAIL"})
    
    # Test 2: Check available models
    print("\nTest 2: Testing available models...")
    try:
        models = cloud_services.get_all_models()
        print(f"OK: Found {len(models)} models")
        for model in models[:3]:  # Show first 3 models
            print(f"  - {model['key']}")
        results.append({"test": "available_models", "status": "PASS", "count": len(models)})
    except Exception as e:
        print(f"FAIL: Could not get models: {e}")
        results.append({"test": "available_models", "status": "FAIL"})
    
    # Test 3: Test actual model call
    print("\nTest 3: Testing actual model call...")
    try:
        # Try to call a simple model
        test_prompt = "Please respond with just 'Hello World'"
        
        # Try different services
        services_to_test = ['together', 'ppinfra', 'glm']
        test_success = False
        
        for service in services_to_test:
            try:
                if service in cloud_services.CLOUD_SERVICES:
                    config = cloud_services.CLOUD_SERVICES[service]
                    model = config['models'][0]  # Use first model
                    
                    response = cloud_services.call_cloud_service(
                        service, model, test_prompt
                    )
                    
                    if response and len(response) > 0:
                        print(f"OK: {service} model call successful")
                        print(f"  Response: {response[:100]}...")
                        results.append({
                            "test": f"model_call_{service}", 
                            "status": "PASS",
                            "response_length": len(response)
                        })
                        test_success = True
                        break
                    else:
                        print(f"FAIL: {service} returned empty response")
            except Exception as e:
                print(f"FAIL: {service} call failed: {e}")
                results.append({
                    "test": f"model_call_{service}", 
                    "status": "FAIL",
                    "error": str(e)
                })
        
        if not test_success:
            print("WARNING: No model calls successful, will use simulation mode")
            results.append({"test": "model_calls", "status": "WARNING"})
            
    except Exception as e:
        print(f"FAIL: Model call test failed: {e}")
        results.append({"test": "model_calls", "status": "FAIL"})
    
    # Test 4: Test actual test execution
    print("\nTest 4: Testing real test execution...")
    try:
        # Try to run a real test
        from tests.utils import run_single_test
        from tests.config import get_test_config
        
        config = get_test_config()
        model_to_test = 'together/mistralai/Mixtral-8x7B-Instruct-v0.1'
        
        # Run a simple test
        response, metadata = run_single_test(
            "Test Logic", 
            "What is 2+2?", 
            model_to_test,
            {"temperature": 0.1}
        )
        
        if response and "调用失败" not in response:
            print("OK: Real test execution successful")
            print(f"  Response: {response[:100]}...")
            results.append({
                "test": "real_test_execution", 
                "status": "PASS",
                "response_length": len(response)
            })
        else:
            print("FAIL: Real test execution failed")
            results.append({
                "test": "real_test_execution", 
                "status": "FAIL",
                "response": response
            })
            
    except Exception as e:
        print(f"FAIL: Test execution failed: {e}")
        results.append({"test": "real_test_execution", "status": "FAIL"})
    
    # Calculate results
    passed = sum(1 for r in results if r["status"] == "PASS")
    total = len(results)
    success_rate = (passed / total) * 100 if total > 0 else 0
    
    print(f"\nResults: {passed}/{total} tests passed ({success_rate:.1f}%)")
    
    # Save results
    report = {
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "total_tests": total,
        "passed_tests": passed,
        "success_rate": success_rate,
        "results": results
    }
    
    os.makedirs("test_reports", exist_ok=True)
    with open("test_reports/real_llm_test_report.json", "w") as f:
        json.dump(report, f, indent=2)
    
    return success_rate >= 50  # 50% threshold for real LLM testing

if __name__ == "__main__":
    success = test_real_llm_integration()
    if success:
        print("\n*** Real LLM integration test PASSED ***")
    else:
        print("\n*** Real LLM integration test FAILED ***")
    
    sys.exit(0 if success else 1)