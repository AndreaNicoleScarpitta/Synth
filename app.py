#!/usr/bin/env python3
"""
Deployment Entry Point for Synthetic Ascension EHR Platform
This file serves as a bridge for deployment systems expecting a Python entry point.
The actual application is a React frontend with FastAPI backends.
"""

import os
import sys
import subprocess
import time
from pathlib import Path

def main():
    """
    Main deployment function that starts the appropriate services
    """
    print("🚀 Starting Synthetic Ascension EHR Platform...")
    print("📊 Architecture: React Frontend + FastAPI Backends")
    
    # Check if we're in deployment mode
    is_production = os.getenv('REPLIT_DEPLOYMENT', False)
    port = int(os.getenv('PORT', 5000))
    
    if is_production:
        print(f"🌐 Production mode - Starting React frontend on port {port}")
        # In production, serve the built React application
        try:
            # Try to build the frontend first
            print("📦 Building React application...")
            subprocess.run(['npm', 'run', 'build'], check=True, cwd='.')
            
            # Serve using a simple HTTP server
            print(f"🌟 Serving application on port {port}")
            subprocess.run([
                'npx', 'serve', '-s', 'dist', '-l', str(port)
            ], check=True)
            
        except subprocess.CalledProcessError as e:
            print(f"❌ Build failed: {e}")
            # Fallback to development server
            print("🔄 Falling back to development server...")
            subprocess.run([
                'npx', 'vite', '--host', '0.0.0.0', '--port', str(port)
            ])
    else:
        print(f"🛠️  Development mode - Starting Vite dev server on port {port}")
        # In development, use Vite dev server
        try:
            subprocess.run([
                'npx', 'vite', '--host', '0.0.0.0', '--port', str(port)
            ], check=True)
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to start development server: {e}")
            sys.exit(1)

if __name__ == "__main__":
    main()