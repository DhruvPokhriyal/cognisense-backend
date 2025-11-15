"""
Logging configuration using Loguru
"""

import sys
from loguru import logger
from app.core.config import settings


def setup_logging():
    """Configure Loguru logger with appropriate settings"""
    
    # Remove default handler
    logger.remove()
    
    # Add custom handler with formatting
    logger.add(
        sys.stdout,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan> - <level>{message}</level>",
        level=settings.LOG_LEVEL,
        colorize=True,
    )
    
    # Add file handler for production
    if settings.ENVIRONMENT == "production":
        logger.add(
            "logs/app_{time}.log",
            rotation="500 MB",
            retention="10 days",
            level="INFO",
            format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function} - {message}",
        )
    
    logger.info(f"Logging initialized - Level: {settings.LOG_LEVEL}, Environment: {settings.ENVIRONMENT}")
