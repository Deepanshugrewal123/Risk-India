"""
RISK // INDIA — Predictive Scenario Engine (Phase 30F)
======================================================
Constructs 3 forward-looking risk scenarios:
1. BASELINE: Persistence of current observed conditions.
2. LIKELY: Expected evolution based on numerical weather prediction and official advisories.
3. ESCALATION: Plausible compounded escalation (e.g. intensified precipitation, track shift, reservoir release).

CRITICAL INVARIANT:
For Earthquakes, scenarios reflect seismic baseline and structural readiness,
never deterministic forward earthquake event predictions.
"""

from typing import List, Dict, Any
from app.services.predictive_risk.fusion_schema import (
    ScenarioType,
    PredictiveScenario,
    TrendState,
    UncertaintyLevel,
    RiskState
)


class ScenarioEngine:
    """Generates deterministic Baseline, Likely, and Escalation scenarios."""

    @classmethod
    def generate_scenarios(
        cls,
        hazard: str,
        current_state: RiskState,
        future_state: RiskState,
        peak_future_score: float,
        corroborating_factors: List[str],
        uncertainty: UncertaintyLevel
    ) -> List[PredictiveScenario]:
        norm_hazard = hazard.upper().strip()

        # -------------------------------------------------------------
        # Earthquake Guard: No forward event prediction
        # -------------------------------------------------------------
        if norm_hazard == "EARTHQUAKE":
            return [
                PredictiveScenario(
                    scenario_type=ScenarioType.BASELINE,
                    title="Ambient Tectonic Background",
                    description="Current regional seismic baseline according to BIS seismic zoning and historical seismic catalogue.",
                    triggering_evidence=["Regional lithospheric baseline", "USGS / NCS historical epicentral depth distribution"],
                    expected_direction=TrendState.STABLE,
                    uncertainty=UncertaintyLevel.VERY_HIGH,
                    preparedness_implications="Structural seismic readiness remains continuously vital regardless of recent micro-seismicity.",
                    safety_actions=[
                        "Inspect non-structural interior hazards and brace heavy objects.",
                        "Verify household emergency grab-bag supplies and clear primary exit corridors."
                    ]
                ),
                PredictiveScenario(
                    scenario_type=ScenarioType.LIKELY,
                    title="Standard Seismic Quiescence",
                    description="Continuation of background micro-tremors without detectable localized seismic clustering.",
                    triggering_evidence=["Current seismic monitoring stations reporting normal baseline noise levels"],
                    expected_direction=TrendState.STABLE,
                    uncertainty=UncertaintyLevel.VERY_HIGH,
                    preparedness_implications="Maintain continuous vigilance and review structural retrofitting guidelines.",
                    safety_actions=[
                        "Participate in community earthquake drill procedures.",
                        "Review family meeting points outside collapse zones."
                    ]
                ),
                PredictiveScenario(
                    scenario_type=ScenarioType.ESCALATION,
                    title="Post-Event Aftershock Sensitivity",
                    description="In the event of unexpected tectonic slippage, secondary structural damage or localized slope instability may occur.",
                    triggering_evidence=["Fault line proximity and regional historical maximum credible earthquake thresholds"],
                    expected_direction=TrendState.STABLE,
                    uncertainty=UncertaintyLevel.VERY_HIGH,
                    preparedness_implications="Identify reinforced door frames and open gathering fields away from overhead wires.",
                    safety_actions=[
                        "Memorize DROP, COVER, and HOLD ON protocols.",
                        "Identify master utility shutoffs for gas and power."
                    ]
                )
            ]

        # -------------------------------------------------------------
        # Meteorological & Hydrological Hazards
        # -------------------------------------------------------------
        # 1. BASELINE SCENARIO
        baseline_sc = PredictiveScenario(
            scenario_type=ScenarioType.BASELINE,
            title=f"Baseline Persistence ({current_state.value})",
            description=f"Current meteorological parameters and ground telemetry continue at present levels over the next 12 hours.",
            triggering_evidence=corroborating_factors[:2] if corroborating_factors else ["Current station observation telemetry"],
            expected_direction=TrendState.STABLE,
            uncertainty=UncertaintyLevel.LOW,
            preparedness_implications="Standard operational readiness; continue regular daily activities with baseline situational monitoring.",
            safety_actions=[
                "Monitor district disaster authority social bulletins and local weather broadcasts.",
                "Maintain standard household emergency battery kits and mobile charge levels."
            ]
        )

        # 2. LIKELY SCENARIO
        likely_trend = TrendState.RISING if peak_future_score > 50.0 else (
            TrendState.DECLINING if current_state in [RiskState.HIGH, RiskState.CRITICAL] and peak_future_score < 40.0 else TrendState.STABLE
        )
        likely_title = (
            f"Expected {norm_hazard.capitalize()} Escalation" if likely_trend == TrendState.RISING else (
                f"Anticipated {norm_hazard.capitalize()} Easing" if likely_trend == TrendState.DECLINING else f"Sustained {norm_hazard.capitalize()} Activity"
            )
        )
        likely_desc = (
            f"Numerical forecast models project progressive hazard development consistent with incoming weather systems."
            if likely_trend == TrendState.RISING else
            f"Weather systems are projected to track eastward with gradual stabilization of ground indicators."
        )

        likely_actions = [
            f"Review household {norm_hazard.lower()} response checklist and secure vulnerable property.",
            "Avoid unnecessary travel into waterlogged or high-exposure transit sectors.",
            "Verify backup lighting, water purification, and non-perishable rations."
        ]
        if norm_hazard == "HEATWAVE":
            likely_actions = [
                "Schedule field work and transport before 10:00 AM or after 5:00 PM.",
                "Ensure electrolyte replacement hydration is accessible throughout the day.",
                "Provide shaded enclosures and adequate water troughs for domestic animals."
            ]

        likely_sc = PredictiveScenario(
            scenario_type=ScenarioType.LIKELY,
            title=likely_title,
            description=likely_desc,
            triggering_evidence=corroborating_factors if corroborating_factors else ["NWP forecast models and official regional advisories"],
            expected_direction=likely_trend,
            uncertainty=uncertainty,
            preparedness_implications="Active preparation warranted. Community members in low-lying or exposed areas should initiate protective measures.",
            safety_actions=likely_actions
        )

        # 3. ESCALATION SCENARIO
        escalation_actions = [
            "Prepare grab-and-go emergency bags with essential documents, medicines, and cash.",
            "Familiarize with nearest designated community cyclone/flood shelter locations.",
            "Cooperate promptly with local civil defense and emergency service directions."
        ]
        if norm_hazard == "HEATWAVE":
            escalation_actions = [
                "Identify air-cooled or community cooling shelters equipped with medical support.",
                "Seek immediate emergency medical care upon witnessing signs of heat stroke or confusion.",
                "Cease all non-critical outdoor labor activities regardless of occupation."
            ]

        escalation_sc = PredictiveScenario(
            scenario_type=ScenarioType.ESCALATION,
            title=f"Severe Compounded Escalation ({norm_hazard.capitalize()})",
            description=(
                f"Adverse compounding factors—such as cloudburst precipitation, upstream reservoir discharges, "
                f"or cyclonic track acceleration—result in heightened community exposure."
            ),
            triggering_evidence=[
                "Upper atmospheric moisture convergence anomaly",
                "Hydraulic basin saturation exceeding 85% capacity",
                "High-tide astronomical compounding" if norm_hazard in ["CYCLONE", "FLOOD"] else "Extended high-pressure heat dome stagnation"
            ],
            expected_direction=TrendState.RISING,
            uncertainty=UncertaintyLevel.HIGH if uncertainty != UncertaintyLevel.VERY_HIGH else UncertaintyLevel.VERY_HIGH,
            preparedness_implications="High consequence threshold. Emergency services on standby; immediate protective action readiness required.",
            safety_actions=escalation_actions
        )

        return [baseline_sc, likely_sc, escalation_sc]
