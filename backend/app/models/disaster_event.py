from sqlalchemy import Column, String, Text, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
import uuid
from datetime import datetime, timezone
from app.database.database import Base

class DisasterEvent(Base):
    __tablename__ = "disaster_events"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    location_id = Column(String, ForeignKey("locations.id"), nullable=False, index=True)
    disaster_type = Column(String, nullable=False, index=True) # FLOOD, LANDSLIDE, CYCLONE, EARTHQUAKE, DROUGHT, HEATWAVE
    severity = Column(String, nullable=False, index=True) # LOW, MODERATE, HIGH, CRITICAL
    status = Column(String, nullable=False, index=True) # MONITORING, WARNING, ACTIVE, CONTAINED, RESOLVED
    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    source = Column(String, nullable=True) # e.g. "IMD", "CWC", "ASDMA"
    source_url = Column(String, nullable=True)
    is_demo = Column(Boolean, default=True)
    started_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    ended_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    # Relationships
    location = relationship("Location", back_populates="disaster_events")
