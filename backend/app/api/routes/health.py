from fastapi import APIRouter
from fastapi.responses import JSONResponse
from sqlalchemy import text
from datetime import datetime, timezone

from app.config import settings
from app.database.database import engine
from app.services.flood_model_service import flood_model_service
from app.services.cache_service import cache_service
from app.services.disaster_provider import disaster_feed_manager
from app.services.metrics_service import metrics_collector
from app.services.config_validator import config_validator

router = APIRouter(tags=["Health"])


@router.get("/health", summary="Overall system health check")
def health_check():
    """
    Comprehensive health check verifying backend, cache, database, and upstream telemetry providers.
    """
    provider_health = disaster_feed_manager.get_health()
    all_providers_healthy = all(
        p.get("status") in ["healthy", "operational", "uninitialized"]
        for p in provider_health.values()
    )

    db_connected = False
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
            db_connected = True
    except Exception:
        db_connected = False

    is_overall_ok = all_providers_healthy and db_connected and flood_model_service.is_ready

    return {
        "status": "ok" if is_overall_ok else "degraded",
        "service": "risk-india-api",
        "database": "connected" if db_connected else "disconnected",
        "model_ready": flood_model_service.is_ready,
        "cache": cache_service.backend_name,
        "providers": provider_health
    }


@router.get("/health/liveness", summary="Application process liveness probe")
def liveness_check():
    """
    Confirms the application process is running and responding to HTTP traffic.
    Strictly isolated: does NOT depend on external APIs, network feeds, or database connections.
    """
    return {
        "status": "alive",
        "service": "risk-india-api",
        "timestamp": datetime.now(timezone.utc).isoformat()
    }


@router.get("/health/readiness", summary="Service dependency readiness probe")
def readiness_check():
    """
    Validates essential operational dependencies before accepting production traffic:
    - Primary Database connectivity (SELECT 1 ping)
    - ML Inference engine availability
    - Cache subsystem availability
    Temporary upstream disaster provider outages do NOT fail readiness, preserving local resilience.
    """
    db_connected = False
    db_error = None
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
            db_connected = True
    except Exception as e:
        db_connected = False
        db_error = "Database connectivity check failed"
        metrics_collector.record_db_error()

    model_ready = flood_model_service.is_ready
    cache_ready = cache_service.is_healthy()

    is_ready = db_connected and model_ready

    payload = {
        "status": "ready" if is_ready else "not_ready",
        "service": "risk-india-api",
        "database": "connected" if db_connected else "disconnected",
        "model_ready": model_ready,
        "cache": cache_service.backend_name,
        "timestamp": datetime.now(timezone.utc).isoformat()
    }

    if not is_ready:
        if db_error:
            payload["error"] = db_error
        return JSONResponse(status_code=503, content=payload)

    return payload


@router.get("/health/metrics", summary="Operational observability metrics snapshot")
def operational_metrics():
    """
    Returns sanitized, machine-readable operational metrics:
    - HTTP request distribution & latency percentiles
    - Rate limit counts
    - Upstream provider reliability & circuit breaker status
    - Cache efficiency (hits/misses/stale/offline fallback)
    - ML inference request audit
    Zero credentials, authorization headers, or PII exposed.
    """
    return metrics_collector.get_snapshot()


@router.get("/health/config", summary="Sanitized configuration audit report")
def configuration_audit():
    """
    Audits active configuration against environment rules (development/staging/production).
    Returns error/warning count and sanitized configuration. All secrets are redacted.
    """
    report = config_validator.validate(settings)
    return report.to_dict()
