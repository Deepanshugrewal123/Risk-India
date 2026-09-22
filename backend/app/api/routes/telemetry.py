"""
RISK // INDIA — Catchment Telemetry Stream REST Endpoints
=========================================================
Exposes authoritative hydrological telemetry feeds, canonical gauge directories,
subsystem operational status, and basin readiness probes.
"""

from typing import Optional, List, Dict, Any
from fastapi import APIRouter, Query, HTTPException
from app.services.telemetry import (
    dynamic_telemetry_service,
    catchment_gauge_registry
)

router = APIRouter(prefix="/telemetry", tags=["Catchment Telemetry"])


@router.get("/status")
def get_telemetry_status() -> Dict[str, Any]:
    """Returns operational health, provider circuit states, observation counts, and freshness metrics."""
    return dynamic_telemetry_service.get_status()


@router.get("/gauges")
def get_canonical_gauges(
    basin: Optional[str] = Query(None, description="Filter by river basin ID (e.g. godavari, mahanadi, brahmaputra)"),
    state: Optional[str] = Query(None, description="Filter by state or UT name"),
    status: Optional[str] = Query(None, description="Filter by status (e.g. ACTIVE_CALIBRATED, UNMAPPED)")
) -> Dict[str, Any]:
    """Returns canonical river basin gauge stations with geographic and hydraulic metadata."""
    gauges = dynamic_telemetry_service.get_gauges(basin=basin, state=state, status=status)
    return {
        "count": len(gauges),
        "basin_filter": basin,
        "state_filter": state,
        "status_filter": status,
        "gauges": gauges
    }


@router.get("/observations")
def get_hydrological_observations(
    gauge_id: Optional[str] = Query(None, description="Station ID (e.g. CWC-GD-001)"),
    basin: Optional[str] = Query(None, description="Basin ID"),
    state: Optional[str] = Query(None, description="State or UT"),
    variable_type: Optional[str] = Query(None, description="WATER_LEVEL, RAINFALL, or DISCHARGE"),
    limit: int = Query(100, ge=1, le=1000, description="Max observations to return")
) -> Dict[str, Any]:
    """Returns chronological hydrological telemetry stream with provenance and normalized units."""
    obs = dynamic_telemetry_service.get_observations(
        gauge_id=gauge_id,
        basin=basin,
        state=state,
        variable_type=variable_type,
        limit=limit
    )
    return {
        "count": len(obs),
        "gauge_id": gauge_id,
        "basin": basin,
        "state": state,
        "variable_type": variable_type,
        "observations": [o.to_dict() for o in obs]
    }


@router.get("/readiness")
def get_telemetry_readiness() -> Dict[str, Any]:
    """Basin-by-basin telemetry readiness assessment for downstream empirical modeling."""
    return dynamic_telemetry_service.get_readiness()
