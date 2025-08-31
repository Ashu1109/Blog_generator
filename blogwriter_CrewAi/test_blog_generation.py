#!/usr/bin/env python3
"""
Test script for the improved blog generation system.
This will generate a blog post and save it in proper markdown format.
"""

import asyncio
import logging
from datetime import datetime

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

async def test_improved_blog_generation():
    """Test the improved blog generation with markdown formatting."""
    try:
        print("🚀 Testing Improved AI Blog Generator")
        print("=" * 50)
        
        # Import components
        from src.blog_generator import blog_generator
        from src.database.connection import db_manager
        
        print("✅ Components imported successfully")
        
        # Test database connection
        await db_manager.connect()
        print("✅ Database connected")
        
        # Generate a blog post with a focused topic
        print("\n📝 Generating blog post...")
        print("Topic: AI Agents in 2024 - practical applications")
        print("This should take 1-3 minutes...")
        
        result = await blog_generator.generate_blog_post(
            custom_topic="AI Agents in 2024 - practical applications and real-world use cases"
        )
        
        if result:
            print(f"\n🎉 Blog post generated successfully!")
            print(f"   📋 Title: {result['title']}")
            print(f"   📊 Word Count: {result['word_count']}")
            print(f"   🏷️  Tags: {', '.join(result['tags'])}")
            print(f"   🆔 Database ID: {result['id']}")
            print(f"   📅 Created: {result['created_at']}")
            
            # Get the full blog post from database to show markdown
            blog_post = await db_manager.db.blogpost.find_unique(where={"id": result['id']})
            
            if blog_post:
                print(f"\n📄 Blog Post Content (Markdown Format):")
                print("=" * 60)
                print(blog_post.content[:500] + "..." if len(blog_post.content) > 500 else blog_post.content)
                print("=" * 60)
                
                if blog_post.metaDescription:
                    print(f"\n🔍 Meta Description: {blog_post.metaDescription}")
                
                if blog_post.slug:
                    print(f"🔗 Slug: {blog_post.slug}")
                
                # Save to a markdown file for your website
                filename = f"blog_post_{blog_post.id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(blog_post.content)
                
                print(f"\n💾 Blog post saved to: {filename}")
                print("   This file is ready to use on your website!")
        else:
            print("❌ Blog generation failed")
        
        # Show recent posts
        print(f"\n📚 Recent blog posts in database:")
        recent_posts = await db_manager.get_recent_blog_posts(limit=3)
        
        for i, post in enumerate(recent_posts, 1):
            print(f"   {i}. {post.title}")
            print(f"      Created: {post.createdAt.strftime('%Y-%m-%d %H:%M:%S')}")
            print(f"      Words: {post.wordCount}, Tags: {len(post.tags)}")
            if post.metaDescription:
                print(f"      Meta: {post.metaDescription[:50]}...")
            print()
        
        # Show generation stats
        stats = await db_manager.get_generation_stats(hours=24)
        if stats:
            print(f"📊 Generation Statistics (Last 24 Hours):")
            print(f"   Total attempts: {stats.get('total_attempts', 0)}")
            print(f"   Successful: {stats.get('successful_attempts', 0)}")
            print(f"   Failed: {stats.get('failed_attempts', 0)}")
            print(f"   Success rate: {stats.get('success_rate', 0):.1f}%")
        
        await db_manager.disconnect()
        print("\n✅ Test completed successfully!")
        
    except Exception as e:
        logger.error(f"Test failed: {e}")
        print(f"\n❌ Test failed: {e}")

if __name__ == "__main__":
    asyncio.run(test_improved_blog_generation())
