"""
RISK // INDIA — Flood Event Corroboration & Verification Service
==============================================================
Enforces strict scientific event corroboration rules for the national flood foundation:
1. An event is NEVER established solely because river stage or rainfall is elevated.
2. Official corroboration from authoritative disaster agencies (CWC Daily Flood Bulletins,
   ASDMA/SDMA Situation Reports, ISRO/NRSC Bhuvan inundation rasters) is strictly mandatory.
3. Uncorroborated stage spikes or isolated sensor fluctuations are rejected deterministically
   with REJECTION_REASON_MISSING_CORROBORATION.
4. Preserves zero-synthetic data policy (synthetic_records = 0).
"""

from typing import Dict, Any, List, Optional
from dataclasses import dataclass, asdict
from enum import Enum
import logging

from .base import (
    EventCategory,
    REJECTION_REASON_MISSING_CORROBORATION,
    REJECTION_REASON_SYNTHETIC_DATA_PROHIBITED,
    REJECTION_REASON_OUT_OF_BOUNDS_COORDINATES,
    REJECTION_REASON_FUTURE_TIMESTAMP
)
from .event_construction import ASSAM_AUDITED_FLOOD_EVENTS

logger = logging.getLogger("event-corroboration")


class CorroborationStatus(str, Enum):
    APPROVED_CORROBORATED = "APPROVED_CORROBORATED"
    UNVERIFIED_PENDING_EVIDENCE = "UNVERIFIED_PENDING_EVIDENCE"
    REJECTED_UNSUBSTANTIATED = "REJECTED_UNSUBSTANTIATED"


# Recognised authoritative keywords for ground-truth corroboration
AUTHORITATIVE_EVIDENCE_SIGNATURES = [
    "cwc",
    "central water commission",
    "asdma",
    "sdma",
    "isro",
    "bhuvan",
    "nrsc",
    "ndma",
    "imd",
    "flood bulletin",
    "situation report",
    "inundation",
    "sitrep"
]


