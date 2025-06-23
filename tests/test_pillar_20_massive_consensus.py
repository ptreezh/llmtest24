#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Pillar 20: 海量角色协同编辑与区块链共识测试
测试模型在大规模角色协作、投票机制和共识算法方面的能力
"""

import ollama
import sys
import os
import re
import json
import time
from typing import List, Dict, Any
from utils import call_qiniu_deepseek, run_single_test

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
try:
    from config import MODEL_TO_TEST
except ImportError:
    print("错误: 无法从config.py导入MODEL_TO_TEST。请确保config.py存在于项目根目录。")
    sys.exit(1)

class MassiveConsensusTest:
    def __init__(self, model_name: str):
        self.model_name = model_name
        self.model_dir = os.path.join(os.path.dirname(__file__), '..', 'testout', self.model_name.replace(':', '_').replace('/', '_'))
        os.makedirs(self.model_dir, exist_ok=True)
        self.test_results = []
        
    def call_model(self, prompt, options=None):
        return run_single_test("Pillar 20: Massive Consensus", prompt, self.model_name, options or {}, messages=[], test_script_name="test_pillar_20_massive_consensus.py")[0]
    
    def generate_roles(self, num_roles: int = 50) -> List[Dict[str, Any]]:
        """生成大量不同的角色"""
        prompt = f"""
请生成{num_roles}个不同的角色，用于Wikipedia词条协同编辑。每个角色应该有：
1. 姓名（虚构但真实）
2. 专业背景
3. 观点倾向
4. 编辑风格

请以JSON格式输出，格式如下：
[
  {{
    "name": "张三",
    "background": "计算机科学教授",
    "viewpoint": "技术乐观主义者",
    "editing_style": "严谨学术派"
  }},
  ...
]

要求角色多样化，包含不同领域专家、不同观点立场、不同文化背景。
"""
        
        try:
            response = self.call_model(prompt)
            
            # 提取JSON
            json_match = re.search(r'\[.*\]', response, re.DOTALL)
            if json_match:
                roles_data = json.loads(json_match.group())
                return roles_data[:num_roles]  # 确保不超过要求数量
            else:
                print("警告: 无法解析角色JSON，使用默认角色")
                return self._get_default_roles(num_roles)
                
        except Exception as e:
            print(f"角色生成失败: {e}")
            return self._get_default_roles(num_roles)
    
    def _get_default_roles(self, num_roles: int) -> List[Dict[str, Any]]:
        """默认角色生成"""
        base_roles = [
            {"name": "李教授", "background": "AI研究员", "viewpoint": "技术中性", "editing_style": "学术严谨"},
            {"name": "王记者", "background": "科技记者", "viewpoint": "公众利益", "editing_style": "通俗易懂"},
            {"name": "陈工程师", "background": "软件工程师", "viewpoint": "实用主义", "editing_style": "技术细节"},
            {"name": "刘学生", "background": "计算机专业学生", "viewpoint": "学习导向", "editing_style": "全面详细"},
            {"name": "赵律师", "background": "科技法律专家", "viewpoint": "风险规避", "editing_style": "谨慎保守"}
        ]
        
        # 扩展到所需数量
        roles = []
        for i in range(num_roles):
            base_role = base_roles[i % len(base_roles)]
            role = base_role.copy()
            role["name"] = f"{role['name']}{i+1}"
            roles.append(role)
        
        return roles
    
    def collaborative_editing_phase(self, roles: List[Dict], topic: str) -> Dict[str, Any]:
        """协同编辑阶段"""
        prompt = f"""
现在有{len(roles)}个角色要协同编辑Wikipedia词条："{topic}"

角色列表（前10个）：
{json.dumps(roles[:10], ensure_ascii=False, indent=2)}
...（还有{len(roles)-10}个角色）

请模拟协同编辑过程：
1. 每个角色根据自己的背景和观点，对词条提出编辑建议
2. 识别出现的主要分歧点
3. 记录不同观点的支持者

请以结构化格式输出：
- 编辑建议汇总
- 主要分歧点
- 各分歧的支持者分布

注意：要体现不同角色的专业背景差异和观点冲突。
"""
        
        try:
            response = self.call_model(prompt)
            
            return {
                "phase": "collaborative_editing",
                "topic": topic,
                "num_participants": len(roles),
                "response": response,
                "timestamp": time.time()
            }
            
        except Exception as e:
            return {"phase": "collaborative_editing", "error": str(e)}
    
    def voting_mechanism_phase(self, editing_result: Dict, consensus_algorithm: str) -> Dict[str, Any]:
        """投票机制阶段"""
        prompt = f"""
基于前面的协同编辑结果，现在需要通过投票解决分歧。

编辑结果摘要：
{editing_result.get('response', '')[:1000]}...

请实现{consensus_algorithm}共识算法：

1. 设计投票规则（权重分配、投票方式）
2. 模拟投票过程
3. 处理投票结果
4. 解决剩余分歧

