import asyncio
from playwright.async_api import async_playwright

async def check_github_actions_status():
    async with async_playwright() as p:
        # 启动浏览器
        browser = await p.chromium.launch(channel="msedge", headless=False)
        page = await browser.new_page()
        
        # 访问GitHub Actions页面
        await page.goto("https://github.com/ptreezh/llmtest24/actions")
        
        # 等待页面加载
        await page.wait_for_load_state("networkidle")
        
        print("正在检查GitHub Actions状态...")
        
        # 等待一段时间确保页面加载完成
        await page.wait_for_timeout(3000)
        
        # 尝试查找工作流运行状态
        try:
            # 查找工作流运行列表
            workflow_runs = await page.query_selector_all(".Box-row")
            print(f"找到 {len(workflow_runs)} 个工作流运行记录")
            
            if workflow_runs:
                # 检查最新的工作流运行
                latest_run = workflow_runs[0]
                status_elements = await latest_run.query_selector_all(".State")
                for element in status_elements:
                    if await element.is_visible():
                        status_text = await element.text_content()
                        print(f"最新工作流状态: {status_text}")
                        break
                
                # 查找工作流名称
                name_elements = await latest_run.query_selector_all("a")
                for element in name_elements:
                    if await element.is_visible():
                        name_text = await element.text_content()
                        print(f"工作流名称: {name_text}")
                        break
            else:
                print("未找到工作流运行记录")
                
        except Exception as e:
            print(f"检查工作流状态时出错: {e}")
        
        # 截图以供检查
        await page.screenshot(path="github_actions_status.png", full_page=True)
        print("已保存Actions状态截图到 github_actions_status.png")
        
        # 关闭浏览器
        await browser.close()

if __name__ == "__main__":
    asyncio.run(check_github_actions_status())