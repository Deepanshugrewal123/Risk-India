"""
RISK // INDIA — Temporal Telemetry Manager & Historical Sequencing
===================================================================
Manages chronological sequencing of observations per gauge, handles
out-of-order and late-arriving packets, and executes instant deduplication.
"""

from typing import Dict, List, Set, Tuple, Optional
import bisect
import threading
from datetime import datetime, timezone
import logging

from .schema import HydrologicalObservation, QualityRejectionReason

logger = logging.getLogger("telemetry-temporal-manager")


class TemporalTelemetryManager:
    """
    Maintains temporally ordered observation series indexed by station and variable.
    Ensures deterministic ordering and duplicate rejection.
    """

    def __init__(self):
        self._lock = threading.RLock()
        # Key: (gauge_id, variable_type) -> List[HydrologicalObservation] sorted by observed_at
        self._series: Dict[Tuple[str, str], List[HydrologicalObservation]] = {}
        # Seen observation IDs for instant deduplication
        self._seen_ids: Set[str] = set()

    def add_observation(self, obs: HydrologicalObservation) -> Tuple[bool, Optional[str]]:
        """
        Attempts to insert an observation chronologically into its series.
        Returns (success, rejection_reason).
        """
        with self._lock:
            # Gate 8: Duplicate observation check
            if obs.observation_id in self._seen_ids:
                return False, QualityRejectionReason.DUPLICATE_OBSERVATION.value

            series_key = (obs.gauge_id.strip().upper(), obs.variable_type.strip().upper())
            if series_key not in self._series:
                self._series[series_key] = []

            obs_list = self._series[series_key]

            # Binary search for chronological insertion
            # Keys are ISO 8601 strings (lexicographically ordered)
            timestamps = [item.observed_at for item in obs_list]
            idx = bisect.bisect_right(timestamps, obs.observed_at)
            obs_list.insert(idx, obs)

            self._seen_ids.add(obs.observation_id)
            return True, None

    def get_series(
        self,
        gauge_id: str,
        variable_type: Optional[str] = None,
        limit: int = 100
    ) -> List[HydrologicalObservation]:
        """Returns observation series for a gauge ordered chronologically ascending."""
        with self._lock:
            clean_gid = gauge_id.strip().upper()
            results = []
            if variable_type:
                key = (clean_gid, variable_type.strip().upper())
                results = list(self._series.get(key, []))
            else:
                for (gid, _), obs_list in self._series.items():
                    if gid == clean_gid:
                        results.extend(obs_list)
                results.sort(key=lambda x: x.observed_at)

            return results[-limit:] if limit else results

    def get_latest(
        self,
        gauge_id: str,
        variable_type: Optional[str] = None
    ) -> Optional[HydrologicalObservation]:
        """Returns the most recent observation for a gauge."""
        with self._lock:
            clean_gid = gauge_id.strip().upper()
            candidates: List[HydrologicalObservation] = []
            if variable_type:
                key = (clean_gid, variable_type.strip().upper())
                obs_list = self._series.get(key, [])
                if obs_list:
                    return obs_list[-1]
                return None
            else:
                for (gid, _), obs_list in self._series.items():
                    if gid == clean_gid and obs_list:
                        candidates.append(obs_list[-1])
                if not candidates:
                    return None
                candidates.sort(key=lambda x: x.observed_at)
                return candidates[-1]

    def get_total_count(self) -> int:
        with self._lock:
            return len(self._seen_ids)

    def clear(self):
        """Resets all temporal series (used in testing)."""
        with self._lock:
            self._series.clear()
            self._seen_ids.clear()


temporal_telemetry_manager = TemporalTelemetryManager()
