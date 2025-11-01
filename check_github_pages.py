import asyncio
from playwright.async_api import async_playwright

async def check_github_pages_status():
    async with async_playwright() as p:
        # 启动浏览器
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()
        
        # 访问GitHub登录页面
        await page.goto("https://github.com/login")
        
        # 等待用户手动登录（因为需要输入用户名和密码）
        print("请在浏览器中手动登录GitHub账户...")
        print("登录完成后，按Enter键继续...")
        
        try:
            # 尝试读取输入，如果失败则继续执行
            input()
        except:
            print("继续执行检查...")
        
        # 访问仓库的Pages设置页面
        await page.goto("https://github.com/ptreezh/llmtest24/settings/pages")
        
        # 等待页面加载
        await page.wait_for_load_state("networkidle")
        
        print("正在检查GitHub Pages配置状态...")
        
        # 等待一段时间确保页面加载完成
        await page.wait_for_timeout(3000)
        
        # 截图以供检查
        await page.screenshot(path="github_pages_status.png", full_page=True)
        print("已保存当前配置页面截图到 github_pages_status.png")
        
        # 尝试获取页面中的关键信息
        try:
            # 查找源配置信息
            source_info = await page.query_selector("div:has-text('Source') + div")
            if source_info:
                source_text = await source_info.text_content()
                print(f"源配置信息: {source_text}")
            
            # 查找部署状态
            status_elements = await page.query_selector_all("div:has-text('Status') + div, div:has-text('status') + div")
            for status_element in status_elements:
                if await status_element.is_visible():
                    status_text = await status_element.text_content()
                    print(f"部署状态: {status_text}")
                    break
            
            # 查找站点URL
            url_elements = await page.query_selector_all("a[href*='github.io']")
            for url_element in url_elements:
                if await url_element.is_visible():
                    url_text = await url_element.get_attribute("href")
                    print(f"站点URL: {url_text}")
                    break
                    
        except Exception as e:
            print(f"获取配置信息时出错: {e}")
        
        # 关闭浏览器
        await browser.close()

if __name__ == "__main__":
    asyncio.run(check_github_pages_status())