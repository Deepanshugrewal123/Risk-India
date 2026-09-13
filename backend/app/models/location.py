from sqlalchemy import Column, String, Float, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from app.database.database import Base

class Location(Base):
    __tablename__ = "locations"

    id = Column(String, primary_key=True, index=True) # e.g. "assam", "delhi", "ladakh"
    name = Column(String, nullable=False, index=True) # e.g. "Assam", "Delhi"
    administrative_type = Column(String, nullable=False, index=True) # "STATE" or "UNION_TERRITORY"
    state_code = Column(String(10), nullable=False, index=True) # e.g. "AS", "DL"
    capital = Column(String, nullable=True) # e.g. "Dispur", "New Delhi"
    region = Column(String, nullable=True) # e.g. "Northeast India", "North India"
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    # Relationships
    risk_assessments = relationship("RiskAssessment", back_populates="location", cascade="all, delete-orphan")
    disaster_events = relationship("DisasterEvent", back_populates="location", cascade="all, delete-orphan")
    resources = relationship("Resource", back_populates="location", cascade="all, delete-orphan")
