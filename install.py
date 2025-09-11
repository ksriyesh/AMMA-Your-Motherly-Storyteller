#!/usr/bin/env python3
"""
AMMA Installation Script
Installs all Python and Node.js dependencies in one command.
"""

import os
import sys
import subprocess
import platform
from pathlib import Path


def run_command(command, cwd=None, shell=False):
    """Run a command and return success status."""
    try:
        print(f"🔧 Running: {command}")
        if isinstance(command, str) and not shell:
            command = command.split()
        
        result = subprocess.run(
            command, 
            cwd=cwd, 
            shell=shell,
            capture_output=True, 
            text=True
        )
        
        if result.returncode == 0:
            print("✅ Success!")
            if result.stdout.strip():
                print(f"   Output: {result.stdout.strip()}")
            return True
        else:
            print(f"❌ Failed with code {result.returncode}")
            if result.stderr.strip():
                print(f"   Error: {result.stderr.strip()}")
            return False
    except Exception as e:
        print(f"❌ Exception: {e}")
        return False


def check_python_version():
    """Check if Python version is 3.11+"""
    version = sys.version_info
    if version.major == 3 and version.minor >= 11:
        print(f"✅ Python {version.major}.{version.minor}.{version.micro} - Compatible")
        return True
    else:
        print(f"❌ Python {version.major}.{version.minor}.{version.micro} - Requires Python 3.11+")
        return False


def check_node_version():
    """Check if Node.js is installed and version 18+"""
    try:
        result = subprocess.run(["node", "--version"], capture_output=True, text=True)
        if result.returncode == 0:
            version_str = result.stdout.strip().replace('v', '')
            major_version = int(version_str.split('.')[0])
            if major_version >= 18:
                print(f"✅ Node.js {version_str} - Compatible")
                return True
            else:
                print(f"❌ Node.js {version_str} - Requires Node.js 18+")
                return False
        else:
            print("❌ Node.js not found")
            return False
    except Exception:
        print("❌ Node.js not found")
        return False


def install_python_dependencies():
    """Install Python dependencies."""
    print("\n📦 Installing Python dependencies...")
    
    # Check if we're in a virtual environment
    in_venv = hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix)
    
    if not in_venv:
        print("⚠️  Not in a virtual environment. Creating one...")
        if not run_command("python -m venv .venv"):
            return False
        
        # Activate virtual environment
        if platform.system() == "Windows":
            activate_script = ".venv\\Scripts\\activate.bat"
            pip_cmd = ".venv\\Scripts\\pip"
        else:
            activate_script = ".venv/bin/activate"
            pip_cmd = ".venv/bin/pip"
        
        print(f"💡 Virtual environment created. Activate it with: {activate_script}")
    else:
        pip_cmd = "pip"
        print("✅ Already in virtual environment")
    
    # Install dependencies
    commands = [
        f"{pip_cmd} install --upgrade pip",
        f"{pip_cmd} install -e ."
    ]
    
    for cmd in commands:
        if not run_command(cmd, shell=True):
            return False
    
    return True


def install_node_dependencies():
    """Install Node.js dependencies."""
    print("\n📦 Installing Node.js dependencies...")
    
    frontend_dir = Path("AMMA-UI")
    if not frontend_dir.exists():
        print("❌ AMMA-UI directory not found")
        return False
    
    # Try different package managers
    package_managers = ["npm", "yarn", "pnpm"]
    
    for pm in package_managers:
        try:
            # Check if package manager is available
            result = subprocess.run([pm, "--version"], capture_output=True, text=True)
            if result.returncode == 0:
                print(f"✅ Using {pm}")
                return run_command(f"{pm} install", cwd=frontend_dir)
        except FileNotFoundError:
            continue
    
    print("❌ No package manager found (npm, yarn, or pnpm)")
    return False


def check_env_file():
    """Check if .env file exists and has required variables."""
    env_file = Path(".env")
    if env_file.exists():
        content = env_file.read_text()
        if "OPENAI_API_KEY" in content:
            print("✅ .env file found with OPENAI_API_KEY")
            return True
        else:
            print("⚠️  .env file exists but missing OPENAI_API_KEY")
    else:
        print("⚠️  .env file not found")
    
    print("\n💡 Create a .env file with your OpenAI API key:")
    print("   echo 'OPENAI_API_KEY=your_key_here' > .env")
    return False


def main():
    """Main installation process."""
    print("🌙" + "="*50 + "🌙")
    print("    AMMA - Bedtime Story Agent Installer")
    print("🌙" + "="*50 + "🌙")
    print()
    
    # Check prerequisites
    print("🔍 Checking prerequisites...")
    
    python_ok = check_python_version()
    node_ok = check_node_version()
    
    if not python_ok:
        print("\n❌ Python 3.11+ is required. Please install it first.")
        sys.exit(1)
    
    if not node_ok:
        print("\n❌ Node.js 18+ is required. Please install it first.")
        print("   Download from: https://nodejs.org/")
        sys.exit(1)
    
    print("\n✅ All prerequisites met!")
    
    # Install dependencies
    success = True
    
    if not install_python_dependencies():
        success = False
    
    if not install_node_dependencies():
        success = False
    
    # Check environment
    check_env_file()
    
    # Final status
    print("\n" + "="*60)
    if success:
        print("🎉 Installation completed successfully!")
        print()
        print("🚀 Next steps:")
        print("   1. Set up your .env file with OPENAI_API_KEY")
        print("   2. Run: python start_app.py")
        print("   3. Visit: http://localhost:3000")
        print()
        print("📖 Or try the CLI: python main.py")
    else:
        print("❌ Installation failed. Please check the errors above.")
        sys.exit(1)


if __name__ == "__main__":
    main()
