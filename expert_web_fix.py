#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
专家级Web界面修复脚本
"""

import os
import sys
import time
import subprocess
import requests
import signal
import json
from pathlib import Path

class ExpertWebFixer:
    """专家级Web界面修复器"""
    
    def __init__(self):
        self.base_url = "http://localhost:8501"
        self.process = None
        self.max_retries = 5
        self.retry_delay = 10
        
    def stop_existing_services(self):
        """停止现有服务"""
        print("🛑 停止现有服务...")
        
        try:
            # 停止Python进程
            subprocess.run(['taskkill', '/F', '/IM', 'python.exe'], 
                         capture_output=True, timeout=5)
            print("✅ Python进程已停止")
        except:
            print("⚠️ 无法停止Python进程")
        
        try:
            # 停止Streamlit进程
            subprocess.run(['taskkill', '/F', '/IM', 'streamlit.exe'], 
                         capture_output=True, timeout=5)
            print("✅ Streamlit进程已停止")
        except:
            print("⚠️ 无法停止Streamlit进程")
        
        # 等待进程完全停止
        time.sleep(3)
    
    def clear_cache(self):
        """清理缓存"""
        print("🧹 清理缓存...")
        
        cache_dirs = [
            os.path.expanduser("~/.streamlit"),
            os.path.join(os.getcwd(), ".streamlit"),
            os.path.join(os.getcwd(), "__pycache__")
        ]
        
        for cache_dir in cache_dirs:
            if os.path.exists(cache_dir):
                try:
                    import shutil
                    shutil.rmtree(cache_dir)
                    print(f"✅ 清理缓存: {cache_dir}")
                except:
                    print(f"⚠️ 无法清理缓存: {cache_dir}")
    
    def validate_config(self):
        """验证配置文件"""
        print("📋 验证配置文件...")
        
        config_files = [
            "config/.env",
            "config/models.txt",
            "requirements.txt"
        ]
        
        all_valid = True
        
        for config_file in config_files:
            config_path = Path(config_file)
            if config_path.exists():
                try:
                    with open(config_path, 'r', encoding='utf-8') as f:
                        content = f.read().strip()
                        if content:
                            print(f"✅ {config_file} 有效")
                        else:
                            print(f"❌ {config_file} 为空")
                            all_valid = False
                except Exception as e:
                    print(f"❌ {config_file} 读取错误: {e}")
                    all_valid = False
            else:
                print(f"❌ {config_file} 不存在")
                all_valid = False
        
        return all_valid
    
    def start_web_service(self):
        """启动Web服务"""
        print("🚀 启动Web服务...")
        
        # 检查visual_test_interface.py是否存在
        script_path = Path("visual_test_interface.py")
        if not script_path.exists():
            print("❌ visual_test_interface.py 不存在")
            return False
        
        # 验证依赖
        try:
            import streamlit
            import pandas
            import numpy
            import matplotlib
            import seaborn
            import pydantic
            import requests
            import yaml
            import dotenv
            print("✅ 所有依赖验证通过")
        except ImportError as e:
            print(f"❌ 依赖验证失败: {e}")
            return False
        
        # 启动服务
        try:
            # 使用Streamlit启动
            cmd = [
                sys.executable, "-m", "streamlit", "run", 
                str(script_path),
                "--server.port=8501",
                "--server.headless=true",
                "--server.enableCORS=true",
                "--server.runOnSave=true",
                "--server.fileWatcherType=none"
            ]
            
            self.process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                cwd=Path(".")
            )
            
            print("✅ Web服务启动命令已执行")
            return True
            
        except Exception as e:
            print(f"❌ 启动Web服务失败: {e}")
            return False
    
    def wait_for_service(self):
        """等待服务启动"""
        print("⏳ 等待服务启动...")
        
        for i in range(self.max_retries):
            try:
                response = requests.get(f"{self.base_url}/", timeout=5)
                if response.status_code == 200:
                    print(f"✅ 服务启动成功 (尝试 {i+1}/{self.max_retries})")
                    return True
            except:
                print(f"⏳ 等待服务启动... (尝试 {i+1}/{self.max_retries})")
                time.sleep(self.retry_delay)
        
        print("❌ 服务启动超时")
        return False
    
    def test_service_health(self):
        """测试服务健康状态"""
        print("🏥 测试服务健康状态...")
        
        tests = [
            ("首页", "/"),
            ("API模型", "/api/models"),
            ("API测试", "/api/tests"),
            ("API结果", "/api/results"),
            ("健康检查", "/api/health")
        ]
        
        all_passed = True
        
        for test_name, endpoint in tests:
            try:
                start_time = time.time()
                response = requests.get(f"{self.base_url}{endpoint}", timeout=10)
                end_time = time.time()
                
                if response.status_code == 200:
                    response_time = end_time - start_time
                    print(f"✅ {test_name}: {response.status_code} ({response_time:.2f}s)")
                else:
                    print(f"❌ {test_name}: {response.status_code}")
                    all_passed = False
                    
            except Exception as e:
                print(f"❌ {test_name}: 连接失败 - {e}")
                all_passed = False
        
        return all_passed
    
    def run_comprehensive_test(self):
        """运行综合测试"""
        print("🧪 运行综合测试...")
        
        # 测试数据
        test_data = {
            "pillar_name": "pillar_01_logic",
            "prompt": "If all roses are flowers and some flowers fade quickly, can we conclude that some roses fade quickly? Explain your reasoning step by step.",
            "model_name": "test_model"
        }
        
        try:
            # 测试run_test端点
            response = requests.post(
                f"{self.base_url}/api/run_test",
                json=test_data,
                headers={"Content-Type": "application/json"},
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                if "success" in result and "score" in result:
                    print("✅ run_test端点测试通过")
                    return True
                else:
                    print("❌ run_test端点返回格式错误")
                    return False
            else:
                print(f"❌ run_test端点返回错误: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"❌ run_test端点测试失败: {e}")
            return False
    
    def generate_report(self):
        """生成修复报告"""
        print("📊 生成修复报告...")
        
        report = {
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "base_url": self.base_url,
            "status": "SUCCESS",
            "tests": {
                "config_validation": True,
                "service_startup": True,
                "health_check": True,
                "comprehensive_test": True
            },
            "recommendations": [
                "定期运行此脚本以保持服务状态",
                "监控服务性能和响应时间",
                "定期备份配置文件",
                "保持依赖包更新"
            ]
        }
        
        # 保存报告
        report_file = Path("test_reports/web_interface_fix_report.json")
        report_file.parent.mkdir(parents=True, exist_ok=True)
        
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        print(f"📄 修复报告已保存: {report_file}")
        return report
    
    def fix_web_interface(self):
        """修复Web界面的主方法"""
        print("🎯 LLM Advanced Testing Suite - 专家级Web界面修复")
        print("=" * 70)
        
        # 执行修复步骤
        self.stop_existing_services()
        self.clear_cache()
        
        if not self.validate_config():
            print("❌ 配置文件验证失败")
            return False
        
        if not self.start_web_service():
            print("❌ Web服务启动失败")
            return False
        
        if not self.wait_for_service():
            print("❌ 服务启动超时")
            return False
        
        if not self.test_service_health():
            print("❌ 健康检查失败")
            return False
        
        if not self.run_comprehensive_test():
            print("❌ 综合测试失败")
            return False
        
        # 生成报告
        report = self.generate_report()
        
        print("\n🎉 Web界面修复完成！")
        print(f"🌐 访问地址: {self.base_url}")
        print("✅ 所有测试通过，服务已正常运行")
        
        return True

def main():
    """主函数"""
    fixer = ExpertWebFixer()
    success = fixer.fix_web_interface()
    
    if success:
        print("\n🚀 Web界面修复成功！")
        sys.exit(0)
    else:
        print("\n❌ Web界面修复失败！")
        sys.exit(1)

if __name__ == "__main__":
    main()