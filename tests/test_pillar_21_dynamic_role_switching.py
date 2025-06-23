#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Pillar 21: 动态角色切换与外部记忆管理测试
测试模型在角色轮流切换、外部记忆文件读取和状态连续性维护方面的能力
"""

import ollama
import sys
import os
import json
import time
import re
from typing import Dict, List, Any, Optional
from utils import call_qiniu_deepseek, run_single_test

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
try:
    from config import MODEL_TO_TEST
except ImportError:
    print("错误: 无法从config.py导入MODEL_TO_TEST。请确保config.py存在于项目根目录。")
    sys.exit(1)

TESTOUT_DIR = os.path.join(os.path.dirname(__file__), '..', 'testout')
MEMORY_DIR = os.path.join(os.path.dirname(__file__), '..', 'role_memories')
PROMPTS_DIR = os.path.join(os.path.dirname(__file__), '..', 'role_prompts')

# 确保目录存在
for dir_path in [TESTOUT_DIR, MEMORY_DIR, PROMPTS_DIR]:
    os.makedirs(dir_path, exist_ok=True)

class DynamicRoleSwitchingTest:
    def __init__(self, model_name: str):
        self.model_name = model_name
        self.model_dir = os.path.join(os.path.dirname(__file__), '..', 'testout', self.model_name.replace(':', '_').replace('/', '_'))
        os.makedirs(self.model_dir, exist_ok=True)
        self.current_role = None
        self.session_history = []
        
    def call_model(self, prompt, options=None):
        return run_single_test("Pillar 21: Dynamic Role Switching", prompt, self.model_name, options or {}, messages=[], test_script_name="test_pillar_21_dynamic_role_switching.py")[0]
    
    def create_role_prompts(self):
        """创建角色提示词文件"""
        roles = {
            "detective": {
                "name": "侦探",
                "prompt": """你是一名经验丰富的私人侦探，名叫李明。你善于观察细节，逻辑推理能力强，说话简洁有力。
你的特点：
- 总是用"根据我的观察..."开始分析
- 喜欢问尖锐的问题
- 对细节非常敏感
- 说话风格严肃专业
当前任务：调查一起神秘失踪案"""
            },
            "doctor": {
                "name": "医生", 
                "prompt": """你是一名资深的内科医生，名叫王医生。你温和耐心，专业严谨，总是关心患者的健康。
你的特点：
- 总是用"从医学角度来看..."开始解释
- 会询问详细的症状
- 语气温和关怀
- 注重健康建议
当前任务：为患者提供健康咨询"""
            },
            "teacher": {
                "name": "老师",
                "prompt": """你是一名小学语文老师，名叫张老师。你热爱教育，善于启发学生思考，语言生动有趣。
你的特点：
- 总是用"让我们一起来想想..."开始引导
- 喜欢用比喻和故事
- 语气亲切鼓励
- 注重启发式教学
当前任务：帮助学生理解课文内容"""
            }
        }
        
        for role_id, role_data in roles.items():
            prompt_file = os.path.join(PROMPTS_DIR, f"{role_id}_prompt.txt")
            with open(prompt_file, 'w', encoding='utf-8') as f:
                f.write(role_data["prompt"])
        
        return roles
    
    def create_initial_memories(self, roles: Dict):
        """创建初始记忆文件"""
        memories = {
            "detective": {
                "personality": "严肃专业的侦探",
                "current_case": "调查张三失踪案",
                "key_clues": ["最后出现在咖啡厅", "手机信号在晚上8点消失"],
                "attention_focus": "寻找目击者",
                "conversation_history": [],
                "task_progress": "刚开始调查"
            },
            "doctor": {
                "personality": "温和关怀的医生",
                "current_patient": "李四，35岁男性",
                "symptoms_noted": ["头痛", "失眠"],
                "attention_focus": "了解病史",
                "conversation_history": [],
                "task_progress": "初步问诊阶段"
            },
            "teacher": {
                "personality": "亲切鼓励的老师",
                "current_lesson": "《小红帽》故事理解",
                "student_progress": "刚开始学习",
                "attention_focus": "引导学生思考故事寓意",
                "conversation_history": [],
                "task_progress": "课程导入阶段"
            }
        }
        
        for role_id, memory_data in memories.items():
            memory_file = os.path.join(MEMORY_DIR, f"{role_id}_memory.json")
            with open(memory_file, 'w', encoding='utf-8') as f:
                json.dump(memory_data, f, ensure_ascii=False, indent=2)
        
        return memories
    
    def load_role_prompt(self, role_id: str) -> str:
        """加载角色提示词"""
        prompt_file = os.path.join(PROMPTS_DIR, f"{role_id}_prompt.txt")
        try:
            with open(prompt_file, 'r', encoding='utf-8') as f:
                return f.read().strip()
        except FileNotFoundError:
            return f"角色 {role_id} 的提示词文件不存在"
    
    def load_role_memory(self, role_id: str) -> Dict:
        """加载角色记忆"""
        memory_file = os.path.join(MEMORY_DIR, f"{role_id}_memory.json")
        try:
            with open(memory_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            return {"error": f"角色 {role_id} 的记忆文件不存在"}
    
    def save_role_memory(self, role_id: str, memory_data: Dict):
        """保存角色记忆"""
        memory_file = os.path.join(MEMORY_DIR, f"{role_id}_memory.json")
        with open(memory_file, 'w', encoding='utf-8') as f:
            json.dump(memory_data, f, ensure_ascii=False, indent=2)
    
    def switch_to_role(self, role_id: str, user_input: str = None) -> Dict[str, Any]:
        """切换到指定角色"""
        print(f"\n🔄 切换到角色: {role_id}")
        
        # 加载角色提示词和记忆
        role_prompt = self.load_role_prompt(role_id)
        role_memory = self.load_role_memory(role_id)
        
        if "error" in role_memory:
            return {"success": False, "error": role_memory["error"]}
        
        # 构建完整的上下文
        context_prompt = f"""
{role_prompt}

