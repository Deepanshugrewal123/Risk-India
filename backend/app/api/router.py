from fastapi import APIRouter
from app.api.routes import (
    health_router,
    locations_router,
    risk_router,
    disasters_router,
    resources_router
)

api_router = APIRouter(prefix="/api")

api_router.include_router(health_router)
api_router.include_router(locations_router)
api_router.include_router(risk_router)
api_router.include_router(disasters_router)
api_router.include_router(resources_router)
