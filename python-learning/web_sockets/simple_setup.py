#!/usr/bin/env python3
"""
Simple setup script for WebSocket examples
"""

import subprocess
import sys

def install_requirements():
    """Install required packages"""
    print("Installing required packages...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "websockets", "aioconsole"])
        print("✅ Packages installed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error installing packages: {e}")
        return False

def main():
    """Main setup function"""
    print("🚀 Setting up Simple WebSocket Examples")
    print("=" * 40)
    
    if install_requirements():
        print("\n✅ Setup completed!")
        print("\n📚 Next steps:")
        print("1. Start with: python 01_simple_server.py")
        print("2. Read SIMPLE_README.md for instructions")
        print("3. Try the examples in order")
        print("\n🎉 Have fun learning WebSockets!")
    else:
        print("\n❌ Setup failed. Please check the error messages above.")

if __name__ == "__main__":
    main() 