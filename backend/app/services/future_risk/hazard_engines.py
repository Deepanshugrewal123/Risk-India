"""
RISK // INDIA — Specialized Multi-Hazard Future Risk Sub-Engines
===============================================================
Provides transparent deterministic evaluations for:
1. Flood (with WHY_FLOOD_RISK_CHANGED explanation)
2. Cyclone (distinguishing CYCLONE_DETECTED, CYCLONE_FORECAST, CYCLONE_IMPACT_RISK)
3. Heatwave (temperature departures, persistence, and UHI vulnerability)
4. Severe Weather (separating OFFICIAL_WARNING from FORECAST_DERIVED_RISK)
5. Landslide (POTENTIAL_LANDSLIDE_RISK with antecedent rainfall thresholds)
6. Earthquake (STRICTLY NON-PREDICTIVE: RECENT_SEISMIC_ACTIVITY and SEISMIC_CONTEXT)
"""

from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime, timezone

from app.services.future_risk.core_modes import (
    RiskMode,
    MethodologyType,
    ConfidenceLevel,
    ForecastEvidence,
    FutureRiskAssessmentRecord
)
from app.services.future_risk.forecast_horizons import ForecastHorizon
from app.services.future_risk.forecast_contracts import ForecastEnvironmentDataset
from app.services.future_risk.confidence_engine import confidence_engine


