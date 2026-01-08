# from pydantic_settings import BaseSettings
# from pydantic import ConfigDict

# class Settings(BaseSettings):
#     DATABASE_URL: str
#     SECRET_KEY: str
#     ALGORITHM: str = "HS256"
#     ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

#     model_config = ConfigDict(env_file=".env", extra='ignore')

# settings = Settings()

# core/settings.py
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    SECRET_KEY: str = "supersecretkey"  # override with environment variables in prod
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 30
    # Add more global settings here
    DATABASE_URL: str = "postgresql://postgres:maryjesu99@localhost:5432/gdg_backend"


# singleton to import everywhere
settings = Settings()
