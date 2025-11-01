#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Complete LLM Testing System Launcher
完整的LLM测试系统启动器
"""

import subprocess
import sys
import os
import time
from pathlib import Path

def check_dependencies():
    """检查依赖"""
    print("Checking dependencies...")
    
    # 检查Python版本
    print(f"Python version: {sys.version}")
    
    # 检查关键模块
    required_modules = [
        "streamlit",
        "requests", 
        "json",
        "pathlib",
        "pandas"
    ]
    
    missing_modules = []
    for module in required_modules:
        try:
            __import__(module)
            print(f"✓ {module} available")
        except ImportError:
            print(f"✗ {module} missing")
            missing_modules.append(module)
    
    if missing_modules:
        print(f"\nMissing modules: {missing_modules}")
        print("Please install missing dependencies:")
        print("pip install streamlit requests pandas")
        return False
    
    return True

def check_project_structure():
    """检查项目结构"""
    print("\nChecking project structure...")
    
    required_files = [
        "complete_web_testing_system.py",
        "enhanced_test_executor.py",
        "scripts/utils/cloud_services.py",
        "tests/"
    ]
    
    missing_files = []
    for file_path in required_files:
        if Path(file_path).exists():
            print(f"✓ {file_path}")
        else:
            print(f"✗ {file_path} missing")
            missing_files.append(file_path)
    
    if missing_files:
        print(f"\nMissing files: {missing_files}")
        return False
    
    return True

def check_api_keys():
    """检查API密钥"""
    print("\nChecking API keys...")
    
    api_keys = [
        'TOGETHER_API_KEY',
        'OPENROUTER_API_KEY', 
        'PPINFRA_API_KEY',
        'GEMINI_API_KEY'
    ]
    
    available_keys = []
    for key in api_keys:
        if os.getenv(key):
            available_keys.append(key)
            print(f"✓ {key} configured")
        else:
            print(f"✗ {key} not configured")
    
    print(f"\nAvailable API keys: {len(available_keys)}/{len(api_keys)}")
    
    if len(available_keys) == 0:
        print("WARNING: No API keys configured. System will run in simulation mode.")
        print("Please set up API keys in your environment variables.")
    
    return True

def launch_web_interface():
    """启动Web界面"""
    print("\n" + "="*60)
    print(" LAUNCHING COMPLETE LLM TESTING SYSTEM")
    print("="*60)
    
    print("\nSystem Features:")
    print("✓ Real LLM model selection (17+ models available)")
    print("✓ Complete test execution (35 test cases)")
    print("✓ Real-time progress monitoring")
    print("✓ Detailed result analysis")
    print("✓ Report download (JSON/CSV)")
    print("✓ Batch testing script generation")
    print("✓ Web-based interface")
    
    print("\nStarting web interface...")
    print("Please wait for the system to initialize...")
    
    try:
        # 启动Streamlit应用
        cmd = [
            sys.executable, "-m", "streamlit", "run",
            "complete_web_testing_system.py",
            "--server.port", "8501",
            "--server.address", "localhost",
            "--server.headless", "false",
            "--server.fileWatcherType", "auto",
            "--theme.primaryColor", "#1E88E5",
            "--theme.backgroundColor", "#FFFFFF",
            "--theme.secondaryBackgroundColor", "#F0F2F6"
        ]
        
        print(f"Command: {' '.join(cmd)}")
        print("\nStarting Streamlit server...")
        
        # 启动进程
        process = subprocess.Popen(cmd, 
                                stdout=subprocess.PIPE, 
                                stderr=subprocess.PIPE,
                                cwd=Path(__file__).parent)
        
        print(f"Process started with PID: {process.pid}")
        
        # 等待服务启动
        print("Waiting for service to start (15 seconds)...")
        time.sleep(15)
        
        # 检查进程是否仍在运行
        if process.poll() is None:
            print("\n" + "="*60)
            print(" SYSTEM STARTED SUCCESSFULLY!")
            print("="*60)
            print("\n📍 Web Interface:")
            print("   http://localhost:8501")
            print("\n📋 Quick Start:")
            print("1. Open your web browser")
            print("2. Go to http://localhost:8501")
            print("3. Select a model from the sidebar")
            print("4. Choose test cases to run")
            print("5. Click 'Start Testing'")
            print("6. Monitor real-time progress")
            print("7. Download results when complete")
            print("\n🔧 Available Commands:")
            print("- Single test: python tests/test_pillar_01_logic.py [model]")
            print("- Batch test: python run_comprehensive_tests.py")
            print("- Real LLM test: python test_real_llm.py")
            print("\n⚠️  To stop the server:")
            print("   Press Ctrl+C in this terminal")
            print("\n" + "="*60)
            
            try:
                # 等待用户中断
                process.wait()
            except KeyboardInterrupt:
                print("\n\n🛑 Stopping server...")
                process.terminate()
                process.wait(timeout=10)
                print("✓ Server stopped")
            
            return True
        else:
            print("\n❌ Server failed to start")
            stderr = process.stderr.read().decode('utf-8', errors='ignore')
            if stderr:
                print(f"Error: {stderr}")
            return False
            
    except Exception as e:
        print(f"\n❌ Failed to launch web interface: {e}")
        return False

def main():
    """主函数"""
    print("LLM Complete Testing System")
    print("="*50)
    
    # 检查系统
    if not check_dependencies():
        print("\n❌ Dependency check failed")
        return False
    
    if not check_project_structure():
        print("\n❌ Project structure check failed")
        return False
    
    if not check_api_keys():
        print("\n⚠️  API key check showed warnings, but continuing...")
    
    # 启动系统
    return launch_web_interface()

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)