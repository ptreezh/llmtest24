#!/usr/bin/env python
# -*- coding: utf-8 -*-

import ollama
import os
from adaptive_prompts import get_adaptive_messages

MODEL_TO_TEST = 'mistral' # This will be replaced by the master script

PROMPT = """
You are a pure logical reasoning engine. Solve the following problem and provide a detailed step-by-step explanation.

Problem:
In a room, there are three light bulbs. Outside the room, there are three switches, each corresponding to one bulb. You are outside the room and cannot see the bulbs. You have only ONE chance to enter the room. How do you determine with certainty which switch controls which bulb?
"""

def test_logic():
    print(f"--- Testing Pillar 1: Logical-Causal Reasoning on [{MODEL_TO_TEST}] ---")
    print(f"PROMPT:\n{PROMPT}")
    
    try:
        response = ollama.chat(
            model=MODEL_TO_TEST,
            messages=get_adaptive_messages(model_name=MODEL_TO_TEST, prompt_text=PROMPT, test_script_name=os.path.basename(__file__)),
            options={'temperature': 0.0} # Use low temperature for deterministic results
        )
        print("\nMODEL RESPONSE:")
        print(response['message']['content'])
    except Exception as e:
        print(f"\nAn error occurred: {e}")

if __name__ == '__main__':
    test_logic()