import os
import sys
import subprocess
import time
import requests
from pathlib import Path

def check_firewall():
    """检查防火墙设置"""
    print("检查防火墙设置...")
    
    try:
        result = subprocess.run(['netsh', 'advfirewall', 'show', 'allprofiles'], 
                              capture_output=True, text=True, shell=True)
        if result.returncode == 0:
            print("防火墙状态:")
            print(result.stdout)
        else:
            print("无法获取防火墙状态")
    except:
        print("无法检查防火墙设置")

def check_visual_interface():
    """检查visual_test_interface.py"""
    print("检查visual_test_interface.py...")
    
    script_path = Path("visual_test_interface.py")
    if script_path.exists():
        print("visual_test_interface.py 存在")
        
        # 尝试导入并检查
        try:
            sys.path.append('.')
            import visual_test_interface
            print("visual_test_interface.py 可以导入")
        except Exception as e:
            print(f"visual_test_interface.py 导入失败: {e}")
    else:
        print("visual_test_interface.py 不存在")

def start_local_service():
    """启动本地服务"""
    print("启动本地服务...")
    
    try:
        # 使用streamlit启动服务
        cmd = [
            sys.executable, "-m", "streamlit", "run", 
            "visual_test_interface.py",
            "--server.port=8501",  # 使用8501端口避免与80端口冲突
            "--server.headless=true",
            "--server.enableCORS=true",
            "--server.runOnSave=true"
        ]
        
        print(f"执行命令: {' '.join(cmd)}")
        
        # 启动服务
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            cwd=Path(".")
        )
        
        print("服务启动命令已执行")
        return process
        
    except Exception as e:
        print(f"启动服务失败: {e}")
        return None

def main():
    print("=== TODO-6: 检查防火墙设置和启动服务 ===")
    
    check_firewall()
    check_visual_interface()
    
    # 启动服务
    process = start_local_service()
    
    if process:
        print("服务启动成功，等待服务就绪...")
        time.sleep(10)  # 等待服务启动
        
        # 测试服务
        try:
            response = requests.get("http://localhost:8501/", timeout=5)
            if response.status_code == 200:
                print("✅ 服务启动成功！")
                return True
            else:
                print(f"❌ 服务启动失败，状态码: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ 服务连接失败: {e}")
            return False
    else:
        print("❌ 服务启动失败")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)