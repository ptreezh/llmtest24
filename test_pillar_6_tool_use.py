#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import ollama
import json
import os
from adaptive_prompts import get_adaptive_messages

MODEL_TO_TEST = 'mistral'

PROMPT = """
You are an AI assistant that can only respond with a JSON array of tool calls. You have the following tools available:
- `search_flight(from: str, to: str, date: str)`
- `book_hotel(city: str, check_in_date: str, check_out_date: str)`

User Instruction: 'Please find me a flight from Shanghai to Beijing for the day after tomorrow, and then book a hotel in Beijing for two nights.'
Assume today's date is 2024-05-20.

Your task is to output a JSON array of the tool calls you need to make, in the correct order. Your response must be only the JSON array.
"""

def test_tool_use():
    print(f"--- Testing Pillar 6: Tool Use & Agency Potential on [{MODEL_TO_TEST}] ---")
    print(f"PROMPT:\n{PROMPT}")
    
    try:
        response = ollama.chat(
            model=MODEL_TO_TEST,
            messages=get_adaptive_messages(model_name=MODEL_TO_TEST, prompt_text=PROMPT, test_script_name=os.path.basename(__file__)),
            options={'temperature': 0.0}
        )
        raw_content = response['message']['content']
        cleaned_content = raw_content.strip().replace('```json\n', '').replace('```', '').strip()
        print("\nMODEL RESPONSE (cleaned):")
        print(cleaned_content)
        try:
            json.loads(cleaned_content)
            print("\n[Auto-Check] Response is valid JSON.")
        except Exception as e:
            print(f"\n[Auto-Check Fail] Invalid JSON: {e}")

    except Exception as e:
        print(f"\nAn error occurred: {e}")

if __name__ == '__main__':
    test_tool_use()