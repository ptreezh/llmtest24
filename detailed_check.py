import asyncio
from playwright.async_api import async_playwright

async def check_github_pages_detailed():
    async with async_playwright() as p:
        # 启动浏览器
        browser = await p.chromium.launch(channel="msedge", headless=False)
        page = await browser.new_page()
        
        # 访问GitHub Pages设置页面
        await page.goto("https://github.com/ptreezh/llmtest24/settings/pages")
        
        # 等待页面加载
        await page.wait_for_load_state("networkidle")
        
        print("正在详细检查GitHub Pages配置...")
        
        # 等待一段时间确保页面加载完成
        await page.wait_for_timeout(5000)
        
        # 获取页面完整文本内容
        page_text = await page.text_content("body")
        print("页面文本内容:")
        print(page_text[:2000])  # 打印前2000个字符
        
        # 查找所有可见的文本元素
        try:
            text_elements = await page.query_selector_all("*")
            config_info = []
            
            for element in text_elements:
                if await element.is_visible():
                    text_content = await element.text_content()
                    if text_content and text_content.strip():
                        # 只收集包含配置相关信息的文本
                        text_lower = text_content.lower().strip()
                        if any(keyword in text_lower for keyword in 
                               ['source', 'branch', 'path', 'status', 'deploy', 'pages', 'main', 'master', 'docs']):
                            config_info.append(text_content.strip())
            
            print("\n可能的配置信息:")
            for info in config_info[:20]:  # 只显示前20条
                print(f"- {info}")
                
        except Exception as e:
            print(f"获取页面信息时出错: {e}")
        
        # 查找所有按钮和链接
        try:
            buttons = await page.query_selector_all("button, a")
            print(f"\n找到 {len(buttons)} 个按钮和链接")
            
            button_texts = []
            for button in buttons:
                if await button.is_visible():
                    text_content = await button.text_content()
                    if text_content and text_content.strip():
                        button_texts.append(text_content.strip())
            
            print("按钮和链接文本:")
            for text in button_texts[:15]:  # 只显示前15个
                print(f"- {text}")
                
        except Exception as e:
            print(f"检查按钮时出错: {e}")
        
        # 截图以供检查
        await page.screenshot(path="github_pages_detailed.png", full_page=True)
        print("\n已保存详细配置截图到 github_pages_detailed.png")
        
        # 关闭浏览器
        await browser.close()

if __name__ == "__main__":
    asyncio.run(check_github_pages_detailed())