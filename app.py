#!/usr/bin/env python3
"""
Deployment Entry Point for Synthetic Ascension EHR Platform
This file serves as a bridge for deployment systems expecting a Python entry point.
The actual application is a React frontend with FastAPI backends.

NOTE: This is NOT a Streamlit application - it's a React app!
The .replit file incorrectly references Streamlit, but this script handles the proper deployment.
"""

import os
import sys
import subprocess
import time
import signal
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor

class ReactDeploymentServer:
    """Deployment server that properly handles React app deployment"""
    
    def __init__(self):
        self.port = int(os.getenv('PORT', 5000))
        self.is_production = os.getenv('REPLIT_DEPLOYMENT', 'false').lower() == 'true'
        self.processes = []
        
    def cleanup(self, signum=None, frame=None):
        """Clean up running processes"""
        print("\n🛑 Shutting down services...")
        for process in self.processes:
            if process and process.poll() is None:
                process.terminate()
        sys.exit(0)
        
    def build_react_app(self):
        """Build the React application for production"""
        print("📦 Building React application...")
        try:
            result = subprocess.run(['npm', 'run', 'build'], 
                                  check=True, 
                                  capture_output=True, 
                                  text=True)
            print("✅ React build completed successfully")
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ Build failed: {e}")
            print(f"Build output: {e.stdout}")
            print(f"Build errors: {e.stderr}")
            return False
            
    def serve_production(self):
        """Serve the built React application in production"""
        print(f"🌐 Starting production server on port {self.port}")
        
        # Try multiple serving methods
        serve_methods = [
            ['npx', 'serve', '-s', 'dist', '-l', str(self.port)],
            ['python', '-m', 'http.server', str(self.port), '--directory', 'dist'],
            ['npx', 'vite', 'preview', '--host', '0.0.0.0', '--port', str(self.port)]
        ]
        
        for method in serve_methods:
            try:
                print(f"🔄 Trying: {' '.join(method)}")
                process = subprocess.Popen(method)
                self.processes.append(process)
                
                # Wait a bit to see if it starts successfully
                time.sleep(3)
                if process.poll() is None:
                    print(f"✅ Production server started successfully")
                    return process
                else:
                    print(f"❌ Method failed, trying next...")
                    
            except Exception as e:
                print(f"❌ Failed to start with {method[0]}: {e}")
                continue
                
        return None
        
    def serve_development(self):
        """Serve the React application in development mode"""
        print(f"🛠️  Starting development server on port {self.port}")
        try:
            process = subprocess.Popen([
                'npx', 'vite', '--host', '0.0.0.0', '--port', str(self.port)
            ])
            self.processes.append(process)
            return process
        except Exception as e:
            print(f"❌ Failed to start development server: {e}")
            return None
            
    def start_backend_services(self):
        """Start backend services in parallel"""
        backend_services = [
            {
                'name': 'Enhanced Backend V3',
                'command': ['python', 'integrated_server_v3_enhanced.py'],
                'port': 8004
            },
            {
                'name': 'Legacy Backend',
                'command': ['python', 'integrated_server_v2.py'],
                'port': 8003
            }
        ]
        
        for service in backend_services:
            try:
                print(f"🚀 Starting {service['name']} on port {service['port']}")
                process = subprocess.Popen(
                    service['command'],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE
                )
                self.processes.append(process)
            except Exception as e:
                print(f"⚠️  Failed to start {service['name']}: {e}")
                
    def run(self):
        """Main run method"""
        # Set up signal handlers for clean shutdown
        signal.signal(signal.SIGINT, self.cleanup)
        signal.signal(signal.SIGTERM, self.cleanup)
        
        print("🚀 Starting Synthetic Ascension EHR Platform...")
        print("📊 Architecture: React Frontend + FastAPI Backends")
        print(f"🔧 Mode: {'Production' if self.is_production else 'Development'}")
        print(f"🔌 Port: {self.port}")
        
        try:
            if self.is_production:
                # Production deployment
                if self.build_react_app():
                    frontend_process = self.serve_production()
                    if not frontend_process:
                        print("🔄 Production build failed, falling back to development...")
                        frontend_process = self.serve_development()
                else:
                    print("🔄 Build failed, starting development server...")
                    frontend_process = self.serve_development()
            else:
                # Development mode
                frontend_process = self.serve_development()
                
            if not frontend_process:
                print("❌ Failed to start frontend server")
                sys.exit(1)
                
            print(f"✅ Frontend server running on http://0.0.0.0:{self.port}")
            
            # Start backend services
            self.start_backend_services()
            
            # Keep the main process alive
            print("🌟 All services started. Press Ctrl+C to stop.")
            try:
                frontend_process.wait()
            except KeyboardInterrupt:
                self.cleanup()
                
        except Exception as e:
            print(f"💥 Unexpected error: {e}")
            self.cleanup()
            sys.exit(1)

def main():
    """Main entry point - this is what gets called by the deployment system"""
    server = ReactDeploymentServer()
    server.run()

if __name__ == "__main__":
    main()