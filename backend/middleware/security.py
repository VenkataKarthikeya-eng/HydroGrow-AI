import time
import logging
from fastapi import Request, Response
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from backend.config.settings import settings

logger = logging.getLogger("hydrogrow.security")

class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    """
    Middleware injecting production security headers on all HTTP responses.
    """
    async def dispatch(self, request: Request, call_next):
        response: Response = await call_next(request)
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        response.headers["Content-Security-Policy"] = "default-src 'self' 'unsafe-inline' 'unsafe-eval' data: blob: https:;"
        return response

class RequestLoggingMiddleware(BaseHTTPMiddleware):
    """
    Middleware logging incoming API requests, HTTP status codes, and execution latency.
    """
    async def dispatch(self, request: Request, call_next):
        t0 = time.time()
        response: Response = await call_next(request)
        duration_ms = round((time.time() - t0) * 1000.0, 2)
        
        # Log non-health requests
        if request.url.path not in ["/health", "/favicon.ico"]:
            logger.info(f"{request.method} {request.url.path} -> {response.status_code} ({duration_ms}ms)")
            
        return response

async def global_exception_handler(request: Request, exc: Exception):
    """
    Production-safe global exception handler.
    Prevents credentials or internal stack traces from leaking in API responses.
    """
    logger.error(f"Unhandled exception on {request.method} {request.url.path}: {str(exc)}")
    
    if settings.IS_PRODUCTION:
        return JSONResponse(
            status_code=500,
            content={"detail": "An internal server error occurred. Please contact system administrator."}
        )
    return JSONResponse(
        status_code=500,
        content={"detail": str(exc), "path": request.url.path}
    )
