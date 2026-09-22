"""
RISK // INDIA — Crisis Intelligence Schema (Phase 30E)
======================================================
Defines operational states, action models, timeline points, explanations,
and complete crisis assessment structures for national public disaster assistance.
"""

from enum import Enum
from typing import Dict, List, Optional, Any
from pydantic import BaseModel, Field
from datetime import datetime, timezone


class CrisisOperationalState(str, Enum):
    """Operational/presentation states for crisis mode."""
    NORMAL = "NORMAL"
    WATCH = "WATCH"
    ELEVATED = "ELEVATED"
    CRISIS = "CRISIS"


class ActionPhase(str, Enum):
    """Life safety action phases."""
    BEFORE = "BEFORE"
    DURING = "DURING"
    AFTER = "AFTER"


class ActionPriority(str, Enum):
    """Action priority ordering for immediate life-safety."""
    LIFE_SAFETY = "LIFE_SAFETY"
    EVACUATION = "EVACUATION"
    AVOID_DANGER = "AVOID_DANGER"
    COMMUNICATION = "COMMUNICATION"
    EMERGENCY_RESOURCES = "EMERGENCY_RESOURCES"
    PREPARATION = "PREPARATION"


class TimelineSignalType(str, Enum):
    """Explicit provenance tags for crisis timeline milestones."""
    OBSERVED = "OBSERVED"
    OFFICIAL_WARNING = "OFFICIAL_WARNING"
    FORECAST = "FORECAST"
    FORECAST_DERIVED_RISK = "FORECAST_DERIVED_RISK"
    BASELINE = "BASELINE"
    EMPIRICAL_ML = "EMPIRICAL_ML"


class CrisisActionItem(BaseModel):
    """Individual human-action recommendation."""
    id: str
    priority: ActionPriority
    phase: ActionPhase
    order_rank: int = Field(..., description="Priority ranking 1-10 (1 is highest priority)")
    title: str
    instruction: str
    rationale: str
    target_hazard: str
    is_urgent: bool = False


class CrisisTimelinePoint(BaseModel):
    """Unified timeline projection point across 5 standard horizons."""
    horizon: str = Field(..., description="NOW, 0_6H, 6_24H, 1_3D, 3_7D")
    window_label: str
    expected_risk_level: str
    expected_risk_score: float
    confidence: float
    primary_hazard: str
    signal_type: TimelineSignalType
    key_factors: List[str] = Field(default_factory=list)
    provenance: str


class CrisisExplanation(BaseModel):
    """Deterministic explanation answering 'Why this risk?'."""
    why: str
    what_changed: str
    supporting_evidence: List[str] = Field(default_factory=list)
    what_could_change: str
    data_limitations: str = Field(..., description="Explicit statement of what we do not know")


class CrisisResourceItem(BaseModel):
    """Verified emergency contact or response facility."""
    id: str
    name: str
    resource_type: str
    category: str
    phone: Optional[str] = None
    contact_number: Optional[str] = None
    website_url: Optional[str] = None
    address: Optional[str] = None
    state: str
    district: Optional[str] = None
    disaster_type: str = "ALL"
    verification_status: str = "VERIFIED"
    distance_km: Optional[float] = None
    services: List[str] = Field(default_factory=list)
    source: str
    provenance: str


class FamilyChecklistItem(BaseModel):
    """Item in the 72-hour family disaster preparedness checklist."""
    category: str
    item: str
    description: str
    is_critical: bool = True


class CrisisAssessment(BaseModel):
    """Comprehensive Crisis Assessment for a state, UT, or locality."""
    region_id: str
    region_name: str
    operational_state: CrisisOperationalState
    is_crisis_recommended: bool
    activation_reason: str
    matched_rules: List[str] = Field(default_factory=list)
    is_manual_activation: bool = False
    
    primary_hazard: str
    current_risk_level: str
    current_risk_score: float
    peak_future_risk_level: str
    peak_future_window: str
    
    # Core Human-First Disaster Answers
    what_is_happening: str
    what_could_happen_next: str
    what_to_do_now: List[CrisisActionItem] = Field(
        default_factory=list,
        description="Top 3-5 prioritized immediate life-safety actions"
    )
    action_protocols: Dict[str, List[CrisisActionItem]] = Field(
        default_factory=dict,
        description="Structured BEFORE, DURING, and AFTER protocols"
    )
    family_prep_checklist: List[FamilyChecklistItem] = Field(default_factory=list)
    
    # Statutory Warnings & Verified Resources
    official_warnings: List[Dict[str, Any]] = Field(default_factory=list)
    emergency_resources: List[CrisisResourceItem] = Field(default_factory=list)
    resource_availability_note: Optional[str] = None
    
    # Projections, Explanation & Audit Guards
    timeline: List[CrisisTimelinePoint] = Field(default_factory=list)
    explanation: CrisisExplanation
    telemetry_summary: Dict[str, Any] = Field(default_factory=dict)
    ml_audit: Dict[str, Any] = Field(default_factory=dict)
    
    evaluated_at: str = Field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )
