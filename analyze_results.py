#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
LLM测评结果深度分析脚本
提供详细的统计分析、趋势分析和对比分析
"""

import os
import re
import json
from datetime import datetime
from collections import defaultdict

class LLMResultAnalyzer:
    def __init__(self, testout_dir="testout"):
        self.testout_dir = testout_dir
        self.pillar_mapping = {
            "creativity": "Pillar 9: 创意生成",
            "math": "Pillar 10: 数学推理", 
            "safety": "Pillar 11: 安全对齐",
            "persona": "Pillar 12: 角色扮演",
            "init": "Pillar 13: 指令解析",
            "persona_depth": "Pillar 14: 角色深度",
            "collaboration": "Pillar 15: 协作能力",
            "emergence": "Pillar 16: 涌现分析",
            "dag": "Pillar 17: 图谱生成",
            "fault_tolerance": "Pillar 18: 容错协调",
            "network_analysis": "Pillar 19: 网络分析"
        }
    
    def load_all_results(self):
        """加载所有测试结果"""
        results = []
        
        if not os.path.exists(self.testout_dir):
            return results
            
        for filename in os.listdir(self.testout_dir):
            if not filename.endswith('.txt'):
                continue
                
            filepath = os.path.join(self.testout_dir, filename)
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 解析文件内容
            result = self.parse_result_file(content, filename)
            if result:
                results.append(result)
        
        return results
    
    def parse_result_file(self, content, filename):
        """解析单个结果文件"""
        lines = content.split('\n')
        result = {
            "filename": filename,
            "case_id": "",
            "type": "",
            "prompt": "",
            "response": "",
            "pillar": self.get_pillar_from_filename(filename)
        }
        
        current_section = None
        for line in lines:
            if line.startswith("用例编号:"):
                result["case_id"] = line.split(":", 1)[1].strip()
            elif line.startswith("类型:"):
                result["type"] = line.split(":", 1)[1].strip()
            elif line.startswith("PROMPT:"):
                current_section = "prompt"
                continue
            elif line.startswith("MODEL RESPONSE"):
                current_section = "response"
                continue
            elif current_section == "prompt" and line.strip():
                result["prompt"] += line + "\n"
            elif current_section == "response" and line.strip():
                result["response"] += line + "\n"
        
        return result if result["response"].strip() else None
    
    def get_pillar_from_filename(self, filename):
        """从文件名推断Pillar类型"""
        for key in self.pillar_mapping:
            if key in filename:
                return key
        return "unknown"
    
    def analyze_response_quality(self, response):
        """分析响应质量的多个维度"""
        if not response:
            return {
                "length": 0,
                "sentence_count": 0,
                "avg_sentence_length": 0,
                "has_code": False,
                "has_structure": False,
                "completeness": 0
            }
        
        # 基本统计
        length = len(response)
        sentences = response.count('。') + response.count('.') + response.count('!')
        avg_sentence_length = length / max(sentences, 1)
        
        # 检查是否包含代码
        has_code = bool(re.search(r'```|`[^`]+`|#!/', response))
        
        # 检查是否有结构化内容
        has_structure = bool(re.search(r'[1-9]\.|[一二三四五六七八九十]、|##|###|\*\*', response))
        
        # 完整性评估（简单版本）
        completeness = min(100, length / 50)  # 假设50字符为基本完整
        
        return {
            "length": length,
            "sentence_count": sentences,
            "avg_sentence_length": avg_sentence_length,
            "has_code": has_code,
            "has_structure": has_structure,
            "completeness": completeness
        }
    
    def generate_comprehensive_report(self):
        """生成综合分析报告"""
        results = self.load_all_results()
        
        if not results:
            return "错误: 没有找到测试结果文件"
        
        # 按Pillar分组统计
        pillar_stats = defaultdict(list)
        for result in results:
            pillar_stats[result["pillar"]].append(result)
        
        report = f"""
# LLM测评结果深度分析报告

**生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**分析文件数**: {len(results)}个
**覆盖维度**: {len(pillar_stats)}个

## 📊 整体表现概览

"""
        
        # 整体统计
        total_responses = len(results)
        valid_responses = len([r for r in results if r["response"].strip()])
        avg_response_length = sum(len(r["response"]) for r in results) / max(len(results), 1)
        
        report += f"""
### 基础统计
- **总测试案例**: {total_responses}
- **有效响应**: {valid_responses} ({valid_responses/total_responses*100:.1f}%)
- **平均响应长度**: {avg_response_length:.0f} 字符

