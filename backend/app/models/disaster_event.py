from sqlalchemy import Column, String, Text, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
import uuid
from datetime import datetime, timezone
from typing import Dict, Any, Optional
from app.database.database import Base


class DisasterEvent(Base):
    __tablename__ = "disaster_events"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    location_id = Column(String, ForeignKey("locations.id"), nullable=False, index=True)
    disaster_type = Column(String, nullable=False, index=True)  # FLOOD, LANDSLIDE, CYCLONE, EARTHQUAKE, DROUGHT, HEATWAVE
    severity = Column(String, nullable=False, index=True)  # LOW, MODERATE, HIGH, CRITICAL
    status = Column(String, nullable=False, index=True)  # MONITORING, WARNING, ACTIVE, CONTAINED, RESOLVED
    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    source = Column(String, nullable=True)  # e.g. "IMD", "CWC", "ASDMA"
    source_url = Column(String, nullable=True)
    is_demo = Column(Boolean, default=True)
    started_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), index=True)
    ended_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    # Relationships
    location = relationship("Location", back_populates="disaster_events")

    def as_geojson_point(self) -> Optional[Dict[str, Any]]:
        """
        WGS84 GeoJSON geometry representation derived from authoritative location coordinates.
        """
        if self.location and self.location.latitude is not None and self.location.longitude is not None:
            return {
                "type": "Point",
                "coordinates": [self.location.longitude, self.location.latitude]
            }
        return None

    def as_wkt_point(self) -> Optional[str]:
        """
        Standard Well-Known Text (WKT) representation for PostGIS spatial integration (SRID 4326).
        """
        if self.location and self.location.latitude is not None and self.location.longitude is not None:
            return f"SRID=4326;POINT({self.location.longitude} {self.location.latitude})"
        return None
