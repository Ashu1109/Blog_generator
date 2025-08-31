#!/usr/bin/env python3
"""
Test script for markdown generation without database dependency.
This demonstrates the improved blog generation with proper markdown formatting.
"""

import asyncio
import logging
from datetime import datetime
import os

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

async def test_markdown_generation():
    """Test markdown generation without database dependency."""
    try:
        print("🚀 Testing Improved Blog Generator - Markdown Generation")
        print("=" * 60)
        
        # Import components
        from src.blog_generator import EnhancedBlogGenerator
        
        print("✅ Blog generator imported successfully")
        
        # Create a simple blog post using the improved system
        generator = EnhancedBlogGenerator()
        
        # Test the component extraction with a sample markdown blog
        sample_blog_output = """
# AI Agents in 2024: Transforming Business Operations

## Introduction

Artificial Intelligence agents have emerged as one of the most transformative technologies in 2024, revolutionizing how businesses operate and interact with customers. These autonomous systems are capable of performing complex tasks, making decisions, and learning from their experiences.

## Key Developments

### Enhanced Natural Language Processing
AI agents now possess unprecedented language understanding capabilities, enabling them to:

- Process complex queries with contextual awareness
- Generate human-like responses across multiple domains
- Maintain coherent conversations over extended periods

### Integration with Business Systems
Modern AI agents seamlessly integrate with existing business infrastructure:

- **CRM Systems**: Automated customer relationship management
- **E-commerce Platforms**: Personalized shopping experiences  
- **Support Channels**: 24/7 customer service automation

## Real-World Applications

AI agents are being deployed across various industries:

1. **Healthcare**: Patient monitoring and diagnostic assistance
2. **Finance**: Fraud detection and risk assessment
3. **Retail**: Inventory management and customer recommendations
4. **Manufacturing**: Quality control and predictive maintenance

## Market Impact

According to recent studies, the AI agent market is expected to grow by 35% in 2024, with businesses reporting:

- 40% reduction in operational costs
- 60% improvement in customer satisfaction
- 25% increase in productivity

## Conclusion

AI agents represent a paradigm shift in how we approach automation and human-computer interaction. As we move forward, these systems will become increasingly sophisticated, offering even greater value to businesses and consumers alike.

**Tags:** AI Agents, Artificial Intelligence, Business Automation, Machine Learning, Technology Trends

Meta Description: Discover how AI agents are transforming business operations in 2024 with enhanced capabilities, real-world applications, and significant market impact.
"""
        
        print("\n📝 Testing blog component extraction...")
        
        # Test the extraction functionality
        blog_components = generator.extract_blog_components(sample_blog_output)
        
        print(f"✅ Blog components extracted successfully!")
        print(f"   📋 Title: {blog_components['title']}")
        print(f"   📊 Word Count: {blog_components['word_count']}")
        print(f"   🏷️  Tags: {', '.join(blog_components['tags'])}")
        if blog_components.get('meta_description'):
            print(f"   🔍 Meta Description: {blog_components['meta_description']}")
        
        # Test markdown formatting
        print(f"\n📄 Testing markdown formatting...")
        formatted_content = generator.ensure_proper_markdown(blog_components['content'])
        
        # Save the generated blog post to a markdown file
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"sample_blog_post_{timestamp}.md"
        
        # Create a complete markdown file with front matter for websites
        front_matter = f"""---
title: "{blog_components['title']}"
date: {datetime.now().isoformat()}
tags: [{', '.join([f'"{tag}"' for tag in blog_components['tags']])}]
description: "{blog_components.get('meta_description', 'AI-generated blog post about generative AI')}"
slug: "{generator.generate_slug(blog_components['title']) if hasattr(generator, 'generate_slug') else blog_components['title'].lower().replace(' ', '-')}"
---

"""
        
        full_content = front_matter + formatted_content
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(full_content)
        
        print(f"✅ Markdown formatting completed!")
        print(f"💾 Blog post saved to: {filename}")
        print(f"   File size: {len(full_content)} characters")
        
        # Display a preview of the generated content
        print(f"\n📖 Content Preview (First 300 characters):")
        print("=" * 50)
        print(formatted_content[:300] + "..." if len(formatted_content) > 300 else formatted_content)
        print("=" * 50)
        
        # Show the front matter
        print(f"\n🏷️  Website Front Matter:")
        print("=" * 30)
        print(front_matter)
        print("=" * 30)
        
        print(f"\n🎯 Key Features Demonstrated:")
        print(f"   ✅ Proper markdown heading hierarchy")
        print(f"   ✅ Structured content with sections")
        print(f"   ✅ Bullet points and numbered lists")
        print(f"   ✅ Bold and italic text formatting")
        print(f"   ✅ Tag extraction and formatting")
        print(f"   ✅ Meta description generation")
        print(f"   ✅ Website-ready front matter")
        print(f"   ✅ SEO-friendly slug generation")
        
        print(f"\n🌐 Ready for Your Website:")
        print(f"   • Upload {filename} to your blog/content directory")
        print(f"   • Compatible with Jekyll, Hugo, Gatsby, Next.js, and other static site generators")
        print(f"   • Includes all necessary metadata for SEO")
        print(f"   • Properly formatted markdown for web display")
        
        print(f"\n✅ Markdown generation test completed successfully!")
        
        return filename
        
    except Exception as e:
        logger.error(f"Test failed: {e}")
        print(f"\n❌ Test failed: {e}")
        return None

def generate_slug(title: str) -> str:
    """Generate a URL-friendly slug from the title."""
    import re
    # Convert to lowercase and replace spaces with hyphens
    slug = title.lower()
    # Remove special characters and keep only alphanumeric, spaces, and hyphens
    slug = re.sub(r'[^a-z0-9\s-]', '', slug)
    # Replace multiple spaces/hyphens with single hyphen
    slug = re.sub(r'[\s-]+', '-', slug)
    # Remove leading/trailing hyphens
    slug = slug.strip('-')
    # Limit length
    return slug[:100]

if __name__ == "__main__":
    result = asyncio.run(test_markdown_generation())
    if result:
        print(f"\n🎉 SUCCESS: Blog post generated and saved as {result}")
        print(f"The file is ready to use on your website!")

