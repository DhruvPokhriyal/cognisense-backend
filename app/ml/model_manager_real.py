"""
ML Model Manager - Singleton pattern for loading and caching Hugging Face models
Models are loaded once at startup and kept in memory for the application lifecycle
"""

from typing import Optional
from transformers import pipeline
from loguru import logger

from app.core.config import settings


class ModelManager:
    """
    Singleton class to manage ML models
    Loads models once and caches them in memory
    """
    
    _instance: Optional['ModelManager'] = None
    _models_loaded: bool = False
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        """Initialize model placeholders"""
        self.sentiment_analyzer = None
        self.zero_shot_classifier = None
        self.emotion_detector = None
    
    async def load_models(self):
        """
        Load all ML models asynchronously
        Called during application startup
        """
        if self._models_loaded:
            logger.info("Models already loaded, skipping...")
            return
        
        try:
            logger.info("Loading ML models...")
            
            # Sentiment Analysis Model
            logger.info(f"Loading sentiment model: {settings.SENTIMENT_MODEL}")
            self.sentiment_analyzer = pipeline(
                "sentiment-analysis",
                model=settings.SENTIMENT_MODEL,
                device=-1  # CPU, use 0 for GPU
            )
            
            # Zero-shot Classification Model (for categorization)
            logger.info(f"Loading zero-shot classifier: {settings.ZERO_SHOT_MODEL}")
            self.zero_shot_classifier = pipeline(
                "zero-shot-classification",
                model=settings.ZERO_SHOT_MODEL,
                device=-1
            )
            
            # Emotion Detection Model
            logger.info("Loading emotion detection model")
            self.emotion_detector = pipeline(
                "text-classification",
                model="j-hartmann/emotion-english-distilroberta-base",
                device=-1,
                top_k=None  # Return all emotion scores
            )
            
            self._models_loaded = True
            logger.info("✓ All ML models loaded successfully")
            
        except Exception as e:
            logger.error(f"Failed to load ML models: {e}")
            raise
    
    def is_loaded(self) -> bool:
        """Check if models are loaded"""
        return self._models_loaded
    
    def get_sentiment_analyzer(self):
        """Get sentiment analysis model"""
        if not self._models_loaded:
            raise RuntimeError("Models not loaded. Call load_models() first.")
        return self.sentiment_analyzer
    
    def get_zero_shot_classifier(self):
        """Get zero-shot classification model"""
        if not self._models_loaded:
            raise RuntimeError("Models not loaded. Call load_models() first.")
        return self.zero_shot_classifier
    
    def get_emotion_detector(self):
        """Get emotion detection model"""
        if not self._models_loaded:
            raise RuntimeError("Models not loaded. Call load_models() first.")
        return self.emotion_detector
