from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
import uuid
from app.database.database import Base

class RiskFactor(Base):
    __tablename__ = "risk_factors"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    assessment_id = Column(String, ForeignKey("risk_assessments.id"), nullable=False, index=True)
    factor_name = Column(String, nullable=False) # e.g. "Rainfall", "Soil Moisture"
    factor_value = Column(String, nullable=False) # e.g. "180", "82"
    importance = Column(String, default="High") # High, Medium, Low
    unit = Column(String, nullable=True) # "mm", "%", "m"

    # Relationships
    assessment = relationship("RiskAssessment", back_populates="factors")
