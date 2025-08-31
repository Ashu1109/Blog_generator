#!/usr/bin/env python3
"""
Simple startup script for the AI Blog Generator.
This script helps you get started quickly with the right configuration.
"""

import os
import sys
import asyncio
import subprocess
from pathlib import Path

def check_requirements():
    """Check if all requirements are met."""
    print("🔍 Checking requirements...")
    
    # Check Python version
    if sys.version_info < (3, 9):
        print("❌ Python 3.9+ is required")
        return False
    
    # Check if .env file exists
    if not Path('.env').exists():
        print("⚠️  .env file not found. Please copy env.example to .env and configure it.")
        if Path('env.example').exists():
            print("   You can run: cp env.example .env")
        return False
    
    # Check if prisma is installed
    try:
        subprocess.run(['prisma', '--version'], capture_output=True, check=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("⚠️  Prisma CLI not found. Installing...")
        try:
            subprocess.run([sys.executable, '-m', 'pip', 'install', 'prisma'], check=True)
            print("✅ Prisma installed successfully")
        except subprocess.CalledProcessError:
            print("❌ Failed to install Prisma")
            return False
    
    print("✅ All requirements met!")
    return True

def setup_database():
    """Setup database schema."""
    print("🗄️  Setting up database...")
    
    try:
        # Generate Prisma client
        print("   Generating Prisma client...")
        subprocess.run(['prisma', 'generate'], check=True)
        
        # Push schema to database
        print("   Pushing schema to database...")
        subprocess.run(['prisma', 'db', 'push'], check=True)
        
        print("✅ Database setup completed!")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Database setup failed: {e}")
        print("   Please check your DATABASE_URL in .env file")
        return False

def main():
    """Main startup function."""
    print("🚀 AI Blog Generator Startup Script")
    print("=" * 50)
    
    # Check requirements
    if not check_requirements():
        print("\n❌ Setup failed. Please fix the issues above and try again.")
        sys.exit(1)
    
    # Setup database
    if not setup_database():
        print("\n❌ Database setup failed. Please check your configuration.")
        sys.exit(1)
    
    print("\n🎉 Setup completed successfully!")
    print("\nYou can now run the application with:")
    print("   python main.py                    # FastAPI server mode")
    print("   RUN_MODE=standalone python main.py  # Standalone mode")
    print("\nOr visit the API documentation at: http://localhost:8000/docs")

if __name__ == "__main__":
    main()
