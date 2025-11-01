#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
云端服务连接缓存管理
记住成功连接的云服务，避免重复试错
"""

import json
import os
import time
from typing import Dict, List, Optional
from datetime import datetime, timedelta

class CloudConnectionCache:
    """云端服务连接缓存管理器"""
    
    def __init__(self, cache_file: str = "cloud_connection_cache.json"):
        self.cache_file = cache_file
        self.cache_data = self._load_cache()
        self.session_successful_services = set()  # 当前会话成功的服务
        
    def _load_cache(self) -> Dict:
        """加载缓存数据"""
        if os.path.exists(self.cache_file):
            try:
                with open(self.cache_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception:
                pass
        
        return {
            "successful_services": {},  # 服务名 -> 最后成功时间
            "failed_services": {},      # 服务名 -> 最后失败时间
            "preferred_order": [],      # 优先顺序
            "last_updated": None
        }
    
    def _save_cache(self):
        """保存缓存数据"""
        self.cache_data["last_updated"] = datetime.now().isoformat()
        try:
            with open(self.cache_file, 'w', encoding='utf-8') as f:
                json.dump(self.cache_data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"⚠️ 保存连接缓存失败: {e}")
    
    def mark_service_success(self, service_name: str):
        """标记服务连接成功"""
        current_time = datetime.now().isoformat()
        self.cache_data["successful_services"][service_name] = current_time
        self.session_successful_services.add(service_name)
        
        # 从失败列表中移除
        if service_name in self.cache_data["failed_services"]:
            del self.cache_data["failed_services"][service_name]
        
        # 更新优先顺序
        self._update_preferred_order(service_name, success=True)
        self._save_cache()
        print(f"✅ 记录服务成功: {service_name}")
    
    def mark_service_failed(self, service_name: str, reason: str = ""):
        """标记服务连接失败"""
        current_time = datetime.now().isoformat()
        self.cache_data["failed_services"][service_name] = {
            "time": current_time,
            "reason": reason
        }
        self._update_preferred_order(service_name, success=False)
        self._save_cache()
        print(f"❌ 记录服务失败: {service_name} - {reason}")
    
    def _update_preferred_order(self, service_name: str, success: bool):
        """更新服务优先顺序"""
        if service_name in self.cache_data["preferred_order"]:
            self.cache_data["preferred_order"].remove(service_name)
        
        if success:
            # 成功的服务放到前面
            self.cache_data["preferred_order"].insert(0, service_name)
        else:
            # 失败的服务放到后面
            self.cache_data["preferred_order"].append(service_name)
    
    def get_preferred_services(self, available_services: List[str]) -> List[str]:
        """获取按优先级排序的服务列表"""
        # 当前会话成功的服务优先
        session_successful = [s for s in available_services if s in self.session_successful_services]
        
        # 历史成功的服务
        historical_successful = []
        for service in self.cache_data["preferred_order"]:
            if (service in available_services and 
                service not in session_successful and
                service in self.cache_data["successful_services"]):
                historical_successful.append(service)
        
        # 未测试过的服务
        untested = [s for s in available_services 
                   if s not in session_successful and 
                   s not in self.cache_data["preferred_order"]]
        
        # 最近失败的服务放最后
        recently_failed = []
        for service in available_services:
            if (service in self.cache_data["failed_services"] and
                service not in session_successful):
                failed_info = self.cache_data["failed_services"][service]
                failed_time = datetime.fromisoformat(failed_info["time"])
                # 如果失败时间在1小时内，放到最后
                if datetime.now() - failed_time < timedelta(hours=1):
                    recently_failed.append(service)
        
        # 组合最终顺序
        final_order = session_successful + historical_successful + untested
        final_order = [s for s in final_order if s not in recently_failed] + recently_failed
        
        return final_order
    
    def should_skip_service(self, service_name: str) -> bool:
        """判断是否应该跳过某个服务"""
        if service_name in self.session_successful_services:
            return False  # 当前会话成功的不跳过
        
        if service_name in self.cache_data["failed_services"]:
            failed_info = self.cache_data["failed_services"][service_name]
            failed_time = datetime.fromisoformat(failed_info["time"])
            # 如果在30分钟内失败过，跳过
            if datetime.now() - failed_time < timedelta(minutes=30):
                print(f"⏭️ 跳过最近失败的服务: {service_name}")
                return True
        
        return False
    
    def get_cache_stats(self) -> Dict:
        """获取缓存统计信息"""
        return {
            "successful_count": len(self.cache_data["successful_services"]),
            "failed_count": len(self.cache_data["failed_services"]),
            "session_successful": list(self.session_successful_services),
            "preferred_order": self.cache_data["preferred_order"][:5]  # 前5个
        }

# 全局缓存实例
connection_cache = CloudConnectionCache()