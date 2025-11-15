"""
Mock Model Manager for development without ML dependencies
This allows the API to run for testing basic functionality
"""

from typing import Optional
from loguru import logger

from app.core.config import settings


class MockModelManager:
    """
    Mock version of ModelManager for development/testing without ML dependencies
    Provides dummy responses to allow API development and testing
    """
    
    _instance: Optional['MockModelManager'] = None
    _models_loaded: bool = False
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        """Initialize mock model placeholders"""
        self.sentiment_analyzer = MockSentimentAnalyzer()
        self.zero_shot_classifier = MockZeroShotClassifier()
        self.emotion_detector = MockEmotionDetector()
    
    async def load_models(self):
        """Mock model loading"""
        logger.info("Loading MOCK ML models (no actual models loaded)")
        self._models_loaded = True
        logger.info("✓ Mock ML models 'loaded' successfully")
    
    def is_loaded(self) -> bool:
        """Check if models are loaded"""
        return self._models_loaded
    
    def get_sentiment_analyzer(self):
        """Get mock sentiment analysis model"""
        return self.sentiment_analyzer
    
    def get_zero_shot_classifier(self):
        """Get mock zero-shot classification model"""
        return self.zero_shot_classifier
    
    def get_emotion_detector(self):
        """Get mock emotion detection model"""
        return self.emotion_detector


class MockSentimentAnalyzer:
    """Mock sentiment analyzer"""
    
    def __call__(self, text: str):
        # Return mock positive sentiment
        return [{"label": "POSITIVE", "score": 0.85}]


class MockZeroShotClassifier:
    """Mock zero-shot classifier"""
    
    def __call__(self, text: str, candidate_labels: list, multi_label: bool = False):
        # Return mock productivity classification
        return {
            "labels": ["Technology", "Productivity", "Other"],
            "scores": [0.70, 0.20, 0.10]
        }


class MockEmotionDetector:
    """Mock emotion detector"""
    
    def __call__(self, text: str):
        # Return mock emotions
        return [[
            {"label": "joy", "score": 0.60},
            {"label": "neutral", "score": 0.30},
            {"label": "sadness", "score": 0.10}
        ]]


# Use MockModelManager instead of real one when ML dependencies aren't available
try:
    from transformers import pipeline
    # If we reach here, transformers is available, use real ModelManager
    from app.ml.model_manager_real import ModelManager
except ImportError:
    # Transformers not available, use mock
    ModelManager = MockModelManager
    logger.warning("Using MockModelManager - install 'transformers' and 'torch' for real ML functionality")