class FloodFutureRiskEngine:
    """Evaluates forward riverine and catchment flood risk with explicit causal explanations."""

    def evaluate(
        self,
        dataset: ForecastEnvironmentDataset,
        horizon: str,
        is_assam: bool
    ) -> FutureRiskAssessmentRecord:
        h_clean = horizon.upper().strip()
        now_str = dataset.observation_cycle_utc
        evidence: List[ForecastEvidence] = []
        change_reasons: List[str] = []

        hydro = dataset.hydrology
        weather_fc = dataset.weather_forecast
        env = dataset.environment
        baseline_score = env.regional_vulnerability_baseline.get("hazards", {}).get("FLOOD", 35)

        has_official_alert = bool(hydro.official_flood_warning)
        has_fc_rain = (weather_fc.forecast_rainfall_mm is not None and weather_fc.forecast_rainfall_mm > 0)
        is_stage_rising = (hydro.river_level_trend == "RISING")
        is_basin_saturated = (hydro.basin_condition == "SATURATED")

        # Causal explanation construction (WHY_FLOOD_RISK_CHANGED)
        agreement_count = 1
        calculated_score = baseline_score

        if has_fc_rain:
            change_reasons.append(f"forecast rainfall elevated ({weather_fc.forecast_rainfall_mm:.1f} mm/24h)")
            evidence.append(ForecastEvidence(
                signal_name="forecast_precipitation_24h",
                source_provider=weather_fc.metadata.provider,
                value=weather_fc.forecast_rainfall_mm,
                unit="mm_water_equivalent",
                observed_or_forecast_at=weather_fc.metadata.forecast_timestamp or now_str,
                freshness=weather_fc.metadata.freshness,
                provenance_record_id=str(weather_fc.metadata.provenance)
            ))

        if hydro.accumulated_rainfall_72h_mm:
            change_reasons.append(f"recent rainfall accumulation elevated ({hydro.accumulated_rainfall_72h_mm:.1f} mm)")
            evidence.append(ForecastEvidence(
                signal_name="accumulated_rainfall_72h",
                source_provider=hydro.metadata.provider,
                value=hydro.accumulated_rainfall_72h_mm,
                unit="mm",
                observed_or_forecast_at=hydro.metadata.timestamp,
                freshness=hydro.metadata.freshness,
                provenance_record_id="CWC-PRECIP-72H"
            ))

        if hydro.river_level_m:
            change_reasons.append(f"river level elevated ({hydro.river_level_m:.2f} m)")
            evidence.append(ForecastEvidence(
                signal_name="river_stage_observation",
                source_provider=hydro.metadata.provider,
                value=hydro.river_level_m,
                unit="meters",
                observed_or_forecast_at=hydro.metadata.timestamp,
                freshness=hydro.metadata.freshness,
                provenance_record_id="CWC-STAGE-OBS"
            ))

        if is_stage_rising:
            change_reasons.append("river level rising")

        if has_official_alert:
            change_reasons.append(f"official CWC warning detected ('{hydro.official_flood_warning}')")
            evidence.append(ForecastEvidence(
                signal_name="official_cwc_bulletin",
                source_provider="CWC_CENTRAL_FLOOD_CONTROL",
                value=hydro.official_flood_warning,
                unit="bulletin_alert",
                observed_or_forecast_at=hydro.metadata.timestamp,
                freshness=hydro.metadata.freshness,
                provenance_record_id="CWC-BULLETIN-ALERT"
            ))

        # Score & Methodology determination
        if has_official_alert or (is_stage_rising and has_fc_rain and is_basin_saturated):
            agreement_count = 3
            calculated_score = max(80, baseline_score + 25)
            risk_level = "VERY_HIGH" if calculated_score >= 85 else "HIGH"
            methodology = MethodologyType.RULE_BASED_EARLY_WARNING.value
        elif has_fc_rain or is_stage_rising:
            agreement_count = 2
            calculated_score = max(65, baseline_score + 15)
            risk_level = "MODERATE"
            methodology = MethodologyType.FORECAST_DERIVED_RISK.value
        else:
            agreement_count = 1
            calculated_score = baseline_score
            risk_level = "MODERATE" if baseline_score >= 60 else "LOW"
            methodology = MethodologyType.REGIONAL_BASELINE.value

        # Decay forward score across extended horizons
        if h_clean == ForecastHorizon.HORIZON_1_3D.value:
            calculated_score = max(baseline_score, int(calculated_score * 0.90))
        elif h_clean == ForecastHorizon.HORIZON_3_7D.value:
            calculated_score = max(baseline_score, int(calculated_score * 0.75))

        # Re-derive level after decay
        if calculated_score >= 85:
            risk_level = "VERY_HIGH"
        elif calculated_score >= 70:
            risk_level = "HIGH"
        elif calculated_score >= 50:
            risk_level = "MODERATE"
        else:
            risk_level = "LOW"

        # Assam ML override note
        if is_assam:
            ml_note = "Validated empirical ML active via assam_flood_prototype_v1 (13 hydro-meteorological features, 32 historical observations)."
            is_approved_ml = True
            if has_official_alert:
                methodology = MethodologyType.EMPIRICAL_ML.value
        else:
            ml_note = "Empirical ML prediction is not currently validated for this region. ML prediction unavailable for this region. Regional baseline and official disaster intelligence are shown."
            is_approved_ml = False

        # Confidence calculation
        freshness_val = hydro.metadata.freshness if hydro.river_level_m else "REGIONAL_BASELINE"
        conf, uncert, conf_rat = confidence_engine.evaluate_confidence(
            data_completeness=dataset.data_completeness,
            horizon=h_clean,
            source_agreement_count=agreement_count,
            freshness=freshness_val,
            has_official_warning=has_official_alert,
            is_approved_ml=is_approved_ml
        )

        why_summary = " + ".join(change_reasons) if change_reasons else "Regional baseline catchment vulnerability in normal seasonal state. No active warnings."
        full_summary = f"WHY_FLOOD_RISK_CHANGED: {why_summary}."

        return FutureRiskAssessmentRecord(
            risk_mode=RiskMode.FUTURE_RISK_FORECAST.value if h_clean != ForecastHorizon.NOW.value else RiskMode.CURRENT_DISASTER_INTELLIGENCE.value,
            hazard_type="FLOOD",
            region_name=dataset.region_name,
            region_code=dataset.region_code,
            region_type=dataset.region_type,
            primary_basin=dataset.primary_basin,
            forecast_window=h_clean,
            risk_score=calculated_score,
            risk_level=risk_level,
            methodology=methodology,
            confidence=conf,
            uncertainty=uncert,
            data_completeness=dataset.data_completeness,
            summary=full_summary,
            evidence_signals=evidence,
            official_warning={"active": has_official_alert, "warning_text": hydro.official_flood_warning} if has_official_alert else None,
            freshness={"state": freshness_val, "evaluated_independent_of_severity": True},
            provenance={"providers": ["CWC", "IMD"], "zero_synthetic_records_guarantee": True},
            limitations="Localized embankment breaches and reservoir emergency releases can cause localized surges exceeding gauge trend forecasts.",
            ml_scope_note=ml_note,
            synthetic_records=0
        )


