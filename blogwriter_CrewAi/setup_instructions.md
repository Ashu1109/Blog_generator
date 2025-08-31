# AI Blog Generator Setup Instructions

This application automatically generates blog posts on the latest generative AI topics every 10 minutes and saves them to a PostgreSQL database using Prisma.

## Prerequisites

1. **Python 3.9+**
2. **PostgreSQL Database**
3. **API Keys:**
   - OpenAI API key (for CrewAI agents)
   - SerperDev API key (for web search)

## Setup Steps

### 1. Install Dependencies

```bash
# Install Python dependencies
pip install -r requirements.txt

# Or using poetry (if you prefer)
poetry install
```

### 2. Database Setup

```bash
# Install Prisma CLI globally (if not already installed)
pip install prisma

# Generate Prisma client
prisma generate

# Apply database migrations
prisma db push
```

### 3. Environment Configuration

```bash
# Copy the example environment file
cp env.example .env

# Edit the .env file with your actual values
nano .env
```

Required environment variables:
- `DATABASE_URL`: Your PostgreSQL connection string
- `OPENAI_API_KEY`: Your OpenAI API key
- `SERPER_API_KEY`: Your SerperDev API key for web search

### 4. Database Migration

```bash
# Push the schema to your database
prisma db push

# Optional: View your database
prisma studio
```

## Running the Application

### Option 1: FastAPI Server Mode (Recommended)

```bash
# Run the FastAPI server
python main.py

# Or with uvicorn directly
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

The API will be available at: `http://localhost:8000`

API Documentation: `http://localhost:8000/docs`

### Option 2: Standalone Mode

```bash
# Set the run mode in .env file
RUN_MODE="standalone"

# Run in standalone mode
python main.py
```

## API Endpoints

- `GET /` - Application info and available endpoints
- `GET /health` - Health check
- `POST /generate` - Manually trigger blog generation
- `GET /posts` - Get recent blog posts
- `GET /posts/{id}` - Get specific blog post
- `GET /stats` - Get generation statistics
- `GET /scheduler` - Get scheduler information
- `POST /scheduler/start` - Start the scheduler
- `POST /scheduler/stop` - Stop the scheduler

## Configuration

### Scheduler Configuration

By default, the application generates a new blog post every 10 minutes. You can change this by:

1. **Environment Variable:**
   ```bash
   BLOG_GENERATION_INTERVAL_MINUTES=15
   ```

2. **API Call:**
   ```bash
   curl -X POST "http://localhost:8000/scheduler/start" \
        -H "Content-Type: application/json" \
        -d '{"interval_minutes": 15}'
   ```

### Database Schema

The application creates two main tables:

1. **blog_posts**: Stores generated blog posts
   - id, title, content, topic, tags, createdAt, updatedAt, published, wordCount

2. **generation_logs**: Tracks generation attempts
   - id, topic, status, errorMsg, createdAt, blogPostId

## Monitoring and Management

### View Recent Blog Posts

```bash
curl "http://localhost:8000/posts?limit=5"
```

### Check Generation Statistics

```bash
curl "http://localhost:8000/stats?hours=24"
```

### Manual Blog Generation

```bash
# Generate with random topic
curl -X POST "http://localhost:8000/generate" \
     -H "Content-Type: application/json" \
     -d '{}'

# Generate with custom topic
curl -X POST "http://localhost:8000/generate" \
     -H "Content-Type: application/json" \
     -d '{"topic": "Latest developments in RAG systems"}'
```

## Troubleshooting

### Common Issues

1. **Database Connection Error:**
   - Check your `DATABASE_URL` in `.env`
   - Ensure PostgreSQL is running
   - Verify database permissions

2. **API Key Errors:**
   - Verify your OpenAI API key is valid
   - Check SerperDev API key and quota
   - Ensure API keys are properly set in `.env`

3. **Prisma Issues:**
   ```bash
   # Regenerate Prisma client
   prisma generate
   
   # Reset database (WARNING: This will delete all data)
   prisma db push --force-reset
   ```

4. **Scheduler Not Starting:**
   - Check application logs
   - Verify no port conflicts
   - Ensure sufficient system resources

### Logs

The application provides detailed logging. Check the console output for:
- Blog generation progress
- Database operations
- Scheduler status
- Error messages

### Performance Considerations

- Each blog generation takes 2-5 minutes depending on AI response times
- The scheduler prevents overlapping jobs
- Database operations are optimized for concurrent access
- Consider increasing interval for high-traffic scenarios

## Development

### Project Structure

```
blogwriter_CrewAi/
├── main.py                 # Main application entry point
├── src/
│   ├── blog_generator.py   # Enhanced blog generation with CrewAI
│   ├── scheduler.py        # APScheduler implementation
│   ├── database/
│   │   ├── connection.py   # Database operations
│   │   └── __init__.py
│   └── config/             # Configuration modules
├── prisma/
│   └── schema.prisma       # Database schema
├── requirements.txt        # Python dependencies
└── pyproject.toml         # Project configuration
```

### Adding New Features

1. **Custom Topics:** Modify `GENERATIVE_AI_TOPICS` in `blog_generator.py`
2. **New Agents:** Add agents in the `EnhancedBlogGenerator` class
3. **Database Models:** Update `schema.prisma` and run `prisma db push`
4. **API Endpoints:** Add new endpoints in `main.py`

## License

This project is licensed under the MIT License.
