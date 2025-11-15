"""
Model Manager with automatic fallback to mock when ML dependencies unavailable
"""

from loguru import logger

try:
    # Try to import transformers and torch
    import torch
    from transformers import pipeline
    
    # If successful, use the real ModelManager
    from app.ml.model_manager_real import ModelManager
    logger.info("Using real ModelManager with ML capabilities")
    
except (ImportError, NameError) as e:
    # If imports fail, use mock ModelManager
    from app.ml.model_manager_mock import MockModelManager as ModelManager
    logger.warning(f"ML dependencies not available ({e}). Using MockModelManager for development.")
    logger.warning("To enable real ML: pip install torch transformers")
