"""
API v1 Main Router
Aggregates all v1 endpoint routers
"""

import importlib.util
import sys
from fastapi import APIRouter
from loguru import logger

from app.api.v1 import content
from app.api.v1.dashboard.dashboard import router as dashboard_router
from app.api.v1.dashboard.insights import router as insights_router
from app.api.v1.dashboard.settings import router as settings_router
from app.api.v1 import tracking, categories, user_domain_category

from pathlib import Path
dashboard_file = Path(__file__).parent / "dashboard.py"
spec = importlib.util.spec_from_file_location("v1_dashboard_summary", dashboard_file)
v1_dashboard_summary = importlib.util.module_from_spec(spec)
sys.modules["v1_dashboard_summary"] = v1_dashboard_summary
spec.loader.exec_module(v1_dashboard_summary)


api_router = APIRouter()


api_router.include_router(content.router, prefix="/content", tags=["Content Analysis"])
api_router.include_router(dashboard_router, prefix="/dashboard", tags=["Dashboard"])
api_router.include_router(insights_router, prefix="/dashboard/insights", tags=["Dashboard Insights"])
api_router.include_router(settings_router, prefix="/dashboard/settings", tags=["Dashboard Settings"])
api_router.include_router(categories.router, prefix="/categories", tags=["Categories"])
api_router.include_router(tracking.router, prefix="/tracking", tags=["Tracking"])
api_router.include_router(user_domain_category.router, prefix="/user-domain-category", tags=["User Domain Category"])
api_router.include_router(v1_dashboard_summary.router, prefix="/dashboard-summary", tags=["Dashboard Summary"])



@api_router.get("/ping")
async def ping():
    """Simple API health check"""
    return {"message": "pong", "api_version": "v1"}
