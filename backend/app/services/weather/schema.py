"""
RISK // INDIA — National Weather Intelligence Canonical Schemas & Contracts
=============================================================================
Defines standard models for current observations, multi-horizon forecasts,
meteorological warnings, 14 machine-readable quality gates, and data categories.
Enforces zero synthetic data (synthetic_records = 0 strictly).
"""

from enum import Enum
from dataclasses import dataclass, field, asdict
from typing import Optional, List, Dict, Any
import hashlib
from datetime import datetime, timezone


class DataClassification(str, Enum):
    OBSERVED = "OBSERVED"
    FORECAST = "FORECAST"
    WARNING = "WARNING"
    HISTORICAL = "HISTORICAL"
    CACHED = "CACHED"
    STALE = "STALE"
    UNAVAILABLE = "UNAVAILABLE"


class ForecastHorizon(str, Enum):
    NOW = "NOW"
    HORIZON_0_6H = "0_6_HOURS"
    HORIZON_6_24H = "6_24_HOURS"
    HORIZON_1_3D = "1_3_DAYS"
    HORIZON_3_7D = "3_7_DAYS"


class ForecastUncertainty(str, Enum):
    LOW = "LOW"
    MODERATE = "MODERATE"
    HIGH = "HIGH"
    VERY_HIGH = "VERY_HIGH"


class WeatherFreshness(str, Enum):
    OFFICIAL_LIVE = "OFFICIAL_LIVE"
    OFFICIAL_RECENT = "OFFICIAL_RECENT"
    FORECAST_CURRENT = "FORECAST_CURRENT"
    FORECAST_NEAR_TERM = "FORECAST_NEAR_TERM"
    CACHED = "CACHED"
    STALE = "STALE"
    UNAVAILABLE = "UNAVAILABLE"


class QualityRejectionReason(str, Enum):
    MISSING_LOCATION = "MISSING_LOCATION"
    INVALID_TIMESTAMP = "INVALID_TIMESTAMP"
    NON_NUMERIC_VALUE = "NON_NUMERIC_VALUE"
    UNKNOWN_UNIT = "UNKNOWN_UNIT"
    PHYSICALLY_IMPOSSIBLE_VALUE = "PHYSICALLY_IMPOSSIBLE_VALUE"
    OUT_OF_BOUNDS_COORDINATES = "OUT_OF_BOUNDS_COORDINATES"
    UNVERIFIED_GEOGRAPHIC_MAPPING = "UNVERIFIED_GEOGRAPHIC_MAPPING"
    DUPLICATE_RECORD = "DUPLICATE_RECORD"
    CORRUPTED_PAYLOAD = "CORRUPTED_PAYLOAD"
    FUTURE_OBSERVATION = "FUTURE_OBSERVATION"
    INVALID_FORECAST_WINDOW = "INVALID_FORECAST_WINDOW"
    STALE_DATA = "STALE_DATA"
    UNSUPPORTED_VARIABLE = "UNSUPPORTED_VARIABLE"
    MISSING_PROVIDER_PROVENANCE = "MISSING_PROVIDER_PROVENANCE"
    SYNTHETIC_DATA_REJECTED = "SYNTHETIC_DATA_REJECTED"


@dataclass
class WeatherUnitConversionRecord:
    """Audit trail of mathematical unit conversion."""
    original_value: float
    original_unit: str
    normalized_value: float
    normalized_unit: str
    conversion_rule: str

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class CanonicalWeatherObservation:
    """
    Standardized real-time weather observation record with complete provenance.
    Zero synthetic records allowed (synthetic_records = 0 strictly).
    """
    observation_id: str
    region_id: str
    region_name: str
    region_type: str                        # STATE, UNION_TERRITORY, DISTRICT, CITY, BASIN
    latitude: float
    longitude: float
    observed_at: str                        # UTC ISO 8601 recorded by meteorological sensor
    ingested_at: str                        # UTC ISO 8601 recorded by system
    data_classification: str = DataClassification.OBSERVED.value
    temperature_celsius: Optional[float] = None
    feels_like_celsius: Optional[float] = None
    relative_humidity_percent: Optional[float] = None
    dew_point_celsius: Optional[float] = None
    rainfall_mm: Optional[float] = None
    wind_speed_mps: Optional[float] = None
    wind_direction_deg: Optional[float] = None
    wind_gust_mps: Optional[float] = None
    surface_pressure_hpa: Optional[float] = None
    visibility_km: Optional[float] = None
    cloud_cover_percent: Optional[float] = None
    uv_index: Optional[float] = None
    weather_condition: str = "CLEAR"
    thunderstorm_indicator: bool = False
    lightning_indicator: bool = False
    source_provider: str = "India Meteorological Department (IMD)"
    source_url: str = "https://mausam.imd.gov.in"
    freshness: str = WeatherFreshness.OFFICIAL_LIVE.value
    synthetic_records: int = 0              # Invariant: strictly 0
    provenance: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class CanonicalWeatherForecast:
    """
    Standardized multi-horizon weather forecast with explicit uncertainty and window.
    Forecast-derived data is never labeled as observed facts.
    """
    forecast_id: str
    region_id: str
    region_name: str
    forecasted_at: str                      # Timestamp when forecast model executed
    forecast_valid_from: str                # Start of validity window
    forecast_valid_until: str               # End of validity window
    forecast_horizon: str                   # NOW, 0_6_HOURS, 6_24_HOURS, 1_3_DAYS, 3_7_DAYS
    data_classification: str = DataClassification.FORECAST.value
    temperature_celsius: Optional[float] = None
    rainfall_mm: Optional[float] = None
    precipitation_probability_percent: Optional[float] = None
    wind_speed_mps: Optional[float] = None
    relative_humidity_percent: Optional[float] = None
    surface_pressure_hpa: Optional[float] = None
    weather_condition: str = "NORMAL"
    thunderstorm_indicator: bool = False
    lightning_indicator: bool = False
    forecast_source: str = "IMD Numerical Weather Prediction / NWFC"
    forecast_type: str = "DETERMINISTIC_ENSEMBLE"
    uncertainty: str = ForecastUncertainty.MODERATE.value
    freshness: str = WeatherFreshness.FORECAST_CURRENT.value
    synthetic_records: int = 0              # Invariant: strictly 0
    provenance: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class WeatherWarning:
    """
    Official government meteorological warning / alert.
    Color coded: GREEN (None), YELLOW (Watch), ORANGE (Alert), RED (Warning).
    """
    warning_id: str
    provider: str
    hazard: str                             # SEVERE_WEATHER, FLOOD, CYCLONE, HEATWAVE, etc.
    severity: str                           # GREEN, YELLOW, ORANGE, RED / LOW, MODERATE, HIGH, CRITICAL
    headline: str
    description: str
    issued_at: str
    valid_from: str
    valid_until: str
    affected_region: str
    source_record_id: str
    source_url: str = "https://mausam.imd.gov.in"
    data_classification: str = DataClassification.WARNING.value
    freshness: str = WeatherFreshness.OFFICIAL_LIVE.value
    synthetic_records: int = 0              # Invariant: strictly 0
    provenance: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


def generate_weather_id(prefix: str, region_id: str, variable_or_horizon: str, timestamp_str: str) -> str:
    """Deterministically creates a 16-character SHA-256 identifier."""
    raw = f"{prefix.strip().lower()}:{region_id.strip().lower()}:{variable_or_horizon.strip().upper()}:{timestamp_str.strip()}"
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()[:16]
