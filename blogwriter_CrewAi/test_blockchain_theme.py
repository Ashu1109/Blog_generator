#!/usr/bin/env python3
"""
Test script to demonstrate blockchain theme functionality.
This script tests the new blockchain theme feature without requiring full setup.
"""

import asyncio
import logging
from datetime import datetime

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

async def test_theme_functionality():
    """Test the theme selection functionality."""
    try:
        print("🧪 Testing Blockchain Theme Functionality")
        print("=" * 50)
        
        # Import the blog generator
        try:
            from src.blog_generator import blog_generator
            print("✅ Blog generator imported successfully")
        except ImportError as e:
            print(f"❌ Import error: {e}")
            print("Please install dependencies: pip install -r requirements.txt")
            return
        
        # Test topic generation with different themes
        print("\n📝 Testing Topic Generation:")
        print("-" * 30)
        
        # Generate GenAI topics
        print("\n🤖 GenAI Topics:")
        for i in range(3):
            topic = blog_generator.generate_dynamic_topic(theme="genai")
            print(f"  {i+1}. {topic}")
        
        # Generate Blockchain topics
        print("\n⛓️  Blockchain Topics:")
        for i in range(3):
            topic = blog_generator.generate_dynamic_topic(theme="blockchain")
            print(f"  {i+1}. {topic}")
        
        # Generate Random topics (mixed themes)
        print("\n🎲 Random Theme Topics:")
        for i in range(5):
            topic = blog_generator.generate_dynamic_topic()  # No theme specified = random
            print(f"  {i+1}. {topic}")
        
        # Test the topic lists
        print(f"\n📊 Topic Statistics:")
        print(f"  • GenAI topics available: {len(blog_generator.GENERATIVE_AI_TOPICS)}")
        print(f"  • Blockchain topics available: {len(blog_generator.BLOCKCHAIN_TOPICS)}")
        print(f"  • Total topics: {len(blog_generator.GENERATIVE_AI_TOPICS) + len(blog_generator.BLOCKCHAIN_TOPICS)}")
        
        print("\n✅ Theme functionality test completed!")
        
    except Exception as e:
        logger.error(f"Test failed: {e}")
        print(f"\n❌ Test failed: {e}")

def show_api_examples():
    """Show API usage examples for the new theme functionality."""
    print("\n🌐 API Usage Examples with Themes")
    print("-" * 40)
    
    examples = [
        ("Generate Random Theme", 'curl -X POST "http://localhost:8000/generate" -H "Content-Type: application/json" -d \'{}\''),
        ("Generate GenAI Theme", 'curl -X POST "http://localhost:8000/generate" -H "Content-Type: application/json" -d \'{"theme": "genai"}\''),
        ("Generate Blockchain Theme", 'curl -X POST "http://localhost:8000/generate" -H "Content-Type: application/json" -d \'{"theme": "blockchain"}\''),
        ("Custom Topic + Theme", 'curl -X POST "http://localhost:8000/generate" -H "Content-Type: application/json" -d \'{"topic": "DeFi innovations", "theme": "blockchain"}\''),
    ]
    
    for name, example in examples:
        print(f"\n{name}:")
        print(f"  {example}")

async def main():
    """Main test function."""
    print("🚀 Blockchain Theme Test Suite")
    print("=" * 60)
    
    await test_theme_functionality()
    show_api_examples()
    
    print("\n📖 Next Steps:")
    print("1. The system now randomly selects between GenAI and Blockchain themes")
    print("2. You can specify a theme in API calls or let it choose randomly")
    print("3. All agents are updated to handle both AI and blockchain content")
    print("4. Run the main application to test full blog generation")

if __name__ == "__main__":
    asyncio.run(main())
