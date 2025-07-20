"""
角色独立性测试基础类

提供所有独立性测试的通用功能和接口
"""

import time
import json
import os
from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
from pathlib import Path

class IndependenceTestBase(ABC):
    """角色独立性测试基础类"""
    
    def __init__(self, config: Dict[str, Any]):
        """初始化独立性测试基类"""
        self.config = config
        self.model_name = config.get('model_name', 'test_model')
        self.output_dir = config.get('output_dir', 'testout')
        self.model_manager = None  # 实际实现中需要注入模型管理器
        
        # 定义标准角色提示词
        self.role_prompts = {
            'software_engineer': '你是一位经验丰富的软件工程师，专注于系统设计和代码优化。你有10年以上的开发经验，熟悉多种编程语言和架构模式。',
            'data_scientist': '你是一位专业的数据科学家，擅长数据分析和机器学习。你精通统计学、Python和各种机器学习算法。',
            'product_manager': '你是一位产品经理，负责产品规划和用户体验设计。你有丰富的市场分析和用户研究经验。',
            'security_expert': '你是一位网络安全专家，专注于系统安全和风险评估。你熟悉各种安全威胁和防护措施。'
        }
        
        # 确保输出目录存在
        os.makedirs(self.output_dir, exist_ok=True)
        
        # 测试状态
        self.test_start_time = None
        self.test_end_time = None
        self.current_role = None
        
    @abstractmethod
    def run_experiment(self) -> Dict[str, Any]:
        """
        运行实验的抽象方法
        
        Returns:
            实验结果字典
        """
        pass
    
    def start_test(self, test_name: str):
        """开始测试"""
        self.test_start_time = time.time()
        print(f"🚀 开始 {test_name} 测试...")
    
    def end_test(self, test_name: str):
        """结束测试"""
        self.test_end_time = time.time()
        duration = self.test_end_time - self.test_start_time if self.test_start_time else 0
        print(f"✅ {test_name} 测试完成 (耗时: {duration:.2f}秒)")
        return duration
    
    def save_results(self, results: Dict[str, Any], filename: str):
        """保存测试结果"""
        filepath = os.path.join(self.output_dir, filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
        print(f"📁 结果已保存到: {filepath}")
    
    def log_test_step(self, step: str, details: str = ""):
        """记录测试步骤"""
        timestamp = time.strftime('%H:%M:%S')
        role_info = f"[{self.current_role}]" if self.current_role else ""
        print(f"[{timestamp}] {role_info} {step}")
        if details:
            print(f"    {details}")
    
    def validate_config(self) -> bool:
        """验证配置有效性"""
        required_keys = ['model_name', 'test_roles']
        
        for key in required_keys:
            if key not in self.config:
                print(f"❌ 配置缺少必需的键: {key}")
                return False
        
        if not self.config['test_roles']:
            print(f"❌ test_roles 不能为空")
            return False
            
        return True
    
    def get_role_prompt(self, role: str) -> str:
        """获取角色提示词"""
        role_prompts = {
            'software_engineer': "你是一名资深软件工程师，专注于系统架构设计和代码优化。",
            'data_scientist': "你是一名数据科学家，擅长数据分析、机器学习和统计建模。",
            'product_manager': "你是一名产品经理，负责产品规划、需求分析和用户体验设计。",
            'security_expert': "你是一名网络安全专家，专注于系统安全、风险评估和防护策略。",
            'marketing_specialist': "你是一名市场营销专家，擅长品牌推广、市场分析和营销策略。",
            'financial_analyst': "你是一名金融分析师，专注于财务分析、投资评估和风险管理。"
        }
        
        return role_prompts.get(role, f"你是一名{role}专家。")
    
    def calculate_base_score(self, responses: List[str], criteria: Dict[str, float]) -> float:
        """计算基础评分"""
        if not responses:
            return 0.0
        
        total_score = 0.0
        total_weight = sum(criteria.values())
        
        for criterion, weight in criteria.items():
            criterion_score = self._evaluate_criterion(responses, criterion)
            total_score += criterion_score * weight
        
        return total_score / total_weight if total_weight > 0 else 0.0
    
    def _evaluate_criterion(self, responses: List[str], criterion: str) -> float:
        """评估特定标准"""
        # 这里可以根据不同标准实现具体的评估逻辑
        # 目前返回基于响应质量的简单评分
        
        if not responses:
            return 0.0
        
        # 基于响应长度和内容的简单评分
        avg_length = sum(len(r) for r in responses) / len(responses)
        
        if criterion == 'consistency':
            # 一致性评分：基于响应间的相似度
            return min(1.0, avg_length / 200)  # 假设200字符为基准
        elif criterion == 'relevance':
            # 相关性评分：基于响应的相关性
            return min(1.0, avg_length / 150)
        elif criterion == 'quality':
            # 质量评分：基于响应的质量
            return min(1.0, avg_length / 100)
        else:
            return 0.5  # 默认评分

