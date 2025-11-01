import asyncio
from playwright.async_api import async_playwright

async def check_repo_settings():
    async with async_playwright() as p:
        # 启动浏览器
        browser = await p.chromium.launch(channel="msedge", headless=False)
        page = await browser.new_page()
        
        # 访问仓库主页
        await page.goto("https://github.com/ptreezh/llmtest24")
        
        # 等待页面加载
        await page.wait_for_load_state("networkidle")
        
        print("正在检查仓库设置...")
        
        # 等待一段时间确保页面加载完成
        await page.wait_for_timeout(3000)
        
        # 查找设置链接
        try:
            # 查找设置选项卡
            settings_link = await page.query_selector("a[href='/ptreezh/llmtest24/settings']")
            if settings_link:
                await settings_link.click()
                print("已点击设置链接")
            else:
                print("未找到设置链接")
                # 尝试其他可能的选择器
                settings_links = await page.query_selector_all("a")
                for link in settings_links:
                    if await link.is_visible():
                        text_content = await link.text_content()
                        if text_content and "settings" in text_content.lower():
                            await link.click()
                            print(f"已点击设置链接: {text_content}")
                            break
                
            # 等待设置页面加载
            await page.wait_for_timeout(3000)
            
            # 查找Pages设置
            pages_link = await page.query_selector("a[href='/ptreezh/llmtest24/settings/pages']")
            if pages_link:
                await pages_link.click()
                print("已点击Pages设置链接")
            else:
                print("未找到Pages设置链接")
                # 尝试在页面中查找"Pages"文本
                page_elements = await page.query_selector_all("*")
                for element in page_elements:
                    if await element.is_visible():
                        text_content = await element.text_content()
                        if text_content and "pages" in text_content.lower():
                            # 尝试点击包含"pages"的元素
                            try:
                                await element.click()
                                print(f"已点击包含'pages'的元素: {text_content}")
                                break
                            except:
                                pass
            
            # 等待Pages设置页面加载
            await page.wait_for_timeout(3000)
            
        except Exception as e:
            print(f"导航到设置页面时出错: {e}")
        
        # 截图以供检查
        await page.screenshot(path="repo_settings_check.png", full_page=True)
        print("已保存设置检查截图到 repo_settings_check.png")
        
        # 关闭浏览器
        await browser.close()

if __name__ == "__main__":
    asyncio.run(check_repo_settings())