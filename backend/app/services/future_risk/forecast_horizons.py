"""
RISK // INDIA — Forecast Horizons & Hazard Predictability Constraints
=====================================================================
Defines standardized forecast horizons and scientifically grounded predictability
rules for each core hazard. Enforces strict non-predictability constraints for earthquakes.
"""

from enum import Enum
from typing import Dict, List, Any


class ForecastHorizon(str, Enum):
    NOW = "NOW"
    HORIZON_0_6H = "0_6_HOURS"
    HORIZON_6_24H = "6_24_HOURS"
    HORIZON_1_3D = "1_3_DAYS"
    HORIZON_3_7D = "3_7_DAYS"


ALL_FORECAST_HORIZONS = [
    ForecastHorizon.NOW.value,
    ForecastHorizon.HORIZON_0_6H.value,
    ForecastHorizon.HORIZON_6_24H.value,
    ForecastHorizon.HORIZON_1_3D.value,
    ForecastHorizon.HORIZON_3_7D.value
]

HAZARD_PREDICTABILITY_RULES: Dict[str, Dict[str, Any]] = {
    "FLOOD": {
        "suitable_horizons": [
            ForecastHorizon.HORIZON_0_6H.value,
            ForecastHorizon.HORIZON_6_24H.value,
            ForecastHorizon.HORIZON_1_3D.value,
            ForecastHorizon.HORIZON_3_7D.value
        ],
        "required_inputs": [
            "rainfall_forecast",
            "accumulated_rainfall",
            "river_stage_observation",
            "river_stage_trend",
            "basin_vulnerability"
        ],
        "predictability_basis": "Hydrological lag and catchment routing permit 6-24h and 1-3d stage forecasts.",
        "scientific_disclaimer": "Local breach dynamics and dam spillway releases may cause localized surges beyond gauge trend forecasts."
    },
    "CYCLONE": {
        "suitable_horizons": [
            ForecastHorizon.HORIZON_0_6H.value,
            ForecastHorizon.HORIZON_6_24H.value,
            ForecastHorizon.HORIZON_1_3D.value,
            ForecastHorizon.HORIZON_3_7D.value
        ],
        "required_inputs": [
            "official_cyclone_system",
            "forecast_track",
            "wind_speed_knots",
            "central_pressure_hpa",
            "coastal_exposure"
        ],
        "predictability_basis": "IMD tropical cyclone tracking models provide cone-of-uncertainty projections updated every 3-6 hours.",
        "scientific_disclaimer": "Track recurvature and rapid intensification (RI) over warm seas can alter landfall timing by ±6 hours."
    },
    "HEATWAVE": {
        "suitable_horizons": [
            ForecastHorizon.HORIZON_6_24H.value,
            ForecastHorizon.HORIZON_1_3D.value,
            ForecastHorizon.HORIZON_3_7D.value
        ],
        "required_inputs": [
            "max_temperature_forecast",
            "climatological_normal_departure",
            "persistence_duration_days",
            "humidity_heat_index"
        ],
        "predictability_basis": "Synoptic anti-cyclonic subsidence and continental advection have high 1-3 day predictability.",
        "scientific_disclaimer": "Local urban heat island (UHI) microclimates may exceed regional station forecasts by 2-4°C."
    },
    "SEVERE_WEATHER": {
        "suitable_horizons": [
            ForecastHorizon.HORIZON_0_6H.value,
            ForecastHorizon.HORIZON_6_24H.value,
            ForecastHorizon.HORIZON_1_3D.value
        ],
        "required_inputs": [
            "nowcast_radar_reflectivity",
            "satellite_infrared_cloud_top",
            "convective_available_potential_energy",
            "official_squall_lightning_alerts"
        ],
        "predictability_basis": "Mesoscale convective systems predictable at nowcast (0-6h) and synoptic (6-24h) scales.",
        "scientific_disclaimer": "Thunderstorm and lightning strikes are localized convective phenomena with low predictability beyond 24 hours."
    },
    "LANDSLIDE": {
        "suitable_horizons": [
            ForecastHorizon.HORIZON_0_6H.value,
            ForecastHorizon.HORIZON_6_24H.value,
            ForecastHorizon.HORIZON_1_3D.value
        ],
        "required_inputs": [
            "rainfall_intensity_nowcast",
            "antecedent_72h_rainfall_accumulation",
            "gsi_nlsm_slope_susceptibility",
            "geological_fracture_zones"
        ],
        "predictability_basis": "Slope failure is driven by critical saturation thresholds following high-intensity precipitation.",
        "scientific_disclaimer": "Anthropogenic road cutting, deforestation, and toe erosion can induce slope failure below hydrological thresholds."
    },
    "EARTHQUAKE": {
        "suitable_horizons": [
            ForecastHorizon.NOW.value
        ],
        "required_inputs": [
            "recent_seismic_telemetry",
            "bis_is_1893_seismic_zone",
            "historical_epicenters",
            "aftershock_sequence_context"
        ],
        "predictability_basis": "Exact deterministic earthquake prediction (time, location, magnitude) is SCIENTIFICALLY IMPOSSIBLE.",
        "scientific_disclaimer": "Exact deterministic earthquake prediction is not scientifically feasible. Regional baseline seismicity (BIS IS 1893:2016) and recent official USGS/NCS tremors are reported. Forward forecasting windows are strictly unavailable."
    }
}


def is_hazard_horizon_suitable(hazard: str, horizon: str) -> bool:
    """Checks if a hazard can scientifically support a specific forecast horizon."""
    rules = HAZARD_PREDICTABILITY_RULES.get(hazard.upper().strip())
    if not rules:
        return False
    return horizon.upper().strip() in rules["suitable_horizons"]


def get_hazard_predictability_metadata(hazard: str) -> Dict[str, Any]:
    """Returns scientific predictability rules and limitations for a hazard."""
    h_clean = hazard.upper().strip()
    return HAZARD_PREDICTABILITY_RULES.get(h_clean, {
        "suitable_horizons": [ForecastHorizon.NOW.value],
        "required_inputs": [],
        "predictability_basis": "Unclassified hazard profile.",
        "scientific_disclaimer": "Predictability bounds not officially cataloged."
    })
