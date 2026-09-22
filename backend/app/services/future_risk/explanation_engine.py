"""
RISK // INDIA — Public Safety Explanation Engine
=================================================
Translates technical hydro-meteorological indicators into plain-language,
medically and physically responsible citizen intelligence.

Directly answers:
- WHAT: Plain-language hazard & risk level
- WHEN: Forecast window & onset timing
- WHY: Physical evidence & causal triggers
- CONFIDENCE: Qualitative confidence & data completeness
- WHAT TO DO: Actionable Before/During life-safety steps from DisasterActionEngine
- SOURCE: Verifiable authoritative government source citations
"""

from typing import Dict, Any, Optional
from app.services.future_risk.core_modes import FutureRiskAssessmentRecord
from app.services.future_risk.action_engine import disaster_action_engine


class PublicSafetyExplanationEngine:
    """Generates accessible, jargon-free public safety explanations for citizens."""

    def explain(
        self,
        assessment: FutureRiskAssessmentRecord,
        district: Optional[str] = None
    ) -> Dict[str, Any]:
        h_clean = assessment.hazard_type.upper().strip()
        reg = assessment.region_name
        window = assessment.forecast_window
        score = assessment.risk_score
        level = assessment.risk_level

        # WHAT: Plain language description
        what_descriptions = {
            "FLOOD": f"{level} flood risk developing in riverine catchments of {reg}." if level in ["HIGH", "VERY_HIGH", "CRITICAL"] else f"Normal seasonal river stage; low flood vulnerability in {reg}.",
            "CYCLONE": f"{level} cyclonic gale and storm surge threat along coastal sectors of {reg}." if level in ["HIGH", "VERY_HIGH", "CRITICAL"] else f"No cyclonic storm threatening maritime or land zones of {reg}.",
            "HEATWAVE": f"{level} heatwave conditions expected with severe thermal distress in {reg}." if level in ["HIGH", "VERY_HIGH", "CRITICAL"] else f"Temperatures within typical seasonal range in {reg}.",
            "SEVERE_WEATHER": f"{level} convective thunderstorm, lightning, and squall risk in {reg}." if level in ["HIGH", "VERY_HIGH", "CRITICAL"] else f"Fair weather conditions across {reg}.",
            "LANDSLIDE": f"POTENTIAL_LANDSLIDE_RISK {level} on saturated hill slopes of {reg}." if level in ["HIGH", "VERY_HIGH", "CRITICAL"] else f"Stable hill slope conditions; low landslide potential in {reg}.",
            "EARTHQUAKE": f"Baseline seismological exposure (BIS Seismic Zone index {score}/100) in {reg}."
        }
        what_text = what_descriptions.get(h_clean, f"{level} disaster risk assessment for {h_clean} in {reg}.")

        # WHEN: Timing window
        when_descriptions = {
            "NOW": "Immediate active observation window (0 to 30 minutes).",
            "0_6_HOURS": "Next 6 hours (Nowcast convective onset).",
            "6_24_HOURS": "Next 24 hours (Diurnal runoff and forecast cycle).",
            "1_3_DAYS": "Next 1 to 3 days (Synoptic progression).",
            "3_7_DAYS": "Extended outlook (3 to 7 days ahead)."
        }
        when_text = when_descriptions.get(window, f"Forecast window: {window}")

        # WHY: Plain language evidence
        if assessment.summary.startswith("WHY_FLOOD_RISK_CHANGED:"):
            why_text = assessment.summary.replace("WHY_FLOOD_RISK_CHANGED:", "").strip()
        elif "CYCLONE_DETECTED:" in assessment.summary:
            why_text = assessment.summary
        else:
            why_text = assessment.summary

        # CONFIDENCE: Accessible representation
        confidence_text = (
            f"{assessment.confidence} (Uncertainty: {assessment.uncertainty}, "
            f"Data Completeness: {assessment.data_completeness*100:.0f}%). "
            "Note: Qualitative confidence reflects evidence completeness and lead-time certainty, not statistical probability."
        )

        # WHAT TO DO: Integration with DisasterActionEngine
        actions = disaster_action_engine.get_actions_for_hazard(h_clean)
        before_steps = actions.get("BEFORE", [])[:3]
        during_steps = actions.get("DURING", [])[:3]

        what_to_do = {
            "preparedness_phase_before": before_steps,
            "immediate_safety_phase_during": during_steps,
            "emergency_dispatch": "Call 112 (National Unified Emergency Response) or 1078 (NDMA National Control Room)."
        }

        # SOURCE: Authoritative citations
        source_text = "Authoritative Government Sources: " + ", ".join(
            assessment.provenance.get("providers", ["Official Indian Disaster Management Authorities"])
        )

        return {
            "hazard": h_clean,
            "region": reg,
            "district": district or "All vulnerable districts",
            "risk_level": level,
            "forecast_window": window,
            "methodology": assessment.methodology,
            "public_safety_advisory": {
                "what": what_text,
                "when": when_text,
                "why": why_text,
                "confidence": confidence_text,
                "what_to_do": what_to_do,
                "source": source_text
            },
            "scientific_limitations": assessment.limitations,
            "ml_scope_note": assessment.ml_scope_note,
            "synthetic_records": 0
        }


public_safety_explanation_engine = PublicSafetyExplanationEngine()
