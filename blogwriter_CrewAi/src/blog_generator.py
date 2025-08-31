"""Enhanced blog generator with dynamic topic generation and database integration."""

import asyncio
import logging
import re
from typing import Optional, List, Dict, Any
from datetime import datetime
import random

from crewai import Agent, Task, Process, Crew
from crewai_tools import SerperDevTool
from dotenv import load_dotenv
import os

from .database.connection import db_manager, save_blog_post, log_generation

# Load environment variables
load_dotenv()

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class EnhancedBlogGenerator:
    """Enhanced blog generator with dynamic topic generation and database integration."""
    
    # Diverse generative AI topics for dynamic content
    GENERATIVE_AI_TOPICS = [
        "Large Language Models (LLMs) and their latest developments",
        "Retrieval-Augmented Generation (RAG) systems and applications",
        "AI Agents and autonomous systems",
        "Multi-modal AI models combining text, image, and audio",
        "AI-powered chatbots and conversational interfaces",
        "AI image generation and computer vision breakthroughs",
        "AI video generation and synthetic media",
        "AI audio and music generation technologies",
        "AI code generation and programming assistants",
        "Prompt engineering and optimization techniques",
        "Fine-tuning and customization of AI models",
        "AI safety and alignment research",
        "Edge AI and on-device machine learning",
        "AI in creative industries and content creation",
        "Generative AI ethics and responsible AI development",
        "AI model compression and efficiency improvements",
        "Open-source vs proprietary AI models comparison",
        "AI-powered automation tools and workflows",
        "Generative AI in healthcare and medical applications",
        "AI in education and personalized learning systems"
    ]
    
    def __init__(self):
        self.search_tool = SerperDevTool()
        self.setup_agents()
    
    def setup_agents(self):
        """Set up CrewAI agents."""
        # Use GPT-3.5-turbo for more efficient token usage
        model_config = {
            "model": "gpt-4o",  # Higher token limit variant
            "temperature": 0.7,
            "max_tokens": 1500  # Limit response length
        }
        
        self.research_agent = Agent(
            role="AI Research Specialist",
            goal="Research the latest trends and developments in generative AI efficiently.",
            backstory="You are an AI researcher who creates concise, informative summaries of the latest developments in generative AI.",
            verbose=False,  # Reduce verbosity to save tokens
            allow_delegation=False,  # Disable delegation to save tokens
            tools=[self.search_tool],
            llm_config=model_config
        )
        
        self.writer_agent = Agent(
            role="Senior Tech Blog Writer",
            goal="Write well-structured, engaging blog posts about generative AI in proper markdown format.",
            backstory="You are an experienced technology writer who creates clear, informative content about AI and emerging technologies.",
            verbose=False,
            allow_delegation=False,
            tools=[self.search_tool],
            llm_config=model_config
        )
        
        self.editor_agent = Agent(
            role="Content Editor and SEO Specialist",
            goal="Edit and optimize blog content for web publication with proper markdown formatting.",
            backstory="You are a content editor who ensures all content is polished, properly formatted, and optimized for web publication.",
            verbose=False,
            allow_delegation=False,
            llm_config=model_config
        )
    
    def generate_dynamic_topic(self) -> str:
        """Generate a dynamic topic for blog generation."""
        base_topic = random.choice(self.GENERATIVE_AI_TOPICS)
        
        # Add current context or trending aspects
        current_year = datetime.now().year
        trending_aspects = [
            f"in {current_year}",
            "latest trends and innovations",
            "breaking developments",
            "industry impact and future prospects",
            "practical applications and use cases",
            "challenges and opportunities ahead"
        ]
        
        aspect = random.choice(trending_aspects)
        return f"{base_topic} - {aspect}"
    
    def create_research_task(self, topic: str) -> Task:
        """Create a research task for the given topic."""
        return Task(
            description=f"""
            Research the latest information about: {topic}
            
            Focus on these key areas:
            1. Latest developments and breakthroughs (2-3 key points)
            2. Major companies and technologies involved
            3. Current market trends and adoption
            4. Real-world applications and use cases
            
            Keep your research summary concise but informative - aim for 200-300 words maximum.
            Include 2-3 key statistics or facts.
            """,
            expected_output="A concise research summary (200-300 words) with key findings and statistics about the topic.",
            agent=self.research_agent,
        )
    
    def create_writing_task(self, topic: str) -> Task:
        """Create a writing task for the given topic."""
        return Task(
            description=f"""
            Write a well-structured blog post about: {topic}
            
            IMPORTANT: Format the output as proper Markdown for web publishing.
            
            Requirements:
            1. Write 800-1200 words (concise but comprehensive)
            2. Start with a compelling title using # header
            3. Include an engaging introduction (2-3 paragraphs)
            4. Use ## for main sections and ### for subsections
            5. Include practical examples and real-world applications
            6. Add relevant statistics and facts from research
            7. Write in an accessible, professional tone
            8. End with a strong conclusion and key takeaways
            9. Include 5-7 relevant tags at the end using **Tags:** format
            
            Markdown Structure Example:
            # Your Compelling Title Here
            
            ## Introduction
            Your engaging introduction here...
            
            ## Main Section 1
            Content with **bold** and *italic* emphasis...
            
            ### Subsection
            - Bullet points for clarity
            - Key statistics and facts
            
            ## Conclusion
            Strong conclusion with actionable insights...
            
            **Tags:** tag1, tag2, tag3, tag4, tag5
            
            Keep content focused and avoid overly long sections to prevent token limits.
            """,
            expected_output="A complete 800-1200 word blog post in proper Markdown format with title, structured content, and tags.",
            agent=self.writer_agent,
        )
    
    def create_editing_task(self) -> Task:
        """Create an editing and optimization task."""
        return Task(
            description="""
            Edit and optimize the blog post for web publication:
            
            1. Ensure perfect Markdown formatting for web display
            2. Review for grammar, spelling, and readability
            3. Verify proper heading hierarchy (# ## ###)
            4. Check that all sections flow logically
            5. Ensure consistent tone and professional style
            6. Optimize for web readability (short paragraphs, bullet points)
            7. Verify all facts and statistics are accurate
            8. Add meta description suggestion (150-160 characters)
            
            Output the final blog post in clean Markdown format ready for web publishing.
            Include a suggested meta description at the end.
            """,
            expected_output="A polished blog post in perfect Markdown format ready for web publication, with meta description.",
            agent=self.editor_agent,
        )
    
    def extract_blog_components(self, crew_output: str) -> Dict[str, Any]:
        """Extract title, content, and tags from crew output."""
        try:
            # Clean the output
            content = crew_output.strip()
            
            # Extract title from markdown (look for # header)
            title_match = re.search(r'^#\s+(.+?)(?:\n|$)', content, re.MULTILINE)
            if title_match:
                title = title_match.group(1).strip()
            else:
                # Fallback title patterns
                title_patterns = [
                    r"(?:Title|TITLE):\s*(.+?)(?:\n|$)",
                    r"(?:^|\n)([A-Z][^.\n]+(?:AI|Technology|Intelligence|Machine Learning|Deep Learning)[^.\n]*)",
                ]
                title = "Latest Developments in Generative AI"  # Default title
                for pattern in title_patterns:
                    match = re.search(pattern, content, re.MULTILINE | re.IGNORECASE)
                    if match:
                        title = match.group(1).strip()
                        break
            
            # Clean up title
            title = title.strip('"\'')  # Remove quotes
            
            # Extract tags (look for **Tags:** pattern first, then fallback patterns)
            tags_patterns = [
                r"\*\*Tags:\*\*\s*(.+?)(?:\n|$)",
                r"(?:Tags|TAGS|Keywords):\s*(.+?)(?:\n|$)",
                r"(?:Suggested tags|Relevant tags):\s*(.+?)(?:\n|$)",
            ]
            
            tags = []
            for pattern in tags_patterns:
                match = re.search(pattern, content, re.MULTILINE | re.IGNORECASE)
                if match:
                    tags_text = match.group(1)
                    # Split by common delimiters
                    tags = [tag.strip().strip(',').strip() for tag in re.split(r'[,;|]', tags_text)]
                    tags = [tag for tag in tags if tag and len(tag) > 1]
                    break
            
            # Default tags if none found
            if not tags:
                tags = ["Generative AI", "Artificial Intelligence", "Technology", "Machine Learning", "Innovation"]
            
            # Extract meta description if present
            meta_desc_match = re.search(r'(?:Meta Description|meta description):\s*(.+?)(?:\n|$)', content, re.IGNORECASE)
            meta_description = meta_desc_match.group(1).strip() if meta_desc_match else None
            
            # Clean content for better web display
            # Remove any meta description lines from the main content
            if meta_description:
                content = re.sub(r'(?:Meta Description|meta description):\s*.+?(?:\n|$)', '', content, flags=re.IGNORECASE)
            
            # Ensure proper markdown formatting
            content = self.ensure_proper_markdown(content)
            
            # Calculate word count (excluding markdown syntax)
            text_only = re.sub(r'[#*`\[\]()]', '', content)
            word_count = len(text_only.split())
            
            return {
                "title": title,
                "content": content,
                "tags": tags[:7],  # Limit to 7 tags
                "word_count": word_count,
                "meta_description": meta_description
            }
            
        except Exception as e:
            logger.error(f"Error extracting blog components: {e}")
            return {
                "title": "Generated Blog Post on Generative AI",
                "content": crew_output,
                "tags": ["Generative AI", "Technology"],
                "word_count": len(crew_output.split()),
                "meta_description": None
            }
    
    def ensure_proper_markdown(self, content: str) -> str:
        """Ensure the content has proper markdown formatting."""
        try:
            # Split into lines for processing
            lines = content.split('\n')
            processed_lines = []
            
            for line in lines:
                line = line.strip()
                if not line:
                    processed_lines.append('')
                    continue
                
                # Ensure main title starts with single #
                if line.startswith('# ') and not line.startswith('## '):
                    processed_lines.append(line)
                # Ensure section headers are properly formatted
                elif line.startswith('##') or line.startswith('###'):
                    processed_lines.append(line)
                # Convert unformatted headers to proper markdown
                elif line.isupper() and len(line.split()) <= 5:
                    processed_lines.append(f"## {line.title()}")
                else:
                    processed_lines.append(line)
            
            return '\n'.join(processed_lines)
            
        except Exception as e:
            logger.error(f"Error formatting markdown: {e}")
            return content
    
    async def generate_blog_post(self, custom_topic: Optional[str] = None) -> Optional[Dict[str, Any]]:
        """Generate a blog post and save it to the database."""
        try:
            # Generate or use provided topic
            topic = custom_topic or self.generate_dynamic_topic()
            logger.info(f"Generating blog post for topic: {topic}")
            
            # Log generation attempt
            await log_generation(topic, "in_progress")
            
            # Create tasks
            research_task = self.create_research_task(topic)
            writing_task = self.create_writing_task(topic)
            editing_task = self.create_editing_task()
            
            # Set up crew
            crew = Crew(
                agents=[self.research_agent, self.writer_agent, self.editor_agent],
                tasks=[research_task, writing_task, editing_task],
                verbose=True,
                process=Process.sequential,
            )
            
            # Generate content
            logger.info("Starting blog generation process...")
            result = crew.kickoff()
            
            if not result:
                await log_generation(topic, "failed", "No output generated from crew")
                return None
            
            # Extract components
            blog_components = self.extract_blog_components(str(result))
            
            # Save to database
            blog_post = await save_blog_post(
                title=blog_components["title"],
                content=blog_components["content"],
                topic=topic,
                tags=blog_components["tags"],
                word_count=blog_components["word_count"],
                meta_description=blog_components.get("meta_description")
            )
            
            if blog_post:
                await log_generation(topic, "success", blog_post_id=blog_post.id)
                logger.info(f"Successfully generated and saved blog post: {blog_post.title}")
                
                return {
                    "id": blog_post.id,
                    "title": blog_post.title,
                    "topic": topic,
                    "tags": blog_post.tags,
                    "word_count": blog_post.wordCount,
                    "created_at": blog_post.createdAt
                }
            else:
                await log_generation(topic, "failed", "Failed to save to database")
                return None
                
        except Exception as e:
            error_msg = f"Error generating blog post: {str(e)}"
            logger.error(error_msg)
            await log_generation(topic if 'topic' in locals() else "unknown", "failed", error_msg)
            return None

# Global blog generator instance
blog_generator = EnhancedBlogGenerator()
