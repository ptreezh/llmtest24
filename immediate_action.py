import os
import sys
import subprocess
import time
import requests
from pathlib import Path

def check_visual_interface():
    """Check if visual_test_interface.py exists and can be imported"""
    print("Checking visual_test_interface.py...")
    
    script_path = Path("visual_test_interface.py")
    if not script_path.exists():
        print("ERROR: visual_test_interface.py does not exist")
        return False
    
    print("visual_test_interface.py exists")
    
    # Try to import
    try:
        sys.path.append('.')
        import visual_test_interface
        print("visual_test_interface.py can be imported")
        return True
    except Exception as e:
        print(f"ERROR: Cannot import visual_test_interface.py: {e}")
        return False

def start_service_with_streamlit():
    """Start service using streamlit"""
    print("Starting service with streamlit...")
    
    try:
        cmd = [
            sys.executable, "-m", "streamlit", "run", 
            "visual_test_interface.py",
            "--server.port=8501",
            "--server.headless=true",
            "--server.enableCORS=true"
        ]
        
        print(f"Command: {' '.join(cmd)}")
        
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            cwd=Path(".")
        )
        
        print("Streamlit service started")
        return process
        
    except Exception as e:
        print(f"ERROR: Failed to start streamlit service: {e}")
        return None

def test_service_availability():
    """Test if service is available"""
    print("Testing service availability...")
    
    # Test different URLs
    test_urls = [
        "http://localhost:8501/",
        "http://localhost:8501"
    ]
    
    for url in test_urls:
        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                print(f"SUCCESS: Service is available at {url}")
                return True, url
            else:
                print(f"Response: {url} - {response.status_code}")
        except Exception as e:
            print(f"Connection failed: {url} - {e}")
        
        time.sleep(2)
    
    return False, None

def main():
    print("=== IMMEDIATE ACTION: Start Local Web Service ===")
    
    # Check if visual interface exists
    if not check_visual_interface():
        print("CRITICAL: visual_test_interface.py check failed")
        return False
    
    # Start service
    process = start_service_with_streamlit()
    
    if not process:
        print("CRITICAL: Failed to start service")
        return False
    
    print("Service started, waiting for availability...")
    time.sleep(15)  # Wait for service to start
    
    # Test service
    success, url = test_service_availability()
    
    if success:
        print(f"SUCCESS: Local web service is running at {url}")
        
        # Test basic functionality
        print("\nTesting basic functionality...")
        try:
            response = requests.get(f"{url}/api/models", timeout=5)
            if response.status_code == 200:
                print("SUCCESS: API endpoint /api/models is working")
            else:
                print(f"WARNING: API endpoint response: {response.status_code}")
        except Exception as e:
            print(f"WARNING: API test failed: {e}")
        
        return True
    else:
        print("CRITICAL: Service is not available")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)