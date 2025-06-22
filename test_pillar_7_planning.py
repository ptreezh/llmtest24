#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import ollama
import os
from adaptive_prompts import get_adaptive_messages

MODEL_TO_TEST = 'mistral'

PROMPT = """
You are a senior Project Manager. A client wants a 'Personal Blog Website' to go live in one month.

Your task:
1. Create a Work Breakdown Structure (WBS) using a Markdown list. The WBS should be decomposed to at least three levels.
2. After the WBS, identify and list at least two critical task dependencies (e.g., 'Task A must be completed before Task B').
"""

def test_planning():
    print(f"--- Testing Pillar 7: Task Decomposition & Planning on [{MODEL_TO_TEST}] ---")
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
    test_planning()