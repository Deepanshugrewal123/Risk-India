"""
RISK // INDIA — Weather Temporal Integrity & Ingestion Lifecycle
=================================================================
Maintains chronological ordering, instant deduplication, out-of-order packet
insertion, and explicit temporal separation between observation and ingestion.
"""

from typing import Dict, List, Set, Tuple, Optional
import bisect
import threading
import logging

from .schema import (
    CanonicalWeatherObservation,
    CanonicalWeatherForecast,
    WeatherWarning,
    QualityRejectionReason
)

logger = logging.getLogger("weather-temporal-manager")


class WeatherTemporalManager:
    """
    Manages observations, forecasts, and warnings per geographic region.
    Guarantees chronological ordering and duplicate detection.
    """

    def __init__(self):
        self._lock = threading.RLock()
        # Key: region_id -> List of observations ordered by observed_at
        self._observations: Dict[str, List[CanonicalWeatherObservation]] = {}
        # Key: (region_id, horizon) -> CanonicalWeatherForecast
        self._forecasts: Dict[Tuple[str, str], CanonicalWeatherForecast] = {}
        # Key: region_id -> List of WeatherWarning
        self._warnings: Dict[str, List[WeatherWarning]] = {}
        # Seen IDs for deduplication
        self._seen_ids: Set[str] = set()

    def add_observation(self, obs: CanonicalWeatherObservation) -> Tuple[bool, Optional[str]]:
        """Inserts an observation in chronological sequence."""
        with self._lock:
            if obs.observation_id in self._seen_ids:
                return False, QualityRejectionReason.DUPLICATE_RECORD.value

            rid = obs.region_id.upper()
            if rid not in self._observations:
                self._observations[rid] = []

            obs_list = self._observations[rid]
            timestamps = [item.observed_at for item in obs_list]
            idx = bisect.bisect_right(timestamps, obs.observed_at)
            obs_list.insert(idx, obs)

            self._seen_ids.add(obs.observation_id)
            return True, None

    def add_forecast(self, fc: CanonicalWeatherForecast) -> Tuple[bool, Optional[str]]:
        """Stores a weather forecast indexed by region and horizon."""
        with self._lock:
            if fc.forecast_id in self._seen_ids:
                return False, QualityRejectionReason.DUPLICATE_RECORD.value

            key = (fc.region_id.upper(), fc.forecast_horizon.upper())
            self._forecasts[key] = fc
            self._seen_ids.add(fc.forecast_id)
            return True, None

    def add_warning(self, warn: WeatherWarning) -> Tuple[bool, Optional[str]]:
        """Stores a weather warning for a region."""
        with self._lock:
            if warn.warning_id in self._seen_ids:
                return False, QualityRejectionReason.DUPLICATE_RECORD.value

            rid = warn.affected_region.upper()
            if rid not in self._warnings:
                self._warnings[rid] = []

            self._warnings[rid].append(warn)
            self._seen_ids.add(warn.warning_id)
            return True, None

    def get_observations(self, region_id: str, limit: int = 100) -> List[CanonicalWeatherObservation]:
        with self._lock:
            rid = region_id.upper()
            return list(self._observations.get(rid, []))[-limit:]

    def get_latest_observation(self, region_id: str) -> Optional[CanonicalWeatherObservation]:
        with self._lock:
            rid = region_id.upper()
            obs_list = self._observations.get(rid, [])
            return obs_list[-1] if obs_list else None

    def get_forecasts(self, region_id: str) -> List[CanonicalWeatherForecast]:
        with self._lock:
            rid = region_id.upper()
            results = []
            for (r, h), fc in self._forecasts.items():
                if r == rid:
                    results.append(fc)
            return results

    def get_forecast(self, region_id: str, horizon: str) -> Optional[CanonicalWeatherForecast]:
        with self._lock:
            key = (region_id.upper(), horizon.upper())
            return self._forecasts.get(key)

    def get_warnings(self, region_id: Optional[str] = None) -> List[WeatherWarning]:
        with self._lock:
            if region_id:
                return list(self._warnings.get(region_id.upper(), []))
            all_w = []
            for w_list in self._warnings.values():
                all_w.extend(w_list)
            return all_w

    def get_total_observations(self) -> int:
        with self._lock:
            return sum(len(l) for l in self._observations.values())

    def get_total_forecasts(self) -> int:
        with self._lock:
            return len(self._forecasts)

    def get_total_warnings(self) -> int:
        with self._lock:
            return sum(len(l) for l in self._warnings.values())

    def clear(self):
        """Resets all data (used in testing)."""
        with self._lock:
            self._observations.clear()
            self._forecasts.clear()
            self._warnings.clear()
            self._seen_ids.clear()


weather_temporal_manager = WeatherTemporalManager()
