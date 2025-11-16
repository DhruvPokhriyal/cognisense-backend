"""
API v1 Main Router
Aggregates all v1 endpoint routers
"""

import importlib.util
import sys
from fastapi import APIRouter
from loguru import logger

# Import routers
from app.api.v1 import content
from app.api.v1.dashboard.dashboard import router as dashboard_router
from app.api.v1.dashboard.insights import router as insights_router
from app.api.v1.dashboard.settings import router as settings_router
from app.api.v1 import tracking, categories, user_domain_category

# Import the top-level dashboard.py file (avoiding conflict with dashboard/ package)
# We need to import it specifically since there's a name conflict
from pathlib import Path
dashboard_file = Path(__file__).parent / "dashboard.py"
spec = importlib.util.spec_from_file_location("v1_dashboard_summary", dashboard_file)
v1_dashboard_summary = importlib.util.module_from_spec(spec)
sys.modules["v1_dashboard_summary"] = v1_dashboard_summary
spec.loader.exec_module(v1_dashboard_summary)

# Optional auth import
try:
    from app.api.v1.auth import auth
    AUTH_AVAILABLE = True
except ImportError as e:
    logger.warning(f"Auth module disabled due to missing dependencies: {e}")
    AUTH_AVAILABLE = False
# from app.api.v1 import tracking, categories, dashboard  # TODO: Create these
api_router = APIRouter()

# Include sub-routers
api_router.include_router(content.router, prefix="/content", tags=["Content Analysis"])
api_router.include_router(dashboard_router, prefix="/dashboard", tags=["Dashboard"])
api_router.include_router(insights_router, prefix="/dashboard/insights", tags=["Dashboard Insights"])
api_router.include_router(settings_router, prefix="/dashboard/settings", tags=["Dashboard Settings"])
api_router.include_router(categories.router, prefix="/categories", tags=["Categories"])
api_router.include_router(tracking.router, prefix="/tracking", tags=["Tracking"])
api_router.include_router(user_domain_category.router, prefix="/user-domain-category", tags=["User Domain Category"])
# Include top-level v1 dashboard endpoints (summary/sites) as a separate tag
api_router.include_router(v1_dashboard_summary.router, prefix="/dashboard-summary", tags=["Dashboard Summary"])

# Include auth router if available
if AUTH_AVAILABLE:
    api_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])
# api_router.include_router(tracking.router, prefix="/tracking", tags=["Tracking"])  # TODO
# api_router.include_router(categories.router, prefix="/categories", tags=["Categories"])  # TODO
# api_router.include_router(dashboard.router, prefix="/dashboard", tags=["Dashboard"])  # TODO


@api_router.get("/ping")
async def ping():
    """Simple API health check"""
    return {"message": "pong", "api_version": "v1"}
