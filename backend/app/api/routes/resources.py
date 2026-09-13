from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from app.database.database import get_db
from app.schemas.resource import ResourceOut
from app.services.resource_service import resource_service

router = APIRouter(prefix="/resources", tags=["Relief & Verified Directory"])

@router.get("", response_model=List[ResourceOut], summary="List verified relief resources with multi-parameter filters")
def get_resources(
    category: Optional[str] = Query(None, description="Filter by assistance category (e.g. 'Medical Assistance', 'Food & Water', 'Rescue', 'Shelter')"),
    resource_type: Optional[str] = Query(None, description="Filter by resource type: GOVERNMENT, NGO, HELPLINE, SHELTER, HOSPITAL"),
    type: Optional[str] = Query(None, description="Alias for resource_type for backward compatibility"),
    state: Optional[str] = Query(None, description="Filter by state name (e.g. 'Assam', 'Odisha', 'Himachal Pradesh')"),
    location: Optional[str] = Query(None, description="Alias for state/location query"),
    district: Optional[str] = Query(None, description="Filter by district name"),
    disaster_type: Optional[str] = Query(None, description="Filter by relevant disaster hazard type: FLOOD, CYCLONE, LANDSLIDE, ALL"),
    verification_status: Optional[str] = Query(None, description="Filter by status: VERIFIED, UNDER_AUDIT, DEMO"),
    db: Session = Depends(get_db)
):
    """
    Retrieve authoritative disaster management entities, verified state emergency control rooms,
    statutory relief organizations, and verified humanitarian support networks.
    """
    effective_type = resource_type or type
    effective_loc = state or location

    return resource_service.get_resources(
        db=db,
        location=effective_loc,
        state=state,
        district=district,
        resource_type=effective_type,
        category=category,
        disaster_type=disaster_type,
        verification_status=verification_status
    )

@router.get("/{id}", response_model=ResourceOut, summary="Get verified resource detail by unique ID")
def get_resource_by_id(id: str):
    """
    Retrieve comprehensive metadata and official verification attributes for a specific resource.
    """
    res = resource_service.get_resource_by_id(id)
    if not res:
        raise HTTPException(status_code=404, detail=f"Resource '{id}' not found")
    return res
