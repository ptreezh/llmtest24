#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
编码问题修复脚本
修复测试脚本中可能出现的Unicode编码问题
"""

import os
import re
import sys
import subprocess
from typing import List, Tuple

def fix_subprocess_calls(file_path: str) -> bool:
    """修复文件中的subprocess调用，添加编码错误处理"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # 查找subprocess.run调用
        pattern = r'subprocess\.run\([^)]+\)'
        matches = re.findall(pattern, content)
        
        for match in matches:
            # 检查是否已经有errors='replace'
            if "errors='replace'" not in match and "errors=\"replace\"" not in match:
                # 添加errors='replace'参数
                if 'encoding=' in match:
                    # 在encoding参数后添加errors参数
                    new_match = re.sub(
                        r"encoding='([^']+)'", 
                        r"encoding='\1', errors='replace'", 
                        match
                    )
                    new_match = re.sub(
                        r'encoding="([^"]+)"', 
                        r'encoding="\1", errors="replace"', 
                        new_match
                    )
                else:
                    # 如果没有encoding参数，添加完整的编码设置
                    new_match = match.rstrip(')') + ", encoding='utf-8', errors='replace')"
                
                content = content.replace(match, new_match)
        
        # 如果内容有变化，写回文件
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        
        return False
        
    except Exception as e:
        print(f"修复文件 {file_path} 时出错: {e}")
        return False

def add_encoding_error_handling(file_path: str) -> bool:
    """为文件添加编码错误处理"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # 检查是否已经有UnicodeDecodeError处理
        if 'UnicodeDecodeError' not in content:
            # 在except Exception之前添加UnicodeDecodeError处理
            pattern = r'(\s+)except Exception as (\w+):'
            replacement = r'\1except UnicodeDecodeError as ude:\n\1    print(f"[ENCODING ERROR] {p[\'case\'] if \'p\' in locals() else \'unknown\'}: Unicode解码错误 - {ude}")\n\1except Exception as \2:'
            
            content = re.sub(pattern, replacement, content)
        
        # 如果内容有变化，写回文件
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        
        return False
        
    except Exception as e:
        print(f"为文件 {file_path} 添加编码处理时出错: {e}")
        return False

def fix_file_operations(file_path: str) -> bool:
    """修复文件操作，确保使用正确的编码"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # 查找open()调用，确保有encoding参数
        pattern = r"open\([^)]+\)"
        matches = re.findall(pattern, content)
        
        for match in matches:
            if "encoding=" not in match and "'r'" in match or '"r"' in match:
                # 为读取操作添加encoding
                new_match = match.rstrip(')') + ", encoding='utf-8'"
                if "errors=" not in match:
                    new_match += ", errors='replace'"
                new_match += ")"
                content = content.replace(match, new_match)
        
        # 如果内容有变化，写回文件
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        
        return False
        
    except Exception as e:
        print(f"修复文件操作 {file_path} 时出错: {e}")
        return False

def scan_and_fix_tests() -> List[Tuple[str, bool]]:
    """扫描并修复所有测试文件"""
    tests_dir = "tests"
    results = []
    
    if not os.path.exists(tests_dir):
        print(f"测试目录 {tests_dir} 不存在")
        return results
    
    for filename in os.listdir(tests_dir):
        if filename.startswith("test_pillar_") and filename.endswith(".py"):
            file_path = os.path.join(tests_dir, filename)
            print(f"\n检查文件: {filename}")
            
            # 修复subprocess调用
            subprocess_fixed = fix_subprocess_calls(file_path)
            if subprocess_fixed:
                print(f"  ✅ 修复了subprocess调用")
            
            # 添加编码错误处理
            error_handling_added = add_encoding_error_handling(file_path)
            if error_handling_added:
                print(f"  ✅ 添加了编码错误处理")
            
            # 修复文件操作
            file_ops_fixed = fix_file_operations(file_path)
            if file_ops_fixed:
                print(f"  ✅ 修复了文件操作")
            
            any_fixed = subprocess_fixed or error_handling_added or file_ops_fixed
            if not any_fixed:
                print(f"  ℹ️ 无需修复")
            
            results.append((filename, any_fixed))
    
    return results

