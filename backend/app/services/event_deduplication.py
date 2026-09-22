"""
RISK // INDIA — Deterministic Event Deduplication Engine
=========================================================
Prevents duplicate ingestion and presentation of multi-source disaster events
while maintaining strict provenance, timestamps, and confidence.
"""

from typing import List, Dict, Any, Optional, Tuple, Set
from datetime import datetime, timezone, timedelta
import math
import logging

logger = logging.getLogger("event-deduplication")

TEMPORAL_TOLERANCE_HOURS: Dict[str, float] = {
    "EARTHQUAKE": 1.5,
    "FLOOD": 12.0,
    "CYCLONE": 6.0,
    "LANDSLIDE": 8.0,
    "HEATWAVE": 24.0,
    "LIGHTNING": 2.0,
    "TSUNAMI": 3.0,
    "HEAVY_RAINFALL": 6.0,
    "DROUGHT": 72.0,
    "OTHER": 6.0,
}

SPATIAL_TOLERANCE_KM = 25.0


def haversine_distance_km(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    r = 6371.0
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)
    a = (
        math.sin(delta_phi / 2.0) ** 2
        + math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2.0) ** 2
    )
    c = 2.0 * math.atan2(math.sqrt(a), math.sqrt(1.0 - a))
    return r * c


class EventDeduplicator:
    @staticmethod
    def are_near_duplicates(ev1: Any, ev2: Any) -> bool:
        h1 = getattr(ev1, "hazard_type", "").upper()
        h2 = getattr(ev2, "hazard_type", "").upper()
        if h1 != h2:
            return False

        id1 = getattr(ev1, "id", None)
        id2 = getattr(ev2, "id", None)
        if id1 and id2 and id1 == id2:
            return True

        src_id1 = getattr(ev1, "source_event_id", None)
        src_id2 = getattr(ev2, "source_event_id", None)
        if src_id1 and src_id2 and src_id1 == src_id2:
            return True

        t1 = getattr(ev1, "observed_at", None)
        t2 = getattr(ev2, "observed_at", None)
        if t1 and t2:
            if t1.tzinfo is None:
                t1 = t1.replace(tzinfo=timezone.utc)
            if t2.tzinfo is None:
                t2 = t2.replace(tzinfo=timezone.utc)
            time_diff_hours = abs((t1 - t2).total_seconds()) / 3600.0
            allowed_hours = TEMPORAL_TOLERANCE_HOURS.get(h1, 6.0)
            if time_diff_hours > allowed_hours:
                return False

        lat1, lon1 = getattr(ev1, "latitude", None), getattr(ev1, "longitude", None)
        lat2, lon2 = getattr(ev2, "latitude", None), getattr(ev2, "longitude", None)

        if lat1 is not None and lon1 is not None and lat2 is not None and lon2 is not None:
            dist_km = haversine_distance_km(lat1, lon1, lat2, lon2)
            if dist_km <= SPATIAL_TOLERANCE_KM:
                return True

        st1 = (getattr(ev1, "state", "") or "").lower().strip()
        st2 = (getattr(ev2, "state", "") or "").lower().strip()
        d1 = (getattr(ev1, "district", "") or "").lower().strip()
        d2 = (getattr(ev2, "district", "") or "").lower().strip()

        if st1 and st2 and st1 == st2 and d1 and d2 and d1 == d2:
            return True

        return False

    @staticmethod
    def merge_events(primary: Any, secondary: Any) -> Any:
        src1 = getattr(primary, "source", "")
        src2 = getattr(secondary, "source", "")
        if src2 and src2 not in src1:
            primary.source = f"{src1} / {src2}"

        if not getattr(primary, "verified", False) and getattr(secondary, "verified", False):
            primary.verified = True
            primary.is_demo = False

        if not getattr(primary, "basin", None) and getattr(secondary, "basin", None):
            primary.basin = secondary.basin

        severity_rank = {"CRITICAL": 4, "HIGH": 3, "MODERATE": 2, "LOW": 1}
        s1 = getattr(primary, "severity", "LOW").upper()
        s2 = getattr(secondary, "severity", "LOW").upper()
        if severity_rank.get(s2, 0) > severity_rank.get(s1, 0):
            primary.severity = secondary.severity
            if getattr(secondary, "risk_score", None):
                primary.risk_score = secondary.risk_score

        return primary

    @classmethod
    def deduplicate(cls, events: List[Any]) -> Tuple[List[Any], Dict[str, int]]:
        initial_count = len(events)
        if initial_count <= 1:
            return events, {"initial": initial_count, "deduped": initial_count, "duplicates_removed": 0}

        deduped: List[Any] = []
        seen_identifiers: Set[str] = set()

        for ev in events:
            ev_id = getattr(ev, "id", None)
            src_ev_id = getattr(ev, "source_event_id", None)

            if ev_id and ev_id in seen_identifiers:
                continue
            if src_ev_id and src_ev_id in seen_identifiers:
                continue

            merged = False
            for existing in deduped:
                if cls.are_near_duplicates(existing, ev):
                    cls.merge_events(existing, ev)
                    merged = True
                    break

            if not merged:
                deduped.append(ev)
                if ev_id:
                    seen_identifiers.add(ev_id)
                if src_ev_id:
                    seen_identifiers.add(src_ev_id)

        stats = {
            "initial": initial_count,
            "deduped": len(deduped),
            "duplicates_removed": initial_count - len(deduped),
        }
        return deduped, stats
