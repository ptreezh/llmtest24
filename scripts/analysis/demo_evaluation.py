#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
LLM测评系统演示脚本
展示如何使用完整的评价体系进行模型测试和分析
"""

import os
import sys
import subprocess
from datetime import datetime

def print_header(title):
    """打印格式化的标题"""
    print("\n" + "="*60)
    print(f" {title}")
    print("="*60)

def print_step(step_num, description):
    """打印步骤信息"""
    print(f"\n📋 步骤 {step_num}: {description}")
    print("-" * 40)

def run_command(command, description):
    """运行命令并显示结果"""
    print(f"执行: {command}")
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True, encoding='utf-8')
        if result.returncode == 0:
            print("✅ 成功")
            if result.stdout.strip():
                print(f"输出: {result.stdout.strip()[:200]}...")
        else:
            print("❌ 失败")
            if result.stderr:
                print(f"错误: {result.stderr.strip()}")
        return result.returncode == 0
    except Exception as e:
        print(f"❌ 执行失败: {e}")
        return False

def check_file_exists(filepath, description):
    """检查文件是否存在"""
    if os.path.exists(filepath):
        size = os.path.getsize(filepath)
        print(f"✅ {description}: {filepath} ({size} bytes)")
        return True
    else:
        print(f"❌ {description}: {filepath} 不存在")
        return False

def main():
    print_header("LLM测评系统完整演示")
    print(f"开始时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # 步骤1: 环境检查
    print_step(1, "环境检查")
    
    # 检查Python版本
    python_version = sys.version.split()[0]
    print(f"Python版本: {python_version}")
    
    # 检查必要文件
    required_files = [
        ("config.py", "配置文件"),
        ("run_all_tests_with_output.py", "增强测试脚本"),
        ("evaluate_results.py", "评价脚本"),
        ("analyze_results.py", "深度分析脚本"),
        ("README_EVALUATION.md", "使用说明")
    ]
    
    all_files_exist = True
    for filepath, description in required_files:
        if not check_file_exists(filepath, description):
            all_files_exist = False
    
    if not all_files_exist:
        print("\n❌ 缺少必要文件，请确保所有脚本都已创建")
        return
    
    # 检查Ollama
    print("\n检查Ollama服务...")
    ollama_ok = run_command("ollama list", "获取模型列表")
    
    if not ollama_ok:
        print("❌ Ollama服务未运行，请先启动: ollama serve")
        return
    
    # 步骤2: 配置检查
    print_step(2, "配置检查")
    
    try:
        from config import MODEL_TO_TEST
        print(f"✅ 配置的测试模型: {MODEL_TO_TEST}")
    except ImportError:
        print("❌ 无法导入配置文件")
        return
    except AttributeError:
        print("❌ 配置文件中缺少 MODEL_TO_TEST")
        return
    
    # 步骤3: 运行测试
    print_step(3, "运行完整测试套件")
    
    print("这将运行所有11个Pillar的测试，可能需要几分钟...")
    user_input = input("是否继续? (y/N): ").strip().lower()
    
    if user_input != 'y':
        print("用户取消测试")
        return
    
    test_success = run_command("python run_all_tests_with_output.py", "运行测试套件")
    
    if not test_success:
        print("❌ 测试运行失败，请检查错误信息")
        return
    
    # 步骤4: 检查测试结果
    print_step(4, "检查测试结果")
    
    testout_dir = "testout"
    if os.path.exists(testout_dir):
        result_files = [f for f in os.listdir(testout_dir) if f.endswith('.txt')]
        print(f"✅ 生成了 {len(result_files)} 个测试结果文件")
        
        # 显示部分结果文件
        for i, filename in enumerate(result_files[:5]):
            filepath = os.path.join(testout_dir, filename)
            size = os.path.getsize(filepath)
            print(f"  - {filename} ({size} bytes)")
        
        if len(result_files) > 5:
            print(f"  ... 还有 {len(result_files) - 5} 个文件")
    else:
        print("❌ 测试结果目录不存在")
        return
    
    # 步骤5: 生成评价报告
    print_step(5, "生成评价报告")
    
    eval_success = run_command("python evaluate_results.py", "生成标准评价报告")
    
    if eval_success:
        check_file_exists("evaluation_report.md", "标准评价报告")
    
    # 步骤6: 生成深度分析
    print_step(6, "生成深度分析报告")
    
    analysis_success = run_command("python analyze_results.py", "生成深度分析报告")
    
    if analysis_success:
        check_file_exists("comprehensive_analysis_report.md", "深度分析报告")
        check_file_exists("analysis_data.json", "分析数据文件")
    
    # 步骤7: 显示结果摘要
    print_step(7, "结果摘要")
    
    try:
        # 读取评价报告的关键信息
        if os.path.exists("evaluation_report.md"):
            with open("evaluation_report.md", 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 提取总体得分
            import re
            score_match = re.search(r'\*\*总体得分\*\*: (\d+)/(\d+) \(([0-9.]+)%\)', content)
            grade_match = re.search(r'\*\*总体等级\*\*: (.+)', content)
            
            if score_match and grade_match:
                score, total, percentage = score_match.groups()
                grade = grade_match.group(1)
                
                print(f"🎯 测试完成！")
                print(f"📊 总体得分: {score}/{total} ({percentage}%)")
                print(f"🏆 总体等级: {grade}")
                
                # 给出简单建议
                percentage_float = float(percentage)
                if percentage_float >= 70:
                    print("✅ 模型表现良好！")
                elif percentage_float >= 40:
                    print("⚠️ 模型表现一般，建议优化")
                else:
                    print("❌ 模型表现不佳，建议更换或重新配置")
            else:
                print("📊 评价报告已生成，请查看详细内容")
        
        # 列出生成的文件
        print(f"\n📁 生成的文件:")
        output_files = [
            "evaluation_report.md",
            "comprehensive_analysis_report.md", 
            "analysis_data.json"
        ]
        
        for filename in output_files:
            if os.path.exists(filename):
                size = os.path.getsize(filename)
                print(f"  ✅ {filename} ({size} bytes)")
            else:
                print(f"  ❌ {filename} (未生成)")
                
    except Exception as e:
        print(f"读取结果时出错: {e}")
    
    # 步骤8: 使用建议
    print_step(8, "后续使用建议")
    
    print("""
📖 查看详细报告:
  - evaluation_report.md: 标准评价报告
  - comprehensive_analysis_report.md: 深度分析报告
  - README_EVALUATION.md: 完整使用指南

🔄 持续改进:
  1. 根据评价结果调整模型配置
  2. 优化提示词设计
  3. 定期重新测试
  4. 与其他模型进行对比

🛠️ 自定义评价:
  - 修改 evaluate_results.py 中的评价标准
  - 添加新的测试维度
  - 调整评分权重
""")
    
    print_header("演示完成")
    print(f"结束时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("感谢使用LLM测评系统！")

if __name__ == "__main__":
    main()
