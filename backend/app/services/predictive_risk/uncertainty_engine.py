"""
RISK // INDIA — Predictive Uncertainty Engine (Phase 30F)
=========================================================
Computes qualitative projection uncertainty strictly as LOW, MODERATE, HIGH, or VERY_HIGH.
Uncertainty expands with forecast lead time, stale data, source disagreement,
and data gaps. Longer horizons must never be presented as more certain.
"""

from typing import List, Dict, Any, Optional
from app.services.predictive_risk.fusion_schema import UncertaintyLevel


class PredictiveUncertaintyEngine:
    """Evaluates projection uncertainty based on lead time, freshness, and evidence agreement."""

    @staticmethod
    def evaluate(
        horizon: str,
        hazard: str,
        overall_freshness: str,
        has_source_disagreement: bool = False,
        missing_critical_signals: bool = False
    ) -> UncertaintyLevel:
        """
        Calculates qualitative uncertainty across lead times and data conditions.
        """
        norm_horizon = horizon.upper().strip().replace("-", "_")
        norm_hazard = hazard.upper().strip()

        # Earthquake Invariant: Tectonic rupture is non-predictable; uncertainty is VERY_HIGH
        if norm_hazard == "EARTHQUAKE":
            return UncertaintyLevel.VERY_HIGH

        # Baseline uncertainty based strictly on forecast lead time
        if norm_horizon in ["NOW", "CURRENT"]:
            base_uncertainty = UncertaintyLevel.LOW if overall_freshness == "OFFICIAL_LIVE" else UncertaintyLevel.MODERATE
        elif norm_horizon in ["0_6H", "0_6_HOURS", "0-6H"]:
            base_uncertainty = UncertaintyLevel.LOW if overall_freshness == "OFFICIAL_LIVE" else UncertaintyLevel.MODERATE
        elif norm_horizon in ["6_24H", "6_24_HOURS", "6-24H"]:
            base_uncertainty = UncertaintyLevel.MODERATE
        elif norm_horizon in ["1_3D", "1_3_DAYS", "1-3D"]:
            base_uncertainty = UncertaintyLevel.HIGH
        else:  # 3-7 Days
            base_uncertainty = UncertaintyLevel.VERY_HIGH

        # Lead time uncertainty escalation rules
        if has_source_disagreement:
            if base_uncertainty == UncertaintyLevel.LOW:
                base_uncertainty = UncertaintyLevel.MODERATE
            elif base_uncertainty == UncertaintyLevel.MODERATE:
                base_uncertainty = UncertaintyLevel.HIGH
            else:
                base_uncertainty = UncertaintyLevel.VERY_HIGH

        if missing_critical_signals or overall_freshness == "STALE":
            if base_uncertainty == UncertaintyLevel.LOW:
                base_uncertainty = UncertaintyLevel.MODERATE
            elif base_uncertainty == UncertaintyLevel.MODERATE:
                base_uncertainty = UncertaintyLevel.HIGH
            else:
                base_uncertainty = UncertaintyLevel.VERY_HIGH

        return base_uncertainty
