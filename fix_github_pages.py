import asyncio
from playwright.async_api import async_playwright

async def check_and_trigger_github_pages():
    async with async_playwright() as p:
        # 启动浏览器
        browser = await p.chromium.launch(channel="msedge", headless=False)
        page = await browser.new_page()
        
        # 访问GitHub Pages设置页面
        await page.goto("https://github.com/ptreezh/llmtest24/settings/pages")
        
        # 等待页面加载
        await page.wait_for_load_state("networkidle")
        
        print("正在检查和配置GitHub Pages...")
        
        # 等待一段时间确保页面加载完成
        await page.wait_for_timeout(5000)
        
        # 查找并尝试重新配置GitHub Pages
        try:
            # 查找"Deploy from a branch"选项
            deploy_from_branch_option = await page.query_selector("button:has-text('Deploy from a branch'), div:has-text('Deploy from a branch')")
            if deploy_from_branch_option:
                await deploy_from_branch_option.click()
                print("已点击'Deploy from a branch'选项")
            else:
                print("未找到'Deploy from a branch'选项")
            
            # 等待选择器出现
            await page.wait_for_timeout(2000)
            
            # 尝试选择main分支
            branch_selectors = await page.query_selector_all("select")
            for selector in branch_selectors:
                if await selector.is_visible():
                    try:
                        await page.select_option(selector, "main")
                        print("已选择main分支")
                        break
                    except:
                        continue
            
            # 尝试选择/docs路径
            path_selectors = await page.query_selector_all("select")
            for selector in path_selectors:
                if await selector.is_visible():
                    try:
                        await page.select_option(selector, "/docs")
                        print("已选择/docs路径")
                        break
                    except:
                        continue
            
            # 查找保存或更新按钮并点击
            save_buttons = await page.query_selector_all("button")
            for button in save_buttons:
                if await button.is_visible() and await button.is_enabled():
                    button_text = await button.text_content()
                    if "save" in button_text.lower() or "update" in button_text.lower() or "configure" in button_text.lower():
                        await button.click()
                        print(f"已点击保存/配置按钮: {button_text}")
                        break
                        
            # 等待配置保存
            await page.wait_for_timeout(3000)
            
        except Exception as e:
            print(f"配置GitHub Pages时出错: {e}")
        
        # 截图以供检查
        await page.screenshot(path="github_pages_final_config.png", full_page=True)
        print("已保存最终配置截图到 github_pages_final_config.png")
        
        # 等待配置生效
        await page.wait_for_timeout(5000)
        
        # 关闭浏览器
        await browser.close()

if __name__ == "__main__":
    asyncio.run(check_and_trigger_github_pages())