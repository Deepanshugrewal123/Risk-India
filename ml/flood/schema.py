"""
RISK // INDIA — Flood ML Feature Schemas & Output Contracts

Defines strict input and output schemas:
- Tiered feature schemas (Core, Optional, Future)
- Standardized Model Output Contract
- Model Artifact Metadata Schema
"""

from typing import Dict, Any, List, Optional, Literal
from datetime import datetime, timezone
from pydantic import BaseModel, Field

RiskLevel = Literal["LOW", "MODERATE", "HIGH", "CRITICAL"]
ImpactDirection = Literal["INCREASES_RISK", "DECREASES_RISK", "NEUTRAL"]
ModelStatus = Literal["AVAILABLE", "MODEL_PENDING", "MODEL_NOT_AVAILABLE", "FALLBACK_HEURISTIC"]

# ==============================================================================
# Feature Schemas (Tiered Availability)
# ==============================================================================

class CoreFloodFeatures(BaseModel):
    """
    Tier 1: Mandatory Core Meteorological & Terrain Features.
    Must be present for any deterministic model evaluation.
    """
    location_id: str = Field(..., description="Indian State or District identifier (e.g. 'assam', 'bihar')")
    rainfall_24h: float = Field(..., ge=0.0, le=2000.0, description="24-hour rainfall in millimeters (IMD / sensor)")
    rainfall_72h_cumulative: float = Field(..., ge=0.0, le=4000.0, description="72-hour cumulative antecedent rainfall (mm)")
    elevation: float = Field(..., ge=-50.0, le=9000.0, description="Terrain elevation in meters above sea level")
    slope: float = Field(..., ge=0.0, le=90.0, description="Topographical slope in degrees")
    monsoon_season_flag: int = Field(default=1, ge=0, le=1, description="1 if month in [June, July, August, September], else 0")


class OptionalFloodFeatures(BaseModel):
    """
    Tier 2: Hydrological & Catchment Dynamics (Available when station telemetry exists).
    """
    rainfall_anomaly: Optional[float] = Field(default=None, description="Percentage departure from 30-year Long Period Average")
    soil_moisture_index: Optional[float] = Field(default=None, ge=0.0, le=100.0, description="Soil saturation percentage (0-100%)")
    river_gauge_above_danger: Optional[float] = Field(default=None, description="Meters above CWC designated danger level")
    distance_to_river_km: Optional[float] = Field(default=None, ge=0.0, description="Distance to nearest major river channel in km")
    historical_flood_frequency: Optional[int] = Field(default=None, ge=0, description="Recorded flood events in preceding 10 years")


class FutureFloodFeatures(BaseModel):
    """
    Tier 3: Advanced Hydro-geomorphological & Satellite Inundation Telemetry.
    """
    catchment_area_sqkm: Optional[float] = Field(default=None, ge=0.0, description="Upstream hydrological catchment area in km²")
    drainage_density: Optional[float] = Field(default=None, ge=0.0, description="Stream length per unit catchment area (km/km²)")
    land_use_impervious_ratio: Optional[float] = Field(default=None, ge=0.0, le=1.0, description="Ratio of built-up/impervious terrain")
    days_since_last_flood: Optional[int] = Field(default=None, ge=0, description="Decay factor tracking time since previous overflow")


class FloodInferenceInput(BaseModel):
    """
    Unified Inference Request combining core, optional, and auxiliary features.
    """
    location_id: str
    rainfall_24h: float = 0.0
    rainfall_72h_cumulative: Optional[float] = None
    elevation: Optional[float] = None
    slope: Optional[float] = None
    monsoon_season_flag: Optional[int] = 1
    rainfall_anomaly: Optional[float] = None
    soil_moisture_index: Optional[float] = None
    river_gauge_above_danger: Optional[float] = None
    distance_to_river_km: Optional[float] = None
    historical_flood_frequency: Optional[int] = None
    auxiliary: Dict[str, Any] = Field(default_factory=dict)


# ==============================================================================
# Model Output Contract
# ==============================================================================

class FactorContribution(BaseModel):
    factor_name: str
    factor_value: str
    impact: ImpactDirection = "INCREASES_RISK"
    importance_rank: int
    contribution_weight: float = Field(..., ge=0.0, le=1.0)
    unit: Optional[str] = None


class StandardizedModelOutput(BaseModel):
    """
    Standardized Model Output Contract across all disaster models in RISK // INDIA.
    """
    location_id: str
    disaster_type: Literal["FLOOD"] = "FLOOD"
    probability: float = Field(..., ge=0.0, le=1.0, description="Calibrated posterior probability P(Flood=1 | X)")
    risk_score: int = Field(..., ge=0, le=100, description="Continuous risk score in [0, 100]")
    risk_level: RiskLevel
    model_version: str
    status: ModelStatus
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    factors: List[FactorContribution] = Field(default_factory=list)
    primary_driver: str = "Hydrological & Meteorological Influx"
    recommended_action: str
    disclaimer: str = "PROVISIONAL ASSESSMENT — VALIDATED TRAINING PIPELINE REQUIRED"


# ==============================================================================
# Model Artifact Metadata Schema
# ==============================================================================

class ModelArtifactMetadata(BaseModel):
    """
    Metadata schema saved alongside trained pipeline artifacts.
    """
    model_id: str
    disaster_type: str = "FLOOD"
    algorithm: str
    training_date: str
    dataset_source: str
    training_samples: int
    test_samples: int
    feature_names: List[str]
    metrics_summary: Dict[str, Any]
    temporal_split: Dict[str, Any]
    git_commit_or_hash: Optional[str] = None
