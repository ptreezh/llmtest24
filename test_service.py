import requests
import time

def test_service():
    """测试服务是否可用"""
    print("测试服务是否可用...")
    
    try:
        response = requests.get("http://localhost:8501/", timeout=5)
        if response.status_code == 200:
            print("服务可用！")
            return True
        else:
            print(f"服务不可用，状态码: {response.status_code}")
            return False
    except Exception as e:
        print(f"服务连接失败: {e}")
        return False

if __name__ == "__main__":
    time.sleep(5)  # 等待服务启动
    success = test_service()
    print(f"测试结果: {'成功' if success else '失败'}")