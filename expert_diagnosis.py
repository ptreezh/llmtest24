#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
专家级网络诊断脚本
"""

import os
import sys
import subprocess
import socket
import requests
import time
from pathlib import Path

def check_port_usage():
    """检查端口使用情况"""
    print("=== 端口使用情况检查 ===")
    
    try:
        # 检查端口8501是否被占用
        result = subprocess.run(['netstat', '-an', '|', 'findstr', ':8501'], 
                              capture_output=True, text=True, shell=True)
        if result.returncode == 0:
            print("⚠️ 端口8501被占用:")
            print(result.stdout)
        else:
            print("✅ 端口8501未被占用")
    except:
        print("❌ 无法检查端口使用情况")

def check_firewall():
    """检查防火墙设置"""
    print("\n=== 防火墙设置检查 ===")
    
    try:
        result = subprocess.run(['Get-NetFirewallRule', '-DisplayName', '*Streamlit*'], 
                              capture_output=True, text=True, shell=True)
        if result.returncode == 0:
            print("✅ Streamlit防火墙规则存在")
        else:
            print("⚠️ 未找到Streamlit防火墙规则")
    except:
        print("❌ 无法检查防火墙设置")

def test_local_connection():
    """测试本地连接"""
    print("\n=== 本地连接测试 ===")
    
    try:
        # 测试本地连接
        response = requests.get("http://localhost:8501/", timeout=5)
        print(f"✅ 本地连接成功 - 状态码: {response.status_code}")
        return True
    except requests.exceptions.ConnectionError:
        print("❌ 本地连接失败 - 连接被拒绝")
        return False
    except requests.exceptions.Timeout:
        print("❌ 本地连接超时")
        return False
    except Exception as e:
        print(f"❌ 本地连接错误: {e}")
        return False

def check_streamlit_process():
    """检查Streamlit进程"""
    print("\n=== Streamlit进程检查 ===")
    
    try:
        result = subprocess.run(['tasklist', '|', 'findstr', 'streamlit'], 
                              capture_output=True, text=True, shell=True)
        if result.returncode == 0:
            print("⚠️ 发现Streamlit进程:")
            print(result.stdout)
        else:
            print("✅ 未发现Streamlit进程")
    except:
        print("❌ 无法检查Streamlit进程")

def main():
    """主函数"""
    print("🔍 LLM Advanced Testing Suite - 专家级网络诊断")
    print("=" * 60)
    
    # 执行各项检查
    check_port_usage()
    check_firewall()
    test_local_connection()
    check_streamlit_process()
    
    print("\n=== 诊断完成 ===")

if __name__ == "__main__":
    main()