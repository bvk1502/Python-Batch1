#!/usr/bin/env python3
"""
Setup script for WebSocket tutorial
"""

import subprocess
import sys
import os

def install_requirements():
    """Install required packages"""
    print("Installing required packages...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ All packages installed successfully!")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error installing packages: {e}")
        return False
    return True

def create_directories():
    """Create necessary directories"""
    directories = ["logs", "data"]
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)
            print(f"�� Created directory: {directory}")

def main():
    """Main setup function"""
    print("🚀 Setting up WebSocket Tutorial Environment")
    print("=" * 50)
    
    # Install requirements
    if not install_requirements():
        print("Setup failed. Please check the error messages above.")
        return
    
    # Create directories
    create_directories()
    
    print("\n✅ Setup completed successfully!")
    print("\n📚 Next steps:")
    print("1. Start with: python 01_basic_server.py")
    print("2. Read the README.md for detailed instructions")
    print("3. Run examples in separate terminals")
    print("\n🎉 Happy WebSocket programming!")

if __name__ == "__main__":
    main() 