#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import ollama
import os
from adaptive_prompts import get_adaptive_messages

MODEL_TO_TEST = 'mistral'

PROMPT = """
Strictly adhere to ALL of the following rules to rewrite the sentence "The quick brown fox jumps over the lazy dog.":
1. The sentence must be translated into Chinese.
2. The translated sentence must NOT contain the character '的'.
3. The response must begin with the exact phrase '报告长官'.
4. The entire response must be a single line with no line breaks.
5. The response must end with exactly three exclamation marks "!!!".
"""

def test_fidelity():
    print(f"--- Testing Pillar 2: Instructional Fidelity on [{MODEL_TO_TEST}] ---")
    print(f"PROMPT:\n{PROMPT}")
    
    try:
        response = ollama.chat(
            model=MODEL_TO_TEST,
            messages=get_adaptive_messages(model_name=MODEL_TO_TEST, prompt_text=PROMPT, test_script_name=os.path.basename(__file__)),
            options={'temperature': 0.0}
        )
        print("\nMODEL RESPONSE:")
        print(response['message']['content'])
    except Exception as e:
        print(f"\nAn error occurred: {e}")

if __name__ == '__main__':
    test_fidelity()