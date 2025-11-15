"""
CogniSense Backend - Digital Footprint Tracking & Analysis
Main FastAPI application entry point
"""

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.core.logging import setup_logging
from app.ml.model_manager import ModelManager
from app.api.v1.router import api_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan manager - handles startup and shutdown events
    """
    # Startup: Load ML models into memory
    setup_logging()
    model_manager = ModelManager()
    await model_manager.load_models()
    
    yield  # Application runs
    
    # Shutdown: Cleanup if needed
    # (Models will be garbage collected automatically)


app = FastAPI(
    title="CogniSense API",
    description="API for tracking and analyzing digital footprint",
    version="1.0.0",
    lifespan=lifespan,
)

# Configure CORS for browser extension
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routers
app.include_router(api_router, prefix="/api/v1")


@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "CogniSense Backend",
        "version": "1.0.0"
    }


@app.get("/health")
async def health_check():
    """Detailed health check with ML model status"""
    model_manager = ModelManager()
    return {
        "status": "healthy",
        "database": "connected",  # TODO: Add actual DB health check
        "ml_models_loaded": model_manager.is_loaded(),
    }
