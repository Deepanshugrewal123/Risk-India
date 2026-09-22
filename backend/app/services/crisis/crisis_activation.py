"""
RISK // INDIA — Crisis Activation Engine (Phase 30E)
====================================================
Deterministic operational state evaluation based on verified warnings,
empirical telemetry, future-risk projections, and multi-signal convergence.
"""

from typing import Dict, List, Any, Optional, Tuple
from app.services.crisis.crisis_schema import CrisisOperationalState


class CrisisActivationEngine:
    """
    Evaluates whether a region should be placed in CRISIS, ELEVATED, WATCH, or NORMAL state.
    
    Implements Deterministic Rules A-E and the Weak Signal Filter:
    - Rule A: Verified Official Warning (RED/ORANGE alert)
    - Rule B: High/Critical current risk with valid empirical telemetry
    - Rule C: High future-risk signal with evidence
    - Rule D: Multi-signal convergence (e.g., heavy rain + rising river stage)
    - Rule E: User manual activation
    - Weak Signal Filter: Stale or isolated weak forecasts do not trigger automated emergency states.
    """

    @staticmethod
    def evaluate(
        current_risk_level: str,
        current_risk_score: float,
        peak_future_risk_level: str,
        peak_future_score: float,
        official_warnings: List[Dict[str, Any]],
        telemetry_summary: Dict[str, Any],
        future_risk_confidence: float = 0.5,
        telemetry_fresh: bool = True,
        manual_activation: bool = False
    ) -> Tuple[CrisisOperationalState, bool, str, List[str]]:
        """
        Returns:
            (operational_state, is_crisis_recommended, activation_reason, matched_rules)
        """
        matched_rules: List[str] = []
        is_crisis_recommended = False
        state = CrisisOperationalState.NORMAL
        reason_parts: List[str] = []

        # Check Official Warnings (Rule A)
        has_red_warning = False
        has_orange_warning = False
        for w in (official_warnings or []):
            sev = str(w.get("severity", "")).upper()
            color = str(w.get("color", "")).upper()
            if sev == "RED" or color == "RED" or "CRITICAL" in sev:
                has_red_warning = True
            elif sev in ["ORANGE", "AMBER", "HIGH"] or color in ["ORANGE", "AMBER"]:
                has_orange_warning = True

        if has_red_warning:
            matched_rules.append("RULE_A_OFFICIAL_RED_WARNING")
            state = CrisisOperationalState.CRISIS
            is_crisis_recommended = True
            reason_parts.append("Official RED alert/bulletin issued by statutory agency (IMD/CWC/INCOIS)")
        elif has_orange_warning:
            matched_rules.append("RULE_A_OFFICIAL_ORANGE_WARNING")
            state = CrisisOperationalState.ELEVATED
            is_crisis_recommended = True
            reason_parts.append("Official ORANGE/AMBER warning issued by statutory agency")

        # Check High Current Risk with Telemetry (Rule B)
        norm_curr_level = str(current_risk_level).upper()
        if norm_curr_level == "CRITICAL" and telemetry_fresh:
            matched_rules.append("RULE_B_CRITICAL_CURRENT_RISK")
            state = CrisisOperationalState.CRISIS
            is_crisis_recommended = True
            reason_parts.append("Current empirical risk score is CRITICAL with active telemetry")
        elif norm_curr_level == "HIGH" and telemetry_fresh:
            matched_rules.append("RULE_B_HIGH_CURRENT_RISK")
            if state != CrisisOperationalState.CRISIS:
                state = CrisisOperationalState.ELEVATED
            is_crisis_recommended = True
            reason_parts.append("Current empirical risk score is HIGH with active telemetry")

        # Check High Future Risk Signal (Rule C)
        norm_future_level = str(peak_future_risk_level).upper()
        if norm_future_level in ["CRITICAL", "HIGH"] and future_risk_confidence >= 0.4:
            matched_rules.append("RULE_C_HIGH_FUTURE_RISK_SIGNAL")
            if norm_future_level == "CRITICAL":
                state = CrisisOperationalState.CRISIS
                is_crisis_recommended = True
            elif state == CrisisOperationalState.NORMAL:
                state = CrisisOperationalState.ELEVATED
                is_crisis_recommended = True
            reason_parts.append(f"Near-term projection indicates {norm_future_level} risk developing (confidence {future_risk_confidence:.2f})")

        # Check Multi-Signal Convergence (Rule D)
        converging_signals = 0
        rain_24h = telemetry_summary.get("rainfall_24h_mm") or telemetry_summary.get("total_rain_24h_mm") or 0.0
        river_ratio = telemetry_summary.get("river_danger_ratio") or 0.0
        temp_c = telemetry_summary.get("temperature_c") or 0.0
        wind_kmh = telemetry_summary.get("wind_speed_kmh") or 0.0

        if rain_24h >= 64.5:  # IMD heavy rainfall threshold
            converging_signals += 1
        if river_ratio >= 0.90:  # Within 90% of danger level or above
            converging_signals += 1
        if temp_c >= 42.0:  # Severe heatwave threshold
            converging_signals += 1
        if wind_kmh >= 60.0:  # Severe gale / squall threshold
            converging_signals += 1

        if converging_signals >= 2:
            matched_rules.append("RULE_D_MULTI_SIGNAL_CONVERGENCE")
            if state in [CrisisOperationalState.NORMAL, CrisisOperationalState.WATCH]:
                state = CrisisOperationalState.ELEVATED
            is_crisis_recommended = True
            reason_parts.append(f"Multi-signal convergence detected ({converging_signals} severe meteorological/hydrological thresholds exceeded)")

        # Weak Signal Filter
        # If no official warning, current risk is not High/Critical, and future risk is low or uncorroborated
        if not matched_rules:
            if norm_curr_level == "MEDIUM" or norm_future_level == "MEDIUM":
                state = CrisisOperationalState.WATCH
                activation_reason = "Elevated baseline or moderate atmospheric indicator under surveillance"
            else:
                state = CrisisOperationalState.NORMAL
                activation_reason = "Standard baseline monitoring. No active disaster threshold exceeded."
        else:
            activation_reason = "; ".join(reason_parts)

        # User Manual Activation (Rule E)
        if manual_activation:
            matched_rules.append("RULE_E_MANUAL_ACTIVATION")
            state = CrisisOperationalState.CRISIS
            activation_reason = f"Manual Crisis Mode activated by user. ({activation_reason})"

        return state, is_crisis_recommended, activation_reason, matched_rules
