"""
Zero-Shot Classification Service
Classifies content into categories without training data
Used for categorizing browsing content (Productivity, Social, Entertainment, etc.)
"""

from typing import List, Dict
from loguru import logger

from app.ml.model_manager import ModelManager


class ZeroShotClassifier:
    """Service for zero-shot classification of content"""
    
    # Default categories for content classification
    DEFAULT_CATEGORIES = [
        "Productivity",
        "Social Media",
        "Entertainment",
        "News",
        "Shopping",
        "Education",
        "Health & Wellness",
        "Technology",
        "Finance",
        "Other"
    ]
    
    def __init__(self):
        self.model_manager = ModelManager()
    
    def classify(
        self,
        text: str,
        categories: List[str] = None,
        multi_label: bool = False
    ) -> Dict[str, any]:
        """
        Classify text into one or more categories
        
        Args:
            text: Text content to classify
            categories: List of possible categories (uses DEFAULT_CATEGORIES if None)
            multi_label: Whether to allow multiple categories (default: False)
        
        Returns:
            Dictionary with labels and scores
            Example: {"labels": ["Productivity", "Technology"], "scores": [0.95, 0.85]}
        """
        if not text or len(text.strip()) == 0:
            return {"labels": ["Other"], "scores": [1.0], "error": "Empty text"}
        
        if categories is None:
            categories = self.DEFAULT_CATEGORIES
        
        try:
            model = self.model_manager.get_zero_shot_classifier()
            
            # Truncate text if too long
            max_length = 512
            if len(text.split()) > max_length:
                text = ' '.join(text.split()[:max_length])
                logger.warning(f"Text truncated to {max_length} words for classification")
            
            result = model(
                text,
                candidate_labels=categories,
                multi_label=multi_label
            )
            
            logger.debug(f"Classification: {result['labels'][0]} ({result['scores'][0]:.2f})")
            
            return {
                "labels": result['labels'],
                "scores": result['scores']
            }
            
        except Exception as e:
            logger.error(f"Zero-shot classification failed: {e}")
            return {"labels": ["Other"], "scores": [1.0], "error": str(e)}
    
    def classify_productivity(self, text: str) -> Dict[str, any]:
        """
        Classify if content is productive or distracting
        
        Args:
            text: Text content to classify
        
        Returns:
            Dictionary with productivity classification
        """
        categories = ["Productive", "Distracting"]
        return self.classify(text, categories=categories)
