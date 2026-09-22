"""
RISK // INDIA — National Predictive Risk Fusion Schema (Phase 30F)
==================================================================
Defines authoritative schemas for multi-source risk fusion, multi-hazard forecasting,
qualitative confidence & uncertainty, trend directionality, scenario analysis,
early-warning decision support, and transparent citizen-facing explanations.
"""

from enum import Enum
from typing import Dict, List, Optional, Any
from pydantic import BaseModel, Field
from datetime import datetime, timezone


class RiskState(str, Enum):
    """Deterministic risk severity states."""
    NORMAL = "NORMAL"
    WATCH = "WATCH"
    ELEVATED = "ELEVATED"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


class TrendState(str, Enum):
    """Directional trend of future hazard trajectory."""
    RISING = "RISING"
    STABLE = "STABLE"
    DECLINING = "DECLINING"
    VOLATILE = "VOLATILE"
    INSUFFICIENT_DATA = "INSUFFICIENT_DATA"


class ConfidenceLevel(str, Enum):
    """Qualitative assessment confidence. Strictly non-probabilistic."""
    LOW = "LOW"
    MODERATE = "MODERATE"
    HIGH = "HIGH"


class UncertaintyLevel(str, Enum):
    """Qualitative projection uncertainty."""
    LOW = "LOW"
    MODERATE = "MODERATE"
    HIGH = "HIGH"
    VERY_HIGH = "VERY_HIGH"


class ForecastHorizon(str, Enum):
    """Authoritative standard forecast horizons."""
    NOW = "NOW"
    H_0_6 = "0-6h"
    H_6_24 = "6-24h"
    D_1_3 = "1-3d"
    D_3_7 = "3-7d"


class EarlyWarningStatus(str, Enum):
    """Progressive early warning decision levels."""
    NO_ACTIVE_SIGNAL = "NO_ACTIVE_SIGNAL"
    WATCH = "WATCH"
    PREPARE = "PREPARE"
    GET_READY = "GET_READY"
    EVACUATION_READINESS = "EVACUATION_READINESS"
    EMERGENCY = "EMERGENCY"


class ScenarioType(str, Enum):
    """Predictive scenario categories."""
    BASELINE = "BASELINE"
    LIKELY = "LIKELY"
    ESCALATION = "ESCALATION"


class EvidenceSignal(BaseModel):
    """Canonical representation of an empirical or forecast input signal."""
    id: str
    provider: str                           # IMD, CWC, NDMA, USGS, NRSC, GSI
    source: str
    source_record_id: Optional[str] = None
    observed_at: str
    ingested_at: str
    geographic_scope: str
    variable: str
    unit: str
    raw_value: Optional[float] = None
    normalized_value: Optional[float] = None
    freshness: str                          # OFFICIAL_LIVE, OFFICIAL_RECENT, STALE, REGIONAL_BASELINE
    data_classification: str                # OBSERVED, FORECAST, BASELINE, OFFICIAL_WARNING, EMPIRICAL_ML
    official_status: str                    # VERIFIED, UNVERIFIED, ADVISORY
    url: Optional[str] = None


class PredictiveScenario(BaseModel):
    """Plausible forward risk scenario projection."""
    scenario_type: ScenarioType
    title: str
    description: str
    triggering_evidence: List[str] = Field(default_factory=list)
    expected_direction: TrendState
    uncertainty: UncertaintyLevel
    preparedness_implications: str
    safety_actions: List[str] = Field(default_factory=list)


class EarlyWarningAssessment(BaseModel):
    """Decision support guidance separating preparation from evacuation."""
    status: EarlyWarningStatus
    lead_time_window: str
    is_evacuation_advised: bool = False
    is_preparation_advised: bool = True
    preparation_guidance: List[str] = Field(default_factory=list)
    evacuation_guidance: Optional[str] = None
    official_bulletin_reference: Optional[str] = None


class CitizenSafetyAnswers(BaseModel):
    """Direct answers to the 12 foundational citizen safety questions."""
    what_is_happening_now: str
    what_could_happen_next: str
    what_is_future_trend: str
    how_serious_could_it_become: str
    why_risk_may_increase: str
    what_evidence_supports_it: List[str]
    what_should_i_do_now: List[str]
    what_to_prepare_before: List[str]
    what_to_do_during: List[str]
    what_to_do_after: List[str]
    what_data_missing_or_uncertain: str
    when_to_check_again: str


class PredictionExplanation(BaseModel):
    """Deterministic, transparent explanation of risk dynamics."""
    why_this_risk: str
    what_changed: str
    what_supports_it: List[str] = Field(default_factory=list)
    what_could_make_it_worse: str
    what_could_make_it_improve: str
    what_we_do_not_know: str
    citizen_answers: CitizenSafetyAnswers


class PredictiveTimelinePoint(BaseModel):
    """Unified timeline point across the 5 standard forecast horizons."""
    horizon: str
    time_window_label: str
    hazard: str
    current_risk_state: RiskState
    future_risk_state: RiskState
    risk_score: float
    trend: TrendState
    confidence: ConfidenceLevel
    uncertainty: UncertaintyLevel
    freshness: str
    evidence_summary: List[str] = Field(default_factory=list)
    official_warning: Optional[str] = None
    recommended_action: str
    data_classification: str


class PredictiveRiskAssessment(BaseModel):
    """Comprehensive fused predictive risk assessment for an entity and hazard."""
    region_id: str
    region_name: str
    region_type: str                        # STATE, UNION_TERRITORY
    hazard: str
    current_risk_state: RiskState
    current_risk_score: float
    future_risk_state: RiskState
    peak_future_score: float
    peak_future_window: str
    trend: TrendState
    confidence: ConfidenceLevel
    uncertainty: UncertaintyLevel
    overall_freshness: str
    
    # Core Evidence Fusion & Signals
    evidence_signals: List[EvidenceSignal] = Field(default_factory=list)
    official_warnings: List[Dict[str, Any]] = Field(default_factory=list)
    conflicting_signals: List[str] = Field(default_factory=list)
    has_conflicting_evidence: bool = False
    conflict_resolution_notes: Optional[str] = None
    
    # Scenarios & Early Warning
    scenarios: List[PredictiveScenario] = Field(default_factory=list)
    early_warning: EarlyWarningAssessment
    crisis_mode_recommended: bool = False
    crisis_activation_reason: Optional[str] = None
    
    # Timeline & Citizen Answers
    timeline: List[PredictiveTimelinePoint] = Field(default_factory=list)
    explanation: PredictionExplanation
    
    # Invariant Guards & ML Scope
    ml_scope: Dict[str, Any] = Field(default_factory=dict)
    synthetic_records: int = 0
    evaluated_at: str = Field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )


class NationalPredictiveOverview(BaseModel):
    """Complete national predictive posture across all 36 Indian entities."""
    title: str = "RISK // INDIA National Predictive Risk Fusion Overview"
    evaluated_at: str = Field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )
    total_entities_monitored: int = 36
    states_covered: int = 28
    union_territories_covered: int = 8
    supported_hazards: List[str]
    forecast_horizons: List[str]
    risk_state_distribution: Dict[str, int]
    trend_distribution: Dict[str, int]
    crisis_recommended_count: int
    crisis_recommended_entities: List[Dict[str, Any]] = Field(default_factory=list)
    synthetic_records: int = 0
    regions: List[Dict[str, Any]] = Field(default_factory=list)
