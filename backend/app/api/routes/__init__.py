from .health import router as health_router
from .locations import router as locations_router
from .risk import router as risk_router
from .disasters import router as disasters_router
from .resources import router as resources_router

__all__ = [
    "health_router",
    "locations_router",
    "risk_router",
    "disasters_router",
    "resources_router",
]
