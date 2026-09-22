"""
RISK // INDIA — National Freshness Engine
========================================
Deterministically evaluates observation and intelligence freshness independently
from risk severity. A high-risk stale observation remains STALE, never converted to LIVE.
"""

from enum import Enum
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from typing import Optional, Dict, Any, Union
import logging

logger = logging.getLogger("national-freshness-engine")


class FreshnessClassification(str, Enum):
    OFFICIAL_LIVE = "OFFICIAL_LIVE"
    OFFICIAL_RECENT = "OFFICIAL_RECENT"
    CACHED = "CACHED"
    STALE = "STALE"
    REGIONAL_BASELINE = "REGIONAL_BASELINE"
    EMPIRICAL_ML = "EMPIRICAL_ML"
    UNAVAILABLE = "UNAVAILABLE"


@dataclass
class FreshnessRecord:
    observed_at: Optional[str]
    fetched_at: str
    source: str
    source_record_id: Optional[str]
    freshness_state: str
    age_seconds: Optional[float]
    age_minutes: Optional[float]
    provider_status: str

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class FreshnessEngine:
    """Evaluates freshness strictly decoupled from risk severity."""

    # Thresholds in seconds
    LIVE_THRESHOLD_SECONDS = 3600.0      # 1 hour
    RECENT_THRESHOLD_SECONDS = 86400.0   # 24 hours

    def parse_timestamp(self, ts: Optional[Union[str, datetime]]) -> Optional[datetime]:
        """Parses ISO 8601 string or datetime into UTC datetime."""
        if not ts:
            return None
        if isinstance(ts, datetime):
            if ts.tzinfo is None:
                return ts.replace(tzinfo=timezone.utc)
            return ts.astimezone(timezone.utc)
        if isinstance(ts, str):
            try:
                clean_ts = ts.strip().replace("Z", "+00:00")
                dt = datetime.fromisoformat(clean_ts)
                if dt.tzinfo is None:
                    return dt.replace(tzinfo=timezone.utc)
                return dt.astimezone(timezone.utc)
            except Exception:
                return None
        return None

    def classify_freshness(
        self,
        observed_at: Optional[Union[str, datetime]],
        fetched_at: Optional[Union[str, datetime]] = None,
        is_cached: bool = False,
        provider_status: str = "OPERATIONAL",
        source: str = "Official Source",
        source_record_id: Optional[str] = None,
        is_baseline: bool = False,
        is_empirical_ml: bool = False
    ) -> FreshnessRecord:
        """
        Deterministically classifies data freshness.
        Crucial: Freshness is strictly evaluated independently of risk severity.
        """
        now_utc = datetime.now(timezone.utc)
        fetched_dt = self.parse_timestamp(fetched_at) or now_utc
        fetched_str = fetched_dt.isoformat()

        if is_baseline:
            return FreshnessRecord(
                observed_at=None,
                fetched_at=fetched_str,
                source=source,
                source_record_id=source_record_id,
                freshness_state=FreshnessClassification.REGIONAL_BASELINE.value,
                age_seconds=None,
                age_minutes=None,
                provider_status=provider_status
            )

        if is_empirical_ml:
            return FreshnessRecord(
                observed_at=None,
                fetched_at=fetched_str,
                source="assam_flood_prototype_v1",
                source_record_id=source_record_id,
                freshness_state=FreshnessClassification.EMPIRICAL_ML.value,
                age_seconds=None,
                age_minutes=None,
                provider_status=provider_status
            )

        obs_dt = self.parse_timestamp(observed_at)
        if not obs_dt:
            state = FreshnessClassification.CACHED.value if is_cached else FreshnessClassification.UNAVAILABLE.value
            return FreshnessRecord(
                observed_at=None,
                fetched_at=fetched_str,
                source=source,
                source_record_id=source_record_id,
                freshness_state=state,
                age_seconds=None,
                age_minutes=None,
                provider_status=provider_status
            )

        # Elapsed seconds between observation and current UTC time
        age_seconds = max(0.0, (now_utc - obs_dt).total_seconds())
        age_minutes = round(age_seconds / 60.0, 1)
        obs_str = obs_dt.isoformat()

        # Cached fallback rule: cached data is never labeled LIVE
        if is_cached:
            if age_seconds >= self.RECENT_THRESHOLD_SECONDS:
                state = FreshnessClassification.STALE.value
            else:
                state = FreshnessClassification.CACHED.value
        elif age_seconds < self.LIVE_THRESHOLD_SECONDS:
            state = FreshnessClassification.OFFICIAL_LIVE.value
        elif age_seconds < self.RECENT_THRESHOLD_SECONDS:
            state = FreshnessClassification.OFFICIAL_RECENT.value
        else:
            state = FreshnessClassification.STALE.value

        return FreshnessRecord(
            observed_at=obs_str,
            fetched_at=fetched_str,
            source=source,
            source_record_id=source_record_id,
            freshness_state=state,
            age_seconds=round(age_seconds, 1),
            age_minutes=age_minutes,
            provider_status=provider_status
        )


freshness_engine = FreshnessEngine()
