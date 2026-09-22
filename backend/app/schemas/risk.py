from pydantic import BaseModel, Field, field_validator
from typing import List, Optional, Dict, Any
from datetime import datetime, timezone

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

class RiskSourceType:
    EMPIRICAL_ML = "EMPIRICAL_ML"
    REGIONAL_BASELINE = "REGIONAL_BASELINE"
    OFFICIAL_INTELLIGENCE = "OFFICIAL_INTELLIGENCE"
    CACHED_OFFICIAL_INTELLIGENCE = "CACHED_OFFICIAL_INTELLIGENCE"

class ScientificRiskState:
    EMPIRICALLY_VALIDATED_ML = "EMPIRICALLY_VALIDATED_ML"
    EMPIRICAL_DATA_INSUFFICIENT = "EMPIRICAL_DATA_INSUFFICIENT"
    BASELINE_ONLY = "BASELINE_ONLY"
    OFFICIAL_INTELLIGENCE_ONLY = "OFFICIAL_INTELLIGENCE_ONLY"

class RiskResponse(BaseModel):
    location: LocationSummary
    assessment: RiskAssessmentData
    risk_factors: List[RiskFactorSchema]
    # Phase 19 Multi-Hazard & Rationale Additions
    data_category: str = "REGIONAL_BASELINE"
    why_this_risk: Optional[str] = None
    methodology: Optional[str] = None
    ml_available: bool = False
    ml_message: Optional[str] = None
    hazard_scope: Optional[List[str]] = None
    # Phase 25 National Risk API & Scientific Honesty Additions
    risk_source: str = RiskSourceType.REGIONAL_BASELINE
    scientific_state: str = ScientificRiskState.BASELINE_ONLY
    model_scope: Optional[str] = "National Regional Baseline (Non-ML)"
    dataset_version: Optional[str] = "1.0.0-baseline"
    data_freshness: str = "LIVE"
    confidence_provenance: Optional[Dict[str, Any]] = None
    limitations: Optional[str] = None

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

    @field_validator("features")
    @classmethod
    def validate_features(cls, v: Optional[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
        if v is None:
            return v

        # Coordinate Validation (Indian bounding box: lat 6-38, lon 68-98)
        if "latitude" in v and v["latitude"] is not None:
            try:
                lat = float(v["latitude"])
                if not (6.0 <= lat <= 38.0):
                    raise ValueError(f"Latitude {lat} out of bounds; must be between 6.0 and 38.0.")
            except (ValueError, TypeError) as e:
                raise ValueError(f"Invalid latitude: {e}")

        if "longitude" in v and v["longitude"] is not None:
            try:
                lon = float(v["longitude"])
                if not (68.0 <= lon <= 98.0):
                    raise ValueError(f"Longitude {lon} out of bounds; must be between 68.0 and 98.0.")
            except (ValueError, TypeError) as e:
                raise ValueError(f"Invalid longitude: {e}")

        # Physical Rainfall Bounds (0.0 to 2000.0 mm)
        rainfall_keys = ["rainfall_6h", "rainfall_24h", "rainfall_72h", "rainfall_168h"]
        for rk in rainfall_keys:
            if rk in v and v[rk] is not None:
                try:
                    r_val = float(v[rk])
                    if not (0.0 <= r_val <= 2000.0):
                        raise ValueError(f"{rk} value {r_val} exceeds physical bounds; must be between 0.0 and 2000.0 mm.")
                except (ValueError, TypeError) as e:
                    raise ValueError(f"Invalid {rk}: {e}")

        # River Level Relative Bounds (-10.0m to 15.0m)
        if "river_level_relative" in v and v["river_level_relative"] is not None:
            try:
                rl = float(v["river_level_relative"])
                if not (-10.0 <= rl <= 15.0):
                    raise ValueError(f"river_level_relative {rl} out of physical bounds; must be between -10.0 and 15.0 m.")
            except (ValueError, TypeError) as e:
                raise ValueError(f"Invalid river_level_relative: {e}")

        return v

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
    # Phase 19 Multi-Hazard & Rationale Additions
    data_category: str = "ML_PREDICTION"
    why_this_risk: Optional[str] = None
    methodology: Optional[str] = None
    # Phase 25 National Risk API & Scientific Honesty Additions
    risk_source: str = RiskSourceType.EMPIRICAL_ML
    scientific_state: str = ScientificRiskState.EMPIRICALLY_VALIDATED_ML
    model_scope: Optional[str] = "Assam Brahmaputra & Barak Basins (Prototype)"
    dataset_version: Optional[str] = "1.0.0"
    data_freshness: str = "LIVE"
    confidence_provenance: Optional[Dict[str, Any]] = None
    limitations: Optional[str] = None
