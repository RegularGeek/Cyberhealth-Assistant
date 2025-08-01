#!/usr/bin/env python3
"""
CyberHealth Assistant Startup Script
Provides an easy way to launch the application with proper setup
"""

import os
import sys
import subprocess
from pathlib import Path

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        print(f"Current version: {sys.version}")
        return False
    print(f"✅ Python version: {sys.version}")
    return True

def check_dependencies():
    """Check if required dependencies are installed"""
    required_packages = [
        'streamlit',
        'requests',
        'pandas',
        'plotly',
        'reportlab',
        'python-dotenv'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
            print(f"✅ {package}")
        except ImportError:
            missing_packages.append(package)
            print(f"❌ {package} - missing")
    
    if missing_packages:
        print(f"\n⚠️  Missing packages: {', '.join(missing_packages)}")
        print("💡 Install missing dependencies with:")
        print("   pip install -r requirements.txt")
        return False
    
    return True

def check_environment():
    """Check environment setup"""
    print("\n🔧 Checking environment...")
    
    # Check if .env file exists
    env_file = Path('.env')
    if not env_file.exists():
        print("⚠️  .env file not found")
        print("💡 Copy .env.example to .env and configure your settings")
        print("   cp .env.example .env")
    else:
        print("✅ .env file found")
    
    # Check if database directory exists
    db_dir = Path('.')
    if not db_dir.exists():
        print("⚠️  Database directory not found")
    else:
        print("✅ Database directory ready")
    
    return True

def run_tests():
    """Run installation tests"""
    print("\n🧪 Running installation tests...")
    
    try:
        result = subprocess.run([sys.executable, 'test_installation.py'], 
                              capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ All tests passed")
            return True
        else:
            print("❌ Some tests failed")
            print(result.stdout)
            print(result.stderr)
            return False
            
    except FileNotFoundError:
        print("⚠️  test_installation.py not found, skipping tests")
        return True

def start_application():
    """Start the Streamlit application"""
    print("\n🚀 Starting CyberHealth Assistant...")
    print("📱 The application will open in your browser")
    print("🔗 URL: http://localhost:8501")
    print("\n💡 Press Ctrl+C to stop the application")
    print("=" * 50)
    
    try:
        # Start Streamlit
        subprocess.run([sys.executable, '-m', 'streamlit', 'run', 'main.py'])
    except KeyboardInterrupt:
        print("\n👋 CyberHealth Assistant stopped")
    except Exception as e:
        print(f"❌ Error starting application: {e}")

def main():
    """Main startup function"""
    print("🔐 CyberHealth Assistant - Startup")
    print("=" * 50)
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Check dependencies
    print("\n📦 Checking dependencies...")
    if not check_dependencies():
        print("\n❌ Please install missing dependencies and try again")
        sys.exit(1)
    
    # Check environment
    if not check_environment():
        print("\n⚠️  Environment issues detected, but continuing...")
    
    # Run tests (optional)
    if os.path.exists('test_installation.py'):
        if not run_tests():
            print("\n⚠️  Tests failed, but continuing...")
    else:
        print("\n⚠️  test_installation.py not found, skipping tests")
    
    # Start application
    start_application()

if __name__ == "__main__":
    main()