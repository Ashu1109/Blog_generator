"""
Main application for automated blog generation with scheduling.

This application automatically generates blog posts on the latest generative AI topics
every 10 minutes and saves them to a PostgreSQL database using Prisma.
"""

import asyncio
import logging
import signal
import sys
from contextlib import asynccontextmanager
from typing import Optional
from datetime import datetime

from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware

from src.scheduler import blog_scheduler, start_blog_scheduler, stop_blog_scheduler, trigger_blog_generation
from src.database.connection import db_manager
from src.blog_generator import blog_generator

# Load environment variables
load_dotenv()

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Global variables
scheduler_started = False

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Handle application startup and shutdown."""
    # Startup
    try:
        logger.info("Starting AI Blog Generator application...")
        
        # Connect to database
        await db_manager.connect()
        logger.info("Database connected successfully")
        
        # Start the scheduler
        global scheduler_started
        if not scheduler_started:
            blog_scheduler.start_scheduler(interval_minutes=10)
            scheduler_started = True
            logger.info("Blog scheduler started successfully")
        
        logger.info("Application startup completed!")
        
    except Exception as e:
        logger.error(f"Error during startup: {e}")
        raise
    
    yield
    
    # Shutdown
    try:
        logger.info("Shutting down AI Blog Generator application...")
        
        # Stop scheduler
        global scheduler_started
        if scheduler_started:
            blog_scheduler.stop_scheduler()
            scheduler_started = False
            logger.info("Scheduler stopped")
        
        # Disconnect from database
        await db_manager.disconnect()
        logger.info("Database disconnected")
        
        logger.info("Application shutdown completed")
        
    except Exception as e:
        logger.error(f"Error during shutdown: {e}")

# FastAPI app
app = FastAPI(
    title="AI Blog Generator",
    description="Automated blog generation system for generative AI topics",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware
origins = [
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:8081",
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins="*",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models for API
class BlogGenerationRequest(BaseModel):
    topic: Optional[str] = None
    
class SchedulerConfig(BaseModel):
    interval_minutes: int = 10

# API Endpoints

@app.get("/")
async def root():
    """Root endpoint with application info."""
    return {
        "message": "AI Blog Generator API",
        "description": "Automated blog generation system for generative AI topics",
        "version": "1.0.0",
        "scheduler_running": blog_scheduler.is_running(),
        "endpoints": {
            "health": "/health",
            "generate": "/generate",
            "posts": "/posts",
            "stats": "/stats",
            "scheduler": "/scheduler"
        }
    }

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    try:
        # Check database health
        db_healthy = await db_manager.health_check()
        if not db_healthy:
            # Try to reconnect
            await db_manager.connect()
            db_healthy = await db_manager.health_check()
        
        status = "healthy" if db_healthy else "unhealthy"
        status_code = 200 if db_healthy else 503
        
        response_data = {
            "status": status,
            "timestamp": datetime.now().isoformat(),
            "database": "connected" if db_healthy else "disconnected",
            "scheduler": "running" if blog_scheduler.is_running() else "stopped"
        }
        
        if db_healthy:
            return response_data
        else:
            return JSONResponse(
                status_code=status_code,
                content=response_data
            )
            
    except Exception as e:
        logger.error(f"Health check error: {e}")
        return JSONResponse(
            status_code=503,
            content={
                "status": "unhealthy",
                "timestamp": datetime.now().isoformat(),
                "database": "error",
                "scheduler": "unknown",
                "error": str(e)
            }
        )

@app.post("/generate")
async def generate_blog_post(request: BlogGenerationRequest, background_tasks: BackgroundTasks):
    """Manually trigger blog post generation."""
    try:
        if request.topic:
            # Generate with custom topic
            result = await blog_generator.generate_blog_post(custom_topic=request.topic)
        else:
            # Generate with random topic
            background_tasks.add_task(trigger_blog_generation)
            return {
                "message": "Blog generation started in background",
                "timestamp": datetime.now().isoformat()
            }
        
        if result:
            return {
                "message": "Blog post generated successfully",
                "blog_post": result,
                "timestamp": datetime.now().isoformat()
            }
        else:
            raise HTTPException(status_code=500, detail="Failed to generate blog post")
            
    except Exception as e:
        logger.error(f"Error generating blog post: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/posts")
async def get_recent_posts(limit: int = 10):
    """Get recent blog posts."""
    try:
        posts = await db_manager.get_recent_blog_posts(limit=limit)
        
        return {
            "posts": [
                {
                    "id": post.id,
                    "title": post.title,
                    "content": post.content,
                    "topic": post.topic,
                    "tags": post.tags,
                    "word_count": post.wordCount,
                    "meta_description": post.metaDescription,
                    "slug": post.slug,
                    "created_at": post.createdAt.isoformat(),
                    "updated_at": post.updatedAt.isoformat(),
                    "published": post.published
                }
                for post in posts
            ],
            "count": len(posts),
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Error fetching posts: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/posts/{post_id}")
async def get_blog_post(post_id: int):
    """Get a specific blog post by ID."""
    try:
        await db_manager.connect()
        post = await db_manager.db.blogpost.find_unique(where={"id": post_id})
        
        if not post:
            raise HTTPException(status_code=404, detail="Blog post not found")
        
        return {
            "id": post.id,
            "title": post.title,
            "content": post.content,
            "topic": post.topic,
            "tags": post.tags,
            "word_count": post.wordCount,
            "created_at": post.createdAt.isoformat(),
            "updated_at": post.updatedAt.isoformat(),
            "published": post.published
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching blog post {post_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/stats")
async def get_generation_stats(hours: int = 24):
    """Get blog generation statistics."""
    try:
        stats = await db_manager.get_generation_stats(hours=hours)
        
        return {
            "stats": stats,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Error fetching stats: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/scheduler")
async def get_scheduler_info():
    """Get scheduler information."""
    try:
        jobs = blog_scheduler.get_job_info()
        
        return {
            "running": blog_scheduler.is_running(),
            "jobs": jobs,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Error fetching scheduler info: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/scheduler/start")
async def start_scheduler(config: SchedulerConfig):
    """Start the scheduler with specified interval."""
    try:
        global scheduler_started
        
        if scheduler_started:
            return {
                "message": "Scheduler is already running",
                "timestamp": datetime.now().isoformat()
            }
        
        blog_scheduler.start_scheduler(interval_minutes=config.interval_minutes)
        scheduler_started = True
        
        return {
            "message": f"Scheduler started with {config.interval_minutes} minute interval",
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Error starting scheduler: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/scheduler/stop")
async def stop_scheduler_endpoint():
    """Stop the scheduler."""
    try:
        global scheduler_started
        
        if not scheduler_started:
            return {
                "message": "Scheduler is not running",
                "timestamp": datetime.now().isoformat()
            }
        
        blog_scheduler.stop_scheduler()
        scheduler_started = False
        
        return {
            "message": "Scheduler stopped successfully",
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Error stopping scheduler: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Signal handlers for graceful shutdown
def signal_handler(signum, frame):
    """Handle shutdown signals."""
    logger.info(f"Received signal {signum}, shutting down gracefully...")
    
    # Stop scheduler
    global scheduler_started
    if scheduler_started:
        blog_scheduler.stop_scheduler()
        scheduler_started = False
    
    sys.exit(0)

# Register signal handlers
signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)

# Standalone mode
async def main():
    """Run the application in standalone mode (without FastAPI server)."""
    try:
        logger.info("Starting AI Blog Generator in standalone mode...")
        
        # Connect to database
        await db_manager.connect()
        logger.info("Database connected")
        
        # Start scheduler
        blog_scheduler.start_scheduler(interval_minutes=10)
        logger.info("Scheduler started - generating blog posts every 10 minutes")
        
        # Generate first blog post immediately
        logger.info("Generating initial blog post...")
        await trigger_blog_generation()
        
        # Keep the application running
        logger.info("Application is running. Press Ctrl+C to stop.")
        
        try:
            while True:
                await asyncio.sleep(60)  # Check every minute
                
        except KeyboardInterrupt:
            logger.info("Received interrupt signal, shutting down...")
            
        finally:
            # Cleanup
            blog_scheduler.stop_scheduler()
            await db_manager.disconnect()
            logger.info("Application stopped")
            
    except Exception as e:
        logger.error(f"Error in main application: {e}")
        raise

if __name__ == "__main__":
    import uvicorn
    
    # Check if we want to run in API mode or standalone mode
    import os
    
    mode = os.getenv("RUN_MODE", "api").lower()
    
    if mode == "standalone":
        # Run in standalone mode
        asyncio.run(main())
    else:
        # Run FastAPI server
        uvicorn.run(
            "main:app",
            host="0.0.0.0",
            port=8000,
            reload=False,
            log_level="info"
        )
