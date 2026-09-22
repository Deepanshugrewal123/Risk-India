from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional, Dict, Any

from app.database.database import get_db
from app.schemas.disaster import DisasterEventOut
from app.services.disaster_service import disaster_service

router = APIRouter(prefix="/disasters", tags=["Disaster Incidents"])

@router.get("", response_model=List[DisasterEventOut], summary="List monitored disaster events with filters")
def get_disasters(
    state: Optional[str] = Query(None, description="Filter by state or UT name/code (e.g. 'assam', 'AS')"),
    type: Optional[str] = Query(None, description="Filter by hazard type (e.g. 'flood', 'cyclone', 'earthquake')"),
    status: Optional[str] = Query(None, description="Filter by status (e.g. 'active', 'monitoring', 'warning')"),
    freshness: Optional[str] = Query(None, description="Filter by freshness ('LIVE', 'RECENT', 'STALE')"),
    live_only: bool = Query(False, description="If True, returns only verified live/recent events"),
    db: Session = Depends(get_db)
):
    """
    Retrieve disaster events and alerts. Supports filtering by state, hazard type, status, and freshness.
    """
    return disaster_service.get_disasters(
        db=db,
        state=state,
        disaster_type=type,
        status=status,
        freshness=freshness,
        live_only=live_only
    )

@router.get("/live", response_model=List[DisasterEventOut], summary="List verified live and recent disaster events")
def get_live_disasters(
    state: Optional[str] = Query(None, description="Filter by state or UT name/code"),
    type: Optional[str] = Query(None, description="Filter by hazard type")
):
    """
    Retrieve specifically verified live and recent disaster events from authoritative feeds.
    Excludes unverified simulation/demo records.
    """
    return disaster_service.get_live_disasters(state=state, disaster_type=type)

@router.get("/refresh", summary="Trigger manual cache refresh from upstream disaster feeds")
def refresh_disasters():
    """
    Forces a cache invalidation and queries live upstream feeds (with rate-limiting guard).
    """
    return disaster_service.refresh()

@router.get("/providers", summary="List authoritative disaster providers and operational tiers")
def get_disaster_providers():
    """
    Returns the audited catalog of authoritative disaster telemetry and bulletin providers.
    Includes data tiers: LIVE_API, PUBLIC_WEB_DATA, AUTHENTICATED_API, DOWNLOADABLE_DATA.
    """
    from app.services.disaster_provider import disaster_feed_manager
    return {
        "count": len(disaster_feed_manager.get_provider_catalog()),
        "providers": disaster_feed_manager.get_provider_catalog(),
        "health": disaster_feed_manager.get_health()
    }

@router.get("/status", summary="Operational telemetry and composite status of disaster feeds")
def get_disasters_feed_status():
    """
    Provides real-time telemetry on the disaster incident feed, including event counts,
    freshness breakdown (LIVE, RECENT, STALE), and deduplication statistics.
    """
    from app.services.disaster_provider import disaster_feed_manager
    return disaster_feed_manager.get_feed_status()

# -----------------------------------------------------------------------------
# Phase 19: Dedicated Multi-Hazard Query Endpoints
# -----------------------------------------------------------------------------

@router.get("/by-hazard/{hazard}", response_model=List[DisasterEventOut], summary="List disaster events for a specific hazard")
def get_disasters_by_hazard_route(
    hazard: str,
    state: Optional[str] = Query(None, description="Optional filter by State or UT"),
    live_only: bool = Query(False, description="Filter strictly for LIVE/RECENT verified feeds")
):
    """
    Retrieve disaster events and alerts filtered by hazard taxonomy.
    Supported: FLOOD, EARTHQUAKE, CYCLONE, HEATWAVE, LANDSLIDE, SEVERE_WEATHER.
    """
    return disaster_service.get_disasters_by_hazard(hazard=hazard, state=state, live_only=live_only)

