"""
RISK // INDIA — Empirical Flood Data Validators & Physical Bounds Engine
========================================================================
Enforces strict physical measurement bounds, coordinate bounding-box validation,
timestamp chronological order, and deterministic duplicate rejection.
"""

from typing import Tuple, Dict, Any, Optional
from datetime import datetime, timezone
import math


# India Subcontinental Coordinate Bounding Box (WGS84 EPSG:4326)
INDIA_LAT_MIN = 6.0
INDIA_LAT_MAX = 38.0
INDIA_LON_MIN = 68.0
INDIA_LON_MAX = 98.0

# Physical Measurement Sanity Bounds
BOUNDS_RAINFALL_MAX_MM = 2000.0        # Cherrapunji world record single-day threshold
BOUNDS_WATER_LEVEL_MAX_M = 1500.0      # MSL bounds
BOUNDS_RIVER_RISE_MAX_M = 20.0         # Maximum physical 24h river surge
BOUNDS_PERCENTILE_MIN = 0.0
BOUNDS_PERCENTILE_MAX = 1.0

INDIAN_BOUNDING_BOX = {
    "latitude": [INDIA_LAT_MIN, INDIA_LAT_MAX],
    "longitude": [INDIA_LON_MIN, INDIA_LON_MAX]
}

PHYSICAL_MEASUREMENT_BOUNDS = {
    "rainfall_max_mm": BOUNDS_RAINFALL_MAX_MM,
    "water_level_max_m": BOUNDS_WATER_LEVEL_MAX_M,
    "river_rise_max_m": BOUNDS_RIVER_RISE_MAX_M,
    "percentile_bounds": [BOUNDS_PERCENTILE_MIN, BOUNDS_PERCENTILE_MAX]
}



def validate_coordinates(lat: Optional[float], lon: Optional[float]) -> Tuple[bool, Optional[str]]:
    """Validates that coordinates exist and fall strictly within the Indian subcontinental bounding box."""
    if lat is None or lon is None:
        return False, "Missing coordinate values (latitude or longitude is None)"

    if math.isnan(lat) or math.isnan(lon):
        return False, "Coordinate values are NaN"

    if not (INDIA_LAT_MIN <= lat <= INDIA_LAT_MAX):
        return False, f"Latitude {lat}° is outside Indian bounding box [{INDIA_LAT_MIN}, {INDIA_LAT_MAX}]"

    if not (INDIA_LON_MIN <= lon <= INDIA_LON_MAX):
        return False, f"Longitude {lon}° is outside Indian bounding box [{INDIA_LON_MIN}, {INDIA_LON_MAX}]"

    return True, None


def validate_physical_measurements(measurements: Dict[str, Any]) -> Tuple[bool, Optional[str]]:
    """Validates that measurement values are physically plausible and non-negative where required."""
    for key, val in measurements.items():
        if val is None:
            continue

        if not isinstance(val, (int, float)):
            return False, f"Non-numeric measurement '{key}': {val}"

        if math.isnan(val) or math.isinf(val):
            return False, f"Invalid floating value for '{key}': {val}"

        # Rainfall bounds
        if "rainfall" in key.lower():
            if val < 0.0:
                return False, f"Negative rainfall measurement '{key}': {val} mm"
            if val > BOUNDS_RAINFALL_MAX_MM:
                return False, f"Rainfall '{key}' {val} mm exceeds physical ceiling of {BOUNDS_RAINFALL_MAX_MM} mm"

        # Water level bounds
        if "water_level" in key.lower() or "river_level" in key.lower():
            if val < -100.0 or val > BOUNDS_WATER_LEVEL_MAX_M:
                return False, f"Water level '{key}' {val} m outside physical sanity bounds [-100, {BOUNDS_WATER_LEVEL_MAX_M}]"

        # River rise bounds
        if "river_rise" in key.lower():
            if abs(val) > BOUNDS_RIVER_RISE_MAX_M:
                return False, f"River rise rate '{key}' {val} m exceeds physical sanity bound of +/-{BOUNDS_RIVER_RISE_MAX_M} m"

        # Percentile bounds
        if "percentile" in key.lower():
            if not (BOUNDS_PERCENTILE_MIN <= val <= BOUNDS_PERCENTILE_MAX):
                return False, f"Percentile '{key}' {val} outside [0.0, 1.0]"

    return True, None


def validate_timestamp(ts_str: str) -> Tuple[bool, Optional[str]]:
    """Validates timestamp format (ISO 8601 UTC) and confirms it is not in the future."""
    if not ts_str or not isinstance(ts_str, str):
        return False, "Timestamp is missing or not a string"

    clean_ts = ts_str.strip().replace("Z", "+00:00")
    try:
        dt = datetime.fromisoformat(clean_ts)
    except ValueError as err:
        return False, f"Invalid ISO 8601 timestamp format: {err}"

    now_utc = datetime.now(timezone.utc)
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)

    # Allow slight clock skew of 5 minutes
    if dt > now_utc + datetime.resolution * 300000000:
        return False, f"Timestamp {ts_str} is in the future relative to current UTC time {now_utc.isoformat()}"

    return True, None


def validate_temporal_consistency(obs_timestamp: str, event_timestamp: Optional[str]) -> Tuple[bool, Optional[str]]:
    """Ensures observations do not post-date the target flood event (Zero Temporal Leakage)."""
    if event_timestamp is None:
        return True, None

    clean_obs = obs_timestamp.strip().replace("Z", "+00:00")
    clean_evt = event_timestamp.strip().replace("Z", "+00:00")
    try:
        dt_obs = datetime.fromisoformat(clean_obs)
        dt_evt = datetime.fromisoformat(clean_evt)
    except ValueError as err:
        return False, f"Error parsing timestamps for temporal consistency: {err}"

    if dt_obs > dt_evt:
        return False, f"Temporal leakage detected: Observation ({obs_timestamp}) occurs after event timestamp ({event_timestamp})"

    return True, None