def create_safe_test_runner():
    """创建一个安全的测试运行器"""
    runner_content = '''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
安全的测试运行器
处理编码问题和异常情况
"""

import os
import sys
import subprocess
import traceback
from datetime import datetime

def run_test_safely(script_path):
    """安全地运行单个测试脚本"""
    print(f"\\n{'='*60}")
    print(f"运行测试: {os.path.basename(script_path)}")
    print(f"{'='*60}")
    
    try:
        # 使用subprocess运行测试，处理编码问题
        result = subprocess.run(
            [sys.executable, script_path],
            capture_output=True,
            text=True,
            encoding='utf-8',
            errors='replace',  # 关键：处理编码错误
            timeout=300  # 5分钟超时
        )
        
        # 打印输出
        if result.stdout:
            print("STDOUT:")
            print(result.stdout)
        
        if result.stderr:
            print("STDERR:")
            print(result.stderr)
        
        if result.returncode != 0:
            print(f"⚠️ 测试返回非零退出码: {result.returncode}")
        else:
            print("✅ 测试完成")
            
        return result.returncode == 0
        
    except subprocess.TimeoutExpired:
        print("❌ 测试超时")
        return False
    except Exception as e:
        print(f"❌ 运行测试时出错: {e}")
        traceback.print_exc()
        return False

def main():
    tests_dir = "tests"
    test_scripts = [
        "test_pillar_09_creativity.py",
        "test_pillar_10_math.py",
        "test_pillar_11_safety.py",
        "test_pillar_12_persona.py",
        "test_pillar_13_init.py",
        "test_pillar_14_persona_depth.py",
        "test_pillar_15_collaboration.py",
        "test_pillar_16_emergence.py",
        "test_pillar_17_dag_generation.py",
        "test_pillar_18_fault_tolerance.py",
        "test_pillar_19_network_analysis.py",
    ]
    
    print(f"开始安全测试运行 - {datetime.now()}")
    
    success_count = 0
    total_count = len(test_scripts)
    
    for script_name in test_scripts:
        script_path = os.path.join(tests_dir, script_name)
        if os.path.exists(script_path):
            if run_test_safely(script_path):
                success_count += 1
        else:
            print(f"⚠️ 测试脚本不存在: {script_path}")
    
    print(f"\\n{'='*60}")
    print(f"测试完成: {success_count}/{total_count} 成功")
    print(f"结束时间: {datetime.now()}")
    print(f"{'='*60}")

if __name__ == "__main__":
    main()
'''
    
    with open("safe_test_runner.py", 'w', encoding='utf-8') as f:
        f.write(runner_content)
    
    print("✅ 创建了安全测试运行器: safe_test_runner.py")

def main():
    print("🔧 LLM测试编码问题修复工具")
    print("=" * 50)
    
    # 扫描并修复测试文件
    results = scan_and_fix_tests()
    
    # 统计结果
    fixed_count = sum(1 for _, fixed in results if fixed)
    total_count = len(results)
    
    print(f"\\n📊 修复结果:")
    print(f"  - 扫描文件: {total_count}")
    print(f"  - 修复文件: {fixed_count}")
    print(f"  - 无需修复: {total_count - fixed_count}")
    
    # 创建安全的测试运行器
    create_safe_test_runner()
    
    print(f"\\n🎯 建议:")
    if fixed_count > 0:
        print("  1. 重新运行测试以验证修复效果")
        print("  2. 使用 safe_test_runner.py 进行安全测试")
    else:
        print("  1. 所有文件都已经是安全的")
        print("  2. 可以正常运行测试")
    
    print("\\n✅ 编码问题修复完成！")

if __name__ == "__main__":
    main()
