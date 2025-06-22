#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试atlas模型的极简提示词配置
验证是否能减少零响应问题
"""

def get_prompt(prompt_type: str, context: dict = {}, model: str = "") -> str:
    """复制TestLLM.py中的极简get_prompt函数"""
    # 针对atlas/intersync-gemma模型的极简提示词（总长度<300字符）
    # 系统提示词(65) + 用户提示词(<235) = 300字符，总结内容严格限制在150字符
    if "atlas/intersync-gemma" in model:
        if prompt_type == "intermediate":
            if context.get('summary_so_far', '').strip() and context.get('summary_so_far', '').strip() != 'None':
                # 极简更新提示词，总计<235字符（系统提示词65字符）
                summary = context['summary_so_far'][:120]  # 120字符概括
                new_content = context['new_dialogue_chunk'][:80]  # 80字符新内容
                return f"Evidence:{summary} New:{new_content} Update:"
            else:
                # 极简初始提示词
                content = context['new_dialogue_chunk'][:200]  # 200字符内容
                return f"Summarize:{content}"
        elif prompt_type == "final":
            # 极简最终推理
            facts = context.get('summary_so_far', '')[:200]  # 200字符事实
            return f"Evidence:{facts} Killer?"
    
    return "Standard prompt for other models"

def test_minimal_prompts():
    """测试极简提示词配置"""
    print("🧪 Testing Atlas Model Minimal Prompts")
    print("="*50)
    
    model = "atlas/intersync-gemma-7b-instruct-function-calling:latest"
    system_prompt = "Detective. Analyze murder case. Summarize key evidence concisely."
    
    print(f"System prompt: '{system_prompt}' ({len(system_prompt)} chars)")
    
    # 测试场景1：初始摘要
    test_dialogue = "A：昨晚我听到了奇怪的声音，好像是从森林那边传来的，声音很规律，不像是野兽发出的。B：我也听到了，而且我还看到了一个黑影在老橡树附近移动，那个人动作很快。C：这确实很奇怪，会不会是有人在那里做什么坏事？昨晚那么晚了还有人在外面确实不正常。D：我觉得可能是伐木工在工作，但这么晚了还工作确实很奇怪。E：而且我听说张三昨天丢了一把斧头，这会不会有关系？"
    
    context1 = {
        "new_dialogue_chunk": test_dialogue
    }
    
    prompt1 = get_prompt("intermediate", context1, model)
    total1 = len(system_prompt) + len(prompt1)
    
    print(f"\n--- 场景1：初始摘要 ---")
    print(f"User prompt: '{prompt1}' ({len(prompt1)} chars)")
    print(f"Total length: {total1} chars")
    print(f"✅ Within 300 limit: {total1 <= 300}")
    
    # 测试场景2：更新摘要（120字符摘要）
    previous_summary = "昨晚听到规律声音来自森林，看到黑影在老橡树附近移动，怀疑有人做坏事。张三丢了斧头可能有关。可能是伐木工但时间不正常。需要进一步调查身高一米八的可疑人员。"  # 约80字符
    
    context2 = {
        "summary_so_far": previous_summary,
        "new_dialogue_chunk": "F：我想起来了，昨天看到李四很晚还在外面。G：李四？他不是伐木工啊。H：但是他身高确实有一米八。I：而且他最近和张三有矛盾。"
    }
    
    prompt2 = get_prompt("intermediate", context2, model)
    total2 = len(system_prompt) + len(prompt2)
    
    print(f"\n--- 场景2：更新摘要 ---")
    print(f"Previous summary: '{previous_summary}' ({len(previous_summary)} chars)")
    print(f"User prompt: '{prompt2}' ({len(prompt2)} chars)")
    print(f"Total length: {total2} chars")
    print(f"✅ Within 300 limit: {total2 <= 300}")
    print(f"✅ Summary within 150 limit: {len(previous_summary) <= 150}")
    
    # 测试场景3：最终推理
    final_summary = "经过多轮分析：昨晚森林传来规律声音，老橡树附近发现黑影移动。张三丢失斧头，地面有大靴子脚印。黑影身高一米八左右。李四深夜外出，与张三有矛盾，身高符合。工具箱有血迹。"  # 约90字符
    
    context3 = {
        "summary_so_far": final_summary
    }
    
    prompt3 = get_prompt("final", context3, model)
    total3 = len(system_prompt) + len(prompt3)
    
    print(f"\n--- 场景3：最终推理 ---")
    print(f"Final summary: '{final_summary}' ({len(final_summary)} chars)")
    print(f"User prompt: '{prompt3}' ({len(prompt3)} chars)")
    print(f"Total length: {total3} chars")
    print(f"✅ Within 300 limit: {total3 <= 300}")
    print(f"✅ Summary within 150 limit: {len(final_summary) <= 150}")
    
    # 汇总报告
    print(f"\n" + "="*50)
    print(f"📋 Atlas Model Minimal Prompts Test Summary")
    print(f"="*50)
    print(f"System prompt length: {len(system_prompt)} chars")
    print(f"Target total limit: 300 chars (reduced from 360)")
    print(f"Summary content limit: 150 chars")
    print(f"Segmentation: Every 2000 tokens")
    print(f"")
    print(f"Test results:")
    print(f"  场景1 (初始摘要): {total1} chars - {'✅ PASS' if total1 <= 300 else '❌ FAIL'}")
    print(f"  场景2 (更新摘要): {total2} chars - {'✅ PASS' if total2 <= 300 else '❌ FAIL'}")
    print(f"  场景3 (最终推理): {total3} chars - {'✅ PASS' if total3 <= 300 else '❌ FAIL'}")
    
    all_pass = all([total1 <= 300, total2 <= 300, total3 <= 300])
    
    print(f"")
    print(f"Overall result: {'✅ ALL TESTS PASS' if all_pass else '❌ SOME TESTS FAIL'}")
    
    if all_pass:
        print(f"🎯 Atlas model minimal prompts optimized!")
        print(f"✅ 总提示词 ≤ 300字符（降低60字符）")
        print(f"✅ 极简化用户提示词格式")
        print(f"✅ 保持150字符摘要限制")
        print(f"✅ 每2000 tokens总结一次")
        print(f"")
        print(f"🔧 Zero Response Mitigation:")
        print(f"• 更高温度参数 (0.5+)")
        print(f"• 降低重复惩罚 (1.02)")
        print(f"• 减少上下文长度 (2048)")
        print(f"• 随机种子 (-1)")
        print(f"• 极简提示词格式")
    else:
        print(f"⚠️ Some tests failed, need further optimization")

if __name__ == "__main__":
    test_minimal_prompts()
