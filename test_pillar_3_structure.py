#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import ollama
import json
import os
from adaptive_prompts import get_adaptive_messages

MODEL_TO_TEST = 'mistral'

PROMPT = """
You are a data processing API. Convert the following unstructured information into a strict JSON object.
Information: "Our project 'Phoenix', code-named PX, is led by John Doe (john.doe@example.com) and is currently in the Alpha testing phase. It has three main milestones: M1, M2, and M3. The current budget is $50,000."

JSON Schema Requirements:
- Root object.
- `projectName`: string.
- `codeName`: string, must be uppercase.
- `leader`: an object with `name` and `email` keys.
- `status`: string, must be one of: ["Planning", "Alpha", "Beta", "GA"].
- `milestones`: an array of strings.
- `budget`: a number, without currency symbols.
Your response must be ONLY the JSON object, with no extra text or markdown code fences.
"""

def test_structure():
    print(f"--- Testing Pillar 3: Structural & Abstract Manipulation on [{MODEL_TO_TEST}] ---")
    print(f"PROMPT:\n{PROMPT}")
    
    try:
        response = ollama.chat(
            model=MODEL_TO_TEST,
            messages=get_adaptive_messages(model_name=MODEL_TO_TEST, prompt_text=PROMPT, test_script_name=os.path.basename(__file__)),
            options={'temperature': 0.0}
        )
        raw_content = response['message']['content']
        # Clean the response to remove common markdown wrappers
        cleaned_content = raw_content.strip().replace('```json\n', '').replace('```', '').strip()
        print("\nMODEL RESPONSE (cleaned):")
        print(cleaned_content)

        # Automated check
        try:
            parsed = json.loads(cleaned_content)
            print("\n[Auto-Check] JSON is valid.")
            if parsed.get('codeName') != 'PX': print("[Auto-Check Fail] codeName format incorrect.")
            if not isinstance(parsed.get('budget'), (int, float)): print("[Auto-Check Fail] budget type incorrect.")
        except json.JSONDecodeError as e:
            print(f"\n[Auto-Check Fail] Response is not a valid JSON object: {e}")
            
    except Exception as e:
        print(f"\nAn error occurred: {e}")

if __name__ == '__main__':
    test_structure()