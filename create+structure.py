"""
Directory Structure Creation Script for testLLM Enhanced

This script creates the necessary directory structure for the enhanced
cognitive independence testing framework.

Author: AI Assistant
Created: 2024-01-14
"""

import os
from pathlib import Path

def create_directory_structure():
    """Create the enhanced testLLM directory structure"""
    
    base_path = Path(__file__).parent
    
    # Define directory structure
    directories = [
        "docs",
        "independence",
        "memory", 
        "nlp",
        "tests",
        "results",
        "memory_db",
        "models"
    ]
    
    # Create directories
    for directory in directories:
        dir_path = base_path / directory
        dir_path.mkdir(exist_ok=True)
        print(f"Created directory: {dir_path}")
        
        # Create __init__.py files for Python packages
        if directory in ["independence", "memory", "nlp", "results"]:
            init_file = dir_path / "__init__.py"
            if not init_file.exists():
                init_file.touch()
                print(f"Created __init__.py: {init_file}")
    
    print("Directory structure created successfully!")

if __name__ == "__main__":
    create_directory_structure()