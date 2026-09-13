"""
RISK // INDIA — Spatial Coordinate & Geography Validation

Validates geographical coordinates and location attributes within sovereign Indian territory:
- Latitude: [6.5, 37.5]
- Longitude: [68.0, 97.5]
"""

from typing import Dict, Any, List, Tuple, Optional
import pandas as pd
import numpy as np

# Sovereign Indian geographical boundary coordinates
INDIA_BOUNDS = {
    "lat_min": 6.5,
    "lat_max": 37.5,
    "lon_min": 68.0,
    "lon_max": 97.5,
}

def validate_coordinates(
    df: pd.DataFrame,
    lat_col: str = "latitude",
    lon_col: str = "longitude"
) -> Dict[str, Any]:
    """
    Audits a DataFrame for geographic coordinate integrity within India.
    
    Returns:
        Dictionary containing counts of valid, invalid, missing, and bounding coordinates.
    """
    if lat_col not in df.columns or lon_col not in df.columns:
        return {
            "has_coordinates": False,
            "message": f"Coordinate columns ('{lat_col}', '{lon_col}') not present in DataFrame."
        }

    total_rows = len(df)
    missing_lat = int(df[lat_col].isna().sum())
    missing_lon = int(df[lon_col].isna().sum())

    valid_coords = df[[lat_col, lon_col]].dropna()
    if valid_coords.empty:
        return {
            "has_coordinates": True,
            "total_rows": total_rows,
            "valid_coordinate_rows": 0,
            "missing_coordinates": total_rows,
            "out_of_bounds_count": 0,
            "is_spatially_valid": False,
            "details": "All coordinate entries are missing or null."
        }

    lats = valid_coords[lat_col].astype(float)
    lons = valid_coords[lon_col].astype(float)

    out_of_lat = ((lats < INDIA_BOUNDS["lat_min"]) | (lats > INDIA_BOUNDS["lat_max"]))
    out_of_lon = ((lons < INDIA_BOUNDS["lon_min"]) | (lons > INDIA_BOUNDS["lon_max"]))
    out_of_bounds_mask = out_of_lat | out_of_lon
    out_of_bounds_count = int(out_of_bounds_mask.sum())

    return {
        "has_coordinates": True,
        "total_rows": total_rows,
        "valid_coordinate_rows": len(valid_coords) - out_of_bounds_count,
        "missing_lat_count": missing_lat,
        "missing_lon_count": missing_lon,
        "out_of_bounds_count": out_of_bounds_count,
        "is_spatially_valid": out_of_bounds_count == 0 and missing_lat == 0 and missing_lon == 0,
        "bounding_box_observed": {
            "min_lat": float(lats.min()) if not lats.empty else None,
            "max_lat": float(lats.max()) if not lats.empty else None,
            "min_lon": float(lons.min()) if not lons.empty else None,
            "max_lon": float(lons.max()) if not lons.empty else None,
        }
    }


def haversine_distance_km(
    lat1: float, lon1: float,
    lat2: float, lon2: float
) -> float:
    """
    Computes great-circle distance between two geographic points in kilometers.
    """
    R = 6371.0  # Earth's mean radius in km
    phi1, phi2 = np.radians(lat1), np.radians(lat2)
    delta_phi = np.radians(lat2 - lat1)
    delta_lambda = np.radians(lon2 - lon1)

    a = (np.sin(delta_phi / 2.0) ** 2 +
         np.cos(phi1) * np.cos(phi2) * np.sin(delta_lambda / 2.0) ** 2)
    c = 2.0 * np.arctan2(np.sqrt(a), np.sqrt(1.0 - a))
    return float(R * c)
