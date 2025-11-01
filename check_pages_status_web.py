import asyncio
from playwright.async_api import async_playwright

async def check_github_pages_status():
    async with async_playwright() as p:
        # 启动浏览器
        browser = await p.chromium.launch(channel="msedge", headless=False)
        page = await browser.new_page()
        
        # 访问GitHub Pages设置页面
        await page.goto("https://github.com/ptreezh/llmtest24/settings/pages")
        
        # 等待页面加载
        await page.wait_for_load_state("networkidle")
        
        print("正在检查GitHub Pages配置状态...")
        
        # 等待一段时间确保页面加载完成
        await page.wait_for_timeout(3000)
        
        # 尝试获取页面中的关键信息
        try:
            # 查找源配置信息
            source_elements = await page.query_selector_all("div:has-text('Source'), label:has-text('Source')")
            for element in source_elements:
                if await element.is_visible():
                    print("找到源配置部分")
                    # 查找分支选择器
                    branch_selectors = await page.query_selector_all("select")
                    for selector in branch_selectors:
                        if await selector.is_visible():
                            try:
                                selected_value = await selector.input_value()
                                print(f"当前选择的分支: {selected_value}")
                            except:
                                pass
                    break
            
            # 查找部署状态
            status_elements = await page.query_selector_all("div:has-text('Status'), div:has-text('status')")
            for element in status_elements:
                if await element.is_visible():
                    status_text = await element.text_content()
                    print(f"部署状态相关文本: {status_text}")
            
            # 查找错误信息
            error_elements = await page.query_selector_all("div:has-text('error'), div:has-text('Error'), div.alert")
            for element in error_elements:
                if await element.is_visible():
                    error_text = await element.text_content()
                    print(f"错误信息: {error_text}")
                    
        except Exception as e:
            print(f"检查配置信息时出错: {e}")
        
        # 截图以供检查
        await page.screenshot(path="github_pages_current_status.png", full_page=True)
        print("已保存当前状态截图到 github_pages_current_status.png")
        
        # 关闭浏览器
        await browser.close()

if __name__ == "__main__":
    asyncio.run(check_github_pages_status())