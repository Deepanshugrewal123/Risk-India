"""
RISK // INDIA — Weather Data Quality Engine (14 Gates)
=======================================================
Evaluates incoming meteorological observations and forecasts against 14 machine-readable gates.
Rejects future observations, invalid forecast windows, impossible physics, synthetic records.
"""

from typing import Dict, Any, Tuple, Optional
from datetime import datetime, timezone, timedelta
import math

from .schema import QualityRejectionReason


class WeatherQualityEngine:
    """
    Validates meteorological payloads against physical boundaries, geographical bounds,
    temporal windows, structural integrity, and synthetic data restrictions.
    """

    INDIA_BOUNDS = {
        "min_lat": 6.0,
        "max_lat": 38.0,
        "min_lon": 68.0,
        "max_lon": 98.0
    }

    PHYSICAL_RANGES = {
        "temperature_celsius": (-50.0, 65.0),
        "feels_like_celsius": (-50.0, 75.0),
        "relative_humidity_percent": (0.0, 100.0),
        "dew_point_celsius": (-50.0, 45.0),
        "rainfall_mm": (0.0, 1500.0),
        "wind_speed_mps": (0.0, 150.0),
        "wind_direction_deg": (0.0, 360.0),
        "wind_gust_mps": (0.0, 180.0),
        "surface_pressure_hpa": (800.0, 1100.0),
        "visibility_km": (0.0, 100.0),
        "cloud_cover_percent": (0.0, 100.0),
        "uv_index": (0.0, 25.0)
    }

    MAX_OPERATIONAL_AGE_DAYS = 90.0

    def validate_payload_structure(self, payload: Any) -> Tuple[bool, Optional[str]]:
        """Gate 9: Structural integrity / payload corruption."""
        if not isinstance(payload, dict):
            return False, QualityRejectionReason.CORRUPTED_PAYLOAD.value
        return True, None

    def validate_location(self, location: Any) -> Tuple[bool, Optional[str]]:
        """Gate 1: Location presence."""
        if not location or not isinstance(location, str) or not location.strip():
            return False, QualityRejectionReason.MISSING_LOCATION.value
        return True, None

    def validate_provider_provenance(self, payload: Dict[str, Any]) -> Tuple[bool, Optional[str]]:
        """Gate 14: Missing provider provenance."""
        provider = payload.get("source_provider") or payload.get("provider")
        if not provider or not isinstance(provider, str) or not provider.strip():
            return False, QualityRejectionReason.MISSING_PROVIDER_PROVENANCE.value
        return True, None

    def validate_numeric_value(self, value: Any) -> Tuple[bool, Optional[float], Optional[str]]:
        """Gate 3: Non-numeric measurements."""
        if value is None or isinstance(value, bool):
            return False, None, QualityRejectionReason.NON_NUMERIC_VALUE.value
        try:
            val = float(value)
            if math.isnan(val) or math.isinf(val):
                return False, None, QualityRejectionReason.NON_NUMERIC_VALUE.value
            return True, val, None
        except (ValueError, TypeError):
            return False, None, QualityRejectionReason.NON_NUMERIC_VALUE.value

    def validate_timestamp(
        self,
        ts_raw: Any,
        is_observation: bool = True,
        now: Optional[datetime] = None
    ) -> Tuple[bool, Optional[str], Optional[str]]:
        """
        Gate 2: Invalid timestamp.
        Gate 10: Future observation rejection (observations only).
        Gate 12: Stale data (> 90 days).
        """
        if not ts_raw or not isinstance(ts_raw, str):
            return False, None, QualityRejectionReason.INVALID_TIMESTAMP.value

        clean_ts = ts_raw.strip().replace("Z", "+00:00")
        try:
            dt = datetime.fromisoformat(clean_ts)
            if dt.tzinfo is None:
                dt = dt.replace(tzinfo=timezone.utc)
            else:
                dt = dt.astimezone(timezone.utc)
        except Exception:
            return False, None, QualityRejectionReason.INVALID_TIMESTAMP.value

        curr = now or datetime.now(timezone.utc)

        # Gate 10: Future observation check
        if is_observation and dt > curr + timedelta(minutes=5):
            return False, None, QualityRejectionReason.FUTURE_OBSERVATION.value

        # Gate 12: Stale data check
        if (curr - dt).total_seconds() > (self.MAX_OPERATIONAL_AGE_DAYS * 86400):
            return False, None, QualityRejectionReason.STALE_DATA.value

        return True, dt.strftime("%Y-%m-%dT%H:%M:%SZ"), None

    def validate_forecast_window(self, valid_from_iso: str, valid_until_iso: str) -> Tuple[bool, Optional[str]]:
        """Gate 11: Invalid forecast window (valid_until < valid_from)."""
        try:
            dt_from = datetime.fromisoformat(valid_from_iso.replace("Z", "+00:00"))
            dt_until = datetime.fromisoformat(valid_until_iso.replace("Z", "+00:00"))
            if dt_until < dt_from:
                return False, QualityRejectionReason.INVALID_FORECAST_WINDOW.value
            return True, None
        except Exception:
            return False, QualityRejectionReason.INVALID_TIMESTAMP.value

    def validate_physical_range(self, variable_name: str, value: float) -> Tuple[bool, Optional[str]]:
        """Gate 5: Physically impossible value."""
        if variable_name in self.PHYSICAL_RANGES:
            min_v, max_v = self.PHYSICAL_RANGES[variable_name]
            if value < min_v or value > max_v:
                return False, QualityRejectionReason.PHYSICALLY_IMPOSSIBLE_VALUE.value
        return True, None

    def validate_coordinates(self, lat: float, lon: float) -> Tuple[bool, Optional[str]]:
        """Gate 6: Out of bounds coordinates (WGS84 India)."""
        if not (self.INDIA_BOUNDS["min_lat"] <= lat <= self.INDIA_BOUNDS["max_lat"]) or            not (self.INDIA_BOUNDS["min_lon"] <= lon <= self.INDIA_BOUNDS["max_lon"]):
            return False, QualityRejectionReason.OUT_OF_BOUNDS_COORDINATES.value
        return True, None

    def validate_geographic_mapping(self, region_type: str) -> Tuple[bool, Optional[str]]:
        """Gate 7: Unverified geographic mapping."""
        if region_type == "UNMAPPED":
            return False, QualityRejectionReason.UNVERIFIED_GEOGRAPHIC_MAPPING.value
        return True, None

    def validate_synthetic_data(self, payload: Dict[str, Any]) -> Tuple[bool, Optional[str]]:
        """Synthetic data rejection: invariant synthetic_records = 0."""
        if payload.get("synthetic_records", 0) > 0:
            return False, QualityRejectionReason.SYNTHETIC_DATA_REJECTED.value
        if payload.get("is_synthetic") is True or payload.get("is_simulated") is True:
            return False, QualityRejectionReason.SYNTHETIC_DATA_REJECTED.value
        for field_name in ["source_provider", "provider", "source", "source_url", "headline", "description", "model"]:
            val = str(payload.get(field_name, "")).lower()
            if "synthetic" in val or "simulated" in val or "mock" in val:
                return False, QualityRejectionReason.SYNTHETIC_DATA_REJECTED.value
        return True, None


weather_quality_engine = WeatherQualityEngine()
