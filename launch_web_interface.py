#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Web Interface Launcher
启动web界面的自动化脚本
"""

import subprocess
import sys
import time
import os
from pathlib import Path

def launch_web_interface():
    """启动web界面"""
    print("Starting Web Interface...")
    print("=" * 40)
    
    # 检查web界面文件
    web_interface = Path("visual_test_interface.py")
    if not web_interface.exists():
        print("FAIL: visual_test_interface.py not found")
        return False
    
    # 启动web界面
    try:
        print("Launching Streamlit web interface...")
        process = subprocess.Popen([
            sys.executable, "-m", "streamlit", "run", 
            "visual_test_interface.py",
            "--server.port", "8502",  # 使用8502端口避免冲突
            "--server.address", "localhost",
            "--server.headless", "true",
            "--server.fileWatcherType", "none"
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        print(f"Web interface process started with PID: {process.pid}")
        
        # 等待服务启动
        print("Waiting for web interface to start...")
        time.sleep(10)
        
        # 检查进程是否仍在运行
        if process.poll() is None:
            print("SUCCESS: Web interface is running")
            print("Access at: http://localhost:8502")
            print("Press Ctrl+C to stop the server")
            
            try:
                # 保持进程运行
                process.wait()
            except KeyboardInterrupt:
                print("\nStopping web interface...")
                process.terminate()
                process.wait()
                print("Web interface stopped")
            
            return True
        else:
            print("FAIL: Web interface process stopped unexpectedly")
            stderr = process.stderr.read().decode('utf-8', errors='ignore')
            if stderr:
                print(f"Error: {stderr}")
            return False
            
    except Exception as e:
        print(f"FAIL: Failed to start web interface: {e}")
        return False

if __name__ == "__main__":
    success = launch_web_interface()
    sys.exit(0 if success else 1)