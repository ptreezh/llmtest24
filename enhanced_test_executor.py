#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Enhanced Test Executor
增强版测试执行器 - 支持完整的测试提取和执行
"""

import sys
import os
import re
import json
import time
import ast
from pathlib import Path
from typing import Dict, List, Any, Optional

# Add project root to path
sys.path.append(str(Path(__file__).parent))
sys.path.append(str(Path(__file__).parent / "scripts" / "utils"))

try:
    import cloud_services
    CLOUD_SERVICES_AVAILABLE = True
except:
    CLOUD_SERVICES_AVAILABLE = False

class TestExtractor:
    """测试内容提取器"""
    
    def __init__(self):
        self.test_cache = {}
    
    def extract_test_content(self, test_file: Path) -> Dict[str, Any]:
        """从测试文件中提取测试内容"""
        if test_file.name in self.test_cache:
            return self.test_cache[test_file.name]
        
        try:
            with open(test_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 提取测试信息
            test_info = {
                "file": test_file.name,
                "path": str(test_file),
                "pillar": self._extract_pillar_number(test_file.name),
                "title": self._extract_title(content),
                "description": self._extract_description(content),
                "prompt": self._extract_prompt(content),
                "assessment_criteria": self._extract_assessment_criteria(content),
                "category": self._get_category(test_file.name)
            }
            
            self.test_cache[test_file.name] = test_info
            return test_info
            
        except Exception as e:
            return {
                "file": test_file.name,
                "path": str(test_file),
                "error": str(e),
                "pillar": 0,
                "title": test_file.name,
                "description": "无法提取测试描述",
                "prompt": "默认测试prompt",
                "assessment_criteria": "默认评估标准",
                "category": "未知"
            }
    
    def _extract_pillar_number(self, filename: str) -> int:
        """提取pillar编号"""
        match = re.search(r'test_pillar_(\d+)', filename)
        if match:
            return int(match.group(1))
        elif 'pillar_25' in filename:
            return 25
        return 0
    
    def _extract_title(self, content: str) -> str:
        """提取测试标题"""
        # 查找PILLAR_NAME或title
        patterns = [
            r'PILLAR_NAME\s*=\s*["\'](.*?)["\']',
            r'title\s*=\s*["\'](.*?)["\']',
            r'["\']([^"\']*(?:测试|Test|Pillar)[^"\']*)["\']'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, content, re.MULTILINE)
            if match:
                return match.group(1).strip()
        
        return "未命名测试"
    
    def _extract_description(self, content: str) -> str:
        """提取测试描述"""
        patterns = [
            r'PILLAR_DESCRIPTION\s*=\s*["\'](.*?)["\']',
            r'description\s*=\s*["\'](.*?)["\']'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, content, re.MULTILINE)
            if match:
                return match.group(1).strip()
        
        return "无描述"
    
    def _extract_prompt(self, content: str) -> str:
        """提取测试prompt"""
        # 尝试提取PROMPT
        prompt_patterns = [
            r'PROMPT\s*=\s*"""(.*?)"""',
            r'PROMPT\s*=\s*["\'](.*?)["\']',
            r'prompt\s*=\s*"""(.*?)"""',
            r'prompt\s*=\s*["\'](.*?)["\']'
        ]
        
        for pattern in prompt_patterns:
            matches = re.findall(pattern, content, re.DOTALL)
            if matches:
                return matches[0].strip()
        
        # 如果找不到PROMPT，尝试提取其他内容
        # 查找问题文本
        question_match = re.search(r'问题[：:](.*?)(?:\n\n|\n[一二三四五六七八九十]、)', content, re.DOTALL)
        if question_match:
            return question_match.group(1).strip()
        
        return "请完成能力测试"
    
    def _extract_assessment_criteria(self, content: str) -> str:
        """提取评估标准"""
        patterns = [
            r'ASSESSMENT_CRITERIA\s*=\s*"""(.*?)"""',
            r'assessment_criteria\s*=\s*"""(.*?)"""',
            r'评估标准[：:](.*?)(?:\n\n|\n---|$)'
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, content, re.DOTALL)
            if matches:
                return matches[0].strip()
        
        return "标准评估"
    
    def _get_category(self, filename: str) -> str:
        """获取测试类别"""
        pillar = self._extract_pillar_number(filename)
        if 1 <= pillar <= 8:
            return "基础能力"
        elif 9 <= pillar <= 19:
            return "高级能力"
        elif 20 <= pillar <= 24:
            return "前沿能力"
        elif pillar == 25:
            return "专项测试"
        else:
            return "其他"

class TestExecutor:
    """测试执行器"""
    
    def __init__(self):
        self.extractor = TestExtractor()
        self.results = []
    
    def execute_test(self, test_info: Dict[str, Any], model_key: str, **options) -> Dict[str, Any]:
        """执行单个测试"""
        try:
            # 解析模型信息
            if '-' in model_key:
                service, model = model_key.split('-', 1)
            else:
                service = model_key
                model = model_key
            
            # 调用真实LLM
            start_time = time.time()
            
            if CLOUD_SERVICES_AVAILABLE:
                response = cloud_services.call_cloud_service(
                    service, model, test_info["prompt"]
                )
            else:
                response = f"模拟响应: {test_info['prompt'][:100]}..."
            
            end_time = time.time()
            
            # 分析响应质量
            analysis = self._analyze_response(response, test_info)
            
            result = {
                "test_file": test_info["file"],
                "test_title": test_info["title"],
                "pillar": test_info["pillar"],
                "category": test_info["category"],
                "model": model_key,
                "service": service,
                "prompt": test_info["prompt"],
                "response": response,
                "response_length": len(response) if response else 0,
                "execution_time": end_time - start_time,
                "analysis": analysis,
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                "status": "completed"
            }
            
            self.results.append(result)
            return result
            
        except Exception as e:
            error_result = {
                "test_file": test_info["file"],
                "test_title": test_info.get("title", test_info["file"]),
                "pillar": test_info.get("pillar", 0),
                "category": test_info.get("category", "未知"),
                "model": model_key,
                "error": str(e),
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                "status": "failed"
            }
            
            self.results.append(error_result)
            return error_result
    
    def _analyze_response(self, response: str, test_info: Dict[str, Any]) -> Dict[str, Any]:
        """分析响应质量"""
        if not response:
            return {"quality": "无响应", "score": 0}
        
        analysis = {
            "quality": "待评估",
            "score": 0,
            "strengths": [],
            "weaknesses": []
        }
        
        # 基本质量评估
        response_length = len(response)
        if response_length < 50:
            analysis["quality"] = "过短"
            analysis["score"] = 1
            analysis["weaknesses"].append("响应过短")
        elif response_length < 200:
            analysis["quality"] = "一般"
            analysis["score"] = 2
        elif response_length < 500:
            analysis["quality"] = "良好"
            analysis["score"] = 3
        else:
            analysis["quality"] = "优秀"
            analysis["score"] = 4
            analysis["strengths"].append("响应详细")
        
        # 内容相关性评估
        if "测试" in response or "answer" in response.lower():
            analysis["strengths"].append("内容相关")
        else:
            analysis["weaknesses"].append("内容相关性不足")
        
        return analysis
    
    def get_test_files(self) -> List[Dict[str, Any]]:
        """获取所有测试文件信息"""
        test_files = []
        tests_dir = Path("tests")
        
        if tests_dir.exists():
            for file in tests_dir.glob("test_pillar_*.py"):
                test_info = self.extractor.extract_test_content(file)
                test_files.append(test_info)
        
        return sorted(test_files, key=lambda x: x["pillar"])
    
    def generate_comprehensive_report(self) -> Dict[str, Any]:
        """生成综合报告"""
        if not self.results:
            return {}
        
        # 基本统计
        total_tests = len(self.results)
        successful_tests = len([r for r in self.results if r["status"] == "completed"])
        failed_tests = total_tests - successful_tests
        
        # 按类别统计
        category_stats = {}
        model_stats = {}
        
        for result in self.results:
            # 类别统计
            category = result["category"]
            if category not in category_stats:
                category_stats[category] = {"total": 0, "success": 0, "total_time": 0, "total_length": 0}
            category_stats[category]["total"] += 1
            if result["status"] == "completed":
                category_stats[category]["success"] += 1
                category_stats[category]["total_time"] += result.get("execution_time", 0)
                category_stats[category]["total_length"] += result.get("response_length", 0)
            
            # 模型统计
            model = result["model"]
            if model not in model_stats:
                model_stats[model] = {"total": 0, "success": 0, "avg_time": 0, "avg_length": 0}
            model_stats[model]["total"] += 1
            if result["status"] == "completed":
                model_stats[model]["success"] += 1
        
        # 计算平均值
        for category in category_stats:
            if category_stats[category]["success"] > 0:
                stats = category_stats[category]
                stats["avg_time"] = stats["total_time"] / stats["success"]
                stats["avg_length"] = stats["total_length"] / stats["success"]
        
        for model in model_stats:
            if model_stats[model]["success"] > 0:
                model_stats[model]["success_rate"] = model_stats[model]["success"] / model_stats[model]["total"] * 100
        
        # 生成报告
        report = {
            "test_summary": {
                "total_tests": total_tests,
                "successful_tests": successful_tests,
                "failed_tests": failed_tests,
                "success_rate": (successful_tests / total_tests * 100) if total_tests > 0 else 0,
                "test_date": time.strftime("%Y-%m-%d %H:%M:%S")
            },
            "category_statistics": category_stats,
            "model_statistics": model_stats,
            "detailed_results": self.results,
            "analysis_summary": {
                "total_response_length": sum(r.get("response_length", 0) for r in self.results),
                "total_execution_time": sum(r.get("execution_time", 0) for r in self.results),
                "avg_response_length": sum(r.get("response_length", 0) for r in self.results) / successful_tests if successful_tests > 0 else 0,
                "avg_execution_time": sum(r.get("execution_time", 0) for r in self.results) / successful_tests if successful_tests > 0 else 0
            }
        }
        
        return report

def main():
    """测试函数"""
    executor = TestExecutor()
    
    # 获取测试文件
    test_files = executor.get_test_files()
    print(f"Found {len(test_files)} test files")
    
    # 显示测试信息
    for test in test_files[:5]:  # 显示前5个
        print(f"Pillar {test['pillar']}: {test['title']}")
        print(f"  Category: {test['category']}")
        print(f"  Prompt: {test['prompt'][:100]}...")
        print()

if __name__ == "__main__":
    main()