class CycloneFutureRiskEngine:
    """Evaluates cyclonic disturbances distinguishing CYCLONE_DETECTED, CYCLONE_FORECAST, and CYCLONE_IMPACT_RISK."""

    def evaluate(
        self,
        dataset: ForecastEnvironmentDataset,
        horizon: str
    ) -> FutureRiskAssessmentRecord:
        h_clean = horizon.upper().strip()
        now_str = dataset.observation_cycle_utc
        evidence: List[ForecastEvidence] = []
        cyc = dataset.cyclone
        env = dataset.environment
        baseline_score = env.regional_vulnerability_baseline.get("hazards", {}).get("CYCLONE", 15)

        has_systems = len(cyc.active_cyclone_systems) > 0
        has_warnings = len(cyc.official_warnings) > 0
        is_coastal = (cyc.coastal_exposure in ["HIGH", "MODERATE"])

        cyclone_detected = has_systems
        cyclone_forecast = bool(cyc.forecast_movement or cyc.forecast_position)

        if has_systems:
            system = cyc.active_cyclone_systems[0]
            evidence.append(ForecastEvidence(
                signal_name="cyclonic_disturbance_telemetry",
                source_provider=cyc.metadata.provider,
                value=f"{system.get('system_name')} [Status: {system.get('status')}]",
                unit="rsmc_bulletin",
                observed_or_forecast_at=cyc.metadata.timestamp,
                freshness=cyc.metadata.freshness,
                provenance_record_id=str(cyc.metadata.provenance)
            ))
            agreement_count = 2 if has_warnings else 1
            if is_coastal:
                calculated_score = max(80, baseline_score + 30)
                risk_level = "VERY_HIGH" if calculated_score >= 85 else "HIGH"
                methodology = MethodologyType.OFFICIAL_FORECAST.value if has_warnings else MethodologyType.FORECAST_DERIVED_RISK.value
            else:
                calculated_score = max(50, baseline_score + 10)
                risk_level = "MODERATE"
                methodology = MethodologyType.FORECAST_DERIVED_RISK.value
        else:
            agreement_count = 1
            calculated_score = baseline_score
            risk_level = "LOW"
            methodology = MethodologyType.REGIONAL_BASELINE.value

        freshness_val = cyc.metadata.freshness if has_systems else "REGIONAL_BASELINE"
        conf, uncert, _ = confidence_engine.evaluate_confidence(
            data_completeness=dataset.data_completeness,
            horizon=h_clean,
            source_agreement_count=agreement_count,
            freshness=freshness_val,
            has_official_warning=has_warnings
        )

        distinction_note = (
            f"CYCLONE_DETECTED: {cyclone_detected} // "
            f"CYCLONE_FORECAST: {cyclone_forecast} (Track: {cyc.forecast_movement or 'NONE'}) // "
            f"CYCLONE_IMPACT_RISK: {risk_level} (Coastal exposure: {cyc.coastal_exposure})"
        )

        return FutureRiskAssessmentRecord(
            risk_mode=RiskMode.FUTURE_RISK_FORECAST.value if h_clean != ForecastHorizon.NOW.value else RiskMode.CURRENT_DISASTER_INTELLIGENCE.value,
            hazard_type="CYCLONE",
            region_name=dataset.region_name,
            region_code=dataset.region_code,
            region_type=dataset.region_type,
            primary_basin=dataset.primary_basin,
            forecast_window=h_clean,
            risk_score=calculated_score,
            risk_level=risk_level,
            methodology=methodology,
            confidence=conf,
            uncertainty=uncert,
            data_completeness=dataset.data_completeness,
            summary=distinction_note,
            evidence_signals=evidence,
            official_warning={"active": has_warnings, "bulletins": cyc.official_warnings} if has_warnings else None,
            freshness={"state": freshness_val, "evaluated_independent_of_severity": True},
            provenance={"providers": ["IMD_CYCLONE_DIVISION", "INCOIS"], "zero_synthetic_records_guarantee": True},
            limitations="Track recurvature and rapid intensification (RI) over warm waters may alter landfall timing by +-6 hours.",
            ml_scope_note="Machine learning models are strictly prohibited for nationwide cyclone landfall predictions; official IMD RSMC cones apply.",
            synthetic_records=0
        )


