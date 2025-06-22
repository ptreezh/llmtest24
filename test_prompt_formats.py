#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试不同提示词格式的效率
比较代码形式、中文、英文缩写、符号形式
"""

def get_prompt_format1_code(prompt_type: str, context: dict = {}) -> str:
    """代码形式 - 最精简"""
    if prompt_type == "intermediate":
        if context.get('summary_so_far', '').strip():
            summary = context['summary_so_far'][:60]
            new_content = context['new_dialogue_chunk'][:50]
            return f"sum({summary},{new_content})"
        else:
            content = context['new_dialogue_chunk'][:70]
            return f"sum({content})"
    elif prompt_type == "final":
        facts = context.get('summary_so_far', '')[:70]
        return f"killer({facts})"

def get_prompt_format2_chinese(prompt_type: str, context: dict = {}) -> str:
    """中文简化形式"""
    if prompt_type == "intermediate":
        if context.get('summary_so_far', '').strip():
            summary = context['summary_so_far'][:60]
            new_content = context['new_dialogue_chunk'][:50]
            return f"证据:{summary} 新:{new_content} 更新:"
        else:
            content = context['new_dialogue_chunk'][:70]
            return f"总结:{content}"
    elif prompt_type == "final":
        facts = context.get('summary_so_far', '')[:70]
        return f"证据:{facts} 凶手?"

def get_prompt_format3_abbrev(prompt_type: str, context: dict = {}) -> str:
    """英文缩写形式"""
    if prompt_type == "intermediate":
        if context.get('summary_so_far', '').strip():
            summary = context['summary_so_far'][:60]
            new_content = context['new_dialogue_chunk'][:50]
            return f"E:{summary} N:{new_content} U:"
        else:
            content = context['new_dialogue_chunk'][:70]
            return f"S:{content}"
    elif prompt_type == "final":
        facts = context.get('summary_so_far', '')[:70]
        return f"E:{facts} K?"

def get_prompt_format4_symbol(prompt_type: str, context: dict = {}) -> str:
    """符号形式"""
    if prompt_type == "intermediate":
        if context.get('summary_so_far', '').strip():
            summary = context['summary_so_far'][:60]
            new_content = context['new_dialogue_chunk'][:50]
            return f"[{summary}]+[{new_content}]=?"
        else:
            content = context['new_dialogue_chunk'][:70]
            return f"[{content}]=?"
    elif prompt_type == "final":
        facts = context.get('summary_so_far', '')[:70]
        return f"[{facts}]->?"

def test_prompt_formats():
    """测试不同提示词格式"""
    print("🧪 Testing Different Prompt Formats for Atlas Model")
    print("="*60)
    
    system_prompt = "Detective. Analyze murder case. Summarize key evidence concisely."
    print(f"System prompt: {len(system_prompt)} chars")
    
    # 测试数据
    test_dialogue = "A：昨晚听到奇怪声音。B：看到黑影在老橡树附近。C：张三丢了斧头。D：脚印很大。"
    test_summary = "昨晚听到声音，看到黑影，张三丢斧头，发现脚印。"
    
    print(f"\nTest data:")
    print(f"  Dialogue: '{test_dialogue}' ({len(test_dialogue)} chars)")
    print(f"  Summary: '{test_summary}' ({len(test_summary)} chars)")
    
    formats = [
        ("代码形式", get_prompt_format1_code),
        ("中文简化", get_prompt_format2_chinese),
        ("英文缩写", get_prompt_format3_abbrev),
        ("符号形式", get_prompt_format4_symbol)
    ]
    
    print(f"\n" + "="*60)
    print(f"📊 Format Comparison Results")
    print(f"="*60)
    
    for format_name, format_func in formats:
        print(f"\n--- {format_name} ---")
        
        # 测试初始提示词
        context1 = {"new_dialogue_chunk": test_dialogue}
        prompt1 = format_func("intermediate", context1)
        total1 = len(system_prompt) + len(prompt1)
        
        # 测试更新提示词
        context2 = {
            "summary_so_far": test_summary,
            "new_dialogue_chunk": test_dialogue
        }
        prompt2 = format_func("intermediate", context2)
        total2 = len(system_prompt) + len(prompt2)
        
        # 测试最终推理
        context3 = {"summary_so_far": test_summary}
        prompt3 = format_func("final", context3)
        total3 = len(system_prompt) + len(prompt3)
        
        print(f"  初始: '{prompt1}' ({len(prompt1)} chars, total: {total1})")
        print(f"  更新: '{prompt2}' ({len(prompt2)} chars, total: {total2})")
        print(f"  推理: '{prompt3}' ({len(prompt3)} chars, total: {total3})")
        print(f"  平均长度: {(len(prompt1) + len(prompt2) + len(prompt3)) / 3:.1f} chars")
    
    # 汇总比较
    print(f"\n" + "="*60)
    print(f"📋 Summary Comparison")
    print(f"="*60)
    
    results = []
    for format_name, format_func in formats:
        context1 = {"new_dialogue_chunk": test_dialogue}
        context2 = {"summary_so_far": test_summary, "new_dialogue_chunk": test_dialogue}
        context3 = {"summary_so_far": test_summary}
        
        prompt1 = format_func("intermediate", context1)
        prompt2 = format_func("intermediate", context2)
        prompt3 = format_func("final", context3)
        
        avg_length = (len(prompt1) + len(prompt2) + len(prompt3)) / 3
        max_total = max(
            len(system_prompt) + len(prompt1),
            len(system_prompt) + len(prompt2),
            len(system_prompt) + len(prompt3)
        )
        
        results.append((format_name, avg_length, max_total))
    
    # 按平均长度排序
    results.sort(key=lambda x: x[1])
    
    print(f"Ranking by efficiency (shorter = better):")
    for i, (name, avg_len, max_total) in enumerate(results, 1):
        print(f"  {i}. {name}: 平均 {avg_len:.1f} chars, 最大总长 {max_total} chars")
    
    # 推荐
    best_format = results[0]
    print(f"\n🎯 Recommendation:")
    print(f"  Most efficient: {best_format[0]}")
    print(f"  Average prompt length: {best_format[1]:.1f} chars")
    print(f"  Max total length: {best_format[2]} chars")
    
    # 分析优缺点
    print(f"\n🔍 Analysis:")
    print(f"  代码形式: 最短，但可能影响模型理解")
    print(f"  中文简化: 平衡效率和理解性")
    print(f"  英文缩写: 简短，国际化")
    print(f"  符号形式: 直观，但可能不够明确")
    
    print(f"\n💡 For Atlas model optimization:")
    print(f"  • 优先考虑最短的格式减少零响应")
    print(f"  • 保持足够的语义信息")
    print(f"  • 测试实际响应质量")

if __name__ == "__main__":
    test_prompt_formats()
