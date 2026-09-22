"""
RISK // INDIA — Qualitative Confidence Engine (Phase 30F)
=========================================================
Computes qualitative assessment confidence strictly as LOW, MODERATE, or HIGH.
CRITICAL INVARIANT:
Never output numeric pseudo-probabilities (e.g., '87% chance', '92% probability').
Confidence reflects empirical evidence corroboration, source diversity, and freshness.
"""

from typing import List, Dict, Any, Optional
from app.services.predictive_risk.fusion_schema import ConfidenceLevel, EvidenceSignal


class QualitativeConfidenceEngine:
    """Evaluates qualitative confidence of future risk assessments."""

    @staticmethod
    def evaluate(
        hazard: str,
        signals: List[EvidenceSignal],
        has_official_warning: bool,
        has_live_telemetry: bool,
        has_forecast_inputs: bool,
        is_assam_ml: bool = False,
        source_disagreement: bool = False
    ) -> ConfidenceLevel:
        """
        Calculates qualitative confidence.
        """
        norm_hazard = hazard.upper().strip()

        # Earthquake Invariant: Future earthquake forecasting is impossible; confidence is LOW
        if norm_hazard == "EARTHQUAKE":
            return ConfidenceLevel.LOW

        # If evidence sources actively disagree, confidence is capped at MODERATE or LOW
        if source_disagreement:
            return ConfidenceLevel.LOW if not has_official_warning else ConfidenceLevel.MODERATE

        # Count corroborated evidence channels
        channels = 0
        if has_live_telemetry:
            channels += 1
        if has_forecast_inputs:
            channels += 1
        if has_official_warning:
            channels += 2  # Statutory warning carries high evidential weight
        if is_assam_ml:
            channels += 1

        if len(signals) >= 4 and channels >= 3 and not source_disagreement:
            return ConfidenceLevel.HIGH
        elif len(signals) >= 2 and channels >= 2:
            return ConfidenceLevel.MODERATE
        else:
            return ConfidenceLevel.LOW
