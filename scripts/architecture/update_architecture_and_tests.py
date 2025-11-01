"""
Script to update architecture maps and generate tests.
This script should be run regularly to keep the architecture maps and tests up-to-date.
"""

import subprocess
import sys
from pathlib import Path

def update_architecture_and_tests():
    """Update architecture maps and generate tests."""
    print("Updating architecture maps and generating tests...")
    
    # Update architecture maps
    print("1. Updating architecture maps...")
    result = subprocess.run([
        sys.executable, "project_architecture_map.py",
        "--root", ".",
        "--architecture-file", "architecture_map.json",
        "--interface-file", "interface_map.json",
        "--verbose"
    ], capture_output=True, text=True)
    
    if result.returncode != 0:
        print(f"Error updating architecture maps: {result.stderr}")
        return False
    
    print(result.stdout)
    
    # Generate tests based on updated maps
    print("2. Generating tests...")
    result = subprocess.run([
        sys.executable, "enhanced_test_generator.py",
        "--interface-map", "interface_map.json",
        "--output-dir", "tests/generated",
        "--interface", "IndependenceTestBase",
        "--verbose"
    ], capture_output=True, text=True)
    
    if result.returncode != 0:
        print(f"Error generating tests: {result.stderr}")
        return False
    
    print(result.stdout)
    print("Architecture maps and tests updated successfully!")
    return True

if __name__ == "__main__":
    update_architecture_and_tests()
