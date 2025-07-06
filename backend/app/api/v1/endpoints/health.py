from fastapi import APIRouter
from typing import Dict, Any

router = APIRouter()


@router.get("/")
async def health_check() -> Dict[str, Any]:
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "research-assistant-api",
        "version": "1.0.0"
    }


@router.get("/detailed")
async def detailed_health_check() -> Dict[str, Any]:
    """Detailed health check with service dependencies"""
    # TODO: Add actual health checks for databases
    return {
        "status": "healthy",
        "services": {
            "api": "healthy",
            "database": "healthy",
            "redis": "healthy",
            "elasticsearch": "healthy"
        }
    } 