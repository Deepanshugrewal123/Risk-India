from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional

from app.database.database import get_db
from app.models.location import Location
from app.schemas.location import LocationOut

router = APIRouter(prefix="/locations", tags=["Locations"])

@router.get("", response_model=List[LocationOut], summary="List all 37 Indian States and Union Territories")
def get_locations(
    type: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """
    Retrieve all 28 States and 9 Union Territories of India.
    Optionally filter by administrative type: `STATE` or `UNION_TERRITORY`.
    """
    query = db.query(Location)
    if type:
        query = query.filter(Location.administrative_type == type.upper())
    return query.order_by(Location.name.asc()).all()

@router.get("/{location_id}", response_model=LocationOut, summary="Get location details by ID or code")
def get_location_by_id(location_id: str, db: Session = Depends(get_db)):
    """
    Retrieve a specific State or Union Territory by ID (e.g. 'assam', 'delhi') or state code ('AS', 'DL').
    """
    loc_clean = location_id.lower().strip()
    location = db.query(Location).filter(
        (Location.id == loc_clean) | (Location.state_code == loc_clean.upper())
    ).first()

    if not location:
        raise HTTPException(status_code=404, detail=f"Location '{location_id}' not found")

    return location
