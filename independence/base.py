#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
独立性测试基础类
"""

import time
import logging
from typing import Dict, List, Any, Optional
from datetime import datetime

import importlib.util
import os
from pathlib import Path

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 动态导入 cloud_services 模块
def _import_cloud_services():
    """动态导入 cloud_services 模块"""
    project_root = Path(__file__).parent.parent
    cloud_services_path = project_root / "scripts" / "utils" / "cloud_services.py"
    
    if not cloud_services_path.exists():
        logger.warning(f"cloud_services.py 文件不存在: {cloud_services_path}")
        # 返回一个模拟对象
        return {
            'call_cloud_service': lambda service_name, model_name, prompt, system_prompt: f"模拟响应: {prompt}",
            'CLOUD_SERVICES': {}
        }
    
    try:
        spec = importlib.util.spec_from_file_location("cloud_services", cloud_services_path)
        cloud_services = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(cloud_services)
        logger.info("成功导入 cloud_services 模块")
        return cloud_services
    except Exception as e:
        logger.error(f"导入 cloud_services 模块失败: {e}")
        # 返回一个模拟对象
        return {
            'call_cloud_service': lambda service_name, model_name, prompt, system_prompt: f"模拟响应: {prompt}",
            'CLOUD_SERVICES': {}
        }

# 执行动态导入
cloud_services = _import_cloud_services()

# 从模块中导入需要的变量
call_cloud_service = cloud_services['call_cloud_service'] if isinstance(cloud_services, dict) else getattr(cloud_services, 'call_cloud_service', None)
CLOUD_SERVICES = cloud_services['CLOUD_SERVICES'] if isinstance(cloud_services, dict) else getattr(cloud_services, 'CLOUD_SERVICES', {})


class IndependenceTestBase:
    """独立性测试基础类"""
    
    def __init__(self, config: Dict[str, Any] = None):
        """初始化基础测试类"""
        self.config = config or {}
        self.role_prompts = {}
        self.test_results = {}
        self.start_time = None
        self.end_time = None
        
    def start_test(self):
        """开始测试"""
        self.start_time = time.time()
        logger.info(f"开始测试: {self.__class__.__name__}")
        
    def end_test(self):
        """结束测试"""
        self.end_time = time.time()
        logger.info(f"结束测试: {self.__class__.__name__}")
        
    def get_test_duration(self) -> float:
        """获取测试持续时间"""
        if self.start_time is None:
            return 0.0
        end_time = self.end_time or time.time()
        return end_time - self.start_time
        
    def validate_config(self) -> bool:
        """
        验证测试配置是否有效。
        这是一个基础实现，子类可以重写以进行更具体的验证。
        """
        if not self.config:
            logger.error(f"[{self.__class__.__name__}] 配置为空。")
            return False
        
        # 基础验证：检查是否存在 model_name
        if 'model_name' not in self.config or not self.config['model_name']:
            logger.error(f"[{self.__class__.__name__}] 配置中缺少 'model_name'。")
            return False
            
        return True

    def _find_services_for_model(self, model_to_find: str) -> List[str]:
        """在CLOUD_SERVICES中查找所有可以提供指定模型的服务商"""
        providers = []
        for service_name, config in CLOUD_SERVICES.items():
            if model_to_find in config.get('models', []):
                providers.append(service_name)
        
        if providers:
            logger.info(f"为模型 '{model_to_find}' 找到 {len(providers)} 个服务商: {providers}")
        else:
            logger.warning(f"未找到可以提供模型 '{model_to_find}' 的服务商")
        return providers

    def _call_model_api(self, model: str, role_prompt: str, user_input: str, 
                       options: Dict[str, Any] = None) -> str:
        """
        调用模型API。
        此方法现在会调用 cloud_services.py 中的真实API函数。
        """
        logger.info(f"调用真实API for model {model}: {user_input[:50]}...")
        
        try:
            # 解析模型名称，格式为 "provider/model-name"
            provider, actual_model_name = model.split('/', 1)

            # --- 增强的 'auto' 逻辑 ---
            if provider == 'auto':
                logger.info(f"自动模式: 正在为模型 '{actual_model_name}' 查找服务商...")
                possible_providers = self._find_services_for_model(actual_model_name)
                if not possible_providers:
                    raise ValueError(f"自动模式下未找到可以提供模型 '{actual_model_name}' 的服务商")

                last_exception = None
                for service_to_use in possible_providers:
                    try:
                        logger.info(f"尝试使用服务商: {service_to_use}")
                        response_content = call_cloud_service(
                            service_name=service_to_use,
                            model_name=actual_model_name,
                            prompt=user_input,
                            system_prompt=role_prompt
                        )
                        logger.info(f"收到来自 {service_to_use} 的真实API响应: {response_content[:100]}...")
                        return response_content
                    except Exception as e:
                        logger.warning(f"调用 {service_to_use}/{actual_model_name} 失败: {e}")
                        last_exception = e
                
                # 如果所有服务商都失败了
                raise last_exception
            
            else:
                # --- 直接指定服务商的逻辑 ---
                response_content = call_cloud_service(
                    service_name=provider,
                    model_name=actual_model_name,
                    prompt=user_input,
                    system_prompt=role_prompt
                )
                logger.info(f"收到真实API响应: {response_content[:100]}...")
                return response_content
        except Exception as e:
            error_msg = f"[API_ERROR] {e}"
            logger.error(f"调用云服务时发生错误: {error_msg}")
            return error_msg
            
    def setup_test(self):
        """设置测试环境"""
        logger.info(f"设置测试环境: {self.__class__.__name__}")
        # 子类可以重写此方法以进行特定的设置
        pass

    def analyze_results(self):
        """分析测试结果"""
        logger.info(f"分析测试结果: {self.__class__.__name__}")
        # 子类可以重写此方法以进行特定的结果分析
        pass

    def generate_report(self):
        """生成测试报告"""
        logger.info(f"生成测试报告: {self.__class__.__name__}")
        # 子类可以重写此方法以生成特定的报告
        pass

    def run_experiment(self, model_name: str = None, test_config: Dict[str, Any] = None) -> Dict[str, Any]:
        """运行实验（子类需要重写）"""
        raise NotImplementedError("子类必须实现 run_experiment 方法")
        
    def run_test(self, model_name: str = None, role_prompt: str = None) -> Dict[str, Any]:
        """运行测试（兼容性方法）"""
        return self.run_experiment(model_name, {'role_prompt': role_prompt})
