import asyncio
from playwright.async_api import async_playwright
import os

async def configure_github_pages():
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
            print("继续执行配置...")
        
        # 访问仓库的Pages设置页面
        await page.goto("https://github.com/ptreezh/llmtest24/settings/pages")
        
        # 等待页面加载
        await page.wait_for_load_state("networkidle")
        
        print("正在配置GitHub Pages...")
        
        # 等待一段时间确保页面加载完成
        await page.wait_for_timeout(3000)
        
        # 尝试找到源设置相关的元素
        try:
            # 查找分支选择器 - GitHub Pages配置通常在下拉菜单中
            # 尝试多种可能的选择器
            selectors_to_try = [
                "select[name*='source']",
                "select[id*='source']",
                "select",
                "summary[role='button']:has-text('Deploy from a branch')",
                "button:has-text('Deploy from a branch')",
                "button:has-text('Source')",
                "div:has-text('Source') select"
            ]
            
            source_found = False
            for selector in selectors_to_try:
                try:
                    elements = await page.query_selector_all(selector)
                    if elements:
                        for element in elements:
                            if await element.is_visible():
                                if "summary" in selector or "button" in selector:
                                    # 如果是summary按钮或按钮，点击它展开选项
                                    await element.click()
                                    print(f"已点击源设置按钮: {selector}")
                                    await page.wait_for_timeout(1000)
                                else:
                                    # 如果是下拉菜单，选择master分支
                                    try:
                                        await page.select_option(element, "master")
                                        print(f"已选择master分支: {selector}")
                                        source_found = True
                                    except:
                                        # 如果选择失败，尝试点击下拉菜单
                                        await element.click()
                                        print(f"已点击下拉菜单: {selector}")
                                        await page.wait_for_timeout(1000)
                                break
                        if source_found:
                            break
                except Exception as e:
                    continue
            
            if not source_found:
                print("未找到源设置下拉菜单，尝试查找其他配置选项")
            
            # 查找并选择 /docs 路径
            try:
                path_selectors = [
                    "select[name*='path']",
                    "select[id*='path']",
                    "select:has(option:has-text('/docs'))",
                    "div:has-text('Path') select"
                ]
                
                for path_selector in path_selectors:
                    try:
                        elements = await page.query_selector_all(path_selector)
                        if elements:
                            for element in elements:
                                if await element.is_visible():
                                    await page.select_option(element, "/docs")
                                    print(f"已选择 /docs 路径: {path_selector}")
                                    break
                            break
                    except:
                        continue
            except:
                print("未找到路径选择器")
            
            # 查找保存或更新按钮
            save_selectors = [
                "button:has-text('Save')",
                "button:has-text('Update')",
                "button:has-text('Save source')",
                "input[type='submit'][name='commit']",
                "button:has-text('Save changes')",
                "button:has-text('Configure')",
                "button:has-text('Enable')"
            ]
            
            save_found = False
            for save_selector in save_selectors:
                try:
                    elements = await page.query_selector_all(save_selector)
                    if elements:
                        for element in elements:
                            if await element.is_visible() and await element.is_enabled():
                                await element.click()
                                print(f"已点击保存按钮: {save_selector}")
                                save_found = True
                                break
                        if save_found:
                            break
                except:
                    continue
            
            if not save_found:
                print("未找到保存按钮，尝试查找其他可能的提交按钮")
                
                # 尝试查找通用的提交按钮
                try:
                    commit_button = await page.query_selector("input[type='submit'], button[type='submit']")
                    if commit_button and await commit_button.is_visible() and await commit_button.is_enabled():
                        await commit_button.click()
                        print("已点击提交按钮")
                        save_found = True
                except:
                    pass
            
            if save_found:
                print("GitHub Pages配置已提交")
                # 等待配置完成
                await page.wait_for_timeout(5000)
            else:
                print("未能找到保存按钮，但GitHub Pages设置可能已经配置完成")
                
        except Exception as e:
            print(f"配置GitHub Pages时出错: {e}")
            print("页面内容可能已经改变，GitHub Pages可能已经配置完成")
        
        # 截图以供检查
        await page.screenshot(path="github_pages_config.png", full_page=True)
        print("已保存配置页面截图到 github_pages_config.png")
        
        # 关闭浏览器
        await browser.close()

if __name__ == "__main__":
    asyncio.run(configure_github_pages())