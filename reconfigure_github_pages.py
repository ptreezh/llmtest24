import asyncio
from playwright.async_api import async_playwright

async def reconfigure_github_pages():
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
            input()
        except:
            print("继续执行配置...")
        
        # 访问仓库的Pages设置页面
        await page.goto("https://github.com/ptreezh/llmtest24/settings/pages")
        
        # 等待页面加载
        await page.wait_for_load_state("networkidle")
        
        print("正在重新配置GitHub Pages...")
        
        # 等待一段时间确保页面加载完成
        await page.wait_for_timeout(3000)
        
        # 尝试找到并点击"Deploy from a branch"选项
        try:
            deploy_button = await page.query_selector("button:has-text('Deploy from a branch')")
            if deploy_button:
                await deploy_button.click()
                print("已点击'Deploy from a branch'按钮")
                await page.wait_for_timeout(1000)
        except:
            print("未找到'Deploy from a branch'按钮")
        
        # 尝试选择master分支和/docs路径
        try:
            # 查找分支选择器
            branch_selectors = await page.query_selector_all("select")
            for selector in branch_selectors:
                if await selector.is_visible():
                    try:
                        await page.select_option(selector, "master")
                        print("已选择master分支")
                        break
                    except:
                        pass
            
            # 查找路径选择器
            path_selectors = await page.query_selector_all("select")
            for selector in path_selectors:
                if await selector.is_visible():
                    try:
                        await page.select_option(selector, "/docs")
                        print("已选择/docs路径")
                        break
                    except:
                        pass
        except Exception as e:
            print(f"选择分支或路径时出错: {e}")
        
        # 尝试保存配置
        try:
            save_buttons = await page.query_selector_all("button")
            for button in save_buttons:
                if await button.is_visible() and await button.is_enabled():
                    button_text = await button.text_content()
                    if "save" in button_text.lower() or "update" in button_text.lower():
                        await button.click()
                        print(f"已点击保存按钮: {button_text}")
                        break
        except Exception as e:
            print(f"保存配置时出错: {e}")
        
        # 截图以供检查
        await page.screenshot(path="github_pages_reconfig.png", full_page=True)
        print("已保存重新配置页面截图到 github_pages_reconfig.png")
        
        # 等待一段时间查看结果
        await page.wait_for_timeout(5000)
        
        # 关闭浏览器
        await browser.close()

if __name__ == "__main__":
    asyncio.run(reconfigure_github_pages())