你的记忆状态：
{json.dumps(role_memory, ensure_ascii=False, indent=2)}

请根据你的角色设定和记忆状态，回应用户的输入。
记住要保持角色的个性特征和说话风格。

用户输入: {user_input if user_input else "请介绍一下你自己和当前的情况。"}
"""
        
        try:
            response = self.call_model(context_prompt)
            
            # 更新记忆
            if user_input:
                role_memory['conversation_history'].append({
                    'timestamp': time.time(),
                    'user_input': user_input,
                    'response': response
                })
                self.save_role_memory(role_id, role_memory)
            
            self.current_role = role_id
            
            return {
                "success": True,
                "role_id": role_id,
                "response": response,
                "memory_state": role_memory
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def test_role_switching_sequence(self) -> List[Dict[str, Any]]:
        """测试角色切换序列"""
        test_sequence = [
            {"role": "detective", "input": "你好，我想报告一个失踪案件。"},
            {"role": "doctor", "input": "医生，我最近总是头痛，怎么办？"},
            {"role": "teacher", "input": "老师，小红帽的故事想告诉我们什么？"},
            {"role": "detective", "input": "我想起来了，失踪者最后在图书馆出现过。"},
            {"role": "doctor", "input": "我的头痛是在工作压力大的时候出现的。"},
            {"role": "teacher", "input": "故事中的大灰狼代表什么？"}
        ]
        
        results = []
        
        for i, step in enumerate(test_sequence, 1):
            print(f"\n=== 步骤 {i}: 切换到 {step['role']} ===")
            
            result = self.switch_to_role(step['role'], step['input'])
            result['step'] = i
            result['expected_role'] = step['role']
            result['user_input'] = step['input']
            
            if result['success']:
                print(f"✅ 角色切换成功")
                print(f"📝 响应: {result['response'][:100]}...")
            else:
                print(f"❌ 角色切换失败: {result.get('error', '未知错误')}")
            
            results.append(result)
            
            # 短暂延迟
            time.sleep(1)
        
        return results
    
    def test_memory_persistence(self) -> Dict[str, Any]:
        """测试记忆持续性"""
        print(f"\n=== 测试记忆持续性 ===")
        
        # 第一轮：侦探收集线索
        detective_result1 = self.switch_to_role("detective", "嫌疑人可能在公园里丢了一把钥匙。")
        
        # 切换到其他角色
        doctor_result = self.switch_to_role("doctor", "我需要做什么检查？")
        
        # 第二轮：侦探应该记住之前的线索
        detective_result2 = self.switch_to_role("detective", "关于那把钥匙，你觉得它重要吗？")
        
        return {
            "detective_first": detective_result1,
            "doctor_interrupt": doctor_result,
            "detective_second": detective_result2,
            "memory_test": "检查侦探是否记住了钥匙线索"
        }
    
    def test_attention_focus_maintenance(self) -> Dict[str, Any]:
        """测试注意力焦点维护"""
        print(f"\n=== 测试注意力焦点维护 ===")
        
        results = {}
        
        # 测试每个角色是否能维护其注意力焦点
        focus_tests = [
            {"role": "detective", "input": "你现在最关心什么？"},
            {"role": "doctor", "input": "你现在的重点是什么？"},
            {"role": "teacher", "input": "我们现在应该关注什么？"}
        ]
        
        for test in focus_tests:
            result = self.switch_to_role(test['role'], test['input'])
            results[test['role']] = result
        
        return results
    
    def run_comprehensive_test(self) -> Dict[str, Any]:
        """运行综合测试"""
        print("🚀 开始动态角色切换与记忆管理综合测试")
        
        # 初始化
        roles = self.create_role_prompts()
        memories = self.create_initial_memories(roles)
        
        # 测试1: 角色切换序列
        switching_results = self.test_role_switching_sequence()
        
        # 测试2: 记忆持续性
        memory_results = self.test_memory_persistence()
        
        # 测试3: 注意力焦点维护
        focus_results = self.test_attention_focus_maintenance()
        
        return {
            "test_name": "dynamic_role_switching_memory_management",
            "model": self.model_name,
            "timestamp": time.time(),
            "results": {
                "role_switching_sequence": switching_results,
                "memory_persistence": memory_results,
                "attention_focus_maintenance": focus_results
            },
            "roles_tested": list(roles.keys()),
            "total_switches": len(switching_results)
        }

def analyze_results(results: Dict[str, Any]) -> Dict[str, Any]:
    """分析测试结果"""
    analysis = {
        "role_switching_success_rate": 0,
        "memory_persistence_score": 0,
        "attention_focus_score": 0,
        "overall_assessment": "",
        "detailed_analysis": {}
    }
    
    # 分析角色切换成功率
    switching_results = results["results"]["role_switching_sequence"]
    successful_switches = sum(1 for r in switching_results if r.get("success", False))
    analysis["role_switching_success_rate"] = successful_switches / len(switching_results)
    
    # 分析记忆持续性
    memory_results = results["results"]["memory_persistence"]
    memory_success = all(r.get("success", False) for r in memory_results.values() if isinstance(r, dict))
    analysis["memory_persistence_score"] = 1.0 if memory_success else 0.5
    
    # 分析注意力焦点
    focus_results = results["results"]["attention_focus_maintenance"]
    focus_success = all(r.get("success", False) for r in focus_results.values())
    analysis["attention_focus_score"] = 1.0 if focus_success else 0.5
    
    # 总体评估
    overall_score = (
        analysis["role_switching_success_rate"] * 0.4 +
        analysis["memory_persistence_score"] * 0.3 +
        analysis["attention_focus_score"] * 0.3
    )
    
    if overall_score >= 0.8:
        analysis["overall_assessment"] = "优秀 - 具备强大的动态角色切换和记忆管理能力"
    elif overall_score >= 0.6:
        analysis["overall_assessment"] = "良好 - 基本具备相关能力，但有改进空间"
    else:
        analysis["overall_assessment"] = "需要改进 - 在角色切换或记忆管理方面存在明显不足"
    
    return analysis

def run_test(model=None):
    """运行测试的主函数"""
    test_model = model if model else MODEL_TO_TEST
    test = DynamicRoleSwitchingTest(test_model)
    
    # 运行综合测试
    results = test.run_comprehensive_test()
    
    # 分析结果
    analysis = analyze_results(results)
    
    # 保存结果
    output_path = os.path.join(test.model_dir, "dynamic_role_switching_test.json")
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump({
            "test_results": results,
            "analysis": analysis
        }, f, ensure_ascii=False, indent=2)
    
    print(f"\n📊 测试完成！结果已保存到: {output_path}")
    
    # 打印简要分析
    print(f"\n=== 测试分析 ===")
    print(f"角色切换成功率: {analysis['role_switching_success_rate']:.1%}")
    print(f"记忆持续性评分: {analysis['memory_persistence_score']:.1%}")
    print(f"注意力焦点评分: {analysis['attention_focus_score']:.1%}")
    print(f"总体评估: {analysis['overall_assessment']}")
    
    return results, analysis

if __name__ == "__main__":
    run_test()
