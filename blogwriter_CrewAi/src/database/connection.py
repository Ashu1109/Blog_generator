"""Database connection and operations module using Prisma."""

import asyncio
import logging
from typing import Optional, List, Dict, Any
from datetime import datetime

from prisma import Prisma
from prisma.models import BlogPost, GenerationLog

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DatabaseManager:
    """Manages database connections and operations."""
    
    def __init__(self):
        self.db = Prisma()
        self._connected = False
    
    def generate_slug(self, title: str) -> str:
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
    
    async def connect(self):
        """Connect to the database."""
        if not self._connected:
            try:
                await self.db.connect()
                self._connected = True
                logger.info("Connected to database successfully")
            except Exception as e:
                logger.error(f"Failed to connect to database: {e}")
                raise
    
    async def disconnect(self):
        """Disconnect from the database."""
        if self._connected:
            try:
                await self.db.disconnect()
                self._connected = False
                logger.info("Disconnected from database")
            except Exception as e:
                logger.error(f"Error disconnecting from database: {e}")
    
    async def create_blog_post(
        self,
        title: str,
        content: str,
        topic: str,
        tags: List[str] = None,
        word_count: Optional[int] = None,
        meta_description: Optional[str] = None,
        slug: Optional[str] = None
    ) -> Optional[BlogPost]:
        """Create a new blog post in the database."""
        try:
            if not self._connected:
                await self.connect()
            
            # Generate slug if not provided
            if not slug:
                slug = self.generate_slug(title)
            
            blog_post = await self.db.blogpost.create(
                data={
                    'title': title,
                    'content': content,
                    'topic': topic,
                    'tags': tags or [],
                    'wordCount': word_count,
                    'metaDescription': meta_description,
                    'slug': slug,
                    'published': True
                }
            )
            
            logger.info(f"Created blog post: {blog_post.title} (ID: {blog_post.id})")
            return blog_post
            
        except Exception as e:
            logger.error(f"Error creating blog post: {e}")
            return None
    
    async def get_recent_blog_posts(self, limit: int = 10) -> List[BlogPost]:
        """Get recent blog posts."""
        try:
            if not self._connected:
                await self.connect()
            
            posts = await self.db.blogpost.find_many(
                order={'createdAt': 'desc'},
                take=limit
            )
            
            return posts
            
        except Exception as e:
            logger.error(f"Error fetching recent blog posts: {e}")
            return []
    
    async def get_blog_posts_by_topic(self, topic: str, limit: int = 5) -> List[BlogPost]:
        """Get blog posts by topic."""
        try:
            if not self._connected:
                await self.connect()
            
            posts = await self.db.blogpost.find_many(
                where={'topic': {'contains': topic, 'mode': 'insensitive'}},
                order={'createdAt': 'desc'},
                take=limit
            )
            
            return posts
            
        except Exception as e:
            logger.error(f"Error fetching blog posts by topic: {e}")
            return []
    
    async def log_generation_attempt(
        self,
        topic: str,
        status: str,
        error_msg: Optional[str] = None,
        blog_post_id: Optional[int] = None
    ) -> Optional[GenerationLog]:
        """Log a blog generation attempt."""
        try:
            if not self._connected:
                await self.connect()
            
            log_entry = await self.db.generationlog.create(
                data={
                    'topic': topic,
                    'status': status,
                    'errorMsg': error_msg,
                    'blogPostId': blog_post_id
                }
            )
            
            logger.info(f"Logged generation attempt: {topic} - {status}")
            return log_entry
            
        except Exception as e:
            logger.error(f"Error logging generation attempt: {e}")
            return None
    
    async def get_generation_stats(self, hours: int = 24) -> Dict[str, Any]:
        """Get generation statistics for the last N hours."""
        try:
            if not self._connected:
                await self.connect()
            
            # Calculate the datetime threshold
            from datetime import datetime, timedelta
            threshold = datetime.now() - timedelta(hours=hours)
            
            # Get total attempts
            total_attempts = await self.db.generationlog.count(
                where={'createdAt': {'gte': threshold}}
            )
            
            # Get successful attempts
            successful_attempts = await self.db.generationlog.count(
                where={
                    'createdAt': {'gte': threshold},
                    'status': 'success'
                }
            )
            
            # Get failed attempts
            failed_attempts = await self.db.generationlog.count(
                where={
                    'createdAt': {'gte': threshold},
                    'status': 'failed'
                }
            )
            
            # Get total blog posts created
            total_posts = await self.db.blogpost.count(
                where={'createdAt': {'gte': threshold}}
            )
            
            return {
                'total_attempts': total_attempts,
                'successful_attempts': successful_attempts,
                'failed_attempts': failed_attempts,
                'total_posts': total_posts,
                'success_rate': (successful_attempts / total_attempts * 100) if total_attempts > 0 else 0,
                'period_hours': hours
            }
            
        except Exception as e:
            logger.error(f"Error getting generation stats: {e}")
            return {}

# Global database manager instance
db_manager = DatabaseManager()

# Convenience functions
async def save_blog_post(title: str, content: str, topic: str, tags: List[str] = None, word_count: Optional[int] = None, meta_description: Optional[str] = None, slug: Optional[str] = None) -> Optional[BlogPost]:
    """Convenience function to save a blog post."""
    return await db_manager.create_blog_post(title, content, topic, tags, word_count, meta_description, slug)

async def log_generation(topic: str, status: str, error_msg: Optional[str] = None, blog_post_id: Optional[int] = None) -> Optional[GenerationLog]:
    """Convenience function to log generation attempt."""
    return await db_manager.log_generation_attempt(topic, status, error_msg, blog_post_id)