"""
        
        # 各Pillar详细分析
        report += "## 🔍 各维度详细分析\n"
        
        for pillar, pillar_results in pillar_stats.items():
            if pillar == "unknown":
                continue
                
            pillar_name = self.pillar_mapping.get(pillar, pillar)
            report += f"\n### {pillar_name}\n"
            
            # 统计该Pillar的表现
            case_count = len(pillar_results)
            avg_length = sum(len(r["response"]) for r in pillar_results) / max(case_count, 1)
            
            # 分析响应质量
            quality_stats = [self.analyze_response_quality(r["response"]) for r in pillar_results]
            avg_completeness = sum(q["completeness"] for q in quality_stats) / max(len(quality_stats), 1)
            code_ratio = sum(1 for q in quality_stats if q["has_code"]) / max(len(quality_stats), 1)
            structure_ratio = sum(1 for q in quality_stats if q["has_structure"]) / max(len(quality_stats), 1)
            
            report += f"""
- **测试案例数**: {case_count}
- **平均响应长度**: {avg_length:.0f} 字符
- **完整性评分**: {avg_completeness:.1f}/100
- **包含代码比例**: {code_ratio*100:.1f}%
- **结构化内容比例**: {structure_ratio*100:.1f}%

**具体案例**:
"""
            
            for result in pillar_results:
                quality = self.analyze_response_quality(result["response"])
                report += f"  - {result['type']}: {quality['length']}字符, 完整性{quality['completeness']:.0f}%\n"
        
        # 问题识别
        report += "\n## ⚠️ 问题识别与分析\n"
        
        # 找出问题案例
        short_responses = [r for r in results if len(r["response"]) < 50]
        empty_responses = [r for r in results if not r["response"].strip()]
        
        if empty_responses:
            report += f"\n### 无响应案例 ({len(empty_responses)}个)\n"
            for r in empty_responses:
                report += f"- {r['filename']}: {r['type']}\n"
        
        if short_responses:
            report += f"\n### 响应过短案例 ({len(short_responses)}个)\n"
            for r in short_responses:
                report += f"- {r['filename']}: {len(r['response'])}字符\n"
        
        # 改进建议
        report += "\n## 🎯 改进建议\n"
        
        if len(empty_responses) > len(results) * 0.2:
            report += "- **紧急**: 超过20%的测试无响应，建议检查模型配置和网络连接\n"
        
        if avg_response_length < 100:
            report += "- **重要**: 平均响应长度过短，建议优化提示词以获得更详细的回答\n"
        
        if code_ratio < 0.3:
            report += "- **建议**: 代码生成能力不足，考虑在提示词中明确要求代码输出\n"
        
        return report
    
    def save_analysis_data(self):
        """保存分析数据为JSON格式，便于进一步处理"""
        results = self.load_all_results()
        
        analysis_data = {
            "timestamp": datetime.now().isoformat(),
            "total_cases": len(results),
            "pillar_summary": {},
            "detailed_results": []
        }
        
        # 按Pillar汇总
        pillar_stats = defaultdict(list)
        for result in results:
            pillar_stats[result["pillar"]].append(result)
        
        for pillar, pillar_results in pillar_stats.items():
            if pillar == "unknown":
                continue
                
            analysis_data["pillar_summary"][pillar] = {
                "name": self.pillar_mapping.get(pillar, pillar),
                "case_count": len(pillar_results),
                "avg_response_length": sum(len(r["response"]) for r in pillar_results) / max(len(pillar_results), 1),
                "cases": [r["type"] for r in pillar_results]
            }
        
        # 详细结果
        for result in results:
            quality = self.analyze_response_quality(result["response"])
            analysis_data["detailed_results"].append({
                "filename": result["filename"],
                "pillar": result["pillar"],
                "type": result["type"],
                "case_id": result["case_id"],
                "quality_metrics": quality
            })
        
        # 保存到文件
        with open("analysis_data.json", 'w', encoding='utf-8') as f:
            json.dump(analysis_data, f, ensure_ascii=False, indent=2)
        
        return "analysis_data.json"

def main():
    analyzer = LLMResultAnalyzer()
    
    # 生成综合报告
    report = analyzer.generate_comprehensive_report()
    
    # 保存报告
    with open("comprehensive_analysis_report.md", 'w', encoding='utf-8') as f:
        f.write(report)
    
    # 保存分析数据
    data_file = analyzer.save_analysis_data()
    
    print("深度分析完成！")
    print("- 综合报告: comprehensive_analysis_report.md")
    print(f"- 分析数据: {data_file}")
    print("\n" + "="*50)
    print(report)

if __name__ == "__main__":
    main()
