"""
Sentiment Analysis Service
Analyzes text to determine positive, negative, or neutral sentiment
"""

from typing import Dict
from loguru import logger

from app.ml.model_manager import ModelManager


class SentimentAnalyzer:
    """Service for analyzing sentiment of text content"""
    
    def __init__(self):
        self.model_manager = ModelManager()
    
    def analyze(self, text: str) -> Dict[str, any]:
        """
        Analyze sentiment of given text
        
        Args:
            text: Text content to analyze
        
        Returns:
            Dictionary with sentiment label and confidence score
            Example: {"label": "POSITIVE", "score": 0.9998}
        """
        if not text or len(text.strip()) == 0:
            return {"label": "NEUTRAL", "score": 0.0, "error": "Empty text"}
        
        try:
            model = self.model_manager.get_sentiment_analyzer()
            
            # Truncate text if too long (tensor size is usually 512 tokens)
            max_length = 512
            if len(text.split()) > max_length:
                text = ' '.join(text.split()[:max_length])
                logger.warning(f"Text truncated to {max_length} words for sentiment analysis")
            
            # Ensure tokenizer-level truncation to model max length
            result = model(text, truncation=True, max_length=512)[0]
            
            # Normalize label to uppercase
            result['label'] = result['label'].upper()
            
            logger.debug(f"Sentiment: {result['label']} ({result['score']:.2f})")
            
            return result
            
        except Exception as e:
            logger.error(f"Sentiment analysis failed: {e}")
            return {"label": "NEUTRAL", "score": 0.0, "error": str(e)}
    
    def analyze_batch(self, texts: list[str]) -> list[Dict[str, any]]:
        """
        Analyze sentiment for multiple texts
        
        Args:
            texts: List of text strings
        
        Returns:
            List of sentiment results
        """
        return [self.analyze(text) for text in texts]
