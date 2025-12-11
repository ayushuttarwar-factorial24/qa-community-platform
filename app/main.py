"""
Main FastAPI Application

Entry point for the QA Community Profile Matching Platform API.
Configures FastAPI app, middleware, routes, and lifecycle events.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import logging

from app.config import settings
from app.repo.profile_repo import profile_repository
from app.routers import profiles_router


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan context manager for application startup and shutdown.
    
    Handles:
    - Database connection on startup
    - Database disconnection on shutdown
    """
    # Startup
    logger.info("Starting QA Community Profile Matching Platform API")
    logger.info(f"Version: {settings.app_version}")
    
    try:
        await profile_repository.connect()
        logger.info("Database connected successfully")
    except Exception as e:
        logger.error(f"Failed to connect to database: {e}")
        raise
    
    yield
    
    # Shutdown
    logger.info("Shutting down application")
    await profile_repository.disconnect()
    logger.info("Database disconnected")


# Create FastAPI application
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description=(
        "API for the QA Community Profile Matching Platform. "
        "Connects QA professionals based on skill alignment and learning goals."
    ),
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)


# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Include routers
app.include_router(profiles_router)


@app.get(
    "/",
    tags=["health"],
    summary="Root endpoint",
    description="Returns API status and version information"
)
async def root():
    """
    Root endpoint - API health check and info.
    
    Returns basic information about the API.
    """
    return {
        "name": settings.app_name,
        "version": settings.app_version,
        "status": "running",
        "docs": "/docs"
    }


@app.get(
    "/health",
    tags=["health"],
    summary="Health check",
    description="Health check endpoint for monitoring"
)
async def health_check():
    """
    Health check endpoint.
    
    Can be extended to check database connectivity and other dependencies.
    """
    return {
        "status": "healthy",
        "version": settings.app_version
    }


if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "app.main:app",
        host=settings.api_host,
        port=settings.api_port,
        reload=settings.api_reload
    )
