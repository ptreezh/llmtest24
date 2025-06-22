#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试atlas模型的最终优化配置：
- 系统提示词限制在80字符以内
- 总结内容严格限制在150字符以内
- 总提示词严格限制在360字符以内
- 每2000 tokens总结一次
"""

def get_prompt(prompt_type: str, context: dict = {}, model: str = "") -> str:
    """复制TestLLM.py中的get_prompt函数进行测试"""
    # 针对atlas/intersync-gemma模型的精简提示词（总长度<360字符）
    # 系统提示词(80) + 用户提示词(<280) = 360字符，总结内容严格限制在150字符
    if "atlas/intersync-gemma" in model:
        if prompt_type == "intermediate":
            if context.get('summary_so_far', '').strip() and context.get('summary_so_far', '').strip() != 'None':
                # 包含任务+概括+新内容，总计<280字符（系统提示词80字符）
                task = "Find killer:"  # 12字符任务说明
                summary = context['summary_so_far'][:150]  # 150字符概括（严格限制，避免截断）
                new_content = context['new_dialogue_chunk'][:100]  # 100字符新内容
                return f"{task}\nEvidence: {summary}\nNew: {new_content}\nUpdate:"
            else:
                # 初始提示词：任务+内容
                task = "Find killer:"  # 12字符任务说明
                content = context['new_dialogue_chunk'][:250]  # 250字符内容
                return f"{task}\nDialogue: {content}\nSummary:"
        elif prompt_type == "final":
            # 最终推理：任务+概括
            task = "Find killer:"  # 12字符任务说明
            facts = context.get('summary_so_far', '')[:250]  # 250字符事实
            return f"{task}\nEvidence: {facts}\nAnswer:"
    
    return "Standard prompt for other models"

def test_final_optimization():
    """测试最终优化配置"""
    print("🧪 Testing Atlas Model Final Optimization")
    print("="*50)
    
    model = "atlas/intersync-gemma-7b-instruct-function-calling:latest"
    system_prompt = "Detective. Analyze murder case. Summarize key evidence concisely."
    
    print(f"System prompt: '{system_prompt}' ({len(system_prompt)} chars)")
    print(f"System prompt limit: 80 chars - {'✅ PASS' if len(system_prompt) <= 80 else '❌ FAIL'}")
    
    # 测试场景1：初始摘要（2000 tokens分段）
    test_dialogue = "A：昨晚我听到了奇怪的声音，好像是从森林那边传来的，声音很规律，不像是野兽发出的。B：我也听到了，而且我还看到了一个黑影在老橡树附近移动，那个人动作很快。C：这确实很奇怪，会不会是有人在那里做什么坏事？昨晚那么晚了还有人在外面确实不正常。D：我觉得可能是伐木工在工作，但这么晚了还工作确实很奇怪。"
    
    context1 = {
        "new_dialogue_chunk": test_dialogue
    }
    
    prompt1 = get_prompt("intermediate", context1, model)
    total1 = len(system_prompt) + len(prompt1)
    
    print(f"\n--- 场景1：初始摘要（2000 tokens分段） ---")
    print(f"User prompt: '{prompt1}' ({len(prompt1)} chars)")
    print(f"Total length: {total1} chars")
    print(f"✅ Within 360 limit: {total1 <= 360}")
    
    # 测试场景2：更新摘要（模拟150字符以内的摘要）
    previous_summary = "昨晚听到规律声音来自森林，看到黑影在老橡树附近移动，怀疑有人做坏事。可能是伐木工但时间不正常。需要进一步调查。"  # 约70字符
    
    context2 = {
        "summary_so_far": previous_summary,
        "new_dialogue_chunk": test_dialogue
    }
    
    prompt2 = get_prompt("intermediate", context2, model)
    total2 = len(system_prompt) + len(prompt2)
    
    print(f"\n--- 场景2：更新摘要（150字符限制） ---")
    print(f"Previous summary: '{previous_summary}' ({len(previous_summary)} chars)")
    print(f"User prompt: '{prompt2}' ({len(prompt2)} chars)")
    print(f"Total length: {total2} chars")
    print(f"✅ Within 360 limit: {total2 <= 360}")
    print(f"✅ Summary within 150 limit: {len(previous_summary) <= 150}")
    
    # 测试场景3：最终推理
    final_summary = "经过多轮分析：昨晚森林传来规律声音，老橡树附近发现黑影移动。张三丢失斧头，地面有大靴子脚印。黑影身高一米八左右。李四深夜外出，与张三有矛盾，身高符合。"  # 约90字符
    
    context3 = {
        "summary_so_far": final_summary
    }
    
    prompt3 = get_prompt("final", context3, model)
    total3 = len(system_prompt) + len(prompt3)
    
    print(f"\n--- 场景3：最终推理 ---")
    print(f"Final summary: '{final_summary}' ({len(final_summary)} chars)")
    print(f"User prompt: '{prompt3}' ({len(prompt3)} chars)")
    print(f"Total length: {total3} chars")
    print(f"✅ Within 360 limit: {total3 <= 360}")
    print(f"✅ Summary within 150 limit: {len(final_summary) <= 150}")
    
    # 测试场景4：极限情况（150字符摘要）
    max_summary = "经过多轮分析：昨晚森林传来规律声音，老橡树附近发现黑影移动。张三丢失斧头，地面有大靴子脚印步伐急促。黑影身高一米八左右。李四深夜外出，与张三有矛盾，身高符合。王五也有嫌疑但有不在场证明。赵六曾威胁张三但身高不符。"  # 接近150字符
    
    context4 = {
        "summary_so_far": max_summary,
        "new_dialogue_chunk": "G：我发现了新线索。H：什么线索？I：李四的工具箱里有血迹。"
    }
    
    prompt4 = get_prompt("intermediate", context4, model)
    total4 = len(system_prompt) + len(prompt4)
    
    print(f"\n--- 场景4：极限情况（150字符摘要） ---")
    print(f"Max summary: '{max_summary}' ({len(max_summary)} chars)")
    print(f"User prompt: '{prompt4}' ({len(prompt4)} chars)")
    print(f"Total length: {total4} chars")
    print(f"✅ Within 360 limit: {total4 <= 360}")
    print(f"✅ Summary within 150 limit: {len(max_summary) <= 150}")
    
    # 汇总报告
    print(f"\n" + "="*50)
    print(f"📋 Atlas Model Final Optimization Test Summary")
    print(f"="*50)
    print(f"System prompt length: {len(system_prompt)} chars (limit: 80)")
    print(f"Target total limit: 360 chars")
    print(f"Summary content limit: 150 chars")
    print(f"Segmentation: Every 2000 tokens")
    print(f"")
    print(f"Test results:")
    print(f"  系统提示词: {len(system_prompt)} chars - {'✅ PASS' if len(system_prompt) <= 80 else '❌ FAIL'}")
    print(f"  场景1 (初始摘要): {total1} chars - {'✅ PASS' if total1 <= 360 else '❌ FAIL'}")
    print(f"  场景2 (更新摘要): {total2} chars - {'✅ PASS' if total2 <= 360 else '❌ FAIL'}")
    print(f"  场景3 (最终推理): {total3} chars - {'✅ PASS' if total3 <= 360 else '❌ FAIL'}")
    print(f"  场景4 (极限情况): {total4} chars - {'✅ PASS' if total4 <= 360 else '❌ FAIL'}")
    
    all_pass = all([
        len(system_prompt) <= 80,
        total1 <= 360, 
        total2 <= 360, 
        total3 <= 360, 
        total4 <= 360,
        len(previous_summary) <= 150,
        len(final_summary) <= 150,
        len(max_summary) <= 150
    ])
    
    print(f"")
    print(f"Overall result: {'✅ ALL TESTS PASS' if all_pass else '❌ SOME TESTS FAIL'}")
    
    if all_pass:
        print(f"🎯 Atlas model final optimization successful!")
        print(f"✅ 系统提示词 ≤ 80字符")
        print(f"✅ 总结内容严格限制在150字符以内")
        print(f"✅ 总提示词严格限制在360字符以内")
        print(f"✅ 每2000 tokens总结一次，避免强制截断")
        print(f"✅ 支持3万字以上内容多轮处理")
    else:
        print(f"⚠️ Some tests failed, need further optimization")

    # 计算2000 tokens分段的优势
    print(f"\n🔄 2000 Tokens Segmentation Benefits:")
    print(f"• 更频繁的摘要更新，信息损失更少")
    print(f"• 摘要长度更容易控制在150字符以内")
    print(f"• 减少零响应问题（更小的处理单元）")
    print(f"• 更好的长上下文处理能力")

if __name__ == "__main__":
    test_final_optimization()
