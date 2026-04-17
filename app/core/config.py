# core/settings.py
from typing import Literal
from pydantic_settings import BaseSettings


def _parse_cors_origins(value: str) -> list[str]:
    """Parse comma-separated CORS origins into a list, no empty strings."""
    return [x.strip() for x in value.split(",") if x.strip()]


class Settings(BaseSettings):
    ALLOWED_ORIGINS: str = "http://localhost:3000"
    SECRET_KEY: str = "your-secret-key-here" 
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 30

    # Google OAuth
    GOOGLE_CLIENT_ID: str 
    GOOGLE_CLIENT_SECRET: str 
    GOOGLE_REDIRECT_URI: str 
    FRONTEND_URL: str = "http://localhost:3000"
    SESSION_SECRET_KEY: str = "change-me-in-production"
    ADMIN_EMAIL: str = "[EMAIL_ADDRESS]"

    # default uses asyncpg driver; override in .env in production
    EMAIL_HOST: str = "smtp.example.com"
    EMAIL_PORT: int = 587
    EMAIL_USER: str = "your_email@example.com"
    EMAIL_PASSWORD: str = "your_email_password"
    EMAIL_FROM: str = "your_email@example.com"
    # Cloudinary
    CLOUDINARY_CLOUD_NAME: str
    CLOUDINARY_API_KEY: str
    CLOUDINARY_API_SECRET: str
    # Comma-separated list of allowed frontend origins, e.g. https://myapp.vercel.app,https://myapp.com
    CORS_ORIGINS: str = (
        "http://localhost:3000,http://127.0.0.1:3000,http://localhost:5173,http://127.0.0.1:5173,https://gdg-website-topaz-rho.vercel.app"
    )
    # Set to False in local .env for cookies over HTTP
    COOKIE_SECURE: bool = True
    # Set to 'lax' in local .env (HTTP). Must be 'none' in production (HTTPS cross-site).
    COOKIE_SAMESITE: Literal["lax", "strict", "none"] = "none"
    DEBUG: bool = False
    DATABASE_URL: str = "ppostgresql+asyncpg://postgres:maryjesu99@localhost:5432/gdg_db"

    model_config = {"env_file": ".env", "extra": "allow"}

    @property
    def cors_origins_list(self) -> list[str]:
        return _parse_cors_origins(self.CORS_ORIGINS)

    @property
    def allowed_origins_list(self) -> list[str]:
        return [origin.strip() for origin in self.ALLOWED_ORIGINS.split(",")]

    @property
    def cookie_samesite(self) -> str:
        """Returns COOKIE_SAMESITE from env. Always lowercased for browser compatibility."""
        return self.COOKIE_SAMESITE.lower()

settings = Settings()