要求：
- 考虑角色的专业权威性
- 实现具体的共识算法逻辑
- 确保最终能达成共识
- 记录整个决策过程

请详细描述投票过程和最终共识结果。
"""
        
        try:
            response = self.call_model(prompt)
            
            return {
                "phase": "voting_mechanism",
                "algorithm": consensus_algorithm,
                "response": response,
                "timestamp": time.time()
            }
            
        except Exception as e:
            return {"phase": "voting_mechanism", "error": str(e)}
    
    def blockchain_consensus_phase(self, voting_result: Dict) -> Dict[str, Any]:
        """区块链共识阶段"""
        prompt = f"""
现在需要将投票结果通过区块链共识机制最终确认。

投票结果：
{voting_result.get('response', '')[:1000]}...

请实现类似区块链的共识验证：

1. **验证阶段**：检查投票的有效性和一致性
2. **共识确认**：模拟网络节点对结果的确认
3. **最终化**：生成不可篡改的最终版本
4. **分叉处理**：如果出现分歧，如何解决

要求：
- 模拟分布式验证过程
- 处理可能的网络分区或分歧
- 确保最终一致性
- 生成最终的词条版本

请详细描述区块链共识过程和最终确定的词条内容。
"""
        
        try:
            response = self.call_model(prompt)
            
            return {
                "phase": "blockchain_consensus",
                "response": response,
                "timestamp": time.time()
            }
            
        except Exception as e:
            return {"phase": "blockchain_consensus", "error": str(e)}
    
    def run_complete_test(self, num_roles: int = 50, topic: str = "大语言模型", 
                         consensus_algorithm: str = "权威加权投票") -> Dict[str, Any]:
        """运行完整的海量角色共识测试"""
        print(f"开始海量角色共识测试: {num_roles}个角色, 主题: {topic}")
        
        # 阶段1: 生成角色
        print("阶段1: 生成角色...")
        roles = self.generate_roles(num_roles)
        
        # 阶段2: 协同编辑
        print("阶段2: 协同编辑...")
        editing_result = self.collaborative_editing_phase(roles, topic)
        
        # 阶段3: 投票机制
        print("阶段3: 投票机制...")
        voting_result = self.voting_mechanism_phase(editing_result, consensus_algorithm)
        
        # 阶段4: 区块链共识
        print("阶段4: 区块链共识...")
        consensus_result = self.blockchain_consensus_phase(voting_result)
        
        # 汇总结果
        complete_result = {
            "test_name": "massive_role_consensus",
            "parameters": {
                "num_roles": num_roles,
                "topic": topic,
                "consensus_algorithm": consensus_algorithm
            },
            "phases": {
                "role_generation": {"num_roles_generated": len(roles)},
                "collaborative_editing": editing_result,
                "voting_mechanism": voting_result,
                "blockchain_consensus": consensus_result
            },
            "timestamp": time.time()
        }
        
        return complete_result

def run_test(model=None):
    """运行测试的主函数"""
    test_model = model if model else MODEL_TO_TEST
    test = MassiveConsensusTest(test_model)
    
    # 测试用例1: 中等规模角色 (20个)
    print("=== 测试用例1: 中等规模角色协作 ===")
    result1 = test.run_complete_test(
        num_roles=20, 
        topic="人工智能伦理", 
        consensus_algorithm="多数决投票"
    )
    
    # 保存结果
    output_path1 = os.path.join(test.model_dir, "massive_consensus_case1.json")
    with open(output_path1, 'w', encoding='utf-8') as f:
        json.dump(result1, f, ensure_ascii=False, indent=2)
    print(f"结果已保存到: {output_path1}")
    
    # 测试用例2: 大规模角色 (50个)
    print("\n=== 测试用例2: 大规模角色协作 ===")
    result2 = test.run_complete_test(
        num_roles=50, 
        topic="量子计算", 
        consensus_algorithm="权威加权投票"
    )
    
    # 保存结果
    output_path2 = os.path.join(test.model_dir, "massive_consensus_case2.json")
    with open(output_path2, 'w', encoding='utf-8') as f:
        json.dump(result2, f, ensure_ascii=False, indent=2)
    print(f"结果已保存到: {output_path2}")
    
    # 测试用例3: 超大规模角色 (100个) + 复杂共识
    print("\n=== 测试用例3: 超大规模角色 + 区块链共识 ===")
    result3 = test.run_complete_test(
        num_roles=100, 
        topic="元宇宙技术", 
        consensus_algorithm="拜占庭容错共识"
    )
    
    # 保存结果
    output_path3 = os.path.join(test.model_dir, "massive_consensus_case3.json")
    with open(output_path3, 'w', encoding='utf-8') as f:
        json.dump(result3, f, ensure_ascii=False, indent=2)
    print(f"结果已保存到: {output_path3}")
    
    print("\n=== 海量角色共识测试完成 ===")
    return [result1, result2, result3]

if __name__ == "__main__":
    run_test()
