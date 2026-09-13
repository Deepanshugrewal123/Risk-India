from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

class ResourceBase(BaseModel):
    name: str
    resource_type: str
    category: Optional[str] = "Disaster Management"
    state: Optional[str] = "Pan-India"
    district: Optional[str] = None
    location_id: Optional[str] = None
    disaster_type: Optional[str] = "ALL"
    description: Optional[str] = None
    phone: Optional[str] = None
    contact_number: Optional[str] = None
    website: Optional[str] = None
    website_url: Optional[str] = None
    address: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    source: Optional[str] = None
    source_url: Optional[str] = None
    verification_status: str = "VERIFIED"
    freshness: str = "CURRENT"
    accessibility_notes: Optional[str] = None
    last_verified_at: Optional[datetime] = None
    is_demo: bool = False
    services: Optional[List[str]] = None

class ResourceCreate(ResourceBase):
    pass

class ResourceOut(ResourceBase):
    id: str
    last_verified: Optional[datetime] = None
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True
        populate_by_name = True
