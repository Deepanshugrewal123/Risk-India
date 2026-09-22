"""
RISK // INDIA — Database Engine & Session Management
====================================================
Provides dual-backend database abstraction supporting:
1. Development & CI: Local SQLite with `check_same_thread=False`
2. Production: PostgreSQL 16 via `psycopg` driver with connection pooling
   (pre-ping liveness, pool sizing, max overflow, and connection recycling).
"""

from typing import Generator, Optional, Dict, Any
from sqlalchemy import create_engine, Engine
from sqlalchemy.orm import declarative_base, sessionmaker, Session
from sqlalchemy.pool import QueuePool

from app.config import settings


def create_app_engine(database_url: Optional[str] = None, echo: bool = False) -> Engine:
    """
    Constructs a production-safe SQLAlchemy Engine based on database dialect.
    """
    url = database_url or settings.DATABASE_URL
    is_sqlite = url.startswith("sqlite")
    is_postgres = url.startswith("postgres")

    connect_args: Dict[str, Any] = {}
    engine_kwargs: Dict[str, Any] = {
        "echo": echo
    }

    if is_sqlite:
        # SQLite specific threading configuration
        connect_args["check_same_thread"] = False
        engine_kwargs["connect_args"] = connect_args
    elif is_postgres:
        # PostgreSQL production connection pooling
        engine_kwargs["poolclass"] = QueuePool
        engine_kwargs["pool_size"] = settings.DB_POOL_SIZE
        engine_kwargs["max_overflow"] = settings.DB_MAX_OVERFLOW
        engine_kwargs["pool_timeout"] = settings.DB_POOL_TIMEOUT
        engine_kwargs["pool_recycle"] = settings.DB_POOL_RECYCLE
        engine_kwargs["pool_pre_ping"] = True

    return create_engine(url, **engine_kwargs)


# Global application engine bound to configured DATABASE_URL
engine = create_app_engine()

# Thread-local session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Declarative ORM base
Base = declarative_base()


def get_db() -> Generator[Session, None, None]:
    """
    FastAPI dependency yielding a thread-safe SQLAlchemy database session,
    guaranteeing deterministic teardown and connection release.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
