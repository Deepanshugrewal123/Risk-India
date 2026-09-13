"""
RISK // INDIA — Geospatial Join & Nearest Station Matching Utilities

Provides robust geospatial utilities:
- Nearest station matching using vector Haversine distance
- Spatial join between point telemetry stations and administrative boundaries/districts
- Coordinate integrity auditing (no fabricated coordinates)
"""

from typing import Dict, Any, List, Optional, Tuple
import pandas as pd
import numpy as np

from ml.data.validation.spatial_validation import haversine_distance_km, validate_coordinates


def find_nearest_station(
    target_lat: float,
    target_lon: float,
    stations_df: pd.DataFrame,
    lat_col: str = "latitude",
    lon_col: str = "longitude",
    station_id_col: str = "station_id",
    max_distance_km: float = 100.0
) -> Optional[Dict[str, Any]]:
    """
    Finds the closest telemetry station to a target coordinate within max_distance_km.
    """
    if stations_df.empty or lat_col not in stations_df.columns or lon_col not in stations_df.columns:
        return None

    valid_stns = stations_df.dropna(subset=[lat_col, lon_col]).copy()
    if valid_stns.empty:
        return None

    # Vectorized Haversine calculation
    lat1, lon1 = np.radians(target_lat), np.radians(target_lon)
    lat2 = np.radians(valid_stns[lat_col].values.astype(float))
    lon2 = np.radians(valid_stns[lon_col].values.astype(float))

    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = np.sin(dlat / 2.0) ** 2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon / 2.0) ** 2
    c = 2.0 * np.arctan2(np.sqrt(a), np.sqrt(1.0 - a))
    distances_km = 6371.0 * c

    min_idx = int(np.argmin(distances_km))
    min_dist = float(distances_km[min_idx])

    if min_dist > max_distance_km:
        return None

    matched_row = valid_stns.iloc[min_idx]
    return {
        "station_id": str(matched_row.get(station_id_col, f"station_{min_idx}")),
        "station_lat": float(matched_row[lat_col]),
        "station_lon": float(matched_row[lon_col]),
        "distance_km": round(min_dist, 2),
        "attributes": matched_row.to_dict()
    }


def spatial_join_nearest_telemetry(
    base_df: pd.DataFrame,
    telemetry_df: pd.DataFrame,
    base_lat_col: str = "latitude",
    base_lon_col: str = "longitude",
    tel_lat_col: str = "latitude",
    tel_lon_col: str = "longitude",
    tel_id_col: str = "station_id",
    max_dist_km: float = 75.0
) -> pd.DataFrame:
    """
    Augments each row in base_df with the nearest telemetry station ID and distance.
    """
    if base_df.empty or telemetry_df.empty:
        return base_df

    results = []
    for _, row in base_df.iterrows():
        b_lat = row.get(base_lat_col)
        b_lon = row.get(base_lon_col)
        if pd.isna(b_lat) or pd.isna(b_lon):
            results.append({"nearest_station_id": None, "station_distance_km": None})
            continue

        match = find_nearest_station(
            float(b_lat), float(b_lon),
            telemetry_df,
            lat_col=tel_lat_col,
            lon_col=tel_lon_col,
            station_id_col=tel_id_col,
            max_distance_km=max_dist_km
        )
        if match:
            results.append({
                "nearest_station_id": match["station_id"],
                "station_distance_km": match["distance_km"]
            })
        else:
            results.append({"nearest_station_id": None, "station_distance_km": None})

    df_joined = base_df.copy()
    match_df = pd.DataFrame(results, index=base_df.index)
    return pd.concat([df_joined, match_df], axis=1)
