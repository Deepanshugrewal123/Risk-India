from fastapi import APIRouter
from app.api.routes import (
    health_router,
    locations_router,
    risk_router,
    disasters_router,
    resources_router,
    data_foundation_router,
    national_risk_router,
    future_risk_router,
    telemetry_router,
    weather_router,
    crisis_router,
    predictive_risk_router
)

api_router = APIRouter(prefix="/api")

api_router.include_router(health_router)
api_router.include_router(locations_router)
api_router.include_router(risk_router)
api_router.include_router(disasters_router)
api_router.include_router(resources_router)
api_router.include_router(data_foundation_router)
api_router.include_router(national_risk_router)
api_router.include_router(future_risk_router)
api_router.include_router(telemetry_router)
api_router.include_router(weather_router)
api_router.include_router(crisis_router)
api_router.include_router(predictive_risk_router)
