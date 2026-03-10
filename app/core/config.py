# core/settings.py
from pydantic_settings import BaseSettings


def _parse_cors_origins(value: str) -> list[str]:
    """Parse comma-separated CORS origins into a list, no empty strings."""
    return [x.strip() for x in value.split(",") if x.strip()]


class Settings(BaseSettings):
    SECRET_KEY: str = "your-secret-key-here"  # override with environment variables in prod
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 30
    ADMIN_EMAIL: str = "admin@example.com"

    ADMIN_PASSWORD: str = "Admin123tyu"
    # default uses asyncpg driver; override in .env in production
    EMAIL_HOST: str = "smtp.example.com"
    EMAIL_PORT: int = 587
    EMAIL_USER: str = "your_email@example.com"
    EMAIL_PASSWORD: str = "your_email_password"
    EMAIL_FROM: str = "your_email@example.com"
    # Comma-separated list of allowed frontend origins, e.g. https://myapp.vercel.app,https://myapp.com
    CORS_ORIGINS: str = (
        "http://localhost:3000,http://127.0.0.1:3000,http://localhost:5173,http://127.0.0.1:5173,"
        "https://gdg-website-llgf.vercel.app,https://gdg-website-llgf-solomons-projects-5010d5f5.vercel.app"
    )
    DEBUG: bool = False
    DATABASE_URL: str = "ppostgresql+asyncpg://postgres:maryjesu99@localhost:5432/gdg_db"

    model_config = {"env_file": ".env", "extra": "allow"}

    @property
    def cors_origins_list(self) -> list[str]:
        return _parse_cors_origins(self.CORS_ORIGINS)


settings = Settings()
