import os
import sys
import subprocess
import time
import requests
from pathlib import Path

def start_local_web_service():
    """Start local web service"""
    print("Starting local web service...")
    
    try:
        # Start visual_test_interface.py
        cmd = [
            sys.executable, "visual_test_interface.py"
        ]
        
        print(f"Executing command: {' '.join(cmd)}")
        
        # Start service
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            cwd=Path(".")
        )
        
        print("Service start command executed")
        return process
        
    except Exception as e:
        print(f"Failed to start service: {e}")
        return None

def wait_for_service():
    """Wait for service to be ready"""
    print("Waiting for service to be ready...")
    
    for i in range(30):  # Wait up to 30 seconds
        try:
            response = requests.get("http://localhost/", timeout=5)
            if response.status_code == 200:
                print("Service is ready!")
                return True
            else:
                print(f"Service response: {response.status_code}")
        except:
            print(f"Waiting... ({i+1}/30)")
        
        time.sleep(1)
    
    print("Service start timeout")
    return False

def main():
    print("=== Step 2: Start Local Web Service ===")
    
    # Start service
    process = start_local_web_service()
    
    if process:
        print("Service started successfully, waiting for service to be ready...")
        time.sleep(10)  # Initial wait
        
        # Check if service is ready
        if wait_for_service():
            print("SUCCESS: Local web service is running!")
            return True
        else:
            print("FAIL: Service start timeout")
            return False
    else:
        print("FAIL: Failed to start service")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)