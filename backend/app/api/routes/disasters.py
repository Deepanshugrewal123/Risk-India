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

@router.get("/{id}", response_model=DisasterEventOut, summary="Get disaster event by ID")
def get_disaster_by_id(id: str, db: Session = Depends(get_db)):
    """
    Retrieve full details for a specific disaster event.
    """
    disaster = disaster_service.get_disaster_by_id(db, id)
    if not disaster:
        raise HTTPException(status_code=404, detail=f"Disaster event '{id}' not found")
    return disaster
