import os
from typing import List, Optional
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    APP_NAME: str = "risk-india-api"
    APP_ENV: str = "development"
    DEBUG: bool = True
    PORT: int = 8000
    WEB_CONCURRENCY: int = 4
    LOG_LEVEL: str = "INFO"

    # Database Configuration (Development: SQLite, Production: PostgreSQL 16 via psycopg)
    DATABASE_URL: str = "sqlite:///./risk_india.db"
    DB_POOL_SIZE: int = 10
    DB_MAX_OVERFLOW: int = 20
    DB_POOL_TIMEOUT: int = 30
    DB_POOL_RECYCLE: int = 1800

    # Cache Configuration (Graceful Fallback to In-Memory if Redis is Unconfigured/Unavailable)
    REDIS_URL: Optional[str] = None
    CACHE_BACKEND: str = "memory"
    CACHE_TTL_SECONDS: int = 300

    # CORS Whitelist: Explicit origins only; wildcard '*' strictly forbidden with allow_credentials=True
    CORS_ORIGINS: str = (
        "http://localhost:5173,"
        "http://127.0.0.1:5173,"
        "http://localhost:5174,"
        "http://127.0.0.1:5174,"
        "http://localhost:5175,"
        "http://127.0.0.1:5175,"
        "http://localhost:3000"
    )

    # Security & Abuse Controls
    SECRET_KEY: str = "dev-insecure-secret-key-risk-india-local-only-32chars"
    ENABLE_HSTS: bool = False
    RATE_LIMIT_GENERAL: int = 60
    RATE_LIMIT_COMPUTE: int = 10

    model_config = SettingsConfigDict(
        env_file=os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env"),
        env_file_encoding="utf-8",
        extra="ignore"
    )

    @property
    def is_sqlite(self) -> bool:
        return self.DATABASE_URL.startswith("sqlite")

    @property
    def is_postgres(self) -> bool:
        return self.DATABASE_URL.startswith("postgres")

    @property
    def cors_origin_list(self) -> List[str]:
        """
        Parses comma-separated origins and strictly filters out wildcard '*'
        to prevent insecure CORS configurations when credentials are enabled.
        """
        origins = []
        for origin in self.CORS_ORIGINS.split(","):
            cleaned = origin.strip()
            if cleaned and cleaned != "*":
                origins.append(cleaned)
        return origins


settings = Settings()
