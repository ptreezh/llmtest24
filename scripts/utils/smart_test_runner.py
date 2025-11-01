#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
智能测试调度器
根据连通性和测试状态决定需要测试的模型
"""

import os
import sys
import json
import argparse
from datetime import datetime
from typing import Dict, List, Any

# 导入云服务模块
try:
    from cloud_services import (
        check_all_services,
        get_all_models,
        get_available_services,
        call_cloud_service,
        CLOUD_SERVICES
    )
except ImportError as e:
    print(f"❌ 导入cloud_services.py失败: {e}")
    sys.exit(1)

# 测试状态文件路径
TEST_STATUS_FILE = "test_status.json"

def load_test_status() -> Dict[str, Any]:
    """加载测试状态"""
    if os.path.exists(TEST_STATUS_FILE):
        try:
            with open(TEST_STATUS_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            print(f"⚠️ 加载测试状态文件失败: {e}")
            return {"models": {}, "last_update": ""}
    else:
        return {"models": {}, "last_update": ""}

def save_test_status(status: Dict[str, Any]) -> None:
    """保存测试状态"""
    status["last_update"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    try:
        with open(TEST_STATUS_FILE, "w", encoding="utf-8") as f:
            json.dump(status, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"⚠️ 保存测试状态文件失败: {e}")

def test_model(service_name: str, model_name: str, test_prompt: str = None) -> Dict[str, Any]:
    """测试单个模型"""
    result = {
        "success": False,
        "response": "",
        "error": "",
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    
    if not test_prompt:
        test_prompt = CLOUD_SERVICES[service_name]["test_prompt"]
    
    try:
        print(f"  测试模型: {model_name} ({service_name})...")
        response = call_cloud_service(service_name, model_name, test_prompt)
        result["success"] = True
        result["response"] = response
        print(f"  ✅ 测试成功: {response[:100]}...")
    except Exception as e:
        result["error"] = str(e)
        print(f"  ❌ 测试失败: {e}")
    
    return result

def run_tests(services_to_test: List[str] = None) -> None:
    """运行测试"""
    print("🔍 检查云服务连通性...")
    
    # 检查所有服务的连通性
    connectivity_results = check_all_services()
    
    # 加载测试状态
    test_status = load_test_status()
    if "models" not in test_status:
        test_status["models"] = {}
    
    # 确定要测试的服务
    available_services = []
    for service_name, result in connectivity_results.items():
        if result["available"]:
            if services_to_test is None or service_name in services_to_test:
                available_services.append(service_name)
                print(f"✅ {result['name']} 可用，将进行测试")
        else:
            print(f"⏭️  跳过 {result['name']} - 服务不可用")
    
    if not available_services:
        print("❌ 没有可用的服务，测试终止")
        return
    
    # 测试每个可用服务的模型
    for service_name in available_services:
        service_config = CLOUD_SERVICES[service_name]
        print(f"\n🧪 测试 {service_config['name']} 的模型...")
        
        for model_name in service_config["models"]:
            model_key = f"{model_name}-{service_name}"
            
            # 检查是否需要测试该模型
            if model_key in test_status["models"]:
                last_test = test_status["models"][model_key]
                if last_test.get("success", False):
                    print(f"  ⏭️  跳过 {model_name} - 上次测试成功 ({last_test.get('timestamp', 'unknown')})")
                    continue
            
            # 测试模型
            result = test_model(service_name, model_name)
            test_status["models"][model_key] = result
            
            # 保存测试状态
            save_test_status(test_status)
    
    print("\n✅ 所有模型都已测试完成！")

def list_services() -> None:
    """列出所有服务"""
    print("📋 可用服务列表:")
    for service_name, config in CLOUD_SERVICES.items():
        print(f"  - {service_name}: {config['name']}")

def list_models() -> None:
    """列出所有模型"""
    print("📋 所有模型列表:")
    models = get_all_models()
    for model_info in models:
        print(f"  - {model_info['key']}: {model_info['model']} ({CLOUD_SERVICES[model_info['service']]['name']})")

def reset_test_status(models: List[str] = None) -> None:
    """重置测试状态"""
    test_status = load_test_status()
    
    if models is None:
        # 重置所有模型
        test_status["models"] = {}
        print("🔄 已重置所有模型的测试状态")
    else:
        # 重置指定模型
        for model_key in models:
            if model_key in test_status["models"]:
                del test_status["models"][model_key]
                print(f"🔄 已重置模型 {model_key} 的测试状态")
            else:
                print(f"⚠️ 模型 {model_key} 不在测试状态中")
    
    save_test_status(test_status)

def main() -> None:
    """主函数"""
    parser = argparse.ArgumentParser(description="智能测试调度器")
    parser.add_argument("--list-services", action="store_true", help="列出所有服务")
    parser.add_argument("--list-models", action="store_true", help="列出所有模型")
    parser.add_argument("--services", type=str, help="要测试的服务，用逗号分隔")
    parser.add_argument("--reset-all", action="store_true", help="重置所有测试状态")
    parser.add_argument("--reset-models", type=str, help="要重置的模型，用逗号分隔")
    
    args = parser.parse_args()
    
    if args.list_services:
        list_services()
        return
    
    if args.list_models:
        list_models()
        return
    
    if args.reset_all:
        reset_test_status()
        return
    
    if args.reset_models:
        models = args.reset_models.split(",")
        reset_test_status(models)
        return
    
    # 运行测试
    services_to_test = args.services.split(",") if args.services else None
    run_tests(services_to_test)

if __name__ == "__main__":
    main()
