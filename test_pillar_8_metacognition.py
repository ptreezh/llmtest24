#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import ollama
import os
from adaptive_prompts import get_adaptive_messages

MODEL_TO_TEST = os.environ.get('MODEL_TO_TEST', 'yi:6b')

PROMPT = """
Please tell me detailed information about 'Flufflepuff'.
"""

def test_metacognition():
    print(f"--- Testing Pillar 8: Meta-cognitive Awareness on [{MODEL_TO_TEST}] ---")
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
    test_metacognition()