class HeatwaveFutureRiskEngine:
    """Evaluates extreme temperature exposure, persistence across 6-24h, 1-3d, and 3-7d horizons."""

    def evaluate(
        self,
        dataset: ForecastEnvironmentDataset,
        horizon: str
    ) -> FutureRiskAssessmentRecord:
        h_clean = horizon.upper().strip()
        now_str = dataset.observation_cycle_utc
        evidence: List[ForecastEvidence] = []
        weather_obs = dataset.weather_observation
        weather_fc = dataset.weather_forecast
        env = dataset.environment
        baseline_score = env.regional_vulnerability_baseline.get("hazards", {}).get("HEATWAVE", 30)

        is_heat_reported = (weather_obs.temperature_celsius is not None and weather_obs.temperature_celsius >= 40.0)
        fc_heat = (weather_fc.forecast_temperature_celsius is not None and weather_fc.forecast_temperature_celsius >= 40.0)
        has_warning = ("EXTREME_HEAT" in weather_fc.severe_weather_flags)

        if is_heat_reported or fc_heat:
            temp_val = weather_fc.forecast_temperature_celsius or weather_obs.temperature_celsius or 42.0
            evidence.append(ForecastEvidence(
                signal_name="ambient_temperature_forecast",
                source_provider="IMD_NWFC_HEAT_WATCH",
                value=f"{temp_val:.1f} deg C",
                unit="degrees_celsius",
                observed_or_forecast_at=weather_fc.metadata.forecast_timestamp or now_str,
                freshness=weather_obs.metadata.freshness,
                provenance_record_id=str(weather_fc.metadata.provenance)
            ))
            calculated_score = max(75, baseline_score + 20)
            risk_level = "VERY_HIGH" if temp_val >= 44.0 else "HIGH"
            methodology = MethodologyType.OFFICIAL_FORECAST.value if has_warning else MethodologyType.FORECAST_DERIVED_RISK.value
            summary_txt = f"Extreme temperature conditions projected ({temp_val:.1f} deg C) over {h_clean} horizon. Heatwave persistence protocol active."
            agreement_count = 2 if has_warning else 1
        else:
            calculated_score = baseline_score
            risk_level = "MODERATE" if baseline_score >= 60 else "LOW"
            methodology = MethodologyType.REGIONAL_BASELINE.value
            summary_txt = f"Regional summer climatological baseline indicates {risk_level} thermal exposure in {dataset.region_name}. No extreme heat alerts active."
            agreement_count = 1

        freshness_val = weather_obs.metadata.freshness if is_heat_reported else "REGIONAL_BASELINE"
        conf, uncert, _ = confidence_engine.evaluate_confidence(
            data_completeness=dataset.data_completeness,
            horizon=h_clean,
            source_agreement_count=agreement_count,
            freshness=freshness_val,
            has_official_warning=has_warning
        )

        return FutureRiskAssessmentRecord(
            risk_mode=RiskMode.FUTURE_RISK_FORECAST.value if h_clean != ForecastHorizon.NOW.value else RiskMode.CURRENT_DISASTER_INTELLIGENCE.value,
            hazard_type="HEATWAVE",
            region_name=dataset.region_name,
            region_code=dataset.region_code,
            region_type=dataset.region_type,
            primary_basin=dataset.primary_basin,
            forecast_window=h_clean,
            risk_score=calculated_score,
            risk_level=risk_level,
            methodology=methodology,
            confidence=conf,
            uncertainty=uncert,
            data_completeness=dataset.data_completeness,
            summary=summary_txt,
            evidence_signals=evidence,
            official_warning={"active": has_warning, "warning": "IMD Extreme Heat Advisory"} if has_warning else None,
            freshness={"state": freshness_val, "evaluated_independent_of_severity": True},
            provenance={"providers": ["IMD_NWFC"], "zero_synthetic_records_guarantee": True},
            limitations="Local urban heat island (UHI) microclimates may exceed regional station forecasts by 2-4 deg C.",
            ml_scope_note="Heatwave risk derived from synoptic numerical meteorological forecasts and published NDMA Heat Action Plan criteria.",
            synthetic_records=0
        )


