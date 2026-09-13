"""
RISK // INDIA — Geospatial Alignment & Spatial Matching Hierarchy

Connects flood observations with hydrometeorological predictor networks:
- CWC Rainfall: 31 active telemetry rainfall stations
- CWC River Level: 3 telemetry highway bridge gauges
- Administrative Districts: 33 Assam districts

Preferred Alignment Hierarchy:
1. EXACT_INTERSECTION: Direct point-in-polygon or coordinate containment.
2. CATCHMENT_BUFFER_INTERSECTION: 15–25 km hydrological buffer intersection.
3. NEAREST_STATION_MATCHING: Nearest reporting sensor with documented distance & quality metric.
4. INVERSE_DISTANCE_WEIGHTING: Multi-station IDW catchment rainfall aggregation.

Audit Record Fields:
- source_spatial_unit
- target_spatial_unit
- matching_method
- distance_km
- match_quality (HIGH, MODERATE, LOW, UNMATCHED)
"""

from typing import Dict, Any, List, Optional, Tuple
from math import radians, cos, sin, asin, sqrt
import pandas as pd
import numpy as np


def haversine_km(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Computes great circle distance between two points in kilometers."""
    R = 6371.0
    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)
    a = sin(dlat / 2.0) ** 2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon / 2.0) ** 2
    c = 2.0 * asin(sqrt(a))
    return R * c


class GeospatialAligner:
    """
    Executes hierarchical spatial alignment between flood event geometries and telemetry sensors.
    """

    def __init__(
        self,
        rainfall_stations_df: pd.DataFrame,
        lat_col: str = "Latitude",
        lon_col: str = "Longitude",
        station_id_col: str = "Station",
        district_col: str = "District"
    ):
        self.rain_stations = rainfall_stations_df.drop_duplicates(subset=[station_id_col]).dropna(subset=[lat_col, lon_col]).copy()
        self.lat_col = lat_col
        self.lon_col = lon_col
        self.id_col = station_id_col
        self.dist_col = district_col

    def match_gauge_to_rainfall_network(
        self,
        gauge_name: str,
        gauge_lat: float,
        gauge_lon: float,
        gauge_district: Optional[str] = None,
        max_search_dist_km: float = 100.0
    ) -> Dict[str, Any]:
        """
        Executes hierarchical spatial matching for a river gauge:
        - 1. Same district matching
        - 2. Nearest station within threshold
        - 3. Quality scoring based on proximity
        """
        if self.rain_stations.empty:
            return {
                "source_spatial_unit": gauge_name,
                "target_spatial_unit": None,
                "matching_method": "NO_STATIONS_AVAILABLE",
                "distance_km": None,
                "match_quality": "UNMATCHED"
            }

        station_distances = []
        for _, row in self.rain_stations.iterrows():
            st_lat = float(row[self.lat_col])
            st_lon = float(row[self.lon_col])
            st_id = str(row[self.id_col])
            st_dist = str(row.get(self.dist_col, "")).strip().upper()

            d = haversine_km(gauge_lat, gauge_lon, st_lat, st_lon)
            if d <= max_search_dist_km:
                station_distances.append({
                    "station": st_id,
                    "district": st_dist,
                    "distance_km": round(d, 2),
                    "is_same_district": bool(gauge_district and st_dist == gauge_district.strip().upper())
                })

        station_distances.sort(key=lambda x: x["distance_km"])

        if not station_distances:
            return {
                "source_spatial_unit": gauge_name,
                "target_spatial_unit": None,
                "matching_method": "EXCEEDED_MAX_DISTANCE",
                "distance_km": None,
                "match_quality": "UNMATCHED"
            }

        closest = station_distances[0]
        dist_km = closest["distance_km"]

        # Determine quality tier
        if dist_km <= 25.0:
            quality = "HIGH"
        elif dist_km <= 60.0:
            quality = "MODERATE"
        else:
            quality = "LOW"

        method = "SAME_DISTRICT_PROXIMITY" if closest["is_same_district"] else "NEAREST_STATION_CATCHMENT"

        return {
            "source_spatial_unit": gauge_name,
            "target_spatial_unit": closest["station"],
            "target_district": closest["district"],
            "matching_method": method,
            "distance_km": dist_km,
            "match_quality": quality,
            "k_nearest_candidates": station_distances[:4]
        }

    def compute_idw_catchment_rainfall(
        self,
        target_lat: float,
        target_lon: float,
        station_rainfall_map: Dict[str, float],
        k: int = 4,
        power: float = 2.0,
        max_dist_km: float = 80.0
    ) -> Optional[float]:
        """
        Computes interpolated catchment precipitation at target location using IDW.
        """
        station_dists = []
        for _, row in self.rain_stations.iterrows():
            st_lat = float(row[self.lat_col])
            st_lon = float(row[self.lon_col])
            st_id = str(row[self.id_col])
            d = haversine_km(target_lat, target_lon, st_lat, st_lon)
            if d <= max_dist_km:
                station_dists.append((st_id, d))

        station_dists.sort(key=lambda x: x[1])

        valid_pairs = []
        for st_id, d in station_dists[:k]:
            if st_id in station_rainfall_map and station_rainfall_map[st_id] is not None:
                d_eff = max(d, 0.1)
                valid_pairs.append((station_rainfall_map[st_id], d_eff))

        if not valid_pairs:
            return None

        weights = [1.0 / (d ** power) for _, d in valid_pairs]
        weighted_sum = sum(rf * w for (rf, _), w in zip(valid_pairs, weights))
        total_weight = sum(weights)

        if total_weight == 0:
            return None

        return round(weighted_sum / total_weight, 3)