@dataclass
class CorroboratedFloodEvent:
    event_id: str
    basin: str
    gauge_ids: List[str]
    start_time: str
    end_time: str
    source_evidence: List[str]
    corroboration_status: str
    confidence_score: float
    feature_completeness: float
    leakage_protection_metadata: Dict[str, Any]
    rejection_reason: Optional[str] = None
    synthetic_records: int = 0
    event_category: str = EventCategory.TRAINING_CANDIDATE.value

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class EventCorroborationService:
    """Evaluates and corroborates candidate flood events against authoritative evidence."""

    def __init__(self):
        self._events: Dict[str, CorroboratedFloodEvent] = {}
        self._init_audited_events()

    def _init_audited_events(self):
        """Seed the 12 historically audited and corroborated Assam flood events."""
        for e in ASSAM_AUDITED_FLOOD_EVENTS:
            self._events[e.event_id] = CorroboratedFloodEvent(
                event_id=e.event_id,
                basin=e.basin,
                gauge_ids=e.gauge_observations,
                start_time=e.start_time,
                end_time=e.end_time,
                source_evidence=e.evidence_sources,
                corroboration_status=CorroborationStatus.APPROVED_CORROBORATED.value,
                confidence_score=0.95 if e.event_confidence == "HIGH" else 0.85,
                feature_completeness=1.0,
                leakage_protection_metadata={
                    "fold_group": e.event_category,
                    "spatial_isolation": "Sub-basin cluster isolation enforced",
                    "temporal_isolation": "Chronologically partitioned (2022-2025)"
                },
                rejection_reason=None,
                synthetic_records=0,
                event_category=e.event_category
            )

    def evaluate_candidate_event(
        self,
        event_id: str,
        basin: str,
        gauge_ids: List[str],
        start_time: str,
        end_time: str,
        source_evidence: List[str],
        is_stage_elevated: bool = True,
        is_synthetic: bool = False
    ) -> CorroboratedFloodEvent:
        """
        Evaluates a candidate flood event. If an event has elevated stage but lacks
        authoritative agency corroboration, it is strictly REJECTED.
        """
        b_clean = basin.lower().strip()

        # Check 1: Zero synthetic data enforcement
        if is_synthetic:
            return CorroboratedFloodEvent(
                event_id=event_id,
                basin=b_clean,
                gauge_ids=gauge_ids,
                start_time=start_time,
                end_time=end_time,
                source_evidence=source_evidence,
                corroboration_status=CorroborationStatus.REJECTED_UNSUBSTANTIATED.value,
                confidence_score=0.0,
                feature_completeness=0.0,
                leakage_protection_metadata={"error": "Synthetic candidate strictly disallowed"},
                rejection_reason=REJECTION_REASON_SYNTHETIC_DATA_PROHIBITED,
                synthetic_records=1
            )

        # Check 2: Authoritative corroboration evidence
        has_authoritative_source = False
        if source_evidence:
            for ev in source_evidence:
                ev_lower = ev.lower()
                if any(sig in ev_lower for sig in AUTHORITATIVE_EVIDENCE_SIGNATURES):
                    has_authoritative_source = True
                    break

        if not has_authoritative_source:
            # Elevated river stage alone without official corroboration is REJECTED
            return CorroboratedFloodEvent(
                event_id=event_id,
                basin=b_clean,
                gauge_ids=gauge_ids,
                start_time=start_time,
                end_time=end_time,
                source_evidence=source_evidence,
                corroboration_status=CorroborationStatus.REJECTED_UNSUBSTANTIATED.value,
                confidence_score=0.0,
                feature_completeness=0.0,
                leakage_protection_metadata={"error": "Elevated stage without corroborating agency report"},
                rejection_reason=REJECTION_REASON_MISSING_CORROBORATION,
                synthetic_records=0
            )

        # Approved Corroborated Event
        return CorroboratedFloodEvent(
            event_id=event_id,
            basin=b_clean,
            gauge_ids=gauge_ids,
            start_time=start_time,
            end_time=end_time,
            source_evidence=source_evidence,
            corroboration_status=CorroborationStatus.APPROVED_CORROBORATED.value,
            confidence_score=0.90,
            feature_completeness=1.0,
            leakage_protection_metadata={
                "fold_group": EventCategory.VALIDATION_CANDIDATE.value,
                "spatial_isolation": f"Validated within {b_clean} catchment"
            },
            rejection_reason=None,
            synthetic_records=0
        )

    def register_event(self, event: CorroboratedFloodEvent) -> bool:
        """Registers an event if approved."""
        if event.corroboration_status == CorroborationStatus.APPROVED_CORROBORATED.value:
            self._events[event.event_id] = event
            return True
        return False

    def get_events(self, basin: Optional[str] = None) -> List[CorroboratedFloodEvent]:
        """Returns registered corroborated events."""
        if not basin:
            return list(self._events.values())
        b_clean = basin.lower().strip()
        return [e for e in self._events.values() if e.basin == b_clean]

    def get_event(self, event_id: str) -> Optional[CorroboratedFloodEvent]:
        """Returns an event by its ID."""
        return self._events.get(event_id.strip())

    def get_corroboration_summary(self, basin: str) -> Dict[str, Any]:
        """Returns corroboration summary for a basin."""
        events = self.get_events(basin)
        approved_count = sum(1 for e in events if e.corroboration_status == CorroborationStatus.APPROVED_CORROBORATED.value)
        return {
            "basin": basin.lower().strip(),
            "total_corroborated_events": len(events),
            "approved_events_count": approved_count,
            "synthetic_events": 0,
            "corroboration_policy": "Authoritative CWC/ASDMA/NRSC evidence required; uncorroborated stage spikes rejected",
            "events": [e.to_dict() for e in events]
        }


event_corroboration_service = EventCorroborationService()