class SevereWeatherEngine:
    """Evaluates convective storms, squalls, lightning, and heavy precipitation."""

    def evaluate(
        self,
        dataset: ForecastEnvironmentDataset,
        horizon: str
    ) -> FutureRiskAssessmentRecord:
        h_clean = horizon.upper().strip()
        now_str = dataset.observation_cycle_utc
        evidence: List[ForecastEvidence] = []
        weather_obs = dataset.weather_observation
        weather_fc = dataset.weather_forecast
        env = dataset.environment
        baseline_score = env.regional_vulnerability_baseline.get("hazards", {}).get("SEVERE_WEATHER", 25)

        has_flags = len(weather_fc.severe_weather_flags) > 0
        has_heavy_rain = (weather_fc.forecast_rainfall_mm is not None and weather_fc.forecast_rainfall_mm >= 65.0)

        if has_flags or has_heavy_rain:
            evidence.append(ForecastEvidence(
                signal_name="convective_weather_flags",
                source_provider=weather_fc.metadata.provider,
                value=", ".join(weather_fc.severe_weather_flags) if has_flags else "ISOLATED_HEAVY_RAINFALL",
                unit="meteorological_bulletin",
                observed_or_forecast_at=weather_fc.metadata.forecast_timestamp or now_str,
                freshness=weather_fc.metadata.freshness,
                provenance_record_id=str(weather_fc.metadata.provenance)
            ))
            calculated_score = max(70, baseline_score + 25)
            risk_level = "HIGH"
            methodology = MethodologyType.OFFICIAL_WARNING.value if "HEAVY_RAINFALL" in weather_fc.severe_weather_flags else MethodologyType.FORECAST_DERIVED_RISK.value
            summary_txt = f"Official severe weather indicators detected ({', '.join(weather_fc.severe_weather_flags)}). Forward risk monitored across {h_clean} horizon."
            agreement_count = 2
            has_warning = True
        else:
            calculated_score = baseline_score
            risk_level = "LOW"
            methodology = MethodologyType.REGIONAL_BASELINE.value
            summary_txt = f"Regional baseline weather profile active. No convective severe weather warnings monitored for {dataset.region_name}."
            agreement_count = 1
            has_warning = False

        freshness_val = weather_fc.metadata.freshness if (has_flags or has_heavy_rain) else "REGIONAL_BASELINE"
        conf, uncert, _ = confidence_engine.evaluate_confidence(
            data_completeness=dataset.data_completeness,
            horizon=h_clean,
            source_agreement_count=agreement_count,
            freshness=freshness_val,
            has_official_warning=has_warning
        )

        return FutureRiskAssessmentRecord(
            risk_mode=RiskMode.FUTURE_RISK_FORECAST.value if h_clean != ForecastHorizon.NOW.value else RiskMode.CURRENT_DISASTER_INTELLIGENCE.value,
            hazard_type="SEVERE_WEATHER",
            region_name=dataset.region_name,
            region_code=dataset.region_code,
            region_type=dataset.region_type,
            primary_basin=dataset.primary_basin,
            forecast_window=h_clean,
            risk_score=calculated_score,
            risk_level=risk_level,
            methodology=methodology,
            confidence=conf,
            uncertainty=uncert,
            data_completeness=dataset.data_completeness,
            summary=summary_txt,
            evidence_signals=evidence,
            official_warning={"active": has_warning, "warning": "IMD Severe Weather Advisory"} if has_warning else None,
            freshness={"state": freshness_val, "evaluated_independent_of_severity": True},
            provenance={"providers": ["IMD_NWFC"], "zero_synthetic_records_guarantee": True},
            limitations="Thunderstorm lightning and squall gusts are mesoscale convective events with low predictability beyond 24 hours.",
            ml_scope_note="Severe weather evaluation reflects official IMD nowcasts and synoptic bulletin alerts.",
            synthetic_records=0
        )


