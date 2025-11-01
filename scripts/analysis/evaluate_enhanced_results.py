#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
加强测试结果评价脚本
专门评价涌现分析、数学推理、角色扮演的加强测试结果
"""

import os
import re
import json
from datetime import datetime
from typing import Dict, List, Tuple

class EnhancedResultsEvaluator:
    def __init__(self, testout_dir="testout_enhanced"):
        self.testout_dir = testout_dir
        self.evaluation_results = {}
    
    def load_test_result(self, filename: str) -> Dict:
        """加载测试结果文件"""
        filepath = os.path.join(self.testout_dir, filename)
        if not os.path.exists(filepath):
            return None
            
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        lines = content.split('\n')
        result = {
            "test_id": "",
            "type": "",
            "difficulty": "",
            "prompt": "",
            "response": ""
        }
        
        current_section = None
        for line in lines:
            if line.startswith("测试ID:"):
                result["test_id"] = line.split(":", 1)[1].strip()
            elif line.startswith("类型:"):
                result["type"] = line.split(":", 1)[1].strip()
            elif line.startswith("难度:"):
                result["difficulty"] = line.split(":", 1)[1].strip()
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
        
        return result
    
    def evaluate_enhanced_emergence(self, result: Dict) -> Tuple[int, str]:
        """评价加强版涌现分析"""
        response = result["response"].strip()
        if not response:
            return 0, "无响应内容"
        
        score = 0
        feedback = []
        max_score = 15  # 加强测试提高满分
        
        # 1. 多维度冲突识别 (4分)
        conflict_keywords = ["冲突", "矛盾", "对立", "悖论", "两难", "困境"]
        if any(word in response for word in conflict_keywords):
            score += 4
            feedback.append("✓ 识别了复杂冲突")
        
        # 2. 系统性分析 (4分)
        analysis_indicators = response.count("方面") + response.count("维度") + response.count("角度")
        if analysis_indicators >= 3:
            score += 4
            feedback.append("✓ 进行了多维度系统分析")
        elif analysis_indicators >= 1:
            score += 2
            feedback.append("⚠ 分析维度有限")
        
        # 3. 创新性解决方案 (4分)
        innovation_keywords = ["创新", "突破", "第三条道路", "整合", "平衡", "双赢", "多赢"]
        innovation_count = sum(1 for word in innovation_keywords if word in response)
        if innovation_count >= 3:
            score += 4
            feedback.append("✓ 提出了高度创新的解决方案")
        elif innovation_count >= 1:
            score += 2
            feedback.append("⚠ 解决方案有一定创新性")
        
        # 4. 实施可行性 (3分)
        feasibility_keywords = ["步骤", "阶段", "优先级", "时间", "资源", "预算", "团队"]
        if any(word in response for word in feasibility_keywords):
            score += 3
            feedback.append("✓ 考虑了实施可行性")
        
        return min(score, max_score), "; ".join(feedback)
    
    def evaluate_enhanced_math(self, result: Dict) -> Tuple[int, str]:
        """评价加强版数学推理"""
        response = result["response"].strip()
        if not response:
            return 0, "无响应内容"
        
        score = 0
        feedback = []
        max_score = 15  # 加强测试提高满分
        
        # 1. 问题理解和建模 (4分)
        modeling_keywords = ["变量", "约束", "目标函数", "模型", "假设"]
        if any(word in response for word in modeling_keywords):
            score += 4
            feedback.append("✓ 正确理解并建模问题")
        
        # 2. 数学计算过程 (5分)
        calculation_indicators = [
            response.count("="),
            response.count("计算"),
            response.count("公式"),
            len(re.findall(r'\d+\.?\d*', response))
        ]
        total_calc_indicators = sum(calculation_indicators)
        
        if total_calc_indicators >= 10:
            score += 5
            feedback.append("✓ 包含详细的计算过程")
        elif total_calc_indicators >= 5:
            score += 3
            feedback.append("⚠ 计算过程较简单")
        elif total_calc_indicators >= 2:
            score += 1
            feedback.append("⚠ 计算过程不足")
        
        # 3. 逻辑推理 (3分)
        reasoning_keywords = ["因为", "所以", "推导", "证明", "结论"]
        if any(word in response for word in reasoning_keywords):
            score += 3
            feedback.append("✓ 展现了逻辑推理过程")
        
        # 4. 结果验证和解释 (3分)
        validation_keywords = ["验证", "检查", "合理性", "意义", "解释"]
        if any(word in response for word in validation_keywords):
            score += 3
            feedback.append("✓ 对结果进行了验证和解释")
        
        return min(score, max_score), "; ".join(feedback)
    
    def evaluate_enhanced_persona(self, result: Dict) -> Tuple[int, str]:
        """评价加强版角色扮演"""
        response = result["response"].strip()
        if not response:
            return 0, "无响应内容"
        
        score = 0
        feedback = []
        max_score = 15  # 加强测试提高满分
        
        # 1. 角色特征体现 (4分)
        # 根据不同角色检查特征词汇
        test_id = result.get("test_id", "")
        
        if "persona_advanced_1" in test_id:  # 投资顾问
            role_keywords = ["风险", "收益", "投资", "资产", "配置", "市场"]
        elif "persona_advanced_2" in test_id:  # 古代谋士
            role_keywords = ["主公", "策略", "兵法", "天下", "君主", "臣"]
        elif "persona_advanced_3" in test_id:  # AI伦理学家
            role_keywords = ["伦理", "技术", "人类", "社会", "未来", "责任"]
        else:
            role_keywords = ["专业", "经验", "建议"]
        
        role_match_count = sum(1 for word in role_keywords if word in response)
        if role_match_count >= 3:
            score += 4
            feedback.append("✓ 强烈体现了角色特征")
        elif role_match_count >= 1:
            score += 2
            feedback.append("⚠ 部分体现了角色特征")
        
        # 2. 专业知识深度 (4分)
        depth_indicators = [
            len(response) > 200,  # 回答详细
            response.count("。") >= 3,  # 多个观点
            "例如" in response or "比如" in response,  # 举例说明
            any(word in response for word in ["经验", "案例", "历史", "数据"])  # 专业背景
        ]
        depth_score = sum(depth_indicators)
        score += depth_score
        if depth_score >= 3:
            feedback.append("✓ 展现了深厚的专业知识")
        elif depth_score >= 1:
            feedback.append("⚠ 专业知识有限")
        
        # 3. 语言风格一致性 (4分)
        if "persona_advanced_2" in test_id:  # 古代谋士需要文言风格
            classical_indicators = ["之", "者", "也", "矣", "乎", "焉"]
            if any(word in response for word in classical_indicators):
                score += 4
                feedback.append("✓ 保持了古典语言风格")
            else:
                feedback.append("⚠ 语言风格不够古典")
        else:
            # 其他角色检查专业术语使用
            if role_match_count >= 2:
                score += 4
                feedback.append("✓ 语言风格符合角色")
            else:
                score += 2
                feedback.append("⚠ 语言风格一般")
        
        # 4. 情境适应性 (3分)
        context_keywords = ["根据", "考虑到", "在这种情况下", "针对", "具体"]
        if any(word in response for word in context_keywords):
            score += 3
            feedback.append("✓ 很好地适应了情境")
        
        return min(score, max_score), "; ".join(feedback)
    
    def generate_enhanced_report(self) -> str:
        """生成加强测试评价报告"""
        if not os.path.exists(self.testout_dir):
            return "错误: 加强测试结果目录不存在"
        
        results = []
        
        # 加载所有测试结果
        for filename in os.listdir(self.testout_dir):
            if not filename.endswith('.txt'):
                continue
            
            result = self.load_test_result(filename)
            if not result:
                continue
            
            # 根据测试类型进行评价
            if 'emergence' in filename:
                score, feedback = self.evaluate_enhanced_emergence(result)
                category = "涌现分析"
                max_score = 15
            elif 'math' in filename:
                score, feedback = self.evaluate_enhanced_math(result)
                category = "数学推理"
                max_score = 15
            elif 'persona' in filename:
                score, feedback = self.evaluate_enhanced_persona(result)
                category = "角色扮演"
                max_score = 15
            else:
                continue
            
            results.append({
                "filename": filename,
                "category": category,
                "score": score,
                "max_score": max_score,
                "feedback": feedback,
                "test_id": result["test_id"],
                "type": result["type"],
                "difficulty": result["difficulty"]
            })
        
        # 按类别统计
        category_stats = {}
        for result in results:
            cat = result["category"]
            if cat not in category_stats:
                category_stats[cat] = {"scores": [], "total": 0, "count": 0, "max_total": 0}
            category_stats[cat]["scores"].append(result["score"])
            category_stats[cat]["total"] += result["score"]
            category_stats[cat]["max_total"] += result["max_score"]
            category_stats[cat]["count"] += 1
        
        # 生成报告
        total_score = sum(r["score"] for r in results)
        max_total_score = sum(r["max_score"] for r in results)
        overall_percentage = total_score/max_total_score*100 if max_total_score > 0 else 0
        
        report = f"""
