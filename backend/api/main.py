import sys
import os
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

# Add the project root folder to Python path to ensure proper module resolution
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.normpath(os.path.join(BASE_DIR, "..", ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from backend.api import health_routes, prediction_routes, assistant_routes, auth_routes, history_routes, analytics_routes, iot_routes, websocket_routes, automation_routes, vision_routes, digital_twin_routes, autonomous_routes, ml_routes, system_routes, cloud_routes, farm_routes, member_routes, greenhouse_routes, marketplace_routes, community_routes, expert_routes, template_routes, intelligence_routes
from backend.database.connection import engine
from backend.database import models
from backend.config.settings import settings
from backend.middleware.security import SecurityHeadersMiddleware, RequestLoggingMiddleware, global_exception_handler

# Auto-create tables on application startup
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="HydroGrow AI Backend API",
    description="Enterprise AI-powered hydroponic farming platform",
    version="1.0.0"
)

# Enable CORS using production settings
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS if settings.CORS_ORIGINS else ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Attach security & logging middleware
app.add_middleware(SecurityHeadersMiddleware)
app.add_middleware(RequestLoggingMiddleware)
app.add_exception_handler(Exception, global_exception_handler)

# Custom exception handler for validation errors to ensure professional format
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    details = exc.errors()
    detail_messages = []
    for detail in details:
        loc = " -> ".join(str(l) for l in detail.get("loc", []))
        msg = detail.get("msg", "")
        detail_messages.append(f"{loc}: {msg}")
    
    return JSONResponse(
        status_code=422,
        content={
            "error": True,
            "message": "Validation failed",
            "details": "; ".join(detail_messages)
        }
    )

# Root Health endpoint
@app.get("/health", summary="Production System Health Check")
def get_health_check():
    return {
        "status": "healthy",
        "database": "connected",
        "service": "HydroGrow AI API",
        "version": "1.0"
    }

# Include routers
app.include_router(health_routes.router)
app.include_router(prediction_routes.router)
app.include_router(assistant_routes.router)
app.include_router(auth_routes.router)
app.include_router(history_routes.router)
app.include_router(analytics_routes.router, prefix="/api/analytics")
app.include_router(iot_routes.router, prefix="/api/iot")
app.include_router(websocket_routes.router)
app.include_router(automation_routes.router, prefix="/api/automation")
app.include_router(automation_routes.crops_router, prefix="/api/crops")
app.include_router(vision_routes.router, prefix="/api/vision")
app.include_router(digital_twin_routes.router, prefix="/api/twin")
app.include_router(autonomous_routes.router, prefix="/api/copilot")
app.include_router(ml_routes.router, prefix="/api/ml")
app.include_router(system_routes.router, prefix="/api/system")
app.include_router(cloud_routes.router, prefix="/api")
app.include_router(farm_routes.router, prefix="/api")
app.include_router(member_routes.router, prefix="/api")
app.include_router(greenhouse_routes.router, prefix="/api")
app.include_router(marketplace_routes.router, prefix="/api")
app.include_router(community_routes.router, prefix="/api")
app.include_router(expert_routes.router, prefix="/api")
app.include_router(template_routes.router, prefix="/api")
app.include_router(intelligence_routes.router, prefix="/api")
