#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
快速修复编码问题脚本
移除有问题的编码错误处理代码
"""

import os
import re

def fix_syntax_errors():
    """修复语法错误"""
    tests_dir = "tests"
    
    for filename in os.listdir(tests_dir):
        if filename.startswith("test_pillar_") and filename.endswith(".py"):
            file_path = os.path.join(tests_dir, filename)
            
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # 移除有问题的编码错误处理行
                problematic_pattern = r'\s+except UnicodeDecodeError as ude:\s+print\(f".*?"\)\s+'
                content = re.sub(problematic_pattern, '\n        ', content, flags=re.DOTALL)
                
                # 简化异常处理
                content = re.sub(
                    r'except Exception as (\w+):',
                    r'except Exception as \1:',
                    content
                )
                
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                
                print(f"✅ 修复了 {filename}")
                
            except Exception as e:
                print(f"❌ 修复 {filename} 时出错: {e}")

if __name__ == "__main__":
    print("🔧 快速修复语法错误...")
    fix_syntax_errors()
    print("✅ 修复完成！")
