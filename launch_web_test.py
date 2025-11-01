#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Web Test Launcher - Final Launch Script
最终的web测试启动脚本
"""

import subprocess
import sys
import time
import os
from pathlib import Path

def main():
    """主启动函数"""
    print("=" * 60)
    print("LLM Advanced Testing Suite - Web Interface Launcher")
    print("=" * 60)
    print()
    
    # 显示系统状态
    print("System Status Check:")
    print("-" * 30)
    
    # 检查关键文件
    critical_files = [
        "visual_test_interface.py",
        "tests/config.py", 
        "core/framework.py",
        "core/model_manager.py"
    ]
    
    all_files_ok = True
    for file_path in critical_files:
        if Path(file_path).exists():
            print(f"✓ {file_path}")
        else:
            print(f"✗ {file_path} - MISSING")
            all_files_ok = False
    
    if not all_files_ok:
        print("\nERROR: Critical files missing!")
        return False
    
    # 检查依赖
    print("\nDependencies Check:")
    print("-" * 30)
    try:
        import streamlit
        print(f"✓ Streamlit {streamlit.__version__}")
        import requests
        print("✓ Requests")
        import yaml
        print("✓ YAML")
        import json
        print("✓ JSON")
    except ImportError as e:
        print(f"✗ Missing dependency: {e}")
        return False
    
    print("\n" + "=" * 60)
    print("STARTING WEB INTERFACE")
    print("=" * 60)
    print()
    
    # 启动说明
    print("Instructions:")
    print("1. Web interface will start automatically")
    print("2. Access it in your browser at the shown URL")
    print("3. Use Ctrl+C to stop the server")
    print("4. Close this window to exit")
    print()
    
    # 启动web界面
    try:
        print("Launching Streamlit...")
        print("-" * 30)
        
        # 使用streamlit命令启动
        subprocess.run([
            sys.executable, "-m", "streamlit", "run",
            "visual_test_interface.py",
            "--server.port", "8501",
            "--server.address", "localhost",
            "--server.headless", "false",  # 显示浏览器
            "--server.fileWatcherType", "auto"
        ])
        
    except KeyboardInterrupt:
        print("\n\nWeb interface stopped by user")
    except Exception as e:
        print(f"\n\nError starting web interface: {e}")
        return False
    
    return True

if __name__ == "__main__":
    success = main()
    if not success:
        print("\nPress Enter to exit...")
        try:
            input()
        except:
            pass
    sys.exit(0 if success else 1)