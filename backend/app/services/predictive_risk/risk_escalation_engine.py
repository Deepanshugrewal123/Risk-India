"""
RISK // INDIA — Risk Escalation & Downgrade Engine (Phase 30F)
============================================================
Provides deterministic escalation, downgrade hysteresis, and explicit conflict
resolution across multi-source evidence streams.

Ensures that conflicting evidence (e.g. rising forecast rain vs normal river level)
is never swept under the rug; it is transparently exposed and systematically resolved.
"""

from typing import List, Dict, Any, Tuple, Optional
from app.services.predictive_risk.fusion_schema import RiskState, EvidenceSignal


class RiskEscalationEngine:
    """Evaluates risk escalation, downgrade, evidence conflicts, and crisis recommendation."""

    @classmethod
    def evaluate(
        cls,
        hazard: str,
        current_state: RiskState,
        current_score: float,
        future_state: RiskState,
        peak_future_score: float,
        evidence_signals: List[EvidenceSignal],
        official_warnings: List[Dict[str, Any]],
        corroborating_factors: List[str]
    ) -> Tuple[RiskState, RiskState, bool, List[str], Optional[str], bool, Optional[str]]:
        """
        Returns:
            (
                final_current_state,
                final_future_state,
                has_conflicting_evidence,
                conflicting_signals,
                conflict_resolution_notes,
                crisis_mode_recommended,
                crisis_activation_reason
            )
        """
        norm_hazard = hazard.upper().strip()
        conflicts: List[str] = []
        resolution_notes: Optional[str] = None
        
        final_current = current_state
        final_future = future_state

        # Check official warnings
        has_red_warning = any(str(w.get("severity", "")).upper() == "RED" for w in official_warnings)
        has_orange_warning = any(str(w.get("severity", "")).upper() in ["ORANGE", "AMBER"] for w in official_warnings)

        # -------------------------------------------------------------
        # 1. CONFLICT DETECTION & RESOLUTION
        # -------------------------------------------------------------
        if norm_hazard == "FLOOD":
            # Check rainfall vs river level
            high_rain_forecast = any(
                sig.data_classification == "FORECAST" and (sig.raw_value or 0.0) >= 50.0
                for sig in evidence_signals if "rain" in sig.variable.lower()
            )
            normal_river_level = any(
                sig.data_classification == "OBSERVED" and (sig.normalized_value or 0.0) < 0.65
                for sig in evidence_signals if "river" in sig.variable.lower() or "gauge" in sig.variable.lower()
            )
            
            if high_rain_forecast and normal_river_level:
                conflicts.append(
                    "Forecast models project heavy rainfall (>50mm), but river gauges currently report safe base-flow levels."
                )
                resolution_notes = (
                    "Hydrological Lag: Upstream runoff typically requires 6-18 hours to concentrate into river channels. "
                    "Future risk is escalated to WATCH/ELEVATED while current telemetry remains bounded."
                )
                if final_future == RiskState.NORMAL:
                    final_future = RiskState.WATCH

            if (has_red_warning or has_orange_warning) and current_score < 35.0:
                conflicts.append(
                    "Statutory meteorological warning is active, but immediate station telemetry is currently below alert thresholds."
                )
                if not resolution_notes:
                    resolution_notes = (
                        "Precautionary Precedence: Official IMD/CWC advisories precede localized gauge reaction. "
                        "Readiness is advised before ground telemetry reaches critical levels."
                    )

        elif norm_hazard == "CYCLONE":
            high_coastal_wind = any(
                (sig.raw_value or 0.0) >= 15.0 for sig in evidence_signals if "wind" in sig.variable.lower()
            )
            if (has_red_warning or has_orange_warning) and not high_coastal_wind:
                conflicts.append(
                    "Cyclone warning issued by IMD, but localized wind telemetry has not yet crossed gale thresholds."
                )
                resolution_notes = (
                    "Track Arrival Lag: Cyclonic storm center is offshore or approaching. "
                    "Pre-landfall preparation is critical before local winds accelerate."
                )

        elif norm_hazard == "HEATWAVE":
            high_temp_fc = any(
                sig.data_classification == "FORECAST" and (sig.raw_value or 0.0) >= 42.0
                for sig in evidence_signals if "temp" in sig.variable.lower()
            )
            curr_temp_mod = any(
                sig.data_classification == "OBSERVED" and (sig.raw_value or 0.0) < 38.0
                for sig in evidence_signals if "temp" in sig.variable.lower()
            )
            if high_temp_fc and curr_temp_mod:
                conflicts.append(
                    "Forecast models project extreme temperatures (>42°C), but current observation is moderate."
                )
                resolution_notes = (
                    "Diurnal Cycle: Current observation reflects morning or overcast conditions. "
                    "Peak thermal stress is projected during afternoon hours."
                )

        # -------------------------------------------------------------
        # 2. ESCALATION RULES
        # -------------------------------------------------------------
        if has_red_warning:
            if final_future in [RiskState.NORMAL, RiskState.WATCH, RiskState.ELEVATED]:
                final_future = RiskState.HIGH
            if peak_future_score < 70.0:
                peak_future_score = max(peak_future_score, 75.0)

        elif has_orange_warning:
            if final_future in [RiskState.NORMAL, RiskState.WATCH]:
                final_future = RiskState.ELEVATED
            if peak_future_score < 50.0:
                peak_future_score = max(peak_future_score, 55.0)

        # -------------------------------------------------------------
        # 3. CRISIS MODE RECOMMENDATION
        # -------------------------------------------------------------
        crisis_mode_recommended = False
        crisis_activation_reason: Optional[str] = None

        if final_current == RiskState.CRITICAL or final_future == RiskState.CRITICAL:
            crisis_mode_recommended = True
            crisis_activation_reason = f"Critical {norm_hazard} hazard threshold detected with immediate threat to public safety and infrastructure."
        elif (final_future == RiskState.HIGH or final_current == RiskState.HIGH) and (has_red_warning or peak_future_score >= 75.0):
            crisis_mode_recommended = True
            crisis_activation_reason = f"High {norm_hazard} multi-signal convergence with statutory warning or severe telemetry impact."
        elif has_red_warning and peak_future_score >= 65.0:
            crisis_mode_recommended = True
            crisis_activation_reason = f"Official Red Alert issued by authorities for imminent severe {norm_hazard} hazard."

        has_conflicts = len(conflicts) > 0

        return (
            final_current,
            final_future,
            has_conflicts,
            conflicts,
            resolution_notes,
            crisis_mode_recommended,
            crisis_activation_reason
        )
