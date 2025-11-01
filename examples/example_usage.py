#!/usr/bin/env python3
"""
LLM Advanced Testing Suite - Example Usage Script
This script demonstrates how to use the testing framework for various scenarios.
"""

import os
import sys
import json
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from scripts.utils.utils import run_single_test, print_assessment_criteria
from config.config import MODEL_TO_TEST

def example_basic_test():
    """Example of running a basic test"""
    print("Example 1: Basic Logic Test")
    print("-" * 40)
    pillar_name = "pillar_01_logic"
    prompt = "If all roses are flowers and some flowers fade quickly, can we conclude that some roses fade quickly? Explain your reasoning step by step."
    model = MODEL_TO_TEST
    
    try:
        result = run_single_test(pillar_name, prompt, model)
        print(f"Test completed successfully")
        print(f"Score: {result.get('score', 'N/A')}")
        print(f"Response: {result.get('model_response', 'N/A')[:200]}...")
        print()
    except Exception as e:
        print(f"Test failed: {e}")
        print()

def example_role_playing_test():
    """Example of running a role-playing test"""
    print("Example 2: Role-Playing Test")
    print("-" * 40)
    pillar_name = "pillar_12_persona"
    prompt = "You are an experienced software architect with 15 years of experience. Explain the key principles of microservices architecture to a junior developer. Include practical examples and common pitfalls to avoid."
    model = MODEL_TO_TEST
    
    try:
        result = run_single_test(pillar_name, prompt, model)
        print(f"Test completed successfully")
        print(f"Score: {result.get('score', 'N/A')}")
        print(f"Response: {result.get('model_response', 'N/A')[:200]}...")
        print()
    except Exception as e:
        print(f"Test failed: {e}")
        print()

def example_creativity_test():
    """Example of running a creativity test"""
    print("Example 3: Creativity Test")
    print("-" * 40)
    pillar_name = "pillar_09_creativity"
    prompt = "Generate 5 innovative business ideas that combine artificial intelligence with sustainable agriculture. For each idea, explain the problem it solves, how it works, and its potential impact."
    model = MODEL_TO_TEST
    
    try:
        result = run_single_test(pillar_name, prompt, model)
        print(f"Test completed successfully")
        print(f"Score: {result.get('score', 'N/A')}")
        print(f"Response: {result.get('model_response', 'N/A')[:200]}...")
        print()
    except Exception as e:
        print(f"Test failed: {e}")
        print()

def main():
    """Run all examples"""
    print("LLM Advanced Testing Suite - Example Usage")
    print("=" * 50)
    print()
    
    # Check if model is configured
    if not MODEL_TO_TEST:
        print("No model configured. Please set MODEL_TO_TEST in config/config.py")
        return
    
    print(f"Using model: {MODEL_TO_TEST}")
    print()
    
    # Run examples
    examples = [
        example_basic_test,
        example_role_playing_test,
        example_creativity_test,
    ]
    
    for example in examples:
        try:
            example()
        except KeyboardInterrupt:
            print("\nExample interrupted by user")
            break
        except Exception as e:
            print(f"Unexpected error in {example.__name__}: {e}")
    
    print()
    print("All examples completed!")
    print()
    print("Tips:")
    print("- Check the test results in the 'testout/' directory")
    print("- View detailed analysis in 'results/' directory")
    print("- Modify prompts and parameters to test different scenarios")
    print("- Use 'python scripts/main_orchestrator.py --help' for more options")

if __name__ == "__main__":
    main()
