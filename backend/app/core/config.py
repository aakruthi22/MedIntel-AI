import os
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    PROJECT_NAME: str = os.getenv("PROJECT_NAME", "MEDINTEL AI")
    VERSION: str = os.getenv("VERSION", "1.0.0")
    API_V1_STR: str = "/api/v1"
    
    # Security
    SECRET_KEY: str = os.getenv("SECRET_KEY", "SUPER_SECRET_KEY_CHANGE_ME")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8  # 8 days
    
    # Persistence
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./medintel.db")
    CHROMA_DB_PATH: str = os.getenv("CHROMA_DB_PATH", "./app/data/chroma")
    
    class Config:
        case_sensitive = True

settings = Settings()