from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class LocationBase(BaseModel):
    id: str
    name: str
    administrative_type: str
    state_code: str
    capital: Optional[str] = None
    region: Optional[str] = None
    latitude: float
    longitude: float

class LocationCreate(LocationBase):
    pass

class LocationSimple(BaseModel):
    id: str
    name: str
    state_code: Optional[str] = None
    administrative_type: Optional[str] = None

    class Config:
        from_attributes = True

class LocationOut(LocationBase):
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True
