"""
RISK // INDIA — Flexible Schema Validation for Heterogeneous Indian Datasets

Audits input dataframes against flexible expected schemas without brittle failures:
- Recognizes variable naming conventions across IMD, CWC, and ISRO
- Confirms minimum required fields for processing
- Preserves raw schema mappings for traceability
"""

from typing import Dict, Any, List, Optional, Set
import pandas as pd

# Canonical column synonym mappings
COLUMN_SYNONYMS: Dict[str, List[str]] = {
    "rainfall": [
        "rainfall", "rainfall_mm", "rf_mm", "precip", "precipitation", "rain_mm", "rain_24h",
        "telemetry_hourly_rainfall_(mm)", "telemetry_hourly_rainfall_mm", "daily_actual", "actual_rainfall"
    ],
    "date": [
        "date", "timestamp", "datetime", "obs_date", "observation_date", "time", "date_time",
        "data_acquisition_time", "week_date", "cumulative_date"
    ],
    "station_id": ["station_id", "station", "station_code", "stn_id", "gauge_id", "site_id"],
    "water_level": [
        "water_level", "water_level_m", "wl_m", "stage", "stage_m", "river_stage", "gauge_reading",
        "river_water_level_telemetry_hourly_(meter)", "river_water_level_telemetry_hourly_meter"
    ],
    "danger_level": ["danger_level", "danger_level_m", "dl_m", "warning_level", "wl_danger"],
    "latitude": ["latitude", "lat", "lat_deg", "y_coord", "y"],
    "longitude": ["longitude", "lon", "long", "lon_deg", "x_coord", "x"],
    "district": ["district", "district_name", "dist_name", "dist"],
    "state": ["state", "state_name", "st_name", "state_code"],
}


def resolve_canonical_column(col_name: str) -> Optional[str]:
    """Resolves raw column names to canonical concept name."""
    clean_name = col_name.strip().lower().replace(" ", "_").replace("-", "_")
    for canonical, synonyms in COLUMN_SYNONYMS.items():
        if clean_name in synonyms:
            return canonical
        # Also check without parentheses or trailing underscores
        stripped = clean_name.replace("(", "").replace(")", "").strip("_")
        if stripped in synonyms:
            return canonical
    return None


def inspect_dataframe_schema(
    df: pd.DataFrame,
    required_concepts: List[str]
) -> Dict[str, Any]:
    """
    Evaluates whether a dataframe fulfills required conceptual components.
    """
    if df is None or df.empty:
        return {
            "is_schema_valid": False,
            "error": "DataFrame is None or empty.",
            "detected_mappings": {},
            "missing_concepts": required_concepts
        }

    detected_mappings: Dict[str, str] = {}
    for col in df.columns:
        canonical = resolve_canonical_column(str(col))
        if canonical and canonical not in detected_mappings:
            detected_mappings[canonical] = str(col)

    missing_concepts = [c for c in required_concepts if c not in detected_mappings]

    return {
        "is_schema_valid": len(missing_concepts) == 0,
        "total_columns": len(df.columns),
        "columns_present": list(df.columns),
        "detected_mappings": detected_mappings,
        "missing_concepts": missing_concepts
    }
