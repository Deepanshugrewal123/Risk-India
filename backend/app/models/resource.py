from sqlalchemy import Column, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
import uuid
from datetime import datetime, timezone
from app.database.database import Base

class Resource(Base):
    __tablename__ = "resources"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, nullable=False, index=True)
    resource_type = Column(String, nullable=False, index=True) # GOVERNMENT, NGO, SHELTER, HOSPITAL, HELPLINE, RELIEF_CENTER
    location_id = Column(String, ForeignKey("locations.id"), nullable=False, index=True)
    description = Column(Text, nullable=True)
    website = Column(String, nullable=True)
    phone = Column(String, nullable=True)
    verification_status = Column(String, default="DEMO", index=True) # VERIFIED, PENDING, DEMO
    last_verified = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    # Relationships
    location = relationship("Location", back_populates="resources")
