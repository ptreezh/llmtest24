import requests
import time

def verify_web_interface():
    """验证Web界面可访问性"""
    print("验证Web界面可访问性...")
    
    # 测试不同的URL
    test_urls = [
        "http://localhost",
        "http://localhost/",
        "http://127.0.0.1",
        "http://127.0.0.1/"
    ]
    
    for url in test_urls:
        try:
            print(f"测试: {url}")
            response = requests.get(url, timeout=5)
            print(f"响应状态码: {response.status_code}")
            
            if response.status_code == 200:
                print(f"✅ 成功访问: {url}")
                return True, url
            else:
                print(f"⚠️ 响应: {response.status_code}")
        except Exception as e:
            print(f"❌ 连接失败: {e}")
        
        time.sleep(1)
    
    return False, None

if __name__ == "__main__":
    success, url = verify_web_interface()
    
    if success:
        print(f"\n✅ Web界面可访问: {url}")
    else:
        print("\n❌ Web界面不可访问")
        print("建议检查:")
        print("1. 本地Web服务是否正在运行")
        print("2. 服务是否绑定到正确的端口")
        print("3. 防火墙设置")
        print("4. visual_test_interface.py是否可以正常运行")