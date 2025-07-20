#!/usr/bin/env python3
"""
工作空间快速初始化脚本
"""

import os
import subprocess
import sys
from pathlib import Path

def print_banner():
    print("""
╔══════════════════════════════════════════════════════════════╗
║                    🚀 AI Develop 工作空间                    ║
║                      快速初始化完成                          ║
╠══════════════════════════════════════════════════════════════╣
║  📁 paper_crew                - AI论文研究自动化系统         ║
║  📁 llm-role-independence-test - LLM角色独立性测试框架       ║
╚══════════════════════════════════════════════════════════════╝
    """)

def install_test_framework():
    """安装独立性测试框架"""
    test_path = Path("../llm-role-independence-test")
    if test_path.exists():
        print("🔧 安装独立性测试框架...")
        try:
            subprocess.run([sys.executable, "-m", "pip", "install", "-e", "."], 
                         cwd=test_path, check=True)
            print("✅ 独立性测试框架安装完成")
            return True
        except subprocess.CalledProcessError:
            print("⚠️ 独立性测试框架安装失败")
            return False
    else:
        print("⚠️ 未找到独立性测试框架目录")
        return False

def install_paper_crew_deps():
    """安装Paper Crew依赖"""
    print("🔧 安装Paper Crew依赖...")
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], 
                     check=True)
        print("✅ Paper Crew依赖安装完成")
        return True
    except subprocess.CalledProcessError:
        print("⚠️ Paper Crew依赖安装失败")
        return False

def run_validation():
    """运行验证测试"""
    print("🧪 运行系统验证...")
    
    # 测试CLI
    try:
        result = subprocess.run([sys.executable, "cli.py", "status"], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ CLI工具验证成功")
        else:
            print("⚠️ CLI工具验证失败")
    except Exception as e:
        print(f"⚠️ CLI验证异常: {e}")
    
    # 测试独立性测试
    try:
        result = subprocess.run([sys.executable, "cli.py", "check-roles"], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ 角色配置验证成功")
        else:
            print("⚠️ 角色配置验证失败")
    except Exception as e:
        print(f"⚠️ 角色验证异常: {e}")

def print_next_steps():
    """打印后续步骤"""
    print("""
╔══════════════════════════════════════════════════════════════╗
║                    🎉 初始化完成！                           ║
╠══════════════════════════════════════════════════════════════╣
║                    📋 下一步操作                             ║
╚══════════════════════════════════════════════════════════════╝

🚀 开始使用Paper Crew:
   python cli.py status
   python main.py

🧪 测试角色独立性:
   python cli.py test-independence

🔬 使用测试框架:
   cd ../llm-role-independence-test
   lrit test --system paper_crew

📚 查看文档:
   cat README.md

🎯 祝你在AI开发之路上取得成功！
    """)

def main():
    """主函数"""
    print_banner()
    
    # 安装依赖
    paper_success = install_paper_crew_deps()
    test_success = install_test_framework()
    
    if paper_success and test_success:
        print("\n✅ 所有依赖安装完成")
        run_validation()
    else:
        print("\n⚠️ 部分依赖安装失败，但系统仍可使用")
    
    print_next_steps()

if __name__ == "__main__":
    main()