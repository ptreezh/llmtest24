#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Launch Real Web Testing System
启动真实的Web测试系统
"""

import subprocess
import sys
import os
import time
import webbrowser
from pathlib import Path

def check_dependencies():
    """检查依赖"""
    print("检查系统依赖...")
    
    # 检查Python版本
    print(f"Python版本: {sys.version}")
    
    # 检查关键模块
    required_modules = [
        "streamlit",
        "requests", 
        "json",
        "pathlib",
        "pandas",
        "threading",
        "queue"
    ]
    
    missing_modules = []
    for module in required_modules:
        try:
            __import__(module)
            print(f"✓ {module}")
        except ImportError:
            print(f"✗ {module} - 缺失")
            missing_modules.append(module)
    
    if missing_modules:
        print(f"\n缺失的模块: {missing_modules}")
        print("请安装缺失的依赖:")
        print("pip install streamlit requests pandas")
        return False
    
    return True

def check_project_structure():
    """检查项目结构"""
    print("\n检查项目结构...")
    
    required_files = [
        "real_web_testing_system.py",
        "scripts/utils/cloud_services.py",
        "tests/"
    ]
    
    missing_files = []
    for file_path in required_files:
        if Path(file_path).exists():
            print(f"✓ {file_path}")
        else:
            print(f"✗ {file_path} - 缺失")
            missing_files.append(file_path)
    
    if missing_files:
        print(f"\n缺失的文件: {missing_files}")
        return False
    
    return True

def check_api_keys():
    """检查API密钥"""
    print("\n检查API密钥...")
    
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
            print(f"✓ {key} - 已配置")
        else:
            print(f"✗ {key} - 未配置")
    
    print(f"\n可用的API密钥: {len(available_keys)}/{len(api_keys)}")
    
    if len(available_keys) == 0:
        print("⚠️  警告: 没有配置API密钥")
        print("系统将使用演示模式")
        print("要使用真实的LLM模型，请设置环境变量:")
        for key in api_keys:
            print(f"  export {key}=your_api_key")
    
    return True

def launch_web_interface():
    """启动Web界面"""
    print("\n" + "="*60)
    print("🚀 启动真实的LLM测试系统")
    print("="*60)
    
    print("\n系统功能:")
    print("✓ 用户可选择真实的LLM模型")
    print("✓ 用户可选择要执行的测试用例")
    print("✓ 实时显示测试进度和日志")
    print("✓ 支持批量并发测试")
    print("✓ 实时显示测试过程")
    print("✓ 生成详细的测试报告")
    print("✓ 支持下载JSON和CSV格式报告")
    
    print("\n正在启动Web界面...")
    
    try:
        # 设置环境变量避免代理问题
        env = os.environ.copy()
        env['HTTP_PROXY'] = ''
        env['HTTPS_PROXY'] = ''
        env['NO_PROXY'] = 'localhost,127.0.0.1'
        
        # 启动Streamlit应用
        cmd = [
            sys.executable, "-m", "streamlit", "run",
            "real_web_testing_system.py",
            "--server.port", "8501",
            "--server.address", "localhost",
            "--server.headless", "false",
            "--server.fileWatcherType", "auto",
            "--server.runOnSave", "true",
            "--browser.gatherUsageStats", "false"
        ]
        
        print(f"启动命令: {' '.join(cmd)}")
        print("\n正在启动Streamlit服务器...")
        
        # 启动进程
        process = subprocess.Popen(cmd, 
                                env=env,
                                stdout=subprocess.PIPE, 
                                stderr=subprocess.PIPE,
                                cwd=Path(__file__).parent)
        
        print(f"进程已启动，PID: {process.pid}")
        
        # 等待服务启动
        print("等待服务启动...")
        time.sleep(5)
        
        # 检查进程是否仍在运行
        if process.poll() is None:
            print("\n" + "="*60)
            print("🎉 系统启动成功！")
            print("="*60)
            
            print("\n📍 Web界面地址:")
            print("   http://localhost:8501")
            
            print("\n📋 使用说明:")
            print("1. 系统会自动打开浏览器")
            print("2. 在左侧选择LLM模型")
            print("3. 选择要执行的测试用例")
            print("4. 点击'开始测试'")
            print("5. 实时查看测试进度和日志")
            print("6. 测试完成后下载报告")
            
            print("\n🔧 可用功能:")
            print("- 真实LLM模型调用 (如果配置了API密钥)")
            print("- 35个完整测试用例")
            print("- 实时进度监控")
            print("- 测试日志显示")
            print("- 并发测试支持")
            print("- 详细报告生成")
            print("- 多格式下载")
            
            print("\n⚠️  停止系统:")
            print("   - 在浏览器中关闭页面")
            print("   - 在终端按 Ctrl+C")
            
            # 尝试自动打开浏览器
            try:
                time.sleep(2)
                webbrowser.open("http://localhost:8501")
                print("\n✅ 浏览器已自动打开")
            except:
                print("\n⚠️  请手动打开浏览器访问: http://localhost:8501")
            
            print("\n" + "="*60)
            print("🌟 系统正在运行中...")
            print("请在浏览器中与系统进行交互！")
            print("="*60)
            
            try:
                # 等待用户中断
                process.wait()
            except KeyboardInterrupt:
                print("\n\n🛑 正在停止系统...")
                process.terminate()
                try:
                    process.wait(timeout=10)
                    print("✅ 系统已停止")
                except:
                    try:
                        process.kill()
                        print("✅ 系统已强制停止")
                    except:
                        print("⚠️  无法停止进程，请手动结束")
            
            return True
        else:
            print("\n❌ 服务启动失败")
            try:
                stderr = process.stderr.read().decode('utf-8', errors='ignore')
                if stderr:
                    print(f"错误信息: {stderr}")
            except:
                pass
            return False
            
    except Exception as e:
        print(f"\n❌ 启动失败: {e}")
        return False

def main():
    """主函数"""
    print("🧪 LLM Complete Testing System - 真实Web版本")
    print("="*50)
    
    # 检查系统
    print("正在检查系统环境...")
    
    if not check_dependencies():
        print("\n❌ 依赖检查失败")
        print("请安装必要的Python包:")
        print("pip install streamlit requests pandas")
        return False
    
    if not check_project_structure():
        print("\n❌ 项目结构检查失败")
        print("请确保所有必要的文件都存在")
        return False
    
    if not check_api_keys():
        print("\n⚠️  API密钥检查完成")
        print("系统将继续启动，可能使用演示模式")
    
    # 启动系统
    return launch_web_interface()

if __name__ == "__main__":
    success = main()
    
    if success:
        print("\n🎊 感谢使用LLM Complete Testing System!")
    else:
        print("\n❌ 系统启动失败，请检查错误信息")
    
    sys.exit(0 if success else 1)