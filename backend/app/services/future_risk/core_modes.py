"""
RISK // INDIA — Core Risk Modes & Methodology Taxonomy
======================================================
Strict conceptual separation of the six core risk modes:
1. CURRENT_DISASTER_INTELLIGENCE: Active official alerts and telemetry.
2. FUTURE_RISK_FORECAST: Forward-looking risk projections across multi-day horizons.
3. REGIONAL_BASELINE_RISK: Static vulnerability and climatological zonation.
4. EMPIRICAL_ML_PREDICTION: Validated machine-learning inference (Assam prototype only).
5. OFFICIAL_WARNING: Bulletins issued directly by government agencies (IMD, CWC, NDMA).
6. EMERGENCY_RESOURCE_INTELLIGENCE: Verified rescue, relief, medical, and volunteer infrastructure.
"""

from enum import Enum
from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any
from datetime import datetime, timezone


class RiskMode(str, Enum):
    CURRENT_DISASTER_INTELLIGENCE = "CURRENT_DISASTER_INTELLIGENCE"
    FUTURE_RISK_FORECAST = "FUTURE_RISK_FORECAST"
    REGIONAL_BASELINE_RISK = "REGIONAL_BASELINE_RISK"
    EMPIRICAL_ML_PREDICTION = "EMPIRICAL_ML_PREDICTION"
    OFFICIAL_WARNING = "OFFICIAL_WARNING"
    EMERGENCY_RESOURCE_INTELLIGENCE = "EMERGENCY_RESOURCE_INTELLIGENCE"


class MethodologyType(str, Enum):
    OFFICIAL_FORECAST = "OFFICIAL_FORECAST"
    OFFICIAL_WARNING = "OFFICIAL_WARNING"
    FORECAST_DERIVED_RISK = "FORECAST_DERIVED_RISK"
    EMPIRICAL_ML = "EMPIRICAL_ML"
    RULE_BASED_EARLY_WARNING = "RULE_BASED_EARLY_WARNING"
    REGIONAL_BASELINE = "REGIONAL_BASELINE"
    CURRENT_OFFICIAL_INTELLIGENCE = "CURRENT_OFFICIAL_INTELLIGENCE"


class ConfidenceLevel(str, Enum):
    HIGH = "HIGH"
    MODERATE = "MODERATE"
    LOW = "LOW"
    VERY_LOW = "VERY_LOW"
    UNAVAILABLE = "UNAVAILABLE"


@dataclass
class ForecastEvidence:
    """Individual telemetry or forecast signal driving a future risk assessment."""
    signal_name: str
    source_provider: str
    value: Any
    unit: str
    observed_or_forecast_at: str
    freshness: str
    provenance_record_id: str

    def to_dict(self) -> Dict[str, Any]:
        return {
            "signal_name": self.signal_name,
            "source_provider": self.source_provider,
            "value": self.value,
            "unit": self.unit,
            "observed_or_forecast_at": self.observed_or_forecast_at,
            "freshness": self.freshness,
            "provenance_record_id": self.provenance_record_id
        }


@dataclass
class FutureRiskAssessmentRecord:
    """Standardized multi-horizon forward risk assessment."""
    risk_mode: str
    hazard_type: str
    region_name: str
    region_code: str
    region_type: str
    primary_basin: str
    forecast_window: str
    risk_score: int
    risk_level: str
    methodology: str
    confidence: str
    summary: str
    evidence_signals: List[ForecastEvidence] = field(default_factory=list)
    freshness: Dict[str, Any] = field(default_factory=dict)
    provenance: Dict[str, Any] = field(default_factory=dict)
    limitations: str = ""
    ml_scope_note: str = ""
    synthetic_records: int = 0
    uncertainty: str = "MODERATE"
    data_completeness: float = 0.85
    official_warning: Optional[Dict[str, Any]] = None
    recommended_action: Optional[Dict[str, Any]] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "hazard": self.hazard_type,
            "hazard_type": self.hazard_type,
            "region": {
                "name": self.region_name,
                "code": self.region_code,
                "type": self.region_type,
                "primary_basin": self.primary_basin
            },
            "risk_mode": self.risk_mode,
            "forecast_window": self.forecast_window,
            "risk_score": self.risk_score,
            "risk_level": self.risk_level,
            "methodology": self.methodology,
            "confidence": self.confidence,
            "uncertainty": self.uncertainty,
            "data_completeness": self.data_completeness,
            "summary": self.summary,
            "evidence": [e.to_dict() for e in self.evidence_signals],
            "evidence_signals": [e.to_dict() for e in self.evidence_signals],
            "official_warning": self.official_warning,
            "freshness": self.freshness,
            "provenance": self.provenance,
            "limitations": self.limitations,
            "ml_scope_note": self.ml_scope_note,
            "recommended_action": self.recommended_action,
            "synthetic_records": self.synthetic_records
        }
