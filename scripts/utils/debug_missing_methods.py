#!/usr/bin/env python3
"""检查缺少的方法"""

import sys
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

try:
    from independence.experiments.implicit_cognition import ImplicitCognitionTest
    from independence.experiments.longitudinal_consistency import LongitudinalConsistencyTest
    
    print("🔍 检查ImplicitCognitionTest类...")
    cognition_test = ImplicitCognitionTest({'model_name': 'test'})
    methods = [method for method in dir(cognition_test) if not method.startswith('_')]
    print(f"可用方法: {methods}")
    
    if hasattr(cognition_test, '_run_bias_detection'):
        print("✅ _run_bias_detection 方法存在")
    else:
        print("❌ _run_bias_detection 方法缺失")
    
    print("\n🔍 检查LongitudinalConsistencyTest类...")
    consistency_test = LongitudinalConsistencyTest({'model_name': 'test'})
    methods = [method for method in dir(consistency_test) if not method.startswith('_')]
    print(f"可用方法: {methods}")
    
    if hasattr(consistency_test, '_execute_conversation_turn'):
        print("✅ _execute_conversation_turn 方法存在")
    else:
        print("❌ _execute_conversation_turn 方法缺失")
        
except Exception as e:
    print(f"❌ 检查失败: {e}")
    import traceback
    traceback.print_exc()