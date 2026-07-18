from fastapi import APIRouter

router = APIRouter()

@router.get("/health", summary="Get API Health Status")
async def health_check():
    """
    Check the health and operational status of the HydroGrow AI Backend API.
    Returns basic service identification and uptime status.
    """
    return {
        "status": "running",
        "service": "HydroGrow AI API",
        "version": "1.0.0"
    }
