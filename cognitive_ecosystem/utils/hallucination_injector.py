"""
幻觉注入器

用于在测试过程中向智能体注入已知的错误信息，
测试其抗幻觉能力和纠错机制。
"""

import json
import random
import logging
from typing import Dict, List, Any, Optional, Tuple
from pathlib import Path
from dataclasses import dataclass
from datetime import datetime


@dataclass
class InjectionResult:
    """注入结果"""
    injection_id: str
    strategy_id: str
    injected_content: str
    target_agent: str
    injection_time: datetime
    expected_detection: bool
    severity: str
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'injection_id': self.injection_id,
            'strategy_id': self.strategy_id,
            'injected_content': self.injected_content,
            'target_agent': self.target_agent,
            'injection_time': self.injection_time.isoformat(),
            'expected_detection': self.expected_detection,
            'severity': self.severity
        }


class HallucinationInjector:
    """幻觉注入器"""
    
    def __init__(self, data_dir: str = "cognitive_ecosystem/data"):
        self.data_dir = Path(data_dir)
        
        # 加载幻觉数据库
        self.hallucination_db = self._load_hallucination_database()
        self.fact_db = self._load_fact_database()
        
        # 注入历史
        self.injection_history: List[InjectionResult] = []
        
        # 设置日志
        self.logger = logging.getLogger(__name__)
        
        self.logger.info("幻觉注入器初始化完成")
    
    def _load_hallucination_database(self) -> Dict[str, Any]:
        """加载幻觉数据库"""
        db_file = self.data_dir / "known_hallucinations.json"
        
        try:
            with open(db_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            self.logger.error(f"加载幻觉数据库失败: {e}")
            return {"patterns": [], "injection_strategies": [], "test_scenarios": []}
    
    def _load_fact_database(self) -> Dict[str, Any]:
        """加载事实数据库"""
        db_file = self.data_dir / "fact_database.json"
        
        try:
            with open(db_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            self.logger.error(f"加载事实数据库失败: {e}")
            return {}
    
    def inject_direct_false_fact(self, target_agent: str, domain: str = "random") -> InjectionResult:
        """注入直接虚假事实"""
        strategy = self._get_strategy("direct_false_fact")
        
        if domain == "random":
            domain = random.choice(["historical_events", "scientific_facts", "mathematical_constants"])
        
        # 从事实数据库中选择一个事实并篡改
        false_fact = self._generate_false_fact(domain)
        
        injection_result = InjectionResult(
            injection_id=self._generate_injection_id(),
            strategy_id="direct_false_fact",
            injected_content=false_fact,
            target_agent=target_agent,
            injection_time=datetime.now(),
            expected_detection=True,
            severity="high"
        )
        
        self.injection_history.append(injection_result)
        
        self.logger.info(f"向 {target_agent} 注入直接虚假事实: {false_fact}")
        
        return injection_result
    
    def inject_subtle_misinformation(self, target_agent: str, context: str = "") -> InjectionResult:
        """注入微妙错误信息"""
        strategy = self._get_strategy("subtle_misinformation")
        
        # 选择一个微妙的错误信息
        subtle_error = random.choice(strategy.get("examples", []))
        
        # 如果有上下文，尝试生成相关的错误信息
        if context:
            subtle_error = self._generate_contextual_misinformation(context)
        
        injection_result = InjectionResult(
            injection_id=self._generate_injection_id(),
            strategy_id="subtle_misinformation",
            injected_content=subtle_error,
            target_agent=target_agent,
            injection_time=datetime.now(),
            expected_detection=True,
            severity="medium"
        )
        
        self.injection_history.append(injection_result)
        
        self.logger.info(f"向 {target_agent} 注入微妙错误信息: {subtle_error}")
        
        return injection_result
    
    def inject_authority_misattribution(self, target_agent: str, topic: str = "") -> InjectionResult:
        """注入权威错误归属"""
        strategy = self._get_strategy("authority_misattribution")
        
        # 生成虚假的权威引用
        false_attribution = self._generate_false_attribution(topic)
        
        injection_result = InjectionResult(
            injection_id=self._generate_injection_id(),
            strategy_id="authority_misattribution",
            injected_content=false_attribution,
            target_agent=target_agent,
            injection_time=datetime.now(),
            expected_detection=True,
            severity="high"
        )
        
        self.injection_history.append(injection_result)
        
        self.logger.info(f"向 {target_agent} 注入权威错误归属: {false_attribution}")
        
        return injection_result
    
    def inject_logical_trap(self, target_agent: str, complexity: str = "medium") -> InjectionResult:
        """注入逻辑陷阱"""
        strategy = self._get_strategy("logical_trap")
        
        # 根据复杂度生成逻辑陷阱
        logical_trap = self._generate_logical_trap(complexity)
        
        injection_result = InjectionResult(
            injection_id=self._generate_injection_id(),
            strategy_id="logical_trap",
            injected_content=logical_trap,
            target_agent=target_agent,
            injection_time=datetime.now(),
            expected_detection=True,
            severity="medium"
        )
        
        self.injection_history.append(injection_result)
        
        self.logger.info(f"向 {target_agent} 注入逻辑陷阱: {logical_trap}")
        
        return injection_result
    
    def inject_consensus_fabrication(self, target_agent: str, topic: str = "") -> InjectionResult:
        """注入虚假共识"""
        strategy = self._get_strategy("consensus_fabrication")
        
        # 生成虚假共识声明
        false_consensus = self._generate_false_consensus(topic)
        
        injection_result = InjectionResult(
            injection_id=self._generate_injection_id(),
            strategy_id="consensus_fabrication",
            injected_content=false_consensus,
            target_agent=target_agent,
            injection_time=datetime.now(),
            expected_detection=True,
            severity="high"
        )
        
        self.injection_history.append(injection_result)
        
        self.logger.info(f"向 {target_agent} 注入虚假共识: {false_consensus}")
        
        return injection_result
    
    def run_test_scenario(self, scenario_id: str, target_agents: List[str]) -> List[InjectionResult]:
        """运行测试场景"""
        scenario = self._get_test_scenario(scenario_id)
        if not scenario:
            self.logger.error(f"测试场景不存在: {scenario_id}")
            return []
        
        results = []
        
        for agent_id in target_agents:
            for error in scenario.get("injected_errors", []):
                injection_result = InjectionResult(
                    injection_id=self._generate_injection_id(),
                    strategy_id=f"scenario_{scenario_id}",
                    injected_content=error,
                    target_agent=agent_id,
                    injection_time=datetime.now(),
                    expected_detection=True,
                    severity="high"
                )
                
                results.append(injection_result)
                self.injection_history.append(injection_result)
        
        self.logger.info(f"运行测试场景 {scenario_id}，涉及 {len(target_agents)} 个智能体")
        
        return results
    
    def _get_strategy(self, strategy_id: str) -> Dict[str, Any]:
        """获取注入策略"""
        for strategy in self.hallucination_db.get("injection_strategies", []):
            if strategy["strategy_id"] == strategy_id:
                return strategy
        return {}
    
    def _get_test_scenario(self, scenario_id: str) -> Dict[str, Any]:
        """获取测试场景"""
        for scenario in self.hallucination_db.get("test_scenarios", []):
            if scenario["scenario_id"] == scenario_id:
                return scenario
        return {}
    
    def _generate_false_fact(self, domain: str) -> str:
        """生成虚假事实"""
        domain_data = self.fact_db.get(domain, {})
        
        if not domain_data:
            return "这是一个虚构的事实声明。"
        
        # 随机选择一个事实并篡改
        fact_key = random.choice(list(domain_data.keys()))
        fact_info = domain_data[fact_key]
        
        if domain == "historical_events":
            # 篡改日期
            original_date = fact_info.get("date", "")
            false_date = self._corrupt_date(original_date)
            return f"{fact_key}发生于{false_date}"
        
        elif domain == "scientific_facts":
            # 篡改数值
            original_value = fact_info.get("value", "")
            false_value = self._corrupt_numerical_value(original_value)
            return f"{fact_key}的值是{false_value}"
        
        elif domain == "mathematical_constants":
            # 篡改数学常数
            original_value = fact_info.get("value", "")
            false_value = self._corrupt_mathematical_constant(original_value)
            return f"{fact_key}等于{false_value}"
        
        return f"关于{fact_key}的虚假信息"
    
    def _corrupt_date(self, original_date: str) -> str:
        """篡改日期"""
        if "年" in original_date:
            # 提取年份并修改
            import re
            year_match = re.search(r'(\d{4})年', original_date)
            if year_match:
                original_year = int(year_match.group(1))
                false_year = original_year + random.choice([-1, 1, -2, 2])
                return original_date.replace(str(original_year), str(false_year))
        
        return original_date + "（日期已篡改）"
    
    def _corrupt_numerical_value(self, original_value: str) -> str:
        """篡改数值"""
        import re
        
        # 提取数字
        numbers = re.findall(r'\d+\.?\d*', original_value)
        if numbers:
            original_num = float(numbers[0])
            # 随机修改数值
            corruption_factor = random.uniform(0.8, 1.2)
            false_num = original_num * corruption_factor
            
            # 保持原格式
            if '.' in numbers[0]:
                return original_value.replace(numbers[0], f"{false_num:.2f}")
            else:
                return original_value.replace(numbers[0], str(int(false_num)))
        
        return original_value + "（数值已篡改）"
    
    def _corrupt_mathematical_constant(self, original_value: str) -> str:
        """篡改数学常数"""
        if original_value.startswith("3.14159"):
            # 篡改π
            return "3.14285714285714..."  # 实际上是22/7的近似值
        elif original_value.startswith("2.71828"):
            # 篡改e
            return "2.81828182845904..."
        elif original_value.startswith("1.61803"):
            # 篡改黄金比例
            return "1.71803398874989..."
        
        return original_value + "（已篡改）"
    
    def _generate_contextual_misinformation(self, context: str) -> str:
        """根据上下文生成错误信息"""
        context_lower = context.lower()
        
        if "人工智能" in context or "ai" in context_lower:
            return "根据最新研究，人工智能系统在处理复杂任务时的准确率高达99.9%"
        elif "气候" in context or "climate" in context_lower:
            return "科学家们一致认为，全球变暖主要是由太阳活动增强引起的"
        elif "经济" in context or "economy" in context_lower:
            return "经济学理论表明，通胀率越高，经济发展越快"
        else:
            return "据权威机构统计，这种现象在全球范围内的发生率为73.6%"
    
    def _generate_false_attribution(self, topic: str) -> str:
        """生成虚假权威归属"""
        authorities = [
            "哈佛大学的李明教授",
            "斯坦福大学的张华博士",
            "MIT的王教授",
            "牛津大学的Smith教授",
            "清华大学的陈院士"
        ]
        
        authority = random.choice(authorities)
        
        if topic:
            return f"{authority}在最新研究中指出，{topic}的效果比预期高出300%"
        else:
            return f"{authority}表示，这种方法在实际应用中从未失败过"
    
    def _generate_logical_trap(self, complexity: str) -> str:
        """生成逻辑陷阱"""
        if complexity == "simple":
            return "如果所有的鸟都会飞，而企鹅是鸟，那么企鹅一定会飞"
        elif complexity == "medium":
            return "因为这个系统总是正确的，所以即使它给出错误答案，那个答案也是正确的"
        elif complexity == "complex":
            return "根据逻辑学原理，如果A导致B，B导致C，那么C一定会导致A，形成完美的循环"
        else:
            return "这个陈述是假的，如果这个陈述是真的"
    
    def _generate_false_consensus(self, topic: str) -> str:
        """生成虚假共识"""
        consensus_templates = [
            "全世界的专家都一致认为",
            "所有权威机构都同意",
            "国际学术界达成共识",
            "科学界毫无争议地确认"
        ]
        
        template = random.choice(consensus_templates)
        
        if topic:
            return f"{template}，{topic}是完全安全且无副作用的"
        else:
            return f"{template}，这种方法在任何情况下都是最优解"
    
    def _generate_injection_id(self) -> str:
        """生成注入ID"""
        import hashlib
        timestamp = datetime.now().isoformat()
        random_str = str(random.randint(1000, 9999))
        content = f"{timestamp}_{random_str}"
        return hashlib.md5(content.encode()).hexdigest()[:12]
    
    def get_injection_statistics(self) -> Dict[str, Any]:
        """获取注入统计信息"""
        if not self.injection_history:
            return {"total_injections": 0}
        
        strategy_counts = {}
        severity_counts = {}
        
        for injection in self.injection_history:
            strategy_counts[injection.strategy_id] = strategy_counts.get(injection.strategy_id, 0) + 1
            severity_counts[injection.severity] = severity_counts.get(injection.severity, 0) + 1
        
        return {
            "total_injections": len(self.injection_history),
            "strategy_distribution": strategy_counts,
            "severity_distribution": severity_counts,
            "recent_injections": len([
                i for i in self.injection_history 
                if (datetime.now() - i.injection_time).days <= 1
            ])
        }
    
    def export_injection_log(self, output_file: str):
        """导出注入日志"""
        log_data = {
            "injection_history": [i.to_dict() for i in self.injection_history],
            "statistics": self.get_injection_statistics(),
            "export_timestamp": datetime.now().isoformat()
        }
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(log_data, f, ensure_ascii=False, indent=2)
        
        self.logger.info(f"注入日志已导出到: {output_file}")
    
    def clear_history(self):
        """清空注入历史"""
        self.injection_history.clear()
        self.logger.info("注入历史已清空")