#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Dependency installation script for LLM Advanced Testing Suite
"""

import sys
import subprocess
import importlib

def check_and_install_package(package_name, pip_name=None):
    """Check if a package is installed, and install if not"""
    if pip_name is None:
        pip_name = package_name
    
    try:
        importlib.import_module(package_name)
        print(f"OK: {package_name} is already installed")
        return True
    except ImportError:
        print(f"ERROR: {package_name} is not installed, installing...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", pip_name])
            print(f"OK: {package_name} installed successfully")
            return True
        except subprocess.CalledProcessError as e:
            print(f"ERROR: Failed to install {package_name}: {e}")
            return False

def main():
    """Main function"""
    print("LLM Advanced Testing Suite - Dependency Installation")
    print("=" * 60)
    
    # List of required packages
    required_packages = [
        ("dotenv", "python-dotenv"),
        ("yaml", "pyyaml"),
        ("pandas", "pandas"),
        ("numpy", "numpy"),
        ("matplotlib", "matplotlib"),
        ("seaborn", "seaborn"),
        ("pydantic", "pydantic"),
        ("requests", "requests"),
        ("streamlit", "streamlit"),
    ]
    
    # Check and install each package
    all_success = True
    for package_name, pip_name in required_packages:
        if not check_and_install_package(package_name, pip_name):
            all_success = False
    
    if all_success:
        print("\nAll dependencies installed successfully!")
    else:
        print("\nSome dependencies failed to install. Please check the error messages above.")
    
    return all_success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)