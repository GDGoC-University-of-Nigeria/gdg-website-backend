# core/settings.py
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    SECRET_KEY: str = "your-secret-key-here"  # override with environment variables in prod
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 30
    ADMIN_EMAIL: str = "admin@example.com"

    ADMIN_PASSWORD: str = "Admin123tyu"
    # default uses asyncpg driver; override in .env in production
    EMAIL_HOST:str = "smtp.example.com"
    EMAIL_PORT: int = 587
    EMAIL_USER:str = "your_email@example.com"
    EMAIL_PASSWORD:str = "your_email_password"
    EMAIL_FROM:str = "your_email@example.com"
    CORS_ORIGINS:str = "http://localhost:3000"
    DEBUG: bool = False
    DATABASE_URL: str = "postgresql+asyncpg://postgres:maryjesu99@localhost:5432/gdg_db"

    model_config = {"env_file": ".env", "extra": "allow"}


settings = Settings()
