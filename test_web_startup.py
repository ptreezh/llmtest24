#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Web interface startup test for LLM Advanced Testing Suite
"""

import sys
import time
import subprocess
import requests
from pathlib import Path

def test_web_interface_startup():
    """Test web interface startup"""
    print("LLM Advanced Testing Suite - Web Interface Startup Test")
    print("=" * 60)
    
    # Check if visual_test_interface.py exists
    script_path = Path("visual_test_interface.py")
    if not script_path.exists():
        print("ERROR: visual_test_interface.py not found")
        return False
    
    print("OK: visual_test_interface.py found")
    
    # Check if all dependencies are available
    try:
        import streamlit
        import pandas
        import numpy
        import matplotlib
        import seaborn
        import pydantic
        import requests
        import yaml
        import dotenv
        print("OK: All dependencies are available")
    except ImportError as e:
        print(f"ERROR: Missing dependency: {e}")
        return False
    
    # Try to start the web interface
    print("\nStarting web interface...")
    try:
        # Start the web interface in background
        process = subprocess.Popen(
            [sys.executable, "visual_test_interface.py"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            cwd=Path(".")
        )
        
        # Wait for web interface to start
        print("Waiting for web interface to start...")
        for i in range(30):  # Wait up to 30 seconds
            try:
                response = requests.get("http://localhost:8501/", timeout=5)
                if response.status_code == 200:
                    print("SUCCESS: Web interface started successfully")
                    print(f"Response time: {response.elapsed.total_seconds():.2f}s")
                    
                    # Test a few endpoints
                    print("\nTesting API endpoints...")
                    endpoints = ["/api/models", "/api/tests", "/api/results"]
                    for endpoint in endpoints:
                        try:
                            response = requests.get(f"http://localhost:8501{endpoint}", timeout=5)
                            if response.status_code == 200:
                                print(f"OK: {endpoint} - {response.status_code}")
                            else:
                                print(f"WARNING: {endpoint} - {response.status_code}")
                        except:
                            print(f"ERROR: {endpoint} - Connection failed")
                    
                    # Stop the web interface
                    process.terminate()
                    process.wait(timeout=5)
                    print("Web interface stopped")
                    
                    return True
            except requests.exceptions.ConnectionError:
                pass
            time.sleep(1)
        
        print("ERROR: Web interface failed to start")
        process.terminate()
        return False
        
    except Exception as e:
        print(f"ERROR: Failed to start web interface: {e}")
        return False

def main():
    """Main function"""
    success = test_web_interface_startup()
    
    if success:
        print("\nWeb interface startup test PASSED!")
        print("The web interface is ready to use.")
        return True
    else:
        print("\nWeb interface startup test FAILED!")
        print("Please check the error messages above.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)