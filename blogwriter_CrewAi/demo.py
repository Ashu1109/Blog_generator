#!/usr/bin/env python3
"""
Demo script to test the AI Blog Generator functionality.
This script demonstrates the core features without requiring the full setup.
"""

import asyncio
import logging
from datetime import datetime

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

async def demo_blog_generation():
    """Demo the blog generation functionality."""
    try:
        print("🤖 AI Blog Generator Demo")
        print("=" * 50)
        
        # Import components (this will fail if dependencies aren't installed)
        try:
            from src.blog_generator import blog_generator
            from src.database.connection import db_manager
            print("✅ All components imported successfully")
        except ImportError as e:
            print(f"❌ Import error: {e}")
            print("Please install dependencies: pip install -r requirements.txt")
            return
        
        # Test database connection
        print("\n🗄️  Testing database connection...")
        try:
            await db_manager.connect()
            print("✅ Database connected successfully")
        except Exception as e:
            print(f"❌ Database connection failed: {e}")
            print("Please check your DATABASE_URL in .env file")
            return
        
        # Generate a test blog post
        print("\n📝 Generating test blog post...")
        print("This may take 2-5 minutes depending on AI response times...")
        
        # Test both themes
        print("Testing GenAI theme...")
        genai_result = await blog_generator.generate_blog_post(
            custom_topic="Latest developments in Large Language Models and their applications in 2024",
            theme="genai"
        )
        
        print("Testing Blockchain theme...")
        blockchain_result = await blog_generator.generate_blog_post(
            custom_topic="DeFi protocols and decentralized finance innovations in 2024", 
            theme="blockchain"
        )
        
        print("Testing Random theme selection...")
        random_result = await blog_generator.generate_blog_post()  # Random theme
        
        # Show results for all tests
        results = [
            ("GenAI", genai_result),
            ("Blockchain", blockchain_result), 
            ("Random", random_result)
        ]
        
        for theme_name, result in results:
            if result:
                print(f"\n🎉 {theme_name} blog post generated successfully!")
                print(f"   Title: {result['title']}")
                print(f"   Topic: {result['topic']}")
                print(f"   Word Count: {result['word_count']}")
                print(f"   Tags: {', '.join(result['tags'])}")
                print(f"   Database ID: {result['id']}")
            else:
                print(f"❌ {theme_name} blog generation failed")
        

        
        # Show recent posts
        print("\n📚 Recent blog posts:")
        recent_posts = await db_manager.get_recent_blog_posts(limit=5)
        
        if recent_posts:
            for i, post in enumerate(recent_posts, 1):
                print(f"   {i}. {post.title[:60]}...")
                print(f"      Created: {post.createdAt}, Words: {post.wordCount}")
        else:
            print("   No posts found in database")
        
        # Show generation stats
        print("\n📊 Generation statistics:")
        stats = await db_manager.get_generation_stats(hours=24)
        if stats:
            print(f"   Total attempts (24h): {stats.get('total_attempts', 0)}")
            print(f"   Successful: {stats.get('successful_attempts', 0)}")
            print(f"   Failed: {stats.get('failed_attempts', 0)}")
            print(f"   Success rate: {stats.get('success_rate', 0):.1f}%")
        
        # Cleanup
        await db_manager.disconnect()
        print("\n✅ Demo completed successfully!")
        
    except Exception as e:
        logger.error(f"Demo failed: {e}")
        print(f"\n❌ Demo failed: {e}")

async def demo_scheduler():
    """Demo the scheduler functionality (without actually starting it)."""
    try:
        print("\n⏰ Scheduler Demo")
        print("-" * 30)
        
        from src.scheduler import blog_scheduler
        
        print("Scheduler features:")
        print("  • Automatic blog generation every 10 minutes (configurable)")
        print("  • Random theme selection (GenAI or Blockchain)")
        print("  • Statistics reporting every hour")
        print("  • Daily cleanup jobs")
        print("  • Manual trigger capability")
        print("  • Graceful shutdown handling")
        
        print(f"\nScheduler status: {'Running' if blog_scheduler.is_running() else 'Stopped'}")
        
        jobs = blog_scheduler.get_job_info()
        if jobs:
            print("Scheduled jobs:")
            for job in jobs:
                print(f"  • {job['name']}: {job['trigger']}")
        
    except Exception as e:
        print(f"Scheduler demo error: {e}")

def show_api_examples():
    """Show API usage examples."""
    print("\n🌐 API Usage Examples")
    print("-" * 30)
    
    examples = [
        ("Health Check", "GET /health", "curl http://localhost:8000/health"),
        ("Generate Random Theme", "POST /generate", 'curl -X POST "http://localhost:8000/generate" -H "Content-Type: application/json" -d \'{}\''),
        ("Generate GenAI Blog", "POST /generate", 'curl -X POST "http://localhost:8000/generate" -H "Content-Type: application/json" -d \'{"theme": "genai"}\''),
        ("Generate Blockchain Blog", "POST /generate", 'curl -X POST "http://localhost:8000/generate" -H "Content-Type: application/json" -d \'{"theme": "blockchain"}\''),
        ("Custom Topic + Theme", "POST /generate", 'curl -X POST "http://localhost:8000/generate" -H "Content-Type: application/json" -d \'{"topic": "DeFi innovations", "theme": "blockchain"}\''),
        ("Get Recent Posts", "GET /posts", "curl http://localhost:8000/posts?limit=5"),
        ("Get Statistics", "GET /stats", "curl http://localhost:8000/stats?hours=24"),
        ("Start Scheduler", "POST /scheduler/start", 'curl -X POST "http://localhost:8000/scheduler/start" -H "Content-Type: application/json" -d \'{"interval_minutes": 10}\''),
    ]
    
    for name, endpoint, example in examples:
        print(f"\n{name}:")
        print(f"  Endpoint: {endpoint}")
        print(f"  Example: {example}")

async def main():
    """Main demo function."""
    print("🚀 AI Blog Generator - Comprehensive Demo")
    print("=" * 60)
    
    # Check if this is a full demo or just info
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "--full":
        print("Running full demo (requires database and API keys)...")
        await demo_blog_generation()
        await demo_scheduler()
    else:
        print("Running info demo (no database required)")
        print("Use --full flag for complete demo with database")
        
        await demo_scheduler()
    
    show_api_examples()
    
    print("\n📖 Next Steps:")
    print("1. Copy env.example to .env and configure your settings")
    print("2. Run: python start.py (for setup)")
    print("3. Run: python main.py (to start the application)")
    print("4. Visit: http://localhost:8000/docs (for API documentation)")
    print("\nFor more details, see: setup_instructions.md")

if __name__ == "__main__":
    asyncio.run(main())
