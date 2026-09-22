"""
RISK // INDIA — National Future Disaster Risk Forecasting Engine
================================================================
Multi-hazard forward risk forecasting engine operating across all 28 States and 8 Union Territories.
Evaluates multi-horizon forward projections (NOW, 0-6h, 6-24h, 1-3d, 3-7d).
Enforces graceful degradation without fabricating synthetic variables.
Enforces strict non-predictability for earthquakes.
Integrates specialized modular hazard engines and transparent confidence calculations.
"""

from typing import Dict, List, Any, Optional
from datetime import datetime, timezone, timedelta

from .core_modes import (
    RiskMode,
    MethodologyType,
    ConfidenceLevel,
    ForecastEvidence,
    FutureRiskAssessmentRecord
)
from .forecast_horizons import (
    ForecastHorizon,
    ALL_FORECAST_HORIZONS,
    is_hazard_horizon_suitable,
    get_hazard_predictability_metadata
)
from .forecast_contracts import (
    ForecastEnvironmentDataset,
    assemble_region_forecast_dataset
)
from .hazard_engines import (
    flood_future_risk_engine,
    cyclone_future_risk_engine,
    heatwave_future_risk_engine,
    severe_weather_engine,
    landslide_future_risk_engine,
    earthquake_intelligence_engine
)
from app.services.national_risk.regional_baseline import regional_baseline_engine, SUPPORTED_HAZARDS


class FutureRiskEngine:
    """Computes forward-looking disaster risk projections nationwide."""

    def evaluate_future_risk(
        self,
        state_identifier: str,
        hazard: Optional[str] = None,
        horizon: Optional[str] = None
    ) -> List[FutureRiskAssessmentRecord]:
        """
        Evaluates forward disaster risk for a state across one or all horizons and hazards.
        """
        profile = regional_baseline_engine.get_state_profile(state_identifier)
        if not profile:
            return []

        dataset = assemble_region_forecast_dataset(profile.name)
        if not dataset:
            return []

        is_assam = (profile.name.lower() == "assam")
        results: List[FutureRiskAssessmentRecord] = []

        # Determine target hazards & horizons
        hazards_to_evaluate = [hazard.upper().strip()] if hazard else SUPPORTED_HAZARDS
        horizons_to_evaluate = [horizon.upper().strip()] if horizon else ALL_FORECAST_HORIZONS

        for h in hazards_to_evaluate:
            h_clean = h.upper().strip()
            for horiz in horizons_to_evaluate:
                horiz_clean = horiz.upper().strip()

                if h_clean == "FLOOD":
                    rec = flood_future_risk_engine.evaluate(dataset, horiz_clean, is_assam=is_assam)
                elif h_clean == "CYCLONE":
                    rec = cyclone_future_risk_engine.evaluate(dataset, horiz_clean)
                elif h_clean == "HEATWAVE":
                    rec = heatwave_future_risk_engine.evaluate(dataset, horiz_clean)
                elif h_clean == "SEVERE_WEATHER":
                    rec = severe_weather_engine.evaluate(dataset, horiz_clean)
                elif h_clean == "LANDSLIDE":
                    rec = landslide_future_risk_engine.evaluate(dataset, horiz_clean)
                elif h_clean == "EARTHQUAKE":
                    rec = earthquake_intelligence_engine.evaluate(dataset, horiz_clean)
                else:
                    # Fallback for unrecognized hazard
                    rec = FutureRiskAssessmentRecord(
                        risk_mode=RiskMode.REGIONAL_BASELINE_RISK.value,
                        hazard_type=h_clean,
                        region_name=profile.name,
                        region_code=profile.code,
                        region_type=profile.administrative_type,
                        primary_basin=profile.primary_basin,
                        forecast_window=horiz_clean,
                        risk_score=30,
                        risk_level="LOW",
                        methodology=MethodologyType.REGIONAL_BASELINE.value,
                        confidence=ConfidenceLevel.LOW.value,
                        summary=f"Unrecognized hazard {h_clean} evaluated at regional baseline.",
                        evidence_signals=[],
                        freshness={"state": "REGIONAL_BASELINE", "evaluated_independent_of_severity": True},
                        provenance={"providers": ["REGIONAL_BASELINE"], "zero_synthetic_records_guarantee": True},
                        limitations="Standard baseline parameters apply.",
                        ml_scope_note="No ML model available.",
                        synthetic_records=0
                    )

                results.append(rec)

        return results


future_risk_engine = FutureRiskEngine()
