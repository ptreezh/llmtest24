#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Complete Web LLM Testing System
完整的Web LLM测试系统 - 支持真实模型选择、批量测试、结果下载
"""

import streamlit as st
import subprocess
import sys
import os
import json
import time
import pandas as pd
from pathlib import Path
from datetime import datetime
import threading
import queue
import asyncio

# Add project root to path
sys.path.append(str(Path(__file__).parent))
sys.path.append(str(Path(__file__).parent / "scripts" / "utils"))

try:
    import cloud_services
    CLOUD_SERVICES_AVAILABLE = True
except:
    CLOUD_SERVICES_AVAILABLE = False

# 导入增强的测试执行器
try:
    from enhanced_test_executor import TestExecutor
    ENHANCED_EXECUTOR_AVAILABLE = True
except:
    ENHANCED_EXECUTOR_AVAILABLE = False

# 页面配置
st.set_page_config(
    page_title="LLM Complete Testing System",
    page_icon="🧪",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 初始化session state
def init_session_state():
    """初始化session state"""
    if 'testing_running' not in st.session_state:
        st.session_state.testing_running = False
    if 'test_results' not in st.session_state:
        st.session_state.test_results = []
    if 'current_test_index' not in st.session_state:
        st.session_state.current_test_index = 0
    if 'test_queue' not in st.session_state:
        st.session_state.test_queue = queue.Queue()
    if 'progress_data' not in st.session_state:
        st.session_state.progress_data = {}

# 获取可用模型
def get_available_models():
    """获取所有可用的真实模型"""
    if not CLOUD_SERVICES_AVAILABLE:
        return []
    
    try:
        models = cloud_services.get_all_models()
        return models
    except:
        return []

# 获取测试文件列表
def get_test_files():
    """获取所有测试文件"""
    if ENHANCED_EXECUTOR_AVAILABLE:
        executor = TestExecutor()
        return executor.get_test_files()
    else:
        # 降级到基本版本
        test_files = []
        tests_dir = Path("tests")
        
        if tests_dir.exists():
            for file in tests_dir.glob("test_pillar_*.py"):
                # 提取pillar编号
                if file.name.startswith("test_pillar_25"):
                    pillar = 25
                else:
                    try:
                        pillar_num = int(file.name.split("_")[2].split(".")[0])
                        pillar = pillar_num
                    except:
                        continue
                
                # 分类测试类型
                if 1 <= pillar <= 8:
                    category = "基础能力"
                elif 9 <= pillar <= 19:
                    category = "高级能力"
                elif 20 <= pillar <= 24:
                    category = "前沿能力"
                elif pillar == 25:
                    category = "专项测试"
                else:
                    category = "其他"
                
                test_files.append({
                    "file": file.name,
                    "pillar": pillar,
                    "category": category,
                    "path": str(file),
                    "title": file.name,
                    "description": "测试文件"
                })
        
        return sorted(test_files, key=lambda x: x["pillar"])

# 执行单个测试
def run_single_test(test_info, model_key):
    """执行单个测试"""
    if ENHANCED_EXECUTOR_AVAILABLE:
        executor = TestExecutor()
        return executor.execute_test(test_info, model_key)
    else:
        # 降级到基本版本
        try:
            # 解析模型信息
            if '-' in model_key:
                service, model = model_key.split('-', 1)
            else:
                service = model_key
                model = model_key
            
            # 使用提取的prompt或默认prompt
            prompt = test_info.get("prompt", f"请完成第{test_info['pillar']}项能力测试")
            
            # 调用真实LLM
            response = cloud_services.call_cloud_service(service, model, prompt)
            
            return {
                "test_file": test_info["file"],
                "test_title": test_info.get("title", test_info["file"]),
                "pillar": test_info["pillar"],
                "category": test_info["category"],
                "model": model_key,
                "service": service,
                "prompt": prompt,
                "response": response,
                "timestamp": datetime.now().isoformat(),
                "status": "completed",
                "response_length": len(response) if response else 0
            }
            
        except Exception as e:
            return {
                "test_file": test_info["file"],
                "test_title": test_info.get("title", test_info["file"]),
                "pillar": test_info["pillar"],
                "category": test_info["category"],
                "model": model_key,
                "error": str(e),
                "timestamp": datetime.now().isoformat(),
                "status": "failed"
            }

# 生成测试报告
def generate_test_report(results):
    """生成测试报告"""
    if not results:
        return None
    
    if ENHANCED_EXECUTOR_AVAILABLE:
        executor = TestExecutor()
        executor.results = results
        return executor.generate_comprehensive_report()
    else:
        # 降级到基本版本
        # 统计信息
        total_tests = len(results)
        successful_tests = len([r for r in results if r["status"] == "completed"])
        failed_tests = total_tests - successful_tests
        
        # 按类别统计
        category_stats = {}
        for result in results:
            category = result["category"]
            if category not in category_stats:
                category_stats[category] = {"total": 0, "success": 0}
            category_stats[category]["total"] += 1
            if result["status"] == "completed":
                category_stats[category]["success"] += 1
        
        # 生成报告
        report = {
            "test_summary": {
                "total_tests": total_tests,
                "successful_tests": successful_tests,
                "failed_tests": failed_tests,
                "success_rate": (successful_tests / total_tests * 100) if total_tests > 0 else 0,
                "test_date": datetime.now().isoformat()
            },
            "category_statistics": category_stats,
            "detailed_results": results
        }
        
        return report

# 主界面
def main():
    init_session_state()
    
    st.title("🧪 LLM Complete Testing System")
    st.markdown("---")
    
    # 侧边栏 - 配置
    with st.sidebar:
        st.header("⚙️ 测试配置")
        
        # 模型选择
        st.subheader("1. 选择LLM模型")
        available_models = get_available_models()
        
        if available_models:
            model_options = [f"{m['model']} ({m['service']})" for m in available_models]
            model_keys = [m['key'] for m in available_models]
            
            selected_model_index = st.selectbox(
                "选择模型:",
                range(len(model_options)),
                format_func=lambda x: model_options[x]
            )
            selected_model = model_keys[selected_model_index]
            
            st.info(f"已选择: {model_options[selected_model_index]}")
        else:
            st.error("无法加载模型列表，请检查配置")
            selected_model = None
        
        # 测试选择
        st.subheader("2. 选择测试")
        test_files = get_test_files()
        
        if test_files:
            # 按类别分组
            categories = {}
            for test in test_files:
                cat = test["category"]
                if cat not in categories:
                    categories[cat] = []
                categories[cat].append(test)
            
            selected_tests = []
            for category, tests in categories.items():
                with st.expander(f"{category} ({len(tests)} 个测试)"):
                    select_all = st.checkbox(f"全选 {category}", key=f"select_all_{category}")
                    
                    for test in tests:
                        test_key = f"{test['pillar']}_{test['file']}"
                        selected = st.checkbox(
                            f"Pillar {test['pillar']}: {test['file']}",
                            value=select_all,
                            key=test_key
                        )
                        if selected:
                            selected_tests.append(test)
            
            st.info(f"已选择 {len(selected_tests)} 个测试")
        else:
            st.error("无法加载测试文件")
            selected_tests = []
        
        # 测试设置
        st.subheader("3. 测试设置")
        test_mode = st.radio(
            "测试模式:",
            ["单个执行", "批量执行", "脚本模式"]
        )
        
        batch_size = st.slider(
            "并发数量:",
            min_value=1,
            max_value=10,
            value=3,
            help="同时执行的测试数量"
        )
        
        # 开始测试按钮
        start_button = st.button(
            "🚀 开始测试",
            disabled=st.session_state.testing_running or not selected_model or not selected_tests,
            type="primary"
        )
    
    # 主界面内容
    if start_button and selected_model and selected_tests:
        st.session_state.testing_running = True
        st.session_state.test_results = []
        st.session_state.current_test_index = 0
        
        # 显示测试进度
        progress_container = st.container()
        with progress_container:
            st.subheader("📊 测试进度")
            
            progress_bar = st.progress(0)
            status_text = st.empty()
            results_container = st.container()
            
        # 执行测试
        total_tests = len(selected_tests)
        
        for i, test_info in enumerate(selected_tests):
            if not st.session_state.testing_running:
                break
            
            # 更新进度
            progress = (i + 1) / total_tests
            progress_bar.progress(progress)
            status_text.text(f"正在执行测试 {i+1}/{total_tests}: {test_info['file']}")
            
            # 执行测试
            with st.spinner(f"执行 {test_info['file']}..."):
                result = run_single_test(test_info, selected_model)
                st.session_state.test_results.append(result)
                
                # 显示实时结果
                with results_container:
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric(f"测试 {i+1}", test_info['file'])
                    with col2:
                        status_icon = "✅" if result["status"] == "completed" else "❌"
                        st.markdown(f"**状态**: {status_icon} {result['status']}")
                    with col3:
                        if result["status"] == "completed":
                            st.metric("响应长度", f"{result['response_length']} 字符")
                
                # 短暂延迟避免API限制
                time.sleep(1)
        
        # 测试完成
        st.session_state.testing_running = False
        progress_bar.progress(1.0)
        status_text.text("🎉 测试完成！")
        
        # 显示结果摘要
        st.subheader("📈 测试结果摘要")
        
        if st.session_state.test_results:
            # 生成报告
            report = generate_test_report(st.session_state.test_results)
            
            if report:
                # 显示统计信息
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("总测试数", report["test_summary"]["total_tests"])
                with col2:
                    st.metric("成功数", report["test_summary"]["successful_tests"])
                with col3:
                    st.metric("失败数", report["test_summary"]["failed_tests"])
                with col4:
                    st.metric("成功率", f"{report['test_summary']['success_rate']:.1f}%")
                
                # 按类别显示结果
                st.subheader("📊 分类统计")
                for category, stats in report["category_statistics"].items():
                    col1, col2 = st.columns(2)
                    with col1:
                        st.write(f"**{category}**")
                    with col2:
                        success_rate = (stats["success"] / stats["total"] * 100) if stats["total"] > 0 else 0
                        st.write(f"{stats['success']}/{stats['total']} ({success_rate:.1f}%)")
                
                # 详细结果表格
                st.subheader("📋 详细结果")
                
                # 准备表格数据
                table_data = []
                for result in st.session_state.test_results:
                    table_data.append({
                        "测试文件": result["test_file"],
                        "类别": result["category"],
                        "状态": result["status"],
                        "响应长度": result.get("response_length", 0) if result["status"] == "completed" else 0,
                        "时间": result["timestamp"][:19]
                    })
                
                df = pd.DataFrame(table_data)
                st.dataframe(df, use_container_width=True)
                
                # 显示详细响应
                st.subheader("🔍 详细响应")
                
                selected_result_index = st.selectbox(
                    "选择测试查看详细结果:",
                    range(len(st.session_state.test_results)),
                    format_func=lambda x: f"{st.session_state.test_results[x]['test_file']}"
                )
                
                if selected_result_index is not None:
                    result = st.session_state.test_results[selected_result_index]
                    
                    st.markdown(f"**测试文件**: {result['test_file']}")
                    st.markdown(f"**模型**: {result['model']}")
                    st.markdown(f"**状态**: {result['status']}")
                    
                    if result["status"] == "completed":
                        with st.expander("查看Prompt"):
                            st.text_area("Prompt", result["prompt"], height=100)
                        
                        with st.expander("查看响应"):
                            st.text_area("Model Response", result["response"], height=200)
                    else:
                        st.error(f"错误: {result.get('error', 'Unknown error')}")
                
                # 下载报告
                st.subheader("💾 下载测试报告")
                
                # JSON格式报告
                json_report = json.dumps(report, indent=2, ensure_ascii=False)
                st.download_button(
                    label="下载JSON报告",
                    data=json_report,
                    file_name=f"llm_test_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                    mime="application/json"
                )
                
                # CSV格式报告
                csv_data = pd.DataFrame(table_data).to_csv(index=False)
                st.download_button(
                    label="下载CSV报告",
                    data=csv_data,
                    file_name=f"llm_test_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv"
                )
                
                # 脚本模式支持
                if test_mode == "脚本模式":
                    st.subheader("📜 批量测试脚本")
                    
                    script_content = f'''#!/usr/bin/env python3
# 自动生成的批量测试脚本
# 生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

import sys
import os
sys.path.append(os.path.dirname(__file__))

from scripts.utils.cloud_services import call_cloud_service

# 测试配置
MODEL_SERVICE = "{selected_model.split('-')[0]}"
MODEL_NAME = "{selected_model.split('-')[1] if '-' in selected_model else selected_model}"

# 测试列表
TESTS = {[
    {
        "file": test["file"],
        "pillar": test["pillar"],
        "prompt": "请完成相关测试"  # 实际使用时需要提取真实的prompt
    }
    for test in selected_tests
]}

def run_batch_tests():
    """执行批量测试"""
    results = []
    
    for i, test in enumerate(TESTS):
        print(f"执行测试 {{i+1}}/{{len(TESTS)}}: {{test['file']}}")
        
        try:
            response = call_cloud_service(MODEL_SERVICE, MODEL_NAME, test["prompt"])
            
            result = {{
                "test_file": test["file"],
                "pillar": test["pillar"],
                "response": response,
                "status": "completed"
            }}
        except Exception as e:
            result = {{
                "test_file": test["file"],
                "pillar": test["pillar"],
                "error": str(e),
                "status": "failed"
            }}
        
        results.append(result)
        print(f"完成: {{result['status']}}")
        
        # 避免API限制
        import time
        time.sleep(1)
    
    # 保存结果
    import json
    with open("batch_test_results.json", "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    print(f"批量测试完成，共执行 {{len(results)}} 个测试")

if __name__ == "__main__":
    run_batch_tests()
'''
                    
                    st.download_button(
                        label="下载批量测试脚本",
                        data=script_content,
                        file_name=f"batch_test_script_{datetime.now().strftime('%Y%m%d_%H%M%S')}.py",
                        mime="text/plain"
                    )
                    
                    st.info("下载脚本后，可以在本地环境中运行批量测试")
    
    else:
        st.info("请选择模型和测试，然后点击'开始测试'")

if __name__ == "__main__":
    main()