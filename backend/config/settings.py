import os

class Settings:
    """
    Centralized HydroGrow AI Environment & Security Settings Loader.
    Provides backward compatibility for local dev & SQLite unit tests while
    enforcing production security requirements.
    """

    def __init__(self):
        self.API_ENV = os.getenv("API_ENV", "development").lower()
        self.DEBUG = os.getenv("DEBUG", "true").lower() == "true"
        
        # Database URL with fallback for local dev / testing
        self.DATABASE_URL = os.getenv(
            "DATABASE_URL", 
            "postgresql://postgres:123456@localhost:5432/hydrogrow"
        )
        
        # Security & JWT
        self.JWT_SECRET_KEY = os.getenv(
            "JWT_SECRET_KEY", 
            "hydrogrow_super_secret_jwt_key_2026_production"
        )
        self.JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
        self.ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "1440"))
        
        # CORS Origins parsing
        raw_cors = os.getenv("CORS_ORIGINS", "http://localhost:3000,http://localhost:5173,http://localhost:80,http://127.0.0.1:3000")
        self.CORS_ORIGINS = [origin.strip() for origin in raw_cors.split(",") if origin.strip()]
        
        # Storage & ML Models
        self.MODEL_PATH = os.getenv("MODEL_PATH", "backend/ml/models/saved/growth_model.joblib")
        self.STORAGE_PROVIDER = os.getenv("STORAGE_PROVIDER", "local")

    @property
    def IS_PRODUCTION(self) -> bool:
        return self.API_ENV == "production"

    def validate_settings(self) -> dict:
        errors = []
        if self.IS_PRODUCTION:
            if "super_secret" in self.JWT_SECRET_KEY.lower():
                errors.append("Production warning: Default JWT_SECRET_KEY is in use.")
            if "postgres:123456" in self.DATABASE_URL:
                errors.append("Production warning: Default local database credentials in DATABASE_URL.")

        return {
            "valid": len(errors) == 0,
            "warnings": errors,
            "environment": self.API_ENV,
            "database_configured": bool(self.DATABASE_URL),
            "cors_count": len(self.CORS_ORIGINS)
        }

settings = Settings()
