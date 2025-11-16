"""
Emotion Detection Service
Analyzes emotional tone of text (joy, anger, sadness, fear, etc.)
"""

from typing import Dict, List
from loguru import logger

from app.ml.model_manager import ModelManager


class EmotionDetector:
    """Service for detecting emotions in text"""
    
    def __init__(self):
        self.model_manager = ModelManager()
    
    def detect(self, text: str) -> List[Dict[str, any]]:
        """
        Detect emotions in text
        
        Args:
            text: Text content to analyze
        
        Returns:
            List of emotions with scores
            Example: [
                {"label": "joy", "score": 0.85},
                {"label": "sadness", "score": 0.10},
                ...
            ]
        """
        if not text or len(text.strip()) == 0:
            return [{"label": "neutral", "score": 1.0, "error": "Empty text"}]
        
        try:
            model = self.model_manager.get_emotion_detector()
            
            # Truncate text if too long
            max_length = 512
            if len(text.split()) > max_length:
                text = ' '.join(text.split()[:max_length])
                logger.warning(f"Text truncated to {max_length} words for emotion detection")
            
            # Ensure inputs never exceed model max length at token level
            results = model(text, truncation=True, max_length=512)[0]  # Returns list of all emotions
            
            # Sort by score descending
            results = sorted(results, key=lambda x: x['score'], reverse=True)
            
            logger.debug(f"Top emotion: {results[0]['label']} ({results[0]['score']:.2f})")
            
            return results
            
        except Exception as e:
            logger.error(f"Emotion detection failed: {e}")
            return [{"label": "neutral", "score": 1.0, "error": str(e)}]
    
    def get_dominant_emotion(self, text: str) -> Dict[str, any]:
        """
        Get the dominant emotion from text
        
        Args:
            text: Text content to analyze
        
        Returns:
            Dictionary with dominant emotion and score
        """
        emotions = self.detect(text)
        return emotions[0] if emotions else {"label": "neutral", "score": 0.0}
    
    def calculate_emotional_balance(self, emotions: List[Dict[str, any]]) -> Dict[str, float]:
        """
        Calculate emotional balance score from emotion results
        
        Args:
            emotions: List of emotion dictionaries with 'label' and 'score'
        
        Returns:
            Dictionary with emotional balance metrics
        """
        positive_emotions = ['joy', 'love', 'surprise']
        negative_emotions = ['anger', 'sadness', 'fear', 'disgust']
        
        positive_score = sum(
            e['score'] for e in emotions if e['label'] in positive_emotions
        )
        negative_score = sum(
            e['score'] for e in emotions if e['label'] in negative_emotions
        )
        
        total = positive_score + negative_score
        if total == 0:
            balance = 0.5  # Neutral
        else:
            balance = positive_score / total
        
        return {
            "positive_score": positive_score,
            "negative_score": negative_score,
            "balance": balance,  # 0.0 (very negative) to 1.0 (very positive)
            "is_balanced": 0.4 <= balance <= 0.6
        }
