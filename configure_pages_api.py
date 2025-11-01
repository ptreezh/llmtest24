import requests
import json

def configure_github_pages_api():
    # 需要一个GitHub个人访问令牌来调用API
    # 请确保您有一个有效的GitHub Personal Access Token
    token = input("请输入您的GitHub Personal Access Token: ")
    
    headers = {
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {token}",
        "X-GitHub-Api-Version": "2022-11-28"
    }
    
    owner = "ptreezh"
    repo = "llmtest24"
    
    # 配置GitHub Pages
    url = f"https://api.github.com/repos/{owner}/{repo}/pages"
    
    data = {
        "source": {
            "branch": "main",
            "path": "/docs"
        }
    }
    
    response = requests.post(url, headers=headers, json=data)
    
    if response.status_code == 201:
        print("GitHub Pages配置成功！")
        print(f"响应: {response.json()}")
    elif response.status_code == 200:
        print("GitHub Pages已存在，正在更新配置...")
        print(f"响应: {response.json()}")
    else:
        print(f"配置失败，状态码: {response.status_code}")
        print(f"错误信息: {response.text}")
        
        # 如果配置失败，尝试获取当前配置
        get_url = f"https://api.github.com/repos/{owner}/{repo}/pages"
        get_response = requests.get(get_url, headers=headers)
        print(f"\n当前配置: {get_response.status_code}")
        if get_response.status_code == 200:
            print(json.dumps(get_response.json(), indent=2))

if __name__ == "__main__":
    configure_github_pages_api()