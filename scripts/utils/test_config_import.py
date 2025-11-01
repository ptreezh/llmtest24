#!/usr/bin/env python3
"""测试配置导入"""

try:
    print("🔍 测试配置导入...")
    from config import MODEL_TO_TEST
    print(f"✅ MODEL_TO_TEST: {MODEL_TO_TEST}")
    
    from config import DEFAULT_OPTIONS_CREATIVE
    print(f"✅ DEFAULT_OPTIONS_CREATIVE: {DEFAULT_OPTIONS_CREATIVE}")
    
    try:
        from config import MODELS_LIST_FILE
        print(f"✅ MODELS_LIST_FILE: {MODELS_LIST_FILE}")
    except ImportError:
        print("⚠️ MODELS_LIST_FILE 不存在")
    
    from config import OLLAMA_HOST
    print(f"✅ OLLAMA_HOST: {OLLAMA_HOST}")
    
    print("🎉 基本配置导入成功！")
    
except ImportError as e:
    print(f"❌ 导入错误: {e}")
    
    # 显示config.py中实际可用的属性
    try:
        import config
        print("📋 config.py中可用的属性:")
        for attr in dir(config):
            if not attr.startswith('_'):
                print(f"  - {attr}")
    except Exception as e2:
        print(f"❌ 无法导入config模块: {e2}")