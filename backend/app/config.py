# ============================================================
# config.py — App Configuration from Environment Variables
# ============================================================
# Loads values from the .env file. Never hardcode secrets!
# ============================================================

from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # MySQL connection string: mysql+pymysql://user:pass@host/dbname
    DATABASE_URL: str = "sqlite:///./fintech.db"

    # Secret key for signing JWT tokens (keep this very secret!)
    SECRET_KEY: str = "your-super-secret-key-change-this"

    # JWT algorithm
    ALGORITHM: str = "HS256"

    # How long a token stays valid (in minutes)
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    class Config:
        env_file = ".env"  # Load from .env file automatically

# Single settings instance used across the app
settings = Settings()
