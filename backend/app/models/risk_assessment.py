from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship
import uuid
from datetime import datetime, timezone
from app.database.database import Base

class RiskAssessment(Base):
    __tablename__ = "risk_assessments"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    location_id = Column(String, ForeignKey("locations.id"), nullable=False, index=True)
    disaster_type = Column(String, nullable=False, default="FLOOD") # FLOOD, LANDSLIDE, CYCLONE, EARTHQUAKE, DROUGHT, HEATWAVE, FOREST_FIRE
    risk_score = Column(Integer, nullable=False) # 0 - 100
    risk_level = Column(String, nullable=False) # LOW, MODERATE, HIGH, CRITICAL
    model_version = Column(String, default="demo-v1")
    assessment_status = Column(String, default="DEMO") # DEMO, MODEL_PENDING, AVAILABLE
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    # Relationships
    location = relationship("Location", back_populates="risk_assessments")
    factors = relationship("RiskFactor", back_populates="assessment", cascade="all, delete-orphan")
