from fastapi import APIRouter
from app.services.disaster_provider import disaster_feed_manager

router = APIRouter()

@router.get("/health", tags=["Health"])
def health_check():
    """
    Health check endpoint verifying backend and upstream provider operational readiness.
    """
    provider_health = disaster_feed_manager.get_health()
    all_healthy = all(
        p.get("status") in ["healthy", "operational", "uninitialized"]
        for p in provider_health.values()
    )
    return {
        "status": "ok" if all_healthy else "degraded",
        "service": "risk-india-api",
        "providers": provider_health
    }
