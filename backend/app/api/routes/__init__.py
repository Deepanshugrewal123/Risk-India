from .health import router as health_router
from .locations import router as locations_router
from .risk import router as risk_router
from .disasters import router as disasters_router
from .resources import router as resources_router
from .data_foundation import router as data_foundation_router
from .national_risk import router as national_risk_router
from .future_risk import router as future_risk_router
from .telemetry import router as telemetry_router
from .weather import router as weather_router
from .crisis import router as crisis_router
from .predictive_risk import router as predictive_risk_router

__all__ = [
    "health_router",
    "locations_router",
    "risk_router",
    "disasters_router",
    "resources_router",
    "data_foundation_router",
    "national_risk_router",
    "future_risk_router",
    "telemetry_router",
    "weather_router",
    "crisis_router",
    "predictive_risk_router",
]
