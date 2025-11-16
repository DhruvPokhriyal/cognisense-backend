"""
Categories API
Allows users to set site classifications and perform content-based classification.
"""

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel, Field
from typing import Dict, Optional
from loguru import logger

from app.ml.zero_shot_classifier import ZeroShotClassifier

router = APIRouter()

# In-memory per-user site classification preferences
USER_SITE_PREFERENCES: Dict[str, Dict[str, str]] = {}

zero_shot = ZeroShotClassifier()


class SitePreference(BaseModel):
    user_id: str
    site: str
    category: str = Field(..., description="User chosen category e.g., Productivity, Entertainment")


@router.post("/user/{user_id}/sites")
async def set_site_preference(user_id: str, pref: SitePreference):
    if user_id != pref.user_id:
        raise HTTPException(status_code=400, detail="user_id mismatch")
    USER_SITE_PREFERENCES.setdefault(user_id, {})[pref.site] = pref.category
    logger.info(f"Set site pref for {user_id} {pref.site} -> {pref.category}")
    return {"status": "ok", "site": pref.site, "category": pref.category}


@router.get("/user/{user_id}/sites")
async def get_site_preferences(user_id: str):
    prefs = USER_SITE_PREFERENCES.get(user_id, {})
    return {"user_id": user_id, "preferences": prefs}


@router.get("/classify")
async def classify_text(text: str = Query(..., min_length=1)):
    """Return zero-shot classification for a short text snippet."""
    try:
        res = zero_shot.classify(text)
        return {"labels": res.get("labels"), "scores": res.get("scores")}
    except Exception as e:
        logger.error(f"Classification failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/labels")
async def get_available_labels():
    """Get all available category labels for content classification."""
    return {
        "categories": zero_shot.DEFAULT_CATEGORIES,
        "total": len(zero_shot.DEFAULT_CATEGORIES)
    }


@router.get("/groups")
async def get_category_groups():
    """Get categories organized by broad groups (Productive, Social, Entertainment, etc.)."""
    return {
        "groups": zero_shot.get_category_groups()
    }


@router.get("/classify/grouped")
async def classify_text_with_group(text: str = Query(..., min_length=1)):
    """Classify text and return both specific category and broad group."""
    try:
        res = zero_shot.classify_with_group(text)
        return res
    except Exception as e:
        logger.error(f"Grouped classification failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))
