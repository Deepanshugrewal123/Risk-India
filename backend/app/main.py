from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import logging

from app.config import settings
from app.api.router import api_router
from app.database.database import engine, Base, SessionLocal
from app.database.init_db import auto_seed_database
from app.middleware.logger import CorrelationIdMiddleware, StructuredLoggingMiddleware
from app.middleware.security import SecurityHeadersMiddleware
from app.middleware.rate_limit import RateLimitMiddleware

from contextlib import asynccontextmanager
from app.services.cache_service import cache_service

# Setup logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("risk-india-api")

# Ensure tables exist on startup and seed initial locations if in development mode.
# In production, schema migrations are managed explicitly via Alembic (alembic upgrade head).
if settings.is_sqlite or getattr(settings, "APP_ENV", "development").lower() != "production":
    Base.metadata.create_all(bind=engine)
    with SessionLocal() as db_session:
        auto_seed_database(db_session)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan context manager managing startup and graceful shutdown.
    Ensures connection pool disposal and cache socket cleanup on termination.
    """
    logger.info("RISK // INDIA API lifecycle starting up...")
    try:
        if settings.is_sqlite or getattr(settings, "APP_ENV", "development").lower() != "production":
            Base.metadata.create_all(bind=engine)
            with SessionLocal() as db_session:
                auto_seed_database(db_session)
    except Exception as e:
        logger.warning(f"Database startup check warning: {e}")
    yield
    logger.info("RISK // INDIA API graceful shutdown initiated...")
    try:
        engine.dispose()
        logger.info("Database connection pool cleanly disposed.")
    except Exception as e:
        logger.warning(f"Error disposing database engine: {e}")
    try:
        cache_service.close()
        logger.info("Cache service connections closed.")
    except Exception as e:
        logger.warning(f"Error closing cache service: {e}")


app = FastAPI(
    title="RISK // INDIA API",
    description=(
        "Backend foundation for RISK // INDIA — AI-Powered Disaster Risk Analyzer & Management System. "
        "Provides REST endpoints for Indian administrative locations, multi-hazard risk assessments, "
        "incident telemetry, and verified relief resources."
    ),
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    lifespan=lifespan
)


# -----------------------------------------------------------------------------
# Middleware Stack (Execution Order: Top-level wrapper executes first on request)
# -----------------------------------------------------------------------------
# Innermost to outermost:
# 5. RateLimiting: checks rate limits closest to endpoint execution
app.add_middleware(RateLimitMiddleware)

# 4. CORS: handles preflight OPTIONS & sets CORS headers
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origin_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 3. Security Headers: injects nosniff, DENY, CSP, HSTS onto all responses
app.add_middleware(SecurityHeadersMiddleware)

# 2. Structured Logging: measures latency and logs structured JSON without credentials
app.add_middleware(StructuredLoggingMiddleware)

# 1. Request Correlation: ensures every request has a validated X-Request-ID (outermost)
app.add_middleware(CorrelationIdMiddleware)


# Global Exception Handler for structured, sanitized JSON errors
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    request_id = getattr(request.state, "request_id", None) or request.headers.get("x-request-id") or "untracked"
    logger.error(f"Unhandled exception [request_id={request_id}]: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal Server Error",
            "detail": "An unexpected error occurred in the risk intelligence service.",
            "request_id": request_id
        },
        headers={"X-Request-ID": request_id}
    )


# Mount API routes
app.include_router(api_router)


@app.get("/", tags=["Root"])
def root():
    return {
        "project": "RISK // INDIA",
        "description": "AI-Powered Disaster Risk Analyzer & Management System",
        "status": "online",
        "docs": "/docs",
        "health": "/api/health"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="127.0.0.1", port=settings.PORT, reload=True)
