"""
RISK // INDIA — Early Warning Decision Support Engine (Phase 30F)
================================================================
Generates actionable early warning posture: NO_ACTIVE_SIGNAL, WATCH, PREPARE,
GET_READY, EVACUATION_READINESS, and EMERGENCY.

CRITICAL INVARIANT:
Strictly decouples 'Prepare' from 'Evacuate'. Evacuation instructions are never issued
prematurely or conflated with routine preparedness advisories.
"""

from typing import List, Dict, Any, Optional
from app.services.predictive_risk.fusion_schema import (
    EarlyWarningStatus,
    EarlyWarningAssessment,
    RiskState
)


class EarlyWarningEngine:
    """Evaluates progressive early warning decision states and actionable guidance."""

    @classmethod
    def evaluate(
        cls,
        hazard: str,
        current_state: RiskState,
        future_state: RiskState,
        peak_score: float,
        peak_window: str,
        official_warnings: List[Dict[str, Any]],
        has_conflicting_evidence: bool = False
    ) -> EarlyWarningAssessment:
        norm_hazard = hazard.upper().strip()

        # Check official warning bulletin reference
        bulletin_ref = None
        has_red = False
        has_orange = False
        for w in official_warnings:
            sev = str(w.get("severity", "")).upper()
            if sev == "RED":
                has_red = True
            elif sev in ["ORANGE", "AMBER"]:
                has_orange = True
            if not bulletin_ref and w.get("warning_id"):
                bulletin_ref = f"{w.get('provider', 'IMD')}: {w.get('warning_id')}"

        # -------------------------------------------------------------
        # Determine Status
        # -------------------------------------------------------------
        if current_state == RiskState.CRITICAL or (future_state == RiskState.CRITICAL and peak_score >= 85.0):
            status = EarlyWarningStatus.EMERGENCY
            is_evacuation = True
            is_preparation = True
        elif has_red or (future_state in [RiskState.HIGH, RiskState.CRITICAL] and peak_score >= 75.0):
            status = EarlyWarningStatus.EVACUATION_READINESS
            is_evacuation = True
            is_preparation = True
        elif has_orange or future_state == RiskState.HIGH or (future_state == RiskState.ELEVATED and peak_score >= 60.0):
            status = EarlyWarningStatus.GET_READY
            is_evacuation = False
            is_preparation = True
        elif future_state == RiskState.ELEVATED or future_state == RiskState.WATCH or peak_score >= 40.0:
            status = EarlyWarningStatus.PREPARE
            is_evacuation = False
            is_preparation = True
        elif current_state == RiskState.WATCH or peak_score >= 25.0:
            status = EarlyWarningStatus.WATCH
            is_evacuation = False
            is_preparation = True
        else:
            status = EarlyWarningStatus.NO_ACTIVE_SIGNAL
            is_evacuation = False
            is_preparation = False

        # -------------------------------------------------------------
        # Generate Action Guidance
        # -------------------------------------------------------------
        prep_guidance: List[str] = []
        evac_guidance: Optional[str] = None

        if norm_hazard == "FLOOD":
            if status in [EarlyWarningStatus.EMERGENCY, EarlyWarningStatus.EVACUATION_READINESS]:
                evac_guidance = (
                    "Move immediately to designated multi-purpose cyclone/flood shelters or higher ground. "
                    "Follow statutory administration evacuation routes. Do not walk or drive through flowing water."
                )
            prep_guidance = [
                "Elevate electrical appliances and critical documents to the upper floor.",
                "Store at least 72 hours of sealed potable drinking water and non-perishable food.",
                "Keep battery-powered torches, mobile power banks, and essential medications in waterproof bags.",
                "Unplug ground-level electrical devices before floodwaters enter premises."
            ]
        elif norm_hazard == "CYCLONE":
            if status in [EarlyWarningStatus.EMERGENCY, EarlyWarningStatus.EVACUATION_READINESS]:
                evac_guidance = (
                    "Evacuate kutcha houses and low-lying coastal surge zones immediately to pucca shelters. "
                    "Secure livestock and stay indoors once gale-force winds commence."
                )
            prep_guidance = [
                "Inspect roof structures, tie down loose outdoor objects, and trim overhang branches.",
                "Check emergency transceivers or battery radios for official IMD landfall bulletins.",
                "Prepare a family grab-and-go kit containing identification, cash, and medical supplies.",
                "Board or tape large glass windows on the windward side of the structure."
            ]
        elif norm_hazard == "HEATWAVE":
            evac_guidance = None  # Heatwaves require sheltering and cooling, not physical evacuation
            prep_guidance = [
                "Suspend all strenuous outdoor physical activity between 11:00 AM and 4:00 PM.",
                "Drink oral rehydration solutions (ORS), lemon water, or buttermilk frequently even if not thirsty.",
                "Keep curtains drawn on sun-facing windows and maintain ventilation in living spaces.",
                "Check on vulnerable elder relatives, pregnant individuals, and infants."
            ]
        elif norm_hazard == "LANDSLIDE":
            if status in [EarlyWarningStatus.EMERGENCY, EarlyWarningStatus.EVACUATION_READINESS]:
                evac_guidance = (
                    "Evacuate hillside dwellings and valley floor drainage paths immediately. "
                    "Move laterally away from active slope movement to stable rock ridges."
                )
            prep_guidance = [
                "Monitor hillside retaining walls and slopes for tension cracks or unusual muddy runoff.",
                "Listen for rumbling sounds, tree cracking, or sudden shifts in boulder stabilization.",
                "Identify two safe uphill or ridge evacuation paths that avoid natural gullies."
            ]
        elif norm_hazard == "SEVERE_WEATHER":
            if status in [EarlyWarningStatus.EMERGENCY, EarlyWarningStatus.EVACUATION_READINESS]:
                evac_guidance = (
                    "Seek shelter immediately inside a sturdy concrete building. Stay away from metal sheds, tin roofs, and tall trees."
                )
            prep_guidance = [
                "Unplug sensitive electronics and avoid contact with wired electrical appliances during lightning.",
                "Park vehicles under solid carports away from mature trees and utility poles.",
                "Keep domestic pets indoors and ensure livestock have sturdy shelter."
            ]
        else:  # EARTHQUAKE / DEFAULT
            evac_guidance = (
                "If shaking occurs: DROP, COVER, and HOLD ON. Do not use elevators. "
                "Evacuate calmly to open fields only after ground shaking ceases, watching for fallen power cables."
            ) if status == EarlyWarningStatus.EMERGENCY else None
            prep_guidance = [
                "Anchor tall bookcases, heavy mirrors, and water heaters securely to structural wall studs.",
                "Know safe spots in every room under sturdy tables or against interior bearing walls.",
                "Locate main gas, electricity, and water shutoff valves and know how to disconnect them."
            ]

        if status == EarlyWarningStatus.NO_ACTIVE_SIGNAL:
            prep_guidance = [
                "Conditions are currently stable. Maintain baseline household disaster readiness supplies.",
                "Check periodic regional weather advisories during seasonal transition periods."
            ]

        return EarlyWarningAssessment(
            status=status,
            lead_time_window=peak_window if peak_window != "NOW" else "Immediate (0-6h)",
            is_evacuation_advised=is_evacuation,
            is_preparation_advised=is_preparation,
            preparation_guidance=prep_guidance,
            evacuation_guidance=evac_guidance,
            official_bulletin_reference=bulletin_ref
        )
