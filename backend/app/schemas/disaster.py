from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

class DisasterEventBase(BaseModel):
    hazard_type: Optional[str] = None
    disaster_type: Optional[str] = None
    severity: str
    status: str
    title: str
    description: Optional[str] = None
    source: Optional[str] = None
    source_url: Optional[str] = None
    is_demo: bool = False
    verified: bool = False
    state: Optional[str] = None
    district: Optional[str] = None
    location: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    coordinates: Optional[List[float]] = None
    freshness: str = "RECENT"
    risk_score: Optional[int] = None
    location_id: Optional[str] = None

class DisasterEventCreate(DisasterEventBase):
    location_id: str
    started_at: Optional[datetime] = None
    ended_at: Optional[datetime] = None

class DisasterEventOut(DisasterEventBase):
    id: str
    observed_at: Optional[datetime] = None
    retrieved_at: Optional[datetime] = None
    started_at: Optional[datetime] = None
    ended_at: Optional[datetime] = None
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True
        populate_by_name = True
