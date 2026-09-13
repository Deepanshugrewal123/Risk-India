from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import logging

from app.config import settings
from app.api.router import api_router
from app.database.database import engine, Base, SessionLocal
from app.database.init_db import auto_seed_database

# Setup logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("risk-india-api")

# Ensure tables exist on startup and seed initial locations if empty
Base.metadata.create_all(bind=engine)
with SessionLocal() as db_session:
    auto_seed_database(db_session)

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
    openapi_url="/openapi.json"
)

# Configure CORS for local development & frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origin_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global Exception Handler for structured JSON errors
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled server exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal Server Error",
            "detail": "An unexpected error occurred in the risk intelligence service.",
            "type": exc.__class__.__name__
        }
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
