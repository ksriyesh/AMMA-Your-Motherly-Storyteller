#!/usr/bin/env python3
"""AMMA Installation Script
Installs all Python and Node.js dependencies in one command.
"""

import platform
import subprocess
import sys
from pathlib import Path


def run_command(command, cwd=None, shell=False):
    """Run a command and return success status."""
    try:
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
            if result.stdout.strip():
                pass
            return True
        else:
            if result.stderr.strip():
                pass
            return False
    except Exception:
        return False


def check_python_version():
    """Check if Python version is 3.11+."""
    version = sys.version_info
    if version.major == 3 and version.minor >= 11:
        return True
    else:
        return False


def check_node_version():
    """Check if Node.js is installed and version 18+."""
    try:
        result = subprocess.run(["node", "--version"], capture_output=True, text=True)
        if result.returncode == 0:
            version_str = result.stdout.strip().replace('v', '')
            major_version = int(version_str.split('.')[0])
            if major_version >= 18:
                return True
            else:
                return False
        else:
            return False
    except Exception:
        return False


def install_python_dependencies():
    """Install Python dependencies."""
    # Check if we're in a virtual environment
    in_venv = hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix)
    
    if not in_venv:
        if not run_command("python -m venv .venv"):
            return False
        
        # Activate virtual environment
        if platform.system() == "Windows":
            pip_cmd = ".venv\\Scripts\\pip"
        else:
            pip_cmd = ".venv/bin/pip"
        
    else:
        pip_cmd = "pip"
    
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
    frontend_dir = Path("AMMA-UI")
    if not frontend_dir.exists():
        return False
    
    # Try different package managers
    package_managers = ["npm", "yarn", "pnpm"]
    
    for pm in package_managers:
        try:
            # Check if package manager is available
            result = subprocess.run([pm, "--version"], capture_output=True, text=True)
            if result.returncode == 0:
                return run_command(f"{pm} install", cwd=frontend_dir)
        except FileNotFoundError:
            continue
    
    return False


def check_env_file():
    """Check if .env file exists and has required variables."""
    env_file = Path(".env")
    if env_file.exists():
        content = env_file.read_text()
        if "OPENAI_API_KEY" in content:
            return True
        else:
            pass
    else:
        pass
    
    return False


def main():
    """Main installation process."""
    # Check prerequisites
    
    python_ok = check_python_version()
    node_ok = check_node_version()
    
    if not python_ok:
        sys.exit(1)
    
    if not node_ok:
        sys.exit(1)
    
    
    # Install dependencies
    success = True
    
    if not install_python_dependencies():
        success = False
    
    if not install_node_dependencies():
        success = False
    
    # Check environment
    check_env_file()
    
    # Final status
    if success:
        pass
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()
