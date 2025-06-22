#!/usr/bin/env python
# -*- coding: utf-8 -*-

import ollama
import os
from adaptive_prompts import get_adaptive_messages

MODEL_TO_TEST = 'mistral'

PROMPT = """
You are an expert chemist. Balance the following chemical equation and explain your balancing logic step-by-step:
C7H6O2 + O2 -> CO2 + H2O
"""

def test_knowledge():
    print(f"--- Testing Pillar 5: Applied Domain Knowledge on [{MODEL_TO_TEST}] ---")
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
    test_knowledge()