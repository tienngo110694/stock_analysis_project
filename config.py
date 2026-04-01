import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    # Discord Configuration
    DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
    
    # AI Configuration (Gemini)
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    GEMINI_MODEL_PRO = 'gemini-2.0-pro-exp-02-05'  # Or latest available
    GEMINI_MODEL_FLASH = 'gemini-2.0-flash'
    
    # Database Configuration (ClickHouse)
    CLICKHOUSE_HOST = os.getenv('CLICKHOUSE_HOST', 'localhost')
    CLICKHOUSE_PORT = int(os.getenv('CLICKHOUSE_PORT', 8123))
    CLICKHOUSE_USER = os.getenv('CLICKHOUSE_USER', 'default')
    CLICKHOUSE_PASSWORD = os.getenv('CLICKHOUSE_PASSWORD', '')
    CLICKHOUSE_DATABASE = os.getenv('CLICKHOUSE_DATABASE', 'stock_analysis')
    
    # Webhook Configuration (n8n)
    N8N_WEBHOOK_URL = os.getenv("N8N_WEBHOOK_URL")
    
    # Ollama Configuration (Local AI)
    OLLAMA_BASE_URL = os.getenv('OLLAMA_BASE_URL', 'http://localhost:11434')
    OLLAMA_EMBED_MODEL = 'nomic-embed-text' # or mxbai-embed-large
