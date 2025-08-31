import os
import asyncio
import json
from crewai import Agent, Task, Process, Crew
from crewai_tools import SerperDevTool
from dotenv import load_dotenv
from apscheduler.schedulers.asyncio import AsyncIOScheduler

# Add src to path to allow for local imports
import sys
sys.path.insert(0, './src')
from database.connection import db_manager

# Load environment variables from .env file
load_dotenv()

import re


# --- CrewAI setup ---
def create_blog_writer_crew():
    """Create and configure the blog writer crew."""
    search_tool = SerperDevTool()

    # Define the blog writer agent
    writer_agent = Agent(
        role="Senior SEO Content Strategist",
        goal="Craft a compelling, SEO-optimized blog post on a given topic, including title, tags, and meta description.",
        backstory=(
            "With a decade of experience in digital marketing and content creation, "
            "you have a proven trackrecord of writing articles that rank high on search engines "
            "and engage readers from start to finish."
        ),
        verbose=True,
        allow_delegation=False,
        tools=[search_tool],
    )

    # Define the blog writing task
    writing_task = Task(
        description="Write a 2000-word, SEO-friendly blog post on the topic: '{topic}'.",
        expected_output=(
            "A comprehensive, well-structured, and engaging blog post in markdown format. "
            "The output should be a JSON object containing the following keys: "
            "'title' (string), 'content' (string in markdown), 'tags' (list of strings), "
            "and 'meta_description' (string)."
        ),
        agent=writer_agent,
    )

    # Assemble the crew
    blog_crew = Crew(
        agents=[writer_agent],
        tasks=[writing_task],
        process=Process.sequential,
        verbose=2,
        output_json=True # Force the output to be JSON
    )
    
    return blog_crew

# --- Main job function ---
async def generate_and_save_blog():
    """The main async job to be scheduled."""
    print("🚀 Starting blog generation job...")
    
    topic = "The Future of AI in Content Creation"
    log_entry = None
    
    try:
        # Log the start of the generation
        await db_manager.connect()
        log_entry = await db_manager.log_generation_attempt(topic, 'in_progress')
        
        crew = create_blog_writer_crew()
        result_json_str = crew.kickoff(inputs={'topic': topic})
        
        # The result from a JSON output crew is a string, so we need to find and parse it.
        # The agent can sometimes add conversational text before or after the JSON.
        json_match = re.search(r'\{.*\}', result_json_str, re.DOTALL)
        
        if not json_match:
            raise ValueError("Could not extract valid JSON from the crew's output.")
            
        json_string = json_match.group(0)
        
        try:
            # The strict=False parameter allows for control characters within the string
            result_data = json.loads(json_string, strict=False)
        except json.JSONDecodeError as e:
            print(f"Failed to decode JSON: {e}")
            print(f"Problematic JSON string: {json_string}")
            raise


        if result_data and all(k in result_data for k in ['title', 'content', 'tags', 'meta_description']):
            word_count = len(result_data['content'].split())
            
            # Save the blog post
            blog_post = await db_manager.create_blog_post(
                title=result_data['title'],
                content=result_data['content'],
                topic=topic,
                tags=result_data['tags'],
                word_count=word_count,
                meta_description=result_data['meta_description']
            )

            if blog_post:
                # Update the log to success
                await db_manager.log_generation_attempt(topic, 'success', blog_post_id=blog_post.id)
                print(f"✅ Blog post on '{topic}' saved to the database.")
            else:
                # Update the log to failed if post saving failed
                await db_manager.log_generation_attempt(topic, 'failed', error_msg="Failed to save blog post to DB.")
                print("❌ Failed to save blog post to the database.")

        else:
            # Update the log to failed if result is invalid
            await db_manager.log_generation_attempt(topic, 'failed', error_msg="Generated content was invalid or incomplete.")
            print("❌ Blog generation returned invalid or incomplete content.")

    except Exception as e:
        print(f"An error occurred during blog generation: {e}")
        if log_entry:
            # Update the log to failed on exception
            await db_manager.log_generation_attempt(topic, 'failed', error_msg=str(e))
    finally:
        if db_manager._connected:
            await db_manager.disconnect()

    print("✅ Blog generation job finished.")

# --- Scheduler setup ---
async def main():
    """Main function to run the scheduled job."""
    print("📅 Initializing blog generation scheduler...")
    
    scheduler = AsyncIOScheduler()
    
    # Schedule the job to run every 10 minutes
    scheduler.add_job(generate_and_save_blog, 'interval', minutes=10)
    
    # Run the job once immediately
    scheduler.add_job(generate_and_save_blog, 'date')
    
    scheduler.start()
    
    print("⏰ Scheduler started. Press Ctrl+C to exit.")
    
    # Keep the script running
    try:
        while True:
            await asyncio.sleep(1)
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()
        if db_manager._connected:
            await db_manager.disconnect()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nScheduler stopped.")
