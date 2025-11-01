import requests

def check_github_pages_status():
    owner = "ptreezh"
    repo = "llmtest24"
    
    # 首先尝试获取GitHub Pages配置
    headers = {
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28"
    }
    
    url = f"https://api.github.com/repos/{owner}/{repo}/pages"
    
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        pages_config = response.json()
        print("GitHub Pages配置信息:")
        print(f"状态: {pages_config.get('status', 'unknown')}")
        print(f"URL: {pages_config.get('html_url', 'unknown')}")
        source = pages_config.get('source', {})
        print(f"源分支: {source.get('branch', 'unknown')}")
        print(f"源路径: {source.get('path', 'unknown')}")
        print(f"构建类型: {pages_config.get('build_type', 'unknown')}")
    else:
        print(f"无法获取GitHub Pages配置，状态码: {response.status_code}")
        print("这可能表示GitHub Pages尚未在仓库中配置")

    print("\n检查网站访问...")
    website_url = f"https://{owner}.github.io/{repo}/"
    website_response = requests.get(website_url)
    print(f"网站访问状态: {website_response.status_code}")
    
    if website_response.status_code == 404:
        print("网站返回404，GitHub Pages可能还未完成部署")
        print("GitHub Pages部署通常需要几分钟时间，请稍后再试")
    elif website_response.status_code == 200:
        print("网站可以正常访问！")
    else:
        print(f"网站访问状态: {website_response.status_code}")

if __name__ == "__main__":
    check_github_pages_status()