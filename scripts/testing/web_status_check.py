#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
LLM Advanced Testing Suite - Web Interface Status Check
This script checks the status of the web interface.
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

def check_web_interface_status():
    """Check if web interface is running"""
    print("LLM Advanced Testing Suite - Web Interface Status Check")
    print("=" * 60)
    
    base_url = "http://localhost:8501"
    
    try:
        response = requests.get(f"{base_url}/", timeout=5)
        if response.status_code == 200:
            print("Web interface is running")
            print(f"Response time: {response.elapsed.total_seconds():.2f}s")
            return True
        else:
            print(f"Web interface returned status code: {response.status_code}")
            return False
    except Exception as e:
        print(f"Web interface is not running: {e}")
        return False

def start_web_interface():
    """Start the web interface"""
    print("\nStarting web interface...")
    
    base_url = "http://localhost:8501"
    
    # Check if web interface is already running
    if check_web_interface_status():
        print("Web interface is already running")
        return True
    
    # Start the web interface
    try:
        script_path = project_root / "visual_test_interface.py"
        if not script_path.exists():
            print(f"Web interface script not found: {script_path}")
            return False
        
        # Start the web interface in background
        process = subprocess.Popen(
            [sys.executable, str(script_path)],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            cwd=project_root
        )
        
        # Wait for web interface to start
        print("Waiting for web interface to start...")
        for i in range(30):  # Wait up to 30 seconds
            if check_web_interface_status():
                print("Web interface started successfully")
                return True
            time.sleep(1)
        
        print("Web interface failed to start")
        return False
        
    except Exception as e:
        print(f"Error starting web interface: {e}")
        return False

def test_basic_functionality():
    """Test basic web interface functionality"""
    print("\nTesting basic functionality...")
    
    base_url = "http://localhost:8501"
    test_results = []
    
    # Test 1: Home page
    print("Test 1: Home page")
    try:
        response = requests.get(f"{base_url}/", timeout=10)
        if response.status_code == 200:
            print("PASS: Home page accessible")
            test_results.append({"test": "Home Page", "status": "PASS"})
        else:
            print(f"FAIL: Home page status {response.status_code}")
            test_results.append({"test": "Home Page", "status": "FAIL"})
    except Exception as e:
        print(f"FAIL: Home page error - {e}")
        test_results.append({"test": "Home Page", "status": "FAIL"})
    
    # Test 2: API models
    print("Test 2: API models")
    try:
        response = requests.get(f"{base_url}/api/models", timeout=10)
        if response.status_code == 200:
            print("PASS: API models accessible")
            test_results.append({"test": "API Models", "status": "PASS"})
        else:
            print(f"FAIL: API models status {response.status_code}")
            test_results.append({"test": "API Models", "status": "FAIL"})
    except Exception as e:
        print(f"FAIL: API models error - {e}")
        test_results.append({"test": "API Models", "status": "FAIL"})
    
    # Test 3: API tests
    print("Test 3: API tests")
    try:
        response = requests.get(f"{base_url}/api/tests", timeout=10)
        if response.status_code == 200:
            print("PASS: API tests accessible")
            test_results.append({"test": "API Tests", "status": "PASS"})
        else:
            print(f"FAIL: API tests status {response.status_code}")
            test_results.append({"test": "API Tests", "status": "FAIL"})
    except Exception as e:
        print(f"FAIL: API tests error - {e}")
        test_results.append({"test": "API Tests", "status": "FAIL"})
    
    # Test 4: API results
    print("Test 4: API results")
    try:
        response = requests.get(f"{base_url}/api/results", timeout=10)
        if response.status_code == 200:
            print("PASS: API results accessible")
            test_results.append({"test": "API Results", "status": "PASS"})
        else:
            print(f"FAIL: API results status {response.status_code}")
            test_results.append({"test": "API Results", "status": "FAIL"})
    except Exception as e:
        print(f"FAIL: API results error - {e}")
        test_results.append({"test": "API Results", "status": "FAIL"})
    
    # Summary
    passed = len([r for r in test_results if r["status"] == "PASS"])
    total = len(test_results)
    
    print(f"\nSummary: {passed}/{total} tests passed")
    
    return passed == total

def main():
    """Main function"""
    # Check web interface status
    if not check_web_interface_status():
        print("Web interface is not running")
        
        # Try to start it
        if start_web_interface():
            print("Web interface started successfully")
        else:
            print("Failed to start web interface")
            return False
    
    # Test basic functionality
    success = test_basic_functionality()
    
    if success:
        print("\nAll tests passed!")
        return True
    else:
        print("\nSome tests failed!")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)