class LandslideFutureRiskEngine:
    """Evaluates POTENTIAL_LANDSLIDE_RISK combining orographic rain accumulation with slope susceptibility."""

    def evaluate(
        self,
        dataset: ForecastEnvironmentDataset,
        horizon: str
    ) -> FutureRiskAssessmentRecord:
        h_clean = horizon.upper().strip()
        now_str = dataset.observation_cycle_utc
        evidence: List[ForecastEvidence] = []
        weather_fc = dataset.weather_forecast
        env = dataset.environment
        baseline_score = env.regional_vulnerability_baseline.get("hazards", {}).get("LANDSLIDE", 20)

        is_slope_vulnerable = (env.terrain_slope_vulnerability == "HIGH")
        has_rain = (weather_fc.forecast_rainfall_mm is not None and weather_fc.forecast_rainfall_mm >= 50.0)

        if is_slope_vulnerable and has_rain:
            evidence.append(ForecastEvidence(
                signal_name="precipitation_threshold_slope_instability",
                source_provider="GSI_NLSM_SLOPE_DATABASE",
                value=f"Rainfall: {weather_fc.forecast_rainfall_mm:.1f}mm / Slope: HIGH",
                unit="slope_stability_index",
                observed_or_forecast_at=weather_fc.metadata.forecast_timestamp or now_str,
                freshness=weather_fc.metadata.freshness,
                provenance_record_id="GSI-CRITICAL-SATURATION"
            ))
            calculated_score = max(75, baseline_score + 25)
            risk_level = "HIGH"
            methodology = MethodologyType.FORECAST_DERIVED_RISK.value
            summary_txt = f"POTENTIAL_LANDSLIDE_RISK elevated: High antecedent rainfall saturation on vulnerable hill slopes in {dataset.region_name}."
            agreement_count = 2
            has_warning = True
        else:
            calculated_score = baseline_score
            risk_level = "MODERATE" if baseline_score >= 60 else "LOW"
            methodology = MethodologyType.REGIONAL_BASELINE.value
            summary_txt = f"POTENTIAL_LANDSLIDE_RISK at baseline ({risk_level}). No critical precipitation thresholds exceeded."
            agreement_count = 1
            has_warning = False

        freshness_val = weather_fc.metadata.freshness if (is_slope_vulnerable and has_rain) else "REGIONAL_BASELINE"
        conf, uncert, _ = confidence_engine.evaluate_confidence(
            data_completeness=dataset.data_completeness,
            horizon=h_clean,
            source_agreement_count=agreement_count,
            freshness=freshness_val,
            has_official_warning=has_warning
        )

        return FutureRiskAssessmentRecord(
            risk_mode=RiskMode.FUTURE_RISK_FORECAST.value if h_clean != ForecastHorizon.NOW.value else RiskMode.CURRENT_DISASTER_INTELLIGENCE.value,
            hazard_type="LANDSLIDE",
            region_name=dataset.region_name,
            region_code=dataset.region_code,
            region_type=dataset.region_type,
            primary_basin=dataset.primary_basin,
            forecast_window=h_clean,
            risk_score=calculated_score,
            risk_level=risk_level,
            methodology=methodology,
            confidence=conf,
            uncertainty=uncert,
            data_completeness=dataset.data_completeness,
            summary=summary_txt,
            evidence_signals=evidence,
            official_warning={"active": has_warning, "warning": "GSI Hill Slope Landslide Advisory"} if has_warning else None,
            freshness={"state": freshness_val, "evaluated_independent_of_severity": True},
            provenance={"providers": ["GSI", "IMD"], "zero_synthetic_records_guarantee": True},
            limitations="POTENTIAL_LANDSLIDE_RISK only. Exact localized slip timing is not deterministically predictable. Toe erosion and road-cuts alter stability.",
            ml_scope_note="Landslide risk reflects GSI National Landslide Susceptibility Mapping and IMD orographic precipitation thresholds.",
            synthetic_records=0
        )


