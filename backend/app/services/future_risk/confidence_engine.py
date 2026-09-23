"""
RISK // INDIA — Confidence & Multi-Source Corroboration Engine
=============================================================
Calculates transparent qualitative confidence and uncertainty ratings for
future disaster risk assessments.

Scientific Constraints:
- Qualitative confidence (LOW, MODERATE, HIGH) is explicitly NOT a statistical probability.
- Multi-source corroboration strengthens evidence weight without fabricating numerical probability intervals.
- Factors evaluated:
  1. Data completeness (ratio of available required variables)
  2. Source authority and reliability
  3. Forecast horizon lead time (uncertainty expands with lead time)
  4. Multi-source agreement (e.g., IMD forecast + CWC stage + official warning)
  5. Observation freshness
  6. Official administrative warning presence
  7. ML validation status (Assam prototype vs baseline fallback)
"""

from typing import Dict, Any, Tuple
from app.services.future_risk.forecast_horizons import ForecastHorizon


class ConfidenceEngine:
    """Computes qualitative confidence, uncertainty, and corroboration ratings."""

    def evaluate_confidence(
        self,
        data_completeness: float,
        horizon: str,
        source_agreement_count: int = 1,
        freshness: str = "OFFICIAL_LIVE",
        has_official_warning: bool = False,
        is_approved_ml: bool = False
    ) -> Tuple[str, str, str]:
        """
        Returns:
            (confidence_level, uncertainty_level, confidence_rationale)
        """
        score = 0.0

        # 1. Data Completeness Contribution (0 - 30 points)
        score += min(30.0, data_completeness * 30.0)

        # 2. Source Agreement / Multi-Source Corroboration (0 - 25 points)
        if source_agreement_count >= 3:
            score += 25.0
        elif source_agreement_count == 2:
            score += 18.0
        else:
            score += 10.0

        # 3. Official Warning Presence (0 - 20 points)
        if has_official_warning:
            score += 20.0
        else:
            score += 8.0

        # 4. Observation Freshness (0 - 15 points)
        if freshness in ["LIVE", "OFFICIAL_LIVE", "LIVE_REALTIME"]:
            score += 15.0
        elif freshness in ["RECENT", "OFFICIAL_RECENT", "ACTIVE_HOURLY"]:
            score += 10.0
        elif freshness == "CACHED":
            score += 6.0
        elif freshness == "STALE":
            score += 2.0
        else:  # REGIONAL_BASELINE
            score += 8.0

        # 5. Lead Time Horizon Penalty (0 - 10 points)
        h_clean = horizon.upper().strip()
        if h_clean == ForecastHorizon.NOW.value:
            score += 10.0
        elif h_clean == ForecastHorizon.HORIZON_0_6H.value:
            score += 8.0
        elif h_clean == ForecastHorizon.HORIZON_6_24H.value:
            score += 6.0
        elif h_clean == ForecastHorizon.HORIZON_1_3D.value:
            score += 3.0
        else:  # 3_7_DAYS
            score += 0.0

        # 6. Approved ML Inference Bonus (risk_india_flood_v1 / calibrated corridor)
        if is_approved_ml:
            score += 5.0

        # Map to qualitative confidence (LOW, MODERATE, HIGH)
        if score >= 75.0:
            confidence = "HIGH"
            uncertainty = "LOW"
            rationale = (
                f"High confidence ({score:.0f}/100) supported by comprehensive data completeness ({data_completeness*100:.0f}%), "
                f"multi-source corroboration ({source_agreement_count} sources), and fresh official telemetry."
            )
        elif score >= 50.0:
            confidence = "MODERATE"
            uncertainty = "MODERATE"
            rationale = (
                f"Moderate confidence ({score:.0f}/100) based on partial telemetry ({data_completeness*100:.0f}%) "
                f"and standard synoptic forecast lead time ({h_clean})."
            )
        else:
            confidence = "LOW"
            uncertainty = "HIGH"
            rationale = (
                f"Low confidence ({score:.0f}/100) due to limited real-time observations, extended lead time ({h_clean}), "
                "or reliance on baseline climatological exposure."
            )

        # For 3-7 day extended outlooks, meteorological uncertainty is naturally elevated
        if h_clean == ForecastHorizon.HORIZON_3_7D.value:
            uncertainty = "VERY_HIGH" if score < 50.0 else "HIGH"

        return confidence, uncertainty, rationale


confidence_engine = ConfidenceEngine()
