from dotenv import load_dotenv
import sys, os
from pydantic_settings import BaseSettings

# Ensure project root is in sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Load .env file
load_dotenv()

class Settings(BaseSettings):
    MONGO_DB_URL: str
    MONGO_DB_NAME: str
    OLLAMA_URL: str
    OLLAMA_MODELS: str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
