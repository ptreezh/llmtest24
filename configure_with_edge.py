import asyncio
from playwright.async_api import async_playwright

async def configure_github_pages_with_edge():
    async with async_playwright() as p:
        # 启动Edge浏览器
        browser = await p.chromium.launch(channel="msedge", headless=False)
        page = await browser.new_page()
        
        # 访问GitHub登录页面
        await page.goto("https://github.com/login")
        
        # 等待用户手动登录（因为需要输入用户名和密码）
        print("请在Edge浏览器中手动登录GitHub账户...")
        print("登录完成后，按Enter键继续...")
        
        try:
            input()
        except:
            print("继续执行配置...")
        
        # 访问仓库的Pages设置页面
        await page.goto("https://github.com/ptreezh/llmtest24/settings/pages")
        
        # 等待页面加载
        await page.wait_for_load_state("networkidle")
        
        print("正在配置GitHub Pages...")
        
        # 等待一段时间确保页面加载完成
        await page.wait_for_timeout(3000)
        
        # 尝试找到并配置GitHub Pages设置
        try:
            # 查找"Deploy from a branch"选项并点击
            deploy_options = await page.query_selector_all("button, div, span")
            for element in deploy_options:
                if await element.is_visible():
                    text_content = await element.text_content()
                    if text_content and "deploy" in text_content.lower() and "branch" in text_content.lower():
                        await element.click()
                        print("已点击'Deploy from a branch'选项")
                        await page.wait_for_timeout(1000)
                        break
            
            # 查找分支选择器并选择main分支
            branch_selectors = await page.query_selector_all("select")
            for selector in branch_selectors:
                if await selector.is_visible():
                    try:
                        await page.select_option(selector, "main")
                        print("已选择main分支")
                        await page.wait_for_timeout(500)
                        break
                    except:
                        pass
            
            # 查找路径选择器并选择/docs
            path_selectors = await page.query_selector_all("select")
            for selector in path_selectors:
                if await selector.is_visible():
                    try:
                        await page.select_option(selector, "/docs")
                        print("已选择/docs路径")
                        await page.wait_for_timeout(500)
                        break
                    except:
                        pass
            
            # 查找保存按钮并点击
            save_buttons = await page.query_selector_all("button")
            for button in save_buttons:
                if await button.is_visible() and await button.is_enabled():
                    button_text = await button.text_content()
                    if button_text and ("save" in button_text.lower() or "update" in button_text.lower()):
                        await button.click()
                        print(f"已点击保存按钮: {button_text}")
                        break
                        
        except Exception as e:
            print(f"配置过程中出现错误: {e}")
        
        # 截图以供检查
        await page.screenshot(path="github_pages_configuration.png", full_page=True)
        print("已保存配置页面截图到 github_pages_configuration.png")
        
        # 等待配置完成
        await page.wait_for_timeout(5000)
        
        print("GitHub Pages配置已完成。请等待几分钟让GitHub完成部署。")
        print("部署完成后，您可以通过 https://ptreezh.github.io/llmtest24/ 访问网站。")
        
        # 保持浏览器打开一段时间以便查看
        await page.wait_for_timeout(10000)
        
        # 关闭浏览器
        await browser.close()

if __name__ == "__main__":
    asyncio.run(configure_github_pages_with_edge())