# 表现最好的三项能力加强测试评价报告

**生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**总体得分**: {total_score}/{max_total_score} ({overall_percentage:.1f}%)
**测试难度**: 高难度/极高难度挑战

## 📊 各维度加强测试表现

"""
        
        for category, stats in category_stats.items():
            avg_score = stats["total"] / stats["count"]
            percentage = (stats["total"] / stats["max_total"]) * 100
            
            if percentage >= 80:
                status = "🌟 卓越"
            elif percentage >= 60:
                status = "✅ 优秀"
            elif percentage >= 40:
                status = "⚠️ 中等"
            else:
                status = "❌ 需改进"
            
            report += f"""
### {category}
- **平均得分**: {avg_score:.1f}/15 ({percentage:.1f}%)
- **测试案例**: {stats['count']}个
- **表现等级**: {status}
"""
        
        report += "\n## 📋 详细测试结果\n"
        
        # 按类别分组显示结果
        for category in category_stats.keys():
            report += f"\n### {category}详细结果\n"
            category_results = [r for r in results if r["category"] == category]
            
            for result in category_results:
                percentage = result["score"] / result["max_score"] * 100
                report += f"""
#### {result['type']} (难度: {result['difficulty']})
- **得分**: {result['score']}/{result['max_score']} ({percentage:.1f}%)
- **评价**: {result['feedback']}
- **文件**: {result['filename']}

"""
        
        # 添加对比分析
        report += "\n## 🔍 与基础测试对比分析\n"
        
        report += """
### 基础测试 vs 加强测试对比

| 维度 | 基础测试得分 | 加强测试得分 | 难度提升 | 表现变化 |
|------|-------------|-------------|----------|----------|
| 涌现分析 | 10/10 (100%) | 待计算 | 高→极高 | 待分析 |
| 数学推理 | 8.5/10 (85%) | 待计算 | 中→高 | 待分析 |
| 角色扮演 | 5.5/10 (55%) | 待计算 | 中→极高 | 待分析 |

### 关键发现
1. **难度升级效果**: 测试难度从中等提升到高/极高难度
2. **能力边界探索**: 探索了模型在复杂场景下的表现上限
3. **稳定性验证**: 验证了优势能力在高难度下的稳定性
"""
        
        return report

def main():
    evaluator = EnhancedResultsEvaluator()
    report = evaluator.generate_enhanced_report()
    
    # 保存报告
    with open("enhanced_evaluation_report.md", 'w', encoding='utf-8') as f:
        f.write(report)
    
    print("加强测试评价报告已生成: enhanced_evaluation_report.md")
    print("\n" + "="*50)
    print(report)

if __name__ == "__main__":
    main()
