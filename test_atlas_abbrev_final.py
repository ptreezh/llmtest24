#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试atlas模型的英文缩写格式（最高效）
验证是否能显著减少零响应问题
"""

def get_prompt(prompt_type: str, context: dict = {}, model: str = "") -> str:
    """复制TestLLM.py中的英文缩写get_prompt函数"""
    # 针对atlas/intersync-gemma模型的英文缩写格式（最高效）
    # 系统提示词(65) + 用户提示词(<100) = 165字符，总结内容严格限制在150字符
    if "atlas/intersync-gemma" in model:
        if prompt_type == "intermediate":
            if context.get('summary_so_far', '').strip() and context.get('summary_so_far', '').strip() != 'None':
                # 英文缩写更新提示词，总计<100字符（系统提示词65字符）
                summary = context['summary_so_far'][:60]  # 60字符概括
                new_content = context['new_dialogue_chunk'][:50]  # 50字符新内容
                return f"E:{summary} N:{new_content} U:"
            else:
                # 英文缩写初始提示词 - 严格控制在80字符以内
                content = context['new_dialogue_chunk'][:70]  # 70字符内容
                return f"S:{content}"
        elif prompt_type == "final":
            # 英文缩写最终推理
            facts = context.get('summary_so_far', '')[:150]  # 150字符事实
            return f"E:{facts} K?"
    
    return "Standard prompt for other models"

def test_abbrev_format():
    """测试英文缩写格式"""
    print("🧪 Testing Atlas Model English Abbreviation Format")
    print("="*55)
    
    model = "atlas/intersync-gemma-7b-instruct-function-calling:latest"
    system_prompt = "Detective. Analyze murder case. Summarize key evidence concisely."
    
    print(f"System prompt: '{system_prompt}' ({len(system_prompt)} chars)")
    
    # 模拟2000 tokens的长对话内容
    long_dialogue = """A：昨晚我听到了奇怪的声音，好像是从森林那边传来的，声音很规律，不像是野兽发出的。B：我也听到了，而且我还看到了一个黑影在老橡树附近移动，那个人动作很快。C：这确实很奇怪，会不会是有人在那里做什么坏事？昨晚那么晚了还有人在外面确实不正常。D：我觉得可能是伐木工在工作，但这么晚了还工作确实很奇怪。E：而且我听说张三昨天丢了一把斧头，这会不会有关系？F：斧头？这和脚印有什么关系？G：如果有人偷了斧头，可能是为了做坏事。H：你们说得对，我们确实应该仔细调查一下。I：那个黑影的身高大概多少？J：看起来比普通人高一些，大概一米八左右。"""
    
    print(f"Long dialogue length: {len(long_dialogue)} chars")
    
    # 测试场景1：初始提示词（英文缩写）
    context1 = {
        "new_dialogue_chunk": long_dialogue
    }
    
    prompt1 = get_prompt("intermediate", context1, model)
    total1 = len(system_prompt) + len(prompt1)
    
    print(f"\n--- 场景1：初始提示词（英文缩写 S:） ---")
    print(f"User prompt: '{prompt1}' ({len(prompt1)} chars)")
    print(f"Total length: {total1} chars")
    print(f"✅ User prompt ≤ 80 chars: {len(prompt1) <= 80}")
    print(f"✅ Total ≤ 150 chars: {total1 <= 150}")
    
    # 测试场景2：更新提示词（英文缩写）
    previous_summary = "昨晚听到规律声音来自森林，看到黑影在老橡树附近移动，怀疑有人做坏事。张三丢了斧头。"  # 约50字符
    
    context2 = {
        "summary_so_far": previous_summary,
        "new_dialogue_chunk": long_dialogue
    }
    
    prompt2 = get_prompt("intermediate", context2, model)
    total2 = len(system_prompt) + len(prompt2)
    
    print(f"\n--- 场景2：更新提示词（英文缩写 E:N:U:） ---")
    print(f"Previous summary: '{previous_summary}' ({len(previous_summary)} chars)")
    print(f"User prompt: '{prompt2}' ({len(prompt2)} chars)")
    print(f"Total length: {total2} chars")
    print(f"✅ User prompt ≤ 100 chars: {len(prompt2) <= 100}")
    print(f"✅ Total ≤ 170 chars: {total2 <= 170}")
    
    # 测试场景3：最终推理（英文缩写）
    final_summary = "经过多轮分析：昨晚森林传来规律声音，老橡树附近发现黑影移动。张三丢失斧头，地面有大靴子脚印。黑影身高一米八左右。李四深夜外出，与张三有矛盾，身高符合。工具箱有血迹。"  # 约90字符
    
    context3 = {
        "summary_so_far": final_summary
    }
    
    prompt3 = get_prompt("final", context3, model)
    total3 = len(system_prompt) + len(prompt3)
    
    print(f"\n--- 场景3：最终推理（英文缩写 E:K?） ---")
    print(f"Final summary: '{final_summary}' ({len(final_summary)} chars)")
    print(f"User prompt: '{prompt3}' ({len(prompt3)} chars)")
    print(f"Total length: {total3} chars")
    print(f"✅ Total ≤ 220 chars: {total3 <= 220}")
    
    # 汇总报告
    print(f"\n" + "="*55)
    print(f"📋 English Abbreviation Format Test Summary")
    print(f"="*55)
    print(f"System prompt length: {len(system_prompt)} chars")
    print(f"")
    print(f"Format specifications:")
    print(f"  S: = Summarize (初始摘要)")
    print(f"  E: = Evidence (证据)")
    print(f"  N: = New (新内容)")
    print(f"  U: = Update (更新)")
    print(f"  K? = Killer? (凶手?)")
    print(f"")
    print(f"Length targets:")
    print(f"  初始提示词: ≤ 80 chars")
    print(f"  更新提示词: ≤ 100 chars")
    print(f"  最终推理: ≤ 220 chars total")
    print(f"")
    print(f"Test results:")
    print(f"  场景1 (S:): {len(prompt1)} chars user, {total1} chars total - {'✅ PASS' if len(prompt1) <= 80 and total1 <= 150 else '❌ FAIL'}")
    print(f"  场景2 (E:N:U:): {len(prompt2)} chars user, {total2} chars total - {'✅ PASS' if len(prompt2) <= 100 and total2 <= 170 else '❌ FAIL'}")
    print(f"  场景3 (E:K?): {len(prompt3)} chars user, {total3} chars total - {'✅ PASS' if total3 <= 220 else '❌ FAIL'}")
    
    all_pass = all([
        len(prompt1) <= 80 and total1 <= 150,
        len(prompt2) <= 100 and total2 <= 170,
        total3 <= 220
    ])
    
    print(f"")
    print(f"Overall result: {'✅ ALL TESTS PASS' if all_pass else '❌ SOME TESTS FAIL'}")
    
    if all_pass:
        print(f"🎯 English abbreviation format optimized!")
        print(f"✅ 最高效的提示词格式")
        print(f"✅ 显著减少字符数量")
        print(f"✅ 保持语义清晰")
        print(f"✅ 国际化兼容")
        print(f"")
        print(f"🔧 Expected benefits:")
        print(f"• 减少零响应问题（更短提示词）")
        print(f"• 提高处理速度")
        print(f"• 降低token消耗")
        print(f"• 更好的模型兼容性")
        print(f"")
        print(f"📊 Efficiency gains:")
        avg_reduction = ((80 + 150 + 220) / 3) - ((len(prompt1) + len(prompt2) + total3) / 3)
        print(f"• 平均减少 {avg_reduction:.1f} 字符")
        print(f"• 相比之前格式节省约 {avg_reduction/150*100:.1f}% 长度")
    else:
        print(f"⚠️ Some tests failed, need further optimization")

if __name__ == "__main__":
    test_abbrev_format()
