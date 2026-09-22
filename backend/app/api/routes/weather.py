"""
RISK // INDIA — National Weather Intelligence REST Endpoints
=============================================================
Exposes synoptic observations, multi-horizon forecasts, official warnings,
hazard evidence feeds, provider circuit statuses, and national readiness.
"""

from typing import Optional, List, Dict, Any
from fastapi import APIRouter, Query, HTTPException, Path
from app.services.weather import (
    national_weather_service,
    weather_provider_client,
    weather_freshness_engine,
    WeatherFreshness
)

router = APIRouter(prefix="/weather", tags=["National Weather Intelligence"])


@router.get("/status")
def get_weather_status() -> Dict[str, Any]:
    """Returns operational metrics, provider circuit states, observation counts, and storage mode."""
    return national_weather_service.get_status()


@router.get("/current")
def get_current_weather(
    region: Optional[str] = Query(None, description="Administrative entity name (State/UT/District)"),
    limit: int = Query(50, ge=1, le=100, description="Max records to return")
) -> Dict[str, Any]:
    """Returns the latest validated synoptic weather observations."""
    if region:
        obs = national_weather_service.get_current_weather(region)
        if obs is None:
            raise HTTPException(status_code=404, detail=f"No weather observations available for region '{region}'")
        return {
            "region": region,
            "count": 1,
            "observations": [obs.to_dict()]
        }
    
    observations = national_weather_service.get_all_latest_observations(limit=limit)
    return {
        "count": len(observations),
        "limit": limit,
        "observations": [o.to_dict() for o in observations]
    }


@router.get("/forecast")
def get_weather_forecasts(
    region: Optional[str] = Query(None, description="Administrative entity name (State/UT/District)"),
    horizon: Optional[str] = Query(None, description="NOW, 0_6H, 6_24H, 1_3D, or 3_7D"),
    limit: int = Query(100, ge=1, le=500, description="Max records to return")
) -> Dict[str, Any]:
    """Returns multi-horizon numerical weather predictions."""
    if region:
        fcs = national_weather_service.get_forecast_timeline(region)
        if horizon:
            fcs = [f for f in fcs if f.forecast_horizon.upper() == horizon.upper()]
        return {
            "region": region,
            "horizon_filter": horizon,
            "count": len(fcs),
            "forecasts": [f.to_dict() for f in fcs]
        }
    
    forecasts = national_weather_service.get_all_forecasts(horizon=horizon, limit=limit)
    return {
        "horizon_filter": horizon,
        "count": len(forecasts),
        "limit": limit,
        "forecasts": [f.to_dict() for f in forecasts]
    }


@router.get("/warnings")
def get_weather_warnings(
    region: Optional[str] = Query(None, description="Filter by affected region name"),
    hazard: Optional[str] = Query(None, description="Filter by hazard type (CYCLONE, HEAVY_RAIN, HEATWAVE, etc.)"),
    severity: Optional[str] = Query(None, description="Filter by severity (RED, ORANGE, YELLOW, GREEN)")
) -> Dict[str, Any]:
    """Returns official meteorological alerts and bulletins."""
    warnings = national_weather_service.get_active_warnings(region_name=region)
    if hazard:
        warnings = [w for w in warnings if w.hazard.upper() == hazard.upper()]
    if severity:
        warnings = [w for w in warnings if w.severity.upper() == severity.upper()]
    return {
        "count": len(warnings),
        "region_filter": region,
        "hazard_filter": hazard,
        "severity_filter": severity,
        "warnings": [w.to_dict() for w in warnings]
    }


@router.get("/regions/{region}")
def get_region_weather_overview(
    region: str = Path(..., description="State, Union Territory, or supported district")
) -> Dict[str, Any]:
    """Comprehensive weather dossier for an administrative entity: current, forecasts, warnings, and hazard evidence."""
    obs = national_weather_service.get_current_weather(region)
    if obs is None:
        raise HTTPException(status_code=404, detail=f"Unrecognized or unmonitored region '{region}'")
    
    timeline = national_weather_service.get_forecast_timeline(region)
    warnings = national_weather_service.get_active_warnings(region)
    evidence = national_weather_service.get_hazard_evidence(region)

    return {
        "region": obs.region_name,
        "region_type": obs.region_type,
        "region_id": obs.region_id,
        "current_weather": obs.to_dict(),
        "forecast_timeline": [f.to_dict() for f in timeline],
        "active_warnings": [w.to_dict() for w in warnings],
        "hazard_evidence": evidence,
        "synthetic_records": 0
    }


@router.get("/regions/{region}/forecast")
def get_region_forecast_timeline(
    region: str = Path(..., description="State, Union Territory, or supported district")
) -> Dict[str, Any]:
    """Dedicated multi-horizon timeline for a specific region."""
    timeline = national_weather_service.get_forecast_timeline(region)
    if not timeline:
        raise HTTPException(status_code=404, detail=f"No forecast series available for region '{region}'")
    return {
        "region": region,
        "forecasts_count": len(timeline),
        "timeline": [f.to_dict() for f in timeline]
    }


@router.get("/freshness")
def get_weather_freshness_breakdown() -> Dict[str, Any]:
    """Freshness policy, SLAs, and data decay parameters."""
    return {
        "freshness_standards": {
            "OFFICIAL_LIVE": "Age <= 1 hour (Surface Synoptic Network)",
            "INTERMEDIATE_UPDATE": "Age <= 3 hours (MWR / Satellite Ingest)",
            "DAILY_BULLETIN": "Age <= 24 hours (Regional Weather Report)",
            "FORECAST_CURRENT": "Valid time window is active",
            "FORECAST_SUPERSEDED": "Valid window expired or newly superseded",
            "HISTORICAL_STALE": "Age > 24 hours (Historical Reference Only)"
        },
        "decoupling_policy": "Strict: Stale observations reduce data confidence but NEVER artificially alter hazard severity.",
        "synthetic_records_allowed": 0
    }


@router.get("/providers")
def get_weather_providers() -> Dict[str, Any]:
    """Live provider circuit breaker health, failure counts, and endpoints."""
    return {
        "providers": weather_provider_client.get_all_circuit_statuses(),
        "resilience_policy": "ISOLATED_CIRCUIT_BREAKER_WITH_IN_MEMORY_FALLBACK"
    }


@router.get("/readiness")
def get_weather_readiness() -> Dict[str, Any]:
    """National coverage probe across 28 States and 8 Union Territories."""
    return national_weather_service.get_readiness()
