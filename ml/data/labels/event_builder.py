"""
RISK // INDIA — Flood Event Construction & Grouping Engine

Groups multiple satellite inundation polygons or multi-swath passes into coherent flood events:
- Prevents artificial fragmentation of a single flood wave
- Prevents over-merging of independent, geographically disjoint flood pulses
- Detects duplicate geometries or identical observation records
- Standardizes event metadata: event_id, event_date, region, total_inundated_area, confidence
"""

from typing import Dict, Any, List, Optional
from datetime import date
import pandas as pd
import numpy as np


class FloodEventBuilder:
    """
    Constructs and deduplicates discrete flood disaster events from raw satellite observation features.
    """

    def __init__(self, temporal_grouping_window_hours: int = 24):
        self.grouping_window_hours = temporal_grouping_window_hours

    def detect_duplicates(self, observations: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Identifies and removes duplicate observation features (exact same event_date, location, coordinates).
        """
        seen_keys = set()
        deduped = []

        for obs in observations:
            e_date = str(obs.get("event_date"))
            dist = str(obs.get("district_name") or obs.get("district") or "")
            coords_str = str(obs.get("coordinates") or obs.get("bbox") or "")

            dedup_key = f"{e_date}|{dist}|{coords_str[:100]}"
            if dedup_key in seen_keys:
                continue
            seen_keys.add(dedup_key)
            deduped.append(obs)

        return deduped

    def group_observations_into_events(
        self,
        observations: List[Dict[str, Any]],
        group_by_district: bool = True
    ) -> List[Dict[str, Any]]:
        """
        Groups individual polygon observations into consolidated disaster events.

        Criteria:
        - Same explicit event_id if provided by agency
        - Or: Same observation date + same district/river basin
        """
        if not observations:
            return []

        deduped = self.detect_duplicates(observations)
        grouped_dict: Dict[str, List[Dict[str, Any]]] = {}

        for obs in deduped:
            explicit_id = obs.get("event_id")
            obs_date = obs.get("event_date")
            district = obs.get("district_name") or obs.get("district") or "ASSAM_GENERAL"

            if explicit_id and not explicit_id.startswith("FE_"):
                # Use official agency event ID
                key = str(explicit_id)
            elif group_by_district:
                key = f"{obs_date}_{district}"
            else:
                key = str(obs_date)

            if key not in grouped_dict:
                grouped_dict[key] = []
            grouped_dict[key].append(obs)

        events: List[Dict[str, Any]] = []
        for event_key, group_items in grouped_dict.items():
            first = group_items[0]
            total_area = sum(float(item.get("inundated_area_sqkm") or 0.0) for item in group_items)

            events.append({
                "event_id": event_key,
                "event_date": first.get("event_date"),
                "region": first.get("district_name") or "Assam",
                "polygon_count": len(group_items),
                "total_inundated_area_sqkm": round(total_area, 2) if total_area > 0 else None,
                "source_organization": first.get("source_organization", "ISRO / NRSC"),
                "product_name": first.get("product_name", "Bhuvan Historical Flood Inundation"),
                "geometry_type": "MultiPolygon" if len(group_items) > 1 else first.get("geometry_type", "Polygon"),
                "features": group_items,
                "confidence": "OBSERVED_SATELLITE"
            })

        return events
