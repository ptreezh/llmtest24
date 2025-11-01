import os
import sys
import subprocess
import time

def stop_existing_services():
    """Stop existing services"""
    print("Stopping existing services...")
    
    try:
        # Stop Python processes
        subprocess.run(['taskkill', '/F', '/IM', 'python.exe'], 
                     capture_output=True, timeout=5)
        print("Python processes stopped")
    except:
        print("No Python processes found")
    
    try:
        # Stop Streamlit processes
        subprocess.run(['taskkill', '/F', '/IM', 'streamlit.exe'], 
                     capture_output=True, timeout=5)
        print("Streamlit processes stopped")
    except:
        print("No Streamlit processes found")
    
    # Wait for processes to stop
    time.sleep(3)
    print("Services stopped successfully")

if __name__ == "__main__":
    stop_existing_services()