@router.get("/by-state/{state}", response_model=List[DisasterEventOut], summary="List disaster events for a specific state or UT")
def get_disasters_by_state_route(
    state: str,
    hazard: Optional[str] = Query(None, description="Optional filter by hazard type"),
    live_only: bool = Query(False, description="Filter strictly for LIVE/RECENT verified feeds")
):
    """
    Retrieve disaster events and alerts normalized to a specific Indian State or Union Territory.
    """
    return disaster_service.get_disasters_by_state(state=state, hazard=hazard, live_only=live_only)

@router.get("/flood", response_model=List[DisasterEventOut], summary="List active and monitored flood events")
def get_flood_disasters(
    state: Optional[str] = Query(None, description="Filter by state or UT"),
    live_only: bool = Query(False, description="Filter strictly for verified live/recent alerts")
):
    """Authoritative CWC river gauge warnings and catchment inundation alerts."""
    return disaster_service.get_disasters_by_hazard(hazard="FLOOD", state=state, live_only=live_only)

@router.get("/earthquake", response_model=List[DisasterEventOut], summary="List verified seismic tremor events")
def get_earthquake_disasters(
    state: Optional[str] = Query(None, description="Filter by state or UT"),
    live_only: bool = Query(False, description="Filter strictly for verified live/recent alerts")
):
    """Live subcontinental seismological feed from USGS Earthquake Hazards Program."""
    return disaster_service.get_disasters_by_hazard(hazard="EARTHQUAKE", state=state, live_only=live_only)

@router.get("/cyclone", response_model=List[DisasterEventOut], summary="List active tropical cyclone advisories")
def get_cyclone_disasters(
    state: Optional[str] = Query(None, description="Filter by state or UT"),
    live_only: bool = Query(False, description="Filter strictly for verified live/recent alerts")
):
    """Official IMD/RSMC tropical storm advisories for Bay of Bengal and Arabian Sea."""
    return disaster_service.get_disasters_by_hazard(hazard="CYCLONE", state=state, live_only=live_only)

@router.get("/heatwave", response_model=List[DisasterEventOut], summary="List official heatwave warnings")
def get_heatwave_disasters(
    state: Optional[str] = Query(None, description="Filter by state or UT"),
    live_only: bool = Query(False, description="Filter strictly for verified live/recent alerts")
):
    """Official IMD and NDMA Heat Wave Action Plan temperature anomaly advisories."""
    return disaster_service.get_disasters_by_hazard(hazard="HEATWAVE", state=state, live_only=live_only)

@router.get("/landslide", response_model=List[DisasterEventOut], summary="List official slope stability and landslide alerts")
def get_landslide_disasters(
    state: Optional[str] = Query(None, description="Filter by state or UT"),
    live_only: bool = Query(False, description="Filter strictly for verified live/recent alerts")
):
    """Official GSI LEWS and State SDMA rainfall-triggered slope stability bulletins."""
    return disaster_service.get_disasters_by_hazard(hazard="LANDSLIDE", state=state, live_only=live_only)

@router.get("/severe-weather", response_model=List[DisasterEventOut], summary="List IMD severe precipitation and storm warnings")
def get_severe_weather_disasters(
    state: Optional[str] = Query(None, description="Filter by state or UT"),
    live_only: bool = Query(False, description="Filter strictly for verified live/recent alerts")
):
    """Official IMD synoptic severe weather, cloudburst, and heavy rainfall advisories."""
    return disaster_service.get_disasters_by_hazard(hazard="SEVERE_WEATHER", state=state, live_only=live_only)

@router.get("/{id}", response_model=DisasterEventOut, summary="Get disaster event by ID")
def get_disaster_by_id(id: str, db: Session = Depends(get_db)):
    """
    Retrieve full details for a specific disaster event.
    """
    disaster = disaster_service.get_disaster_by_id(db, id)
    if not disaster:
        raise HTTPException(status_code=404, detail=f"Disaster event '{id}' not found")
    return disaster
