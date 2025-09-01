"""Blog generation scheduler using APScheduler."""

import asyncio
import logging
from datetime import datetime
from typing import Optional

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger
from apscheduler.triggers.cron import CronTrigger
from apscheduler.executors.asyncio import AsyncIOExecutor

from .blog_generator import blog_generator
from .database.connection import db_manager

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class BlogScheduler:
    """Manages scheduled blog generation tasks."""
    
    def __init__(self):
        # Configure scheduler with asyncio executor
        executors = {
            'default': AsyncIOExecutor(),
        }
        
        job_defaults = {
            'coalesce': False,
            'max_instances': 1,  # Prevent overlapping jobs
            'misfire_grace_time': 300  # 5 minutes grace time
        }
        
        self.scheduler = AsyncIOScheduler(
            executors=executors,
            job_defaults=job_defaults,
            timezone='UTC'
        )
        
        self._running = False
    
    async def generate_blog_job(self):
        """Job function to generate a blog post."""
        try:
            logger.info("Starting scheduled blog generation...")
            
            # Ensure database connection
            await db_manager.connect()
            
            # Generate blog post
            result = await blog_generator.generate_blog_post()
            
            if result:
                logger.info(f"Successfully generated blog post: {result['title']}")
                logger.info(f"Blog ID: {result['id']}, Word count: {result['word_count']}")
            else:
                logger.warning("Blog generation returned no result")
                
        except Exception as e:
            logger.error(f"Error in scheduled blog generation: {e}")
    
    async def generate_stats_job(self):
        """Job function to log generation statistics."""
        try:
            await db_manager.connect()
            stats = await db_manager.get_generation_stats(hours=24)
            
            if stats:
                logger.info("=== Blog Generation Stats (Last 24 Hours) ===")
                logger.info(f"Total attempts: {stats.get('total_attempts', 0)}")
                logger.info(f"Successful: {stats.get('successful_attempts', 0)}")
                logger.info(f"Failed: {stats.get('failed_attempts', 0)}")
                logger.info(f"Success rate: {stats.get('success_rate', 0):.1f}%")
                logger.info(f"Total posts created: {stats.get('total_posts', 0)}")
                
        except Exception as e:
            logger.error(f"Error getting generation stats: {e}")
    
    def start_scheduler(self, interval_minutes: int = 1440):  # Default to 1 day
        """Start the blog generation scheduler."""
        try:
            if self._running:
                logger.warning("Scheduler is already running")
                return
            
            # Add the main blog generation job (every N minutes)
            self.scheduler.add_job(
                self.generate_blog_job,
                trigger=IntervalTrigger(minutes=interval_minutes),
                id='blog_generation_job',
                name='Generate Blog Post',
                replace_existing=True
            )
            
            # Add a stats reporting job (every hour)
            self.scheduler.add_job(
                self.generate_stats_job,
                trigger=IntervalTrigger(hours=1),
                id='stats_reporting_job',
                name='Report Generation Stats',
                replace_existing=True
            )
            
            # Add a daily cleanup job (at 2 AM UTC)
            self.scheduler.add_job(
                self.cleanup_job,
                trigger=CronTrigger(hour=2, minute=0),
                id='daily_cleanup_job',
                name='Daily Cleanup',
                replace_existing=True
            )
            
            # Start the scheduler
            self.scheduler.start()
            self._running = True
            
            logger.info(f"Blog scheduler started successfully!")
            if interval_minutes >= 1440:
                hours = interval_minutes // 60
                logger.info(f"Blog generation interval: {hours} hours ({interval_minutes} minutes)")
            else:
                logger.info(f"Blog generation interval: {interval_minutes} minutes")
            logger.info("Next job times:")
            
            for job in self.scheduler.get_jobs():
                logger.info(f"  - {job.name}: {job.next_run_time}")
                
        except Exception as e:
            logger.error(f"Error starting scheduler: {e}")
            raise
    
    def stop_scheduler(self):
        """Stop the blog generation scheduler."""
        try:
            if not self._running:
                logger.warning("Scheduler is not running")
                return
            
            self.scheduler.shutdown(wait=True)
            self._running = False
            logger.info("Blog scheduler stopped successfully")
            
        except Exception as e:
            logger.error(f"Error stopping scheduler: {e}")
    
    async def cleanup_job(self):
        """Daily cleanup job to maintain database health."""
        try:
            logger.info("Running daily cleanup job...")
            await db_manager.connect()
            
            # Get cleanup stats
            stats = await db_manager.get_generation_stats(hours=24)
            logger.info(f"Cleaned up data. Stats: {stats}")
            
        except Exception as e:
            logger.error(f"Error in cleanup job: {e}")
    
    def is_running(self) -> bool:
        """Check if the scheduler is running."""
        return self._running
    
    def get_job_info(self) -> list:
        """Get information about scheduled jobs."""
        if not self._running:
            return []
        
        jobs_info = []
        for job in self.scheduler.get_jobs():
            jobs_info.append({
                'id': job.id,
                'name': job.name,
                'next_run_time': job.next_run_time,
                'trigger': str(job.trigger)
            })
        
        return jobs_info
    
    async def generate_now(self):
        """Trigger blog generation immediately (for testing/manual trigger)."""
        logger.info("Manually triggering blog generation...")
        await self.generate_blog_job()

# Global scheduler instance
blog_scheduler = BlogScheduler()

# Convenience functions
async def start_blog_scheduler(interval_minutes: int = 10):
    """Start the blog generation scheduler."""
    blog_scheduler.start_scheduler(interval_minutes)

def stop_blog_scheduler():
    """Stop the blog generation scheduler."""
    blog_scheduler.stop_scheduler()

async def trigger_blog_generation():
    """Manually trigger blog generation."""
    await blog_scheduler.generate_now()
