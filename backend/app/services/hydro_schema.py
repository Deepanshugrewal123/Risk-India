"""
RISK // INDIA — Standardized Hydro-Meteorological Observation Schema
====================================================================
Canonical data schema and normalization helpers for river stage and precipitation
telemetry across Indian river basins.

SCIENTIFIC PRINCIPLES:
- All temporal values are strictly normalized to UTC ISO 8601 strings.
- Units are standardized to the International System of Units (meters for levels, mm for rainfall).
- Freeboard and crest percentages are mathematically derived relative to official CWC danger levels.
- Flood status classifications follow standard CWC telemetry rules:
    * NORMAL: water_level < warning_level
    * WARNING: warning_level <= water_level < danger_level
    * DANGER: danger_level <= water_level < (hfl or danger_level + 1.0m)
    * SEVERE_DANGER: water_level >= hfl (or water_level >= danger_level + 1.0m when HFL is unspecified)
"""

from typing import Dict, Any, Optional, Union
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
import math


class FloodStatus:
    NORMAL = "NORMAL"
    WARNING = "WARNING"
    DANGER = "DANGER"
    SEVERE_DANGER = "SEVERE_DANGER"


@dataclass
class HydroObservation:
    station_id: str
    station_name: str
    basin_id: str
    sub_basin: str
    river_name: str
    latitude: float
    longitude: float
    observation_timestamp: str  # ISO 8601 UTC
    water_level_m: float
    warning_level_m: float
    danger_level_m: float
    hfl_m: Optional[float] = None
    water_level_change_24h_m: Optional[float] = 0.0
    rainfall_1h_mm: Optional[float] = 0.0
    rainfall_24h_mm: Optional[float] = 0.0
    rainfall_72h_mm: Optional[float] = 0.0
    rainfall_168h_mm: Optional[float] = 0.0
    flood_status: str = FloodStatus.NORMAL
    freeboard_to_danger_m: float = 0.0
    crest_percentage: float = 0.0
    source: str = "Central Water Commission (CWC)"
    source_tier: str = "PUBLIC_WEB_DATA"
    quality_flag: str = "VALIDATED_EMPIRICAL"
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class HydroObservationNormalizer:
    """
    Standardization engine for hydro-meteorological readings.
    """

    @staticmethod
    def feet_to_meters(feet: float) -> float:
        """Converts feet to meters rounded to 3 decimal places."""
        return round(feet * 0.3048, 3)

    @staticmethod
    def meters_to_feet(meters: float) -> float:
        """Converts meters to feet rounded to 2 decimal places."""
        return round(meters / 0.3048, 2)

    @staticmethod
    def normalize_timestamp(ts: Union[str, datetime]) -> str:
        """
        Normalizes any datetime or ISO string to UTC ISO 8601 representation.
        Raises ValueError if invalid.
        """
        if isinstance(ts, datetime):
            if ts.tzinfo is None:
                dt_utc = ts.replace(tzinfo=timezone.utc)
            else:
                dt_utc = ts.astimezone(timezone.utc)
            return dt_utc.isoformat()

        # String handling
        ts_clean = str(ts).strip()
        # Handle 'Z' suffix
        ts_iso = ts_clean.replace("Z", "+00:00")
        try:
            dt = datetime.fromisoformat(ts_iso)
            if dt.tzinfo is None:
                dt = dt.replace(tzinfo=timezone.utc)
            else:
                dt = dt.astimezone(timezone.utc)
            return dt.isoformat()
        except Exception as e:
            raise ValueError(f"Invalid timestamp format: '{ts}'. Expected ISO 8601 format: {e}")

    @classmethod
    def derive_flood_status(
        cls,
        water_level_m: float,
        warning_level_m: float,
        danger_level_m: float,
        hfl_m: Optional[float] = None
    ) -> str:
        """
        Derives CWC standard flood status based on water level and thresholds.
        """
        if hfl_m is not None and water_level_m >= hfl_m:
            return FloodStatus.SEVERE_DANGER
        if water_level_m >= danger_level_m:
            if hfl_m is None and water_level_m >= (danger_level_m + 1.0):
                return FloodStatus.SEVERE_DANGER
            return FloodStatus.DANGER
        if water_level_m >= warning_level_m:
            return FloodStatus.WARNING
        return FloodStatus.NORMAL

    @classmethod
    def calculate_relative_metrics(
        cls,
        water_level_m: float,
        danger_level_m: float
    ) -> Dict[str, float]:
        """
        Calculates freeboard to danger and crest percentage.
        Freeboard = danger_level - water_level (positive means safely below danger).
        Crest % = (water_level / danger_level) * 100
        """
        freeboard = round(danger_level_m - water_level_m, 3)
        crest_pct = round((water_level_m / danger_level_m * 100.0), 2) if danger_level_m > 0 else 0.0
        return {
            "freeboard_to_danger_m": freeboard,
            "crest_percentage": crest_pct
        }

    @classmethod
    def build_normalized_observation(
        cls,
        station_id: str,
        station_name: str,
        basin_id: str,
        sub_basin: str,
        river_name: str,
        latitude: float,
        longitude: float,
        timestamp: Union[str, datetime],
        water_level_m: float,
        warning_level_m: float,
        danger_level_m: float,
        hfl_m: Optional[float] = None,
        water_level_change_24h_m: Optional[float] = 0.0,
        rainfall_1h_mm: Optional[float] = 0.0,
        rainfall_24h_mm: Optional[float] = 0.0,
        rainfall_72h_mm: Optional[float] = 0.0,
        rainfall_168h_mm: Optional[float] = 0.0,
        source: str = "Central Water Commission (CWC)",
        source_tier: str = "PUBLIC_WEB_DATA",
        quality_flag: str = "VALIDATED_EMPIRICAL",
        metadata: Optional[Dict[str, Any]] = None
    ) -> HydroObservation:
        """
        Factory creating a fully normalized and validated HydroObservation object.
        """
        norm_ts = cls.normalize_timestamp(timestamp)
        status = cls.derive_flood_status(water_level_m, warning_level_m, danger_level_m, hfl_m)
        rel_metrics = cls.calculate_relative_metrics(water_level_m, danger_level_m)

        return HydroObservation(
            station_id=station_id,
            station_name=station_name,
            basin_id=basin_id.lower().strip(),
            sub_basin=sub_basin.lower().strip(),
            river_name=river_name,
            latitude=latitude,
            longitude=longitude,
            observation_timestamp=norm_ts,
            water_level_m=water_level_m,
            warning_level_m=warning_level_m,
            danger_level_m=danger_level_m,
            hfl_m=hfl_m,
            water_level_change_24h_m=water_level_change_24h_m or 0.0,
            rainfall_1h_mm=max(0.0, rainfall_1h_mm or 0.0),
            rainfall_24h_mm=max(0.0, rainfall_24h_mm or 0.0),
            rainfall_72h_mm=max(0.0, rainfall_72h_mm or 0.0),
            rainfall_168h_mm=max(0.0, rainfall_168h_mm or 0.0),
            flood_status=status,
            freeboard_to_danger_m=rel_metrics["freeboard_to_danger_m"],
            crest_percentage=rel_metrics["crest_percentage"],
            source=source,
            source_tier=source_tier,
            quality_flag=quality_flag,
            metadata=metadata or {}
        )
