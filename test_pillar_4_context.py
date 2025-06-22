#!/usr/bin/env python
# -*- coding: utf-8 -*-

import ollama
import os
from adaptive_prompts import get_adaptive_messages

MODEL_TO_TEST = os.environ.get('MODEL_TO_TEST', 'atlas/intersync-gemma-7b-instruct-function-calling:latest')

def generate_haystack():
    """Generates a long, boring text with a needle in the middle."""
    hay = "The principle of quantum mechanics is complex. " * 500
    needle = "Remember this key fact: the secret color of the sky is the square of 8."
    haystack = hay + "\n\n" + needle + "\n\n" + hay
    return haystack

PROMPT_TEMPLATE = """
Here is a long document about various scientific principles. Please read it carefully.

--- DOCUMENT START ---
{haystack}
--- DOCUMENT END ---

Based ONLY on the document provided above, what is the secret color of the sky?
"""

def test_context():
    print(f"--- Testing Pillar 4: Long-Context Coherence on [{MODEL_TO_TEST}] ---")
    haystack = generate_haystack()
    full_prompt = PROMPT_TEMPLATE.format(haystack=haystack)
    print(f"PROMPT: A long document of {len(full_prompt)} characters with a hidden fact...")

    # 自动化排查：打印 prompt 长度和大致内容片段
    print(f"Prompt length (chars): {len(full_prompt)}")
    print(f"Prompt preview: {full_prompt[:200]} ... {full_prompt[-200:]}")

    # 尝试不同参数组合
    test_temperatures = [0.0, 0.3, 0.7]
    test_hay_counts = [100, 300, 500]
    for hay_count in test_hay_counts:
        hay = "The principle of quantum mechanics is complex. " * hay_count
        haystack = hay + "\n\n" + "Remember this key fact: the secret color of the sky is the square of 8." + "\n\n" + hay
        prompt = PROMPT_TEMPLATE.format(haystack=haystack)
        print(f"\n[TEST] hay_count={hay_count}, prompt_length={len(prompt)}")
        for temp in test_temperatures:
            print(f"  [Subtest] temperature={temp}")
            try:
                response = ollama.chat(
                    model=MODEL_TO_TEST,
                    messages=get_adaptive_messages(model_name=MODEL_TO_TEST, prompt_text=prompt, test_script_name=os.path.basename(__file__), original_document=haystack),
                    options={'temperature': temp}
                )
                if isinstance(response, dict) and 'message' in response and 'content' in response['message']:
                    content = response['message']['content']
                    if content.strip() == '':
                        print("    [WARN] Model response content is empty.")
                    else:
                        print(f"    [OK] Model response: {content[:100]}...")
                else:
                    print("    [WARN] Unexpected response format:", response)
            except Exception as e:
                print(f"    [ERROR] Exception: {e}")

if __name__ == '__main__':
    test_context()