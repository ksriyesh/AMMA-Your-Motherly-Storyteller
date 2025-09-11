#!/usr/bin/env python3
"""Startup script for AMMA - Bedtime Story Agent."""

import os
import sys
import subprocess
import time
import signal
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def check_environment():
    """Check if required environment variables are set."""
    required_vars = ["OPENAI_API_KEY"]
    missing_vars = []
    
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        print("ERROR: Missing required environment variables:")
        for var in missing_vars:
            print(f"   - {var}")
        print("\nPlease set these environment variables before starting.")
        return False
    
    return True

def start_backend():
    """Start the FastAPI backend."""
    print("Starting AMMA backend on port 8001...")
    try:
        backend_process = subprocess.Popen([
            sys.executable, "-m", "uvicorn", "app:app",
            "--host", "0.0.0.0",
            "--port", "8001",
            "--reload"
        ])
        return backend_process
    except Exception as e:
        print(f"ERROR: Failed to start backend: {e}")
        return None

def start_frontend():
    """Start the React frontend."""
    print("Starting React frontend on port 3000...")
    ui_dir = Path("AMMA-UI")
    
    if not ui_dir.exists():
        print("ERROR: AMMA-UI directory not found")
        return None
    
    try:
        # Try different package managers
        commands = [
            ["npm.cmd", "run", "dev"],
            ["npm", "run", "dev"],
            ["pnpm.cmd", "dev"],
            ["pnpm", "dev"]
        ]
        
        for cmd in commands:
            try:
                test_result = subprocess.run([cmd[0], "--version"], 
                                           capture_output=True, timeout=5)
                if test_result.returncode == 0:
                    print(f"Using {cmd[0]} to start frontend...")
                    frontend_process = subprocess.Popen(cmd, cwd=ui_dir)
                    return frontend_process
            except:
                continue
        
        print("ERROR: No package manager found (npm, pnpm)")
        return None
        
    except Exception as e:
        print(f"ERROR: Failed to start frontend: {e}")
        return None

def wait_for_backend():
    """Wait for backend to be ready."""
    print("Waiting for backend to start...")
    
    for i in range(30):
        try:
            import requests
            response = requests.get("http://localhost:8001/health", timeout=2)
            if response.status_code == 200:
                print("Backend is ready!")
                return True
        except:
            pass
        time.sleep(1)
        if i % 5 == 0 and i > 0:
            print(f"Still waiting... ({i}/30s)")
    
    print("ERROR: Backend failed to start within timeout")
    return False

def main():
    """Main function."""
    print("AMMA - Bedtime Story Agent")
    print("=" * 40)
    
    # Check environment
    if not check_environment():
        return False
    
    # Start backend
    backend_process = start_backend()
    if not backend_process:
        return False
    
    # Wait for backend
    if not wait_for_backend():
        if backend_process:
            backend_process.terminate()
        return False
    
    # Start frontend
    frontend_process = start_frontend()
    if not frontend_process:
        if backend_process:
            backend_process.terminate()
        return False
    
    print("\nAMMA is now running!")
    print("Frontend: http://localhost:3000")
    print("Backend: http://localhost:8001")
    print("API Docs: http://localhost:8001/docs")
    print("\nPress Ctrl+C to stop")
    
    try:
        # Keep running
        while True:
            if backend_process.poll() is not None:
                print("Backend process stopped")
                break
            if frontend_process.poll() is not None:
                print("Frontend process stopped")
                break
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nShutting down...")
    finally:
        if backend_process:
            backend_process.terminate()
        if frontend_process:
            frontend_process.terminate()
        print("AMMA has been shut down")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
