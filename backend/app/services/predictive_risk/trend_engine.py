"""
RISK // INDIA — Risk Trend Engine (Phase 30F)
=============================================
Calculates directional trajectory: RISING, STABLE, DECLINING, VOLATILE, or INSUFFICIENT_DATA.
Never manufactures a trend when evidence is insufficient.
"""

from typing import List, Dict, Any, Optional
from app.services.predictive_risk.fusion_schema import TrendState, RiskState


class RiskTrendEngine:
    """Evaluates the directional momentum of future disaster risk."""

    @staticmethod
    def evaluate(
        current_score: float,
        future_scores: List[float],
        hazard: str,
        has_insufficient_evidence: bool = False
    ) -> TrendState:
        """
        Determines the directional trend across projection horizons.
        """
        norm_hazard = hazard.upper().strip()

        # Earthquake Invariant: Earthquakes do not have predictable future trajectories
        if norm_hazard == "EARTHQUAKE":
            return TrendState.STABLE

        if has_insufficient_evidence or not future_scores:
            return TrendState.INSUFFICIENT_DATA

        max_future = max(future_scores)
        min_future = min(future_scores)
        delta = max_future - current_score

        # Check for volatility: large swings up and down
        if len(future_scores) >= 3:
            diffs = [future_scores[i+1] - future_scores[i] for i in range(len(future_scores)-1)]
            has_positive = any(d >= 15.0 for d in diffs)
            has_negative = any(d <= -15.0 for d in diffs)
            if has_positive and has_negative:
                return TrendState.VOLATILE

        if delta >= 12.0:
            return TrendState.RISING
        elif current_score - min_future >= 12.0 and max_future <= current_score:
            return TrendState.DECLINING
        else:
            return TrendState.STABLE
