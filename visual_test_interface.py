import streamlit as st
import subprocess
import os
import json
import re
import time
from scripts.utils.cloud_services import get_all_models

# 设置页面配置
st.set_page_config(page_title="LLM 测评可视化界面", page_icon="📊", layout="wide")

# 初始化 session state
if 'test_running' not in st.session_state:
    st.session_state.test_running = False
if 'selected_tests' not in st.session_state:
    st.session_state.selected_tests = {}

# 应用标题
st.title("LLM 高级能力测评套件 - 可视化界面")

# 添加项目说明和测试解释的超链接
st.markdown("📖 [项目使用说明 (README)](https://github.com/ptreezh/llmtest24/blob/main/README.md) | 📊 [测试解释说明 (SCORING_EXPLANATION)](https://github.com/ptreezh/llmtest24/blob/main/docs/SCORING_EXPLANATION.md)")

# 创建三个主要布局区域
col1, col2 = st.columns([1, 2])

# --- Column 1: Controls ---
with col1:
    st.header("1. 模型与测试选择")
    
    @st.cache_data(ttl=300) # 缓存模型列表5分钟
    def get_available_models():
        """从 cloud_services.py 获取所有可用的模型列表"""
        try:
            all_models = get_all_models()
            return [model['key'] for model in all_models]
        except Exception as e:
            st.error(f"获取模型列表失败: {e}")
            return []

    available_models = get_available_models()
    if available_models:
        selected_model = st.selectbox(
            "选择要测试的LLM模型:",
            available_models,
            disabled=st.session_state.test_running
        )
    else:
        st.warning("未能加载可用模型列表。请检查网络连接或配置。")
        if st.button("重试"):
            st.rerun()

    @st.cache_data # 缓存测试发现结果
    def discover_tests():
        """扫描 tests/ 目录，发现所有测试并按支柱分组"""
        try:
            tests_dir = "tests"
            test_files = []
            pattern = re.compile(r'test_pillar_(\d+)')
            
            for file in os.listdir(tests_dir):
                if file.endswith('.py') and file.startswith('test_pillar_'):
                    if file.startswith('test_pillar_25'):
                        pillar = 25
                    else:
                        match = pattern.match(file)
                        if match:
                            pillar = int(match.group(1))
                        else:
                            continue
                    test_files.append((file, pillar))
            
            test_groups = {
                "基础能力测试": [], "高级能力测试": [],
                "前沿能力测试": [], "专项测试": []
            }
            
            for file, pillar in test_files:
                if 1 <= pillar <= 8:
                    test_groups["基础能力测试"].append(file)
                elif 9 <= pillar <= 19:
                    test_groups["高级能力测试"].append(file)
                elif 20 <= pillar <= 24:
                    test_groups["前沿能力测试"].append(file)
                elif pillar == 25:
                    test_groups["专项测试"].append(file)
            
            return test_groups
        except Exception as e:
            st.error(f"发现测试失败: {e}")
            return {}

    test_groups = discover_tests()
    
    for group_name, tests in test_groups.items():
        if tests:
            with st.expander(f"{group_name} ({len(tests)} 个测试)"):
                all_key = f"select_all_{group_name.replace(' ', '_')}"
                all_selected = st.checkbox(f"全选 {group_name}", key=all_key, disabled=st.session_state.test_running)
                
                for test in sorted(tests):
                    # If 'select all' is checked, mark this as selected in session_state
                    if all_selected:
                        st.session_state[test] = True
                    else:
                        st.session_state[test] = False
                    
                    # The checkbox's state is now managed by its key in session_state
                    st.checkbox(test, key=test, disabled=st.session_state.test_running)

    st.header("2. 执行与监控")
    
    # 添加检查连通性按钮
    if st.button("检查模型连通性", disabled=st.session_state.test_running):
        with st.spinner('正在检查所有模型的连通性...'):
            try:
                from scripts.utils.cloud_services import check_all_services
                connectivity_results = check_all_services()
                
                with col2:
                    st.header("模型连通性状态")
                    for service, result in connectivity_results.items():
                        status = "✅ 可用" if result["available"] else "❌ 不可用"
                        st.write(f"{result['name']} ({service}): {status}")
                        if not result["available"]:
                            st.write(f"  原因: {result['reason']}")
                        
            except Exception as e:
                st.error(f"检查连通性时发生错误: {e}")
    
    # 添加运行测试按钮
    if st.button("运行测试", disabled=st.session_state.test_running):
        selected_test_files = [
            test for test, selected in st.session_state.items() 
            if isinstance(selected, bool) and selected and test.startswith('test_pillar_')
        ]

        if not selected_model:
            st.error("请先选择一个要测试的LLM模型。")
        elif not selected_test_files:
            st.error("请至少选择一个要运行的测试。")
        else:
            st.session_state.test_running = True
            st.rerun()

# --- Column 2: Output & Results ---
with col2:
    st.header("3. 测试输出与结果")
    output_placeholder = st.empty()
    results_placeholder = st.empty()


def run_tests(model_key, test_files):
    command = [
        "python", "-u", "scripts/run_web_tests.py",
        "--model", model_key,
        "--tests"
    ] + [os.path.join("tests", f) for f in test_files]
    
    output_log = ""
    with output_placeholder.container():
        st.info(f"正在为模型 {model_key} 运行 {len(test_files)} 个测试...")
        log_display = st.code(output_log, language="log")

        process = subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            encoding='utf-8',
            bufsize=1
        )

        for line in iter(process.stdout.readline, ''):
            output_log += line
            log_display.code(output_log, language="log")

        process.stdout.close()
        return_code = process.wait()

    if return_code == 0:
        st.success("测试运行完成！")
        # 查找并解析JSON结果
        json_output = None
        for line in reversed(output_log.strip().split('\n')):
            try:
                # Check if the line is a potential JSON object
                if line.strip().startswith('{') and line.strip().endswith('}'):
                    json_output = json.loads(line)
                    break
            except json.JSONDecodeError:
                continue
        
        if json_output:
            with results_placeholder.container():
                st.subheader("测试结果摘要")
                st.write(f"**模型:** {json_output['model_name']}")
                st.write(f"**成功率:** {json_output['success_rate']:.1f}%")
                st.write(f"**总耗时:** {json_output['duration_seconds']:.2f} 秒")
                
                st.subheader("详细结果")
                for detail in json_output['test_details']:
                    status_icon = "✅" if detail['status'] == "SUCCESS" else "❌"
                    with st.expander(f"{status_icon} **{detail['test_name']}**: {detail['status']}", expanded=(detail['status'] != "SUCCESS")):
                         if detail['status'] != "SUCCESS":
                            st.code(detail.get('error') or detail.get('output'), language="log")
        else:
            st.error("无法从测试输出中解析最终的JSON结果。")

    else:
        st.error(f"测试运行失败，返回码: {return_code}")

# --- Main logic to run tests ---
if st.session_state.test_running:
    # Get selected model and tests from session state
    selected_test_files = [
        test for test, selected in st.session_state.items() 
        if isinstance(selected, bool) and selected and test.startswith('test_pillar_')
    ]
    
    # This assumes selected_model is available from the selectbox
    # (it is, because we disable it so it retains its value)
    run_tests(selected_model, selected_test_files)
    
    # Reset running state
    st.session_state.test_running = False
    # Clear selections for next run
    for key in list(st.session_state.keys()):
        if key.startswith('test_pillar_') or key.startswith('select_all_'):
            del st.session_state[key]
    st.rerun()
