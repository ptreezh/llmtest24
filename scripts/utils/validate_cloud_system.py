#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
云LLM服务扩展系统验证脚本
检查所有组件是否正常工作
"""

import os
import sys
import json
from datetime import datetime

def check_file_exists(filepath: str, description: str) -> bool:
    """检查文件是否存在"""
    if os.path.exists(filepath):
        print(f"✅ {description}: {filepath}")
        return True
    else:
        print(f"❌ {description}: {filepath} (不存在)")
        return False

def validate_cloud_services():
    """验证云服务配置"""
    try:
        from cloud_services import CLOUD_SERVICES, check_all_services
        
        print(f"✅ 云服务配置加载成功，共 {len(CLOUD_SERVICES)} 个服务")
        
        # 列出所有服务
        for service_name, config in CLOUD_SERVICES.items():
            print(f"  - {config['name']} ({service_name}): {len(config['models'])} 个模型")
        
        return True
    except Exception as e:
        print(f"❌ 云服务配置验证失败: {e}")
        return False

def validate_smart_runner():
    """验证智能测试调度器"""
    try:
        from smart_test_runner import load_test_status, get_models_to_test
        
        # 测试状态加载
        status = load_test_status()
        print(f"✅ 测试状态加载成功，已测试 {len(status['tested_models'])} 个模型")
        
        return True
    except Exception as e:
        print(f"❌ 智能测试调度器验证失败: {e}")
        return False

def validate_status_tool():
    """验证状态管理工具"""
    try:
        sys.path.insert(0, 'tools')
        from reset_test_status import load_test_status as tool_load_status
        
        status = tool_load_status()
        print(f"✅ 状态管理工具验证成功")
        
        return True
    except Exception as e:
        print(f"❌ 状态管理工具验证失败: {e}")
        return False

def main():
    """主验证函数"""
    print("🔍 云LLM服务扩展系统验证")
    print("="*50)
    
    # 检查核心文件
    print("\n📁 检查核心文件:")
    files_ok = True
    files_ok &= check_file_exists("cloud_services.py", "云服务配置文件")
    files_ok &= check_file_exists("smart_test_runner.py", "智能测试调度器")
    files_ok &= check_file_exists("test_status.json", "测试状态文件")
    files_ok &= check_file_exists("tools/reset_test_status.py", "状态管理工具")
    files_ok &= check_file_exists("enhanced_test_runner.py", "增强测试运行器")
    files_ok &= check_file_exists(".env.example", "环境变量示例")
    files_ok &= check_file_exists("docs/simple_cloud_guide.md", "使用指南")
    
    if not files_ok:
        print("\n❌ 部分核心文件缺失，请检查安装")
        return False
    
    # 验证功能模块
    print("\n🧪 验证功能模块:")
    modules_ok = True
    modules_ok &= validate_cloud_services()
    modules_ok &= validate_smart_runner()
    modules_ok &= validate_status_tool()
    
    if not modules_ok:
        print("\n❌ 部分功能模块验证失败")
        return False
    
    # 检查环境变量配置
    print("\n🔑 检查环境变量配置:")
    env_file_exists = os.path.exists(".env")
    if env_file_exists:
        print("✅ .env 文件存在")
    else:
        print("⚠️ .env 文件不存在，请复制 .env.example 并配置API密钥")
    
    print("\n🎉 系统验证完成！")
    
    if env_file_exists:
        print("\n📋 下一步操作:")
        print("1. 配置 .env 文件中的API密钥")
        print("2. 运行: python smart_test_runner.py --list-services")
        print("3. 运行: python smart_test_runner.py")
    else:
        print("\n📋 下一步操作:")
        print("1. 复制 .env.example 为 .env")
        print("2. 在 .env 中配置您的API密钥")
        print("3. 运行: python smart_test_runner.py")
    
    return True

if __name__ == "__main__":
    main()