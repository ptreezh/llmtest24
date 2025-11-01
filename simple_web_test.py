#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Simple web interface test for LLM Advanced Testing Suite
"""

import sys
import time
import subprocess
from pathlib import Path

def test_web_interface_simple():
    """Simple web interface test"""
    print("LLM Advanced Testing Suite - Simple Web Interface Test")
    print("=" * 60)
    
    # Check if visual_test_interface.py exists
    script_path = Path("visual_test_interface.py")
    if not script_path.exists():
        print("ERROR: visual_test_interface.py not found")
        return False
    
    print("OK: visual_test_interface.py found")
    
    # Check if streamlit is available
    try:
        import streamlit
        print(f"OK: Streamlit is available (version: {streamlit.__version__})")
    except ImportError:
        print("ERROR: Streamlit is not available")
        return False
    
    # Try to import the visual_test_interface module
    try:
        sys.path.append('.')
        import visual_test_interface
        print("OK: visual_test_interface module can be imported")
        return True
    except Exception as e:
        print(f"ERROR: Failed to import visual_test_interface: {e}")
        return False

def main():
    """Main function"""
    success = test_web_interface_simple()
    
    if success:
        print("\nSimple web interface test PASSED!")
        print("The web interface module is ready to use.")
        return True
    else:
        print("\nSimple web interface test FAILED!")
        print("Please check the error messages above.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)