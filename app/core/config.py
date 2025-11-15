"""
Application Configuration using Pydantic Settings
All configuration loaded from environment variables
"""

from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List


class Settings(BaseSettings):
    """Application settings with type validation"""
    
    # Database
    DATABASE_URL: str = "postgresql://cognisense:devpassword@localhost:5432/cognisense_db"
    
    # Security
    SECRET_KEY: str = "dev-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # CORS
    ALLOWED_ORIGINS: List[str] = ["http://localhost:3000", "chrome-extension://*"]
    
    # ML Models
    MODEL_CACHE_DIR: str = "./models"
    SENTIMENT_MODEL: str = "distilbert-base-uncased-finetuned-sst-2-english"
    ZERO_SHOT_MODEL: str = "facebook/bart-large-mnli"
    
    # Environment
    ENVIRONMENT: str = "development"
    LOG_LEVEL: str = "INFO"
    
    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=True,
        extra="ignore"
    )


# Global settings instance
settings = Settings()
