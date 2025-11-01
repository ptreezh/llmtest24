#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
测试cloud_services.py模块
"""

try:
    from cloud_services import (
        check_all_services, 
        get_all_models,
        get_available_services,
        CLOUD_SERVICES
    )
    print("✅ cloud_services.py 导入成功")
except ImportError as e:
    print(f"❌ cloud_services.py 导入失败: {e}")
    exit(1)

def test_cloud_services():
    """测试云服务模块"""
    print("🔍 测试云服务模块...")
    
    # 测试获取可用服务
    print("\n📋 可用服务:")
    services = get_available_services()
    for service in services:
        config = CLOUD_SERVICES[service]
        print(f"  - {service}: {config['name']}")
    
    # 测试获取所有模型
    print("\n📋 所有模型:")
    models = get_all_models()
    for model_info in models[:5]:  # 只显示前5个
        print(f"  - {model_info['key']}")
    print(f"  ... 总共 {len(models)} 个模型")
    
    # 测试连通性检查
    print("\n🔍 检查服务连通性:")
    results = check_all_services()
    
    output = ""
    for service_name, result in results.items():
        status = "✅ 可用" if result["available"] else "❌ 不可用"
        output += f"  {result['name']}: {status}\n"
        if not result["available"]:
            output += f"    原因: {result['reason']}\n"
    
    return output

if __name__ == "__main__":
    output = test_cloud_services()
    with open("cloud_test_results.txt", "w", encoding="utf-8") as f:
        f.write(output)
