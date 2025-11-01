import pytest
from playwright.sync_api import Page, expect
import subprocess
import os
import time
import requests # Added for checking Streamlit app readiness

# Assuming Streamlit is run on port 8501 by default
STREAMLIT_URL = "http://localhost:8501"
STREAMLIT_PROCESS = None

@pytest.fixture(scope="module", autouse=True)
def setup_streamlit_app():
    """Starts the Streamlit app before tests and stops it afterwards."""
    global STREAMLIT_PROCESS
    # Ensure the Streamlit app is stopped if it was running
    if STREAMLIT_PROCESS:
        STREAMLIT_PROCESS.terminate()
        STREAMLIT_PROCESS.wait()

    # Start the Streamlit app
    print(f"Starting Streamlit app from {os.getcwd()}")
    STREAMLIT_PROCESS = subprocess.Popen(
        ["streamlit", "run", "visual_test_interface.py"],
        cwd="D:/AIDevelop/testLLM",
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )

    # Wait for Streamlit app to be ready
    retries = 10
    for i in range(retries):
        try:
            requests.get(STREAMLIT_URL, timeout=1)
            print(f"Streamlit app is ready after {i+1} attempts.")
            break
        except requests.exceptions.ConnectionError:
            print(f"Attempt {i+1}/{retries}: Streamlit app not yet ready. Waiting...")
            time.sleep(5) # Wait for 5 seconds before retrying
    else:
        raise Exception("Streamlit app did not start within the expected time.")
    
    yield
    # Teardown: Stop the Streamlit app
    print("Stopping Streamlit app...")
    if STREAMLIT_PROCESS:
        STREAMLIT_PROCESS.terminate()
        STREAMLIT_PROCESS.wait()
    print("Streamlit app stopped.")

def test_full_evaluation_workflow(page: Page):
    """
    Tests the full workflow of selecting a model, selecting tests,
    running them, and verifying results display.
    """
    page.goto(STREAMLIT_URL)
    expect(page).to_have_title("LLM 测评可视化界面")
    
    st_header_locator = page.locator("h1", has_text="LLM 高级能力测评套件 - 可视化界面")
    expect(st_header_locator).to_be_visible()

    # 1. Select a model
    # Assuming there's at least one model in the selectbox
    model_selector = page.locator("xpath=//label[text()='选择要测试的LLM模型:']/following-sibling::div//div[contains(@class, 'st-emotion-cache') and @data-testid='stSelectbox']")
    
    # Click on the selectbox to open options
    model_selector.click()
    
    # Wait for the options to appear and select the first one
    page.locator("role=option").first.click()
    print("Selected a model.")

    # 2. Select tests - expand a group and select at least one test
    # Expand "基础能力测试"
    page.locator("summary:has-text('基础能力测试')").click()
    
    # Select the first test in "基础能力测试"
    test_checkbox_locator = page.locator("label:has-text('test_pillar_01_logic.py')").first
    if not test_checkbox_locator.is_checked():
        test_checkbox_locator.click()
    expect(test_checkbox_locator).to_be_checked()
    print("Selected 'test_pillar_01_logic.py'.")

    # 3. Click "运行测试" button
    run_button = page.locator("button", has_text="运行测试")
    run_button.click()
    print("Clicked '运行测试' button.")

    # 4. Verify "实时测试输出" and "结果仪表盘" appear
    realtime_output_header = page.locator("h2", has_text="2. 实时测试输出")
    results_dashboard_header = page.locator("h2", has_text="3. 结果仪表盘")
    
    expect(realtime_output_header).to_be_visible(timeout=60000) # Give it time to start
    expect(results_dashboard_header).to_be_visible(timeout=60000) # Give it time to finish and display

    # Optionally, wait for results content to appear (might need to be more specific)
    # This is a very basic check; a real test would parse the output content.
    page.wait_for_selector("div.stSpinner", state="hidden", timeout=120000) # Wait for spinner to disappear
    print("Spinner disappeared, tests likely completed.")

    # Verify success message or content in results dashboard
    expect(page.locator("p", has_text="测试运行完成！")).to_be_visible(timeout=30000)
    expect(page.locator("h3", has_text="测试结果摘要")).to_be_visible()
    expect(page.locator("p", has_text="**成功率:**")).to_be_visible()
    print("Test workflow completed successfully.")

def test_connectivity_check(page: Page):
    """
    Tests the model connectivity check functionality.
    """
    page.goto(STREAMLIT_URL)
    
    connectivity_button = page.locator("button", has_text="检查模型连通性")
    connectivity_button.click()
    print("Clicked '检查模型连通性' button.")

    # Wait for the connectivity results to appear
    expect(page.locator("h3", has_text="模型连通性状态")).to_be_visible(timeout=30000)
    # Check if some connectivity status is displayed (e.g., "可用" or "不可用")
    expect(page.locator("p", has_text="可用")).to_be_visible(timeout=30000)
    print("Connectivity check results displayed.")
