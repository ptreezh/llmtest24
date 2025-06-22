import requests
import os

def split_long_text(text, max_length):
    return [text[i:i+max_length] for i in range(0, len(text), max_length)]

OLLAMA_API_URL = 'http://localhost:11434/api/chat'
# 只测试 atlas/intersync-gemma-7b-instruct-function-calling:latest
MODEL_TO_TEST = 'atlas/intersync-gemma-7b-instruct-function-calling:latest'

def call_ollama(model, prompt, temperature=0.1):
    payload = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "stream": False,
        "options": {"temperature": temperature}
    }
    try:
        response = requests.post(OLLAMA_API_URL, json=payload, timeout=120)
        response.raise_for_status()
        data = response.json()
        return data.get('message', {}).get('content', '')
    except Exception as e:
        print(f"[ERROR] API call failed: {e}")
        return ''

PROMPT_TEMPLATE = """
Here is a long document about various scientific principles. Please read it carefully.

--- DOCUMENT START ---
{haystack}
--- DOCUMENT END ---

Based ONLY on the document provided above, what is the secret color of the sky?
"""

def test_context_multi_turn():
    print("--- Testing Pillar 4: Multi-turn Summarization/Dialogue (TestLLM style) ---")
    hay = "The principle of quantum mechanics is complex. " * 500
    needle = "Remember this key fact: the secret color of the sky is the square of 8."
    haystack = hay + "\n\n" + needle + "\n\n" + hay
    full_prompt = PROMPT_TEMPLATE.format(haystack=haystack)
    print(f"Full prompt length: {len(full_prompt)}")

    chunk_size = 1500
    chunks = split_long_text(full_prompt, chunk_size)
    summary = ""
    for idx, chunk in enumerate(chunks):
        print(f"\n[Multi-turn] Round {idx+1}/{len(chunks)} | Chunk size: {len(chunk)}")
        if idx == 0:
            prompt = chunk
        else:
            prompt = f"Here is the previous summary:\n{summary}\n\nHere is the next part of the document:\n{chunk}\n\nPlease update the summary to include all new facts from this part."
        content = call_ollama(MODEL_TO_TEST, prompt, temperature=0.1)
        if content.strip() == '':
            print("    [WARN] Model response content is empty.")
        else:
            print(f"    [OK] Model response: {content[:100]}...")
            summary = content
    print("\nFinal summary after multi-turn dialogue:")
    print(summary)

if __name__ == '__main__':
    test_context_multi_turn()
