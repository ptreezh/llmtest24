#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
测试状态管理工具
用于重置、查看和管理测试状态
"""

import os
import sys
import json
import argparse
from datetime import datetime
from typing import List, Dict, Optional

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from cloud_services import CLOUD_SERVICES, get_all_models

# 测试状态文件路径
TEST_STATUS_FILE = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "test_status.json")

def load_test_status() -> Dict:
    """加载测试状态"""
    try:
        if os.path.exists(TEST_STATUS_FILE):
            with open(TEST_STATUS_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        else:
            return {"tested_models": [], "last_update": None}
    except Exception as e:
        print(f"⚠️ 加载测试状态失败: {e}")
        return {"tested_models": [], "last_update": None}

def save_test_status(status: Dict) -> None:
    """保存测试状态"""
    status["last_update"] = datetime.now().isoformat()
    try:
        with open(TEST_STATUS_FILE, "w", encoding="utf-8") as f:
            json.dump(status, f, indent=2)
    except Exception as e:
        print(f"⚠️ 保存测试状态失败: {e}")

def reset_all_status() -> None:
    """重置所有测试状态"""
    save_test_status({"tested_models": [], "last_update": None})
    print("✅ 已重置所有测试状态")

def reset_service_status(service_name: str) -> None:
    """重置指定服务的测试状态"""
    if service_name not in CLOUD_SERVICES:
        print(f"❌ 未知服务: {service_name}")
        return
    
    status = load_test_status()
    
    # 找出该服务的所有模型
    service_models = []
    for model in CLOUD_SERVICES[service_name]["models"]:
        service_models.append(f"{model}-{service_name}")
    
    # 从已测试列表中移除
    new_tested_models = [m for m in status["tested_models"] if not m.endswith(f"-{service_name}")]
    
    # 保存新状态
    status["tested_models"] = new_tested_models
    save_test_status(status)
    
    removed_count = len(status["tested_models"]) - len(new_tested_models)
    print(f"✅ 已重置 {CLOUD_SERVICES[service_name]['name']} 的测试状态 (移除了 {removed_count} 个模型)")

def reset_model_status(model_key: str) -> None:
    """重置指定模型的测试状态"""
    status = load_test_status()
    
    if model_key in status["tested_models"]:
        status["tested_models"].remove(model_key)
        save_test_status(status)
        print(f"✅ 已重置模型 {model_key} 的测试状态")
    else:
        print(f"ℹ️ 模型 {model_key} 尚未被测试")

def show_test_status() -> None:
    """显示当前测试状态"""
    status = load_test_status()
    
    print("📊 当前测试状态:")
    
    if status["last_update"]:
        print(f"最后更新: {status['last_update']}")
    
    # 获取所有可能的模型
    all_models = get_all_models()
    all_model_keys = [m["key"] for m in all_models]
    
    # 计算测试进度
    tested_count = len(status["tested_models"])
    total_count = len(all_model_keys)
    progress = tested_count / total_count * 100 if total_count > 0 else 0
    
    print(f"测试进度: {tested_count}/{total_count} ({progress:.1f}%)")
    
    # 按服务分组显示
    for service_name, config in CLOUD_SERVICES.items():
        service_models = [m for m in all_models if m["service"] == service_name]
        service_tested = [m for m in service_models if m["key"] in status["tested_models"]]
        
        service_progress = len(service_tested) / len(service_models) * 100 if service_models else 0
        
        print(f"\n{config['name']} ({service_name}):")
        print(f"  进度: {len(service_tested)}/{len(service_models)} ({service_progress:.1f}%)")
        
        for model in service_models:
            status_icon = "✅" if model["key"] in status["tested_models"] else "⏳"
            print(f"  {status_icon} {model['model']}")

def main():
    """主函数"""
    parser = argparse.ArgumentParser(description="测试状态管理工具")
    parser.add_argument("--reset-all", action="store_true", help="重置所有测试状态")
    parser.add_argument("--reset-service", type=str, help="重置指定服务的测试状态")
    parser.add_argument("--reset-model", type=str, help="重置指定模型的测试状态")
    parser.add_argument("--show", action="store_true", help="显示当前测试状态")
    
    args = parser.parse_args()
    
    # 默认显示状态
    if not (args.reset_all or args.reset_service or args.reset_model):
        args.show = True
    
    if args.reset_all:
        reset_all_status()
    
    if args.reset_service:
        reset_service_status(args.reset_service)
    
    if args.reset_model:
        reset_model_status(args.reset_model)
    
    if args.show:
        show_test_status()

if __name__ == "__main__":
    main()