#!/usr/bin/env python3
"""
Database connection checker for the AI Blog Generator.
This script helps diagnose database connectivity issues.
"""

import asyncio
import os
import sys
from dotenv import load_dotenv

# Add src to path
sys.path.insert(0, './src')

# Load environment variables
load_dotenv()

from src.database.connection import db_manager

async def check_database():
    """Check database connection and configuration."""
    print("🔍 AI Blog Generator - Database Connection Checker")
    print("=" * 60)
    
    # Check environment variables
    database_url = os.getenv('DATABASE_URL')
    if not database_url:
        print("❌ DATABASE_URL environment variable not found!")
        print("   Please check your .env file.")
        return False
    
    print(f"📋 Database URL: {database_url[:50]}...")
    
    # Test database connection
    try:
        print("\n🔗 Testing database connection...")
        await db_manager.connect(retries=1)
        
        print("✅ Database connection successful!")
        
        # Test health check
        print("🏥 Testing database health check...")
        healthy = await db_manager.health_check()
        
        if healthy:
            print("✅ Database health check passed!")
        else:
            print("❌ Database health check failed!")
            return False
        
        # Test basic operations
        print("🧪 Testing basic database operations...")
        
        # Try to count blog posts
        posts = await db_manager.get_recent_blog_posts(limit=1)
        print(f"📊 Found {len(posts)} recent blog posts")
        
        # Try to get stats
        stats = await db_manager.get_generation_stats(hours=24)
        print(f"📈 Generation stats: {stats.get('total_attempts', 0)} attempts in last 24h")
        
        print("\n🎉 All database tests passed!")
        return True
        
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        print("\n🔧 Troubleshooting tips:")
        print("1. Check if PostgreSQL is running")
        print("2. Verify DATABASE_URL in .env file")
        print("3. Ensure database exists and schema is applied")
        print("4. Run: prisma db push")
        print("5. Check network connectivity if using remote database")
        return False
        
    finally:
        if db_manager._connected:
            await db_manager.disconnect()
            print("🔌 Database connection closed")

async def main():
    """Main function."""
    try:
        success = await check_database()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n⏹️  Check cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())