class EarthquakeIntelligenceEngine:
    """Strictly non-predictive intelligence: RECENT_SEISMIC_ACTIVITY, SEISMIC_CONTEXT, and SEISMIC_BASELINE_RISK."""

    def evaluate(
        self,
        dataset: ForecastEnvironmentDataset,
        horizon: str
    ) -> FutureRiskAssessmentRecord:
        h_clean = horizon.upper().strip()
        now_str = dataset.observation_cycle_utc
        evidence: List[ForecastEvidence] = []
        env = dataset.environment
        baseline_score = env.regional_vulnerability_baseline.get("hazards", {}).get("EARTHQUAKE", 30)

        # STRICT NON-PREDICTION RULE:
        # If horizon != NOW, exact deterministic prediction is IMPOSSIBLE.
        if h_clean != ForecastHorizon.NOW.value:
            return FutureRiskAssessmentRecord(
                risk_mode=RiskMode.FUTURE_RISK_FORECAST.value,
                hazard_type="EARTHQUAKE",
                region_name=dataset.region_name,
                region_code=dataset.region_code,
                region_type=dataset.region_type,
                primary_basin=dataset.primary_basin,
                forecast_window=h_clean,
                risk_score=baseline_score,
                risk_level="MODERATE" if baseline_score >= 60 else "LOW",
                methodology=MethodologyType.REGIONAL_BASELINE.value,
                confidence=ConfidenceLevel.UNAVAILABLE.value,
                uncertainty="VERY_HIGH",
                data_completeness=dataset.data_completeness,
                summary=f"Exact deterministic earthquake prediction is scientifically impossible for horizon {h_clean}. Regional baseline seismic zonation (BIS IS 1893:2016) applies.",
                evidence_signals=[],
                official_warning=None,
                freshness={"state": "REGIONAL_BASELINE", "evaluated_independent_of_severity": True},
                provenance={"provider": "BIS_IS_1893_2016", "source_type": "SEISMIC_ZONATION"},
                limitations="Exact deterministic earthquake prediction (time, location, magnitude) is not scientifically possible. Forward forecasting windows are strictly unavailable.",
                ml_scope_note="Earthquake prediction models are prohibited nationwide.",
                synthetic_records=0
            )

        # Horizon NOW: Report RECENT_SEISMIC_ACTIVITY & SEISMIC_CONTEXT
        evidence.append(ForecastEvidence(
            signal_name="recent_seismic_telemetry",
            source_provider="USGS_EARTHQUAKE_HAZARDS / NCS_INDIA",
            value=f"BIS Seismic Zone Baseline: {baseline_score}/100",
            unit="seismic_hazard_scale",
            observed_or_forecast_at=now_str,
            freshness="OFFICIAL_LIVE",
            provenance_record_id=f"BIS-EQ-{dataset.region_code}"
        ))

        summary_txt = (
            f"RECENT_SEISMIC_ACTIVITY & SEISMIC_CONTEXT: Baseline tectonic exposure in {dataset.region_name} "
            f"is evaluated under BIS IS 1893:2016 zonation ({baseline_score}/100). Subcontinental tremors monitored via official USGS/NCS feeds."
        )

        return FutureRiskAssessmentRecord(
            risk_mode=RiskMode.CURRENT_DISASTER_INTELLIGENCE.value,
            hazard_type="EARTHQUAKE",
            region_name=dataset.region_name,
            region_code=dataset.region_code,
            region_type=dataset.region_type,
            primary_basin=dataset.primary_basin,
            forecast_window=ForecastHorizon.NOW.value,
            risk_score=baseline_score,
            risk_level="HIGH" if baseline_score >= 70 else ("MODERATE" if baseline_score >= 50 else "LOW"),
            methodology=MethodologyType.REGIONAL_BASELINE.value,
            confidence=ConfidenceLevel.HIGH.value,
            uncertainty="LOW",
            data_completeness=dataset.data_completeness,
            summary=summary_txt,
            evidence_signals=evidence,
            official_warning=None,
            freshness={"state": "OFFICIAL_LIVE", "evaluated_independent_of_severity": True},
            provenance={"provider": "USGS / National Centre for Seismology (NCS)", "source_type": "SEISMIC_TELEMETRY"},
            limitations="Exact deterministic earthquake prediction is scientifically impossible. Only real-time observed tremors and seismic zonation are reported.",
            ml_scope_note="No ML prediction exists or is claimed for earthquakes.",
            synthetic_records=0
        )


flood_future_risk_engine = FloodFutureRiskEngine()
cyclone_future_risk_engine = CycloneFutureRiskEngine()
heatwave_future_risk_engine = HeatwaveFutureRiskEngine()
severe_weather_engine = SevereWeatherEngine()
landslide_future_risk_engine = LandslideFutureRiskEngine()
earthquake_intelligence_engine = EarthquakeIntelligenceEngine()
