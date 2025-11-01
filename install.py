#!/usr/bin/env python3
"""
LLM Advanced Testing Suite - Installation Script
This script helps users set up the testing suite environment.
"""

import os
import sys
import subprocess
import platform
from pathlib import Path
import shutil

def print_header():
    """Print installation header"""
    print("=" * 60)
    print("🚀 LLM Advanced Testing Suite - Installation")
    print("=" * 60)
    print()

def check_python_version():
    """Check if Python version is compatible"""
    print("🔍 Checking Python version...")
    
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        print(f"Current version: {sys.version}")
        sys.exit(1)
    
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor} is compatible")
    print()

def check_pip():
    """Check if pip is available"""
    print("🔍 Checking pip availability...")
    
    try:
        subprocess.run([sys.executable, "-m", "pip", "--version"], 
                      check=True, capture_output=True)
        print("✅ pip is available")
        print()
    except subprocess.CalledProcessError:
        print("❌ pip is not available")
        print("Please install pip first")
        sys.exit(1)

def create_virtual_environment():
    """Create virtual environment if it doesn't exist"""
    print("🔍 Checking for virtual environment...")
    
    venv_path = Path("venv")
    if venv_path.exists():
        print("✅ Virtual environment already exists")
        print()
        return
    
    print("📦 Creating virtual environment...")
    try:
        subprocess.run([sys.executable, "-m", "venv", "venv"], 
                      check=True, capture_output=True)
        print("✅ Virtual environment created successfully")
        print()
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to create virtual environment: {e}")
        sys.exit(1)

def activate_virtual_environment():
    """Print activation commands"""
    print("🔧 To activate the virtual environment:")
    
    if platform.system() == "Windows":
        print("  venv\\Scripts\\activate")
    else:
        print("  source venv/bin/activate")
    print()

def install_dependencies():
    """Install required dependencies"""
    print("📦 Installing dependencies...")
    
    # Upgrade pip first
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "--upgrade", "pip"], 
                      check=True)
        print("✅ pip upgraded")
    except subprocess.CalledProcessError:
        print("⚠️  Failed to upgrade pip, continuing...")
    
    # Install requirements
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], 
                      check=True)
        print("✅ Core dependencies installed")
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install core dependencies: {e}")
        sys.exit(1)
    
    # Install optional dependencies if user wants
    install_optional = input("\n🤔 Install optional dependencies? (y/N): ").lower().strip()
    if install_optional in ['y', 'yes']:
        try:
            subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements-optional.txt"], 
                          check=True)
            print("✅ Optional dependencies installed")
        except subprocess.CalledProcessError as e:
            print(f"⚠️  Failed to install some optional dependencies: {e}")
    
    print()

def setup_environment():
    """Set up environment configuration"""
    print("⚙️  Setting up environment configuration...")
    
    env_file = Path("config/.env")
    env_example = Path("config/.env.example")
    
    if not env_file.exists() and env_example.exists():
        print("📝 Creating .env file from template...")
        shutil.copy2(env_example, env_file)
        print("✅ .env file created")
        print("📝 Please edit config/.env with your API keys and model configurations")
    elif env_file.exists():
        print("✅ .env file already exists")
    else:
        print("⚠️  .env.example not found, please create config/.env manually")
    
    print()

def run_initial_tests():
    """Run initial tests to verify installation"""
    print("🧪 Running initial tests...")
    
    try:
        # Test basic imports
        subprocess.run([sys.executable, "-c", "
import sys
sys.path.append('.')
try:
    from core.framework import TestFramework
    from config.config import MODEL_TO_TEST
    print('✅ Core modules imported successfully')
except ImportError as e:
    print(f'❌ Import error: {e}')
    sys.exit(1)
        "], check=True, capture_output=True)
        print("✅ Initial tests passed")
    except subprocess.CalledProcessError as e:
        print(f"❌ Initial tests failed: {e}")
        print("Please check the installation")
        return False
    
    print()
    return True

def create_directories():
    """Create necessary directories"""
    print("📁 Creating necessary directories...")
    
    directories = [
        "testout",
        "results", 
        "test_logs",
        "memory_db",
        "docs/build",
        "examples"
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        print(f"✅ Created: {directory}")
    
    print()

def print_next_steps():
    """Print next steps for the user"""
    print("🎉 Installation completed successfully!")
    print()
    print("📋 Next steps:")
    print("1. Activate virtual environment:")
    if platform.system() == "Windows":
        print("   venv\\Scripts\\activate")
    else:
        print("   source venv/bin/activate")
    print()
    print("2. Configure your models:")
    print("   - Edit config/.env with your API keys")
    print("   - Update config/models.txt with your model configurations")
    print()
    print("3. Run your first test:")
    print("   python scripts/main_orchestrator.py --model your_model_name")
    print()
    print("4. For more information, see:")
    print("   - README.md for quick start guide")
    print("   - docs/ for detailed documentation")
    print("   - CONTRIBUTING.md for development guidelines")
    print()

def main():
    """Main installation function"""
    print_header()
    
    check_python_version()
    check_pip()
    create_virtual_environment()
    activate_virtual_environment()
    install_dependencies()
    create_directories()
    setup_environment()
    
    if run_initial_tests():
        print_next_steps()
    else:
        print("❌ Installation completed with some issues.")
        print("Please check the error messages above and try again.")
        sys.exit(1)

if __name__ == "__main__":
    main()