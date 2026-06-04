#!/usr/bin/env python3
"""
Deployment Verification Script
Checks if all required files and configurations are ready for deployment
"""

import os
import sys
from pathlib import Path

def check_file(filepath, required=True):
    """Check if a file exists"""
    exists = os.path.exists(filepath)
    status = "✅" if exists else ("❌" if required else "⚠️")
    req_text = "REQUIRED" if required else "OPTIONAL"
    print(f"{status} {filepath} [{req_text}]")
    return exists

def check_model():
    """Check if model file exists"""
    model_path = "runs/detect/train3/weights/best.pt"
    if os.path.exists(model_path):
        size_mb = os.path.getsize(model_path) / (1024 * 1024)
        print(f"✅ Model file: {model_path} ({size_mb:.2f} MB)")
        return True
    else:
        print(f"❌ Model file not found: {model_path}")
        print("   Please ensure your trained YOLO model is in the correct location")
        return False

def check_directories():
    """Check if required directories exist"""
    dirs = [
        ("static", True),
        ("static/uploads", True),
        ("static/results", True),
        ("templates", True),
        ("runs", True),
    ]
    
    all_exist = True
    for directory, required in dirs:
        exists = os.path.exists(directory) and os.path.isdir(directory)
        status = "✅" if exists else ("❌" if required else "⚠️")
        req_text = "REQUIRED" if required else "OPTIONAL"
        print(f"{status} Directory: {directory}/ [{req_text}]")
        if required and not exists:
            all_exist = False
    
    return all_exist

def check_python_version():
    """Check Python version"""
    version = sys.version_info
    if version.major == 3 and version.minor >= 9:
        print(f"✅ Python version: {version.major}.{version.minor}.{version.micro}")
        return True
    else:
        print(f"⚠️ Python version: {version.major}.{version.minor}.{version.micro}")
        print("   Recommended: Python 3.9 or higher")
        return False

def check_env_file():
    """Check if .env file exists and has required variables"""
    if not os.path.exists('.env'):
        print("⚠️ .env file not found")
        print("   Create one from .env.example: cp .env.example .env")
        return False
    
    print("✅ .env file exists")
    
    # Check for important variables
    with open('.env', 'r') as f:
        content = f.read()
        
    required_vars = ['SECRET_KEY', 'FLASK_ENV']
    missing = []
    
    for var in required_vars:
        if var not in content:
            missing.append(var)
    
    if missing:
        print(f"⚠️ Missing environment variables: {', '.join(missing)}")
        return False
    
    if 'your-secret-key-here' in content or 'change-in-production' in content:
        print("⚠️ WARNING: SECRET_KEY still has default value!")
        print("   Generate a new one: python -c \"import secrets; print(secrets.token_hex(32))\"")
        return False
    
    print("✅ Environment variables configured")
    return True

def main():
    """Run all deployment checks"""
    print("=" * 60)
    print("🔍 Car Damage Detection - Deployment Verification")
    print("=" * 60)
    print()
    
    checks = []
    
    # Python version
    print("📌 Python Version:")
    checks.append(check_python_version())
    print()
    
    # Core application files
    print("📌 Core Application Files:")
    checks.append(check_file("app.py", required=True))
    checks.append(check_file("cost_estimator.py", required=True))
    checks.append(check_file("wsgi.py", required=True))
    print()
    
    # Requirements files
    print("📌 Requirements Files:")
    checks.append(check_file("requirements.txt", required=True))
    checks.append(check_file("requirements-prod.txt", required=True))
    print()
    
    # Deployment files
    print("📌 Deployment Configuration Files:")
    check_file("Dockerfile", required=False)
    check_file("docker-compose.yml", required=False)
    check_file("Procfile", required=False)
    check_file("nginx.conf", required=False)
    check_file(".gitignore", required=False)
    print()
    
    # Deployment scripts
    print("📌 Deployment Scripts:")
    check_file("deploy.sh", required=False)
    check_file("deploy.bat", required=False)
    print()
    
    # Documentation
    print("📌 Documentation:")
    check_file("DEPLOYMENT.md", required=False)
    check_file("README-DEPLOYMENT.md", required=False)
    print()
    
    # Directories
    print("📌 Required Directories:")
    checks.append(check_directories())
    print()
    
    # Model file
    print("📌 Model File:")
    checks.append(check_model())
    print()
    
    # Environment configuration
    print("📌 Environment Configuration:")
    checks.append(check_env_file())
    print()
    
    # Summary
    print("=" * 60)
    if all(checks):
        print("✅ ALL CRITICAL CHECKS PASSED!")
        print("🚀 Your application is ready for deployment!")
        print()
        print("Next steps:")
        print("1. Choose a deployment method (see DEPLOYMENT.md)")
        print("2. Run: docker-compose up -d  (for Docker)")
        print("   OR: ./deploy.sh  (for automated deployment)")
        print("   OR: gunicorn wsgi:app --bind 0.0.0.0:5000  (manual)")
    else:
        print("❌ SOME CHECKS FAILED")
        print("⚠️ Please fix the issues above before deploying")
        print()
        print("Common fixes:")
        print("- Create .env from .env.example")
        print("- Ensure model file exists")
        print("- Install required dependencies")
        sys.exit(1)
    
    print("=" * 60)

if __name__ == "__main__":
    main()
