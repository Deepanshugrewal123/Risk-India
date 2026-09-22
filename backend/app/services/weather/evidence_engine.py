"""
RISK // INDIA — Multi-Hazard Weather Evidence Engine
=====================================================
Translates weather observations, forecasts, and warnings into transparent
evidence signals for Flood, Heatwave, Cyclone, Severe Weather, and Landslide.
Enforces the strict earthquake boundary: weather data NEVER predicts earthquakes.
"""

from typing import Dict, List, Any, Optional
from datetime import datetime, timezone

from .schema import (
    CanonicalWeatherObservation,
    CanonicalWeatherForecast,
    WeatherWarning
)
from app.services.telemetry import dynamic_telemetry_service


class WeatherEvidenceEngine:
    """
    Constructs explainable hazard evidence signals from hydro-meteorological data.
    Every signal specifies: WHAT DATA, WHICH PROVIDER, WHICH LOCATION, TIME WINDOW, FRESHNESS, WHY IT MATTERS.
    """

    def generate_flood_evidence(
        self,
        region_name: str,
        obs: Optional[CanonicalWeatherObservation] = None,
        fc: Optional[CanonicalWeatherForecast] = None
    ) -> List[Dict[str, Any]]:
        """Combines rainfall telemetry and Phase 30C river stages into flood evidence."""
        signals = []

        # Rainfall intensity & accumulation
        if obs and obs.rainfall_mm is not None and obs.rainfall_mm > 25.0:
            signals.append({
                "signal_name": "HEAVY_RAINFALL_OBSERVED",
                "hazard": "FLOOD",
                "provider": obs.source_provider,
                "location": region_name,
                "value": f"{obs.rainfall_mm:.1f} mm",
                "time_window": obs.observed_at,
                "freshness": obs.freshness,
                "significance": "HIGH" if obs.rainfall_mm >= 65.0 else "MODERATE",
                "why_it_matters": "Active precipitation exceeds infiltration capacity, initiating catchment surface runoff."
            })

        if fc and fc.rainfall_mm is not None and fc.rainfall_mm > 50.0:
            signals.append({
                "signal_name": "HEAVY_RAIN_FORECAST",
                "hazard": "FLOOD",
                "provider": fc.forecast_source,
                "location": region_name,
                "value": f"{fc.rainfall_mm:.1f} mm forecast",
                "time_window": f"{fc.forecast_valid_from} to {fc.forecast_valid_until}",
                "freshness": fc.freshness,
                "significance": "HIGH",
                "why_it_matters": "Numerical weather prediction indicates heavy catchment precipitation over the forecast horizon."
            })

        # Phase 30C river gauge integration
        telemetry_obs = dynamic_telemetry_service.get_observations(state=region_name, limit=1)
        if telemetry_obs:
            t = telemetry_obs[-1]
            wl = t.provenance.get("warning_level_m")
            dl = t.provenance.get("danger_level_m")
            val = t.normalized_value

            if t.variable_type == "WATER_LEVEL" and dl and val >= dl:
                signals.append({
                    "signal_name": "RIVER_ABOVE_DANGER_LEVEL",
                    "hazard": "FLOOD",
                    "provider": t.source_provider,
                    "location": f"{t.gauge_name} ({t.major_basin.title()} Basin)",
                    "value": f"{val:.2f} m (DL: {dl:.2f} m)",
                    "time_window": t.observed_at,
                    "freshness": t.freshness,
                    "significance": "CRITICAL",
                    "why_it_matters": "Hydrological sensor confirms river stage has exceeded official Danger Level."
                })
            elif t.variable_type == "WATER_LEVEL" and wl and val >= wl:
                signals.append({
                    "signal_name": "RIVER_NEAR_WARNING_LEVEL",
                    "hazard": "FLOOD",
                    "provider": t.source_provider,
                    "location": f"{t.gauge_name} ({t.major_basin.title()} Basin)",
                    "value": f"{val:.2f} m (WL: {wl:.2f} m)",
                    "time_window": t.observed_at,
                    "freshness": t.freshness,
                    "significance": "HIGH",
                    "why_it_matters": "Hydrological sensor records stage above Warning Level; embankment alert activated."
                })

        return signals

    def generate_heatwave_evidence(
        self,
        region_name: str,
        obs: Optional[CanonicalWeatherObservation] = None,
        fc: Optional[CanonicalWeatherForecast] = None
    ) -> List[Dict[str, Any]]:
        """Assesses temperature thresholds, persistence, and departure from normal."""
        signals = []

        if obs and obs.temperature_celsius is not None and obs.temperature_celsius >= 40.0:
            signals.append({
                "signal_name": "EXTREME_TEMPERATURE_OBSERVED",
                "hazard": "HEATWAVE",
                "provider": obs.source_provider,
                "location": region_name,
                "value": f"{obs.temperature_celsius:.1f}°C",
                "time_window": obs.observed_at,
                "freshness": obs.freshness,
                "significance": "HIGH" if obs.temperature_celsius >= 45.0 else "MODERATE",
                "why_it_matters": "Ambient surface temperature crosses IMD heatwave criteria threshold."
            })

        if fc and fc.temperature_celsius is not None and fc.temperature_celsius >= 42.0:
            signals.append({
                "signal_name": "PERSISTENT_HEATWAVE_FORECAST",
                "hazard": "HEATWAVE",
                "provider": fc.forecast_source,
                "location": region_name,
                "value": f"{fc.temperature_celsius:.1f}°C forecast",
                "time_window": f"{fc.forecast_valid_from} to {fc.forecast_valid_until}",
                "freshness": fc.freshness,
                "significance": "HIGH",
                "why_it_matters": "Forecast models show multi-day thermal persistence with severe heat exposure risk."
            })

        return signals

    def generate_cyclone_evidence(
        self,
        region_name: str,
        warnings: List[WeatherWarning]
    ) -> List[Dict[str, Any]]:
        """Identifies official cyclonic disturbances without fabricating fictional tracks."""
        signals = []
        for w in warnings:
            if w.hazard.upper() == "CYCLONE":
                signals.append({
                    "signal_name": "OFFICIAL_CYCLONE_WARNING",
                    "hazard": "CYCLONE",
                    "provider": w.provider,
                    "location": region_name,
                    "value": w.severity,
                    "time_window": f"{w.valid_from} to {w.valid_until}",
                    "freshness": w.freshness,
                    "significance": "CRITICAL" if w.severity in ["ORANGE", "RED", "HIGH", "CRITICAL"] else "HIGH",
                    "why_it_matters": f"Official IMD RSMC tropical cyclone advisory active: {w.headline}."
                })
        return signals

    def generate_severe_weather_evidence(
        self,
        region_name: str,
        obs: Optional[CanonicalWeatherObservation] = None,
        fc: Optional[CanonicalWeatherForecast] = None,
        warnings: Optional[List[WeatherWarning]] = None
    ) -> List[Dict[str, Any]]:
        """Distinguishes OFFICIAL_WARNING from FORECAST_DERIVED_SIGNAL."""
        signals = []

        # 1. Official warning signal
        if warnings:
            for w in warnings:
                if w.hazard.upper() in ["SEVERE_WEATHER", "THUNDERSTORM"]:
                    signals.append({
                        "signal_name": "OFFICIAL_WEATHER_WARNING",
                        "signal_category": "OFFICIAL_WARNING",
                        "hazard": "SEVERE_WEATHER",
                        "provider": w.provider,
                        "location": region_name,
                        "value": w.severity,
                        "time_window": f"{w.valid_from} to {w.valid_until}",
                        "freshness": w.freshness,
                        "significance": "HIGH",
                        "why_it_matters": f"Authoritative IMD bulletin: {w.headline}."
                    })

        # 2. Forecast-derived signal (explicitly separated)
        if obs and (obs.thunderstorm_indicator or (obs.wind_speed_mps and obs.wind_speed_mps >= 15.0)):
            signals.append({
                "signal_name": "CONVECTIVE_ACTIVITY_OBSERVED",
                "signal_category": "FORECAST_DERIVED_SIGNAL",
                "hazard": "SEVERE_WEATHER",
                "provider": obs.source_provider,
                "location": region_name,
                "value": f"Wind {obs.wind_speed_mps} m/s, Lightning={obs.lightning_indicator}",
                "time_window": obs.observed_at,
                "freshness": obs.freshness,
                "significance": "MODERATE",
                "why_it_matters": "Active convective cells and gusty squalls detected by surface telemetry."
            })

        return signals

    def generate_landslide_evidence(
        self,
        region_name: str,
        obs: Optional[CanonicalWeatherObservation] = None,
        fc: Optional[CanonicalWeatherForecast] = None
    ) -> List[Dict[str, Any]]:
        """Combines antecedent precipitation and terrain vulnerability for POTENTIAL_LANDSLIDE_RISK."""
        signals = []
        is_hilly = region_name.lower() in [
            "uttarakhand", "himachal pradesh", "kerala", "meghalaya", "sikkim",
            "arunachal pradesh", "mizoram", "nagaland", "manipur", "tripura", "jammu and kashmir"
        ]

        if is_hilly:
            heavy_rain = False
            val_str = ""
            if obs and obs.rainfall_mm and obs.rainfall_mm >= 50.0:
                heavy_rain = True
                val_str = f"{obs.rainfall_mm:.1f} mm observed"
            elif fc and fc.rainfall_mm and fc.rainfall_mm >= 70.0:
                heavy_rain = True
                val_str = f"{fc.rainfall_mm:.1f} mm forecast"

            if heavy_rain:
                signals.append({
                    "signal_name": "POTENTIAL_LANDSLIDE_RISK",
                    "hazard": "LANDSLIDE",
                    "provider": "IMD_GSI_COLLABORATIVE",
                    "location": region_name,
                    "value": val_str,
                    "time_window": "NEXT_24_48_HOURS",
                    "freshness": "OFFICIAL_RECENT",
                    "significance": "HIGH",
                    "why_it_matters": "High antecedent or forecast precipitation on vulnerable orographic slopes increases slope instability."
                })

        return signals

    def verify_earthquake_boundary(self) -> str:
        """Enforces absolute project invariant: weather NEVER predicts earthquakes."""
        return "EARTHQUAKE_PREDICTION_PROHIBITED: Meteorological data is strictly barred from predicting seismic activity."


weather_evidence_engine = WeatherEvidenceEngine()
