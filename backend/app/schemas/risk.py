from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime

class RiskFactorSchema(BaseModel):
    id: Optional[str] = None
    factor_name: str
    factor_value: str
    importance: str = "High"
    unit: Optional[str] = None

    class Config:
        from_attributes = True

class RiskAssessmentData(BaseModel):
    id: Optional[str] = None
    disaster_type: str = "FLOOD"
    risk_score: int
    risk_level: str
    model_version: str = "demo-v1"
    status: str = "DEMO"
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class LocationSummary(BaseModel):
    id: str
    name: str

class RiskResponse(BaseModel):
    location: LocationSummary
    assessment: RiskAssessmentData
    risk_factors: List[RiskFactorSchema]

class ModelFactorContribution(BaseModel):
    feature: str
    contribution: float
    direction: str  # "increases_risk" | "decreases_risk"
    display_label: str
    value: Optional[str] = None

class RiskAnalyzeRequest(BaseModel):
    location_id: str
    district: Optional[str] = None
    disaster_type: Optional[str] = Field(default="flood", description="Primary hazard category")
    hazard: Optional[str] = Field(default="flood", description="Hazard name")
    features: Optional[Dict[str, Any]] = Field(
        default=None,
        description="Antecedent CWC rainfall, river stage, and spatial telemetry features"
    )

class RiskAnalyzeResponse(BaseModel):
    status: str = "success"
    message: Optional[str] = None
    location_id: str
    district: Optional[str] = None
    state: Optional[str] = "Assam"
    hazard: str = "flood"
    disaster_type: str = "flood"
    model_version: str = "assam_flood_prototype_v1"
    flood_probability: Optional[float] = None
    probability: Optional[float] = None
    risk_score: Optional[int] = None
    risk_level: Optional[str] = None
    top_factors: List[ModelFactorContribution] = Field(default_factory=list)
    risk_factors: List[RiskFactorSchema] = Field(default_factory=list)
    is_prototype: bool = True
    emergency_warning: bool = False
    primary_driver: Optional[str] = "Antecedent Precipitation Influx"
    recommended_action: Optional[str] = None
    recommended_immediate_action: Optional[str] = None
    disclaimer: str = (
        "Experimental Assam flood-risk prototype based on a limited event dataset. "
        "Results are for research and awareness only and should not replace official emergency warnings."
    )
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
