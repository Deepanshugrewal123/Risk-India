"""
RISK // INDIA — Empirical Data Normalization Engine
===================================================
Normalizes state names, river basins, gauge IDs, coordinates (WGS84 EPSG:4326),
and measurement units into canonical forms.
"""

from typing import Optional, Dict, Any, Tuple
from datetime import datetime, timezone
import math

from app.services.geo_basin_service import INDIAN_ADMINISTRATIVE_ENTITIES


STATE_ALIASES: Dict[str, str] = {
    "orissa": "Odisha",
    "pondicherry": "Puducherry",
    "uttaranchal": "Uttarakhand",
    "nct of delhi": "Delhi",
    "delhi nct": "Delhi",
    "jammu & kashmir": "Jammu and Kashmir",
    "andaman & nicobar": "Andaman and Nicobar Islands",
    "daman & diu": "Dadra and Nagar Haveli and Daman and Diu",
    "dadra & nagar haveli": "Dadra and Nagar Haveli and Daman and Diu",
    "dadra and nagar haveli": "Dadra and Nagar Haveli and Daman and Diu",
    "daman and diu": "Dadra and Nagar Haveli and Daman and Diu"
}

BASIN_ALIASES: Dict[str, str] = {
    "brahmaputra basin": "brahmaputra",
    "brahmaputra and barak": "brahmaputra",
    "assam valley": "brahmaputra",
    "ganga basin": "ganga",
    "ganges": "ganga",
    "godavari basin": "godavari",
    "dakshin ganga": "godavari",
    "mahanadi basin": "mahanadi",
    "krishna basin": "krishna"
}


def normalize_state_name(state_raw: str) -> str:
    """Standardizes state or UT name against the 28 States and 8 Union Territories."""
    if not state_raw:
        return "Unknown"

    s_clean = state_raw.strip().lower()
    if s_clean in STATE_ALIASES:
        return STATE_ALIASES[s_clean]

    for entity in INDIAN_ADMINISTRATIVE_ENTITIES:
        canonical_name = entity.get("name", "")
        if s_clean == canonical_name.lower():
            return canonical_name

    return state_raw.strip().title()


def normalize_basin_name(basin_raw: Optional[str]) -> str:
    """Normalizes basin name to canonical identifier."""
    if not basin_raw:
        return "unknown"

    b_clean = basin_raw.strip().lower()
    if b_clean in BASIN_ALIASES:
        return BASIN_ALIASES[b_clean]

    for canonical in ["brahmaputra", "ganga", "godavari", "mahanadi", "krishna"]:
        if canonical in b_clean:
            return canonical

    return b_clean


def normalize_coordinates(lat: float, lon: float) -> Tuple[float, float]:
    """Standardizes coordinates to WGS84 EPSG:4326 rounded to 6 decimal places."""
    return round(float(lat), 6), round(float(lon), 6)


def normalize_timestamp(ts_raw: str) -> str:
    """Converts timestamp to standard UTC ISO 8601 string (ending in 'Z')."""
    clean_ts = ts_raw.strip().replace("Z", "+00:00")
    dt = datetime.fromisoformat(clean_ts)
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    else:
        dt = dt.astimezone(timezone.utc)
    return dt.strftime("%Y-%m-%dT%H:%M:%SZ")


def normalize_unit(param_name: str, value: float, unit_str: str) -> Tuple[float, str]:
    """
    Normalizes measurement to SI / standard Indian units (m for levels, mm for rain).
    Returns (normalized_value, normalized_unit).
    """
    u_clean = unit_str.strip().lower()
    val = float(value)

    # Feet to meters
    if u_clean in ["ft", "feet", "foot"]:
        return round(val * 0.3048, 4), "m"

    # Inches to mm
    if u_clean in ["in", "inch", "inches"]:
        return round(val * 25.4, 2), "mm"

    # Centimeters to meters
    if u_clean in ["cm", "centimeter", "centimeters"]:
        return round(val / 100.0, 4), "m"

    return val, unit_str


def normalize_observation_record(record_dict: Dict[str, Any]) -> Dict[str, Any]:
    """Normalizes an empirical observation dictionary into canonical format."""
    normalized = record_dict.copy()
    if "state" in normalized and normalized["state"]:
        normalized["state"] = normalize_state_name(normalized["state"])
    if "basin" in normalized and normalized["basin"]:
        normalized["basin"] = normalize_basin_name(normalized["basin"])
    if "latitude" in normalized and "longitude" in normalized and normalized["latitude"] is not None and normalized["longitude"] is not None:
        try:
            normalized["latitude"], normalized["longitude"] = normalize_coordinates(normalized["latitude"], normalized["longitude"])
        except Exception:
            pass
    if "timestamp" in normalized and normalized["timestamp"]:
        try:
            normalized["timestamp"] = normalize_timestamp(normalized["timestamp"])
        except Exception:
            pass
    return normalized

