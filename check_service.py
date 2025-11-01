import os
import sys
import subprocess
import time
import requests
from pathlib import Path

def check_service_status():
    """检查服务状态"""
    print("检查本地Web服务状态...")
    
    # 检查端口占用
    try:
        result = subprocess.run(['netstat', '-an', '|', 'findstr', ':80'], 
                              capture_output=True, text=True, shell=True)
        if result.returncode == 0:
            print("端口80被占用:")
            print(result.stdout)
        else:
            print("端口80未被占用")
    except:
        print("无法检查端口占用情况")
    
    # 检查Python进程
    try:
        result = subprocess.run(['tasklist', '|', 'findstr', 'python'], 
                              capture_output=True, text=True, shell=True)
        if result.returncode == 0:
            print("发现Python进程:")
            print(result.stdout)
        else:
            print("未发现Python进程")
    except:
        print("无法检查Python进程")
    
    # 检查visual_test_interface.py是否存在
    script_path = Path("visual_test_interface.py")
    if script_path.exists():
        print("visual_test_interface.py 存在")
    else:
        print("visual_test_interface.py 不存在")

def main():
    check_service_status()

if __name__ == "__main__":
    main()