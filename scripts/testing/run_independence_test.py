#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
快速运行独立性测试验证
"""

import subprocess
import sys

def main():
    print("🚀 开始验证独立性测试框架修复效果...")
    
    try:
        # 运行测试脚本
        result = subprocess.run(
            [sys.executable, "test_independence_fix.py"],
            capture_output=True,
            text=True,
            encoding='utf-8',
            errors='replace'
        )
        
        print("STDOUT:")
        print(result.stdout)
        
        if result.stderr:
            print("STDERR:")
            print(result.stderr)
        
        if result.returncode == 0:
            print("\n✅ 测试脚本执行成功")
        else:
            print(f"\n⚠️ 测试脚本返回码: {result.returncode}")
        
    except Exception as e:
        print(f"❌ 执行测试时出错: {e}")

if __name__ == "__main__":
    main()