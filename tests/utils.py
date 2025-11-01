#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
通用测试工具函数
"""

import logging
import os
import sys
from pathlib import Path
from typing import Dict, Any, Optional

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def run_single_test(pillar_name: str, prompt: str, model: str, options: Optional[Dict[str, Any]] = None, test_script_name: str = ""):
    """
    运行单个测试的通用函数
    """
    logger.info(f"开始执行测试: {pillar_name}")
    
    # 从 independence.utils 导入 call_llm_api 函数
    try:
        from independence.utils import call_llm_api
    except ImportError as e:
        logger.error(f"无法导入 independence.utils: {e}")
        return f"导入失败: {str(e)}", {}
    
    # 调用本地LLM API
    try:
        response = call_llm_api(model, "", prompt, options)
        logger.info(f"测试完成: {pillar_name}")
        return response, {}
    except Exception as e:
        logger.error(f"调用本地LLM API失败: {e}")
        return f"调用失败: {str(e)}", {}

def print_assessment_criteria(criteria: str):
    """
    打印评估标准
    """
    print("\n--- 评估标准 ---")
    print(criteria)
    print("--- 结束 ---")

def setup_test_environment():
    """
    设置测试环境
    """
    logger.info("设置测试环境")
    # 可以在这里添加创建测试目录等操作
    test_dir = Path("test_workspace")
    test_dir.mkdir(exist_ok=True)
    return test_dir

def cleanup_test_environment():
    """
    清理测试环境
    """
    logger.info("清理测试环境")
    # 可以在这里添加删除测试文件等操作

def save_file(file_path: str, content: str):
    """
    保存文件
    """
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        logger.info(f"文件已保存: {file_path}")
    except Exception as e:
        logger.error(f"保存文件失败: {e}")

def execute_bash_script(script_content: str):
    """
    执行Bash脚本
    """
    # 这是一个简化版本，实际可能需要更复杂的逻辑
    logger.info("执行Bash脚本")
    print(script_content)
